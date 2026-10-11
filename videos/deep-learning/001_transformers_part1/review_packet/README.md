# Review packet — 001_transformers_part1 (HARD STOP: human review required)

> **CURATION OUTCOME (2026-10-11):** the founder completed the review — the deck is
> now **45 slides**, densely renumbered (`slide_001..slide_045`). This packet and its
> contact sheets document the PRE-curation 123-frame set and are kept as the review
> record. Post-curation state of record: `unique_slides/slides_index.json` (45),
> `unique_slides/new2old_mapping.json`, `slide_dependencies.json`,
> `slides_progress.db` (45 rows + dependency edges; pre-curation DB archived as
> `slides_progress_old123.db.bak`). The 123-frame index backup:
> `unique_slides/slides_index_old123.json`.

Video: `videos/deep-learning/001_transformers_part1/001_transformers_part1.mp4`
(1280×720, 10 fps source, 4479.3 s ≈ 74.7 min)

## What the machine did (pipeline stages 10–11 only)

1. **Frame extraction** — 1 FPS, scaled to 960px, JPEG q4 → `frames/` (4479 frames).
2. **phash dedup** — threshold 8, sequential grouping, **kept the LAST frame of each
   group** (fully-built slide) → `unique_slides/` — **123 unique slides** +
   `slides_index.json` (slide number, kept frame, start/end seconds, frame count).

## What the machine did NOT do (HARD STOP, founder directive 2026-10-10)

- No vision analysis (script 12), no validation (script 13), no builds, no subagent
  dispatch on these frames.
- No approved/ready marker was set anywhere. The DB rows are registered as
  `analysis_status=pending` only.

## What the human reviews (curation is human-owned)

- **Contact sheets**: `contact_sheet_p01.jpg` … `p07.jpg` — 20 labeled slides per page,
  in extraction order (slide_001 = first appearance at 0 s).
- **Hints**: `review_hints.md` — passive flags only. 1-frame groups are prime
  cull candidates (transitions / cursor moves / camera cuts); short 2–4-frame groups
  may be partial builds that kept the wrong frame.

## Decisions that belong to the human (machine must never make these)

1. Which of the 123 frames are real, valid slides (cull duplicates, transition noise,
   placeholders, non-slide frames).
2. Numbering/badges: current names are extraction-order (`slide_001…123`); if the
   slides carry printed badge numbers, rename so `slide_NNN` = the printed number
   (ml-intro precedent), and the new2old mapping is drafted from that decision.
3. Final approval of the set — only then do scripts 12/13 and the build chain start.

## Reference state

- Frames kept on disk under `frames/` (gitignored) — timestamps recoverable from
  `slides_index.json` (`frame_00021.jpg` ≈ t=20 s).
- Progress DB: `slides_progress.db` (VIDEO=deep-learning/001_transformers_part1),
  123 rows, all `analysis_status=pending`.
