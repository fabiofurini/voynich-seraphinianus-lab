# Research code and outputs

[Home](../README.md) · [Experiment register](../notebook/EXPERIMENTS.md) · [Reproduce](../notebook/REPRODUCIBILITY.md) · [Sources](../DATA_SOURCES.json)

| Folder | Contents |
|---|---|
| [`grammar_comparison/`](grammar_comparison/README.md) | Main comparative experiments E01–E11: Markov and back-off models, boundary dependencies, affixes, OCR audit, PCFG/HMM, calibration, bootstrap, multiscale |
| [`patterns/`](patterns/README.md) | Word families, paragraph-initial gallows, word-pair associations, repeated sequences |
| [`substitution_attack/`](substitution_attack/README.md) | E12: simple-substitution solver (C++ with a Python driver) and positive controls |
| [`structure_probes/`](structure_probes/README.md) | Pre-registered E13 (syllabary fingerprint) and E14 (zodiac labels as a cycle) |
| [`early_studies/`](early_studies/README.md) | First experiments: glyph inventory, full count, final-*m* test and controls, section classifier |

Raw third-party texts are downloaded by `scripts/fetch_data.py` with hash checks and are not stored in the repository. The public OCR audit output keeps aggregates only.
