# Worker report — slide 026 "Self Attention Mechanism (Fundamental Operation)"

Video: `videos/deep-learning/001_transformers_part1` (Deep Learning DSAI 308, Transformers Part I)
Worker: per-slide BUILD WORKER, 2026-10-11. **Dependency status: ROOT with dependents 27, 28, 29.**
Final verdict: **PASS** (judge attempt 1) — DB `gen_status=passed`, `visual_check=PASS`.

## Deliverable

- `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_026_recreated.pptx` (single-version law)
- Build: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_026.js`
  (pptxgenjs, LAYOUT_WIDE; house chrome via `drawHouseChrome(pptx, s, {numeral: 26})`)

## Shared components (for dependents 27/28/29 — confirm final)

- `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js`
  — delegates verbatim to `videos/deep-learning/shared_patterns/house_chrome.js` (created by the
  parallel slide-6 worker; identical content to the shared pattern by construction).
- `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_026.js`
  — the certified base composition: `renderBase(pptx, slide, opts)` at BLOCK granularity with
  `opts.skip` / `opts.only` selectors. Blocks: `canvas, title, stackLeft, dotProduct, softmax,
  sigma, yOutput, arrowsGreen, labels, flowLines, stackRight, strip, queryArrows, feedCurves`
  (canonical z-order in `ORDER`; house chrome deliberately NOT drawn here — children draw it once
  via `components/house_chrome.js` then call `renderBase`). Colors/block functions exported via
  `COLORS / FONT / BLOCKS / ORDER`. Component frozen as of this PASS — copy-then-modify, never
  edit in place (cascade law).

## Geometry provenance

PIL pixel forensics on `unique_slides/slide_026.jpg` (960x540, 1px = 1pt), 12 measurement rounds
(scripts in `scratch/slide026/`: measure_original.py, blobs.py, geom_masks.py, precision.py,
micro.py, round3–12.py) + an 8-panel vision structure read (`qa/slide026/structure_probe.txt`).
Key measured facts (all in the component header): peach canvas x52..866 y108..522 fill F7E2CD;
title ink x260..745 y58..76 (20pt bold, highlight FBF29B x508..748 behind "(Fundamental
Operation)" only); subtitle ink x186..809 y79..101 (19.5pt bold, red 9E101E subscripted tokens,
red commas, verbatim unbalanced parens); label ellipses (F9FCDB, no border): Similarity
x266..341 y160..188, Probabilities x428..516 y161..192, Weighted SUM x568..693 y152..187 (text
offset right-of-center as measured); stacks x57..139 / x761..843 y226..395 (fill E6FCE7, dashed
3B7A40); glyphs = 5 cells (yellow FCFFC6 ×2, orchid D791C8 with red X label, lavender E6E2F8,
pale pink F3D3EC) — vision panel A read "yellow, yellow, X-cell, lavender, pink"; Dot Product
box x253..343 y194..404 DBCBBB, 2-line label 13pt 5C3712 pitch 15px, 4 dots d8 0200AB
staggered; Soft max bar x458..488 y196..401 F8DEFB with ONE-line 16.5pt 6B006E label rotated 270
(bottom-to-top); Σ box x516..649 y196..217 EAFEFC, Σ 20pt 2A2AB5; 4 flow rows y246/287/328/372
(line 4 measured to STOP at x~688 — reproduced), verticals into Σ with UP arrowheads at y219;
W₂₁–W₂₄ 10pt 0033CC at x495..510; nodes = red-ring circles d10 + 6-spoke asterisks + flanking
INWARD arrowheads on the line (tips at rim); Y box x547..617 y119..147 with 5-cell green vector
(B2DCA5/AFDAA6/96CE91/A0CC9A/A5C8BD) + dark-green "Y"; green 12B45A block arrow TILTED ~26°
up-right (tip (566,145)) + thin dark-red 8C0007 Σ→Y arrow at x583 drawn behind the Weighted-SUM
ellipse; strip x178..492 y473..517, X₂ highlight = 5-cell MAGENTA glyph (E39FBE/E0A5D3/C44C88/
D595E2/DC92E3) + sysDot A01450 border (pixel-verified: no yellow cells inside); query arrow
x298 y473..406; chunky red C5000F diagonal arrow (266,526)→(284,512); feed curves = thin dashed
AC9F90 with GREEN 1E7A34 up-arrowheads (vision panels E/F: "thin gray curved connector lines
ending in small green arrows"). Mouse cursor over X₂ in the original = video artifact, not
recreated (ground rule c). The spec's estimated colors (FBE5D6/C8B39C/DFA6DF/C5E0F5) were
superseded by frame-measured values per the fidelity law.

## Pre-judge checks (all banked in qa/slide026/)

- `house_chrome_check.py` on render_1.png: **PASS** (panel x89..1913, badge (1860,148) d70, tol 8).
- `selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt`: fills, box/ellipse/dot geometry
  (max deviation ≤1 frame-px on every box), title ink 259.2..744.5/57.7..75.9 (target 260..745 /
  58..76), subtitle 185.8..807.8 (target 186..809), highlight 508.5..746.1 (target 508..748),
  "Dot/Product" line pitch 14.9 (target 15, explicit lineSpacing 15), all lines/verticals/curves/
  arrowheads/labels present, containment clean (0 ink above the canvas zone). One reported FAIL
  line ("Ybox bbox") is a mask-tolerance artifact — cells 4/5 verified directly by median
  sampling (#A0CC9A / #A5C8BD exact).
- Equations: none printed on the slide (subscripts are native text runs — math-format rule not
  triggered); no tables; no multi-line delimiters.

## Dense-region crop comparisons (check 6, through the gate, default route)

- `crop_compare_1.txt` — 9 matched panels render-vs-original: **FAIL** with 3 real fix triggers:
  (C MAJOR) green arrow vertical instead of tilted up-right; (D/H MAJOR) X₂ highlight solid slab
  instead of internal cells; (B MINOR→fixed) nodes drawn as wide ellipses instead of small circles
  with flanking arrowheads. All three fixed in the build (rotate 26; 5-cell magenta glyph; circle
  + flanking heads).
- `crop_compare_2.txt` (re-check of the fixed regions): **PASS** — "FIX CONFIRMED" on all three;
  remaining MINORs: faint dotted outline on the Weighted-SUM ellipse in the original (cosmetic),
  X₂ cell-count nuance, cursor artifact correctly omitted.

## Judge (banked procedure executed by the worker)

- No Agent/Task spawn tool in this environment — per 17 §7 (orchestrator-approved fallback) the
  banked judge procedure was executed byte-for-byte via Bash: `judge_prompt_1.txt` banked before
  dispatch; build banked (`build_attempt_1.js`, `build_attempt_1_component.js`); probe (2 tries —
  both hard-walled at 150s, gateway saturated by parallel workers; window-open was already proven
  by the three successful gate calls this session) then the comparison at the W4 wide wall
  (`--thinking high --max-tokens 65536 --timeout 420` in `timeout 540`), default route, single-read.
- `judge_attempt_1.txt` — **FINAL VERDICT: PASS** ("faithful, usable recreation"). Findings: 3
  MINOR (multiplier glyph style reads ⊗ vs circled-asterisk at full-slide res — same
  position/size/topology; possible faint diagonal segments in the Dot Product box, medium
  confidence "may be compression artifact"; slight relative scale within tolerance). No
  MAJOR/BLOCKER. Frame containment, vertical centering, delimiter geometry all clean.
- Certificate label: single-read, default route (images), glm leg DEFERRED/BLOCKED.

## Attempts & DB

- Judge attempts used: 1 of 6 (plus 2 pre-judge crop-compare rounds that drove 3 build fixes).
- DB milestones: gen_status building → judging → **passed**; visual_check=PASS;
  visual_attempts=1; visual_transcript=qa/slide026/judge_attempt_1.txt; build_script + pptx_path set.
- Dependents 27/28/29 now show `unblocked` in `15_progress.py deps` (30 waits on 29 as designed).

## Evidence index

| File | What |
|---|---|
| qa/slide026/render_1.png | 150dpi render (attempt 1, post-fix) |
| qa/slide026/judge_prompt_1.txt | banked judge prompt (verbatim template + worker context) |
| qa/slide026/build_attempt_1.js, build_attempt_1_component.js | per-attempt build provenance |
| qa/slide026/judge_attempt_1.txt | judge comparison winner body (PASS) |
| qa/slide026/crop_compare_1.txt / crop_compare_2.txt | dense-region crop compares (FAIL→PASS) |
| qa/slide026/structure_probe.txt | 8-panel original-frame structure read |
| qa/slide026/selfcheck_attempt_1.py + _output.txt | closed-loop PIL self-check |
| qa/slide026/probe_judge_1.txt | judge probe (hung; non-evidentiary) |
| scratch/slide026/* | measurement scripts + composites (not evidence, provenance) |
