# Current status — 18 October 2026

[Home](README.md) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

Exploratory snapshot, not a peer-reviewed publication. One manuscript and one OCR corpus; split replications reuse pages and are not independent books.

| Experiment | Status | Result | Main limitation |
|---|---|---|---|
| Whole-transcription inventory | Completed | 174,004 conventionally classified units; 5,385 loci; 227 panel identifiers | Not physical folios and not phonemes; alternative readings resolved by convention |
| Initial local Markov comparison (E01) | Completed, superseded | Both codices strongly predictable locally | Unequal sample sizes and codings |
| Matched interpolated back-off (E02) | Completed | Voynich extra-context gain small; Italian and Latin much larger | Three splits, small matched samples, unknown segmentation |
| Boundary dependency permutations (E03) | Completed | Both codices exceed line- and page-position controls | Does not identify syntax |
| Shared affixes (E04) | Completed, descriptive | Large families; association survives length and page controls | Not identified morphemes |
| Affix predictive tests (E04) | Completed | Prefix adds almost nothing beyond local context in the Voynich | Representation-specific |
| Long disjoint segments (E05) | Inconclusive | Only 33–53 (3-unit) or 1 (4-unit) Voynich test tokens per split | Cannot infer the absence of a rule |
| OCR audit (E06) | Completed, limited | Disagreements include counts of repeated strokes | Training labels, not independent ground truth |
| Multiscale clustering (E11) | Completed, exploratory | All corpora, the Seraphinianus included, show clustering | Not a full replication of published semantic-network analyses |
| PCFG/HMM first fit (E07) | Calibration failed; superseded | Initial optimiser missed a synthetic hierarchy | Must not be used as negative evidence |
| PCFG/HMM stronger fit (E08–E10) | Completed and calibrated | Voynich PCFG worse; Seraphinianus nominal advantage uncertain | Two states, suffix classes, lines not known to be sentences |
| Substitution attack, Italian/Latin (E12) | No coherent reading | Controls recovered; Voynich not | Heuristic; chosen languages, units and spacing only |
| Moro's structural constraints | Not directly tested | No established mapping from syntax to unknown glyphs | Cannot infer compliance from local statistics |
| Decipherment or meaninglessness | Unresolved | No claim either way | Statistical similarity is not identifiability |

**Correction on record.** With connected EVA units the Voynich keeps a small positive context gain. Any earlier wording of “no information beyond two characters” is too strong (see H05).
