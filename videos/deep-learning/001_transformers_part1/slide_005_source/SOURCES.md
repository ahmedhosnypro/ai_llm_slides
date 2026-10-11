# SOURCES.md — slide 005 "1-D Convolutional Neural Network"

Provenance record per `videos/deep-learning/001_transformers_part1/AGENTS.md`
(web-verified analysis is mandatory). Researched 2026-10-11 by correction worker
W-A (no image access — frame facts below come from the script-12 vision pass
transcription in `../analysis/slide_005_raw.json`, ground truth for WHAT is shown;
no new web calls — everything below reuses evidence already banked in
`../SOURCES_MAP.md` and `../slide_004_source/SOURCES.md`).

## Slide identity

- New (curated) slide **005** ← old extraction slide **5**, diff 0.062,
  **swapped: true** (`unique_slides/new2old_mapping.json`; the `_meta` records
  `founder_frame_swap: true`, `original_kept_frame: frame_00147.jpg` — the founder
  swapped the analysis frame from the group's LAST frame to its FIRST,
  `frame_00095.jpg`, during curation).
- Frame `unique_slides/slide_005.jpg` (kept from `frame_00095.jpg`, 92–146 s of
  the lecture — 55 frames, the longest screen time of the deck's opening run).
- Frame facts (vision pass): full-slide schematic — red title "1-D Convolutional
  Neural Network" top-center; 'Convolutional Kernel' pictogram (three stacked
  pink rectangles) upper-left; green callout "Can be Computed In Parallel";
  five vertical 13-cell stacks (Words Vectors → 1st–4th Feature Maps) with four
  gray rotated "Non Linearity" bars interleaved; red funnel-triangle connectors
  + one solid red block arrow; vertical red "Sequence Length" arrow at left;
  long red-hatched right arrow along the bottom; diagonal yellow warning banner
  "*** Not Practical for Very Long Sequences***"; blue caption "As Word Sequence
  Length Increases, we need to stack many convolution Layers."; yellow badge "5"
  top-right; mouse-cursor artifact near the top of the diagram.

## Primary source

- **Course-authored** (per `../SOURCES_MAP.md` §2 row "1–5": CONFIRMED
  course-authored, no external source expected). No paper is cited on the slide;
  the diagram is the course's own teaching schematic in the deck's house style
  (same red/blue palette, badge, and frame as the rest of the deck).
- **Lecture video** (the deck's own provenance, and the spoken source of this
  slide's content): https://www.youtube.com/watch?v=Ff8KU1dyJMA — "[11]
  Transformers - Part I", channel "Dr. Khaled Mostafa Elsayed"
  (@dr.khaledmostafaelsayed7516), uploaded 2024-12-11, playlist "Deep Learning
  DSAI 308 Fall 2024 - Zewail"
  (https://www.youtube.com/playlist?list=PL5JZLxl_tFCcmulUU7suv9DkAFrOTm34w;
  verified live in `../SOURCES_MAP.md` §1).

## What the sources CONFIRM

- **Title = line 1 of slide 004**: "1-D Convolutional Neural Network" is
  verbatim agenda/body line 1 of the previous slide ("1-D Convolutional Neural
  Network   (1-D CNN)", `../analysis/slide_004_raw.json`) — direct deck-internal
  confirmation of both slides. Slide 005 is the diagram slide for that line
  (the 4→5 content relationship is already recorded in
  `../slide_004_source/SOURCES.md`; `../slide_dependencies.json` has no edge here).
- **Content matches the spoken lecture**: during this slide's exact screen time
  (92–146 s) the lecturer, per the banked auto-caption evidence recorded in
  `../slide_004_source/SOURCES.md` (YouTube auto-generated transcript fetched
  2026-10-11 via yt-dlp; garbled but usable as spoken-content evidence), "walks
  a convolution kernel over the words" — precisely the diagram this slide shows
  (kernel pictogram applied to the Words Vectors stack producing successive
  Feature Maps). The same banked evidence records the lecturer's dichotomy that
  this slide illustrates: RNN-style processing where "each one [is] waiting for
  the process before it" (sequential) vs. word sequences where each word "has
  its own code" (parallel) — the slide's green callout "Can be Computed In
  Parallel", the yellow banner "Not Practical for Very Long Sequences", and the
  stacking-many-layers caption are the visual rendering of that spoken framing.
  The exact on-slide wording is frame-only/course-authored (captions are
  auto-generated; used only as spoken-content evidence, never as verbatim text).
- **Frame-swap consistency**: the raw `_meta` (`founder_frame_swap: true`,
  `original_kept_frame: frame_00147.jpg`) agrees with the mapping's
  `swapped: true` / diff 0.062 — the analyzed frame is the founder-swapped
  `frame_00095.jpg`, and the vision pass reports the slide fully built on it.
- **Badge numeral "5"** matches the deck's fifth slide.

## Course-authored elements (frame-only; do not "fix" from any web source)

- All label wording ("Words Vectors", "1st/2nd/3rd/4th Feature Map", "Non
  Linearity", "Sequence Length", the callout/banner/caption sentences with
  their literal triple asterisks and odd capitalization "Layers"), the cell
  stack structure and its color highlights, the connector arrows, the kernel
  pictogram, the hatched arrow, the yellow-highlight rotation of the banner,
  the badge, and the mouse-cursor artifact (brief says omit) are the deck's
  own. No external figure was identified, downloaded, or claimed; per the
  fidelity law nothing here may be "corrected" toward any textbook rendering.

## [?] Uncertain items

- [?] Exact cell-highlight mapping (which rows of each Feature Map are
  colored — e.g. "1st Feature Map: cell 2 and cells 10–13 peach") is a
  vision-pass read of a dense fine-grained graphic; the recreation worker
  should verify row assignments against the frame at build time.
- [?] Geometric placement of the four "Non Linearity" bars: the raw's
  arrangement text says the bars sit interleaved between the five stacks, but
  its own approximate x-estimates (bars ~43.5/58.5/73.5/88% vs stacks
  ~17/32/47/62/77%) do not cleanly interleave for the last bar. Both readings
  are of the same diagram; pin exact bar/stack geometry from the frame —
  not patchable without image access.
- [?] Whether the pipeline drawing is an original course schematic or a redraw
  of a textbook/paper figure: no citation appears on the slide and the fleet
  map (`../SOURCES_MAP.md` §2 row "1–5") records 1–5 as CONFIRMED
  course-authored; no external match was claimed or checked (out of scope for
  this pass).
- [?] The founder's frame swap (last → first frame of the 92–146 s group) means
  the analyzed capture moment differs from the phash rule's usual last-frame
  keep; the vision pass reports the slide fully built either way, and text
  content is unaffected. Any sub-second difference (e.g. cursor position) is
  frame-level only.

## Corrections

- **No JSON patches** (0) — none — raw transcription consistent. The title
  cross-checks against slide 004, the badge and screen-time window are coherent
  with the banked lecture evidence, the `_meta` swap agrees with
  `new2old_mapping.json`, and no verifiable source contradicts any transcribed
  string. The geometry tensions above are frame-level details for the
  recreation worker, not transcription errors.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
verbatim text, drawn content). These sources confirm/correct DATA and record
provenance; they never license inventing or "improving" content the slide
doesn't show. If source and slide disagree, record the discrepancy above — the
slide wins for recreation, the source wins for understanding.
