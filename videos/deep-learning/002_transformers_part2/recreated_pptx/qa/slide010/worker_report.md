# Worker report — slide 010 (deep-learning/002_transformers_part2)

**Resumed** after the prior worker died on a harness API timeout (~160 min in, right after
banking build_attempt_5). This worker is the sole owner; no live peer appeared (collision
sweep: last slide-010 artifact 11:40, takeover at 12:43; other slides' workers (022/044/046/055)
active in parallel — not collisions).

## Final state

- **Verdict: PASS** (visual judge attempt 1, real comparison winner body, single-read,
  default route `images`, glm leg DEFERRED/BLOCKED, no HangError / GarbageError).
- **DB row: gen_status=passed, visual_check=PASS, visual_attempts=1**, transcript
  `judge_attempt_1.txt`. Deliverable (single-version law):
  `recreated_pptx/slide_010_recreated.pptx` (from `build/slide_010.js` = attempt 8).

## Attempts (builds 1–8, all banked in qa/slide010/)

| Attempt | What happened |
|---|---|
| 1–3 | Prior worker: initial build + geometry iterations (renders 1–3 banked 10:50–11:10). |
| 4 | Prior worker: pre-crop state (render_4 11:15); cropA/cropB vision comparisons run against it (attempt-1 crops, 11:20/11:23) — PASS with one MAJOR: pptxgenjs leftBrace/rightBrace shapes rendered as straight bars. |
| 5 | Prior worker (11:36): replaced brace shapes with generated bezier PNGs (gen_brace.py → `build/assets/s010_brace{L,R}.png` at exact px/600 size), split Y/T superscript, resized sigmoid box + pill. render_5 banked. |
| 6 | This worker: **y_i output labels green→RED.** Frame scan (fx 248..274, fy 144..176): glyphs+subscripts red (cores (125,15,26)/(143,33,46)), only the arrow green; label geometry = 009's 0-px-verified `drawOutputs` (19pt red at (cx+18, cy−26.5) valign-top) — slide-10 ink top cy−16.7 == 009's certified cy−17. Prior "green labels" was a wrong delta. |
| 7 | This worker: **fn-label wrap fix** — "= Sigmoid"/"= Linear" wrapped in LO at box w 72 (probe: "=" block at sy 195–200, "Sigmoid" at 211–222). Text tightened to "=Sigmoid"/"=Linear" (original is tight; cropA item 6). |
| 8 | This worker: **fn-label fontSize 16→14** (still wrapped at 16pt; original ink 63.5px wide, cap ~10.5 slide px → ~14pt). Final build; render_8. |

## Closed-loop verification (attempt 8, all banked)

- `house_chrome_check.py`: **PASS** (panel x 89–1913, badge center (1860,148) d=70).
- `selfcheck8.py` (render-vs-original direct, mapped): braces d ≤ 5.4/4.6; y1/y2 labels
  d ≤ 6.3/2.3; sigmoid d 2.4/4.5 (single line, correct size/position). Documented
  predicate/window artifacts (not defects): y4 rim-halo in original zone; arrow
  left-extension = 009-certified shaft geometry vs JPEG-faded ink; callout2 dark
  drop-line pixels; pill window clipping. callout1: 2 text bands, pitch exactly 27px (13pt).
- Re-render determinism: render_6 == render_5 byte-identical (md5) before the fixes.

## Vision evidence (through scripts/16_vision_gate.sh only)

- `cropA_attempt_2.txt` — middle-panel row crop (attempt 8 vs original): **PASS**, no fix triggers.
- `cropB_attempt_2.txt` — right-panel crop: **PASS**, no BLOCKER/MAJOR (attempt-4 brace MAJOR resolved).
- `judge_attempt_1.txt` — full-slide judge attempt 1: **PASS**, issues [] (2 non-blocking
  MINOR notes: subtitle q-subscript baseline offset; weight-label antialiasing).
- Probe: 2 hangs (RC 124) on the shared fleet gate → skipped per certified 009 precedent
  + dispatcher directive (comparison is the evidentiary call).
- judge_prompt_1.txt banked before dispatch (frozen template + GROUND RULES; worker-editable
  context carries the 10←9 inheritance + playlist chrome law).

## Banking

- No slide in EITHER deck's slide_dependencies.json references 002:10 as a content parent
  (checked both; P1 members 12/14/16 are pattern siblings, not dependents) → **no
  components/slide_010.js export required**. The build script notes it is importable by
  P1 members only as a PATTERN reference.
- Group-shared pattern asset banked for P1 members 12/14/16: `qa/slide010/gen_brace_pattern.py`
  (bezier curly-brace → 600dpi transparent PNG + exact-size embed sidecar pattern), assets
  live in `build/assets/s010_brace{L,R}.png/.json`.
- All 8 build attempts + renders 1–8 preserved; nothing deleted.

## Known minor deviations (documented, judge-accepted)

- "=Linear" ink center 4.2 slide px right of the original's (same width; sub-visible;
  row-1 sigmoid centers match exactly).
- Subtitle W_q subscript baseline offset; weight-label antialiasing (judge MINORs).
