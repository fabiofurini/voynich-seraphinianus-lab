# Voynich and Seraphinianus: consolidated statistical checks

[Home](../README.md) · [Reports](README.md) · [Experiments](../notebook/EXPERIMENTS.md) · [Reproduce](../notebook/REPRODUCIBILITY.md) · [Sources](../DATA_SOURCES.json) · [Rights](../RIGHTS.md)

18 October 2026. Reproducible exploratory study; no translation and no proof of untranslatability.

> **Final outcomes.**
> 1. The weak usefulness of extra context in the Voynich survives sample matching and back-off, but it is not exactly zero with connected EVA units.
> 2. OCR audit on 388 locatable words: disagreements and segmentation prevent an independent character error rate.
> 3. Affixes of 3–4 units: Voynich data are too sparse for reliable disjoint inference.
> 4. A strengthened hierarchical model, calibrated on a synthetic control, does not improve on an HMM for the Voynich in the examined representation; the Seraphinianus result is inconclusive.
>
> No proof of untranslatability or of equivalence between the two codices.

## 1. Matched comparison and rare contexts (E02)

Three page splits (seeds 19201–19203): 60% training, 20% validation, 20% test. Within each split, every one of the five corpora has the same number of words of each length from 4 to 10 units. Depending on the split there are 1,104–1,139 training words and 270–301 test words, with 874–1,070 internal test characters. Pseudo-pages for the control texts are blocks of 150 words.

Interpolated models of order 0–5: each context backs off to the shorter one, with back-off strength chosen on validation from {0.1, 1, 10, 100, 1000}. Evaluation uses only real letters from the fourth position of the word onward, identical for every order; word starts and ends are excluded. The alphabet is derived from the training split only, with an unknown class. Matching uses the availability of word lengths in each corpus, not the frequencies of the characters to be predicted.

| Corpus | Gain from order 2 to 3, min–max (bits) | Mean, order 2 | Mean, order 3 |
|---|---:|---:|---:|
| Voynich | 0.0003–0.0014 | 1.9998 | 1.9988 |
| Seraphinianus OCR | 0.0878–0.1052 | 2.0392 | 1.9420 |
| Voynich, connected EVA | 0.0034–0.0146 | 2.0143 | 2.0071 |
| Latin | 0.3189–0.3844 | 2.8926 | 2.5413 |
| Italian | 0.2955–0.3425 | 2.8722 | 2.5530 |

The raw Voynich gain is very small, and all three page-bootstrap intervals include zero. Merging the six connected EVA groups makes the gain small but positive, with 2 of 3 intervals excluding zero: saying that the text contains no further information would be wrong. The Seraphinianus and the control texts show larger gains.

The intervals are conditional on the samples; they do not give a probability that the book is asemic. These are exploratory multiple comparisons, and the splits reuse pages. Differences in script and transliteration remain.

## 2. Seraphinianus OCR audit (E06)

Scripts and outputs: `ocr_audit*`. The documented sample contains 442 original labels (no augmentation), 411 locatable positions, and 388 comparable single words on 199 pages.

| Agreement | Words | Share |
|---|---:|---:|
| Exact, at the same position | 284 / 388 | 73.20% |
| Within ±2 positions | 335 / 388 | 86.34% |

Disagreements include segmentation shifts. These figures are **not** a validated CER or WER: they are training-set labels, not an independent check. Twelve original images were inspected. Graphic recurrences are visible, but the sign-to-transliteration convention was not independently certified.

Examples of differences in the number of repeated strokes: label `Xeeei` against OCR `Xeei`; label `rrgiiiiiiiiLb` against OCR `rrgiiiiiiiLb`. These are exactly the discrepancies that can alter context statistics. The OCR limitation is documented, not solved.

## 3. Long affixes and disjoint segments (E05)

Script `long_affix_prediction.py` with parameter 3 or 4. Prefix, pre-suffix local context and suffix do not overlap; the minimum length is 3A. The model predicts only the suffix, not a whole word. Smoothing uses a vocabulary of suffixes observed in the corpus (transductive information about types, not test frequencies). In the earlier `affix_prediction.py` tests, segments were 2 units long with a minimum word length of 5, so prefix and local context could partly overlap in shorter words.

In the Voynich, 33–53 test occurrences per split remain with 3-unit segments, and **one** per split with 4-unit segments. The synthetic control is detected, but the real data lack the power for any conclusion about long segments. No null value should be read as the absence of grammar. The files `long_affix_3/4_results` keep the first, less restrictive analysis; `long_affix_disjoint_3/4_results` keep the disjoint check.

## 4. Organisation beyond the word: multiscale comparison (E11)

`multiscale.py`: the first 7,500 tokens of each corpus; blocks of 100, 300, 1,000 and 3,000 tokens; mutual information between word and block; 99 global permutations and 99 within-page permutations. All four corpora show an excess over global shuffling, the Seraphinianus included.

| Corpus | Excess at block size 1,000 (bits) |
|---|---:|
| Latin | 0.1614 |
| Voynich | 0.1256 |
| Italian | 0.0963 |
| Seraphinianus | 0.0820 |

These values are not an equivalence test. Shuffling within pages leaves the indicator almost unchanged at large scales. This is partly mathematical: the statistic uses word counts per block, not syntactic order, and if a page stays in the same block its counts do not change. The same happens in the linguistic controls. This is neither a refutation of semantics nor a full replication of Montemurro & Zanette; it shows that the measure alone does not identify syntax or meaning.

Reference: Montemurro & Zanette (2013), <https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0066344>. That work analyses reordered sections and co-occurrence structures that are not fully replicated here.

## 5. Hierarchy against sequence (E07–E10)

### 5.1 First comparison and failed positive control (E07)

A comparison beyond the single word used lines of 4–14 words, mapped to 5 suffix classes frequent in the training split plus OTHER. PCFG2 and HMM2 each have two latent states; unigram and bigram models are sequential baselines. Page split 60/20/20, training capped at 1,200 lines, 2 initialisations, 25 EM epochs, selection on validation.

| Corpus | Bigram (bits/token) | HMM2 | PCFG2 |
|---|---:|---:|---:|
| Voynich | 2.29638 | 2.29752 | 2.31111 |
| Seraphinianus | 2.08774 | 2.08965 | 2.11333 |

**The positive control failed.** On 2,000 lines generated by a grammar of the same family, the learned PCFG scored 0.991189 bits/token, the HMM 0.899125, and the known true grammar 0.875845. A hierarchical signal existed, but the first fit did not recover it. The lack of advantage on the real texts is therefore **not** evidence of absent hierarchy. Length-conditional probabilities and PCFG normalisation were verified by enumerating every binary string of length 1–5.

### 5.2 Correction after strengthened calibration (E08)

The first failure was not definitive. With Dirichlet(0.3) initialisation, more restarts and up to 100 iterations, the synthetic control succeeded: four restarts completed within 60 s, and the best PCFG reached 0.875506 bits/token, against 0.899125 for the HMM and 0.875845 for the true grammar. The initial fit had collapsed into a local optimum. This shows the importance of calibration; it does not guarantee power for human grammars or for the unknown representation of the codices.

### 5.3 Final result of the strengthened comparison (E09–E10)

Four initialisations (seeds 13, 29, 43, 61), 100 iterations each, Dirichlet(0.3) initialisation, smoothing 0.1 and model selection on validation, for both PCFG2 and HMM2. Corpus, representation and split unchanged.

| Corpus | PCFG2 test (bits/token) | HMM2 test (bits/token) | PCFG − HMM | 95% page bootstrap |
|---|---:|---:|---:|---|
| Voynich | 2.312988 | 2.293697 | +0.019291 | [+0.006544, +0.034324] |
| Seraphinianus OCR | 2.075637 | 2.079046 | −0.003408 | [−0.008042, +0.000793] |

2,000 paired bootstrap resamples over 40 Voynich and 57 Seraphinianus test pages; exploratory intervals, conditional on the selected models and this split. The hierarchical model is worse for the Voynich; for the Seraphinianus the nominal advantage is very small and the interval includes zero. The strengthened positive control succeeds.

This result excludes only the additional predictive value of **this** two-state PCFG on **this** representation in suffix classes. It does not exclude richer grammars, different representations, structure inside words, or syntax not preserved by line boundaries. Lines are not equivalent to sentences; suffix classes may remove dependencies; two states are an extreme simplification. No semantic interpretation and no direct test of Moro.

## 6. Moro: what a test would require

Musso, Moro et al. (2003), *Broca's area and the language instinct*, <https://www.nature.com/articles/nn1077>; Moro, *Impossible Languages*, <https://academic.oup.com/mit-press-scholarship-online/book/18683>.

The results on rule learning and structure dependence do not provide a known function that projects grammatical constraints onto the sequences of an unknown script. A PCFG-versus-sequential comparison is an exploratory test of statistical models, not a test of Moro's constraints. A regular morphology can also be produced by an automaton; the existence of a concatenation tree does not prove linguistic hierarchical syntax.

## 7. Why these data cannot prove absolute untranslatability

Without restricting the family of encodings, any finite string C can be made compatible with any text P of the same length by defining a key K = C − P modulo the alphabet size. This is an identifiability argument, not a historical claim that a one-time pad was used. One must therefore state which encodings, languages and segmentations are being excluded; a learning failure does not exclude all grammars.

## Provisional conclusion

The most robust result is the weak usefulness of extra within-word context in the Voynich compared with the control texts, even after matching lengths and amounts and using back-off. A small gain survives with connected EVA segmentation. The similarities with the Seraphinianus are specific, not a general equivalence. Untranslatability cannot be deduced without restrictive assumptions about the encoding.

## Reproduction and provenance

The public repository contains code, aggregates and original documents in Markdown. Third-party transcriptions, complete OCR labels and images of the modern book are not redistributed: the downloader fetches them locally with verified hashes. Public audit results are limited to aggregates. The earlier private version of the package included analysis materials not included in this publication.
