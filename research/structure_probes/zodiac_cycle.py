"""E14 - Zodiac labels as a cycle.

Pre-registered question
  Each zodiac sign carries about thirty figures, each with a label. If the labels
  were a cyclic numbering (degrees, days), the same label types would recur across
  signs, labels at the same position in different signs would resemble one another,
  and angularly adjacent labels within a sign would resemble one another as
  consecutive numerals do. If they were names, none of this would hold.

Data
  Lz labels on the twelve $I=Z pages of ZL3b. Reading policy as elsewhere: first
  alternative of [x:y]; labels containing ?, @nnn; or {..} are excluded from the
  similarity tests (counted separately). Labels are compared as sequences of
  units23 tokens; multi-word labels keep a '.' boundary token.

Tests (fixed before running)
  B1 cross-sign repetition: share of clean single-word labels whose type occurs on
     >= 2 zodiac pages; same statistic for other label families (pharmaceutical Lf,
     cosmological L0, star Ls, nymph Ln) and for 999 samples of running-text blocks
     of the same sizes drawn from 12 random paragraph pages.
  B2 cross-sign positional alignment: labels ordered by (ring, clock angle); pages
     compared pairwise when their label counts differ by <= 3; labels paired by
     normalised rank; statistic = mean normalised edit distance, minimised over cyclic
     rotations and reading direction. Null: 999 random permutations of the second
     page's labels, same minimisation. Reported per pair and pooled.
  B3 within-ring adjacency: mean normalised edit distance between angularly adjacent
     labels (cyclic) in rings with >= 4 labels, pooled; null: 999 within-ring
     permutations.
  B4 descriptive: label length, initial glyph, share of labels that also occur as
     running-text words.
  Positive controls: twelve "signs" each labelled 1-30 with Latin cardinals and,
     separately, with Roman numerals (a counting cycle); names control: 12 x 30
     distinct Latin word types. All run through B1-B3 with the same code.

Decision rules (fixed before running)
  cycle-like:  B1 well above the running-text baseline AND (B2 p < 0.01 pooled OR
               B3 p < 0.01 pooled), with the numeral controls passing the same tests;
  names-like:  B1 at or below the baseline of other label families AND B2, B3 not
               significant;
  otherwise:   mixed. A positive B3 alone is also compatible with copy-with-drift
               production and is not read as evidence of numbering.
"""
import collections
import json
import random
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

SEED = 20261018
PERMUTATIONS = 999
OUT = Path(__file__).resolve().parent / 'zodiac_cycle_results.json'
SIGN = {'f70v2': 'Pisces', 'f70v1': 'Aries (dark)', 'f71r': 'Aries (light)', 'f71v': 'Taurus (light)',
        'f72r1': 'Taurus (dark)', 'f72r2': 'Gemini', 'f72r3': 'Cancer', 'f72v3': 'Leo', 'f72v2': 'Virgo',
        'f72v1': 'Libra', 'f73r': 'Scorpio', 'f73v': 'Sagittarius'}


def units(label_words):
    seq = []
    for i, w in enumerate(label_words):
        if i:
            seq.append('.')
        seq.extend(C.tokenize(w, 'units23'))
    return seq


# ------------------------------------------------------------------ B1

def repetition(groups):
    """groups: {group_id: [label strings]} -> cross-group repetition statistics."""
    where = collections.defaultdict(set)
    total = 0
    for g, labs in groups.items():
        for lab in labs:
            where[lab].add(g)
            total += 1
    types_multi = {lab for lab, gs in where.items() if len(gs) >= 2}
    labels_recurring = sum(1 for labs in groups.values() for lab in labs if lab in types_multi)
    return {'labels': total, 'types': len(where), 'types_on_2plus_groups': len(types_multi),
            'share_of_labels_recurring_elsewhere': labels_recurring / total if total else None,
            'most_repeated': sorted(((lab, len(gs)) for lab, gs in where.items() if len(gs) >= 2),
                                    key=lambda x: -x[1])[:12]}


def text_baseline(rows, sizes, rng, reps):
    by_page = collections.defaultdict(list)
    for p, ws in rows:
        by_page[p].extend(ws)
    pages = [p for p, ws in by_page.items() if len(ws) >= max(sizes) + 1]
    out = []
    for _ in range(reps):
        chosen = rng.sample(pages, len(sizes))
        groups = {}
        for p, n in zip(chosen, sizes):
            ws = by_page[p]
            start = rng.randrange(0, len(ws) - n + 1)
            groups[p] = ws[start:start + n]
        out.append(repetition(groups)['share_of_labels_recurring_elsewhere'])
    return out


# ------------------------------------------------------------------ B2

def align_distance(a, b):
    """Mean normalised edit distance of rank-paired labels, minimised over rotations and direction."""
    n1, n2 = len(a), len(b)
    best = None
    for direction in (1, -1):
        bb = b[::direction]
        for rot in range(n2):
            br = bb[rot:] + bb[:rot]
            d = 0.0
            for i in range(n1):
                j = round(i * (n2 - 1) / (n1 - 1)) if n1 > 1 else 0
                d += C.norm_lev(a[i], br[j])
            d /= n1
            if best is None or d < best:
                best = d
    return best


def plain_distance(a, b):
    n1, n2 = len(a), len(b)
    return float(np.mean([C.norm_lev(a[i], b[round(i * (n2 - 1) / (n1 - 1)) if n1 > 1 else 0]) for i in range(n1)]))


def positional_alignment(sequences, rng, max_diff=3, perms=PERMUTATIONS):
    """sequences: {page: [unit sequences in order]}."""
    pages = sorted(sequences)
    pairs, pooled_obs, pooled_null = [], [], np.zeros(perms)
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            a, b = sequences[pages[i]], sequences[pages[j]]
            if abs(len(a) - len(b)) > max_diff or min(len(a), len(b)) < 4:
                continue
            obs = align_distance(a, b)
            null = []
            for _ in range(perms):
                bp = b[:]
                rng.shuffle(bp)
                null.append(align_distance(a, bp))
            s = C.summarize_null(obs, null, larger_is_extreme=False)
            s.update({'pages': [pages[i], pages[j]], 'plain_rank_distance': plain_distance(a, b)})
            pairs.append(s)
            pooled_obs.append(obs)
            pooled_null += np.array(null)
    if not pairs:
        return {'pairs': [], 'pooled': None}
    pooled = C.summarize_null(float(np.mean(pooled_obs)), pooled_null / len(pairs), larger_is_extreme=False)
    pooled['pairs_tested'] = len(pairs)
    pooled['pairs_p_below_0_05'] = sum(1 for p in pairs if p['p_empirical'] < 0.05)
    return {'pairs': pairs, 'pooled': pooled}


# ------------------------------------------------------------------ B3

def adjacency(rings, rng, perms=PERMUTATIONS):
    """rings: list of lists of unit sequences in angular order (cyclic)."""
    rings = [r for r in rings if len(r) >= 4]

    def mean_adjacent(r):
        return float(np.mean([C.norm_lev(r[k], r[(k + 1) % len(r)]) for k in range(len(r))]))

    obs = float(np.mean([mean_adjacent(r) for r in rings]))
    null = []
    for _ in range(perms):
        vals = []
        for r in rings:
            rp = r[:]
            rng.shuffle(rp)
            vals.append(mean_adjacent(rp))
        null.append(float(np.mean(vals)))
    s = C.summarize_null(obs, null, larger_is_extreme=False)
    s['rings'] = len(rings)
    s['labels'] = sum(len(r) for r in rings)
    return s


# ------------------------------------------------------------------ controls

def control_sets(latin, rng):
    """Return {name: {'groups':..., 'sequences':..., 'rings':...}} for the controls."""
    out = {}
    for name, numerals in (('control_latin_cardinals_1_30', C.LATIN_CARDINALS),
                           ('control_roman_numerals_1_30', C.ROMAN_NUMERALS)):
        seqs = [list(x) for x in numerals]
        out[name] = {'groups': {f'sign{k}': list(numerals) for k in range(12)},
                     'sequences': {f'sign{k}': seqs[:] for k in range(12)},
                     'rings': [seqs[:] for _ in range(12)]}
    types = sorted({w for w in latin if 4 <= len(w) <= 8})
    names = rng.sample(types, 360)
    groups = {f'sign{k}': names[30 * k:30 * (k + 1)] for k in range(12)}
    out['control_distinct_latin_words'] = {'groups': groups,
                                           'sequences': {g: [list(w) for w in ws] for g, ws in groups.items()},
                                           'rings': [[list(w) for w in ws] for ws in groups.values()]}
    return out


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    labs = C.labels(('Lz',), illustration='Z')
    rows = C.voynich_rows()
    text_words = collections.Counter(w for _, ws in rows for w in ws)
    res = {'experiment': 'E14 zodiac cycle', 'seed': SEED, 'permutations': PERMUTATIONS,
           'pages': {p: SIGN.get(p, p) for p in sorted({l['page'] for l in labs})}}

    # inventory
    clean = [l for l in labs if not l['uncertain']]
    single = [l for l in clean if not l['multiword']]
    res['inventory'] = {'labels': len(labs), 'clean_single_word': len(single),
                        'clean_multi_word': sum(1 for l in clean if l['multiword']),
                        'uncertain_or_special': sum(1 for l in labs if l['uncertain']),
                        'without_clock_position': sum(1 for l in labs if l['angle'] is None),
                        'per_page': {p: sum(1 for l in labs if l['page'] == p) for p in res['pages']},
                        'rings_per_page': {p: max(l['ring'] for l in labs if l['page'] == p) for p in res['pages']}}

    # B1
    groups = collections.defaultdict(list)
    for l in single:
        groups[l['page']].append(l['text'])
    sizes = [len(v) for v in groups.values()]
    b1 = {'zodiac_Lz': repetition(groups)}
    for fam, typ, ill in (('pharmaceutical_Lf', 'Lf', 'P'), ('cosmological_L0', 'L0', 'C'),
                          ('star_Ls', 'Ls', 'A'), ('nymph_Ln', 'Ln', 'B')):
        g = collections.defaultdict(list)
        for l in C.labels((typ,), illustration=ill):
            if not l['uncertain'] and not l['multiword']:
                g[l['page']].append(l['text'])
        b1[fam] = repetition(g)
        b1[fam]['pages'] = len(g)
    base = text_baseline(rows, sizes, random.Random(SEED), PERMUTATIONS)
    b1['running_text_blocks_same_sizes'] = {'mean_share': float(np.mean(base)), 'p5': float(np.percentile(base, 5)),
                                            'p95': float(np.percentile(base, 95)), 'samples': len(base)}
    b1['within_page_repeats'] = sum(len(v) - len(set(v)) for v in groups.values())
    res['B1_cross_sign_repetition'] = b1

    # B2 and B3 on zodiac
    ordered = collections.defaultdict(list)
    for l in sorted(clean, key=lambda l: (l['page'], l['ring'], l['angle'] if l['angle'] is not None else 1e9, l['locus'])):
        ordered[l['page']].append(l)
    sequences = {p: [units(l['words']) for l in ls] for p, ls in ordered.items()}
    rings = []
    for p, ls in ordered.items():
        for r in sorted({l['ring'] for l in ls}):
            rings.append([units(l['words']) for l in ls if l['ring'] == r and l['angle'] is not None])
    res['B2_positional_alignment'] = positional_alignment(sequences, random.Random(SEED))
    res['B3_within_ring_adjacency'] = adjacency(rings, random.Random(SEED))

    # B4
    lens = [len(units(l['words'])) for l in clean]
    tl = [len(C.tokenize(w, 'units23')) for w in text_words.elements()]
    init = collections.Counter(l['words'][0][0] for l in clean)
    tinit = collections.Counter(w[0] for w in text_words.elements())
    res['B4_descriptive'] = {
        'label_length_units_mean': float(np.mean(lens)), 'text_word_length_units_mean': float(np.mean(tl)),
        'label_initial_share': {k: round(v / len(clean), 3) for k, v in init.most_common(6)},
        'text_initial_share': {k: round(v / sum(tinit.values()), 3) for k, v in tinit.most_common(6)},
        'single_word_labels_also_in_running_text': sum(1 for l in single if l['text'] in text_words) / len(single),
        'labels_starting_ot_or_ok': sum(1 for l in clean if l['words'][0][:2] in ('ot', 'ok')) / len(clean)}

    # controls
    latin = C.latin_words()
    res['controls'] = {}
    for name, c in control_sets(latin, random.Random(SEED)).items():
        res['controls'][name] = {
            'B1': repetition(c['groups']),
            'B2': positional_alignment(c['sequences'], random.Random(SEED), perms=199)['pooled'],
            'B3': adjacency(c['rings'], random.Random(SEED), perms=199)}
    res['runtime_seconds'] = round(time.time() - t0, 1)
    OUT.write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ('inventory', 'B1_cross_sign_repetition', 'B3_within_ring_adjacency', 'B4_descriptive')}, indent=1))
    print('B2 pooled', json.dumps(res['B2_positional_alignment']['pooled'], indent=1))
    print('controls', json.dumps({k: {t: (v[t] if t == 'B1' else {kk: v[t][kk] for kk in ('observed', 'null_mean', 'p_empirical')})
                                      for t in ('B1', 'B2', 'B3')} for k, v in res['controls'].items()}, indent=1, default=str))
    print('written', OUT)


if __name__ == '__main__':
    main()
