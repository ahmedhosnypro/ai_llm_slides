# Worker report — slide 027, 001_introduction (Deep Learning DSAI 308)

**Slide:** 27 — "[4] Introduction to Deep Learning and CNN" (section [4] divider)
**Date:** 2026-10-12 · **Worker:** slide-recreation builder (fresh start, ROOT — no
dependency edges: `slide_dependencies.json` has no 27 row; `deps` shows root/unblocked)

## Dispatch-note correction (recorded, not acted on)

The dispatch's "SLIDE FACTS" parenthetical described a "Visualization of Single
Perceptron" slide with equations — that is an old-numbering slide (founder swap
`new 22←old27` territory), NOT this slide. The authoritative sources — ground truth
`unique_slides/slide_027.jpg` and the PASSED spec `analysis/slide_027_final.json` —
agree: this is the four-line title slide, **no equations, no bullets**. Built per the
actual ground truth. `slide_027_source/SOURCES.md` honored (web verification discharged
at analysis stage; nothing from sources appears on this title slide).

## Verdict chain (attempt 1 of max 6 — PASS on first attempt)

1. **PIL forensics** (`scratch_027/measure_027.py`, `measure2_027.py`, `measure3_027.py`):
   4 title text bands measured; font solve — Liberation Sans Bold (sans) wins decisively
   on all lines (IoU 0.83–0.90 vs Liberation Serif Bold 0.31–0.60); sizes L1=50, L2=70,
   L3=48, L4=71 pt; baselines 169.5 / 280 / 346.5 / 422.5; ink centers 473 / 479.5 /
   478.5 / 478.5; title ink #B4000B (5x5-core modal, overrides spec's #C11B22 estimate
   per deck law); black strip rows 519–539 + mouse cursor (276–288, 443–457) = video
   artifacts, omitted per spec recreation_brief + judge ground rule (c).
2. **Build** (`recreated_pptx/build/slide_027.js`): playlist house chrome via
   `shared_patterns/house_chrome.js` `drawHouseChrome(pptx, slide, {numeral: "27"})`
   (imported, never re-drawn; originals carry no printed numbers — numeral = file number
   per 001_introduction/AGENTS.md, pending founder veto). Four single-line text boxes,
   Arial Bold (LO → Liberation Sans), measured per-line size/baseline/center-x, the
   slide_015-certified baseline model (`baseline = box_top + ascent·size`,
   ascent = 0.9053 = LibSans hhea 1854/2048, `lineSpacing = boxH = (asc+desc)·size`),
   `lineSpacing` explicit, `margin: 0`, bare hex, `fontFace` everywhere.
3. **Render**: private LO profile + TMPDIR inside the namespace
   (`scratch_027/lo_render/`), 150 dpi → `qa/slide027/render_1.png`.
4. **Pre-judge self-checks (all PASS)**:
   - `house_chrome_check.py` → PASS (panel x 89–1913, badge center (1860,148) d=70 render px).
   - Closed-loop PIL (`qa/slide027/selfcheck_attempt_1.py` + `_out.txt`): all 4 line
     bands within **2.2 frame px** (tol 4), flat-glyph baselines within **0.3 px**,
     centers within 1.9 px, core color exactly #B4000B, containment TRUE, zero red ink
     outside the panel block. (No equations/tables/delimiters on this slide — the
     equation-alignment, delimiter-geometry, table-data and mandatory-crop-comparison
     checks do not apply.)
5. **Judge (attempt 1)** — no Agent/Task spawn tool in this environment; the banked
   judge procedure was executed by the worker via Bash, byte-for-byte per the banked
   prompt (orchestrator-approved fallback per scripts/17_worker_instructions.md §7):
   - Probe: `probe_1.txt` — valid window; transcription confirms badge "27" + the four
     verbatim title lines.
   - Comparison: `scripts/16_vision_gate.sh timeout 1700` wrapper, `--timeout 280`,
     `--thinking high --max-tokens 65536`, `-p "$(cat judge_p_payload_1.txt)"` (frozen
     ground rules, numeral 27) → `judge_attempt_1.txt`, real winner body, 0 degenerate
     events.
   - **FINAL VERDICT: PASS** for 'faithful, usable recreation'. Findings: 0 BLOCKER,
     0 MAJOR; 2 MINOR (title-block vertical placement ~2–3% of panel height, judged
     "borderline perceptible; not actionable" — contradicted by the pixel-measured
     closed-loop band deltas ≤2.2 px, so judge variance; letterform antialiasing = medium
     difference). Certificate basis: single-read, default route (images), glm leg
     DEFERRED/BLOCKED.

## DB state (VIDEO=deep-learning/001_introduction, slide 27)

- `gen_status=passed` · `visual_check=PASS` · `visual_attempts=1`
- `visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide027/judge_attempt_1.txt`
- `pptx_path=videos/deep-learning/001_introduction/recreated_pptx/slide_027_recreated.pptx`
- `build_script=videos/deep-learning/001_introduction/recreated_pptx/build/slide_027.js`
- `last_error=null`

## Deliverable & evidence

- **Deliverable (single-version, no suffix):**
  `videos/deep-learning/001_introduction/recreated_pptx/slide_027_recreated.pptx`
- Build: `recreated_pptx/build/slide_027.js`; provenance copy
  `qa/slide027/build_attempt_1.js`
- Judge: `qa/slide027/judge_prompt_1.txt`, `judge_p_payload_1.txt`, `probe_1.txt`,
  `judge_attempt_1.txt`, `render_1.png`
- Self-checks: `qa/slide027/chrome_check_1.txt`,
  `qa/slide027/selfcheck_attempt_1.py` + `selfcheck_attempt_1_out.txt`
- Forensics: `scratch_027/measure_027.py`, `measure2_027.py`, `measure3_027.py`
- No OMML pass (no equations). No component banking obligation (no dependents in any
  video's graph — dispatch confirms).

## Deviations / notes

- None from spec content. Title color #B4000B (measured) vs spec estimate #C11B22 —
  measurement wins per deck AGENTS.md law. Chrome (panel/badge) follows the playlist
  law, not this frame's own inset border (founder directive 2026-10-11; judge ground
  rule (a)). Cursor + bottom black strip deliberately omitted (spec + ground rule (c)).
- Two self-check script iterations fixed unit bugs in MY checker (assertions compared
  render indices vs frame thresholds); the BUILD was never changed after attempt 1 —
  one build, one render, one judge.
