# AGENTS.md — machine-learning lecture 03: Ridge Regression & Gradient Descent

Namespace: `videos/machine-learning/03_ridger_regression_gradient_descent/`
51 founder-curated unique slides (`unique_slides/slide_001.jpg` … `slide_051.jpg`,
numbered by the founder 2026-10-19; frames are 960×540, 1px = 1pt).
**Founder approved the frame set 2026-10-19** ("i have removed slides_index.json and
deleted duplicated slides, and it's your job now …" — verbatim record in
`slide_dependencies.json` under `founder_message_2026-10-19`). The 2026-10-10 HARD STOP
is lifted for this set. The founder also removed `frames/` and the pre-curation
index/mapping: the 51 files are the authoritative set and the pre-curation state is
intentionally unrecoverable — never hunt for old artifacts (owner-replaced-state law).

## House chrome — THIS deck (measured 2026-10-19; overrides 17_worker_instructions.md's ml-intro values)

Every recreated slide uses the SAME outer template, measured from
`unique_slides/slide_003.jpg` and verified constant across 001/005/009/018/040.
Same family as lecture 02 (white canvas + gray panel + red strokes + yellow badge
with purple ring), but the geometry DIFFERS from 02's ratified values — use THESE:

- Slide `LAYOUT_WIDE` 13.33 × 7.5 in; canvas `FFFFFF`.
- Gray panel `E9E9E7`: rect at x 54px, y 45px, w 850px (x54..903), h to the slide
  bottom (540px). The rect carries NO border line.
- Thin red `C00000` 1pt strokes, drawn as THREE line shapes — left vertical at
  x 58.5 (rows 46..539), right vertical at x 901 (rows 46..539), bottom horizontal
  at y 538.5 (cols 58..902, half-visible at the slide edge). **NO TOP STROKE** —
  measured red px in the top band = 0 on all five reference frames; a top stroke on
  a render is a BUILD DEFECT, and "missing top stroke" is never a judge finding.
- Badge: circle d≈35px centered (876, 73)px — fill `FDFD96`, purple ring `6A5ACD`
  ~2pt, bold numeral `333333` (Arial 18pt). **Numeral = the file number N** (the
  originals print it; verified against 48/48 raw analyses; no zero-padding).
- Runnable module + checker: `shared_patterns/house_chrome.js`
  (`drawHouseChrome(pptx, slide, {numeral})`) and `shared_patterns/house_chrome_check.py`
  — run the checker on every 150dpi render BEFORE judging; FAIL = fix first.
- NOT the ml-intro chrome (E8E8E8 / 0.15in frame / outline-less FFF9C4 badge), and
  NOT 02's geometry (02: panel x61..899 WITH a top stroke). The GROUND RULES clause
  in judge prompts must describe THESE values — the frozen template is
  `shared_patterns/judge_protocol_03.md`; source the `-p` payload byte-for-byte from it.

## ZOOMED VISUAL JUDGE — EVERY slide (founder directive 2026-10-19, non-negotiable)

All of the slides require zoomed visual judging. A slide's certification needs BOTH:

1. the full-slide comparison judge (frozen template in
   `shared_patterns/judge_protocol_03.md`), AND
2. zoomed crop-pair certificates — at minimum ONE per slide covering its densest
   content region (one per dense region on multi-region slides: tables, equation
   stacks, small-text clusters, graph annotations). Crop-vs-crop ONLY, matched
   effective scale, coordinates mapped back to slide space before any edit —
   full procedure + frozen crop prompt in `shared_patterns/judge_protocol_03.md`.

Both must be clean (or findings adjudicated PIL-first per judging.md) before
`visual_check=PASS` is written. This deck's judge dispatches go through
`scripts/16_vision_gate.sh` with `--thinking high --max-tokens 65536` — see the
protocol file for walls and invocation.

## Slide dependency graph (founder-supplied 2026-10-19 — canonical, also in slide_dependencies.json)

Edges (child → parent; child builds on the parent's certified composition):

- `10 > 9`
- `13 > 12` — shares slide 12's table PATTERN (same table layout, different numbers)
  at a DIFFERENT position: inherit 12's table component, redraw with 13's measured
  geometry + 13's values
- `17 > 13` — shares 13's tables (same pattern, different numbers); the chain
  12→13→17 composes transitively
- `18 > 17`

Builds gate on parent certification (`gen_status='passed'` AND `visual_check='PASS'`).
Children import the parent's certified component from
`recreated_pptx/build/components/slide_NNN.js` (`renderBase(pptx, slide, opts)` +
per-block exports with skip/only; never copy-paste, never re-derive). Components are
certified single-source-of-truth: editing one re-opens its descendants (cascade law).
Full law: `~/.zcode/skills/slide-recreation/references/dependencies.md` + the
DEPENDENCY-GATED section of `scripts/17_worker_instructions.md`.

## Deck-specific notes

- Badge numerals: originals print their own number; the badge numeral is exactly N
  (file number). Verified 48/48 against the raws' verbatim_text; the three
  pending raws (033/043/044) were checked at build time by their workers.
- Provenance: 35 of 51 slides carry recovered precuration provenance in
  `unique_slides/slides_index.json` (rebuilt from the raws' `_meta`); 16 slides
  (1,2,3,13,24-29,33,35,36,43,44,47) are honestly marked unrecoverable — the owner
  removed the pre-curation state. Do not treat the gap as an error.
- `analysis/RECONCILE_NOTE.md` records the `slide_50_raw.json` → `slide_050_raw.json`
  rename (OCR-attribution verified; mv preserves bytes).
- No cross-video dependencies.
- **Web-source research IS mandated for this deck** (founder in-session directive
  2026-10-19: "you have dropped the websearch part from the slide-recreation …
  check the skill references/source-research.md"). Full section below.
- Equations: professional 2D format (matplotlib mathtext → 600dpi transparent PNG →
  addImage at exact px/600 size), OMML wrap post-certification per the single-version
  law (`scripts/18_omml_wrapper.py`, manifest rel-ids re-derived from the CURRENT pptx).
- Advanced graphs (if any slide shows fitted curves / loss contours / 3-D surfaces):
  graphgen venv + topic-correct library per the advanced-graph rule; single
  plain-named deliverable `slide_NNN_recreated.pptx`.
- Scratch/QA law: TMPDIR redirects to project scratch
  (`export TMPDIR=/home/ahmed/Projects/ai_llm_slides/scratch/tmp`); all vision calls
  through `scripts/16_vision_gate.sh`; qa/ + scratch/ untracked by convention;
  never delete banked evidence.

## Web-source research mandate (founder in-session directive 2026-10-19)

The founder activated web-verified source research for THIS deck in-session
("you have dropped the websearch part from the slide-recreation and i wanna you
to do it, check the skill references/source-research.md"). The binding contract is
`~/.zcode/skills/slide-recreation/references/source-research.md` — read it before
any research work. Deck-specific activation details:

- **Tool**: the agy search CLI (`agy -p "<query>"`; on 401/403 auth errors mint a
  fresh token with `agy -p "hi"` and retry once). Fetch with WebFetch (curl as
  fallback). Every URL recorded in a SOURCES.md was fetched live in the same work
  window that recorded it — search snippets are LEADS, never sources.
- **Layout** (per the reference's layout law): fleet map
  `SOURCES_MAP.md` at the namespace root (orchestrator-owned — research workers
  never edit it), per-slide records under `sources/slide_NNN_source/` with the
  required `SOURCES.md` skeleton. No SOURCES.md = the leg did not happen.
  Originals are saved as downloaded, never renamed or deleted.
- **Interleaves with builds; never dependency-gated** — a slide's research may
  land before, during, or after its build; it never blocks build dispatch, and a
  closed search window never blocks certification (bank the attempt log as a debt
  record, mark `[?]`, move on; the leg re-runs when the window reopens).
- **Corrections** patch analysis-JSON model annotations ONLY (dimension/
  attribute/provenance guesses) — NEVER transcribed frame text. The frame wins
  for recreation; the source wins for understanding. Course-authored deltas
  (recoloring, pedagogy callouts) are recorded, never "fixed" toward the source.
- **No vision calls**: research is web + local-file work only (frame facts come
  from the slide's analysis record; view frames with local image reads, never
  through `16_vision_gate.sh`).
- **Economy law**: check sibling SOURCES.md records before re-spending a query;
  disclose the query budget per worker in the final report.
- **Close-out deliverable**: 51/51 SOURCES.md + SOURCES_MAP.md rows — research
  completeness is recorded in CLOSEOUT_REPORT.md alongside the visual gate.
