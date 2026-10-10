# AGENTS.md — AI Agent Context for ai_llm_slides

## What this project is

A pipeline that cuts course videos into unique slide frames, analyzes each slide with a
vision model (verbatim text + layout + colors + charts), validates the extraction with a
text model, and saves PowerPoint-recreation-ready JSON. The outputs feed a later
"generate PowerPoint slides with AI" step — **fidelity of content and visualization
description is the whole point**.

## Multi-video layout (founder directive 2026-10-09)

The project processes **several videos in parallel**. Every video owns a namespace under
`videos/<VIDEO>/` — currently `ml-intro` is the only one, but nothing is shared between
namespaces except the scripts and the model endpoint. Adding a video = adding a directory:

```
videos/
  ml-intro/                 # <VIDEO> id used in commands and env vars
    ml-intro.mp4            # source video
    frames/                 # 1 FPS extraction (large)
    unique_slides/          # kept slide images + slides_index.json (+ new2old mapping)
    analysis/               # slide_XXX_raw.json → slide_XXX_final.json, slides_final.json
    analysis_old104/        # archive of the pre-curation 104-slide run (never delete)
    recreated_pptx/         # build/slide_XXX.js, qa/slideXXX/, slide_XXX_recreated.pptx
    slides_progress.db      # per-video progress DB (+ slides_progress_old104.db.bak)
```

Rules:
- **Everything a command touches must stay inside one video's namespace.** Pass the
  video's dirs explicitly to scripts 10–13 (`10_extract_frames.sh <video> <frames_dir>`,
  `11_unique_slides.py <frames_dir> <unique_slides_dir>`, `12_analyze_slides.py
  <unique_slides_dir> <analysis_dir>`, `13_validate_slides.py <analysis_dir>`), and set
  `VIDEO=<id>` for `15_progress.py` (defaults to `ml-intro`) so parallel videos' DBs
  never collide.
- **The vision gate (`scripts/16_vision_gate.sh`) is fleet-global** — it throttles ALL
  videos' vision calls together through the shared localhost:17844 gateway.
- Never write one video's artifacts into another video's directory or into the project
  root; never delete banked evidence (builds, QA transcripts, archived runs).

## Model & Endpoint

| Setting | Value |
|---|---|
| Base URL | `http://localhost:17844/v1` (local IronRouter **dist** lane) |
| API key | `.analyze-image-key` in the project root (mode 600); `IR_API_KEY` env overrides |
| Vision model | `images` (IronRouter virtual model; fallback that worked on a codespace: `glm-5.3-flash`) |
| Validation model | `glm-5.3` |

## Hard-won operational facts (do not relearn these)

1. **Always stream** (`stream=True`) — the NVIDIA NIM upstream gateway cuts non-streaming
   responses at ~60s. Big vision analyses take 3–5 min; non-streaming requests die as
   `ServiceTimeout` on every key while the router churns the key pool. Streaming works.
2. `finish_reason=length` with `content=null` and a filled `reasoning_content` means the model
   spent its whole budget thinking — raise `max_tokens` (analysis uses 16000).
3. Vision-frame token cost: **~540 tokens/frame** at 960px JPEG q4. Budget accordingly.
4. **phash dedup with threshold 8** groups slide builds/animations reliably. Keep the
   **last** frame of each group (fully-built slide), not the first.
5. Analysis is slow (~3–5 min/slide including upstream key churn). Validate with
   `finish=stop` per slide in the log; retry individual failures by deleting the
   `slide_XXX_raw.json` and re-running — both 12 and 13 are idempotent (skip existing outputs).
6. glm-5.3 occasionally returns empty content (parse error "Expecting value: line 1 column 1") —
   just re-run script 13; it retries only the missing finals.
7. YouTube blocks anonymous downloads from datacenter/rate-limited IPs — use
   `--cookies /tmp/yt-cookies.txt` (exported from Chrome).

## House frame rule (founder directive 2026-10-09 — OVERRIDES per-slide analysis & judge)

ALL recreated slides share ONE outer visual template, taken from slide 3 (the reference
render). This is a hard rule that overrides any per-slide image-analysis JSON, any
`recreation_brief`, and any visual-judge finding about these elements:

- Slide size: `LAYOUT_WIDE` 13.33 × 7.5 in; slide background `#E8E8E8`.
- **Outer red frame**: rectangle at `x=0.15, y=0.15, w=13.03, h=7.2` (0.15 in inset from
  every edge), border `#C00000` width 1.5, no visible fill (background gray).
- **Slide-number badge**: yellow circle `x=12.48, y=0.30, w=0.5, h=0.5` (fill `#FFF9C4`,
  outline `#FFF9C4`), centered bold number 18pt, `#333333`. **Badge numeral = the number
  printed on the ORIGINAL slide image** (founder directive 2026-10-09, deck curation). After
  the founder's curation the deck is 64 slides and `unique_slides/slide_NNN.jpg` is named
  BY that printed number, so in practice the badge reads exactly `N` (no zero-padding) —
  and a recreation whose badge does not match the original image's number is WRONG.
  The mapping from the old 104-slide numbering lives in `unique_slides/new2old_mapping.json`.
- **Slide title**: text box starts at `y=0.28` (`x=0.6, w=12.13`, horizontally centered).

If a slide's spec or a judge verdict disagrees with these positions/sizes, the house rule
wins. Never "fix" a slide away from these values, and treat judge discrepancies about the
frame / badge / title-y as overridden (they are not fix triggers).

**Math equation format rule (founder directive 2026-10-09):** any equation on a recreated
slide is rendered in **Professional Format (2D / non-linear visual representation)** —
never Linear Format (plain-text/linear math notation):

- **Fractions**: stacked visually with a horizontal fraction bar (numerator above, denominator below) — never inline `a/b` or `a over b` text.
- **Summation (`∑`)**: a large summation glyph with upper and lower limits placed directly above and below it (or to the right, e.g. `∑ᵢ₌₁ⁿ`-style, as the original slide shows) — never inline `sum from i=1 to n`.
- **Subscripts & superscripts**: spatially aligned with proper math-font spacing and proportions — never caret/underscore text (`x^2`, `x_1`), never Unicode look-alike approximations of stacked constructs.

The equation's *content* stays verbatim per the output contract; only its *rendering* is
professional-format. The concrete mechanism is **vision-certified (2026-10-09)**: matplotlib
mathtext → tight transparent PNG (600 dpi) → `pptxgenjs.addImage()` at exact size
(`w = px/600` in, never rescaled). Hand-authoring OMML/Office-Math *for rendering* is
forbidden — LibreOffice headless renders only the linear fallback (measured, see
`videos/ml-intro/recreated_pptx/qa/math/`). Full usage contract lives in
`scripts/17_worker_instructions.md` + `qa/math/scratch_validation_report.md`.
Equation-vs-original linear-notation differences are covered by a judge GROUND RULES clause
(e-format upgrade, not a discrepancy).

**Dual-representation standard (validated 2026-10-10; naming per single-version rule):**
after a slide's PNG-based equation build is certified, `scripts/18_omml_wrapper.py`
upgrades the pptx so PowerPoint shows **editable native equations** while LibreOffice
renders the exact certified pixels. It is a zip-level post-processor: each
manifest-listed equation `<p:pic>` is wrapped in `mc:AlternateContent` —
`mc:Choice Requires="a14"` holds real OMML in the **PowerPoint-authored pattern**
(wrapper v2: `m:oMathPara(jc=centerGroup)`, Cambria Math runs with `i`/`smtClean`,
`m:ctrlPr` in every construct, Choice shape id = the Fallback pic's id — v1's
LibreOffice-writer pattern rendered NOTHING in PowerPoint, measured), `mc:Fallback`
holds the original PNG pic verbatim. Validated: LO render of the wrapped file is
**pixel-identical** (0 of 2,251,225 pixels differ), idempotent, fail-loud, no
rels/content-types touched. Contract: `python3 scripts/18_omml_wrapper.py
<input.pptx> <manifest.json> [-o out.pptx]`; manifest values come from the `eq_*.json`
sidecars (`rel_id, image, mathtext, font_size_pt, color`), re-derived from the CURRENT
pptx after any rebuild (never assume rel ids survive). Apply the wrap to the slide's
own pptx (the single plain-named version); never LO-resave a wrapped deck (LO's writer
drops the OMML it never understood — measured). Details:
`qa/omml_v2/OMML_V2_REPORT.md`.

**Advanced-graph generation rule (founder directive 2026-10-09; naming per
single-version rule):** slides whose originals contain advanced graphs (3-D scatters,
PCA projections, learned-model plots — anything the native pptxgenjs chart/shape engine
can only approximate) get their graphs embedded from a properly generated image:

- Images are produced by the **correct Python libraries for the slide's topic** (e.g.
  scikit-learn + matplotlib for ML plots), running the **same AI algorithm** on the right
  data (e.g. `sklearn.decomposition.PCA` on the real IRIS dataset for a PCA slide) — not
  hand-drawn approximations. Library/function/algorithm/data are chosen **per slide**.
- Tooling lives in the `graphgen/` venv subproject (see `graphgen/README.md`); web research
  for lib choice goes through the agy search CLI.
- Workflow per slide: pick lib/function/algorithm/data → generate image matched to the
  original's measured colors/orientation/region → validate (vision comparison vs the
  original frame) → fix → embed in the slide build.
- **Single version per slide (founder directive 2026-10-10):** the deliverable is ONE
  pptx per slide, named `slide_NNN_recreated.pptx` with NO suffix. A graph slide's own
  pptx HAS the generated graph embedded; an equation slide's own pptx HAS the OMML wrap
  applied. There are no `_graphed`/`_omml` variants — superseded builds live only in QA
  evidence dirs, never as parallel deliverables. Evidence banks under `qa/slideNNN/graphgen/`.
- Pilot: slide 64. The validated pilot pattern in `qa/slide64/graphgen/` is the reference
  for all subsequent graph slides.

**Deck curation note (2026-10-09):** the founder manually reviewed all extracted slides,
deleted duplicates and non-valid slides (including "Processing..." placeholder frames and
number mismatches), and renamed the remainder to 64 files numbered by the original on-slide
number. The mapping from the old 104-slide numbering lives in
`videos/ml-intro/unique_slides/new2old_mapping.json`. The old 104-slide artifacts are
archived under their old names (`videos/ml-intro/analysis_old104/`,
`videos/ml-intro/slides_progress_old104.db.bak`, `videos/ml-intro/recreated_pptx/build/slide_OOO.js`,
`videos/ml-intro/recreated_pptx/qa/slideOOO/`) and may be reused as prior work via the
mapping file — never delete them.

## Directory layout

```
scripts/   10_extract_frames.sh, 11_unique_slides.py, 12_analyze_slides.py, 13_validate_slides.py
videos/    one namespace per video (see "Multi-video layout" above)
.agents/skills/slide-recreation/   the distillation of this whole pipeline as a
                                    self-learning skill (SKILL.md + references/ +
                                    memory/ lessons + scripts/). Use it for any
                                    slide-recreation/PPTX-generation task; append new
                                    experience to its memory/ dir per its README.
```

All working data lives under `videos/<VIDEO>/`; the project root holds only scripts,
docs, and the API key.

## Output contract (what the PPTX-generation step consumes)

`analysis/slides_final.json` — array of slide objects with: `slide_title`,
`verbatim_text` (bullets/labels/equations — VERBATIM, no paraphrasing), `layout`
(arrangement + regions), `visual_elements` (type, chart data values, colors, position),
`imagery`, `colors` (approx hex), `typography_notes`, `recreation_brief` (numbered
recreation checklist), and a `validation` block (verdict, fixes, uncertain items
marked `[?]`, recreatability score). Never invent facts — uncertain content keeps its
`[?]` marker.

## QA evidence removal (founder directive 2026-10-10)

The `videos/ml-intro/recreated_pptx/qa/` evidence tree was REMOVED at the founder's
direction after the program completed. What survives: the certified deliverables (64
single-version pptx + ml-intro_final.pptx), the full build chain (`recreated_pptx/build/`
with per-slide scripts, graph assets, OMML base builds + manifests + wrapper), the
certified reference render (`videos/ml-intro/ml-intro_final_render_certified.pdf`),
the pixel-gate record (`videos/ml-intro/final_deck_pixel_gate_2026-10-10.txt`), the
program report (`videos/ml-intro/CLOSEOUT_REPORT.md`), the certified math tooling
(`scripts/render_eq*.py`), and the 30+ lesson corpus in the skill memory. Historical
references in docs/skill files to `qa/slideNNN/...` paths are historical — those dirs
no longer exist. Per-slide re-certification after any future fix is mandatory (judge
template in scripts/17_worker_instructions.md).
