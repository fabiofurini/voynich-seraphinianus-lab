# Reproducibility

[Home](README.md) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

## Requirements

Python 3.10+ with NumPy (latent-state models). Pillow is needed only for the optional OCR image panel. A C++17 compiler (`g++`) is needed only for the substitution attack. Record your Python and dependency versions when you report a replication.

## Run

```bash
pip install -r requirements.txt
python scripts/fetch_data.py                   # exact source versions, SHA-256 verified
python scripts/reproduce.py --suite matched
python scripts/reproduce.py --suite affixes
python scripts/reproduce.py --suite hierarchy
python scripts/reproduce.py --suite multiscale
```

The downloader verifies exact source hashes and stops on any mismatch; it never substitutes another version silently. Downloaded texts and images are gitignored. The OCR audit can be reproduced with `python scripts/fetch_data.py --ocr-labels`; its image panel also needs the original image archives from the cited upstream repository, and a missing image does not invalidate the numeric summary.

## Experiment entry points

| Suite | Script | Scope |
|---|---|---|
| `matched` | matched_backoff.py | 3 page splits; identical word counts per length; train-derived alphabet; interpolation chosen on validation |
| `affixes` | affix_prediction.py, long_affix_prediction.py | Predict the suffix from prefix and local context; 5 page splits; long segments disjoint |
| `hierarchy` | hierarchy_stronger.py | 4 restarts × 100 EM iterations; same page split and encoding as the baseline |
| `calibration` | hierarchy_control.py, hierarchy_calibration.py | Known synthetic PCFG; the initial failure and the stronger recovery are both kept |
| `multiscale` | multiscale.py | 7,500 tokens per corpus; not a full replication of published semantic-network work |
| `boundary` | robust_boundary.py | 199 permutations within page, position bin and length bin |
| `substitution` | substitution_attack/voynich_attack.py | Heuristic simple-substitution search for Italian and Latin, with positive controls |

The earliest studies run directly:

```bash
python research/voynich_inventory.py research/patterns/voynich_ZL3b.txt <Stolfi H file> > inventory.json
python research/voynich_full_inventory.py research/patterns/voynich_ZL3b.txt > full_inventory.json
python research/patterns/patterns.py                 # add --merge-commas for the joined-space variant
python research/voynich_sections.py research/patterns/voynich_ZL3b.txt > sections.json
```

## Known limitations of the code

- Historical scripts and results remain marked as such. `stability.py` and `matched_backoff.py` reuse the data-preparation prefix of earlier scripts; this is kept for numerical fidelity, and a shared tested parser is planned.
- The first experiments on the Takahashi (H) transcription need an older source that the standard downloader does not fetch. They are documented in the [reports](reports/README.md) and are not run silently by the main suites.
- The numerical outputs are an exploratory snapshot, not an immutable software release.

## Uncertainty

- The min–max range across overlapping splits is not a confidence interval.
- Page-bootstrap intervals are conditional on the fitted models and the corpus.
- No correction for exploratory multiple comparisons has been applied.
- Lines are not assumed to be sentences.

## Before publishing changes

```bash
python scripts/check_publication.py
```

It checks Python syntax, JSON, every web page's ids and local links, every Markdown link, and that no private data or non-redistributable source has been committed.
