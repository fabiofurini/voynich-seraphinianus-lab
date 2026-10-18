# Research code and outputs

[Home](../README.md) · [Experiment register](../EXPERIMENTS.md) · [Reproduce](../REPRODUCIBILITY.md) · [Sources](../DATA_SOURCES.json)

| Folder or file | Contents |
|---|---|
| [`grammar_comparison/`](grammar_comparison/README.md) | Main comparative experiments E01–E11: Markov and back-off models, boundary dependencies, affixes, OCR audit, PCFG/HMM, calibration, bootstrap, multiscale |
| [`patterns/`](patterns/README.md) | Word families, paragraph-initial gallows, word-pair associations, repeated sequences |
| [`substitution_attack/`](substitution_attack/README.md) | E12: simple-substitution solver (C++ with a Python driver) and positive controls |
| `voynich_inventory.py` → [`voynich_inventory.json`](voynich_inventory.json) | 23-unit working inventory on ZL3b and Takahashi H; contexts of c, h, q, n |
| `voynich_full_inventory.py` → [`voynich_full_inventory.json`](voynich_full_inventory.json) | Every transcribed unit in ZL3b (174,004) |
| `voynich_test.py` → [`voynich_results.json`](voynich_results.json) | Final-*m* substitution test |
| `voynich_controls.py` → [`voynich_controls.json`](voynich_controls.json), [`voynich_contexts.json`](voynich_contexts.json) | Controls for the final-*m* test |
| `voynich_sections.py` → [`voynich_sections.json`](voynich_sections.json) | Herbal vs bathing section classifier |
| [`voynich_sources.json`](voynich_sources.json) | Source notes for the earliest experiments |

Raw third-party texts are downloaded by `scripts/fetch_data.py` with hash checks and are not stored in the repository. The public OCR audit output keeps aggregates only.
