# Review packet — 002_transformers_part2 (HARD STOP: human review required)

Video: `videos/deep-learning/002_transformers_part2/002_transformers_part2.mp4`
(181 MB, 5440.1 s ≈ 90.7 min)

## What the machine did (pipeline stages 10–11 only)

1. **Frame extraction** — 1 FPS, scaled to 960px, JPEG q4 → `frames/` (5440 frames).
2. **phash dedup** — threshold 8, sequential grouping, **kept the LAST frame of each
   group** (fully-built slide), `--limit 100000` (full deck) → `unique_slides/` —
   **150 unique slides** + `slides_index.json` (slide number, kept frame, start/end
   seconds, frame count). Slide density matches lecture 1 (~1 unique image / 36 s).

## What the machine did NOT do (HARD STOP, founder directive 2026-10-10)

- No vision analysis (script 12), no validation (script 13), no builds, no subagent
  dispatch on these frames.
- No approved/ready marker was set anywhere. The DB rows are registered as
  `analysis_status=pending` only.

## What the human reviews (curation is human-owned)

- **Contact sheets**: `contact_sheet_p01.jpg` … `p08.jpg` — 20 labeled slides per page
  (last page 10), in extraction order (slide_001 = first appearance at 0 s).
- **Hints**: `review_hints.md` — passive flags only. 48 1-frame groups are prime
  cull candidates (transitions / cursor moves / camera cuts); 14 short 2–4-frame
  groups may be partial builds that kept the wrong frame; 13 groups on screen
  > 2 min are likely core lecture slides.

## Decisions that belong to the human (machine must never make these)

1. Which of the 150 frames are real, valid slides (cull duplicates, transition noise,
   placeholders, non-slide frames).
2. Numbering/badges: current names are extraction-order (`slide_001…150`); if the
   slides carry printed badge numbers, rename so `slide_NNN` = the printed number
   (ml-intro precedent), and the new2old mapping is drafted from that decision.
3. Final approval of the set — only then do scripts 12/13 and the build chain start.

## Reference state

- Frames kept on disk under `frames/` (gitignored) — timestamps recoverable from
  `slides_index.json` (`frame_00021.jpg` ≈ t=20 s).
- Progress DB: `slides_progress.db` (VIDEO=deep-learning/002_transformers_part2),
  150 rows, all `analysis_status=pending`.
