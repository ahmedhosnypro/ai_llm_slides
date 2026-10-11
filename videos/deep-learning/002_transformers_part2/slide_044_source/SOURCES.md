# SOURCES — slide 44 — "Layer , Group, and Instance Normalization"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_044_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker).

## Slide content (from the vision transcript — ground truth)

- Title (verbatim, anomalous space kept): "Layer , Group, and Instance
  Normalization" (badge 44). Heading top-left: "Sample Based Normalization".
- FOUR isometric cube stacks, left to right (pattern-group **P3** with 42/43 —
  shared cube-diagram family):
  1. Reference stack (no caption): axis arrows "Channels" (under front face) and
     "Samples" (along depth).
  2. Group Normalization — "(Group of Channels)" / "General Case": contiguous
     channel-group highlight.
  3. Instance Normalization — "Calculate (then Normalize) μ, σ for ONE Channel in
     ONE Sample (Output of ONE Filter)": single-channel-per-sample highlight.
  4. Layer Normalization — "Calculate (then Normalize) μ, σ for ALL Channels in
     the Same Sample (Input to Same Layer)": whole front face (all channels)
     highlighted; axes labeled "Feature Vector" / "Channels" / "Batch size";
     emphasized by a red outline box + black oval callout "Transformer choice".

## 1. Source URLs (fetched live 2026-10-11)

- Wu, Y. & He, K. (2018), "Group Normalization", ECCV 2018 —
  https://arxiv.org/abs/1803.08494 — **Figure 2 "Normalization methods"**
  (`all_norms.svg`, banked at `../slide_042_source/all_norms.svg`): four subplots
  whose highlighted regions are exactly this slide's four stacks — reference
  tensor, then GN (channel group), IN (one channel in one sample), LN (all
  channels of one sample), over the (N, C, H, W) tensor. Family verification
  recorded in `../slide_042_source/SOURCES.md`; correction: the vision model
  guessed "Figure 1 style" — Figure 1 is ImageNet-error-vs-batch-size; the
  normalization-subplot figure is **Figure 2** (verified from the ar5iv render:
  figure id S2.F2, 4 subplot clip regions).
- Ba, J.L., Kiros, J.R., Hinton, G.E. (2016), "Layer Normalization" —
  https://arxiv.org/abs/1607.06450 (verified live 2026-10-11). LN definition:
  μ, σ computed over ALL hidden units (all channels/features) within ONE sample —
  matches the slide's LayerNorm box verbatim in meaning.
- Vaswani et al. (2017), "Attention Is All You Need" —
  https://arxiv.org/html/1706.03762v7 (already banked in 001's
  `../001_transformers_part1/slide_18_source/`), §3.1: each sub-layer output is
  "LayerNorm(x + Sublayer(x))" — the ground truth behind the slide's
  "Transformer choice" callout on Layer Normalization.
- Ulyanov, D. et al. (2016), "Instance Normalization: The Missing Ingredient for
  Fast Stylization" — https://arxiv.org/abs/1607.08022 — IN definition behind
  caption box 2 (per-sample, per-channel normalization). [Referenced from the
  Wu & He §2 taxonomy; abs page verified live 2026-10-11.]

## 2. Downloaded figures

- None new for THIS slide — the family figure bank is
  `../slide_042_source/all_norms.svg` (Wu & He Fig 2, 4 subplots verified).

## 3. What the sources CONFIRM

- "Sample Based Normalization" grouping: GN, IN, LN all compute μ/σ **per
  sample** (batch-size independent), unlike BN — exactly Wu & He's motivation
  ("GN's computation is independent of batch sizes") and Ba et al.'s LN.
- GN = "(Group of Channels)" + "General Case": confirmed — GN divides channels
  into groups; GN with one group = LN, with all groups = IN (Wu & He §3 — the
  "general case" framing).
- IN = μ,σ for one channel in one sample: confirmed (Wu & He Fig 2 IN subplot;
  Ulyanov 2016).
- LN = μ,σ for ALL channels in the same sample: confirmed (Ba et al. 2016).
- "Transformer choice" on LayerNorm: confirmed — the Transformer uses LayerNorm
  in every Add & Normalize step (arXiv 1706.03762 §3.1).

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- Course order (GN → IN → LN) differs from the paper's subplot order
  (BN → LN → IN → GN); presentation choice, kept.
- Course axes vocabulary: "Feature Vector" plays the paper's (H,W) role; "Samples"
  ≡ N; "Channels" ≡ C. Same tensor, course vocabulary kept.
- "Input to Same Layer" is course phrasing for the transformer's per-layer
  activations; no source conflict.

## 5. Numeric verification

- n/a (0/0) — no numeric values on the slide (badge 44 only).

## 6. Open questions

- [?] Exact pixel origin of the course's cube rendering (instructor-made redraw;
  axis semantics and highlight topology CONFIRMED via Wu & He Fig 2).

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (second web-verification worker, 2026-10-11 — appended, nothing above edited)

- `all_norms.svg` (Wu & He Figure 2) is ALSO banked in THIS dir
  (`slide_044_source/all_norms.svg`, sha256[:16] f5f57e932869f740 — byte-identical
  to `../slide_042_source/all_norms.svg`), per the "download into the slide's own
  dir" rule; this slide is the closest single-figure match of the P3 group.
- Independent Wu & He ar5iv fetch agrees with the scope mapping: BN over (N,H,W)
  per channel; LN over (C,H,W) per sample; IN over (H,W) per sample per channel;
  GN over channel groups, with LN (G=1) and IN (G=C) as its extremes — the
  course's "General Case" framing confirmed.
- Vaswani §3.1 "LayerNorm(x + Sublayer(x))" independently re-verified live (same
  day) — the "Transformer choice" callout's ground truth.
- No script-12 raw exists for 044; the two independent vision transcripts agree on
  all four cube stacks and all three caption boxes.

## Cross-check (parallel web-verification worker, 2026-10-11 — reconciliation note by this worker)

The parallel worker ALSO banked a copy of the family figure into THIS dir:
`all_norms.svg` (byte-identical to `../slide_042_source/all_norms.svg`,
sha256[:16] f5f57e932869f740 — verified on disk by this worker). Either copy
may be referenced; do not re-download.

## Raw-landing verification (slide 44, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_044_raw.json` (script-12; kept frame frame_03679.jpg, t≈3541–3678 s, old
  extraction 113) now EXISTS and was read in full: agrees verbatim with this record — title
  "Layer , Group, and Instance Normalization" centered on the gray top bar (space before the
  comma confirmed), heading "Sample Based" / "Normalization" (blue bold italic), four cube
  stacks (reference with "Samples" + "Channels" arrows; GN magenta/orange channel-group
  split; IN magenta with one orange right-hand column; LN magenta inside a thin red outline
  box with "Feature Vector" / "Channels" / "Batch size" arrows), three caption boxes
  verbatim (incl. "ONE Channel in ONE Sample (Output of ONE Filter)" and "ALL Channels in
  the Same Sample (Input to Same Layer)" with bold green underlined parenthetical), solid
  black oval "Transformer choice" (bold yellow) overlapping the LayerNorm box's right end,
  badge 44.
- Additional frame facts: white mouse cursor on the left salmon cube's front face and a thin
  black bottom strip — both recording artifacts, omit from recreation.
- No corrections; the cube-pixel-origin [?] stands (course redraw; scopes confirmed via
  Wu & He Fig 2 + Ba et al. + Ulyanov + Vaswani §3.1 — all previously live-verified).
