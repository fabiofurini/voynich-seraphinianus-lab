# Roadmap

[Home](../README.md) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](../reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

No roadmap item implies a promised decipherment. Completed and inconclusive work is in [STATUS.md](STATUS.md).

## P0 — Reliability before interpretation
- [ ] Independently transcribe a pre-registered Seraphinianus image sample, split by pages not used for OCR training. Report CER/WER only with validated alignment.
- [ ] Document and test several Voynich transliterations and glyph segmentations.
- [ ] Larger Italian and Latin corpora, plus other languages, manuscript abbreviations, syllabic encodings and artificial controls.
- [ ] Matched learning curves across data sizes; nested validation; familywise or FDR correction for confirmatory tests.
- [ ] Independent reproduction of this snapshot.

## P1 — Stronger generative comparisons
- [ ] Learn sub-word tokens on training pages only; compare tokenisations under complexity penalties.
- [ ] Compare left/right extension grammars, finite-state models and richer PCFGs on exactly the same held-out targets.
- [ ] Synthetic positive and negative controls that vary hierarchy strength, noise and coding.
- [ ] Separate lexical memorisation from generalisation to unseen forms.
- [ ] Held-out analysis within scribal hands and Currier languages; control for layout, section, word length and page.

## P2 — Larger-scale evidence
- [ ] Replicate Montemurro & Zanette (2013) with their exact method and data ordering before evaluating alternatives.
- [ ] Topic-varying asemic generators and copy-and-edit controls matched to section structure.
- [ ] Compare document-level and sentence-level signals without treating physical lines as known sentences.

## P2b — Follow-ups from E13/E14
- [ ] Repeat E13 with a positive control that passes (larger mock-syllabary corpora, real syllabic scripts such as Linear B or Japanese kana transliterations) before reading any syllabary verdict.
- [ ] Test whether the three positional glyph classes of E13 predict held-out word structure better than Stolfi's core–mantle–crust model.
- [ ] Look for non-cyclic anchors: zodiac labels against star-name lists; label onsets (`ot-`, `ok-`) by section.

## P3 — Interpretation
- [ ] Work with a linguist on which latent units could carry Moro-style structural dependencies.
- [ ] Define identifiability assumptions for each family of claimed decipherments.
- [ ] Seek independent semantic anchors; require prospective prediction, not retrospective fitting.
