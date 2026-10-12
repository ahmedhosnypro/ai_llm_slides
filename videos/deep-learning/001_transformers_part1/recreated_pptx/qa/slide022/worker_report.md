# Worker report — slide 022 (001_transformers_part1, Deep Learning DSAI 308)

**Slide:** 022 — "Continuous bag-of-words (CBOW)   vs Skip-Gram Models" (Mikolov 2013
Figure 1 architectures, course recoloring; provenance in `slide_022_source/SOURCES.md`,
figure banked as `efficient-models.svg`, byte-verified).
**Final verdict: PASS** (attempt 1 of 6; judge procedure executed by worker — no
spawn tool in this environment, fallback per `scripts/17_worker_instructions.md` §7,
which is orchestrator-approved).

## Deliverables

- PPTX: `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_022_recreated.pptx`
- Build: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_022.js`
  (per-attempt copy: `qa/slide022/build_attempt_1.js`)
- Render (150 dpi): `qa/slide022/render_1.png`
- Judge transcript: `qa/slide022/judge_attempt_1.txt` (banked prompt: `judge_prompt_1.txt`)
- Probe transcript: `qa/slide022/probe_1.txt`
- Self-check: `qa/slide022/selfcheck_attempt_1.py` + `selfcheck_attempt_1_output.txt`
- Measurements: `scratch/slide022/measure1..7.py`, vision reads
  `scratch/slide022/vision_lproj.txt` (CBOW PROJECTION zoom), `vision_title.txt`

## DB final state

`gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`,
`visual_transcript=videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide022/judge_attempt_1.txt`,
`pptx_path` and `build_script` set. Slide 22 is a ROOT (no deps, no dependents in any
video's `slide_dependencies.json`) — no component-banking obligation triggered.

## How the build was derived

1. PIL-measured the frame (960x540, 1px=1pt): blue panels x117..487 / x486..840
   (shared middle edge) y122..524 #0000CC; six containers y142..462 (INPUT #8B0000 /
   PROJECTION #E8940A + #F5C99B fill / OUTPUT #008000, white fills); header band
   y164..173; label bands; yellow tags x254..378 / x551..675 y474..502; title ink
   x131..857 caps y76..94.
2. The paper SVG (`efficient-models.svg`) pinned the topology: 4 tall squares per
   column in an uneven pair-gap-pair rhythm; converging/fanning arrows; SUM above the
   projection square. The frame preserves that rhythm exactly (label centers
   213.5/271/378.5/432 match the paper's 59/113/59 spacing scaled).
3. High-sensitivity edge tests confirmed the small squares DO exist in the frame
   (edges y193/235, 248/290, 355/397, 409/451 — #D9D9D9 outlines invisible to naive
   scans on the white containers). Projection squares pinned by gate vision read:
   x305..328 / x607..630, y302..348.
4. Typography solved from glyph-advance math: all diagram text Arial 11 regular
   (#404040 headers/labels, #000000 w(t) labels — widths match regular advances
   exactly, bold rejected); title Arial Bold 26pt #C00000 (26pt, not the spec's ~28pt
   estimate, because measured ink width 726px and cap height ~18.5px both solve to
   26pt; the spec's 3-space gap renders 24px at 26pt = measured gap exactly); title
   box centered on the MEASURED ink center x494 (not slide center 480).
5. Tag text: frame pixels prove the tag text is dark olive #4A4A00, NOT the spec's
   "red" (core pixels 110,117,37 = exactly a #4A4A00-on-#FFFF99 JPEG blend; a #C00000
   text would measure R>>G, measured R==G). Border stays #C00000 per spec. Tag fill
   #FFFF99 confirmed. Recorded here as a frame-wins-over-spec decision per the
   fidelity law.

## Pre-judge self-checks (all PASS)

- `house_chrome_check.py`: PASS (panel, badge within tol 8).
- Closed-loop PIL vs original (tolerances 4-6px): title bbox (all 5 metrics PASS,
  center 493 vs 494), 3 blue panel edges each axis, 12 container border columns
  (dkred/orange/green color-specific), 16 small-square edges (<=1px), both PROJECTION
  squares, 6 headers, 8 word labels, SUM, both tag boxes, all 10 arrows present,
  containment (no content ink outside the chrome panel; flagged "stray" ink is the
  chrome's own #C00000 border, verified identical to the original).
- One build bug found and fixed pre-judge: `label()` used the frame-px center as
  inches (headers + SUM landed off-slide; LibreOffice clamped one to the left edge).
- No equations / multi-line delimiters / tables on this slide, so the mandatory
  dense-region crop comparison is not triggered (N/A per self-check list).

## Judge (attempt 1)

Gateway probe initially returned empty twice (fleet congestion; other slides building
in parallel); after the mandated sleep 300 + single re-probe the window opened, and
the comparison landed on the first invocation with `--thinking high --max-tokens
65536` at the W4 wall (540 outer / 420 inner). Certificate: single-read, default route
(images), glm leg DEFERRED/BLOCKED.

Findings (verbatim summary): element-by-element inventory all "Yes" (title verbatim
incl. the wide pre-"vs" gap, badge 22, blue split frame, both three-column diagrams,
SUM, flows, tags, headers, label sides). Discrepancies: 3 x MINOR (proportions note,
title weight/size slightly heavier, arrow endpoints touching square edges rather than
stopping short) — none MAJOR, none BLOCKER. No missing elements, no frame-containment
violations, text verbatim throughout, no clipping/collisions. Mouse cursor correctly
omitted per ground rule (c).

**FINAL VERDICT: PASS for 'faithful, usable recreation'.**

The MINOR #1 rationale ("original is a squarer 4:3 capture") is factually imprecise
(both images are 16:9) but non-blocking and does not change the verdict.

## Attempts used

1 (first-attempt PASS; the pre-judge loop consumed one local rebuild for the label()
bug before any judge dispatch — attempt numbering counts judge dispatches).
