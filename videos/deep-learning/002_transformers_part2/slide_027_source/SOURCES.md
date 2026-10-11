# SOURCES.md — slide 027 "Sequence of 5 words — Positions are defined as angles"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_027_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + live curl of the Kazemnejad tutorial (page + two
figures downloaded) + the paper fetch banked on slide 021's run. Child of
slide 026 (dep `28 ← [27, 26]`).

## Slide identity

- New (curated) slide **027** ← old extraction **58** (kept frame
  `frame_01583.jpg`, shown t≈1509–1582 s) (`unique_slides/slides_index.json`),
  frame `unique_slides/slide_027.jpg`.
- Frame facts (vision transcript): three-line title top-left "Sequence of 5
  words / Positions are defined / as angles" (dark red); badge "27". A
  clock-face diagram: pale-yellow circle, 12 dotted red radial spokes at 30°,
  five green chips "Word 0"…"Word 4" placed at 0°, 30°, 60°, 90°, 120°
  counterclockwise, orange curved arrows between consecutive words each
  labeled "+ω". Pale-yellow inset box (left): "Sin(ω t)" / "Cos(ω t)" /
  "t=0,1,2,3,....". Mouse-cursor artifact inside the circle (recording
  artifact); black letterbox bar at frame bottom.

## Primary sources

1. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl 2026-10-11, `scratch/webverify/kazemnejad_pe.html`). This is
   the canonical published presentation of EXACTLY this slide's idea —
   encoding position t as a point rotating on a circle and reading off
   [sin(ωt); cos(ωt)]. The blog's proposed method builds each positional
   vector from sine/cosine pairs, p_t = [sin(ω₁t), cos(ω₁t), …,
   sin(ω_{d/2}t), cos(ω_{d/2}t)], and its intuition section frames positions
   as clock/rotation ("we can think of each of these 2-D values as… a needle
   of a clock" framing); its rotation-matrix result (p_{t+φ} is a linear
   function of p_t for fixed φ, independent of t) is the "+ω per step"
   property. Figures downloaded into this dir, originals unrenamed:
   - `positional_encoding.png` (1070×517, 43,159 B) — Figure 2: the 2-D
     sin/cos position-encoding plot (point on circle at successive t).
     Byte size matches the Part II SOURCES_MAP record exactly.
   - `time-steps_dot_product.png` (786×632, 30,320 B) — Figure 3: dot
     product of position embeddings over time-steps. (Stored here as the
     family's pair; the slide itself shows only the circle concept.)
   NOTE: the slide does NOT copy either figure's pixels — the vision
   transcript judges the drawing "a custom clock/angle analogy diagram, not
   a verbatim copy of a well-known published figure". Kazemnejad's figure is
   therefore the concept/figure-family origin (HIGH origin), the drawing is
   course-authored.
2. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11,
   `scratch/webverify/paper_v7.html`) — the formulas behind the inset:
   PE(pos,2i)=sin(pos/10000^(2i/d_model)), PE(pos,2i+1)=cos(…) and "for any
   fixed offset k, PE_{pos+k} can be represented as a linear function of
   PE_pos" (the +ω/arithmetic-sequence-of-angles framing).

## What the source CONFIRMS

- "Positions are defined as angles": Kazemnejad's circle/rotation framing —
  position t ↔ angle ωt on a unit circle; coordinates (cos ωt, sin ωt).
- The inset Sin(ωt) / Cos(ωt) with t = 0,1,2,3,…: the blog's 2-D building
  block [sin(ωt); cos(ωt)] evaluated at integer time-steps; paper §3.5's
  sin/cos PE at integer positions.
- The "+ω" constant angular increment between consecutive words: the
  constant-step rotation property (uniform discrete steps of ω per token),
  and the paper's fixed-offset linearity property.
- Five words (Word 0…Word 4) at 30° steps in the drawing: course example
  (5 is the course's illustrative length; ω = 30° in the drawing's geometry,
  unlabeled — the spokes are generic clock marks).

## Figures used by this slide

- Downloaded (concept-family references, NOT pixel sources):
  `positional_encoding.png`, `time-steps_dot_product.png` (Kazemnejad, as
  above). The slide's clock diagram is course-drawn.

## Course-authored elements

- Three-line title wording, the 5-word example, chip styling, the +ω arc
  annotations, the pale-yellow inset box, badge "27".

## [?] Uncertain items

- [?] Whether ω in the drawing is meant as 30° (the spoke spacing) or is
  symbolic — the slide does not print a numeric value; keep symbolic for
  recreation.
- [?] Whether the course also drew on Brandon Rohrer's circle/"wiggle"
  framing (https://e2eml.school/transformers.html, live per the Part II map)
  — same concept family; no distinctive Rohrer fingerprint visible in the
  transcript. Kazemnejad remains the closest published match.

## Corrections

- none — the slide's math (angles, sin/cos of ωt, integer t) is consistent
  with both sources.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This
source confirms/corrects DATA and records provenance; it never licenses
inventing or "improving" content the slide doesn't show.
