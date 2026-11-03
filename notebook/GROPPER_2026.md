# Gropper (2026): *What the Voynich Manuscript Says: Nothing* — critical integration

**Status:** literature assessment and prospective replication plan, not an independent reproduction.  
**Source:** Jonathan Gropper, *What the Voynich Manuscript Says: Nothing* (August 2026), SSRN preprint, DOI [10.2139/ssrn.7367158](https://doi.org/10.2139/ssrn.7367158). The paper points to [Zenodo 10.5281/zenodo.22152069](https://doi.org/10.5281/zenodo.22152069) for its reproduction package; this project's review has not verified the archive contents.  
**Scope:** 17-page uploaded PDF, especially pp. 7–17. The paper is not treated as peer-reviewed or as proof of meaninglessness.

## What the paper reports (not independently verified here)

- Conditional character entropy approximately 2.08–2.10 bits (Voynich) against 3.26–3.52 in selected language corpora (pp. 7, 17). A bijective, context-independent character substitution preserves this statistic when tokenisation is held fixed. The empirical gap is evidence **against the tested plaintext/coding assumptions**, not an exclusion of all languages, encodings, abbreviation systems, or semantic content.
- Approximately 96% of word tokens fit one 10-slot template or a concatenation of two templates (p. 9), with strong glyph-order asymmetry. Template coverage must be compared with parsimonious baselines and held-out data; post-hoc template selection risks overfitting.
- A copy-and-mutate generator with parameter drift reportedly reproduces several local distributions (p. 10). **Reproducing selected observables does not identify the historical production mechanism.**
- The first signs of adjacent lines reportedly exhibit unusually strong anti-repetition and transition preferences, replicated in a second transcription (p. 13; z ~24–26 reported). The author says the generator does **not** explain this feature. Test against formatting, page, glyph frequency, line position, Currier dialect and hand controls.
- A compression-versus-pair-entropy comparison reports a ratio of 1.10 in Voynich versus 0.63–0.78 for selected real-text controls (pp. 13, 17). The precise definition of the ratio, compressor, theoretical bound, scaling, alphabet and preprocessing **must be reproduced** before interpreting it as an 'emptiness' test; a lack of detected long-range redundancy cannot establish a lack of semantics.
- A section/topic effect within Currier B (reported 13 sigma) disappears after a within-scribe comparison (p. 14). Confounding remains an essential issue, but the sample sizes, partitioning and exact comparisons require verification.
- The author's headline judgment (p. 14) of roughly 9:1 odds for asemic generation versus unrecoverable register is **not a calibrated posterior without stated priors and likelihoods**.

## Intersection with experiments in this repository

| Gropper claim | Our existing evidence | What is and is not comparable |
|---|---|---|
| Short-range character dependence | E02 finds minimal incremental gain from 2 to 3 preceding units (~0.0003–0.0014 bits in matched samples); connected-EVA variant yields a small positive gain (0.003–0.015) | Different estimands: conditional entropy given 1 previous character is **not** incremental benefit of a longer history. Must harmonise EVA units, samples and entropy estimators. |
| Simple substitution insufficient | E12 recovers synthetic enciphered Italian and Latin controls, finds no coherent reading in Voynich | Our attack is heuristic, language- and unit-restricted; the invariance argument applies to a bijective *glyph*-substitution with fixed boundaries, not general transduction. |
| Grammar/local production process | E04–E10 test affix dependency and limited PCFG-vs-HMM prediction; E09–E10 PCFG underperforms HMM on tested targets | Our models do not implement Gropper's ten-slot model; neither result determines semantics. |
| Weak global thematic organization | Our section classifier reports 34/39 herbal-vs-bathing pages with scribe and Currier held fixed, but quire confounded | **Potential tension, not a contradiction yet.** Re-run on identical page/hand/quire subsets, matched page lengths, and true held-out evaluation. |
| Repetition/formatting effects | Our E03 word-boundary dependence, gallows paragraph onsets, and E11 exploratory clustering | Gropper's *adjacent line opening glyph* phenomenon is distinct and needs an explicit new test. |
| Copy-and-edit baseline | Roadmap P2 already calls for copy-and-edit and topic-varying asemic generators | Implement his exact published generator if accessible, preserve original baseline and compare on held-out, multi-scale metrics. |
| Seraphinianus comparison | E02/E06: similarities in predictability, but Seraphinianus OCR needs independent validation | Gropper does not establish equivalence to Seraphinianus. Our Seraphinianus evidence remains provisional. |

## Prospective tests before interpretation

1. **Reproduction audit:** obtain source archive and hashes, enumerate exact transcriptions (Takahashi; Zandbergen–Landini ZL3b), exclusions, tokenisation, corpora, scripts and random seeds. Independently execute the reported analyses and compare reported counts.
2. **Common entropy protocol:** compare \(H(X_t\mid X_{t-1})\), \(H(X_t\mid X_{t-1},X_{t-2})\), etc. and held-out cross-entropy on precisely matched units and sizes. Repeat with connected EVA, alternative segmentation and positive synthetic ciphers; report uncertainty.
3. **Slot grammar generalisation:** train the 10-slot template on designated pages, evaluate held-out coverage, code length and perplexity, and compare against frequency-matched and position-aware null generators.
4. **Generator benchmark:** replicate copy/mutate+drift with calibrated training-only parameters and held-out data. Compare local entropy, word lengths, Zipf, repetition, near-neighbour words, between-line initials, section discrimination, multiscale dependence and compression. Include a natural-language positive control and at least one meaning-free negative control.
5. **Line-opener test:** pre-register exact adjacent-line initial transitions and nulls stratified by page, hand, section, Currier and paragraph opening; evaluate both Voynich transcriptions and pre-specified multiple-test correction.
6. **Topic-versus-scribe:** reproduce the paper's Currier B/hand comparisons and our 34/39 classifier on shared page subsets; check class availability and quire confounding before drawing semantic conclusions.
7. **Compression audit:** define numerator/denominator, compressor, alphabet, normalisation, confidence intervals and matched synthetic texts. A negative finding is model-specific, not proof of absence.
8. **External validation:** do not assert decipherment, indecipherability or meaninglessness without a prospective prediction tested on genuinely held-out material or independently established semantic anchors.

## Interpretation policy

**Supported direction:** Voynich exhibits strong local regularities, and rule-governed text generation can mimic some apparently linguistic statistics.  
**Unresolved:** whether any encoded semantic layer exists; whether Gropper's mechanism generated the manuscript; whether the Seraphinianus is a close statistical counterpart.  
**Do not repeat as fact:** 'mathematical proof that the manuscript says nothing', 'no one will ever decipher it', or the paper's 9:1 odds.

## Reference

Gropper, J. (2026). *What the Voynich Manuscript Says: Nothing.* SSRN preprint. https://doi.org/10.2139/ssrn.7367158. Reproduction package reported in article: https://doi.org/10.5281/zenodo.22152069.
