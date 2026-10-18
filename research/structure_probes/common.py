"""Shared loaders and utilities for the structure probes E13 (syllabary fingerprint)
and E14 (zodiac cycle). Parsing conventions follow research/patterns/patterns.py and
research/grammar_comparison/run.py so that samples match earlier experiments.
"""
import collections
import itertools
import math
import re
import unicodedata
from pathlib import Path

import numpy as np

RESEARCH = Path(__file__).resolve().parent.parent
ZL = RESEARCH / 'patterns/voynich_ZL3b.txt'
SERAPH = RESEARCH / 'seraph_ocr/CS_OCR_TRANSLITERATION.txt'
LATIN = RESEARCH / 'substitution_attack/sources/crib_latin.txt'
ITALIAN = RESEARCH / 'substitution_attack/sources/crib_italian.txt'

SEGMENTATIONS = {
    # EVA letters, one unit per character
    'eva': re.compile(r'.'),
    # the 23-unit working inventory: six connected clusters are single units
    'units23': re.compile(r'ckh|cth|cph|cfh|ch|sh|.'),
    # units23 plus the two most debated merges (conjecture C3): qo and i-runs + n
    'units23_qo_in': re.compile(r'ckh|cth|cph|cfh|ch|sh|qo|iiin|iin|in|.'),
}


def tokenize(word, seg):
    return SEGMENTATIONS[seg].findall(word)


# ---------------------------------------------------------------- Voynich (ZL3b)

def zl_illustration_types():
    """page id -> $I= illustration code (H herbal, Z zodiac, B balneological, ...)."""
    out = {}
    for line in ZL.read_text().splitlines():
        m = re.match(r'<(f[^>]+)>\s+<!.*\$I=([A-Z])', line)
        if m:
            out[m[1]] = m[2]
    return out


def voynich_rows():
    """Strict paragraph sample: fully legible P0 rows with >= 2 words -> [(page, words)]."""
    rows = []
    for line in ZL.read_text().splitlines():
        m = re.match(r'<(f[^.>]+)\.([^,>]+),([^>]*P0)>\s*(.*)', line)
        if not m:
            continue
        text = re.sub(r'<[^>]*>', '', m[4].replace('<->', '.'))
        words = [w for w in re.split(r'[.,\s]+', text) if w]
        if len(words) > 1 and all(re.fullmatch('[a-z]+', w) for w in words):
            rows.append((m[1], words))
    return rows


def _clean_label(raw):
    """Apply the project's reading policy to a label: drop comments, take the first
    alternative of [x:y] groups, split on '.' and ',' (uncertain spaces)."""
    t = re.sub(r'<[^>]*>', '', raw)
    t = re.sub(r'\[([^\]:]*):[^\]]*\]', r'\1', t)
    words = [w for w in re.split(r'[.,\s]+', t) if w]
    uncertain = bool(re.search(r'[?@{]', t)) or not words
    return words, uncertain


def labels(types=('Lz',), illustration=None):
    """Labels of the given locus subtypes -> list of dicts.

    ring: increments at each '@' locus (first label of a group) within a page;
    angle: clock position from <!HH:MM> comments, in degrees (0 = top), or None."""
    illus = zl_illustration_types()
    out, page_prev, ring = [], None, 0
    for line in ZL.read_text().splitlines():
        m = re.match(r'<(f[^.>]+)\.(\d+),([@&+*=])(L.)>\s*(.*)', line)
        if not m or m[4] not in types:
            continue
        page, locus, mark, raw = m[1], int(m[2]), m[3], m[5]
        if illustration and illus.get(page) != illustration:
            continue
        if page != page_prev:
            page_prev, ring = page, 0
        if mark == '@':
            ring += 1
        clock = re.search(r'<!(\d\d):(\d\d)>', raw)
        angle = ((int(clock[1]) % 12) * 30 + int(clock[2]) / 2) if clock else None
        words, uncertain = _clean_label(raw)
        out.append({'page': page, 'locus': locus, 'ring': ring, 'angle': angle,
                    'words': words, 'text': '.'.join(words), 'uncertain': uncertain,
                    'multiword': len(words) > 1, 'illustration': illus.get(page)})
    return out


# ---------------------------------------------------------------- controls

def seraph_rows():
    rows, page = [], None
    for line in SERAPH.read_text().splitlines():
        if line.startswith('###PAGE'):
            page = line.split()[-1]
            continue
        if line.startswith('#') or not line.strip():
            continue
        w = line.split()
        if page and len(w) > 1 and all(re.fullmatch('[A-Za-z]+', x) for x in w):
            rows.append((page, w))
    return rows


def _norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.findall('[a-z]+', s)


def latin_words():
    raw = LATIN.read_text(encoding='utf-8', errors='replace')
    return _norm(re.sub(r'<[^>]*>', '', raw))


def italian_words():
    try:
        raw = ITALIAN.read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        raw = ITALIAN.read_text(encoding='latin-1')
    if '*** START' in raw:
        raw = raw.split('*** START', 1)[1].split('***', 1)[1]
    if '*** END' in raw:
        raw = raw.split('*** END', 1)[0]
    return _norm(raw)


VOWELS = set('aeiouy')


def cv_syllabary(word):
    """Encode a Latin word in a mock open syllabary (Linear B style): CV -> one sign,
    lone vowel -> one sign, a consonant not followed by a vowel -> C + dummy 'a'."""
    out, i = [], 0
    while i < len(word):
        c = word[i]
        if c in VOWELS:
            out.append(c)
            i += 1
        elif i + 1 < len(word) and word[i + 1] in VOWELS:
            out.append(c + word[i + 1])
            i += 2
        else:
            out.append(c + 'a')
            i += 1
    return out


def sign_class_cv(sign):
    return sign[0] if len(sign) == 2 else 'V'


def sign_class_letter(ch):
    return 'V' if ch in VOWELS else 'C'


LATIN_CARDINALS = ('unus duo tres quattuor quinque sex septem octo novem decem undecim duodecim '
                   'tredecim quattuordecim quindecim sedecim septendecim duodeviginti undeviginti '
                   'viginti vigintiunus vigintiduo vigintitres vigintiquattuor vigintiquinque '
                   'vigintisex vigintiseptem vigintiocto vigintinovem triginta').split()
ROMAN_NUMERALS = ('i ii iii iv v vi vii viii ix x xi xii xiii xiv xv xvi xvii xviii xix xx '
                  'xxi xxii xxiii xxiv xxv xxvi xxvii xxviii xxix xxx').split()


# ---------------------------------------------------------------- metrics

def levenshtein(a, b):
    """Edit distance between two sequences (lists of units)."""
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def norm_lev(a, b):
    n = max(len(a), len(b))
    return levenshtein(a, b) / n if n else 0.0


def modularity(W, part):
    """Weighted Newman modularity of a partition (list of node lists)."""
    m2 = W.sum()
    if m2 == 0:
        return 0.0
    k = W.sum(1)
    q = 0.0
    for comm in part:
        idx = np.array(comm)
        q += W[np.ix_(idx, idx)].sum() / m2 - (k[idx].sum() / m2) ** 2
    return float(q)


def greedy_modularity(W):
    """Clauset-Newman-Moore agglomeration on a weighted symmetric matrix (zero diagonal).
    At each step merges the pair (i < j) with the largest modularity gain; ties go to the
    first pair in row-major order. Returns (partition, Q). Small graphs only."""
    n = len(W)
    m2 = W.sum()
    if n == 0 or m2 == 0:
        return [[i] for i in range(n)], 0.0
    E = W / m2
    a = W.sum(1) / m2
    comms = [[i] for i in range(n)]
    while len(comms) > 1:
        k = len(comms)
        dq = 2 * (E - np.outer(a, a))
        dq[np.tril_indices(k)] = -np.inf
        flat = int(np.argmax(dq))
        if dq.flat[flat] <= 1e-12:
            break
        i, j = divmod(flat, k)
        E[i, :] += E[j, :]
        E[:, i] += E[:, j]
        a[i] += a[j]
        E = np.delete(np.delete(E, j, 0), j, 1)
        a = np.delete(a, j)
        comms[i] += comms[j]
        del comms[j]
    return comms, modularity(W, comms)


def purity_nmi(part, classes):
    """Purity and normalised mutual information of a partition against true classes
    (classes: list indexed by node)."""
    n = sum(len(c) for c in part)
    pur = sum(max(collections.Counter(classes[i] for i in comm).values()) for comm in part) / n
    pc = collections.Counter(classes)
    hc = -sum(v / n * math.log(v / n) for v in pc.values())
    hk = -sum(len(c) / n * math.log(len(c) / n) for c in part)
    mi = 0.0
    for comm in part:
        cc = collections.Counter(classes[i] for i in comm)
        for cls, v in cc.items():
            mi += v / n * math.log((v / n) / ((len(comm) / n) * (pc[cls] / n)))
    nmi = mi / math.sqrt(hc * hk) if hc > 0 and hk > 0 else 0.0
    return float(pur), float(nmi)


def summarize_null(obs, null, larger_is_extreme=True):
    null = np.asarray(null, dtype=float)
    sd = null.std(ddof=1) if len(null) > 1 else 0.0
    z = (obs - null.mean()) / sd if sd > 0 else None
    if larger_is_extreme:
        p = (1 + np.sum(null >= obs)) / (len(null) + 1)
    else:
        p = (1 + np.sum(null <= obs)) / (len(null) + 1)
    return {'observed': float(obs), 'null_mean': float(null.mean()), 'null_sd': float(sd),
            'null_min': float(null.min()), 'null_max': float(null.max()),
            'z': None if z is None else float(z), 'p_empirical': float(p), 'permutations': int(len(null))}
