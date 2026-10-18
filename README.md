# Oltre i segni

### Voynich e Seraphinianus: un’indagine aperta

Un quaderno di ricerca pubblico sulla struttura dei segni, sulla prevedibilita e sui limiti della decifrazione. Progetto di **Fabio Furini**, sviluppato con assistenza AI e aperto a verifiche indipendenti.

**Non abbiamo decifrato il Voynich, dimostrato che sia privo di significato o stabilito che equivalga al Codex Seraphinianus.** Mettiamo alla prova ipotesi esplicite e conserviamo anche gli esiti contrari alle nostre aspettative.

## Da dove iniziare

|Per capire|Per verificare|
|---|---|
|[Sito divulgativo](https://fabiofurini.github.io/voynich-seraphinianus-lab/)|[Metodi e riproduzione](REPRODUCIBILITY.md)|
|[Stato attuale dei lavori](STATUS.md)|[Registro degli esperimenti](EXPERIMENTS.md)|
|[Ipotesi e loro esito](HYPOTHESES.md)|[Codice e risultati](research/README.md)|
|[Documenti e rapporti](reports/README.md)|[Fonti, versioni e hash](DATA_SOURCES.json)|
|[Roadmap](ROADMAP.md)|[Contribuire](CONTRIBUTING.md)|

## Risultati principali - 18 ottobre 2026

1. Additional within-word context has much less predictive value in the selected Voynich transcription than in our Italian and Latin controls; this persists after matching word lengths and sample sizes and using interpolated backoff.
2. Both codices have local regularities. This is not a test of semantic content. The Seraphinianus OCR audit identifies important limitations.
3. Many shared prefixes and suffixes exist; their association does not by itself establish morphology or hierarchical syntax.
4. A calibrated two-state PCFG does not improve Voynich suffix-class prediction over a two-state HMM. This rejects a prediction about **one model and representation**, not all hierarchical grammars.
5. Simple substitution attacks calibrated on Italian and Latin controls did not yield coherent held-out readings. They are heuristic, limited experiments, not exhaustive impossibility proofs.

## Struttura del repository

|Location|Contents|
|---|---|
|`docs/`|Responsive, buildless public website with interactive result explorer|
|`reports/`|Readable reports and research history|
|`research/grammar_comparison/`|Markov/backoff, affixes, OCR, PCFG/HMM, calibration and bootstrap|
|`research/patterns/`|Repeated sequences and positional controls|
|`research/Voynich_test_sostituzione/`|C++/Python simple-substitution experiments|
|`scripts/`|Source fetching, integrity and publication checks|
|`DATA_SOURCES.json`|Source URLs, exact checksums, rights notes and local paths|

## Riproduzione rapida

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

## Sito e collaborazione

Enable GitHub Pages with branch `main`, folder `/docs`. No framework, account or database is needed to view the website. See [deployment](DEPLOYMENT.md). Contributions use issues and pull requests. Leo has not yet been granted access or listed as an author; see [collaboration](CONTRIBUTING.md).

Code: MIT. Original documentation: CC BY4.0. Third-party materials retain their own terms: [rights and provenance](RIGHTS.md).
