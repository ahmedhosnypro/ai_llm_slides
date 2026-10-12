# Review packet — 02_linear-regression-classification-MSSE (HARD STOP: human review required)

Video: `videos/machine-learning/02_linear-regression-classification-MSSE/02_linear-regression-classification-MSSE.mp4`
(154 MB, 6197.7 s ≈ 103.3 min, 1280×720) — ML Zewail CSAI playlist, lecture [02]
"Linear Regression & Classification (MSSE)", CSAI 251 Spring 2024.

## What the machine did (pipeline stages 10–11 only)

1. **Frame extraction** — 1 FPS, scaled to 960px, JPEG q4 → `frames/` (6198 frames).
2. **phash dedup** — threshold 8, sequential grouping, **kept the LAST frame of each
   group** (fully-built slide), `--limit 100000` (full deck) → `unique_slides/` —
   **210 unique slides** + `slides_index.json` (slide number, kept frame, start/end
   seconds, frame count). Slide density ≈ 1 unique image / 29.5 s.

## What the machine did NOT do (HARD STOP, founder directive 2026-10-10)

- No vision analysis (script 12), no validation (script 13), no builds, no subagent
  dispatch on these frames.
- No approved/ready marker was set anywhere. The DB rows are registered as
  `analysis_status=pending` only (210 rows,
  VIDEO=machine-learning/02_linear-regression-classification-MSSE).
- No new2old mapping exists yet — it is drafted AFTER the founder's curation
  (content-hash reconciliation law, incidents 2026-10-11).
- No playlist-level AGENTS.md / chrome law exists yet for `videos/machine-learning/` —
  the deck's chrome gets measured and codified only after the frame set is approved.

## What the human reviews (curation is human-owned)

- **Contact sheets**: `contact_sheet_p01.jpg` … `p11.jpg` — 20 labeled slides per page,
  in extraction order (slide_001 = first appearance at 0 s).
- **Hints**: `review_hints.md` — passive flags only. 66 single-frame groups are prime
  cull candidates (transitions / cursor moves / camera cuts — note the consecutive
  runs 062-064, 095-098, 113-117, 155, 160-163, 192-194, 196-197, which look like
  rapid-fire board work or slide flips); 16 short 2–4-frame groups may be partial
  builds that kept the wrong frame; 12 groups on screen > 2 min are likely core
  lecture slides.

## Decisions that belong to the human (machine must never make these)

1. Which of the 210 frames are real, valid slides (cull duplicates, transition noise,
   placeholders, non-slide frames).
2. Numbering/badges: current names are extraction-order (`slide_001…210`); if the
   slides carry printed badge numbers, rename so `slide_NNN` = the printed number
   (ml-intro precedent), and the new2old mapping is drafted from that decision.
3. Whether this playlist gets its own chrome law + `shared_patterns/` (measured from
   the approved reference slide) before any builder is dispatched.
4. Final approval of the set — only then do scripts 12/13 and the build chain start.

## Reference state

- Frames kept on disk under `frames/` (6198 files) — timestamps recoverable from
  `slides_index.json` (`frame_00046.jpg` ≈ t=45 s).
- Progress DB: `slides_progress.db`, 210 rows, all `analysis_status=pending`,
  `gen_status=pending`.
