# Worker report — slide 015 (001_introduction) "[2] Machine Learning vs Deep Learning"

## Verdict chain

| Attempt | Build | Render | Pre-judge checks | Judge | Verdict |
|---|---|---|---|---|---|
| 1 | `build/slide_015.js` (banked `build_attempt_1.js`) | `qa/slide015/render_1.png` (150 dpi, 2001x1125) | house_chrome_check PASS; closed-loop PIL PASS (see below) | `qa/slide015/judge_attempt_1.txt` (comparison, `--thinking high --max-tokens 65536`, wall 280/1700, frozen payload `judge_p_payload_1.txt`) | **FINAL VERDICT: PASS** — 0 BLOCKER, 0 MAJOR, 2 MINOR |

**Attempts used: 1 of 6. Certified on the first judge read.**

## Pre-judge closed-loop numbers (attempt 1, `selfcheck_attempt_1.py` / `selfcheck_attempt_1_out.txt`)

Tolerance ~4 render px (~1.9 frame px at scale 2.0844):

- L1 `[2] Machine Learning`: rows 191.4..243.2 (exp 189..242, d 2.4/1.2), cols 219.7..761.9 (exp 219..761, d 0.7/0.9), ink w 542 (exp 542), cx d 0.8 — OK
- L2 `vs`: rows 270.6..291.2 (d 0.6/2.2), cols 470.2..506.1 (d 0.8/0.9), ink w 36 (exp 36), cx d 0.8 — OK
- L3 `Deep Learning`: rows 321.4..373.3 (d 1.4/1.3), cols 302.2..674.5 (d 1.8/0.5), ink w 372 (exp 370), cx d 0.6 — OK
- Render text 5x5-core mean color **#B3000C** = measured original core (exact match)
- Text ink containment: cols 220..762, rows 191..373 frame — fully inside panel (42..918, top 45)
- `house_chrome_check.py`: **PASS** (panel x 89-1913, y 95-bottom; badge center (1860,148) d=70; tol 8) — `chrome_check_1.txt`

## Measurement forensics (banked under `scratch_015/`)

- `measure_original2.py`: panel border cols 58-59 / 902, top row 43, red line 516-517, black strip 518-539, canvas FFFFFF, fill (231,233,230)=E9E9E7; text bands L1 189-242/219-761, vs 270-289/471-507, L3 320-372/304-674.
- `font_solve2_015.py`: titles = **Liberation Serif (Times New Roman) Bold @59** (IoU 0.845/0.840 vs Liberation Sans 0.468/0.517 — SERIF on this frame, unlike slide_003's sans solution; per-frame forensics, not family assumption). Text 5x5-core modal **#B3000C..#B7000B, mean #B3000C** (n=4124) — overrides spec estimate #B22222.
- `vs_solve.py` (native-scale alignment IoU): lowercase **'vs' serif bold @43.5-44** (IoU 0.833 vs uppercase 'VS' 0.743).
- Spec deviations by measurement (frame is ground truth; spec marked its sizes/positions as unmeasured estimates): title ~59pt not ~44pt; 'vs' ~43.5pt (73% of title) not ~15pt (one-third); text block centers ~490 frame px (panel center 480, reproduced with centered boxes on x=489.5); bands sit ~4-11 px lower than the spec's percentage estimates.

## Intentional omissions (judge ground rules, certified slide_040 convention)

- Bottom black strip (video-player bar) and white pen/cursor icon at ~(595,297): video artifacts, per rule (c) and the content spec — deliberately not recreated.
- Original's panel border sits inset (58..902, top 43) vs canonical chrome (42..918, top 45): playlist law fixes chrome to canonical values — covered by rule (a).
- Badge numeral 15 = file number (001_introduction originals carry no printed numbers; assumption pending founder veto per video AGENTS.md).

## Self-check coverage notes

- No equations, multi-line delimiters, or tables on this slide → zoomed crop vision (check 6), delimiter geometry (check 4), table data (check 5), equation existence (check 3) N/A. The smallest region ('vs', 20x37 frame px) was instead solved by native-scale mask IoU forensics + the closed-loop band check; the full-slide judge confirmed it.
- Multi-line spacing check N/A (three single-line boxes); explicit `lineSpacing` set on every box anyway, baseline model `box_top + 0.891em` (validated slide_002/slide_040) — landed within 2.4 render px on first build, no calibration pass needed.

## Judge findings (attempt 1, transcribed)

1. MINOR — typeface marginally wider/heavier than the original's compressed serif (~1-2%); confidence high.
2. MINOR — title block ~1% lower relative to panel height; confidence medium.
No BLOCKER/MAJOR. Frame containment clean. Missing elements: none. Ground rules (a)-(f) settled first.

## Paths

- Deliverable: `videos/deep-learning/001_introduction/recreated_pptx/slide_015_recreated.pptx` (single-version)
- Build: `videos/deep-learning/001_introduction/recreated_pptx/build/slide_015.js` (banked copy `qa/slide015/build_attempt_1.js`)
- Judge transcript: `videos/deep-learning/001_introduction/recreated_pptx/qa/slide015/judge_attempt_1.txt`; probe `probe_1.txt`
- Judge prompt/payload: `qa/slide015/judge_prompt_1.txt` + `judge_p_payload_1.txt` (frozen template from certified slide_040 payload_3, numeral 40→15 only change)

## DB state

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`, `visual_transcript=.../qa/slide015/judge_attempt_1.txt`, `build_script`/`pptx_path` set. Slide 15 is root — no dependents in this video's graph (`deps`: 16 waits on 9, not 15); no cross-video children reference `001_introduction:15`; no banking obligation per dispatch.

## Judge procedure note

Judge procedure executed by the worker via Bash (no Agent/Task spawn tool in this environment) — byte-for-byte per the banked prompt through `scripts/16_vision_gate.sh`, orchestrator-approved fallback per `scripts/17_worker_instructions.md` §Judge step 7. Certificate: single-read, default route (images), glm leg DEFERRED/BLOCKED.
