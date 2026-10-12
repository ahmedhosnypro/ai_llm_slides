# Review packet — deep-learning/001_introduction (HARD STOP: human review required)

Extracted 2026-10-12 by the slide-recreation pipeline. **The frame set below is NOT
approved.** Per the founder directive (2026-10-10, non-negotiable): no script 12
(analysis), no script 13 (validation), no DB ready-marking, no build dispatch until a
human reviews and approves this set.

## Contents

- `contact_sheet_page1..4.jpg` — 20 slides per page, 4x5 grid, labeled `slide_NNN.jpg`.
- `../unique_slides/slide_001..080.jpg` — the kept (LAST) frame of each phash group, 960x540.
- `../unique_slides/slides_index.json` — per-group: kept_frame, start/end sec, frame_count.
- `../unique_slides/new2old_mapping.json` — DRAFT identity mapping (new N == extraction
  group N). Must be REBUILT from content hashes after the founder's curation
  (curation-metadata law, videos/deep-learning/AGENTS.md).

## Extraction facts

- Source: `001_introduction.mp4` — 1280x720 @10fps, 5425.7s (~90.4 min), Deep Learning
  DSAI 308 (Dr. Ahmed Mustafa ElSayed) — same playlist as 001_transformers_part1 /
  002_transformers_part2.
- 5,426 frames @1 FPS → **80 groups** (phash threshold 8, keep-last).
- Deck character: HEAVY live-handwriting lecture — the instructor annotates slides with
  a stylus, so many groups are annotation STATES of one base slide, and several slides
  are purely hand-drawn whiteboard sketches.

## Machine observations (for the reviewer's convenience — NOT curation decisions)

Short groups (1–4 frames) that look like transitions/blanks rather than content
(timestamps from slides_index.json):

| slide | span (s) | frames | look |
|---|---|---|---|
| 15 | 523–523 | 1 | near-blank white frame |
| 17 | 535–535 | 1 | near-blank white frame |
| 36 | 1553–1553 | 1 | near-blank white frame |
| 44 | 2046–2048 | 3 | near-blank white frame |
| 47 | 2342–2342 | 1 | near-blank white frame |
| 50 | 2753–2753 | 1 | near-blank white frame |
| 55 | 3091–3091 | 1 | near-blank white frame |
| 56 | 3092–3092 | 1 | near-blank white frame |
| 59 | 3237–3237 | 1 | near-blank white frame |
| 61 | 3337–3337 | 1 | near-blank white frame |
| 63 | 3340–3340 | 1 | near-blank white frame |
| 70 | 3891–3891 | 1 | near-blank white frame |
| 76 | 4765–4765 | 1 | near-blank white frame |

Other patterns the reviewer may want to rule on:

- **Annotation-state near-duplicates**: e.g. 18/19 vs 9 (Complete ML Classification
  Process), 21/23/25 (Complete DL Model + backprop), 27/28 (Single Perceptron), 29/30
  (NN Model), 37/39/40/41 (Where to Get Filters), 52/53 (How many filters), 58/65/67
  (Output dimensions), 60/62/64/66/68/77/78 (hand-drawn CNN sketches at successive
  states). Keep-first-vs-last vs keep-one-state is the founder's call; phash threshold 8
  grouped these because ink differences are small.
- **Section titles**: 3 ([1] Revision of Machine Learning), 16 ([2] ML vs DL), 26 ([3]
  Quick revision of Neural Netwok (NN) — original's own typo), 32 ([4] Introduction to
  Deep Learning and CNN).
- **No yellow slide-number badges visible** in this lecture's frames (unlike
  001_transformers_part1). Chrome implications (playlist law vs this deck's own
  pixels) need a founder ruling before any build.
- Slide 2 title area shows the agenda; slide 1 is the course cover (no printed number
  visible).

## After approval

Once the human approves (and curates: deletions / group splits / frame swaps /
renumbering), the machine will: rebuild `slides_index.json` + `new2old_mapping.json`
from content hashes, back up the pre-curation index/DB, register the curated set in
`slides_progress.db` (VIDEO=deep-learning/001_introduction), and only then dispatch
analysis (script 12).
