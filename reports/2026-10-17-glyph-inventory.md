# Voynich: a candidate graphic inventory, not a phonetic alphabet

[Home](../README.md) · [Reports](README.md) · [Experiments](../notebook/EXPERIMENTS.md) · [Current status](../notebook/STATUS.md)

17 October 2026 · Historical document; read it together with the [current status](../notebook/STATUS.md).

## Outcome

A working inventory of **23 graphic units**, built on EVA conventions and on distinctions documented by transcribers. The choice of the six compounds is **not** an automatic discovery: it comes from the documentation of the writing system. What is new here is only the reproducible count and the comparison between two transcriptions, not a scientific claim of novelty.

- 17 forms written with a single EVA label: `a d e f g i k l m n o p q r s t y`
- 6 forms written with compound EVA labels: `ch sh ckh cth cph cfh`

This is not a recovered alphabetical order, and no label assigns a sound to a sign.

## Sample

Paragraph text only: loci P0 in ZL, loci P in H. Fully legible tokens are counted even if other tokens on the same line are uncertain, so this is not the sample of fully clean lines used in other experiments. Ambiguous sequences, special ZL groups and uninterpreted annotations are excluded, as are labels, marginal sequences and circular texts. Graphic tokenisation is maximal: `ckh/cth/cph/cfh/ch/sh` before single characters. Commas are treated as separators; this is a convention, not a result.

| Transcription | Legible text tokens | Graphic units counted | Coverage by the 23 units |
|---|---:|---:|---:|
| ZL3b (2025) | 32,888 | 146,382 | 99.963% |
| Takahashi H, Stolfi archive | 33,017 | 149,575 | 99.795% |

Coverage applies only to text already transcribed and to accepted tokens. It does not include every sign in the manuscript, is not an exhaustive palaeographic check, and does not justify ignoring rare forms.

## Why EVA letters should not be read naively

- In ZL P0, `h` occurs 15,517 times; only 3 fall outside the six compounds. In H, 165 of 15,958 remain outside: the two transcriptions do not segment every case the same way. A connected compound is not thereby a simple letter; it may be a ligature.
- `q` is token-initial in 5,061 of 5,087 cases (99.49%) and is followed by `o` in 4,987 of 5,087 (98.03%). This makes `qo` a candidate unit or prefixed element, without deciding between the two.
- `n` follows `i` in 5,439 of 5,550 cases (98.00%) and ends the token in 5,493 of 5,550 (98.97%). The groups `in/iin/iiin` may need to be treated as distinct units or as a compositional system of strokes.
- Maximal sequences ending in `n` in ZL: `in` 1,601, `iin` 3,688, `iiin` 149, `iiiin` 1. The proposal does not remove this variability in stroke count.
- `m` is kept separate from `r`: earlier experiments do not justify a global merge.

## Working conclusion

We can use 23 units as a working representation with very high coverage. We have **not** shown that they are 23 linguistic letters, and we have not found a correspondence table with Latin, Italian or any other language. The segmentation of `in/iin` and `qo`, and the relation between ligature and letter, remain unresolved. Reconstructing a graphic inventory and phonetic decipherment are distinct results; only the first was attempted here. Assigning values A/B/C to the forms would be arbitrary.

## Sources

- Gabriel Landini, EVA documentation (1998): <https://www.ic.unicamp.br/~stolfi/EXPORT/projects/voynich/work/programs/c/projects/voynich/alphabet-gabriel/eva.htm>. It distinguishes conventions of graphic connection from phonetic interpretation.
- Original EVA reference table: <https://www.voynich.nu/hist/gabriel/eva2_reference.pdf>
- René Zandbergen, analysis of the writing system: <https://www.voynich.nu/writing.html>
- ZL source: version 3b of 13 May 2025, as stated in the file header. Hashes are in [DATA_SOURCES.json](../DATA_SOURCES.json).

## Reproduction

```bash
python research/early_studies/voynich_inventory.py research/patterns/voynich_ZL3b.txt <Stolfi H file> > inventory.json
```

Python 3 standard library only. The [JSON output](../research/early_studies/voynich_inventory.json) contains the frequency of each unit, residual signs and the context distributions of `c/h/q/n`.
