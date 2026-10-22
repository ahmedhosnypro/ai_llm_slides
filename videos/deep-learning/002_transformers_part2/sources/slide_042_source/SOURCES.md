# SOURCES — slide 42 — "Batch Data (Feature Vectors)"

Researched: 2026-10-11 (web-research worker, slide-recreation pipeline).
Vision transcript of record: `transcripts/slide_042_vision_2026-10-11.txt` — BANKED
by the previous (interrupted) run, 2026-10-11, default `images` route, validated
winner; reused verbatim by this worker (no re-probe spent).

## Slide content (from the banked transcript — ground truth)

- Title "Batch Data (Feature Vectors)" (badge 42). Three boxed illustrations, left
  to right, increasing tensor rank:
  1. "Feature Vector of One Input Sample (Using one filter)" — a 1×5 column of
     lime-green 3-D cubes.
  2. "Feature Vectors of One Input Sample (Using 4 filters) [ 4 Channels]" — a 5×5
     plane of green cubes.
  3. "Feature Vectors of : / FIVE Input Samples [mini-Batch] / Using 4 filters
     [ 4 Channels]" — a 3-D cuboid of 5 parallel 5×5 slabs (front slab magenta,
     then orange, yellow, blue-gray), with three double-headed red axis arrows:
     "Feature Vector" (vertical), "Channels (4 Filters)" (horizontal),
     "Batch size (5 samples)" (diagonal/depth).
- Known frame-internal discrepancy (flagged by the transcript): 5 columns are DRAWN
  where the label says "4 filters [ 4 Channels]" — recreation keeps the frame.
- This is CNN-background material on batched feature-map tensors (NOT a transformer
  figure), used in the lecture as the setup for the normalization block (slide 41
  precedes it; 43–44 continue the same diagram family — pattern group P3).

## 1. Source URLs (fetched live 2026-10-11)

- Wu, Y. & He, K. (2018), "Group Normalization", ECCV 2018 —
  https://arxiv.org/abs/1803.08494; ar5iv render
  https://ar5iv.labs.arxiv.org/html/1803.08494 — **Figure 2 "Normalization
  methods"** (figure id S2.F2). Caption (verbatim from the render): "Each subplot
  shows a feature map tensor, with N as the batch axis, C as the channel axis, and
  (H, W) as the spatial axes. The pixels in blue are normalized by the same mean
  and variance, computed by aggregating the values of these pixels."
- agy (2026-10-11, 2 queries): identifies Wu & He Figure 2 as the canonical
  published illustration of a (N, C, feature) tensor with labeled batch/channel
  axes; CS231n-style tutorials depict batch tensors but never label this axis
  triple with highlighted slices.

## 2. Downloaded figures

- `all_norms.svg` — Wu & He Figure 2 (all four normalization subplots), fetched
  from `https://ar5iv.labs.arxiv.org/html/1803.08494/assets/all_norms.svg`
  (184,742 B, 820×215, sha256[:16] f5f57e932869f740; 4 subplot clip-regions
  verified programmatically at x≈24–191 / 231–397 / 437–603 / 643–810).
  **This is the shared diagram family bank for pattern group P3 (slides 42, 43,
  44)** — see also `../slide_041_source/SOURCES.md` (taxonomy) and 43/44's own
  SOURCES.md records.

## 3. What the source CONFIRMS

- The course's right-hand cuboid reproduces the GN-paper figure's axis structure:
  batch axis (course "Batch size (5 samples)" ≡ N), channel axis (course
  "Channels (4 Filters)" ≡ C), feature/vector axes (course "Feature Vector" ≡ the
  spatial/feature plane). The course's "[ 4 Channels]" label coincides with the
  paper figure's small channel count (drawn with few channels so slices are
  visible).
- The progression one filter → 4 filters (channels) → mini-batch of samples is the
  standard tensor-rank ladder used to introduce batched normalization.

## 4. Course vs source discrepancies (recreation keeps course verbatim)

- Course relabels H,W as a single "Feature Vector" axis and draws 5×5 cubes per
  slab; the paper figure uses image-shaped feature maps. Course numbers (5 samples,
  4 channels, 5-vector) are course-illustrative; the drawn 5-columns-vs-"4 filters"
  mismatch is a course artifact (frame wins).
- The course cube colors (magenta/orange/yellow/blue-gray slabs) are NOT the GN
  figure's blue-slice highlight scheme — the course uses slab colors to separate
  batch members. [?] whether 43/44 recolor slices to mark normalization regions
  (that would be the direct Figure 2 analogue) — resolved by 43/44's own records.

## 5. Numeric verification

- "FIVE Input Samples [mini-Batch]", "(5 samples)", "4 filters", "[ 4 Channels]",
  "one filter" — no external numeric claims to verify (course illustration
  constants). n/a beyond the drawn-vs-labeled count noted above.

## 6. Open questions

- [?] Exact upstream source of the course's cube style (possibly a freelance CNN
  tutorial; nothing published matches the exact 5×5×5 green-cube rendering). The
  axis structure and taxonomy are CONFIRMED via Wu & He; the pixel style is the
  course's own (Part I precedent: course redraws figures).
- [?] Whether the GN paper figure's own sample/channel counts (the figure draws 3
  samples × 4 channels) influenced the course's "4 Channels" label — plausible,
  unprovable from the caption; recorded as suggestive only.

## Corrections

none yet — verify against script-12 raw transcription when it lands.

## Cross-check (second web-verification worker, 2026-10-11 — appended, nothing above edited)

- Independent Wu & He ar5iv fetch agrees: Figure 2 = `all_norms.svg`
  (figure id S2.F2), caption axes N (batch) / C (channel) / (H,W) spatial; BN
  subplot normalizes over (N,H,W) per channel. agy's generic "CS231n" answer
  (this worker's own query) was equally non-specific — the [?] on cube-style
  provenance stands.
- Byte-identical copy of `all_norms.svg` (sha256[:16] f5f57e932869f740) re-verified
  at `../slide_044_source/all_norms.svg` (family bank duplicated into 44's dir per
  the download rule; canonical reference stays `slide_042_source/all_norms.svg`).
- No script-12 raw exists for 042 (only 041/046/048/049/050 of this range have
  raws) — the vision transcript of record is the sole frame evidence; both the
  banked transcript and the second worker's independent transcript agree on all
  labels and on the 5-drawn-vs-"4 filters" mismatch.

## Raw-landing verification (slide 42, 2026-10-11 — raw pass; nothing above edited)

- `analysis/slide_042_raw.json` (script-12; kept frame frame_03392.jpg, t≈3305–3391 s, old
  extraction 111) now EXISTS (the cross-check above predates it) and was read in full. It
  RESOLVES the flagged frame-internal discrepancy: the middle diagram is drawn as a
  **4-column × 5-row grid of 20 cubes** (raw: "4 columns x 5 rows = 20 identical green
  cubes") — the drawn channel count MATCHES the "[ 4 Channels]" label; the earlier
  "5 columns drawn" reading is SUPERSEDED. The right block is five **4-wide × 5-tall**
  cube layers, front-to-back magenta #CC00CC / yellow #FFD700 / orange #FF7F00 / green
  #00A800 / blue #4477AA, with the three red double-headed dimension arrows ("Feature
  Vector" vertical, "Channels (4 Filters)" horizontal, "Batch size (5 samples)" diagonal)
  and a small down-right stacking arrow between the magenta and yellow layers. Left
  diagram: 1-wide × 5-tall green cube stack. All label strings agree verbatim (incl. the
  "FIVE  Input Samples  [mini-Batch]" and "with 4 filters)  [4 Channels]" double spaces).
- Build note: draw the middle grid 4×5 per the raw. The two transcripts' slab-color readings
  differ (earlier: magenta/orange/yellow/blue-gray; raw: magenta/yellow/orange/green/blue) —
  PIL-check `unique_slides/slide_042.jpg` slab order at build time [?].
- The SOURCES_MAP 042 row's "5 columns drawn vs 4 filters (course artifact)" flag is
  superseded by this resolution (dated append recorded in the map).
- No source changes: Wu & He Figure 2 axis mapping (N/C/feature ≡ Batch size/Channels/
  Feature Vector) and the course-redraw [?] are unaffected by the count resolution.
