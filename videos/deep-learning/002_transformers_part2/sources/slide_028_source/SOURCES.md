# SOURCES.md — slide 028 "Sequence of 9 words — Positions are defined as angles"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_028_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1). Deps: `28 ← [27, 26]`; old extraction group 60 was
SPLIT by the founder into new slides 028 (mid-group state, founder frame swap
kept `frame_01605.jpg`) and 029 (final state, `frame_01653.jpg`). No new agy
query spent — the source family was verified on slides 021/022/023/027 and
this slide adds no new claims beyond 027's.

## Slide identity

- New (curated) slide **028** ← old extraction **60** (split with new slide
  029; shown t≈1584–1652 s) (`unique_slides/slides_index.json`), frame
  `unique_slides/slide_028.jpg`.
- Frame facts (vision transcript): same three-line heading as 027 but
  "Sequence of **9** words / Positions are defined / as angles"; badge "28".
  Same clock-face diagram scaled up: pale-yellow circle, 9 dotted red radial
  diameters, nine green chips "Word 0"…"Word 8" counterclockwise (Word 0 at
  3 o'clock/0°, Word 6 at 9 o'clock/180°, Word 8 near the bottom/lower-right
  region), nine curved orange arrows each labeled "+ω". Same pale-yellow
  inset box: "Sin(ω t)" / "Cos(ω t)" / "t=0,1,2,3,....". Mouse-cursor
  artifact overlapping "Word 1" (recording artifact).

## Relationship to the family

- **Direct sibling of slide 027** (same composition, 5 words → 9 words) and
  a state of the old group that continues on slide 029. The concept, the
  inset, and the +ω arcs are identical to 027's; the delta is only the
  sequence length (5 → 9), which extends the rotation past 90° (Word 6 at
  180°) and past half-circle into the fourth quadrant (Word 8) — visually
  making the course's point that positions keep accumulating angle as t
  grows while the encoding stays on the same circle.

## Primary sources (family bank)

1. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live-verified on slide 027's run; both figures —
   `positional_encoding.png`, `time-steps_dot_product.png` — already
   downloaded in the family bank `../slide_027_source/`; not duplicated
   here). Source of the [sin(ωt); cos(ωt)] circle/rotation pedagogy this
   slide redraws; the 9-word version is the course's own example length.
2. **arXiv 1706.03762v7 §3.5** (live curl banked at
   `../002…/scratch/webverify/paper_v7.html`) — sin/cos PE formulas at
   integer positions; "for any fixed offset k, PE_{pos+k} can be represented
   as a linear function of PE_pos" (the +ω step property); wavelengths from
   2π to 10000·2π (the circle geometry generalizes to higher-frequency
   pairs — the 2-D drawing is the first pair only).
- The vision transcript again judges the drawing course-authored ("appears
  instructor-drawn (PowerPoint-style)"); no published figure matches it
  verbatim.

## What the source CONFIRMS

- Same confirmations as slide 027 (angles as positions, Sin(ωt)/Cos(ωt)
  readout, +ω constant increment, t = 0,1,2,3,…), now demonstrated for 9
  positions. Nothing new is claimed; nothing contradicts the sources.

## Figures used by this slide

- None downloaded here (see the family bank `../slide_027_source/`). The
  clock diagram is course-drawn.

## Course-authored elements

- The 9-word example (vs Kazemnejad's generic t and the paper's d_model
  pairs), the 40°-step geometry (360°/9, unstated numerically), chip
  styling, badge "28".

## [?] Uncertain items

- [?] Exact per-word angles in the drawing (transcript reads 40° spacing
  with Word 3 at the top — i.e. possibly 9 words at 40° = full circle;
  geometry reading has minor transcription ambiguity around Word 5/Word 8
  positions). Frame wins; confirm at build time from the frame.
- [?] Why 9 words (course choice; possibly to reach beyond 180° and show
  wrap-around). Not a source question — recorded as course-authored.

## Corrections

- none.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This
source confirms/corrects DATA and records provenance; it never licenses
inventing or "improving" content the slide doesn't show.
