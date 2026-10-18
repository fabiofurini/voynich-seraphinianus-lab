# Voynich: controls and results, second analysis

[Home](../README.md) · [Reports](README.md) · [Experiments](../EXPERIMENTS.md) · [Current status](../STATUS.md)

17 October 2026 · All forms cited are EVA transliterations, not phonetic readings. No translation obtained, no claim of novelty.

## Main result

The controls do **not** uniquely identify `m` with `r`. The text distinguishes some illustrated sections even with scribal hand and Currier language held fixed, but the final sign of each word alone gives almost the same discriminating power. This analysis documents structure and variation; it does not show semantic content.

## Sources

1. Stolfi/Landini 1.6e6, H layer by Takeshi Takahashi: <https://www.ic.unicamp.br/~stolfi/EXPORT/00-EXPORT/98-12-28-interln16e6/>
2. Zandbergen–Landini ZL3b, version stated in the file as 13 May 2025, copy published as research material: <https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/ZL3b.txt>. The two transcriptions share sources: they are not statistically independent samples.
3. Emma May Smith, “What is [m]?”, 27 December 2016: <https://agnosticvoynich.wordpress.com/2016/12/27/what-is-m/>. This exploratory research post already discusses m → r and its limits. René Zandbergen's comment points out `otalar`/`otalam` on two nearby labels; we checked their presence in the ZL transcription, not in the images.
4. Bowern & Lindemann, *The Linguistics of the Voynich Manuscript* (2021): <https://doi.org/10.1146/annurev-linguistics-011619-030613>

## A. Controls on replacing final m

119 development and 83 test pages for H, by a deterministic split on SHA-256 of the page code modulo 3; the same rule applies to ZL. In every test the vocabulary contains only non-final words of development lines. Details and counts for each sample are in [voynich_controls.json](../research/voynich_controls.json). The additional candidates `iin/ain/ry/rl` were introduced **after** reading the literature: they are exploratory comparisons, not a new blind test of the previously selected candidate.

| Corpus and treatment of uncertain spaces | n | m unchanged | m → r | m → l | m → iin |
|---|---:|---:|---:|---:|---:|
| H, original clean sample | 277 | 118 | 207 | 192 | 189 |
| ZL, commas as separators | 198 | 89 | 133 | 123 | 132 |
| ZL, commas joined | 198 | 69 | 110 | 103 | 117 |

The best substitution changes with the treatment of uncertain spaces: `r` is not uniquely identified. The H and ZL samples also differ in their exclusion of ambiguous lines, so the comparison of percentages does not measure a pure difference between transcribers.

In ZL with commas as separators, m → r gives 67.2%, while l → r produces a known form in 124 of 160 cases (77.5%). This does not show that l → r is a valid substitution; it shows that vocabulary coverage alone favours transformations that are not necessarily correct.

### Unseen forms

Of the 150 distinct forms with final `m` in the H test set, 91 were absent from development in any position: m → r finds a match for 32/91, m → l for 27/91, m → iin for 22/91. In ZL (separated): 64 new forms, matched by r 20/64, l 12/64, iin 15/64. The per-occurrence percentages were inflated by frequent words; coverage on new forms is much lower.

A page bootstrap (4,000 resamples, fixed seed) gives roughly +1.2 to +9.5 points for the r − l advantage in H, and −0.6 to +11.0 in ZL separated. This is a descriptive interval: pages in the same quire are not necessarily independent.

### Preceding context

Also requiring the same preceding word within development lines, the 198 ZL test occurrences give 20 matches for r, 22 for l, 24 for iin, 17 for in, and 5 with m unchanged. The pairs are sparse and frequency-driven; this test does not support a unique preference for r.

### A counter-example to indiscriminate merging

ZL contains:

```
<f70v2.24,&Lz> <!00:00>otalar
<f70v2.25,&Lz> <!01:30>otalam
```

These are labels, not words at the edge of prose lines. Their co-occurrence needs an explanation before `m` is always normalised to `r`. It is not a logical refutation of every possible allography, since other conditions may exist, but it forbids treating the equivalence as established.

## B. Does the text distinguish illustrated sections with the hand held fixed?

ZL selection: hand 2, Currier language B; only illustration categories H (herbal) and B (bathing/human figures). Category names describe the images, not a translation of the text. 39 pages remain: 20 H and 19 B.

For each page, 30 tokens were sampled without replacement from line-internal positions, excluding the first and last word and whole lines with uncertain readings. This limits length and margin effects.

Multinomial naive Bayes classifier, add-one smoothing, uniform class prior. Validation leaves out one Q+B group (quire + bifolio number) at a time, 10 groups in total. Each fold's vocabulary is built only on development groups; test groups enter neither the vocabulary nor the parameters.

| Information used | Pages correct | Balanced accuracy |
|---|---:|---:|
| Whole words | 34 / 39 | 87.4% |
| Only the last EVA character of each word | 34 / 39 | 87.5% |
| Only the last two EVA characters | 33 / 39 | 85.0% |

Main seed 20261017. Over 30 different samplings, median balanced accuracy is 92.5% for words and 84.8% for the last character; min–max ranges 82.2–97.5% and 74.5–95.0%. These ranges describe sensitivity to word sampling, **not** uncertainty about generalisation to other manuscripts. In the main test, whole words do not recognise more pages than the final character alone. In the resamplings there is a median difference, but no semantic advantage was formally tested.

Exploratory reference: 1,999 label permutations by bifolio group; empirical p (+1) = 0.012. This reference does **not** control for position or quire and is not evidence of semantics.

**Decisive limitation:** the selected B pages belong to quire M, the H pages to other quires. Illustrated subject and physical position remain confounded. Chronological, orthographic or coding variation could explain the result. Controlling for hand and Currier language is useful but not sufficient.

## C. What was established and what was not

**Established in the sample:** positional structure; the absence of an m → r substitution uniquely supported by these tests; textual variation that predicts illustrated categories even with hand and Currier language fixed.

**Not established:** that spaces separate linguistic words; the value of any glyph; a language; a translation; semantic content; a discovery new to the literature.

It is methodologically correct to abandon the global m = r normalisation for now. The next useful experiment must separate subject from quire and spelling, and check the images directly; improving dictionary coverage is not enough.

## Reproduction

Python 3; the section test needs NumPy. The first two tests use only the standard library.

```bash
python research/voynich_test.py <Stolfi H file> > results_base.json
python research/voynich_controls.py <Stolfi H file> research/patterns/voynich_ZL3b.txt > controls.json
python research/voynich_sections.py research/patterns/voynich_ZL3b.txt > sections.json
```

The included JSON files contain counts, page-by-page predictions and parameters. This final version uses a strictly development-only vocabulary: a first exploratory run had produced 35/39 before types present only in testing were also excluded from the vocabulary. The figure to cite is **34/39**.
