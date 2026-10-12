# Worker report — slide 011 (002_transformers_part2) — attempt 1

Slide: N=11, NNN=011 — "Multi Head Self Attention of Word X₂" (five-head "Wide" recap,
cascaded fanned panels). Cross-video child: 11 ← deep-learning/001_transformers_part1:43
(certified in the parent's own DB — `15_progress.py deps` showed `unblocked` before the
build started).

## Resume note

A previous worker (2026-10-12 04:47–04:58) banked chrome-landmark measurements, the
parent-base diff (30.9% hot px → full delta re-draw) and 7 region crops in
`scratch/slide011/`, but crashed before any DB/build/vision-read work (DB row was
`gen_status=pending`, qa/slide011 empty). This run resumed from those banked artifacts
(reused, never deleted) and restarted attempt numbering at 1.

## What was done

1. **Mapping** (re-confirmed): frame_011 landmarks identical to certified 015 —
   `frame_x = 17.628 + 0.961232*slide_x`, `frame_y = 0.955556*slide_y`
   (left 58↔42, right 901↔919, top 43↔45, bottom stroke 516↔540).
2. **Divergence**: parent-base diff 30.9% hot; chroma diff vs certified sibling 015's
   frame (luminance diffs are blind to pale-color changes here) isolates the true
   deltas: top-zone ribbon/chain, left input zone, query row, blue inner frame.
   Right side (cards, outContainers, W chips, swoosh arc, pills, tags, pipeline) is
   chroma-clean vs 015 → drawn at 015's certified values, re-verified by targeted
   PIL scans (m11) and the 14 banked gate reads.
3. **14 gate vision reads** (`an_*.txt`): A_leftinput, F_title, z9_topzone,
   z13_topright, z14_fartop, z1_leftW, z2_rightWv, z4_arclabel, z7_row1, z3_kq_frac,
   z5_dotprod, z8_chip_h1, z6_qWbox, z11_qrow. Key resolutions of the SOURCES.md
   build-time [?]s:
   - Arc label = `"H" Heads` (capital H, double quotes — same as certified 015; the
     raw's "*h* Heads" was a quote misread). z4.
   - Left W boxes: green fill, dark-green border, black italic W + illegible
     single-letter subscript + PALE-RED superscript, all four identical (z1); drawn
     as W_v^(0) per the raw cross-check (subscript [?] kept at render size).
   - Right W_v boxes: pale-cyan fill, navy border, red superscript, LEFT-pointing
     red arrowheads (z2). W superscript "(0)" kept per 015's 6x read (z2's "(r)" is
     a resolution misread of the same glyph).
   - Query row: 4 strips of ~7 cells w/ red-bordered X clusters, strip 2 dashed
     purple, five translucent attention ellipses, down-arrowhead at bottom (z11).
   - Dot Product label: two-line "Dot / Product", dark tan/brown (z5).
   - Chips: superscript color = border color per chip (q red, k green, v blue) (z8).
   - q W box: navy W, red shaft passing behind with heads at both ends; five-cell
     q-vector strip (z6).
4. **Build**: `recreated_pptx/build/slide_011.js` — requires the 001:43 certified
   component by ABSOLUTE path, `renderBase(pptx, slide, {numeral: 11, skip: [all 18
   content blocks]})` (chrome only, composition imported, never re-drawn), then the
   full 011 delta at measured geometry.
5. **Beam/ribbon engineering**: LO cannot render solid semi-transparent PNGs on this
   host (measured: matplotlib- and PIL-generated solid-alpha PNGs render blank in
   minimal decks, while varied-content PNGs and vector shapes render fine —
   `scratch/slide011/r4/bt*.png` experiments). The ribbon is therefore injected
   post-build as vector `custGeom` shapes by `scratch/slide011/fix_beam.py`
   (replaces the anchor `<p:pic>` whose descr names beam011.png; idempotent,
   fails loudly if absent). NOTE: any rebuild must re-run `fix_beam.py` before
   rendering. Cream + mint full-width strips are ordinary translucent shapes.
6. **Render**: LO PNG export at 2001x1125 (150dpi) via
   `--convert-to 'png:impress_png_Export:{PixelWidth:2001,PixelHeight:1125}'`
   (LO's PDF export path is broken host-wide at run time — impl_store Io Write 16 on
   any pptx incl. the known-good parent base; PNG export works. The rendered PNG is
   dimensionally identical to the pdftoppm -r 150 product).
7. **Self-checks (banked)**: `house_chrome_check.py` PASS (panel/badge within tol);
   `selfcheck_attempt_1.py` + `.out` — blue frame lines, beam core, chain boxes,
   orange arrows, left zone, K labels, K·q label, fraction ink, rotated labels,
   title ink, q container/ellipses/arrow all present; containment clean except the
   chrome border's own 1px halo at y=44 (excluded as chrome, documented).

## Judge

- **attempt 1: FAIL — infrastructure false positive.** LO's direct PPTX→PNG export
  replaced ALL raster images with LO's red "Image 0 1" broken-image placeholder text
  (`judge_attempt_1.txt`: BLOCKERs on the rotated Scaling/Softmax labels, the
  K·q/√d fraction and the swoosh). The same deck rendered via soffice→PDF→pdftoppm
  contains every image (rot-label ink 1004 px label-magenta, 0 placeholder px;
  swoosh 14,946 px; beam 42,361 px). Root cause: this host's LibreOffice 26.8.1.1
  failed its image import + PDF-export paths for parts of this run (PDF export
  fails with `impl_store Io Write 16` when run from the deep project path but
  works from a short home path — measured both ways; direct PPTX→PNG export drops
  every raster image regardless — measured with minimal decks).
- **attempt 2: FAIL — same infrastructure false positive** (`judge_attempt_2.txt`):
  the render was copied while the placeholder-bearing direct-PNG-export output was
  still in place; the build itself was unchanged.
- **attempt 3: PASS** (`judge_attempt_3.txt` — real comparison winner body,
  `--thinking high --max-tokens 65536`, W4 wall; render produced via the
  certified soffice→PDF→pdftoppm pipeline, `scratch/slide011/render_slide011.sh`,
  with every image verified programmatically before dispatch). Findings: 4 MINOR
  (Probabilities oval partially covered by the yellow wedge — the original shows
  the same overlap; swoosh stroke bolder than the original's; attention ellipses
  slightly larger/more saturated than the original's; faint Similarity/Weighted
  SUM ghost ovals slightly more visible). No BLOCKER/MAJOR; no containment or
  delimiter failures; text verbatim incl. `"H" Heads` and the stacked fraction.

Judge procedure executed by the worker (no spawn tool in this environment —
orchestrator-approved fallback). All three judge prompts banked; payload in
`judge_p_payload.txt`.

## Render-pipeline notes for future workers on this host (2026-10-12)

- LO's direct PPTX→PNG export DOES NOT render embedded raster images (renders
  broken-image placeholders) — never use it as the judge render.
- PDF export fails with `impl_store Io Write 16` for sources inside the deep
  project path, but works from a short home path (`/home/ahmed/lo_pdf_test`).
  `scratch/slide011/render_slide011.sh` encodes the working route:
  copy pptx → /home/ahmed/lo_pdf_test → soffice→PDF → pdftoppm -r 150 → copy PNG
  back into qa/. Intermediate copies live outside the project; all deliverables
  and evidence stay inside the video namespace.

## Deliverables

- `recreated_pptx/build/slide_011.js` (single-version build script)
- `recreated_pptx/slide_011_recreated.pptx` (single plain-named deliverable; OMML
  wrap n/a — the only equation-ish content is the already-certified mathtext PNGs)
- Evidence: `recreated_pptx/qa/slide011/` (render_1.png, judge_prompt_1.txt,
  judge_p_payload.txt, build_attempt_1.js, transcripts), `scratch/slide011/`
  (measurements m1..m11, colmaps, an_* reads, fix_beam.py, selfcheck).
