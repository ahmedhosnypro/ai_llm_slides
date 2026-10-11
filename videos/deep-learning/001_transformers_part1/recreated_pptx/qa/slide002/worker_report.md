# Worker report — slide 002 ("Transformers / Part I / Aug. 2020")

Video: `deep-learning/001_transformers_part1` (Deep Learning DSAI 308, Transformers — Part I)
Date: 2026-10-11. Attempts used: **1** (judge dispatches). Final verdict: **PASS**.

## Deliverable

- PPTX (single-version law, no suffixes): `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_002_recreated.pptx`
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_002.js` (pptxgenjs, LAYOUT_WIDE)
- Comparison transcript: `videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide002/judge_attempt_1.txt`
- Probe transcript: `videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide002/probe_1.txt`
- Banked per-attempt evidence: `judge_prompt_1.txt`, `judge_p_payload_1.txt` (frozen `-p` GROUND
  RULES verbatim), `build_attempt_1.js`, `render_1.png`, `selfcheck_attempt_1.py` + output.

## Chrome interpretation (documented decision)

This deck's shared chrome — measured identically on slides 1/2/3 — is: white outer canvas,
light-gray panel (`#E9E9E7`) with a thin red (`#C00000`) border inset left/right/top with the
bottom edge AT the slide bottom (stroke half-visible), yellow badge (`#FDFD96`) with a PURPLE
outline (`#6A5ACD`) top-right. That is this deck's own house template; the ml-intro values
(full-bleed `#E8E8E8`, frame inset 0.15in on all sides, outline-less badge) visibly contradict
this deck's originals. Per the video fidelity law (original frame = ground truth) and
`slide_002_source/SOURCES.md` ("badge outline hue ... confirm at recreation time from the
frame"), the frame's own chrome was reproduced. All geometry is PIL-measured from
`unique_slides/slide_002.jpg` (960×540, 1px = 1pt). The judge settled ground rule (a) as
non-discrepancy "either way" and confirmed the chrome matches the original.

## Omitted element (by the book)

The small gray '+' crosshair at ~(40%, 68%) below the date: the validated spec marks it a
likely cursor/alignment artifact (uncertain_items), the recreation brief makes it optional,
and judge GROUND RULES (c) covers video-capture artifacts. Omitted; carried in the judge
`--view` context; the judge confirmed the omission is correct. No other content omitted.

## Build → self-check → judge loop

1. **Build**: spec `analysis/slide_002_final.json` (PASS_WITH_FIXES, score 9) + verbatim text
   ("Transformers" / "Part I" / "Aug. 2020", badge "2"). Colors verbatim from spec
   (`#C00000` text/border, `#E9E9E7` panel, `#FDFD96` badge fill, `#6A5ACD` badge outline,
   `#333333` numeral, `#FFFFFF` canvas). No equations, tables, delimiters, or charts on this
   slide (self-check items 3/4/5/6 N/A; all text boxes single-line — explicit-lineSpacing N/A).
2. **Self-check attempt 1** (PIL, 150dpi, closed-loop vs frame, banked): first pass caught
   title/subtitle ~5-6px low and ~2-7% narrow → calibrated (title 73.5pt; subtitle 50pt +
   `charSpacing: 1.4` to reproduce the frame's tracking at matched cap height; badge ring 2pt;
   small y-shifts). Re-render: **ALL CHECKS PASS** — text bands within ~3px @150dpi (≈0.15%
   of frame height), width/height ratios 0.987–1.007, numeral digit height 23px vs 22.9
   expected, containment 0 outliers, canvas/fill/border colors verified.
3. **Judge attempt 1** (no Agent/Task tool in this environment — judge procedure executed by
   the worker via Bash per 17 §7, orchestrator-approved fallback; probe + comparison through
   `scripts/16_vision_gate.sh`, default route, `--thinking high --max-tokens 65536`, W4 wall;
   degenerate events: 0): **FINAL VERDICT: PASS** for 'faithful, usable recreation'.
   Findings: two MINORs (inter-line gaps and block height each read ~1-1.5% of frame height
   looser/higher; medium confidence), no MAJOR/BLOCKER. Note: the banked PIL measurements
   (bands within ~3px @150dpi) contradict the MINOR gap read — recorded as judge variance;
   PASS not affected. Certificate: single-read, default route (images), glm leg DEFERRED/BLOCKED.

## DB milestones (all set)

`gen_status=building` → `judging` → `passed`; `build_script`, `pptx_path`,
`visual_check=PASS`, `visual_attempts=1`, `visual_transcript=.../qa/slide002/judge_attempt_1.txt`.

## Dependencies

Slide 2 is a ROOT (`15_progress.py deps`) and has NO dependents (no child edges point to 2),
so no component export was required under the dependency law.
