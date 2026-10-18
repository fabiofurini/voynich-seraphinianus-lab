# Roadmap

[Home](README.md) · [Stato](STATUS.md) · [Ipotesi](HYPOTHESES.md) · [Esperimenti](EXPERIMENTS.md) · [Metodo](REPRODUCIBILITY.md) · [Documenti](reports/README.md) · [Roadmap](ROADMAP.md)

## P0 — reliability before interpretation
- [ ] Independently transcribe a preregistered Seraphinianus image sample; split by pages not used for OCR training. Report CER/WER only with validated alignment.
- [ ] Document and test multiple Voynich transliterations and glyph segmentations.
- [ ] Larger Italian/Latin corpora plus other languages, manuscript abbreviations, syllabic encodings and artificial controls.
- [ ] Matched learning curves across data sizes; nested validation; familywise or FDR correction for confirmatory tests.
- [ ] Independent reproduction of this snapshot.

## P1 — stronger generative comparisons
- [ ] Learn subword tokens on training pages only; compare tokenizations under complexity penalties.
- [ ] Compare left/right extension grammars, finite-state models and richer PCFGs on exactly the same held-out targets.
- [ ] Synthetic positive and negative controls varying hierarchy strength, noise and coding, not only one easy grammar.
- [ ] Separate lexical memorization from generalization to unseen forms.
- [ ] Held-out analysis within scribal hands and Currier varieties; control for layout, section, word length and page.

## P2 — larger-scale evidence
- [ ] Replicate Montemurro–Zanette with their exact method/data ordering before evaluating alternatives.
- [ ] Topic-varying asemic generators and copying/editing controls matched to section structure.
- [ ] Compare document-level and sentence-level signals without treating physical lines as known sentences.

## P3 — interpretation
- [ ] Work with a linguist on which proposed latent units could bear Moro-style structural dependencies.
- [ ] Define identifiability assumptions for each claimed decipherment family.
- [ ] Seek independent semantic anchors; require prospective prediction, not retrospective fitting.

Completed experiments and inconclusive tests are in STATUS.md. No roadmap item implies a promised decipherment.
