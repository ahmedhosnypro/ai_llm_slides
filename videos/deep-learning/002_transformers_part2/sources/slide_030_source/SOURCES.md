# SOURCES.md — slide 030 "Position vectors as rotations" (no printed title; rotation-matrix derivation)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_030_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1) + the Kazemnejad page (live curl, banked on slide
027's run) + the paper §3.5 fetch (banked on slide 021's run). No new agy
query spent — this slide's content is fully covered by the two already-live
sources and the script-12 raw (`analysis/slide_030_raw.json`).

## Slide identity

- New (curated) slide **030** ← old extraction **61** (kept frame
  `frame_01816.jpg`, shown t≈1653–1815 s — heavily taught) —
  (`unique_slides/slides_index.json`), frame `unique_slides/slide_030.jpg`.
- Frame facts (vision transcript): no title; badge "30". An equation-
  derivation layout, top to bottom:
  1. Red box: "Vector of Pos "t"" → [ sin(ωt) ; cos(ωt) ]; "Vector of Pos
     "t+δ"" → [ Sin (ω(t+δ)) ; cos(ω(t+δ)) ] (capital "Sin" verbatim).
  2. Yellow box, "Remember:" (underlined): sin(a+b)=sin (a) cos(b) +
     cos(a) sin(b); cos(a+b)=cos(a) cos(b) – sin(a) sin(b).
  3. Blue box: the two-line expansion — sin(ω(t+δ)) = sin(ωt + ωδ) =
     sin(ωt) cos(ωδ) + cos(ωt) sin(ωδ); cos(ω(t+δ)) = cos(ωt + ωδ) =
     cos(ωt) cos(ωδ) - sin(ωt) sin(ωδ).
  4. Blue box: [ Sin (ω(t+δ)) ; cos(ω(t+δ)) ] = [ cos(ωδ)  sin(ωδ) ;
     - sin(ωδ)  cos(ωδ) ] × [ sin(ωt) ; cos(ωt) ], curly brace under the
     2×2 matrix captioned "Independent of Position "t"".
  5. Green box: "From Computer Graphics:" / "Rotation Matrix of Vector at
     Pos "t" with angle "ωδ" e.g "ω" , "2ω" , "3ω" , …".
  Mouse-cursor artifact above the matrix (recording artifact).

## Primary sources

1. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl 2026-10-11, `scratch/webverify/kazemnejad_pe.html`). The
   slide's derivation is this blog's "Relative Positioning" section, step
   for step (φ ↔ δ, ω_k ↔ ω). Verbatim from the blog: the addition-theorem
   expansion "[sin(ω_k t)cos(ω_k φ) + cos(ω_k t)sin(ω_k φ); cos(ω_k
   t)cos(ω_k φ) − sin(ω_k t)sin(ω_k φ)]", then "So the final transformation
   matrix M is: M_{φ,k} = [[cos(ω_k φ)  sin(ω_k φ)], [−sin(ω_k φ)
   cos(ω_k φ)]]", "**As you can see, the final transformation does not
   depend on t.** Note that one can find the matrix M **very similar to the
   rotation matrix**. Similarly, we can find M for other sine-cosine pairs,
   which eventually allows us to represent p_{t+φ} as a linear function of
   p_t for any fixed offset φ."
2. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11,
   `scratch/webverify/paper_v7.html`) — "We hypothesized it would allow the
   model to easily learn to attend by relative positions, since for any
   fixed offset k, **PE_{pos+k} can be represented as a linear function of
   PE_pos**." — the property the whole slide proves for the 2-D pair.
- The trig identities in "Remember:" are standard angle-addition formulas
  (course refresher, no source needed).

## What the source CONFIRMS (equation-by-equation)

- [sin(ωt); cos(ωt)] as the position vector — Kazemnejad's p_t = [sin(ω_k
  t); cos(ω_k t)] (2-D building block; the course's single-pair toy case).
- The expansion lines — identical to the blog's addition-theorem expansion.
- The matrix [cos(ωδ) sin(ωδ); −sin(ωδ) cos(ωδ)] — exactly the blog's
  M_{φ,k} (with φ→δ), including entry order and signs.
- "Independent of Position "t"" — blog: "the final transformation does not
  depend on t"; paper: PE_{pos+k} is a linear function of PE_pos (the
  matrix depends only on the offset, not the position).
- "From Computer Graphics: Rotation Matrix … with angle ωδ" — the blog's
  "very similar to the rotation matrix" remark, expanded by the lecturer
  into the computer-graphics analogy; "e.g ω, 2ω, 3ω, …" = the
  frequency-per-pair indexing (ω_k / 10000^(2i/d_model) across the d_model/2
  pairs).

## Figures used by this slide

- **None.** Course-authored math-derivation composition; no published
  figure reproduced (vision transcript: "matches no standard figure").

## Course-authored elements

- The boxed derivation layout, the "Remember:" refresher box, the "From
  Computer Graphics" box with the e.g. list, the capital-Sin inconsistency
  ([Sin (ω(t+δ)); cos(ω(t+δ))]) — keep verbatim for recreation, badge "30".

## [?] Uncertain items

- none. (All printed math cross-checks against the blog's derivation and
  the paper's property; no numeric data on the slide.)

## Corrections

- none — no discrepancy between frame and sources.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This
source confirms/corrects DATA and records provenance; it never licenses
inventing or "improving" content the slide doesn't show.
