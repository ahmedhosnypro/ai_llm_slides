# Worker report — slide 036 (Self Attention Mechanism, Scaling based on √d)

Deep Learning DSAI 308, Transformers — Part I (`videos/deep-learning/001_transformers_part1`).
Build worker run 2026-10-11. Deliverable: `recreated_pptx/slide_036_recreated.pptx`
(single-version law; no suffix variants).

## Result

- **Verdict: PASS — judge attempt 2 of 6** (attempt 1 also PASSed the full-slide
  comparison, but the mandatory dense-region crop battery found a MAJOR the full-slide
  judge had missed; the fix was applied and the slide re-judged).
- Full-slide judge transcripts (real comparison winner bodies, degenerate events 0):
  - attempt 1: `qa/slide036/judge_attempt_1.txt` — PASS, 4 MINOR (render_5)
  - attempt 2: `qa/slide036/judge_attempt_2.txt` — **PASS, 3 MINOR** (render_7; DB-recorded)
- Dense-region crop compares (self-check #6, full judge params):
  - `cropcmp_eqbox_1.txt` — PASS (render_5)
  - `cropcmp_formularow_1.txt` — PASS w/ noted bracket-proportion deviation (render_5 → fixed)
  - `cropcmp_fc2_1.txt` — PASS (render_5)
  - `cropcmp_vec_1.txt` — **FAIL (MAJOR: delimiter shape family)** → fixed →
    `cropcmp_vec_2.txt` — **PASS** ("square serif-style brackets … prior flag resolved")
- Judge prompt banked verbatim (frozen template from `scripts/17_worker_instructions.md`):
  `judge_prompt_1.txt` / `judge_prompt_2.txt`, payload `judge_p_payload_1.txt`.
  Build provenance: `build_attempt_1.js` / `build_attempt_2.js`.
- DB: `gen_status=passed`, `visual_check=PASS`,
  `visual_transcript=…qa/slide036/judge_attempt_2.txt`, `visual_attempts=2`.
- Judge subagent spawn: NOT available in this environment (no Agent/Task tool) — the
  judge procedure was executed by the worker itself via Bash through
  `scripts/16_vision_gate.sh` + `.agents/skills/image-analysis/scripts/analyze_image.py`,
  byte-for-byte per the banked prompt (documented orchestrator-approved fallback, 17 §7).
  Label: per-read single comparison, default route (`images`, no --models), glm leg
  DEFERRED. Note: `analyze_image.py` lives at `.agents/skills/image-analysis/scripts/`
  (the 17 template's `.agents/image-analysis/scripts/` path is stale).

## Renders (all banked in `qa/slide036/`)

| file | note |
|---|---|
| `render_1.png` | first build — title/subtitle unit bug caught by self-check |
| `render_2.png` | title/subtitle fixed; font calibration round 1 |
| `render_3.png` | calibration round 2 (statements/FC labels/Remember) |
| `render_4.png` | calibration round 3 (subtitle 20pt, statements 18.5pt, FC2 hairline parens) |
| `render_5.png` | highlight as explicit rect (LO `highlight` quirk); judged attempt 1 |
| `render_6.png` | square brackets v1 (glyph-squash arms too thick — replaced) |
| `render_7.png` | **final deliverable render** — square brackets drawn at measured geometry; judged attempt 2 PASS |

Renders 1–6 are self-check/fix iterations; the judge loop used 2 attempts (render_5,
render_7). `house_chrome_check.py` PASS on render_7 (panel x89–1913, badge (1860,148)
d70, tol 8).

## Pre-judge self-check battery (banked `scratch/slide036/selfcheck_*.py`)

1. REUSABLE PATTERNS: `patterns/index.json` read; used `equations-mathtext-png`
   (mathtext → 600dpi transparent PNG → addImage exact px/600, baseline-law alignment,
   closed loop ≤5 frame-px on every equation band), `delimiters-stretched-glyph` (FC/BOX
   parens), a measured-geometry square-bracket generator for the VEC enclosures (the
   stretched-glyph squash could not reproduce the 2px serif arms + notch),
   `judge-invocation`, `dense-region-crop-compare`.
2. FRAME CONTAINMENT: 0 content-ink px outside the house panel (badge excluded).
3. EQUATIONS EXIST: all 7 equation regions carry ink.
4. DELIMITER GEOMETRY: all delimiter/bracket spans within tolerance of the original's
   measured spans (VEC brackets y134..347 / y133..212, ±2px).
5. TABLE DATA: n/a (no dataset table).
6. ZOOMED CROP COMPARISONS: 4 regions run at full judge params (vec, eqbox,
   formularow, fc2) + the vec re-compare after the fix — all transcripts banked.
7. LINE/BOX WRAP: all text boxes single-line at measured y; no ink outside expected bands.
8. EXPLICIT LINE SPACING: no multi-line text box exists (per-line boxes); pitch is positional.

## Geometry & color provenance

PIL pixel forensics on `unique_slides/slide_036.jpg` (960×540, 1px = 1pt = 1/72 in):
`scratch/slide036/measure1..19.py`. Colors reconciled from darkest-2% stroke cores
(video-chroma corrected): maroon 990000, blue 0000B0, C00000, green 3B7A40, indigo
333399, purple 800080 + fill F9E3FA, highlight FFFF00, chip fills FFFCC0/FFFDCE.

**Measured frame facts that OVERRIDE the spec JSON** (frame is ground truth; also in
the build header):
- Equations-box border GREEN (spec said red), fill WHITE (spec said mint E7F0E2),
  rounded corners.
- Statement-box 1 fill pale green E6FCEC (spec said white).
- Statement math tokens (√d, ⁴√d) BLUE, prose MAROON (spec said green token / dark prose).
- Formula boxes 1+2: entire content maroon 990000 incl. w′ᵢⱼ (spec said blue math).
- FBOX3: 'd=100,' blue + '√d' MAROON + ' =10' blue.
- EQBOX L1/L2: black prose + maroon V₁/V₂ token + blue M; L3/L4: blue bold italic with
  maroon V-token (x439..451) and maroon √d-token (x610..633).
- **V₂ toy columns contain FOUR glyphs each** (left X bands y142/158/175/192; right M
  bands y142/161/180/199; brackets span y133..212) — NOT five as the spec claims.
  Both crop-compare judges independently counted 4+4 and 12+12 ("counts exact match").
- **VEC enclosures are SQUARE serif brackets** (vertical stroke 3px + 2px arms with
  notch), not parentheses — caught by the vec crop compare, confirmed by 1px pixel maps.
- FC1 fill = panel gray, border 1A1A1A; output-chip digits BLACK.
- Bell box border INDIGO (spec said red); red L-axes inside (x704/y201) are real.
- Subtitle maroon 990000, highlight FFFF00 on '(Scaling' (measured block x196..267
  y77..98, drawn as an explicit rect — LO mis-renders pptxgenjs run `highlight`).
- FC2 parens are HAIRLINES (~4px) unlike VEC/FC1; FBOX2 parens ~2px.

## Judge findings & dispositions (final, attempt 2)

1. MINOR — Gaussian grid scale slightly larger than original (curve/axes/dashed/M all match). Accepted.
2. MINOR — rightmost blue ")" close to the purple frame (no touch). Accepted (measured containment: 0 px outside).
3. MINOR — FBOX1 bracket weight heavier than original. Accepted (shape/span correct).
Carried MINORs from the crop battery: math glyph serif-vs-sans (rule d/medium),
radical size slightly larger (rule e), 1xd₂ vertical gap ~2% larger, dashed-line top
extent slightly lower. All non-blocking, all banked in the transcripts.

## Environment notes

- /tmp quota-blocked → scratch under `scratch/slide036/`; TMPDIR prefixed for soffice
  and the vision gate; private LO profile `scratch/slide036/lo_profile`.
- Vision route congested early (probe HangError ×2 at the script's 150s hard wall);
  judge comparisons landed on first background attempts thereafter.
- Dependency status: 36 = root (unblocked); no dependents → no component export required.

## Artifacts

- Deliverable: `recreated_pptx/slide_036_recreated.pptx`
- Build: `recreated_pptx/build/slide_036.js` (+ `qa/slide036/build_attempt_1.js`, `build_attempt_2.js`)
- Assets: `recreated_pptx/build/assets/slide036/` — 8 mathtext equation PNGs + sidecars,
  24 delimiter/bracket PNGs + sidecars, `bell_plot.png`
- QA: `qa/slide036/` — renders 1–7, judge_prompt_1/2.txt, judge_attempt_1/2.txt,
  cropcmp_eqbox_1 / formularow_1 / fc2_1 / vec_1 / vec_2 .txt, build_attempt_1/2.js
- Forensics: `scratch/slide036/` (measure*.py, selfcheck_*.py, crops/)
