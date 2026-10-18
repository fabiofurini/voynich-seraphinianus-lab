# Voynich & Seraphinianus Lab

An open research notebook on structure, predictability and the limits of decipherment. Coordinated by **Fabio Furini**. Exploratory work developed with AI assistance; independent replication is welcome.

**We have not deciphered the Voynich manuscript, demonstrated that it is meaningless, or established that it is equivalent to the Codex Seraphinianus.** Our goal is to test explicit hypotheses, including those that could contradict our working ideas.

- [Public-facing website](https://fabiofurini.github.io/voynich-seraphinianus-lab/) · [Current status](STATUS.md) · [Experiment index](EXPERIMENTS.md) · [Hypotheses](HYPOTHESES.md)
- [Reproduce the experiments](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md) · [Consolidated report](reports/2026-10-18-consolidated.md)
- Website source: [`docs/`](docs/) · numerical outputs and scripts: [`research/`](research/)

## Main findings — 18 October 2026

1. Additional within-word context has much less predictive value in the selected Voynich transcription than in our Italian and Latin controls; this persists after matching word lengths and sample sizes and using interpolated backoff.
2. Both codices have local regularities. This is not a test of semantic content. The Seraphinianus OCR audit identifies important limitations.
3. Many shared prefixes and suffixes exist; their association does not by itself establish morphology or hierarchical syntax.
4. A calibrated two-state PCFG does not improve Voynich suffix-class prediction over a two-state HMM. This rejects a prediction about **one model and representation**, not all hierarchical grammars.
5. Simple substitution attacks calibrated on Italian and Latin controls did not yield coherent held-out readings. They are heuristic, limited experiments, not exhaustive impossibility proofs.

## Repository map

|Location|Contents|
|---|---|
|`docs/`|Responsive, buildless public website with interactive result explorer|
|`reports/`|Readable reports and research history|
|`research/grammar_comparison/`|Markov/backoff, affixes, OCR, PCFG/HMM, calibration and bootstrap|
|`research/patterns/`|Repeated sequences and positional controls|
|`research/Voynich_test_sostituzione/`|C++/Python simple-substitution experiments|
|`scripts/`|Source fetching, integrity and publication checks|
|`DATA_SOURCES.json`|Source URLs, exact checksums, rights notes and local paths|

## Quick start

```bash
python -m venv .venv
# Activate the environment for your operating system, then:
pip install -r requirements.txt
python scripts/fetch_data.py
python scripts/reproduce.py --suite matched
python scripts/check_publication.py
python -m http.server 8000 --directory docs
```

Raw third-party transcriptions and book images are **not re-licensed or bundled**. The fetcher downloads exact versions for local analysis and checks their hashes. Some historical scripts require the separately documented Stolfi/H transcription; unavailable inputs are reported rather than silently replaced. Precomputed outputs remain available.

## Hosting and collaboration

Enable GitHub Pages with branch `main`, folder `/docs`. No framework, account or database is needed to view the website. See [deployment](DEPLOYMENT.md). Contributions use issues and pull requests. Leo has not yet been granted access or listed as an author; see [collaboration](CONTRIBUTING.md).

Code: MIT. Original documentation: CC BY4.0. Third-party materials retain their own terms: [rights and provenance](RIGHTS.md).
