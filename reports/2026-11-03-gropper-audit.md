# Gropper 2026 — initial independent audit (3 November 2026)

## Scope and provenance

This is a **summary-level audit**, NOT a reproduction of Gropper's original experiments. Source: Gropper (2026), *What the Voynich Manuscript Says: Nothing*, SSRN DOI 10.2139/ssrn.7367158, 17-page PDF, SHA-256 `d3454275842f5569be072ec8a4580e96fd2b8b7d3cdc9ea2e31bfefa86a8ef82`. Its appendix points to Zenodo DOI 10.5281/zenodo.22152069. The DOI URL was inaccessible through the available web retrieval and the execution environment has no DNS/network access, so **no Zenodo code or data were imported and no Gropper script was executed**. SSRN publication metadata was accessible.

## Independently recalculated from this repository's published outputs

Input: `research/patterns/results.json` (ZL3b, strict P0 sample, commas split): 25,373 tokens in 2,952 lines = **22,421 within-line adjacent pairs**. Observed immediate identical-word pairs 218, expected under exact within-line permutation 210.8628856. Hence 218/22421 = **0.9723%**, expected 210.8628856/22421 = **0.9405%**, observed/expected 1.0338. Observed 218 lies inside the 499-shuffle reported range [174,254]. Thus our null **does not establish a global immediate-repeat excess**, even though local examples and selected pairs are striking. Gropper reports 0.83–0.87% on a different sample (PDF p. 17); this numerical difference is **not** evidence of an error until matching filters, segmentation and denominator.

Input: `research/early_studies/voynich_sections.json`: **34/39 = 87.1795%** correct labels (20 herbal, 19 bathing) for one recorded configuration, with hand 2 and Currier B fixed, leave-one-quire+bifolio-group-out, 30 randomly sampled interior words/page. A simple Wilson 95% binomial descriptive interval is **[0.7329, 0.9440]**, but this ignores dependence between pages and grouping and MUST NOT be read as a valid inferential confidence interval. The existing permutation-reference p≈0.012 does not control for quire/location. Gropper's reported vanishing within-scribe topic signal (PDF p. 14) and ours address **different samples, metrics and controls**. Their claims cannot yet be declared contradictory.

An independent toy check shows first-order conditional character entropy is exactly invariant under a bijective symbol relabelling, but this checks only the mathematical identity, not any measured Voynich entropy, segmentation or plaintext-language exclusion.

## Verdict / blockers

- **Available and checked:** SSRN preprint, our GitHub original scripts and stored numerical outputs, above arithmetic cross-checks.
- **Not available / not run:** original Gropper Zenodo archive; replication code, 10-slot grammar, generator, matched entropy estimates, line-initial statistic, compression ratio, and topic-scribe results.
- **Do not report:** 'Gropper's results reproduced', 'paper disproved', 'text meaningless', or 'our topic signal proves semantics'.
- **Next required action:** obtain a working Zenodo archive or direct ZIP from the author and pin its SHA-256; run in an isolated local environment, inspect licenses before importing source/data to this repository, then execute the pre-specified experiments against harmonised samples.

Script for the independently executed arithmetic and toy identity: `research/gropper_2026/verify_summary.py`.
