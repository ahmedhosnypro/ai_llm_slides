# Worker report — slide 010 "RNN  Seq2Seq model [with Attention]"

Video: `videos/deep-learning/001_transformers_part1` · Worker: per-slide build worker (subagent)
Date: 2026-10-11 · **FINAL VERDICT: PASS** (judge attempt 1, real comparison transcript —
self-execution fallback: no Agent/Task spawn tool available in this environment, judge
procedure executed by the worker byte-for-byte per scripts/17_worker_instructions.md §7).

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_010_recreated.pptx`
  (SINGLE-VERSION law; no equations → no OMML pass; no advanced graphs → no graphgen pass)
- Build: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_010.js`
- **DEPENDENCY-GATED CHILD (edge 10 ← 6)**: parent certified (gen=passed, vis=PASS) before
  build; base imported from the certified `build/components/slide_006.js` via
  `renderBase(pptx, slide, opts)` with `opts.only`/`opts.skip` — nothing re-derived, nothing
  copy-pasted. Slide 10 has NO dependents in `slide_dependencies.json` → no component export.
- New 600dpi assets (built alongside the parent's, none touched):
  `build/assets/curve_a10.png`, `curve_b10.png` (decoder recurrence hooks regenerated at the
  fanned column pitch), `pink_conn.png` (callout connector bezier), `dash_fan.png` (dashed
  attention fan + broad translucent lavender band + sage connector).

## Inheritance decision (block granularity)

- **INHERITED (certified pixels; measured within ~4px tolerance):** `dec_container`,
  `enc_container`, `ctx_arc`, `dec_dot`, `enc_dot`, chrome (numeral 10).
- **SKIPPED (removed/replaced by slide-10 blocks):** the other 22 parent blocks — title,
  decoder content (column pitch fans 555.5/690/824 vs parent 554/685/815.5; o-labels 6.5px
  higher; softmax 18.5pt), encoder content (bars x −10/−5/−2; lower half +5..+10px lower),
  captions ("Decoder"/"Encoder" without "(RNN)"), pink callout (moved up 30px) + its leader
  (now a bezier connector), plus slide-6 has no: green callout, attention boxes/node/lines,
  dashed fan, olive heads, summary box, white card.
- **White backdrop card:** present in BOTH frames (slide_006.jpg too) but omitted by the
  certified parent build. Measured on slide_010: x36.5..921.5, y116.5..500 (covers the chrome
  side borders in the frame). Drawn INSET (x43..917) so the playlist-mandated chrome border
  stays visible (chrome law overrides; keeps house_chrome_check.py PASS). Documented deviation.

## Measurement provenance (frame is ground truth)

- `scratch/slide010/`: `diff_006_010.py` (17.54% changed), `measure1_fills.py`,
  `measure1b_census.py` (color census), `measure2_scan.py` (scanlines),
  `measure3_ink.py` (ink components), `measure4_ascii.py` (ASCII maps),
  `measure5_parent_ink.py` (parent-frame side-by-side), plus probes inside worker notes.
- Vision through the gate (banked .txt): `scratch/slide010/vision_attention.txt` (2x crop),
  `vision_rightbox.txt` (3x, dashed-curve topology), `vision_leftbox.txt` (4x, node/lines),
  `vision_broadstroke.txt` (6x, translucent band + sage-connector terminus).

## Self-checks (attempt 1 — ALL PASS)

`recreated_pptx/qa/slide010/selfcheck_attempt_1.py`: 29 render-vs-frame ink-bbox
comparisons (worst ≤4px), 14 fill color modes, bar-edge columns, underline-scope
(underline ONLY under "Bottleneck" — frame-verified), containment strips, arrowhead
presence, connector ink presence. `house_chrome_check.py`: **PASS**.
Font calibrations driven by ink-width loops: title 25.25pt (frame ink 445px), subtitle
20pt (345px ✓), softmax 18.5pt, node text 20pt, Attention captions 19.5pt/16.5pt
(frame shows different sizes for the two), gray-box header 19.5pt / bullets 18pt,
green callout 15.5pt, emb labels 17.5pt.
`inheritdiff_attempt_1.py`: vs the certified slide-006 render — **0 changed pixels outside
the declared delta zones** (22.59% inside; zones include the white card + caption deltas).
Crop comparison through the gate (`cropcmp_attempt_1.txt`) caught a real miss early
(broad translucent lavender band + green connector's lower terminus + taller olive heads)
— fixed and re-verified before judging.

## Judge (attempt 1)

- Banked: `judge_prompt_1.txt` (frozen -p template verbatim; shared-base fact in --view),
  `build_attempt_1.js`, `probe` procedure run twice (window busy; comparison opened it),
  comparison `judge_attempt_1.txt`: **FINAL VERDICT: PASS** for "faithful, usable recreation".
- No BLOCKER/MAJOR. Four MINOR findings + dispositions:
  1. "Context Vector (of Whole Inputs)" italic in original vs bold upright — DISPOSITION:
     slide_006's frame shows the same (non-)italic lean (+0.3px vs +0.4px measured); the
     certified parent renders the same callout upright at the same size; spec says "red bold".
     Judge variance vs the certified parent style — documented, not a fix trigger.
  2. Sage connector detached from the green callout — DISPOSITION: frame-verified: the
     connector's ink genuinely starts at (403,178), ~52px right of the callout edge (x351);
     nothing between x352..400 (scanned at threshold 40 and 90). The frame wins.
  3. Attention node fill "stronger gray than near-white" — DISPOSITION: node interior
     measured #D6D8E4 vs surround #EFF1FD (the spec's "white node" was a vision-model
     approximation). Frame wins; legibility unaffected per the judge.
  4. Lavender band's left tip slightly more prominent than the original — sub-MINOR; PASS
     stands. Recorded for any future re-touch (could drop alpha 0.45 → 0.35).

## Attempts used: 1 of 6 (first-judge PASS)

## Final state

DB slide 10: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide010/judge_attempt_1.txt`,
`build_script` + `pptx_path` set. QA evidence banked under
`recreated_pptx/qa/slide010/` (render_1.png, selfcheck, inheritdiff, cropcmp, probe,
judge transcripts, prompt + build copies, this report).
