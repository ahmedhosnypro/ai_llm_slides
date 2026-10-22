# SOURCES.md — slide 006 "Transformers – Part II" (agenda/outline)

Provenance record per `videos/deep-learning/002_transformers_part2/AGENTS.md`
(web-verified analysis mandatory). Written 2026-10-11 by the Part II web-verification
worker.

## Slide identity

- Frame `unique_slides/slide_006.jpg`, badge numeral **6** (matches file id).
- Old extraction: slide 6 ← old 5 (`unique_slides/new2old_mapping.json`).

## Vision transcript of record

- `transcripts/slide006_vision_2026-10-11.txt` — ONE default-route (`images`) probe,
  `--thinking high --max-tokens 65536`, via `scripts/16_vision_gate.sh`; winner
  `images (round 1, attempt 1)`, degenerate events 0. Cross-checked against the
  pre-existing script-12 raw `analysis/slide_006_raw.json` — consistent (six
  bullet lines, blue bold, no bullet glyphs).

## Frame facts (vision, ground truth)

- Title "Transformers – Part II" (large dark red, centered top); six left-aligned
  blue bold lines: "Parallelization  Implementation Issues" (double space as
  shown), "Positional Information", "Building Transformer Block",
  "Transformer Decoder", "Transformer Encoder  as a Classifier" (wide gap as
  shown), "What is Next ?" (space before "?"). Badge "6"; thin dark-red border;
  mouse-cursor artifact; black bottom letterbox. No diagrams, no equations.

## Primary source

- **None — course-authored agenda slide.**
- **agy websearch 2026-10-11** (`../scratch/agy_s006.txt`): the six-item sequence
  matches no published tutorial/book chapter/deck; instructor-authored agenda.
  The topics map onto the session's later content (parallelization → slide 007;
  positional information → 026–034 family; building the block; decoder;
  encoder-as-classifier; next steps) — each gets its own provenance record on
  its own slide.

## Figures used

- None. Nothing downloaded.

## What the source CONFIRMS / CORRECTS

- CONFIRMS: outline is instructor-authored; item wording kept verbatim from the
  frame (including the irregular double spaces and "What is Next ?" spacing —
  these are frame ground truth for recreation, likely slide-authoring artifacts,
  NOT transcription errors; do not "fix" them).
- CORRECTS: nothing. No `[?]` items.

## Law reminder

The ORIGINAL VIDEO FRAME is ground truth for what the slide shows. House slide;
verbatim spacing anomalies recorded above are features of the original, not errors
to correct.

## Script-12 raw cross-check (raw-verification worker, 2026-10-11)

- `analysis/slide_006_raw.json` re-read in full (model `images`; old extraction 5;
  kept_frame frame_00091, 33 frames). Fully consistent with this record: title
  "Transformers – Part II" and the six agenda lines verbatim, INCLUDING the
  double spaces ("Parallelization  Implementation Issues",
  "Transformer Encoder  as a Classifier") and "What is Next ?" — raw's
  typography note independently flags them as on-slide spacing, i.e. frame truth.
  Cursor artifact frozen over line 5; no bullet glyphs; no diagrams/equations.
- [?]: none. Corrections: none yet — verify against script-13 final when it lands
  (no final for 006 as of this pass).

## Recreation record (build worker, 2026-10-12)

- Built `recreated_pptx/build/slide_006.js` -> `slide_006_recreated.pptx` (house chrome
  numeral 6; title 40pt bold C00000 at measured ink center cx 427.4pt — NOT slide-centered,
  matching this spec's 24%..66% title region; six 20pt bold single-line boxes at the
  measured per-line ink positions, pitch 41.8/43.9/41.8/41.8/45.9 reproduced).
- COLOR REFINEMENT (frame wins per fidelity law): agenda blue measured census (6544
  near-pure px: R 0-8, G 0-8, B 96-128 cores, darkest-1/8 mean (12.8, 6.0, 104.3))
  matches the certified slide_032 calibration (cores B~100-110 -> true #000080); the
  spec's #1414B8 is a validator estimate overridden per this deck's precedent
  (slide_035: measured cores -> 0000A8; slide_018: -> 0000A0). Build header documents it.
- Verbatim spacing anomalies (double spaces; "What is Next ?") preserved — frame truth.
- Mouse cursor + bottom letterbox omitted (judge GROUND RULES (c)).
- Pre-judge self-checks all banked under `recreated_pptx/qa/slide006/`
  (house_chrome_check PASS; PIL closed-loop: title dw -0.6px, all lines <=3px
  profile-aligned @150dpi; frame containment PASS; gap bands clean).
- JUDGE: comparison attempt 1 (single-read, default route images, glm leg
  DEFERRED/BLOCKED) -> FINAL VERDICT: PASS, no BLOCKER/MAJOR, 2 MINORs (title size
  "~5% larger" — contradicted by PIL measurement dw -0.6px; first-gap "few px lower" —
  measured <=2.1px). Transcript: `recreated_pptx/qa/slide006/judge_attempt_1.txt`.
