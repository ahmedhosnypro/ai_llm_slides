# Slide 027 worker report — "Self Attention Mechanism (Fundamental Operation)"

Deep Learning DSAI 308, `videos/deep-learning/001_transformers_part1`. Worker: slide-027
build worker, 2026-10-11. DEPENDENCY-GATED CHILD (27 <- 26, parent 26 certified
passed/PASS at dispatch — `15_progress.py deps` reported 27 `unblocked`).

## Result

- **Final verdict: PASS (attempt 1 of 6 used)** — real comparison transcript:
  `recreated_pptx/qa/slide027/judge_attempt_1.txt` (single-read, default route images,
  `--thinking high --max-tokens 65536`, W4 wall; probe landed on the 2nd call after one
  documented sleep-300 re-probe).
- **Deliverable (SINGLE-VERSION law):** `recreated_pptx/slide_027_recreated.pptx`
- **Build script:** `recreated_pptx/build/slide_027.js`
- **DB:** gen_status=passed, visual_check=PASS, visual_attempts=1,
  visual_transcript=qa/slide027/judge_attempt_1.txt.
- **Judge procedure executed by the worker** (no Agent/Task spawn tool in this
  environment) — the documented 17 §7 self-execution fallback, byte-for-byte per the
  banked prompt `qa/slide027/judge_prompt_1.txt`.

## Child-build compliance (dependencies.md)

- Base = certified component `components/slide_026.js` via `renderBase(pptx, slide, {})`
  — never re-derived. House chrome drawn ONCE via `components/house_chrome.js`
  (`drawHouseChrome(pptx, slide, {numeral: 27})`), before renderBase.
- Delta (verified pure addition; the only non-delta inter-frame diffs are
  panel-border/canvas-edge capture jitter):
  1. top-right white box + `y_i = Σ_j w_ij x_j` (mathtext PNG, large Σ, j limit below)
  2. bottom-center-left box + `w'_ij = x_i^T x_j` (mathtext PNG)
  3. bottom-center-right box + `w_ij = exp w'_ij / Σ_j exp w'_ij` — composed of TWO
     mathtext PNGs + a drawn fraction bar (the original's generous bar clearance and
     small side-set Σ_j cannot be matched by a single \frac render)
  4. boxed `X_ℓ` label above the left stack (white box, blue X + blue script-ℓ)
  5. boxed `X_i = X_2` label above the strip's X2 (red X_i, red =, blue X_2)
  6. worked-example table at bottom right: brown-bordered pale-yellow table
     (x678..867, y418..519), headers Output/layer, Softmax/activation function,
     Probabilities (Arial Narrow — measured digit w/h ratio 0.64 = Narrow), bracketed
     column vectors [1.3 5.1 2.2 0.7 1.1] and [0.02 0.90 0.05 0.01 0.02]
     (SOURCES.md-verified 5/5), black-bordered fraction box with
     `e^{z_i} / Σ_{j=1}^K e^{z_j}` (side-set limits, as measured), two black arrows.
     Drawn AFTER renderBase — covers the parent's right feed curve exactly as in the frame.
  7. red `Remember` note (regular 11pt, muted red 943634 — crop-compare corrected an
     initial bold/C00000 draft).

## Equation mechanism (Math equation format rule)

`scripts/render_eq.py` (matplotlib mathtext → 600 dpi transparent PNG → addImage at
exact px/600 size, never rescaled). Assets banked under
`recreated_pptx/build/assets/slide027/` with sidecar JSONs (baseline_frac used for
baseline/bar alignment). Closed-loop PIL verification: every equation's render ink bbox
matches the original's measured ink bbox within ≤3.5 render px (tolerance ~6.5).

## Pre-judge self-checks (all PASS — `scratch/slide027/selfcheck_attempt_1.py` + output)

house_chrome_check PASS; inheritance diff vs certified parent render confined to delta
zones (79 px residual = Remember AA jitter, tol 400); house containment clean; every
equation region has ink; bracket delimiters span all 5 value rows with 1.9-2.9 px
clearance; explicit lineSpacing verified (value pitch 29.0 render px = 14pt; header
pitch 15.5 = 8pt); Remember single-line (probe caught a wrapped 'r' in the draft — fixed
with wrap:false + wider box); 6 gated zoomed crop comparisons banked under
`scratch/slide027/crops/cmp_*.txt` — table/eqtop/eqbc/xell/xx2/remember all favor the
render or flag only MINOR weight/color impressions; the "colored subscripts" the crop
model saw in the equations was measured to be JPEG chroma fringing (subscript cores are
black in the original).

## Judge findings (all MINOR, none fix triggers on this slide's delta)

1. MINOR multiplier glyph style (⊛ vs ⊗) — INHERITED parent region (slide 026's certified
   nodes) → judge variance per the dependency law, not charged.
2. MINOR Dot Product dot rings — INHERITED parent region → judge variance.
3. MINOR faint red fan-lines — INHERITED parent region → judge variance.
4. MINOR X_i = X_2 vs "X=X2" at video resolution — low confidence; delta spec + pixel
   forensics (red sub-i glyphs at x253..254) confirm X_i = X_2.

## Deliberate omissions (documented)

- The faint 1-2px gray canvas-bottom-edge line at y~522-523 present in BOTH frames 26 and
  27 is a video-encode artifact; the certified parent component omits it → omitted here
  (judge-variance defense banked in the build header).
- OMML dual-representation wrap NOT applied: out of this slide's dispatch scope, and the
  deck's certified precedent (slide 011, which has equations) ships PNG-only (no
  mc:AlternateContent in its XML). The BC_R equation is also composite (2 PNGs + drawn
  bar), which the wrapper's single-pic manifest does not model. Left to the orchestrator.

## Evidence index

- Render: `recreated_pptx/qa/slide027/render_1.png`
- Judge prompt (banked): `recreated_pptx/qa/slide027/judge_prompt_1.txt`
- Judge transcript: `recreated_pptx/qa/slide027/judge_attempt_1.txt`
- Probe transcript: `recreated_pptx/qa/slide027/probe_1.txt`
- Build provenance: `recreated_pptx/qa/slide027/build_attempt_1.js`
- Self-check: `scratch/slide027/selfcheck_attempt_1.py` +
  `scratch/slide027/selfcheck_attempt_1_output.txt`
- Crop compares: `scratch/slide027/crops/cmp_{table,eqtop,eqbc,xell,xx2,remember}.txt`
  (+ original crop structure read `crops/orig_table_read.txt`)
- Equation assets: `recreated_pptx/build/assets/slide027/` (eq27_yi, eq27_wprime,
  wfA/wfB/wfC, eq27_smx + sidecar JSONs)
