# SOURCES.md — slide 016 (annotated Figure 1: 5 callouts)

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Machine-verified 2026-10-11 via WebFetch of
arXiv HTML v7 (no vision calls run; no image access — frame facts below come from
the verified vision pass description of 2026-10-11).

## Slide identity

- New (curated) slide **016** ← old extraction slide **30**
  (`unique_slides/new2old_mapping.json`), frame `unique_slides/slide_016.jpg`.
- Frame facts (vision pass, ground truth): a single recolored Figure 1 (course
  style) annotated with **5 callouts**: "Decoder Block", "Encoder Block",
  "N cascaded blocks", "Encoder-Decoder Attention", "V,K,Q input sources".

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]

## Figures used by this slide

**Per-figure use: Figure 1 ONLY** (consistent with the vision verification; this
slide does not draw on Figure 2 left/right).

- **Figure 1** — caption (verbatim, v7): "Figure 1: The Transformer - model
  architecture."
- Founder-downloaded original already banked in
  `../slide_18_source/The Transformer - model architecture..png` (1520×2239) —
  **do not modify that dir's files**; this slide references it. No new figures
  were downloaded into this dir.
- arXiv v7 asset provenance (verified live, byte-identical to the founder's
  download — 159,152 bytes):
  https://arxiv.org/html/1706.03762v7/Figures/ModalNet-21.png
  (in-page src `1706.03762v7/Figures/ModalNet-21.png`, id `S3.F1.g1`).

## What the paper CONFIRMS (data behind each callout)

- **"Decoder Block" / "Encoder Block"** — the paper's architecture is exactly an
  encoder block-stack plus a decoder block-stack: "The Transformer follows this
  overall architecture using stacked self-attention and point-wise, fully
  connected layers for both the encoder and decoder" (§3.1).
- **"N cascaded blocks"** — "The encoder is composed of a stack of N=6 identical
  layers" and "The decoder is also composed of a stack of N=6 identical layers"
  (§3.1). The paper's value is **N = 6**; the slide's "N" glyph in Figure 1 is the
  paper's.
- **"Encoder-Decoder Attention"** — the paper names the construct verbatim
  (§3.2.3): "In 'encoder-decoder attention' layers, the queries come from the
  previous decoder layer, and the memory keys and values come from the output of
  the encoder." Also §3.1: the decoder "inserts a third sub-layer, which performs
  multi-head attention over the output of the encoder stack."
- **"V,K,Q input sources"** — §3.2.3 gives the exact sourcing per attention type:
  self-attention (encoder): "all of the keys, values and queries come from the
  same place, in this case, the output of the previous layer in the encoder";
  self-attention (decoder): same rule within the decoder; encoder-decoder
  attention: Q from the previous decoder layer, K and V (memory) from the encoder
  output. The callout is a faithful compression of this.

## Course-authored elements (no paper counterpart — not paper data, do not "fix" to paper)

- The callout style/anchoring and the recoloring are course presentation
  choices; the paper's Figure 1 has no callouts.

## [?] Uncertain items

- RESOLVED (raw): anchors per the raw's recreation brief — 'Decoder Block' →
  decoder container; 'Encoder Block' → encoder container; 'N Cascaded Blocks'
  → both Nx circles; 'Encoder Decoder Attention' → the yellow/red-dashed
  highlight region straddling the panel boundary (encoder output → decoder
  cross-attention V,K); the two 'Inputs to …' callouts → the encoder and
  decoder input paths respectively.
- RESOLVED (raw): callout wording pinned verbatim, and there are SIX boxes,
  not 5 — the "V,K,Q input sources" theme is two separate boxes:
  'Inputs to Encoder Block (V,K,Q) / All are from Previous Block' and
  'Inputs to Decoder Block (V,K,Q) / (V,K) from Attention, (Q) from Previous
  Block'. On-frame spelling is unhyphenated 'Encoder Decoder Attention'. Both
  wordings match §3.2.3's sourcing rules.

## Corrections

none — raw transcription consistent with paper labels (capital-H attention
labels; per diagram 5× Add & Norm, 2× Feed Forward, 2× Multi-Head Attention,
1× Masked; V/K/Q circle sourcing matching §3.2.3 — encoder: all from previous
block; decoder cross-attention: V,K from encoder output, Q from previous
block). Note: the earlier pass counted "5 callouts"; the raw pins 6 boxes
(encoder-side and decoder-side V,K,Q callouts are separate).

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout, verbatim
text, drawn content). This source confirms/corrects DATA and records provenance; it
never licenses inventing or "improving" content the slide doesn't show. If source
and slide disagree, record the discrepancy above — the slide wins for recreation,
the source wins for understanding.
