# Scripts

[Home](../README.md) · [Reproduce](../REPRODUCIBILITY.md)

| Script | What it does |
|---|---|
| `fetch_data.py` | Downloads every source listed in [DATA_SOURCES.json](../DATA_SOURCES.json), verifies its SHA-256 and stops on any mismatch. Add `--ocr-labels` for the optional OCR training labels. |
| `reproduce.py --suite <name>` | Runs one experiment suite: `matched`, `affixes`, `hierarchy`, `calibration`, `multiscale`, `boundary`, `substitution`. |
| `check_publication.py` | Pre-push checks: Python syntax, JSON, website ids and links, Markdown links, and no committed private data or third-party sources. |
