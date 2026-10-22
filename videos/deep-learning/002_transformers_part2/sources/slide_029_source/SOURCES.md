# SOURCES.md — slide 029 "Sequence of 12 words — Positions are defined as angles"

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`.
Machine-verified 2026-10-11: vision transcript of record
`transcripts/slide_029_vision_2026-10-11.txt` (default `images` route,
`--thinking high --max-tokens 65536`, gated via `scripts/16_vision_gate.sh`,
validated winner round 1). Deps: `29 ← 28` (chain from 27/26); old extraction
group 60 split — 029 keeps the group's FINAL frame `frame_01653.jpg`. No new
agy query spent — source family verified on slides 021–023/027/028; the only
new claim (smaller ω → longer sequences, ω = 1/10000) is confirmed directly
against the already-fetched paper §3.5 text.

## Slide identity

- New (curated) slide **029** ← old extraction **60** (split with new slide
  028; the group's final, fully-built state; shown t≈1584–1652 s)
  (`unique_slides/slides_index.json`), frame `unique_slides/slide_029.jpg`.
- Frame facts (vision transcript): heading "Sequence of **12** words /
  Positions are defined / as angles"; badge "29". Same clock-face circle:
  12 dashed red spokes at 30°, twelve mint chips "Word 0"…"Word 11"
  counterclockwise (Word 0 at 3 o'clock, Word 3 at 12, Word 6 at 9, Word 9
  at 6), red curved arcs with "+ω" labels between consecutive words (some
  right-side arc labels cropped/absent per transcript), same pale-yellow
  inset "Sin(ω t) / Cos(ω t) / t=0,1,2,3,....". **New** red-bordered callout
  box (bottom-left): "Using smaller ω value, allow representation of longer
  sequences" ("smaller" highlighted yellow) + "(practically use ω =
  1/10000)".

## Primary sources (family bank + direct confirmation)

1. **arXiv 1706.03762v7 §3.5** (live curl 2026-10-11,
   `scratch/webverify/paper_v7.html`) — confirms BOTH the new claim's
   constant and its motivation, verbatim:
   - Base 10000: "PE(pos,2i)=sin(pos/10000^(2i/d_model)),
     PE(pos,2i+1)=cos(pos/10000^(2i/d_model))" — the smallest frequency
     (largest-wavelength pair) has ω = 1/10000 in the slide's 2-D toy
     setting (d_model = 2 ⇒ the single pair's argument is pos/10000).
   - "The wavelengths form a geometric progression from 2π to 10000·2π." —
     smaller ω ⇔ longer wavelength ⇔ longer sequences distinguishable
     before the encoding wraps.
   - "We chose the sinusoidal version because it may allow the model to
     extrapolate to sequence lengths longer than the ones encountered
     during training." — the slide's "allow representation of longer
     sequences" motivation.
2. **Kazemnejad, "Positional Encoding in Transformers"** —
   https://kazemnejad.com/blog/transformer_architecture_positional_encoding/
   (live curl banked on slide 027's run; figures banked in
   `../slide_027_source/`): "By decreasing their frequencies, we can go from
   red bits to orange ones" — the frequency/wavelength spectrum framing of
   the same point. The 12-word circle drawing itself is again
   course-authored (vision transcript: "instructor-drawn custom slide, not a
   direct copy").

## What the source CONFIRMS

- "Using smaller ω value, allow representation of longer sequences":
  §3.5's wavelength-geometric-progression + extrapolation sentence;
  Kazemnejad's decreasing-frequency remark.
- "(practically use ω = 1/10000)": the paper's 10000 base — in the 2-D
  single-pair pedagogy (d_model = 2) the frequency is exactly 1/10000; in
  the full model the slowest pair's frequency approaches 1/10000 (argument
  pos/10000^(2i/d_model) with 2i → d_model).
- The 12-word circle: same family as 027/028 (positions as angles, +ω
  steps, sin/cos readout); 12 words at 30° = full circle is the course's
  example extension.

## Figures used by this slide

- None downloaded here (family bank: `../slide_027_source/` — Kazemnejad
  figures). Drawing course-drawn.

## Course-authored elements

- The 12-word example, the "smaller ω → longer sequences" callout with its
  ω = 1/10000 practical note (the paper states the base and the
  extrapolation motive but never the slide's phrasing), badge "29".

## [?] Uncertain items

- [?] Whether some "+ω" arc labels are genuinely absent near Word 0→Word 1
  (transcript: cropped/absent) or hidden by the crop — frame wins; check at
  build time.

## Corrections

- none — the ω = 1/10000 note is consistent with the paper's base.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. This
source confirms/corrects DATA and records provenance; it never licenses
inventing or "improving" content the slide doesn't show.
