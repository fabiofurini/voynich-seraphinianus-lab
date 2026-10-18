# Reproducibility

[Home](README.md) · [Stato](STATUS.md) · [Ipotesi](HYPOTHESES.md) · [Esperimenti](EXPERIMENTS.md) · [Metodo](REPRODUCIBILITY.md) · [Documenti](reports/README.md) · [Roadmap](ROADMAP.md)

Use Python3.10+; NumPy for latent-state models, Pillow for the optional OCR image audit. Record Python/dependency versions for a replication. C++17 and g++ are needed only for the substitution attack.

```bash
pip install -r requirements.txt
python scripts/fetch_data.py
python scripts/reproduce.py --suite matched
python scripts/reproduce.py --suite affixes
python scripts/reproduce.py --suite hierarchy
python scripts/reproduce.py --suite multiscale
```

The downloader verifies exact source hashes and fails on mismatches. It makes no silent version substitutions. Downloaded text and images are gitignored. The OCR audit can be reproduced with `python scripts/fetch_data.py --ocr-labels`; its image panel additionally requires the original image zip files from the cited upstream checkout, and a missing image does not invalidate the numeric summary.

## Experiment entry points

|Suite|Script|Scope|
|---|---|---|
|matched|matched_backoff.py|3page splits; identical counts by word length; train-derived alphabet; validation-selected interpolation|
|affixes|affix_prediction.py and long_affix_prediction.py|Predict suffix from prefix/local context;5page splits; long segments disjoint|
|hierarchy|hierarchy_stronger.py|4restarts ×100EM; same page split and encoding as baseline|
|calibration|hierarchy_control.py and hierarchy_calibration.py|Known synthetic PCFG; initial failure and stronger recovery retained|
|multiscale|multiscale.py|7500tokens each; not a full replication of published semantic-network work|
|boundary|robust_boundary.py|199permutations; same page, position bin and length bin|
|substitution|research/Voynich_test_sostituzione/voynich_attack.py|Italian/Latin heuristic simple-substitution attempt with positive controls|

Historical scripts/results remain marked as such. `stability.py` and `matched_backoff.py` currently reuse the preparation prefix of earlier scripts; this is retained for numerical fidelity, with refactoring to a shared tested parser planned. The numerical outputs are an exploratory snapshot, not an immutable software release.

The initial H-transcription terminal-symbol experiment requires a separate older source not included by the standard downloader. It is documented in the historical report and is not silently run by the main suites.

Uncertainty: min–max across overlapping splits is not a confidence interval. Page-bootstrap intervals are conditional on the fitted models and corpus. No correction for exploratory multiple comparisons has been made. Rows are not assumed to be sentences.
