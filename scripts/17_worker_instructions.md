# Slide-recreation worker instructions (per-slide, executed by a worker subagent)

You own ONE slide end-to-end: build the PPTX recreation from the validated analysis JSON,
render it, run the visual QA loop with a judge subagent, and update the progress DB. Work
autonomously — never ask questions; if blocked, record `last_error` in the DB and report.

Throughout, substitute your slide id for `N` and its zero-padded form for `NNN`
(e.g. N=7, NNN=007). Project root: `/home/ahmed/Projects/ai_llm_slides`.
**Multi-video layout:** all data lives under `videos/<VIDEO>/` (your dispatch tells you
the video; currently `ml-intro`). Your paths are therefore
`videos/<VIDEO>/unique_slides/slide_NNN.jpg` (original), `videos/<VIDEO>/analysis/` (spec),
`videos/<VIDEO>/recreated_pptx/` (build + qa + pptx). Run progress-DB commands with
`VIDEO=<VIDEO>` set, e.g. `VIDEO=ml-intro python3 scripts/15_progress.py set N field value`.

## HARD STOP: human review of unique frames (founder directive 2026-10-10 — non-negotiable)

For EVERY new video, after frame extraction + phash dedup produce
`videos/<VIDEO>/unique_slides/`, the pipeline HARD-STOPS: a HUMAN must review the
extracted unique frames and approve the set before ANY downstream processing begins —
no script-12 analysis, no script-13 validation, no DB registration as ready, no build
or subagent dispatch on those frames. The machine may prepare a review packet (index,
contact sheet, new2old mapping draft) but must NEVER approve the set itself. Curation
(duplicates, non-valid frames, numbering/badges) is human-owned. If you are dispatched
for extraction, deliver the packet, report that the pipeline is stopped at the human
review gate, and stop.

## Authoritative content spec

`videos/<VIDEO>/analysis/slide_NNN_final.json` — contains `slide_title`, `verbatim_text`, `layout`,
`visual_elements`, `imagery`, `colors`, `typography_notes`, `recreation_brief`, and a
`validation` block. Rules:

- Text is VERBATIM — no paraphrasing, no fixing typos.
- Keep `[?]` markers on uncertain content; NEVER invent facts, numbers, labels, or colors
  not in the spec.
- Apply `validation.fixes` where present.
- Fidelity to the original lecture slide is the goal; do NOT "modernize" the design.
  Reproduce layout, colors, and structure as described.

## House frame rule (founder directive 2026-10-09 — overrides spec AND judge)

Every slide MUST use slide 3's house template for the shared outer chrome. These values
override the spec JSON and any judge finding about these elements — the judge may NOT
veto them, and a judge discrepancy about frame/badge/title-y is NOT a fix trigger:

- Slide: LAYOUT_WIDE 13.33 × 7.5 in, background `E8E8E8`.
- Outer red frame: rectangle `x: 0.15, y: 0.15, w: 13.03, h: 7.2` (0.15 in inset from
  every edge), line `C00000` width 1.5, no visible fill (gray, i.e. `E8E8E8`).
- Slide-number badge: oval `x: 12.48, y: 0.30, w: 0.5, h: 0.5`, fill `FFF9C4`,
  line `FFF9C4` width 0.5; the numeral is the NUMBER PRINTED ON THE ORIGINAL SLIDE
  IMAGE (founder directive, deck curation 2026-10-09). The deck is 64 slides and
  `videos/<VIDEO>/unique_slides/slide_NNN.jpg` is named BY that printed number, so slide N's badge
  reads exactly `N` (no zero-padding). A recreation whose badge does not match the
  original image's number is WRONG. Bold 18pt, color `333333`.
- Slide title: text box starts `y: 0.28`, `x: 0.6, w: 12.13`, `align: "center"`.
- If the spec's frame/badge/title geometry differs, use the house values anyway.

## Math equation format rule (founder directive 2026-10-09 — binding on every build)

If your slide contains ANY equation (distance formulas, sums, squared terms, indexed
variables, etc.), it MUST be rendered in **Professional Format (2D / non-linear visual
representation)** — never Linear Format (plain-text math notation):

- **Fractions**: stacked with a horizontal fraction bar (numerator above bar, denominator
  below) — never inline `a/b` or `a over b` as text.
- **Summation (`∑`)**: a large summation glyph with limits above/below it (or stacked to
  its right, matching how the ORIGINAL slide shows them) — never inline `sum from i=1 to n`.
- **Subscripts & superscripts**: spatially aligned with proper math-font spacing and
  proportions — never caret/underscore text (`x^2`, `x_1`) and never Unicode look-alike
  approximations of stacked constructs.

The equation's CONTENT stays verbatim from the spec; only its rendering is professional.
**The approved, vision-certified mechanism (2026-10-09, PASS on first comparison):
matplotlib mathtext → tight transparent PNG at 600 dpi → `pptxgenjs.addImage()`.**
Hand-authoring OMML/Office-Math *for rendering* is FORBIDDEN — LibreOffice headless renders
only its linear fallback (measured; see `qa/math/research_report.md`).

**Dual-representation post-pass (validated 2026-10-10; wrapper v2 + single-version naming):**
once a slide's PNG-based build is visually certified, `scripts/18_omml_wrapper.py
<slide.pptx> <manifest.json>` upgrades the SAME pptx (the single plain-named deliverable,
see the SINGLE-VERSION law below) so PowerPoint shows editable native equations (OMML in
`mc:Choice Requires="a14"` in the **PowerPoint-authored pattern** — v2: `m:oMathPara`,
Cambria Math runs, `m:ctrlPr` everywhere, Choice shape id = Fallback pic id; v1's
LibreOffice-writer pattern rendered NOTHING in PowerPoint, measured) while LibreOffice
keeps rendering the certified PNG (`mc:Fallback` = original pic verbatim — LO render is
pixel-identical, measured 0/2,251,225 px). Manifest values come straight from the
`eq_*.json` sidecars (`rel_id, image, mathtext, font_size_pt, color`), RE-DERIVED from the
current pptx after any rebuild (never assume rel ids survive a rebuild); validated v2
example + report in `qa/omml_v2/`. Apply AFTER certification only; never LO-resave a
wrapped deck (the LO writer drops OMML it never understood). This pass does not change
pixels and does NOT need a re-judge.

**SINGLE-VERSION LAW (founder directive 2026-10-10 — binding on every build):** the
deliverable is ONE pptx per slide, named `slide_NNN_recreated.pptx` — NO `_graphed` or
`_omml` suffixes, ever. If the slide's original contains advanced graphs, the generated
graph image is embedded IN this same pptx; if it contains equations, the OMML wrap is
applied to this same pptx post-certification. Superseded/intermediate builds live only
in QA evidence dirs, never as parallel deliverables.

Usage contract (validated in `videos/ml-intro/recreated_pptx/qa/math/` — read
`scratch_validation_report.md` and use `render_eq.py` + `scratch_build.js` as the pattern):
1. Generate per equation: `python3 scripts/render_eq.py '<mathtext>' <out.png> <fontsize_pt> '<hex>'` — 600 dpi, tight bbox, transparent bg; it prints a JSON sidecar with exact pixel width/height and baseline fraction. Store generated PNGs under `recreated_pptx/build/assets/` (or qa), never delete them.
2. Embed at EXACT size: `w = px/600` inches (and `h = py/600`) — NEVER rescale the image
   (blurs the math glyphs); font size and color are baked at render time.
3. Inline alignment: place with `y: lineY - h_in/2` centered on the text-line center
   (validated: ≤1.5px off at 150 dpi); use the sidecar's baseline fraction for tighter
   alignment when needed.
4. PNG only — never SVG (LibreOffice rasterizes SVG unpredictably). Watch the pitfalls
   list in `research_report.md` (mathtext subset of LaTeX; DejaVu math font look —
   acceptable per the scratch vision validation; private soffice profile for renders).
5. **EQUATION ALIGNMENT LAW (founder feedback 2026-10-10 — binding; visual position
   defects are fix triggers even when a judge PASSed):**
   - **Vertical**: the equation image's math BASELINE must sit on the same baseline as
     the text it belongs with. Compute from the sidecar's `baseline_frac`:
     `y_image = target_baseline_in − baseline_frac × h_image_in`. "Center the image on
     the line" (`lineY − h/2`) is WRONG for any equation taller than the line.
   - **Horizontal**: position against the ORIGINAL frame's measured ink position, not
     by intuition — PIL-measure the equation region in the original (960×540 px,
     1px = 1pt), including the ink's left edge, and match it.
   - **Closed-loop verification (mandatory before judging)**: render, then PIL-compare
     the equation's ink band in the 150dpi render against the original frame's measured
     region (scale ×2000/960): the equation's top/bottom/left/right ink edges must match
     within ~4 px (150dpi space). Iterate placement until within tolerance. A judge
     PASS does not waive this check.

## MANDATORY PRE-JUDGE SELF-CHECK (founder directive 2026-10-10 — every recreation, no exceptions)

Before ANY judge dispatch, run ALL of these on your 150 dpi render (2001x1125; 1 px @150dpi = 1/200 in). A judge PASS does NOT waive any of them — founder feedback overrides judge PASS. If any check fails, fix and re-render before judging. Bank each check's numbers in your QA dir (`selfcheck_attempt_K.py` + printed output).

1. **REUSABLE PATTERNS**: read `.agents/skills/slide-recreation/references/patterns.md` FIRST and use its confirmed-working patterns (house chrome, inner-frame budget, delimiters, equations, highlight boxes, data tables). If your slide hits a situation a pattern already solves, use the pattern — do not improvise a variant. When your fix produces a NEW confirmed-working pattern, append it to that file.
2. **FRAME CONTAINMENT (PIL)**: for every inner frame/panel on the slide, PIL-measure the ink bbox of the content assigned to it and assert the ink sits fully inside the frame edges (no ink on or beyond the boundary). Include the house frame: content ink must not cross x<0.15in / x>13.18in / y<0.15in / y>7.35in equivalents at 150 dpi.
3. **EQUATIONS EXIST**: if the original has equations, assert the equation regions in YOUR render contain ink (nonzero ink pixels in the measured region). An empty equation box is a BLOCKER — never judge with one.
4. **DELIMITER GEOMETRY**: for every multi-line parenthesized/bracketed block, PIL-measure the delimiter strokes' vertical extent vs the enclosed text lines' extent (must cover ALL lines, topmost to bottommost) and the horizontal clearance between delimiter stroke and enclosed text (strokes must not sit on text).
5. **TABLE DATA**: if the slide shows a table of a known dataset (e.g. IRIS), every cell value must come from the canonical dataset file (see patterns.md §data) — same file for all slides; count rows/columns vs the original.
6. **ZOOMED CROP VISION ANALYSIS (images model, through the gate)**: for every dense/small region (equations, delimiters, table cells, tight gaps), crop BOTH the render and the original to that region (upscale ×2 if the region is < ~400px), save as separate images, and run an `analyze_image.py comparison <render_crop> <original_crop>` on the cropped pair with the SAME judge template. Dense-region defects are invisible at full-slide resolution — the full-slide judge is NOT sufficient for these regions; the crop comparison is mandatory when the slide has equations, multi-line delimiters, or tables.
7. **LINE/BOX WRAP CHECK**: for every text box near a delimiter or frame edge, PIL-assert no ink appears OUTSIDE the expected band (text boxes wrap at BOX width, not ink width — widen boxes ~20% beyond the longest line's advance and assert no ink below/above the intended band).
8. **EXPLICIT LINE SPACING (PowerPoint-vs-LO divergence — founder evidence slide 5)**: LO's auto line pitch is SHORTER than PowerPoint's for the same font size (~15% cumulative over a 14-line block — enough to push the last line outside a frame that LO-verifies as fitting). EVERY multi-line text box MUST set explicit `lineSpacing: <pt>` (pptxgenjs, exact points) — measure the pitch from the LO render or the original's line gaps and pin it; with explicit spacing PowerPoint and LO render the same pitch, so the LO containment check PREDICTS PowerPoint. Never rely on auto line pitch for blocks near frame bounds. After setting it, re-measure the render's band pitch and assert it equals the pinned value.

## Progress DB — update at every milestone

```
python3 scripts/15_progress.py set N <field> <value>
```

Whitelisted fields you will use: `gen_status`, `pptx_path`, `build_script`, `visual_check`,
`visual_attempts`, `visual_transcript`, `last_error`.
Milestones: `gen_status=building` (start) → `judging` (each judge dispatch) →
`passed`/`failed` (end); set `pptx_path`/`build_script` once built; update
`visual_check`/`visual_attempts`/`visual_transcript`/`last_error` as they change.

## Build (attempt 1)

1. Read the spec JSON fully. Read `scripts/14_build_slide_007_pptx.js` as the working
   pptxgenjs pattern example.
2. Write `videos/<VIDEO>/recreated_pptx/build/slide_NNN.js` (mkdir -p `recreated_pptx/build` first) using
   pptxgenjs:
   - Run with: `cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node videos/<VIDEO>/recreated_pptx/build/slide_NNN.js`
   - `const pptxgen = require("pptxgenjs"); pres.layout = "LAYOUT_WIDE"` (13.33 × 7.5 in).
   - NEVER prefix hex colors with `#` (corrupts the file); never 8-char hex; use the
     `transparency` property, not alpha hex.
   - Set `fontFace` explicitly on every text element (Arial unless the spec says
     otherwise); set `margin: 0` on text boxes that must align with shapes.
   - Multi-line text: array items with `breakLine: true`.
   - Where the spec has data charts use native `addChart` (data values verbatim from the
     spec); tables via `addTable`; diagrams via shapes + connectors; arrows via connector
     shapes with `line.endArrowType`.
   - Output: `videos/<VIDEO>/recreated_pptx/slide_NNN_recreated.pptx`
3. DB: `gen_status=building`, `build_script=videos/<VIDEO>/recreated_pptx/build/slide_NNN.js`,
   `pptx_path=<actual>`.

## Render

4. In a private scratch dir (`mktemp -d`), with your OWN LibreOffice profile (workers run
   in parallel — the default profile allows only one instance):
   ```
   soffice --headless -env:UserInstallation=file:///tmp/lo_slideNNN --convert-to pdf --outdir <scratch> videos/<VIDEO>/recreated_pptx/slide_NNN_recreated.pptx
   pdftoppm -png -r 150 <scratch>/slide_NNN_recreated.pdf <scratch>/slide
   mkdir -p videos/<VIDEO>/recreated_pptx/qa/slideNNN
   cp <scratch>/slide-1.png videos/<VIDEO>/recreated_pptx/qa/slideNNN/render_K.png     # K = attempt number
   ```

## Self-check (corroboration only — NEVER a substitute for the visual check)

5. PIL-sample the rendered PNG at expected title/box/background regions and compare to the
   spec colors. Fix obvious misses before spending a vision call.

## Judge (one per attempt)

6. BEFORE spawning, bank the exact substituted judge prompt (the block below with your
   NNN/K values filled in) to `videos/<VIDEO>/recreated_pptx/qa/slideNNN/judge_prompt_K.txt`, and bank this
   attempt's build script verbatim: `cp videos/<VIDEO>/recreated_pptx/build/slide_NNN.js
   videos/<VIDEO>/recreated_pptx/qa/slideNNN/build_attempt_K.js` (per-attempt provenance — the live script
   gets overwritten on fixes).
7. Spawn ONE `presentations:visual-judge` subagent with `run_in_background: true`, with
   EXACTLY the prompt you banked (substitute `K` = attempt number). If your toolset has no
   Agent/Task tool (observed in this environment), do NOT stall: execute the banked judge
   procedure yourself via Bash, byte-for-byte per the prompt (probe + comparison through
   `scripts/16_vision_gate.sh`, transcripts banked as instructed), and take the verdict
   verbatim from the vision model's comparison winner body — your own reading of the PNG is
   never evidence (you cannot see images). This fallback is ORCHESTRATOR-APPROVED; note it
   in your final report ("judge procedure executed by worker; no spawn tool available").

```
You are the visual acceptance gate for slide NNN of /home/ahmed/Projects/ai_llm_slides.
The session model cannot see images; ALL vision analysis must go through the image-analysis
skill's script. First read /home/ahmed/Projects/ai_llm_slides/.agents/image-analysis/SKILL.md
and follow its routing and dispatch law.
- Render being judged (attempt K): /home/ahmed/Projects/ai_llm_slides/videos/<VIDEO>/recreated_pptx/qa/slideNNN/render_K.png
- Original frame (ground truth): /home/ahmed/Projects/ai_llm_slides/videos/<VIDEO>/unique_slides/slide_NNN.jpg
- Content spec: /home/ahmed/Projects/ai_llm_slides/videos/<VIDEO>/analysis/slide_NNN_final.json

Method (mandatory, in order):
1. Probe the gateway window (NO --models flag — the default route IS the images model):
   cd /home/ahmed/Projects/ai_llm_slides && scripts/16_vision_gate.sh timeout 150 python3 \
     .agents/image-analysis/scripts/analyze_image.py analysis \
     videos/<VIDEO>/recreated_pptx/qa/slideNNN/render_K.png \
     --view "Slide NNN recreation attempt K — probe" \
     --capture "150dpi PNG render of a 13.33x7.5in PPTX" \
     --timeout 120 --rounds 1 --tries 1 \
     --transcript videos/<VIDEO>/recreated_pptx/qa/slideNNN/probe_K.txt
   A valid body opens the window; a hang means sleep 300 and re-probe ONCE.
2. Comparison (gate wraps timeout, so queue wait never burns the wall).
   MANDATORY judge parameters (user directive 2026-10-09): `--thinking high`
   (maximum reasoning effort) and `--max-tokens 65536`.
   MEASURED FACT (slide-008 worker, 2026-10-09): with `--thinking high`, the
   comparison RELIABLY exceeds the 240s wall — use the W4 wide wall from the
   start, do NOT start at 240s:
   cd /home/ahmed/Projects/ai_llm_slides && scripts/16_vision_gate.sh timeout 540 python3 \
     .agents/image-analysis/scripts/analyze_image.py comparison \
     videos/<VIDEO>/recreated_pptx/qa/slideNNN/render_K.png videos/<VIDEO>/unique_slides/slide_NNN.jpg \
     --view "Slide NNN recreation — fidelity check vs original lecture frame" \
     --capture "IMG1=150dpi PNG render of a 13.33x7.5in PPTX; IMG2=original lecture video frame" \
     --thinking high --max-tokens 65536 \
     --timeout 420 --rounds 1 --tries 1 \
     --transcript videos/<VIDEO>/recreated_pptx/qa/slideNNN/judge_attempt_K.txt \
     -p "GROUND RULES (founder-mandated, settle these FIRST and never raise them as discrepancies): (a) The recreation uses a house template — outer red frame x:0.15 y:0.15 w:13.03 h:7.2 line #C00000 1.5pt over #E8E8E8 bg, yellow slide-number badge oval x:12.48 y:0.30 w:0.5 h:0.5 fill #FFF9C4, title box y:0.28 x:0.6 w:12.13 centered. These are INTENTIONAL house chrome and are NOT discrepancies. (b) If image 2 (the original) is a contentless placeholder/Processing slide, then matching contentlessness IS a match — do not demand content the original does not have. (c) Any mouse cursor / video-capture artifact visible in image 2 is a video artifact and is CORRECTLY omitted from the recreation. (d) Typed-vs-handwritten ink is an inherent medium difference — at most MINOR. (e) Equations in the recreation are rendered in PROFESSIONAL 2D FORMAT (stacked fractions with a horizontal bar, large ∑ with limits above/below, spatially aligned sub/superscripts) per founder directive 2026-10-09 — if image 2 (the original) shows the same equation in LINEAR/typed notation, that difference is a mandated format upgrade and is NOT a discrepancy. (f) Your verdict is about fidelity of renderable content ONLY. Image 1 is a PowerPoint recreation; image 2 is the original lecture slide. Compare them element by element for fidelity: title and all text (verbatim, line breaks), layout/regions, table contents and structure, chart types and data values, diagram shapes/arrows, colors (approx hex), imagery. Be PRECISE about text metrics and geometry — measure with your eyes, not vibes: (1) line height / line separation inside multi-line text blocks (e.g. a two-line value listed under a '(weight (kg), length (cm))' header must have the same inter-line spacing as the original); (2) vertical centering of enclosed content — text inside brackets, parentheses, or cells must sit vertically CENTERED within the delimiters, not hugging the top while the delimiter's lower section wraps empty space; (3) sizes, gaps and ordering of legend items (e.g. 'red class / blue class / green class') must match the original's sizes and gaps; (4) horizontal AND vertical alignment of every label against its value, every value against its enclosing marks, and every region against the original. (5) FRAME CONTAINMENT — every content element (text, box, table, graph, image) must sit fully INSIDE its enclosing frame/panel: any ink that crosses or touches the boundary of the inner frame it belongs to (top/bottom/left/right), or of the house frame, is an overflow and a MAJOR defect; scrutinize the items closest to every frame edge. (6) MISSING ELEMENTS — if the original shows an equation, graph, image, table row, or any visual element that the recreation omits ENTIRELY (absent, not just styled differently), that is a BLOCKER defect; an equation region that renders empty is a BLOCKER even if everything else matches. (7) DELIMITER GEOMETRY — parentheses/brackets/braces that span multiple lines in the original must (i) span ALL the lines they enclose (topmost to bottommost), (ii) be wide enough that their strokes do not sit ON or overlap the enclosed text, (iii) match the original's curvature/shape style; a delimiter covering only some of its lines, drawn over the text between it, clipped, or invisible is a MAJOR defect. (8) TABLE DATA — every table cell value must match the original exactly (or the real dataset the original displays, when it is a known dataset such as IRIS); missing rows, truncated tables, or wrong values are MAJOR-to-BLOCKER. A visible deviation in line spacing, vertical centering, gap, size, alignment, frame containment, delimiter geometry, or table data vs the original is a MAJOR defect even when all text is verbatim (founder directives 2026-10-10). List EVERY discrepancy with severity (BLOCKER/MAJOR/MINOR) and confidence, then any visual-quality defects in the recreation (text overflow/clipping, wrong wrapping, misalignment, collisions, illegibility). End with: FINAL VERDICT: PASS or FAIL for 'faithful, usable recreation'."
   On a hard-wall HangError, retry ONCE at the same wide wall (skill amendment W4).
   Never wrap analyze_image.py in any other retry loop.
2b. DEGENERATE GARBBAGE RETRY (user directive): if the comparison call aborts with
   GarbageError, or the winner body you read is degenerate garbage (word salad,
   looping repetition, no coherent FINAL VERDICT line), the check has NO evidentiary
   value — re-invoke the comparison (same parameters, new attempt count) up to 3
   garbage retries before treating it as a failed judge attempt. NEVER certify a
   pass from a degenerate body; a degenerate body is a FAIL and must be retried.
3. Read the banked transcript (never Read PNG bytes with the Read tool). The verdict must
   come from a real comparison winner body — a check without vision evidence is a FAILURE
   by law; if the comparison never lands, your verdict is fail with issue "no vision evidence".
4. Standard: fidelity recreation of a plain lecture slide — do not penalize the plain/retro
   look. Mouse cursors or video-capture artifacts in the original must NOT be recreated;
   don't flag their absence. Label the certificate: single-read, default route (images),
   glm leg DEFERRED/BLOCKED.

FINAL MESSAGE (mandatory): line 1 exactly:
{"page": 1, "verdict": "pass"|"fail", "issues": ["..."]}
then a short evidence section (transcript paths, findings). You are read-only: fix nothing.
```

7. Wait for the judge with TaskOutput (block=true, timeout=600000; if it returns
   "running", call TaskOutput again). Parse the JSON verdict line.

## Verdict law (from the user, non-negotiable)

- A slide is done ONLY with a real visual-judge PASS. A failed visual judge is
  BLOCKING — there is NO success criteria without the visual judge at all:
  programmatic checks, probes, pixel sampling, or any non-comparison evidence can
  never mark a slide done.
- `pass` AND backed by a comparison transcript → DB: `visual_check=PASS`,
  `visual_transcript=<comparison transcript path>`, `gen_status=passed`. DONE.
- `fail`, no vision evidence, or degenerate garbage → DB: `visual_check=FAIL`,
  `visual_attempts=K`, `gen_status=building`; apply the judge's issues to the
  build script, re-render as `render_{K+1}.png`, judge again. Up to 6 attempts
  total. After 6 failures: `gen_status=failed`, `last_error=<summary of
  remaining issues>`, and STOP (the orchestrator will re-dispatch you — a failed
  row is never silently dropped).

## Resume rule (if a previous worker ran on this slide)

If the DB row or `videos/<VIDEO>/recreated_pptx/qa/slideNNN/` shows progress from a previous
(e.g. crashed) worker: reuse the existing build script and renders where valid,
continue attempt numbering from the highest existing `render_K`/`judge_attempt_K`,
and NEVER delete banked evidence (transcripts, prompt copies, build copies).
State in your report that you resumed and from which attempt.

## Final message

Write your full final report to `videos/<VIDEO>/recreated_pptx/qa/slideNNN/worker_report.md` (attempts used,
per-attempt verdicts and judge issues, final verdict, pptx path, transcript paths) BEFORE
ending, then ALSO summarize in your final message: slide id, attempts used, final verdict,
pptx path, comparison transcript path, one-line summary of what the judge flagged (if any).
If you could not spawn the judge subagent, say NEEDS_JUDGE and explain.
