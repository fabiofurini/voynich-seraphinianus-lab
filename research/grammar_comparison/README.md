# Grammar comparison (E01–E11)

[Home](../../README.md) · [Experiment register](../../notebook/EXPERIMENTS.md) · [Consolidated report](../../reports/2026-10-18-consolidated.md)

Comparative experiments on five corpora: Voynich (EVA and connected-EVA units), Codex Seraphinianus (OCR), Latin (Celsus) and Italian (Murri). Every script writes a JSON file of the same name with `_results`.

| Script | Experiment | Output |
|---|---|---|
| `run.py` | E01 first local-context comparison (superseded) | [results.json](results.json) |
| `stability.py` | Split sensitivity of E01 | [stability_results.json](stability_results.json) |
| `matched_backoff.py` | **E02** matched samples, interpolated back-off | [matched_backoff_results.json](matched_backoff_results.json) |
| `robust_boundary.py` | E03 boundary dependencies, 199 stratified permutations | [robust_boundary_results.json](robust_boundary_results.json) |
| `affix_prediction.py` | E04 suffix prediction from prefix and context | [affix_prediction_results.json](affix_prediction_results.json) |
| `long_affix_prediction.py 3` / `4` | E05 long affixes (first and disjoint versions) | [3](long_affix_3_results.json) · [4](long_affix_4_results.json) · [disjoint 3](long_affix_disjoint_3_results.json) · [disjoint 4](long_affix_disjoint_4_results.json) |
| `ocr_audit.py` | E06 Seraphinianus OCR against training labels | [ocr_audit_results.json](ocr_audit_results.json) |
| `hierarchy_probe.py` | E07 first PCFG vs HMM fit (**calibration failed**) | [hierarchy_probe_results.json](hierarchy_probe_results.json) |
| `hierarchy_control.py` | E08 synthetic grammar control | [hierarchy_control_results.json](hierarchy_control_results.json) |
| `hierarchy_calibration.py` | E08 strengthened calibration | [hierarchy_calibration_results.json](hierarchy_calibration_results.json) |
| `hierarchy_stronger.py` | **E09** calibrated PCFG vs HMM on real text | [hierarchy_stronger_results.json](hierarchy_stronger_results.json) |
| `hierarchy_bootstrap.py` | E10 paired page bootstrap for E09 | [hierarchy_bootstrap_results.json](hierarchy_bootstrap_results.json) |
| `multiscale.py` | E11 word–block mutual information at four scales | [multiscale_results.json](multiscale_results.json) |

Run through the suites in [`scripts/reproduce.py`](../../scripts/README.md), after `python scripts/fetch_data.py`.

**Code notes.** The scripts are compact and some reuse the data-preparation prefix of earlier scripts (by executing them); this is kept so that the published numbers are reproduced exactly. A shared, tested parser is on the [roadmap](../../notebook/ROADMAP.md).
