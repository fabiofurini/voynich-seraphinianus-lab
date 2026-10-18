# Experiment register

[Home](README.md) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

All scripts live in [`research/`](research/README.md). Run them through `scripts/reproduce.py` (see [REPRODUCIBILITY.md](REPRODUCIBILITY.md)).

| ID | Experiment | Question | Code | Output | Status |
|---|---|---|---|---|---|
| E01 | Local context, first comparison | How predictable is each corpus locally? | [run.py](research/grammar_comparison/run.py) | [results](research/grammar_comparison/results.json) | Superseded by E02 |
| E02 | Matched samples and back-off | Does a third preceding glyph help, with matched samples? | [matched_backoff.py](research/grammar_comparison/matched_backoff.py) | [results](research/grammar_comparison/matched_backoff_results.json) | Completed |
| E03 | Boundary dependencies | Do word ends predict the next word's start? | [robust_boundary.py](research/grammar_comparison/robust_boundary.py) | [results](research/grammar_comparison/robust_boundary_results.json) | Completed |
| E04 | Prefixes and suffixes | Does a word's start predict its ending? | [affix_prediction.py](research/grammar_comparison/affix_prediction.py) | [results](research/grammar_comparison/affix_prediction_results.json) | Completed |
| E05 | Long disjoint affixes | Same, with non-overlapping 3- and 4-unit segments | [long_affix_prediction.py](research/grammar_comparison/long_affix_prediction.py) | [3 units](research/grammar_comparison/long_affix_disjoint_3_results.json) · [4 units](research/grammar_comparison/long_affix_disjoint_4_results.json) | Inconclusive (too few test tokens) |
| E06 | OCR audit | How reliable is the Seraphinianus transcription? | [ocr_audit.py](research/grammar_comparison/ocr_audit.py) | [summary](research/grammar_comparison/ocr_audit_results.json) | Completed, limited |
| E07 | Hierarchy, first fit | Does a PCFG beat an HMM? | [hierarchy_probe.py](research/grammar_comparison/hierarchy_probe.py) | [results](research/grammar_comparison/hierarchy_probe_results.json) | Calibration failed: not evidence |
| E08 | Synthetic control and calibration | Can the fit recover a known grammar? | [hierarchy_control.py](research/grammar_comparison/hierarchy_control.py) · [hierarchy_calibration.py](research/grammar_comparison/hierarchy_calibration.py) | [control](research/grammar_comparison/hierarchy_control_results.json) · [calibration](research/grammar_comparison/hierarchy_calibration_results.json) | Passed |
| E09 | Hierarchy, stronger fit | The calibrated PCFG vs. HMM on real text | [hierarchy_stronger.py](research/grammar_comparison/hierarchy_stronger.py) | [results](research/grammar_comparison/hierarchy_stronger_results.json) | Completed |
| E10 | Page bootstrap | Uncertainty for E09 | [hierarchy_bootstrap.py](research/grammar_comparison/hierarchy_bootstrap.py) | [results](research/grammar_comparison/hierarchy_bootstrap_results.json) | Completed |
| E11 | Multiscale organisation | Do words cluster in parts of the text? | [multiscale.py](research/grammar_comparison/multiscale.py) | [results](research/grammar_comparison/multiscale_results.json) | Exploratory |
| E12 | Simple substitution | Is the herbal text Latin or Italian in a secret alphabet? | [voynich_attack.py](research/substitution_attack/voynich_attack.py) · [solver](research/substitution_attack/voynich_attack.cpp) | [results](research/substitution_attack/results.json) | No reading found |

**Earlier studies** (17 October 2026), documented in [reports](reports/README.md): glyph inventory ([code](research/voynich_inventory.py), [full count](research/voynich_full_inventory.py)), final-*m* test ([code](research/voynich_test.py)), controls ([code](research/voynich_controls.py)), section classifier ([code](research/voynich_sections.py)), positional patterns ([code](research/patterns/patterns.py)).

**How to read this register.** E07 must not be used as negative evidence: its calibration failed. E08 fixed the optimiser with more initialisations; the final evaluation is E09 with intervals from E10. E05 is inconclusive for lack of data. `stability.py` checks the sensitivity of E01 across splits ([results](research/grammar_comparison/stability_results.json)).
