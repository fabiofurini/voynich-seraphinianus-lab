# Contributing

[Home](README.md) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

This repository is meant to be a shared base for research on the Voynich manuscript and comparable scripts. Replications, corrections and contrary results are welcome.

## Propose a hypothesis or report a result

Open an issue that states:

1. **the hypothesis**, written so that it could fail;
2. **the data**: corpus and version (with hash), transliteration and segmentation into units;
3. **the design**: train/validation/test split by page, the null model, and a **positive control** on which the method is known to succeed;
4. **the prediction**: the result that would prove the hypothesis wrong.

Keep failed calibrations on record. Do not promote an exploratory p-value to a decipherment claim.

## Change code or documents

- Work on a branch and open a pull request.
- Keep raw copyrighted sources and private correspondence out of commits.
- Add new external sources to [DATA_SOURCES.json](DATA_SOURCES.json) with URL, SHA-256 and rights note.
- Run `python scripts/check_publication.py` before pushing; it must pass.
- Write in English, with units and numbers separated by spaces (`0.019 bits`, not `0.019bits`).

## Joining the project

Leo Liberti is a prospective collaborator, not yet an author or repository collaborator. Collaborators are added only after their GitHub username and desired access are confirmed. Anyone can already read, fork and cite the repository.
