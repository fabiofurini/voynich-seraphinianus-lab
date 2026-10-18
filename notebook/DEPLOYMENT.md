# Website deployment (GitHub Pages)

[Home](../README.md) · [Status](STATUS.md) · [Hypotheses](HYPOTHESES.md) · [Experiments](EXPERIMENTS.md) · [Reports](../reports/README.md) · [Reproduce](REPRODUCIBILITY.md) · [Roadmap](ROADMAP.md)

The website in [`docs/`](../docs/) is static: HTML, one stylesheet, two scripts and images, with no build step. Relative links work under the project sub-path.

**One-time setup (repository owner):** Settings → Pages → *Build and deployment* → Source: *Deploy from a branch* → Branch: `main`, folder `/docs` → Save.

The site is then served at <https://fabiofurini.github.io/voynich-seraphinianus-lab/> and updates on every push to `main`.

| Page | File | Audience |
|---|---|---|
| The story | `docs/index.html` | General readers |
| Results | `docs/results.html` | Everyone; panels for linguists and statisticians |
| Voynich Lab | `docs/lab.html` + `docs/lab.js` | Interactive exploration |
| Methods & tests | `docs/methods.html` | Statisticians, replicators |
| Hypotheses | `docs/hypotheses.html` | Linguists, researchers |

Preview locally with `python -m http.server 8000 --directory docs`, and run `python scripts/check_publication.py` before pushing.
