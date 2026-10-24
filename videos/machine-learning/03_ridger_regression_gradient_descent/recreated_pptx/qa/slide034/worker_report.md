# Slide 034 "Non-Convex Function" — worker report (worker-fresh-034b)

## Attempt history

| # | render | build | table crop | plot crop | Template A | outcome |
|---|--------|-------|-----------|-----------|------------|---------|
| 1 | render_1 | prior worker | — | — | — | prior worker, superseded |
| 2 | render_2 | prior worker | — | — | judge_attempt_2.txt | banked |
| 3 | render_3 | slide_034.js (fixed x-row 9.6) | crop_3_table_judge.txt = **FAIL** (x-row c16/c18 must be 9.6) | — | — | FAIL adjudicated |
| 4 | render_4 | slide_034.js | — | — | — | banked, superseded |
| 5 | render_5 | slide_034.js (01:57) | — | — | — | byte-identical to render_6 |
| 6 | render_6 | **slide_034_attempt6.js** (04:38) | crop_6_table → run pending | crop_6_plot → run pending | judge_attempt_6 → run pending | **IN PROGRESS** |

## STEP 1 — fresh PIL adjudication of the x-row c16/c18 FAIL

Verdict recorded in `step1_xrow_verify.txt`. Summary:
- Method: locate the x-row text band (rows 333..347) from the frame's horizontal
  gridlines (330/331 top, 348/349 bottom); the 18 data cells are the group spans
  c13 641-651, c14 682-692, c15 725-734, c16 765-775, c17 807-817, c18 843-853;
  classify the units digit by NCC of the right-digit bitmap against c14 (known '6')
  and c15 (known '8').
- Controls: c14 → 1.000 vs 0.888 ⇒ '6' (expected 6) OK; c15 → 0.888 vs 1.000 ⇒ '8'
  (expected 8) OK. Method validated.
- Results: c17 → '8' (both extractions agree). c16 and c18 are **indecidable** at
  6 px glyph height — the two independent extractions disagree and no hard frame-based
  refutation exists in either direction.
- Decision: **keep the banked fix** (x c16=9.6, c18=9.6). The frame does not refute
  it, four independent rows of the slide's own table force it, and the banked
  orchestrator ruling stands. No build change was needed — the build already carried
  `x = [..., 9.4, 9.6, 9.8, 9.6, 9.8, 9.6]`.

## STEP 2 — rebuild (copy-then-modify, never edit a certified file in place)

- `build/slide_034_attempt6.js` = byte-identical copy of `build/slide_034.js`
  (`cmp` verified). Output path unchanged: `recreated_pptx/slide_034_recreated.pptx`.
- Registered in DB: `build_script = .../build/slide_034_attempt6.js`.
- Pipeline: `node build/slide_034_attempt6.js` (run from the PROJECT ROOT, paths in
  the script are root-relative) → `soffice --headless --convert-to pdf` with a fresh
  `-env:UserInstallation` → `pdftoppm -png -r 150 -singlefile` → `render_6.png`
  (2001×1125). All under `TMPDIR=.../scratch/tmp`.
- render_6 is byte-identical to render_5 (diff px = 0) — the fix was already present.
- **SELFCHECK: PASS** (`selfcheck_attempt_6_output.txt`): ABOVE-PANEL ink none;
  panel content ink x67.2..894.2 y54.1..516.4; equation ink 3780; 144/144 table
  values present; **dataset invariants 7/7 hold**; analytic curve residual median
  0.27 px / p95 0.95 px / 96.94% within 2px.
- **HOUSE CHROME CHECK: PASS**: panel x112-1882, y94-bottom; strokes L/R/bottom
  present, **top bare**; badge center (1824,152) d=68; all within tol 8.
- NOTE for the next worker: `selfcheck_attempt_2.py` defaults to `render_1.png` when
  called with no argument — always pass the render path explicitly.

## STEP 3 — judge legs on the CURRENT render (render_6)

Crops re-cut from render_6 at matched effective scale (2.084 px/frame-px both sides,
LANCZOS ×(1125/540)); `make_crops_6.py` asserts the match:
- table: slide bbox (74,313)-(887,525), both crops 1694×442
- plot : slide bbox (599,50)-(853,321), both crops 529×565
- `crop_6_table_orig/plot_orig` are byte-identical to crop_4's originals (0 diff px);
  the render sides differ because crop_4 was cut from render_4. Both legs therefore
  MUST be re-run on crop_6 (no crop transcript is reusable).

Payloads verified byte-for-byte against `shared_patterns/judge_protocol_03.md`:
Template A = `judge_prompt_6.txt` (4115 chars, md5 9387f5fbb9), Template B with
NNN→034 = `crop_table_prompt_6.txt` / `crop_plot_prompt_6.txt` (1914 chars, md5
d137335f92). Only the trailing file newline differs from the fenced block.

Dispatch scripts banked and syntax-checked: `judge_crops_6.sh <table|plot> <transcript>`
and `judge_templateA_6.sh`.

### Gateway status (real numbers, not pgrep noise)

`pgrep -c -f analyze_image.py` reported 25-30, but that counts parked `timeout`/`bash`
wrappers whose python child already exited. The real measure:
- live python vision calls: **6-8**
- flock slots actually held: **5 of 16** (slots 5-15 all test FREE)

So a slot WAS available. The probe (`timeout 150 ... --timeout 120`) returned
rc=124 — the outer `timeout 150` fired before the call completed. Per protocol
("a hang means sleep 300 and re-probe ONCE") a 300 s sleep was started and ONE
re-probe is the only remaining probe attempt.

## Verdict transcripts (to be banked)

- table leg → `recreated_pptx/qa/slide034/crop_6_table_judge.txt`
- plot  leg → `recreated_pptx/qa/slide034/crop_6_plot_judge.txt`
- Template A → `recreated_pptx/qa/slide034/judge_attempt_6.txt`

## DB row at hand-off

`gen_status=building`, `visual_check=null`, `visual_attempts=2`,
`worker_id=worker-fresh-034b`, `build_script=.../slide_034_attempt6.js`,
`pptx_path=.../slide_034_recreated.pptx`.

## STATUS: **UNFINISHED** — both judge legs still to run on render_6.

Blocking condition: the shared localhost:17844 vision gateway is saturated fleet-wide
(16 flock slots, 5-16 live calls from other lanes). Per VISION GATE LAW I must wait
for a slot, never retry-loop the gate, and never trim a payload.

Resume steps for the next worker:
1. `VIDEO=machine-learning/03_ridger_regression_gradient_descent python3 scripts/15_progress.py claim 034 <your-id>`
2. Probe: `timeout 150 bash scripts/16_vision_gate.sh python3 .agents/skills/image-analysis/scripts/analyze_image.py analysis $B/recreated_pptx/qa/slide034/render_6.png --view "Slide 034 recreation attempt 6 — probe" --capture "150dpi PNG render of a 13.33x7.5in PPTX" --timeout 120 --rounds 1 --tries 1 --transcript $B/recreated_pptx/qa/slide034/probe_6.txt`
3. Table leg: `bash $B/recreated_pptx/qa/slide034/judge_crops_6.sh table crop_6_table_judge.txt`
4. Plot leg:  `bash $B/recreated_pptx/qa/slide034/judge_crops_6.sh plot crop_6_plot_judge.txt`
5. Template A: `bash $B/recreated_pptx/qa/slide034/judge_templateA_6.sh`
6. Adjudicate any finding PIL-first against the ORIGINAL frame before any edit.
7. On both legs PASS: `record-visual 34 PASS <transcript>`, `set 34 gen_status passed`,
   `release 034 <worker-id>`, verify with `get 034`.
