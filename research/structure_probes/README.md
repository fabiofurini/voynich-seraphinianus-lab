# Structure probes: the two "Linear B" conditions (E13, E14)

[Home](../../README.md) · [Research](../README.md) · [Experiment register](../../notebook/EXPERIMENTS.md) · [Hypotheses](../../notebook/HYPOTHESES.md)

Every decipherment of an unknown script has needed two things: a sign system whose internal structure could be worked out (Kober's paradigms, Ventris's grid) and an anchor to the outside world (place names, numerals, logograms). These two experiments test whether the Voynich text offers either, **before** any reading is attempted.

The protocol below was written and committed before the scripts were run. Results follow it in a separate section and are reported whatever they say.

---

## Pre-registration

### E13 — Syllabary fingerprint (Kober-grid test)

**Question.** In a consonant–vowel syllabary used for an inflected language, signs sharing a consonant alternate with one another after the same stem. The sign-alternation graph then falls into many small classes. In an alphabet the same graph has few large classes (vowels alternate with vowels, consonants with consonants). Under free combination of parts there is no class structure beyond chance. Which pattern does the Voynich alternation graph show?

**Data.** Word types from the strict paragraph sample (P0 rows, fully legible, ≥ 2 words), under three pre-stated segmentations: EVA letters; the 23-unit inventory; the 23-unit inventory with `qo` and `in/iin/iiin` merged (conjecture C3). Controls: Latin letters (Celsus), Italian letters (Murri), Seraphinianus OCR, and Latin re-encoded in a mock open syllabary (CV → one sign, lone vowel → one sign, consonant without a following vowel → consonant + dummy *a*), which is the positive control for grid structure.

**Procedure.**
1. Stem = first 2 units (secondary analysis: 3). The unit after the stem is the junction sign. For every stem with ≥ 2 distinct junction signs, every unordered pair of them adds 1 to the alternation matrix (stems counted, not tokens). A mirrored analysis uses the last 2 units as stem.
2. Nodes: signs with weighted degree ≥ 5.
3. Statistics: modularity *Q* of a greedy (Clauset–Newman–Moore) partition; number of communities of size ≥ 2; share of nodes in the largest community; concentration (share of alternation weight in the top 10% of node pairs).
4. Null: 499 permutations of the junction-sign column over the distinct (stem, sign) pairs, preserving each stem's fan-out and each sign's frequency; seed 20261018.
5. Primary comparison on the same number of word types in every corpus (the minimum, sampled with the seed); full-corpus values secondary.
6. Where true classes are known, purity and NMI of the found partition against them.

**Decision rules.**
- *Syllabary-like*: *Q* above null (p < 0.01) **and** ≥ 6 communities **and** largest community ≤ 25% of nodes, with the CV control showing the same pattern and purity against consonant classes ≥ 0.6.
- *Alphabet-like*: *Q* above null **and** ≤ 3 communities with one holding ≥ 40% of nodes.
- *Free-combination-like*: *Q* not above null (p ≥ 0.05).
- Otherwise: mixed / not classifiable by this test.

**What this cannot show.** A syllabary-like result would not identify consonants or vowels; it would only say that a grid is worth building. A negative result excludes the Kober–Ventris route under these segmentations, not under all possible ones.

### E14 — Zodiac labels as a cycle

**Question.** Each zodiac sign carries about thirty figures with a label. If the labels were a cyclic numbering (degrees, days), label types would recur across signs, labels at the same position in different signs would resemble one another, and angularly adjacent labels would resemble one another as consecutive numerals do. If they were names, none of this would hold.

**Data.** The 299 `Lz` labels on the twelve zodiac pages (`$I=Z`) of ZL3b, with their ring (groups starting at `@Lz`) and clock position (`<!HH:MM>`). Reading policy as elsewhere: first alternative of `[x:y]`; labels containing `?`, `@nnn;` or `{…}` excluded from similarity tests and counted. Labels compared as sequences of 23-unit tokens.

**Tests.**
- **B1 cross-sign repetition**: share of clean single-word labels whose type occurs on ≥ 2 zodiac pages. Baselines: the same statistic for pharmaceutical (`Lf`), cosmological (`L0`), star (`Ls`) and nymph (`Ln`) labels, and for 999 samples of running-text blocks of the same sizes from 12 random paragraph pages.
- **B2 cross-sign positional alignment**: labels ordered by (ring, angle); pages compared pairwise when their counts differ by ≤ 3; labels paired by normalised rank; mean normalised edit distance minimised over cyclic rotations and reading direction. Null: 999 permutations of the second page's labels with the same minimisation. Pooled over pairs.
- **B3 within-ring adjacency**: mean normalised edit distance between angularly adjacent labels in rings with ≥ 4 labels; null: 999 within-ring permutations; pooled.
- **B4 descriptive**: label length, initial glyph, overlap with running-text vocabulary.
- **Controls**: twelve "signs" labelled 1–30 with Latin cardinals and, separately, Roman numerals (counting cycles); twelve groups of 30 distinct Latin words (names). All through the same code.

**Decision rules.**
- *Cycle-like*: B1 well above the running-text baseline **and** (B2 p < 0.01 pooled **or** B3 p < 0.01 pooled), with the numeral controls passing.
- *Names-like*: B1 at or below the other label families **and** B2, B3 not significant.
- Otherwise: mixed. A positive B3 alone is also compatible with copy-with-drift production and is not read as evidence of numbering.

**What this cannot show.** A names-like result does not say what the names are; a cycle-like result would not identify the numerals. The two Aries and two Taurus pages carry 15 figures each and are compared as they stand, without assuming which half comes first.

### Run

```bash
python scripts/fetch_data.py
python research/structure_probes/syllabary_fingerprint.py   # -> syllabary_fingerprint_results.json
python research/structure_probes/zodiac_cycle.py            # -> zodiac_cycle_results.json
```

Python 3.10+, NumPy only.

---

## Results (run on 18 October 2026, after the pre-registration commit `56565ef`)

Outputs: [syllabary_fingerprint_results.json](syllabary_fingerprint_results.json) · [zodiac_cycle_results.json](zodiac_cycle_results.json). Runtime about 3 minutes each.

**Implementation note.** Before the first run, two functions were rewritten for speed without changing the protocol: the CNM partition is vectorised with NumPy (identical partitions and *Q* on 200 of 200 random test graphs, same tie-breaking), and B2 pre-computes the label distance matrix once per page pair instead of once per permutation. Both changes are in the results commit.

### E13 — Syllabary fingerprint

**Controls.** Latin and Italian letters are classified *alphabet-like* in all 16 analyses, and the found partition recovers vowels vs consonants (Latin purity 0.95–1.00). The **mock CV syllabary never reaches the pre-registered "syllabary-like" criteria.** Its closest result (stem 3, forward) has 6 communities and a largest community of 27% of nodes (rule: ≤ 25%), with purity against consonant classes 0.53 (rule: ≥ 0.6). Under the decision rules the positive control fails narrowly, so **this test cannot classify any corpus as a syllabary**: its power to detect one is not demonstrated.

**Voynich**, 24 analyses (3 segmentations × forward/mirrored × stem 2/3 × matched/full):

| Verdict | Analyses |
|---|---:|
| syllabary-like | **0** |
| alphabet-like | 12 |
| mixed / not classifiable | 9 |
| free-combination-like | 3 (all stem 2, matched sample, mirrored) |

Modularity is above the null in 21 of 24 analyses (p ≤ 0.006); the partitions have 2–3 communities, the largest holding 36–70% of nodes. The Seraphinianus behaves the same way (alphabet-like, mixed or free-combination; never syllabary-like), so this pattern does **not** separate a script with meaning from an invented one.

**Verdict under the pre-registered rules.** No syllabary signature in any of 24 analyses; the dominant pattern is "few large classes". Because the CV control did not pass, the absence of a syllabary signature is **suggestive, not conclusive**.

**Observations not covered by the pre-registration** (reported as exploratory):
- *Inventory size.* Signs with alternation degree ≥ 5 number 18–31 in the Voynich, 20–23 in the alphabets and 51–77 in the mock syllabary. The Voynich alternation graph is alphabet-sized.
- *Stable glyph classes.* In the forward analyses the Voynich splits into three classes that recur across stems, segmentations and samples:
  1. the gallows and their bench forms with `q`: `k t p f ckh cth cph cfh q` (sometimes `g`, `b`);
  2. `a e o y d ch sh`;
  3. `i l r m n` with the `in/iin/iiin` units (sometimes `s`, `g`, `j`).

  The alphabets split into vowels and consonants instead. The first class matches the "core" of Stolfi's [*A Grammar for Voynichese Words*](https://www.ic.unicamp.br/~stolfi/voynich/00-EXPORT/00-06-07-word-grammar/) (2000); the other two divide his "mantle" and "crust" differently. The classes look **positional** (where a glyph can stand in a word) rather than phonological. This replicates, by a blind method, a structure described in the literature; it is not a new discovery.

### E14 — Zodiac labels as a cycle

**Controls.** The power check passes. Latin cardinals and Roman numerals 1–30: B1 = 100% recurrence, B2 p = 0.005 (perfect alignment), B3 p = 0.005 (the minimum with 199 permutations). Distinct Latin words: B1 = 0%, B2 p = 0.57, B3 p = 0.35.

**Voynich** (247 clean single-word labels, 285 clean labels on 12 pages, 28 rings):

| Test | Result | Reference |
|---|---|---|
| B1 cross-sign repetition | 21.5% of labels recur on another sign (22 types; `otaly` on 4 signs) | running-text blocks 34.6% (5th–95th percentile 27.5–42.1%); pharmaceutical 5.7%, nymph 7.1%, cosmological 0%, star 0% |
| B2 positional alignment | pooled p = 0.128; 2 of 34 page pairs below 0.05 (1.7 expected by chance) | numerals p = 0.005 |
| B3 within-ring adjacency | p = 0.301 | numerals p = 0.005 |
| B4 descriptive | 77% start with `o`, 54% with `ot-`/`ok-` (running text: 20% start with `o`); mean length 6.5 units (text 4.5); 48% also occur in running text | — |

**Verdict under the pre-registered rules: mixed.** B1 falls between the two definitions: below running text, above the other label families. B2 and B3 are clearly negative while the numeral controls pass. **The labels do not behave as a numbering cycle**: labels at the same position on different signs are no more alike than chance, and neighbouring labels do not progress like consecutive numerals.

Exploratory reading: the zodiac labels form a distinct vocabulary class with a characteristic `o-`/`ot-`/`ok-` onset. They recur across signs more than other labels do because they share that vocabulary, not because they share positions.

### What the two probes say together

The question was whether the Voynich offers either of the two footholds that made Linear B decipherable.

- **Sign system (Kober/Ventris grid):** no syllabary signature; the alternation structure has alphabet size and positional glyph classes. The test's power for syllabaries is not demonstrated, so this route is weakened, not closed.
- **Internal anchor (zodiac as a numbered cycle):** not present in its most natural form, with demonstrated power. The zodiac labels may still be names (of stars, days or figures), but they cannot be used as a numeral key.

Neither probe opens the Linear B route; both narrow it. A decipherment from internal evidence alone would now need either a non-cyclic anchor or a sign system that is neither an alphabet written letter by letter nor a simple syllabary.
