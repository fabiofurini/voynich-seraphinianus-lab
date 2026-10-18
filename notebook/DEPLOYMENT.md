# Website deployment (GitHub Pages)

[Home](../README.md) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](../reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

The website in [`docs/`](../docs/) is static: HTML, one stylesheet, two scripts and images, with no build step. Relative links work under the project sub-path.

The site is bilingual. English pages are in `docs/`, Italian translations with the same file names in `docs/it/`; every page links to its counterpart (EN · IT switch and `hreflang` tags). Both versions share `styles.css`, `app.js`, `lab.js` and `assets/`; the scripts read `<html lang>` and switch chart labels and number format accordingly. **When you change a page, change its translation too.**

**One-time setup (repository owner):** Settings → Pages → *Build and deployment* → Source: *Deploy from a branch* → Branch: `main`, folder `/docs` → Save.

The site is then served at <https://fabiofurini.github.io/voynich-seraphinianus-lab/> and updates on every push to `main`.

| Page | File | Audience |
|---|---|---|
| The story | `docs/index.html` | General readers |
| Results | `docs/results.html` | Everyone; panels for linguists and statisticians |
| Voynich Lab | `docs/lab.html` + `docs/lab.js` | Interactive exploration |
| Methods & tests | `docs/methods.html` | Statisticians, replicators |
| Hypotheses | `docs/hypotheses.html` | Linguists, researchers |
| Italian version | `docs/it/*.html` | Italian-speaking readers |

Preview locally with `python -m http.server 8000 --directory docs`, and run `python scripts/check_publication.py` before pushing.
