# SOURCES — slide 43 — "Batch Normalization"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_043_vision_2026-10-11.txt` (2026-10-11,
default `images` route, thinking=high, streamed — banked by this worker).

## Slide content (from the vision transcript — ground truth)

- Title "Batch Normalization" (badge 43). Pattern-group **P3** with slides 42/44
  (shared cube-diagram family — verified once, referenced here):
  - LEFT: unlabeled 3-D cube block (stacked channel slabs, one orange slab
    highlighted).
  - CENTER callout (yellow box, red border): "Batch Normalization — Calculate
    (then Normalize) μ, σ for ALL Samples in the batch (for each channel)".
  - RIGHT: same cube block as slide 42's right-hand diagram, with the three
    double-headed red axis arrows "Feature Vector" / "Channels" / "Batch size".
  - BOTTOM panel (green border): "Batch Normalization Calculate Mean and Variance
    of Each Mini-Batch instead of Calculating Mean and Variance of the Whole
    Data." / "The mean and variance will differ from mini-batch to another
    (Source of Error)." / "Mini Batch Size should be large enough to minimize
    'batching' effect. (Constrain)".

## 1. Source URLs (fetched live 2026-10-11)

- Ioffe, S. & Szegedy, C. (2015), "Batch Normalization: Accelerating Deep Network
  Training by Reducing Internal Covariate Shift", ICML 2015 —
  https://arxiv.org/abs/1502.03167 (verified live 2026-10-11). Definition ground
  truth: normalize each activation by the mean/variance computed over the mini-
  batch (per channel, across all batch samples + spatial positions).
- Wu, Y. & He, K. (2018), "Group Normalization", ECCV 2018 —
  https://arxiv.org/abs/1803.08494 — **Figure 2 "Normalization methods"
  (`all_norms.svg`, banked at `../slide_042_source/all_norms.svg`)**: its FIRST
  subplot is exactly this slide's picture — one channel's slice extended over ALL
  batch samples (N axis) is the region normalized by the same μ/σ. The family
  verification (axis labels N/C/H-W ≡ course Batch size/Channels/Feature Vector)
  is recorded in `../slide_042_source/SOURCES.md`.
- agy (2026-10-11, 2 queries in the 41/42 research): Figure 2 of Wu & He is the
  canonical published contrast of these normalization slices.

## 2. Downloaded figures

- None new for THIS slide (course-redrawn cube diagrams). The family figure bank
  lives at `../slide_042_source/all_norms.svg` (Wu & He Fig 2; 4 subplots verified).

## 3. What the sources CONFIRM

- The callout's semantics: BN computes μ, σ **per channel over ALL samples in the
  mini-batch** — exactly Ioffe & Szegedy's definition (per-feature/ per-channel
  statistics over the batch dimension) and exactly the GN paper's Fig 2 BatchNorm
  subplot (blue pixels = one channel across all N).
- "Each Mini-Batch instead of … the Whole Data" — confirmed: BN estimates batch
  statistics per mini-batch rather than full-dataset statistics (Ioffe & Szegedy
  §2/§3).
- "The mean and variance will differ from mini-batch to another (Source of
  Error)" — confirmed: batch-statistics estimation noise is BN's known weakness;
  Wu & He §1 ("BN's error increases rapidly when the batch size becomes smaller,
  caused by inaccurate batch statistics estimation").
- "Mini Batch Size should be large enough" — confirmed as the standard constraint
  (same source; batch-size sensitivity motivates GN/LN).

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- Course restricts the normalized region to "for each channel" WITHOUT naming the
  spatial axes (its "Feature Vector" axis plays the H,W role); the paper normalizes
  over (N,H,W) per channel. Same semantics; course vocabulary kept.
- The drawn cube colors (magenta/green/orange/yellow slab checker) are the
  course's; GN Fig 2 uses a blue-slice highlight. Style difference, not content.

## 5. Numeric verification

- n/a (0/0) — no numeric values on the slide (badge 43 only).

## 6. Open questions

- [?] Exact pixel origin of the course's cube drawing (instructor-made or adapted
  from a blog figure; the transcript itself says no exact published match can be
  asserted). Axis semantics CONFIRMED via Wu & He Fig 2 — the pixel style is the
  course's (Part I precedent).

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (second web-verification worker, 2026-10-11 — appended, nothing above edited)

- Independent Ioffe & Szegedy abs fetch (1502.03167) confirms the definition
  verbatim: "making normalization a part of the model architecture and performing
  the normalization for each training mini-batch."
- Independent Wu & He ar5iv fetch confirms the BatchNorm subplot semantics: the
  blue region = one channel's slice extended over ALL batch samples (N axis) —
  exactly this slide's "for ALL Samples in the batch (for each channel)".
- No script-12 raw exists for 043; both independently banked vision transcripts
  (this worker's + second worker's) agree on all strings, including the
  μ, σ callout and the three bottom paragraphs.

## Raw-landing verification (slide 43, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_043_raw.json` (script-12; kept frame frame_03541.jpg, t≈3392–3540 s, old
  extraction 112) now EXISTS and was read in full: every string agrees verbatim with this
  record — cream callout "Batch Normalization" (red bold) / "Calculate (then Normalize)
  μ, σ" (μ, σ red) / "for ALL Samples in the batch" ("ALL Samples" bold blue) / "(for each
  channel)" (green, underlined) with the pencil icon bottom-left; bottom green-bordered box
  with the three paragraphs exactly as recorded (incl. black "(Source of Error)." and the
  red "Mini Batch Size should be large enough to minimize \"batching\" effect.  (Constrain)");
  two cube stacks; three red double-headed arrows on the right stack ("Feature Vector"
  rotated 90° reading bottom-to-top, "Channels" horizontal, "Batch size" diagonal); badge 43;
  thin black bottom strip (frame artifact).
- Raw cube details for the build: left stack front face 4×4 magenta with orange right-face
  column and navy/yellow/green/orange top bands; right stack same style with green / orange /
  yellow / light-blue #6699CC / navy receding slices. The cube-pixel-style [?] above stands
  (course redraw; axis semantics confirmed via Wu & He Fig 2 + Ioffe & Szegedy — unaffected).
- No corrections; no new open questions.

## Recreation cross-check (build worker, 2026-10-12 — appended, nothing above edited)

The build's PIL census + crop-vision rounds corrected/refined the spec's vision-model
guesses (frame wins per the fidelity law; the recreation follows these):

1. **"(Constrain)" is BLACK, not red.** B-L3's red cores end at x718 (frame); dense
   black cores ((0,0,0)/(22,22,22)) span x732..831 = "(Constrain)". The spec's
   PASS_WITH_FIXES item "line 3 is entirely red" is overridden by the frame.
2. **Callout line 3 coloring:** blue ink spans x376..598 continuously = "ALL Samples
   in the batch" is ALL blue; black cores only at 348..368 = "for ". So the line reads
   "for " (black regular) + "ALL Samples" (blue BOLD) + " in the batch" (blue regular —
   the blue-cluster density drops after "Samples", and the judge crop-read confirms the
   selective bold). The spec's "'ALL Samples' only, rest black" is overridden.
3. **Left stack structure (the build's decoded model):** 5-layer batch block, 3 visible
   magenta front columns x 5 rows (seams = bright 4-5px vertical bands at x139/169/200,
   spanning the full front height), DEEP top faces (dx 44.5 — each top band extends to
   ox+133 with a bright seam lattice), and a connected deep right wall (dx 44.5
   parallelograms in engine paint order) whose partial coverage produces the measured
   strips [204..231.5 rust #D05127][231.5..246 salmon #EB4D42][246..262 dark-gold
   #D4A108][262..283 orange #E47C09][283..296 bright-gold #F2A614][298..314.5 tan
   #CA8537] with staircase tops 188/164/151/111/107 (at x210/240/255/285/300).
   OPEN [?]: the frame splits the front layer's deep right at x=231.5 into rust+salmon
   sub-strips (stable across all rows) — read here as the "orange column slice" front +
   its right face; exact provenance unverified. The wall/sliver colors are the frame's,
   NOT the 042 layer palette (measured; the right stack keeps the 042 palette exactly).
4. **The pencil icon** is TINY (~15x16fp at [354..368]x[243..259], a thin light-gray
   diagonal stroke with a small dark tip, left of line 4's parenthesis) — earlier
   "pencil bbox x348..399 y235..260" measurements had mixed in line 3's baseline ink
   and line 4's "(" glyph.
5. **Omitted as video-capture artifacts** (ground rule (c)): the bottom letterbox strip
   and the full-height pale I-beam cursor line at x615 (spans y42..516 — the 042 x330
   artifact class).
