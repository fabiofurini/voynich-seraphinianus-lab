# GitHub Pages deployment

[Home](README.md) · [Stato](STATUS.md) · [Ipotesi](HYPOTHESES.md) · [Esperimenti](EXPERIMENTS.md) · [Metodo](REPRODUCIBILITY.md) · [Documenti](reports/README.md) · [Roadmap](ROADMAP.md)

1. Create public repository `fabiofurini/voynich-seraphinianus-lab` initialized with a README.
2. Upload this checkout to its default branch.
3. Settings → Pages → Deploy from a branch → `main` → `/docs` → Save.
4. Verify the returned Pages URL. Expected project address: `https://fabiofurini.github.io/voynich-seraphinianus-lab/` (not a claim that deployment has occurred).

No build step: docs/index.html, styles.css and app.js are static, with local JSON. Relative paths work under the project subpath. Run python scripts/check_publication.py before pushing updates.

If repository creation is unavailable through the connected tools, the owner must create it once. This local project remains fully reviewable before publication.
