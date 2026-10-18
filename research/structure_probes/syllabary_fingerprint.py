"""E13 - Syllabary fingerprint (Kober-grid test).

Pre-registered question
  In a consonant-vowel syllabary used for an inflected language, signs that share a
  consonant alternate with one another after the same stem (Kober's triplets). The
  sign-alternation graph then splits into many small classes. In an alphabet the same
  graph has few large classes (vowels alternate with vowels). Under free combination
  of parts there is no class structure beyond chance. Which of the three does the
  Voynich alternation graph resemble, under three pre-stated segmentations?

Procedure (fixed before running)
  1. Word types only (no token weighting), length >= STEM + 1 units.
  2. Stem = first STEM units (primary STEM=2, secondary STEM=3). The sign that follows
     the stem is the "junction sign". For every stem with >= 2 distinct junction signs
     and every unordered pair {X, Y} of them, A[X, Y] += 1 (counting stems).
     The mirrored analysis (stem = last STEM units, junction sign before it) is also run.
  3. Nodes = signs with weighted degree >= MIN_DEGREE in the observed graph.
  4. Statistics: modularity Q of the greedy (CNM) partition; number of communities of
     size >= 2; share of nodes in the largest community; concentration = share of the
     total alternation weight carried by the top 10% of node pairs.
  5. Null: permute the junction-sign column over the list of distinct (stem, sign)
     pairs, keeping each stem's fan-out and each sign's overall frequency; duplicates
     created within a stem are dropped. PERMUTATIONS = 499, seed 20261018. Statistics
     are recomputed on the observed node set.
  6. Controls: Latin letters and Italian letters (alphabets), Latin in a mock CV
     syllabary (positive control for grid structure), Seraphinianus OCR (invented script).
     Where true classes are known (consonant of each CV sign; vowel/consonant of each
     letter) purity and NMI of the found partition are reported.
  7. Primary comparison uses the same number of word types in every corpus
     (the minimum, sampled with the seed); full-corpus values are secondary.

Decision rules (fixed before running)
  syllabary-like: Q above the null (p < 0.01) AND >= 6 communities AND largest
                  community <= 25% of nodes, with the CV control showing the same
                  pattern and purity against consonant classes >= 0.6;
  alphabet-like:  Q above the null AND <= 3 communities with one holding >= 40% of nodes;
  free-combination-like: Q not above the null (p >= 0.05).
  Anything else is reported as "mixed / not classifiable by this test".
"""
import collections
import itertools
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

SEED = 20261018
PERMUTATIONS = 499
MIN_DEGREE = 5
STEMS = (2, 3)
OUT = Path(__file__).resolve().parent / 'syllabary_fingerprint_results.json'


def word_types(seq_list, min_len):
    types = {}
    for seq in seq_list:
        if len(seq) >= min_len:
            types[tuple(seq)] = None
    return list(types)


def build_corpora():
    rows = C.voynich_rows()
    vwords = [w for _, ws in rows for w in ws]
    corpora = {}
    for seg in ('eva', 'units23', 'units23_qo_in'):
        corpora['Voynich_' + seg] = {'seqs': [C.tokenize(w, seg) for w in vwords], 'classes': None}
    corpora['Seraphinianus_OCR'] = {'seqs': [list(w) for _, ws in C.seraph_rows() for w in ws], 'classes': None}
    lat = C.latin_words()
    corpora['Latin_letters'] = {'seqs': [list(w) for w in lat], 'classes': C.sign_class_letter}
    corpora['Italian_letters'] = {'seqs': [list(w) for w in C.italian_words()], 'classes': C.sign_class_letter}
    corpora['Latin_CV_syllabary'] = {'seqs': [C.cv_syllabary(w) for w in lat], 'classes': C.sign_class_cv}
    return corpora


def alternation_pairs(types, stem_len, mirrored):
    """Distinct (stem, junction sign) pairs."""
    pairs = set()
    for t in types:
        if mirrored:
            stem, sign = t[-stem_len:], t[-stem_len - 1]
        else:
            stem, sign = t[:stem_len], t[stem_len]
        pairs.add((stem, sign))
    return sorted(pairs)


def graph_from_pairs(pairs, nodes_index):
    by_stem = collections.defaultdict(set)
    for stem, sign in pairs:
        if sign in nodes_index:
            by_stem[stem].add(sign)
    n = len(nodes_index)
    W = np.zeros((n, n))
    for signs in by_stem.values():
        if len(signs) < 2:
            continue
        for x, y in itertools.combinations(sorted(signs), 2):
            i, j = nodes_index[x], nodes_index[y]
            W[i, j] += 1
            W[j, i] += 1
    return W


def stats(W):
    part, q = C.greedy_modularity(W)
    sizes = sorted((len(c) for c in part), reverse=True)
    n = len(W)
    tri = W[np.triu_indices(n, 1)]
    top = max(1, int(round(0.1 * len(tri))))
    conc = float(np.sort(tri)[::-1][:top].sum() / tri.sum()) if tri.sum() else 0.0
    return {'Q': q, 'communities_ge2': sum(1 for s in sizes if s >= 2), 'largest_share': sizes[0] / n if n else 0,
            'concentration_top10': conc, 'partition': part}


def analyse(name, types, classes_fn, stem_len, mirrored, rng):
    pairs = alternation_pairs(types, stem_len, mirrored)
    # observed node set
    deg = collections.Counter()
    by_stem = collections.defaultdict(set)
    for stem, sign in pairs:
        by_stem[stem].add(sign)
    for signs in by_stem.values():
        for x, y in itertools.combinations(sorted(signs), 2):
            deg[x] += 1
            deg[y] += 1
    nodes = sorted(s for s, d in deg.items() if d >= MIN_DEGREE)
    index = {s: i for i, s in enumerate(nodes)}
    if len(nodes) < 4:
        return {'nodes': len(nodes), 'skipped': 'fewer than 4 nodes'}
    W = graph_from_pairs(pairs, index)
    obs = stats(W)
    null = collections.defaultdict(list)
    stems = [p[0] for p in pairs]
    signs = [p[1] for p in pairs]
    for _ in range(PERMUTATIONS):
        rng.shuffle(signs)
        Wn = graph_from_pairs(list(zip(stems, signs)), index)
        s = stats(Wn)
        for k in ('Q', 'communities_ge2', 'largest_share', 'concentration_top10'):
            null[k].append(s[k])
    out = {'nodes': len(nodes), 'word_types': len(types), 'stems': len(by_stem),
           'alternation_weight': float(W.sum() / 2), 'signs': nodes,
           'communities': [[nodes[i] for i in comm] for comm in obs['partition']]}
    for k in ('Q', 'concentration_top10'):
        out[k] = C.summarize_null(obs[k], null[k], larger_is_extreme=True)
    for k in ('communities_ge2', 'largest_share'):
        out[k] = {'observed': obs[k], 'null_mean': float(np.mean(null[k])),
                  'null_min': float(np.min(null[k])), 'null_max': float(np.max(null[k]))}
    if classes_fn:
        classes = [classes_fn(s) for s in nodes]
        pur, nmi = C.purity_nmi(obs['partition'], classes)
        out['purity_vs_true_classes'] = pur
        out['nmi_vs_true_classes'] = nmi
        out['true_classes'] = sorted(set(classes))
    out['verdict'] = verdict(out, classes_fn is C.sign_class_cv)
    return out


def verdict(r, is_cv_control):
    q_sig = r['Q']['p_empirical'] < 0.01
    ncomm = r['communities_ge2']['observed']
    big = r['largest_share']['observed']
    if r['Q']['p_empirical'] >= 0.05:
        return 'free-combination-like (Q not above null)'
    if q_sig and ncomm >= 6 and big <= 0.25:
        return 'syllabary-like (many small classes)'
    if q_sig and ncomm <= 3 and big >= 0.40:
        return 'alphabet-like (few large classes)'
    return 'mixed / not classifiable by this test'


def main():
    t0 = time.time()
    corpora = build_corpora()
    results = {'experiment': 'E13 syllabary fingerprint', 'seed': SEED, 'permutations': PERMUTATIONS,
               'min_degree': MIN_DEGREE, 'analyses': {}}
    for stem_len in STEMS:
        min_len = stem_len + 1
        typed = {name: word_types(c['seqs'], min_len) for name, c in corpora.items()}
        n_match = min(len(t) for t in typed.values())
        results['analyses'][f'stem{stem_len}'] = {'matched_word_types': n_match, 'full': {}, 'matched': {}}
        for mode in ('matched', 'full'):
            for name, c in corpora.items():
                rng = random.Random(SEED)
                types = typed[name]
                if mode == 'matched':
                    types = rng.sample(types, n_match)
                for mirrored in (False, True):
                    key = name + ('_mirrored' if mirrored else '')
                    results['analyses'][f'stem{stem_len}'][mode][key] = analyse(
                        name, types, c['classes'], stem_len, mirrored, random.Random(SEED + stem_len))
                    print(f'stem{stem_len} {mode:7s} {key:36s} '
                          + json.dumps({k: results['analyses'][f'stem{stem_len}'][mode][key].get(k)
                                        for k in ('nodes', 'verdict')}), flush=True)
    results['runtime_seconds'] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(results, indent=1))
    print('written', OUT)


if __name__ == '__main__':
    main()
