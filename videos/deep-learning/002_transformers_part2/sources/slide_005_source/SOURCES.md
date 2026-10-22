# SOURCES.md — slide 005 "Encoder – Decoder Transformer" (Figure 1 + Figure 2 left + Figure 2 right zoom ladder)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_005.jpg`, badge numeral **5** (matches file id).
- Old extraction: slide 5 ← old 4 (`unique_slides/new2old_mapping.json`).
- Not a declared cross-video dependency child, but its composition is the SAME
  figure family as 001's slide-18/19 family (Fig 1 + Fig 2 left + Fig 2 right);
  provenance carried from the bank.

## Vision transcript of record

- `transcripts/slide005_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. Cross-checked against the
  pre-existing script-12 raw `analysis/slide_005_raw.json` — consistent.

## Primary source

- **arXiv 1706.03762v7 "Attention Is All You Need" (Vaswani et al., 2017)** —
  Figures 1, 2 (left), 2 (right) — ALREADY BANKED, do not re-download:
  - Figure 1 = `../001_transformers_part1/slide_18_source/The Transformer - model architecture..png`
    (ModalNet-21.png, sha256-verified 2026-10-11),
  - Figure 2 left = `../001_transformers_part1/slide_18_source/slide18 scaled dot-production attention figure.png`
    (ModalNet-19.png),
  - Figure 2 right = `../001_transformers_part1/slide_18_source/slide18 Multi-Head Attention\n\n.png`
    (ModalNet-20.png; filename contains literal newlines — always quote).
  Page: https://arxiv.org/html/1706.03762v7 (verified live 2026-10-11; asset URLs
  re-confirmed by agy same day, `../scratch/agy_s004_005.txt`).

## Figures used by this slide (per-figure identity, vision-confirmed)

- **Left inset "Scaled Dot-Product Attention"** = paper **Figure 2 (left)**:
  Q(red)/K(blue)/V(blue) circles → MatMul → Scale → Mask (opt.) → SoftMax → MatMul,
  bottom-up. Course redraw: green-bordered box, pastel fills.
- **Middle inset "Multi-Head Attention"** = paper **Figure 2 (right)**:
  V/K/Q circles → three Linear boxes → one "Scaled Dot-Product Attention" block
  (h parallel copies drawn as stacked shadow duplicates + small brown "h" bubble)
  → Concat → Linear. Course redraw.
- **Right panel** = paper **Figure 1** redrawn in the course's style: Encoder zone
  (peach, red-italic label) + Decoder zone (light green) in a green border;
  Inputs/Outputs (shifted right) → embeddings (maroon) + Positional Encoding
  containers with clock icons → attention blocks with explicit V/K/Q input circles
  → Add & Norm pairs → Feed Forward → Linear → Softmax → Output Probabilities;
  N× on the decoder edge; encoder→decoder cross-connection drawn as red dashed
  curves.
- **Callout banners (course-authored, not in the paper)**: "Both Encoder and
  Decoder Blocks Contain "Multi-Head Self Attention" block" and ""h" Heads /
  Outputs of Heads are concatenated" — same banner wording as 001's slide-18
  family record. Two red dashed connectors tie the left inset to the center
  panel (zoom relation, not data flow).

## Course-authored differences from the paper figures (frame wins for recreation)

- Orange highlight bands over the encoder attention block and decoder
  Multi-Head Attention block; yellow translucent band over the decoder's upper
  Add & Norm/Feed Forward region (teaching emphasis, static in this frame).
- Clock/timer icons beside both Positional Encoding containers; explicit colored
  V/K/Q circles at attention inputs; stacked-shadow rendering of the h heads.
- Decoder column here shows Masked MHA → cross MHA → FF (paper topology, correct).

## What the source CONFIRMS / CORRECTS

- CONFIRMS: all three panels match the paper's figures topologically and
  label-wise; §3.2.1/§3.2.2 back the block sequences; "Mask (opt.)" and
  "h" bubble are the course's rendering choices, consistent with the paper's
  "Mask (opt.)" label and h heads.
- CORRECTED/flagged [?]: the encoder attention block's label in the right panel
  is partially obscured by the orange highlight — probe reads "Attention"
  (partially legible, "consistent with Multi-Head Attention"), raw reads
  "Multi-Head Attention [?]". **Build-time zoom re-check required; frame wins.**
- No equation content ("h", "N×" tokens only; no numeric data).

## [?] Uncertain items

- [?] Encoder attention block label in the right panel (obscured by highlight)
  — build-time zoom re-check; no patch.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows; the banked paper
figures confirm topology/labels and are the build's source images. Discrepancies
are recorded above, never silently "fixed".

## Script-12 raw cross-check (raw-verification worker, 2026-10-11)

- `analysis/slide_005_raw.json` re-read in full (model `images`; old extraction 4;
  kept_frame frame_00058, 28 frames). Consistent with this record on the
  three-panel zoom-ladder composition, banner wording, and overlays.
- [?] STANDS: raw marks the right panel's decoder cross-attention box as
  "Multi-Head Attention [?]" — partially obscured by the orange highlight,
  exactly as the probe did. Build-time zoom re-check remains.
- Raw refinements (frame wins, record for the build):
  - Decoder top reads: Linear → Softmax → small text "Probabilities" → thick red
    block up-arrow → bold "Output" — i.e. "Probabilities" + "Output" as separate
    tokens (slide 004 prints a single "Output Probabilities" chip; cross-slide
    difference, each frame wins).
  - Spelling inconsistency confirmed: "SoftMax" in the left inset vs "Softmax" in
    the decoder stack — preserve both verbatim.
  - The translucent yellow band spans the upper Feed Forward / Add & Norm zone of
    BOTH panels (record said decoder upper region — raw broadens it).
  - Left SDPA inset shows a vertical bypass line along its left inner edge [?]
    (V into the top MatMul) — same motif as slide 019's left panel.
- Script-13 final: NOT YET LANDED for 005. Corrections: none yet — verify against
  script-13 final when it lands.
