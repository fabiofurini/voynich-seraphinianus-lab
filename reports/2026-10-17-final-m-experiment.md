# Voynich: a reproducible experiment on final m

[Home](../README.md) · [Reports](README.md) · [Experiments](../EXPERIMENTS.md) · [Current status](../STATUS.md)

17 October 2026 · Exploratory analysis; no translation and no claim of novelty. Superseded by the [controls report](2026-10-17-controls-and-sections.md).

## Question

Could the sign written `m` in EVA be a positional variant of another sign?

## Source and method

Stolfi/Landini archive 1.6e6, transcriber Takeshi Takahashi (H): <https://www.ic.unicamp.br/~stolfi/EXPORT/00-EXPORT/98-12-28-interln16e6/>. The local file was a UTF-8 copy of the text, originally decompressed as Latin-1. Thanks to the transcribers and the curator; conditions are on the source page.

- Only P lines with at least two words and no uncertain tokens; comments and alignment fillers removed. Commas treated as separators (a choice to be checked against other segmentations). 3,840 clean lines, 202 pages.
- Deterministic split by hash of the page code: 119 development pages, 83 test pages. Test pages do not enter the vocabulary.
- The reference vocabulary contains every **non-final** word in development lines (initial words included).
- Only the final `m` of line-final words is replaced. Candidates: observed characters, deletion, `ch/sh/aiin/in/dy`. On development pages we choose the substitution that produces the most forms present in the reference vocabulary. The target is lexical coverage, not linguistic probability or meaning.

## Result

| Substitution | Development pages | Held-out pages (83) |
|---|---:|---:|
| m → r (best on development) | 280 / 363 (77.1%) | 207 / 277 (74.7%) |
| m kept | — | 118 / 277 (42.6%) |
| m → l | — | 69.3% |
| m → in | — | 54.5% |
| deletion | — | 31.8% |

Examples of transformations that produce a form found in the vocabulary: `dam→dar`, `am→ar`, `qokam→qokar`, `otam→otar`, `okam→okar`, `chom→chor`. These are EVA signs, not words read in a language and not phonetic values.

## Interpretation and limits

The result motivates a test of the positional-variant hypothesis but does **not** show m = r. Both `r` and `l` are productive endings; their frequency and the presence of short forms may explain part of the result. The comparison with leaving `m` unchanged is descriptive, not a calibrated significance test. Forms seen in testing may already have appeared in development: the test separates pages, not word types. The split does not necessarily separate scribes or bifolios. There was no check against the images and no replication on another transcription. Earlier figures of 203 pages included lines with uncertain words; the sample here is more restrictive.

## Next discriminating test

Compare the preceding contexts of `Xam/Xar/Xal` pairs while controlling for section, hand, line length and frequency; repeat on word types never seen in development; check the glyphs in the images. If the advantage disappears after controls, abandon the global substitution. *(Done in the [controls report](2026-10-17-controls-and-sections.md): the global merge was abandoned.)*

## Reproduction

```bash
python research/voynich_test.py <Stolfi H file> > results.json
```

The source hash is recorded in the [results](../research/voynich_results.json). No external dependencies.
