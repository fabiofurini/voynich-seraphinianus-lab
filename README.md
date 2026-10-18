# Beyond the Signs

**An open, reproducible research notebook on the Voynich manuscript and the Codex Seraphinianus.**

[**Website**](https://fabiofurini.github.io/voynich-seraphinianus-lab/) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md) · [Contribute](CONTRIBUTING.md)

> We have **not** deciphered the Voynich manuscript, **not** shown that it is meaningless, and **not** shown that it is equivalent to the Codex Seraphinianus. We test explicit hypotheses against controls and keep the results that go against our expectations.

---

## 1. What we want to do

The Voynich manuscript (Beinecke MS 408, vellum dated 1404–1438) is written in a script nobody can read. Its text is highly regular, and that regularity is often cited as evidence that it encodes a language. The Codex Seraphinianus (Luigi Serafini, 1981) is a modern illustrated book in an invented script that its author has said carries no message.

The project asks one question: **which measurable properties of a script can tell meaningful writing apart from writing that only looks systematic?**

We answer it by:

1. measuring the Voynich text with methods that are first proven on **positive controls** (Latin, Italian, synthetic grammars with known rules);
2. using the **Seraphinianus as a negative-ish control**, a fluent invented script;
3. testing on **held-out pages**, with stated **null models** and uncertainty;
4. writing every claim as a **falsifiable hypothesis** and scoping every negative result to a model, a dataset and a segmentation.

The aim is a shared, reusable base for anyone working on this subject: code, derived data, protocols and a public record of what worked and what did not.

## 2. What has been done

Twelve experiments, all scripted and reproducible (full register in [EXPERIMENTS.md](EXPERIMENTS.md)):

| Area | Experiments | Status |
|---|---|---|
| Glyph inventory and frequencies | Whole-transcription count: 174,004 units, 5,385 loci, 227 panels | Done |
| Local predictability | E01 first comparison · **E02 matched samples with back-off** · E03 word-boundary dependencies | Done |
| Word structure | E04 prefixes and suffixes · E05 long disjoint affixes | Done · E05 inconclusive |
| Data quality | E06 audit of the Seraphinianus OCR | Done, limited |
| Hierarchical grammar | E07 first fit (**calibration failed**, kept on record) · E08 calibration · E09 stronger fit · E10 page bootstrap | Done |
| Beyond the word | E11 multiscale word clustering | Exploratory |
| Decipherment | E12 simple-substitution attack with positive controls | No reading found |
| Earlier studies | Final-*m* allograph test, section classifier, positional patterns | Done ([reports](reports/README.md)) |

## 3. What evidence we have

Evidence pointing in **both** directions. Each line links to the full result.

**Toward a simple, local process (little information beyond the next glyph)**

- Extra context barely helps: the gain from 2 to 3 preceding glyphs is **0.0003–0.0014 bits** in the Voynich against **0.30–0.38 bits** in Latin and Italian, with matched samples ([E02](EXPERIMENTS.md)).
- A two-state tree grammar (PCFG) predicts Voynich suffix classes **worse** than a chain model (HMM): +0.0193 bits/token, 95% page-bootstrap interval [+0.0065, +0.0343] ([E09–E10](EXPERIMENTS.md)).
- A simulated-annealing cipher solver recovers 100% of enciphered Latin and Italian but finds **no readable key** for the Voynich ([E12](research/substitution_attack/README.md)).
- 39 of 3,844 Voynich words contain a glyph tripled; the Latin control has 0 of 7,595. A simple substitution of Latin cannot produce this.

**Toward an organised, possibly meaningful system**

- 30 words per page classify herbal vs. bathing pages correctly for **34 of 39 pages**, with scribe and Currier language held fixed ([report](reports/2026-10-17-controls-and-sections.md)). Confounded with quire, so not proof of meaning.
- The last glyph of a word shares **0.207 bits** with the first glyph of the next, against 0.016 in line shuffles ([patterns](research/patterns/README.md)).
- **89.4%** of paragraph-initial words begin with a gallows glyph, against 8.5% of other line-initial words.
- With connected EVA units the extra-context gain is small but **not zero** (0.003–0.015 bits).

**Our reading.** The text is highly organised, mostly at very short range. The invented Seraphinianus shares several of these properties, so organisation is not proof of meaning, and a weak local signal is not proof of its absence. See [HYPOTHESES.md](HYPOTHESES.md) for verdicts on ten explicit hypotheses.

## 4. What comes next

Priorities from the [roadmap](ROADMAP.md):

1. **Reliability first:** an independent, pre-registered transcription sample of the Seraphinianus; multiple Voynich transliterations and segmentations.
2. **Better units:** learn sub-word tokens on training pages only; test whether `qo`, `iin` and gallows are single signs.
3. **Richer grammars, fairly compared:** finite-state vs. context-free models on identical held-out targets, with synthetic controls of graded difficulty.
4. **Replicate before interpreting:** an exact replication of Montemurro & Zanette (2013); topic-varying generators and copy-and-edit models as baselines.
5. **Linguistic collaboration:** identify which latent units could carry structure-dependent rules (Moro).

## Repository map

| Path | What is inside |
|---|---|
| [`docs/`](docs/) | The public website (static HTML/CSS/JS, no build step): story, results, interactive lab, methods, hypotheses |
| [`reports/`](reports/README.md) | Readable reports, from the consolidated snapshot back to the first experiments |
| [`research/grammar_comparison/`](research/grammar_comparison/README.md) | Main comparative experiments E01–E11 and their outputs |
| [`research/patterns/`](research/patterns/README.md) | Word families, positional patterns, word-pair associations |
| [`research/substitution_attack/`](research/substitution_attack/README.md) | E12: C++/Python simple-substitution solver with positive controls |
| [`research/`](research/README.md) | Inventory, final-*m* test, controls and section classifier (earliest studies) |
| [`scripts/`](scripts/README.md) | Download sources with hash checks, reproduce suites, pre-publication checks |
| [`DATA_SOURCES.json`](DATA_SOURCES.json) | Every external source: URL, SHA-256, rights note, local path |

## Reproduce in five commands

```bash
git clone https://github.com/fabiofurini/voynich-seraphinianus-lab
cd voynich-seraphinianus-lab
pip install -r requirements.txt          # NumPy; Pillow only for the OCR image panel
python scripts/fetch_data.py             # downloads exact source versions, verifies SHA-256
python scripts/reproduce.py --suite matched
```

Other suites: `affixes`, `hierarchy`, `calibration`, `multiscale`, `boundary`, `substitution`. Details and caveats in [REPRODUCIBILITY.md](REPRODUCIBILITY.md). To view the website locally: `python -m http.server 8000 --directory docs`.

## Cite, reuse, contribute

- **Cite** with [CITATION.cff](CITATION.cff). Please describe this work as exploratory analysis, never as a decipherment.
- **Licences:** code MIT; original text and derived tables CC BY 4.0. Third-party sources keep their own terms and are not redistributed ([RIGHTS.md](RIGHTS.md)). Voynich images on the website come from the Beinecke Library (public-domain work); no Seraphinianus images are reproduced.
- **Contribute** through issues and pull requests: state a hypothesis, corpus version, segmentation, split, control and the result that would prove it wrong ([CONTRIBUTING.md](CONTRIBUTING.md)).

Project by **Fabio Furini**, developed with AI assistance and open to independent verification. Snapshot of 18 October 2026, version 0.2.0.
