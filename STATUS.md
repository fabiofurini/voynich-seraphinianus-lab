# Current status — 18 October 2026

[Home](README.md) · [Stato](STATUS.md) · [Ipotesi](HYPOTHESES.md) · [Esperimenti](EXPERIMENTS.md) · [Metodo](REPRODUCIBILITY.md) · [Documenti](reports/README.md) · [Roadmap](ROADMAP.md)

Exploratory snapshot, not a peer-reviewed publication. One manuscript and one OCR corpus; the split replications reuse pages and are not independent books.

|Experiment|Status|Result|Main limitation|
|---|---|---|---|
|Whole-transcription inventory|Completed|174,004 conventionally classified units; 5,385 loci; 227 panel identifiers|Not physical folios, not phonemes; alternatives resolved by convention|
|Initial local Markov comparison|Completed, superseded for robustness|Both codices strongly predictable locally|Unequal sample size and coding|
|Matched interpolated backoff|Completed|Voynich extra-context gain small; Italian/Latin much larger|Three splits, small matched samples, unknown segmentation|
|Boundary dependency permutations|Completed|Both exceed line/page-position controls|Does not identify syntax|
|Shared affixes|Completed descriptive|Large families; association survives length/page controls|Not identified morphemes|
|Affix predictive tests|Completed|Prefix adds almost no value beyond local context in Voynich|Representation-specific; long-affix sample underpowered|
|Long disjoint segments|Inconclusive|Only33–53 or1 test tokens per split in Voynich|Cannot infer absence of a rule|
|OCR audit|Completed limited audit|Disagreements include repeated-stroke counts|Training labels, not independent ground truth|
|Multiscale clustering|Completed exploratory|All corpora, including Seraphinianus, show clustering|Not a full replication of published semantic-network analyses|
|PCFG/HMM initial fit|Calibration failed; superseded|Initial optimizer missed synthetic hierarchy|Must not be used as negative evidence|
|PCFG/HMM stronger fit|Completed and calibrated|Voynich PCFG worse; Seraph nominal advantage uncertain|Two states; suffix classes; rows not known sentences|
|Substitution attack Italian/Latin|No coherent reading obtained|Controls recovered; Voynich did not|Heuristic, chosen languages/units/spaces only|
|Moro's structural constraints|Not directly tested|No established projection from syntax to unknown glyphs|Cannot infer compliance from local statistics|
|Decipherment / meaninglessness|Unresolved|No claim either way|Statistical similarity is not identifiability|

The matched Voynich connected-EVA variant has a small positive context gain. Any earlier wording of “no information beyond two characters” is too strong.
