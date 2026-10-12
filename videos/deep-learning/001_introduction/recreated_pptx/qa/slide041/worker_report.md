# Worker report — slide 041 "The Convolution Process" (001_introduction)

Worker: per-slide build worker, dispatched 2026-10-12. Parent: certified slide 35
(edge `41 <- [35]`; deps gate verified UNBLOCKED before build — parent gen_status=passed,
visual_check=PASS in this video's DB).

## Deliverable

- `videos/deep-learning/001_introduction/recreated_pptx/slide_041_recreated.pptx`
  (single plain-named version; OMML dual-representation wrap applied post-certification,
  LO render verified 0 / 2,251,125 pixels differing vs the certified pre-wrap render).
- Build script: `recreated_pptx/build/slide_041.js` (pptxgenjs, LAYOUT_WIDE).

## Child composition (dependency law)

Parent component `recreated_pptx/build/components/slide_035.js` imported BY ABSOLUTE PATH;
`renderBase(pptx, slide, { numeral: "41", only: [] })` draws the playlist chrome only.
Measured diff of frame_041 vs frame_035 shows NONE of the parent's 9 content blocks
survive in slide 41's frame (different title text, panel rect 70..891 x 120..433 vs
379.5..885.5 x 168.5..431.5, different grids/labels/captions), so the child is the
chrome (via the certified parent) + its own full delta at PIL-measured geometry.
No slide depends on 41 (`slide_dependencies.json` edges: 16←9, 17←16, 18←9, 19←9,
25←24, 37←36, 41←35) — no component-banking obligation.

## Measurement provenance (all PIL, 960x540 px, 1px = 1pt)

Content panel red border x 70..891 / y 120..433, interior WHITE; title ink x 296..667 /
y 81..105 (Times New Roman Bold 35, C00000); labels Comic Sans MS 20 (deck precedent
slide_030); filter grid x 143..221 / y 319..381 native 3x3 table (FFFF00 fill, 8BD33F
borders — parent filterTable convention, Verdana Bold 14); notation lines Arial Bold 19.5
black + red math spans Times New Roman Bold 20 / TNR Bold Italic 19.5 (probe-calibrated:
Arial Bold punctuation rendered ~34% wider than the original's red math); instruction box
x 78..876 / y 445..511 (border 9797B2 — same as certified parent captionBox — fill white),
text Times New Roman 21 / 21.35 navy 1F3864, upright (stem/envelope slant test).

Baked crops (certified parent pattern — slide_035 banks leftgrid035.png +
panelcontent035.png the same way; pixel-verified in-render: mean |diff| 3.5–10.3,
resample-limited):
- `leftgrid041.png` — photo + 5x5 overlay (99,158)-(272,288); bottom cut at y=288 AFTER
  the attempt-1 judge flagged 2 rows of the 'Convolutional filter 1' label ascenders
  baked at the crop's bottom edge (fixed in attempt 2).
- `convgrid041.png` — 'Convolving the image' label + 5x5 convolving grid (381,131)-(637,357)
  (label and grid interleave rows 155–161 with the arrow; baked whole).
- `result041.png` — 'Result' label + curved arrow + tan-bordered result grid with olive
  '4' cell (548,131)-(863,286).
- `innerprod041.png` — 'Inner product' hand label + hand curly brace as a white-unblended
  transparent red-ink overlay (694,334)-(887,384); black equation glyphs in the same band
  are NOT baked (the equation is mathtext-rendered per the math law).

Equation (Math equation format rule): matplotlib mathtext -> 600 dpi transparent PNG via
`scripts/render_eq.py` at 19.5pt -> `build/assets/eq041.png` (3224x485 px, sidecar
`eq041.json`), embedded at exact size w=5.37333in at measured ink position (left 459,
top 364 @960). Mathtext: `I(x,y) \ast h = \sum_{i=-a}^{a} \;\; \sum_{j=-b}^{b}
I(x-i,\ y-j) \cdot h(i,j)`. The `\;\;` inter-sum space and `\cdot` operator were fixes
from the dense-region crop comparison (attempt 1 flagged limit-group collision and the
`\circ` glyph; spec verbatim_text allows "∘ or \cdot" and the vision read confirms the
original shows a centered dot; PIL: inter-limit-group gap 10.1px vs original 9px).
Closed-loop ink-bbox check: render (458.7..838.7, 364.6..420.2)@960 vs original
(459..841, 364..418) — all edges within ~2.5px@960 (≈4px@150dpi).

Deliberately NOT drawn (documented overrides):
- Bottom letterbox strip y 518..539 — video-player artifact; certified precedent
  slide_034/slide_017 (letterbox deliberately NOT recreated) + judge ground rule (c).
- The tall red line at x≈58 (y 45..516) — present in the parent frame 35 too: the
  original deck's own chrome border, overridden by the playlist house chrome (founder
  directive 2026-10-11; judge ground rule a2).
- 3x2px dark speck at (445..447, 80..81) on the title + cursor artifacts — video
  artifacts per ground rule (c).

## Self-checks (pre-judge, banked)

- `house_chrome_check.py`: PASS on every render (badge numeral "41", pending-veto note
  honored — numeral = file number, no zero-padding).
- `selfcheck_attempt_1.py` (21 checks, output in `selfcheck_attempt_1.out`): 21/21 PASS
  on the final render — panel borders, title, filter grid, equation ink bbox, brace ink,
  instruction box, both instruction lines, both notation lines, a=1/b=1 (+ pitch 14pt
  lineSpacing check), 3 bake-placement pixel diffs, containment vs chrome panel and vs
  content panel, no-letterbox check. (A units bug found by the first self-check run —
  `px(N)/72` double-division pushed all native text off-slide — was fixed and the check
  re-run to green before any judge dispatch.)
- Dense-region crop comparisons (mandated; `cropcmp_*.txt`, default route, --thinking
  high --max-tokens 65536): notation PASS; instructions PASS; filter_a1 PASS;
  eq_brace FAIL -> fixed (\;\; spacing + \cdot) -> attempt-3 PASS (only MINOR notes:
  cell-separator styling nuance on the baked crop, slightly wider inter-sum air — which
  matches the original's limit-group gap, typed-letterform style per ground rule (d)).

## Judge loop

| Attempt | Render | Verdict | Evidence |
|---|---|---|---|
| 1 | render_1.png (pre crop-recut) | PASS (3 MINOR: photo-crop label sliver at bake bottom; "scale" impression; "stray tick above v") | `judge_attempt_1.txt` |
| 2 | render_1.png (crop bottom recut to y=288) | **PASS** (3 cosmetic MINOR: brace span, baked-photo lightness, equation letterform — all covered by ground rules (d)/(e) or PIL bake evidence) | `judge_attempt_2.txt` |

Note on attempt 1's MINOR 1/3: PIL evidence overrides both — the baked crop's ink bbox
in the render is (100.3..271.1, 157.9..289.3)@960 vs the original photo's (101..269,
158..287) — geometry exact; and the region above the title caps in the recreation is
provably empty (no ink at y<168@render in the title x-range), so no "stray tick" exists.
The judge procedure was executed by the worker (no Agent/Task spawn tool available in
this environment) — orchestrator-approved fallback per scripts/17_worker_instructions.md
§7; verdicts taken verbatim from real `[winner]` comparison bodies (default route,
single-read, glm leg DEFERRED/BLOCKED).

## Post-certification OMML dual-representation wrap

`scripts/18_omml_wrapper.py` v2 applied to the deliverable with
`eq_041_omml_manifest.json` (image-matched rel rId5; mathtext; 19.5pt; #000000).
Verification: LO render of the wrapped pptx vs the certified pre-wrap render =
**0 of 2,251,125 pixels differ**. Pre-wrap bytes banked at
`qa/slide041/slide_041_recreated_prewrap.pptx`. Never LO-resave the wrapped deck.

## DB final state

gen_status=passed, visual_check=PASS, visual_attempts=2,
visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide041/judge_attempt_2.txt,
pptx_path + build_script set. Milestones written at building/judging/passed.

## Evidence index (qa/slide041/)

- `render_1.png` (final 150dpi render), `judge_prompt_1.txt` / `judge_prompt_2.txt` /
  `judge_prompt_1_body.txt` (banked frozen judge prompts), `build_attempt_1.js` /
  `build_attempt_2.js` (per-attempt build provenance), `judge_attempt_1.txt` /
  `judge_attempt_2.txt` (judge comparison transcripts), `probe_1.txt` (probe attempts —
  two short-wall hangs recorded, then wide-wall dispatches per W4).
- `cropcmp_eq_brace.txt` (FAIL, attempt 1), `cropcmp_eq_brace_2.txt` (FAIL — stale crop
  discovered: the refresh had written to qa/ while the dispatch read the scratch copy;
  re-cut and re-dispatched), `cropcmp_eq_brace_3.txt` (PASS), `cropcmp_notation.txt`,
  `cropcmp_instructions.txt`, `cropcmp_filter_a1.txt` (PASS).
- `selfcheck_attempt_1.py` + `.out`, `eq_041_omml_manifest.json`,
  `slide_041_recreated_prewrap.pptx`.
- Assets: `build/assets/{leftgrid,convgrid,result,innerprod,eq}041.png` + `eq041.json`.

---

## ADDENDUM — parallel duplicate dispatch (second builder), independent verification

A SECOND builder was dispatched for slide 041 and ran in parallel with the primary worker
above (its draft work: assets stamped 11:03–11:26 under `build/assets/`, continued
11:37–11:47). Conflict was detected at 11:44 when the primary worker's pptx/render landed;
the second builder immediately STOPPED writing to the slide-041 lineage (its own draft
build-script write failed harmlessly before touching anything) and switched to a read-only
watch, resuming nothing because the primary worker stayed alive through certification.
Resolution: the primary worker's lineage above is the certified one; no evidence was
deleted or overwritten by either side.

Superseded artifacts of the second builder, PRESERVED UNMODIFIED as banked evidence
(never referenced by the certified build):
- `build/assets/eq_041.png` (+ sidecar), `photo041.png`, `arrow_041.png`, `brace_041.png`
- `qa/slide041/gen_strokes_041.py` (its own arrow/brace tracing notes)

### Independent verification by the second builder (read-only, on the certified artifact)

- `house_chrome_check.py` on `render_1.png`: **PASS** (badge center (1860,148) d70 @150dpi
  = (893,71) d36 frame-scale, within tol 8).
- Equation region ink present (5,910 px); badge fill present; deliverable pptx = OMML-wrapped
  single-version (prewrap banked), DB row complete: gen_status=passed, visual_check=PASS,
  visual_attempts=2, transcript=judge_attempt_2.txt, pptx_path + build_script set.
- Independent PIL re-measurements that CORROBORATE the certified build: title Times New
  Roman Bold 35 C00000 (correlation-fitted, center 482.5); content panel x71..890 y120..433;
  photo-crop position (99,158); filter grid x143..222 y319..382; equation ink bbox
  x459..842 y363..419; instruction box x79..877 y444..512; swoosh/brace/label entanglement
  → bake (same precedent); letterbox + x58 template line + title pen-speck NOT drawn.
- Banking: skipped per dispatch (41 has no dependents; `slide_dependencies.json` edges
  confirmed). No component banked — consistent.

### Residual pixel-law deviation (banked for founder disposition; certification stands)

The second builder's independent pixel measurement of the frame contradicts the certified
render's notation color layout on two spans (small-text color is a known vision-judge blind
spot; both full-slide judges and the notation crop judge passed these):

- `(-a:a , -b:b)` (frame x183..276, y413..429): original-frame pixels are BLACK (modal
  (0,0,0), n=370; ZERO red pixels anywhere in x175..309 of that band). The certified
  render draws the whole `h (-a:a , -b:b)` span in solid C00000 (render region x183..276:
  1,340 pure-red px, 0 dark px). The spec's recreation_brief step 13 also claimed red —
  the frame's own pixels say otherwise (deck law: ink wins).
- `I (x,y)` (frame x165..212, y386..406): original shows a red `I` stem (x165..167) and
  BLACK `(x,y)` (x177..212, modal (0,0,0) n=184); the render draws both red.

Disposition: the visual judge is the binding acceptance gate (verdict law) and passed the
slide twice; this note banks the pixel evidence so the founder can order a targeted
rebuild of the two notation spans (re-derive `eq_041_omml_manifest.json` after any rebuild,
per the OMML contract) without re-deriving the analysis.

### Other measurement deltas (all judge-accepted, recorded for provenance)

- Labels: certified build uses Comic Sans MS 20 (certified deck precedent slide_030/048);
  the second builder's glyph-correlation favored Verdana Bold 21-22. Both plausible; judge
  accepted the certified choice.
- Filter border: certified 8BD33F (parent filterTable convention) vs measured core
  #B2D24A on this frame. Instruction box border: certified 9797B2 (parent captionBox
  convention) vs measured #AFABCC. a=1/b=1: certified Arial Bold 14 / pitch 14pt vs
  measured regular 13 / 16px pitch. Instruction navy: certified 1F3864 (spec) vs measured
  core #191157. All within judge tolerance; noted here for completeness.

---

## ADDENDUM 2 — targeted frame-is-truth fix of the two notation spans (attempt 3, 2026-10-12)

The residual pixel-law deviation banked above ("Residual pixel-law deviation") was ordered
fixed. Prior certified evidence preserved copy-then-modify; nothing in qa/slide041/ was
deleted or overwritten (new files carry attempt-3 names).

### Independent PIL re-verification (before touching anything)

`pil_verify_addendum.py` + `.out` (banked here): the addendum REPRODUCES. Frame
`unique_slides/slide_041.jpg`: `(-a:a , -b:b)` x183..276 y413..429 = 315 dark px, modal
(0,0,0), ZERO red; `(x,y)` x177..212 y386..406 = 151 dark px, modal (0,1,0)-black, zero
red; `I` stem x165..167 and `h` x165..174 RED (controls: `a=1,b=1` red 64/0 dark;
equation black 706/0 red — method sanity confirmed). Certified render drew both spans
solid C00000 (L1 region 522 red / 0 dark; L2 region 1285 red / 0 dark). One refinement
over the banked addendum: the 10 faint red px it noted near x290..305 are antialiasing of
the RED `(odd dimension)` span, not part of the fixed spans; and `h` is RED in the frame,
so it stayed red.

### Fix (build/slide_041.js — now banked as build_attempt_3.js)

The two spans are native text runs. Only change: run splits + color of the two spans.
- L1: `"I (x,y)"` (all red TNR 18.5) -> `"I "` red TNR 18.5 + `"(x,y)"` BLACK (#000000) TNR 18.5.
- L2: `"h (-a:a , -b:b)"` (all red TNR 20.5) -> `"h "` red TNR 20.5 + `"(-a:a , -b:b)"` BLACK TNR 20.5.
Every other byte of the composition (chrome, panel, title, grids, bakes, equation embed,
instruction box, fonts, sizes, positions, remaining run colors) identical. Header comments
updated with the frame-is-truth basis.

### Closed-loop verification (all banked)

- Rebuild -> LO render 150dpi -> `qa/slide041/render_3.png` (2001x1125).
- `closedloop_attempt_3.py` + `.out`: PASS — 2,931 diff px vs certified `render_1.png`, ALL
  inside the two span allow-boxes, 0 outside; 12 guard zones (Image:/Filter: prefixes, I
  stem, h, (odd dimension), a=1/b=1, equation region, instruction box, filter grid, title,
  rows above/below spans) all 0 diff; both spans now modal (0,0,0) zero red (L1 568 dark,
  L2 1547 dark); I/h/(odd dimension) red ink preserved (143/258/1142 red px); span glyph
  positions unchanged (L1 dev 0.00 frame px, L2 max dev 0.48 frame px — subpixel antialias
  only, from the run-boundary reshaping).
- `house_chrome_check.py render_3.png 41`: PASS (badge (1860,148) d70, panel 89..1913).
- `selfcheck_attempt_3.py` (the banked 21-check suite, render path pointed at render_3):
  21/21 PASS (`.out` banked).

### OMML dual-representation wrap re-applied (rebuild had regenerated the pptx unwrapped)

`scripts/18_omml_wrapper.py` v2 re-run on the rebuilt pptx with the SAME banked manifest
`eq_041_omml_manifest.json` (image-basename matching re-derived rId5 from the CURRENT pptx;
mathtext, 19.5pt, #000000). 0-px verify: LO render of the wrapped deck vs `render_3.png` =
**0 of 2,251,125 pixels differ**. New pre-wrap bytes banked at
`slide_041_recreated_prewrap_attempt3.pptx`; the wrapped file promoted to the single
plain-named deliverable `slide_041_recreated.pptx`. Prior certified (attempt-2, wrapped)
bytes banked at `slide_041_recreated_certified_attempt2.pptx`. Never LO-resave the
wrapped deck.

### Judge attempt 3 (verdict law: binding acceptance gate)

Frozen template + GROUND RULES prelude with the mandated measured-facts clause (g) banked
at `judge_prompt_3_body.txt` / `judge_prompt_3.txt`; probe `probe_3.txt` landed clean;
comparison (default route, --thinking high, --max-tokens 65536, W4 wall 540/420, single
read, glm leg DEFERRED/BLOCKED) banked at `judge_attempt_3.txt`. Ground rule (g) settled
first ("correct in the recreation, not flagged"); zero BLOCKER/MAJOR; 4 cosmetic MINORs
(brace geometry, subscript color nuance, title metrics, thumbnail crispness). 
**FINAL VERDICT: PASS** for 'faithful, usable recreation'.

### DB final state (after this fix)

gen_status=passed, visual_check=PASS, visual_attempts=3,
visual_transcript=videos/deep-learning/001_introduction/recreated_pptx/qa/slide041/judge_attempt_3.txt,
pptx_path + build_script unchanged.
