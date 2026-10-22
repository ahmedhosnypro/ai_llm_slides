# SOURCES.md — attention/transformer figure bank (slide_18_source)

Provenance record per the video's AGENTS.md research directive. Founder-provided
source + founder-downloaded originals (2026-10-11); machine-verified same day.

> **NUMBERING NOTE (2026-10-11, post-curation):** this analysis was made against the
> pre-curation frame set, when the Encoder–Decoder Transformer slide was extraction
> slide 18 (hence this dir's name). After the founder's curation to 45 slides that
> exact frame was culled, and per the founder these downloaded figures serve the
> family of NEW slides 14, 15, 16, 17, 18, 19 (old extraction 28, 29, 30, 32, 42, 44 —
> see `unique_slides/new2old_mapping.json`). The figure provenance below is unchanged
> and remains the reference for that whole family.

## Primary source

- **URL**: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11)
- **Paper**: "Attention Is All You Need" — Vaswani, Shazeer, Parmar, Uszkoreit,
  Jones, Gomez, Kaiser, Polosukhin (2017), arXiv:1706.03762v7 [cs.CL]
- The slide's three diagram panels are **redrawn versions of the paper's figures**
  in the course's own style/colors (paper topology, slide pixels — course-house
  chrome, pastel fills, Q/K/V shown as colored circles q/k/v instead of letters).

## Downloaded originals (in this dir, untouched as the founder downloaded them)

| File | Paper figure | Caption (as written in v7) |
|---|---|---|
| `The Transformer - model architecture..png` (1520×2239 RGBA) | **Figure 1** | "The Transformer - model architecture." |
| `slide18 scaled dot-production attention figure.png` (445×884 RGBA) | **Figure 2 (left)** | "(left) Scaled Dot-Product Attention. …" |
| `slide18 Multi-Head Attention\n\n.png` (835×1282 RGBA) | **Figure 2 (right)** | "… (right) Multi-Head Attention consists of several attention layers running in parallel." |

⚠️ The multi-head figure's filename contains **literal newline characters**
(`slide18 Multi-Head Attention\n\n.png`). Always quote it in shell (or use the
glob), or work from a copy; never delete or rename the founder's original.

## Mapping to the slide frame (`unique_slides/slide_018.jpg`, 960×540, badge 18)

- Left panel "Scaled Dot-Product Attention" ← Figure 2 left (bottom-up in the
  paper: MatMul→Scale→Mask(opt.)→SoftMax→MatMul; the slide draws it top-down).
- Middle panel "Multi-Head Attention" ← Figure 2 right (Linear×h → Scaled
  Dot-Product Attention ×h → Concat → Linear).
- Right panel ← Figure 1 full architecture (encoder stack Nx orange, decoder
  stack Nx green, positional encodings, Add & Norm, Feed Forward, Linear+Softmax
  → Output Probabilities; "Outputs (shifted right)").
- Banner: "Both Encoder and Decoder Blocks Contain 'Multi-Head Self Attention'
  block" + "'h' Heads / Outputs of Heads are concatenated". Red dashed connectors
  tie the two small panels to the highlighted blocks inside the architecture.

## Data confirmation status

- The slide matches the paper's figures **topologically and label-wise**; no
  data discrepancy found so far. The paper's §3.2.1 defines Attention(Q,K,V) =
  softmax(QKᵀ/√d_k)V and the h=8/64-dim head config the slide's "h Heads" refers to.

## Vision transcripts — PENDING (vision debt banked, not certified)

Per the image-analysis skill law (no real transcript = no PASS): the four planned
default-route calls (frame + 3 figures) did **not** land — gateway window closed
2026-10-11 (attempt 1: HangError @150 s hard wall ×3 internal; attempt 2 after the
§G 300 s backoff: EmptyStreamError ×3 internal at the wider 420 s wall). Both legs
are banked in `transcripts/vision_debt_slide018_2026-10-11.log`; per §R1 this is
recorded debt to re-run when the gateway recovers — likely alongside the slide's
script-12 analysis after the founder approves the frame set. The mapping above
stands on three independent non-gateway reads (agent reads of the frame + all 3
PNGs, and the arXiv caption fetch), labeled **single-session, unconfirmed** — not a
vision-transcript certificate.

## White-composited working copies (machine-generated, safe to delete)

`analysis_work/fig1_transformer_architecture.png`, `fig2_left_scaled_dot_product.png`,
`fig2_right_multihead.png` — the RGBA originals flattened onto white for any future
vision call (transparent-background figures render dark through some backends and
would hide the black text). Originals above are never modified.
