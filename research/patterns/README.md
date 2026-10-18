# Patterns observed in the Voynich

[Home](../../README.md) · [Research](../README.md) · [Results (website)](https://fabiofurini.github.io/voynich-seraphinianus-lab/results.html#structure)

17 October 2026. Exploratory results; no sound or meaning is attributed.

## Sample and conventions

Zandbergen–Landini ZL3b of 13 May 2025. Only P0 paragraph lines with at least two tokens, fully legible: whole lines with alternatives, special glyphs or uncertain readings are excluded. Main sample: **2,952 lines, 202 pages/panels, 25,373 tokens**, with uncertain spaces (commas) split. A second test joins them (2,951 lines, 23,560 tokens). These are not the whole-manuscript counts of other reports.

Tokens are transcription conventions, not identified linguistic words. Every pattern below is internal to a line; no n-gram crosses a line break. Breaks caused by figures are treated as separators. EVA labels are only names for signs.

## 1. Combinatorial families

The six endings `aiin, ain, edy, eedy, ol, ar` occur after each of the starts `ok, qok, ot, qot, ch, sh`: **all 36 selected combinations are attested.**

| start \ ending | aiin | ain | edy | eedy | ol | ar |
|---|---:|---:|---:|---:|---:|---:|
| ok | 166 | 102 | 80 | 76 | 46 | 90 |
| qok | 220 | 230 | 209 | 244 | 75 | 117 |
| ot | 118 | 74 | 110 | 69 | 47 | 98 |
| qot | 58 | 53 | 66 | 63 | 35 | 52 |
| ch | 37 | 14 | 383 | 41 | 287 | 54 |
| sh | 16 | 8 | 335 | 64 | 130 | 25 |

This is not an identified grammar: starts and endings could reflect morphology, encoding or mechanical production. The families were selected for description, not found by a blind search. Note the uneven rows: `qok-` spreads over all endings, while `ch-` and `sh-` concentrate on `-edy` and `-ol`.

## 2. Position in the paragraph

**438 of 490** paragraph-initial tokens (89.39%) begin with one of the EVA signs `f/k/p/t`, the so-called gallows. At other line starts: 208 of 2,462 (8.45%).

Page control: of the 178 pages with both categories in the sample, 169 show a higher rate at paragraph start, 6 are tied and 3 show the opposite. This limits explanations based only on the mixture of pages. Decorated initials and the selection of legible lines may influence the measure. We cannot tell whether these signs are separate structural markers or part of the words.

## 3. Associations between tokens

Compared with the expectation under uniform permutations of words within each line, preserving content, length and line membership:

| Pair | Observed | Expected | Pages with the pair |
|---|---:|---:|---:|
| s aiin | 38 | 5.45 | 32 |
| or aiin | 37 | 6.49 | 29 |
| chol daiin | 25 | 11.25 | 24 |
| ol shedy | 21 | 7.15 | 16 |
| shedy qokedy | 20 | 8.04 | 14 |

These pairs were selected after counting frequencies: the ratios are descriptive, not tests corrected for multiple selection. `s aiin` and `or aiin` may be affected by segmentation. Joining commas, `s aiin` stays at 18 against 2.18 expected, `or aiin` at 17 against 2.96, and `chol daiin` at 22 against 10.66.

## 4. Longer sequences

`ol shedy qokedy` recurs 5 times on 5 pages in the main sample, and 3 times on 3 pages with commas joined. `ol shedy qokedy qokeedy` recurs twice on two pages under both conventions. No identical sequence of 5 or 6 tokens repeats within a line. This does not rule out paraphrases, variants or repetitions across lines.

## 5. Dependency between the end and start of tokens

Mutual information between the last EVA character of a token and the first of the next: **0.2071 bits**. Across 499 within-line permutations: mean 0.01626, observed range 0.01280–0.02078. Joining uncertain spaces: 0.17276 bits against a mean of 0.01622 (null range 0.01290–0.01927). Neither result comes close to the shuffle reference.

The calculation concerns EVA characters at token edges, not established phonemes or glyphs. The dependency could also come from segmentation, ligatures or encoding constraints. The control shows dependency in the transcribed order relative to the chosen null model; it does not show language or semantics.

## 6. A pattern that does NOT pass the global control

Immediate repetitions of the same word: **218**, against an exact expectation of 210.86; across 499 permutations, 174–254. There is no clear global excess in this sample. With commas joined: 192 against 171.34 (reference 140–205). This result forbids describing every repetition as exceptional.

## Conclusion

The transcribed text shows at least three families of constraints: token construction, position in the paragraph, and linkage between consecutive tokens. The figures make it possible to test models of the writing; we do not yet have a verified correspondence with meanings. These phenomena are already studied in Voynich research and are not presented as new discoveries; these are reproducible counts made here.

## Reproduction and sources

```bash
python research/patterns/patterns.py                 # -> results.json
python research/patterns/patterns.py --merge-commas  # -> results_merge.json
```

Standard Python only. Outputs: [results.json](results.json), [results_merge.json](results_merge.json); source hash in [source_hash.json](source_hash.json).

- Transcription: <https://arxiv.org/src/2608.17096v1/anc/data/voynich-units/ZL3b.txt>
- EVA glyph shapes (G. Landini's reference font): <https://www.voynich.nu/hist/gabriel/eva2_reference.pdf>
