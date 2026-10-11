# SOURCES.md — slide 015 "Multi Head Self Attention of Word X_2"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Vision transcript of record: `transcripts/slide_015_webverify.txt` (2026-10-11,
default `images` route, `--thinking high`, via `scripts/16_vision_gate.sh`).

## CROSS-VIDEO RECAP (founding rule for this slide)

`slide_dependencies.json`: **15 ← deep-learning/001_transformers_part1:43**.
Parent record: `../001_transformers_part1/slide_043_source/SOURCES.md`
(verified 2026-10-11): the paper (§3.2.2) + Bloem confirm the multi-head
semantics and the course's "Wide" vocabulary originates from Bloem's post
(update log 19 Oct 2019); course-vs-paper mapping table there (per-head
projections → dot/scale/softmax/weighted-sum → concat → linear
transformation). Per the recap rule that verification CARRIES; only new
visual differences were re-checked here. Sources re-confirmed live this
session (see slide_012 record: §3.2.2 verbatim excerpts + Bloem per-head
W_q^r/W_k^r/W_v^r).

## Slide identity

- Frame `unique_slides/slide_015.jpg`, badge "15". Title (transcript): "Multi
  Head Self Attention of Word X_2" ("Multi Head" and "X_2" in red) — the
  transcript reads the title line at the BOTTOM of the slide [? position;
  zoom before building].
- Frame facts (vision transcript): FIVE head panels stacked in perspective —
  badges **h=1..h=5** (h=1 front, salmon; h=2 lavender, h=3 yellow, h=4
  green, h=5 tan, fading rearward) — each computing **Similarity →
  Probabilities → Weighted SUM** (stage tags repeated per panel). Front
  (h=1) panel detail: orange X-token ellipse + green **W_k** boxes → key
  vectors → beige **"Dot Product"** box (callout **"K.q"**, and above it
  **"K.q / √d"**) → pink **"Scaling by √d"** → pink **"Soft max"** → ⊗
  multiply nodes with **v_1..v_3** → blue **Σ** → per-row blue **W^o** boxes
  → output token strips. Query rail: green-dashed token row **X_1..X_4**
  (X_2 red-highlighted, red pointer) with a red **W_q** box. Right/bottom:
  stacked small red- and blue-outlined weight boxes reading **W_i^Q /
  W_i^K / W_i^V** pattern [? tiny]. Global thick red curved arrow labeled
  **"H Heads"** sweeping bottom-left → top-right across the stack.
- Video artifacts (do not recreate): white mouse cursor over the back
  panels' Similarity tags (~x310,y150); red drawn pointer at X_2; letterbox
  bars top/bottom.

## Primary sources (carried from parent; re-confirmed live 2026-10-11)

- **Vaswani et al. 2017** — https://arxiv.org/html/1706.03762v7 §3.2.2
  (WebFetch-confirmed verbatim this session): heads = Attention(QW_i^Q,
  KW_i^K, VW_i^V) with "different, learned linear projections"; h=8 heads;
  output = Concat(head_1..head_h)W^O. CONFIRMED.
- **Peter Bloem, "Transformers from scratch"** —
  https://peterbloem.nl/blog/transformers (WebFetch-confirmed this session):
  heads r "each with different matrices W_q^r, W_k^r, W_v^r"; per-head
  outputs concatenated then linearly mapped back. CONFIRMED.
- No downloads — course-authored diagram (parent's conclusion stands; the
  stacked-perspective composition is the instructor's own; no published
  figure is redrawn).

## New visual differences vs the 001 parent (fresh-verification notes)

- **Composition**: parent's slide 43 shows the five heads side-by-side with
  an explicit "Concatenated Vector 1×dH" and "Linear Transformation [T]
  dH×d" step; THIS frame stacks the five heads in perspective (h=1..h=5
  badges) with a global **"H Heads"** arrow and NO visible concat/linear-
  transformation labels [? — possibly occluded by the stack or below the
  fold]. The concat+W^O step is the paper's; if genuinely absent here, the
  course may defer it to the next slide (001's 43→44 pattern: 44 = same
  family). Zoom the video frame before building.
- **Per-panel "W^o" boxes**: the transcript reads a small blue W^o per
  output row/panel. In the paper W^O is applied ONCE after concatenation,
  not per head; in the parent's record the linear transformation is the
  post-concat step. If these W^o boxes are per-head output projections,
  that is a COURSE convention (wide-flavor bookkeeping) — recreation keeps
  the course's labels verbatim. [?] tiny text; zoom needed.
- **"K.q / √d"** printed above the Dot-Product box (in addition to the
  "Scaling by √d" stage box): explicit scaled-score notation; consistent
  with the parent's per-head pipeline (Dot Product → Scaling by √d → Soft
  max) and with paper §3.2.1. No discrepancy.
- Weight-box superscripts **W_i^Q/W_i^K/W_i^V pattern [?]** (head indices
  1..5 too small to read): paper-style head-indexed notation (vs 001's
  indexless W^Q/W^K/W^V legend). [?] zoom needed.

## What the sources CONFIRM (carried + re-verified)

- H parallel heads, each with its own learned W_q/W_k/W_v, computing scaled
  dot-product attention (K·q / √d → softmax → weighted sum of V): paper
  §3.2.1–3.2.2. CONFIRMED.
- Course illustrates h=5 heads vs paper h=8: illustration choice (parent's
  record already notes this). Kept verbatim.
- Self-attention framing ("all of the keys, values and queries come from the
  same place", paper §3.2.3 — re-confirmed live this session on the
  slide-014 fetch). CONFIRMED.

## Open questions

- [?] title line position (bottom vs top of slide).
- [?] presence/absence of "Concatenated Vector 1×dH" / "Linear
  Transformation dH×d" labels on this frame (vs parent's slide 43).
- [?] per-panel W^o semantics (per-head projection vs post-concat strips)
  and the W_i^Q/W_i^K/W_i^V tiny superscripts — zoom the video frame
  (t≈slides_index(slide_015)) before building.
