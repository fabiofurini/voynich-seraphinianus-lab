# Voynich: a substitution test with positive controls (E12)

[Home](../../README.md) · [Research](../README.md) · [Results (website)](https://fabiofurini.github.io/voynich-seraphinianus-lab/results.html#cipher)

17 October 2026. No decipherment obtained.

## Question

Could a homogeneous botanical sample be Latin or Italian written with a fixed one-to-one substitution, keeping the transcription's spaces?

The test concerns exactly this hypothesis with the chosen graphic segmentation. It does not concern homophonic ciphers, syllabic codes, abbreviations, other languages or other segmentations.

## Method

- Voynich source: Zandbergen–Landini ZL3b, version of 13 May 2025.
- Only P0 paragraphs of the herbal (H) pages, hand 1, Currier language A, according to the ZL metadata.
- Graphic segmentation into 23 units: `ch/sh/ckh/cth/cph/cfh` are units; `i` and `n` stay separate. Only fully legible tokens are accepted.
- Pages split by SHA-256 of the page name modulo 3: about two thirds development, one third test. No optimisation on test pages.
- 19,113 conventional characters (spaces included) for the key search and 18,820 for testing. The search does not use the whole manuscript: the restriction limits mixing of sections and hands.
- Character 4-gram models with smoothing 0.01: medical Latin from Celsus, *De medicina* book I (40,052 characters for the model), and Italian from Romolo Murri, *Il partito radicale e il radicalismo italiano* (95,555 characters). The latter is modern Italian, not a medieval corpus.
- Normalisation to lower case without accents; punctuation removed. For the Gutenberg text, the delimiters and final licence block are removed before modelling; the original file keeps its own header and licence.
- Simulated annealing: 8 restarts, 50,000 swap proposals per restart, temperature 60 → 0.06, seed 20261017.
- The model searches a permutation of the 26-letter Latin alphabet. The 23 Voynich units occupy 23 positions; the rest allow swaps with unassigned letters.

## Positive calibration

For each language, a passage from the part of the text excluded from model building is enciphered with a known random permutation, keeping spaces. The same algorithm then tries to recover it.

| Test | Letters of the control recovered | Tokens found in the reference vocabulary |
|---|---:|---:|
| Latin control | 100% | 933 / 1,360 = 68.60% |
| Italian control | 100% | 1,770 / 2,387 = 74.15% |
| Voynich, key optimised on Latin, test pages | Not measurable (no true text) | 35 / 3,153 = 1.11% |
| Voynich, key optimised on Italian, test pages | Not measurable (no true text) | 221 / 3,153 = 7.01% |

The vocabulary is the set of words in the text used to build the model, not a complete dictionary. Percentages are on tokens of at least three letters. Occasional matches are not words read with demonstrated meaning. The Voynich output does not give a justifiable coherent reading; the strings in the JSON are mechanical results, not translations.

## A key-independent check: triples

In the Voynich development sample, **39 of 3,844 tokens** contain three identical consecutive units. A one-to-one substitution necessarily preserves this property. The Latin comparison text has no triples (0 / 7,595 tokens); normalised Italian has one (`www`, 1 / 19,118). This signals a difference between the chosen graphic units and the letters of the comparison texts. The segmentation of `iin` and other strokes may contribute; it is not a proof that the manuscript has no language.

## What the test concludes

The search works on both simple-substitution controls but produces no convincing key on the Voynich sample. This is a negative result on a limited family of hypotheses, not an impossibility proof or an exhaustive search over all keys. The search is heuristic and the models are limited. A reading hypothesis cannot be promoted to a translation; further progress needs better-identified writing units and/or an external anchor that imposes independent constraints.

## Earlier zodiac lead

`okeodaly` is confirmed in historical transcriptions on f71v and f72r1, both Taurus, in the outer ring. The exact sequence appears twice in ZL. The immediate contexts differ; it is not a repeated phrase. Forms within one edit of `okeodaly` (including itself) cover 10 pages with commas split and 9 with commas joined: graphic similarity does not prove semantic identity. The two folios belong to the same bifolio, so they are not independent replicates. No phonetic value was derived from this lead.

## Data sources

- <https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/ZL3b.txt>
- <https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/latin/celsus.de_medicina.part.1.tess>
- <https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/italian/26166.txt>
- <https://www.voynich.nu/q11/f071v_tr.txt> · <https://www.voynich.nu/q11/f072r1_tr.txt>

## Reproduction

Python 3 and g++ with C++17; no extra Python libraries.

```bash
python scripts/fetch_data.py
python scripts/reproduce.py --suite substitution     # or: python research/substitution_attack/voynich_attack.py
```

The driver compiles the solver and saves results to `run/results.json`, resuming completed runs (delete that file to repeat both languages). The published results are in [results.json](results.json); source hashes in [source_hashes.json](source_hashes.json).
