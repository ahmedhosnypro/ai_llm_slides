# Worker report — slide 049 "Transformer Stacked Encoder Blocks" (002_transformers_part2)

Worker: fresh dispatch build worker, sole owner (peer-collision check performed on
coordinator warning at 06:53 EEST: no active peer — only own processes; prior worker's
04:46–05:00 measurement scratch was ~2h stale and reused per the resume law; DB row had
no field changes from others).

## Dependency gate

- `deps`: 49 ← 26 (in-video). Parent 26 certified in this deck's DB
  (gen_status=passed, visual_check=PASS) → UNBLOCKED, build permitted.
- Build IMPORTS the certified parent composition
  `recreated_pptx/build/components/slide_026.js` and calls
  `renderBase(pptx, slide, { numeral: 49, only: [] })` — the parent contributes the
  playlist house chrome with this slide's badge numeral (49, printed on slide_049.jpg).
  Slide 49 shares NO content blocks with 26 (pattern-derived dependency,
  "common patterns but not same as them" per deck AGENTS.md + SOURCES.md), so the
  entire content is this slide's own measured delta, drawn at geometry PIL-measured
  from THIS frame through the deck's fitted frame→slide mapping
  (frame_x = 18.628 + 0.96123·slide_x; frame_y = 0.95556·slide_y — the same mapping as
  the certified 002 slide_002 build and slide_026 component).

## Analysis inputs (no re-run of 12/13, per dispatch)

- Spec FINAL: analysis/slide_049_final.json (PASS_WITH_FIXES, recreatability 9).
- Provenance: slide_049_source/SOURCES.md (Vaswani §3.1/§3.5 anchors; course quirks
  kept verbatim: Word Embedding bar ABOVE the PE bar; blocks 0..M).

## Measurement + pre-judge verification (banked evidence)

- PIL census: scratch/slide049/measure_full.py/.json, probe2/3 (this worker) on top of
  the prior worker's measure_chrome/regions/bands/lines + 6–8x zoom crops.
- Vision-gate crop readings (dense-region self-check #6 surrogate; no equations,
  tables, or multi-line delimiters on this slide, so the crop-comparison clause is not
  mandatory — original-side crops were still read through the gate):
  qa/slide049/crops_sheetA.txt (chips: 5 sub-cells yellow→green→peach→lavender→pink,
  dark-red serif italic labels; **X_{N-1} confirmed — resolves the spec's X_{N-3}[?]**;
  5 ellipsis dots per row), crops_sheetB.txt (left column: cream-filled red-bordered
  boxes, non-boxed red italic "Embedding Words & Pos.", vertical bottom-to-top blue
  bold italic "Transformer Encoder"), crops_sheetC.txt (arrow families are hatched
  block arrows; **NO gray arrows between word row and embedding box** — the spec's
  "8 gray up-arrows" was a full-slide analysis hallucination; the real arrows there
  are navy-outline/white-fill block arrows; one black-bordered box encloses both
  embedding bars; navy bottom rule = content, also present on slide 045, NOT player
  chrome; the black strip y≥517 IS the player bar and is excluded per GROUND RULES).
- house_chrome_check.py: PASS on every render (1 and 2).
- Closed-loop PIL geometry self-checks (~4px tolerance, 150dpi): selfcheck_attempt_5.py
  → 33/36 PASS on render_2; the 3 residual single-edge deltas (Y-label x0 +2.4 frame px,
  word-label-1 x0 −2.4, vertical-text x1 −1.9) are glyph-halo/ink-distribution variance —
  element centers and sizes all within tolerance (selfcheck_attempt_5_out.txt).
  Attempt history: v1 (24/36 — window pollution bugs diagnosed), v3 (17/36 — real font
  deltas fixed: title 28pt+charSpacing, token labels, vertical text, left column),
  v4 (30/36), v5 (33/36 + word-row wrap proof).
- Word-row single-line proof after the attempt-1 fix: all 8 boxes show ONE contiguous
  label band (rows ~1064..1087) with clear margins from the box borders.

## Builds & judge attempts

- Attempt 1: build_attempt_1.js → render_1.png → judge FAIL
  (judge_attempt_1.txt): one MAJOR — "Word N-2"/"Word N-1" wrapped to two lines and
  overflowed their 60px boxes (my 16pt BOLD was too wide). All content otherwise
  verified present/verbatim/positioned.
  Fix (frame-metric-backed): word labels NON-bold Times italic 16pt + wrap:false
  (original ink 41–52px at cap 10px ⇒ ~0.455em/char ⇒ non-bold). → build_attempt_2.js,
  render_2.png, chrome check PASS, self-check 33/36 + single-line proof.
- Attempt 2: judge PASS (judge_attempt_2.txt) — "No BLOCKER or MAJOR defects found:
  all text verbatim, all rows/regions present, no missing elements, no frame overflow".
  3 MINOR notes (dot-count readability at 150dpi — PIL census says 5 dots/column and 5
  are drawn; stack-region proportion nuance within template tolerance; arrow glyph
  proportions slightly taller/narrower — same counts/colors/alignment).

## Deliverable (single-version law)

- videos/deep-learning/002_transformers_part2/recreated_pptx/slide_049_recreated.pptx
  (plain name; build chain: recreated_pptx/build/slide_049.js)

## DB final state

gen_status=passed · visual_check=PASS · visual_attempts=2 ·
visual_transcript=qa/slide049/judge_attempt_2.txt · pptx_path/build_script set.

## Banking

No deck's slide_dependencies.json references 002:49 as a parent (checked
001_introduction, 001_transformers_part1, 002_transformers_part2) → no component
export obligation. (If a future deck needs it, the composition is expressible from
build/slide_049.js's DELTA blocks.)

## Provenance notes

- Judge procedure executed by the worker (no spawn tool in this environment;
  orchestrator-approved fallback), through scripts/16_vision_gate.sh, default route
  (images), streaming; transcripts banked. Certificate: single-read comparison,
  default route, thinking=high, max-tokens 65536, frozen GROUND RULES prelude.
- Gateway flakiness encountered: 2 probe aborts (HangError at 150s; EmptyStreamError
  after the mandated sleep-300 re-probe) before the attempt-1 comparison — the
  comparison itself landed on first invocation both attempts (one empty-stream inside
  attempt-1's race was absorbed by the gate's internal retries).
- Colors are PIL census cores / vision readings per region (frame wins over spec
  approximations, per the certified 026 precedent): navy #00008B (borders/dots/arrow
  outlines), bar blue #353BB7, stack #C9DFF0, tan #FDE9D9 / cyan #CCFFFF, red #C00000,
  label red #990000, green arrow #BAEDC2/#2E8B57, left-column cream #F9E8D6.
