# AGENTS.md — 001_transformers_part1 (Transformers — Part I, Deep Learning DSAI 308)

## Founder directive 2026-10-11 — web-verified analysis is MANDATORY on this video (CRUCIAL video)

For EVERY slide's analysis (script 12), validation (13), recreation, and QA on this
video — before trusting any extracted data:

1. **Websearch always** to find/confirm the primary source behind the slide
   (equations, numbers, diagram labels, figure provenance). Tool: `agy -p "<query>"`
   (on 401/403 run `agy -p "hi"` once to re-mint the token, then retry).
2. **Webfetch the sources** (WebFetch/curl) and confirm the slide's content against
   them.
3. **Download the site's own images when they exist** — if a source page hosts the
   original figure the slide reuses, save it to `slide_NNN_source/`. These are
   reference-grade ground truth; the video's JPEG frames are not.

## Per-slide pattern

```
slide_NNN_source/
  <downloaded figures>        # originals as downloaded — never renamed/deleted
  SOURCES.md                  # provenance record
```

SOURCES.md records: source URL(s), what each downloaded file is (figure number +
caption), what data the source confirmed or corrected, open questions marked `[?]`.
**No SOURCES.md = the research step did not happen.** Vision work runs through
`.agents/skills/image-analysis` (banked `.txt` transcripts; never Read raw image
bytes into agent context).

## House chrome — RATIFIED at playlist level (founder directive 2026-10-11)

The founder ratified the deck-native chrome and generalized it: **one outer frame
size/position and one badge position/size for EVERY recreated slide in EVERY lecture
under `videos/deep-learning/`**, measured from THIS deck's slide 1. The binding law
and the shared runnable pattern live at:
- `../AGENTS.md` (playlist AGENTS.md — read it before building anything here)
- `../shared_patterns/house_chrome.js` (import it; never re-draw the frame/badge)
- `../shared_patterns/house_chrome_check.py` (run on every 150dpi render pre-judge)

The ml-intro house values in the root AGENTS.md / `scripts/17_worker_instructions.md`
are superseded for this playlist. Certified slides 2 and 3 already conform.

## Slide dependency graph & shared component builds (founder directive 2026-10-11)

Many advanced slides in this deck re-use a previous slide's composition with a delta
(extra blocks / removed blocks / replaced blocks). The founder-supplied graph lives in
`slide_dependencies.json` (canonical) and the DB (`depends_on`; view with
`python3 scripts/15_progress.py deps`, `VIDEO=deep-learning/001_transformers_part1`).

Edges (child ← parent): 7←6, 8←6, 9←6, 10←6, 15←14, 18←17, 19←18, 27←26, 28←26,
29←26, 30←29, 35←34, 38←37, 44←43, 45←43.

- **Builds are gated**: a dependent slide's build may start ONLY when its parent is
  certified (`gen_status=passed` AND `visual_check=PASS`). One parent's certification
  unblocks ALL its children at once (e.g. 6 certifying unblocks 7/8/9/10 — dispatch
  them in parallel). **Analysis (12) and validation (13) are never dep-gated.**
- **Shared components (u-components model)**: a parent's certified composition is
  exported as `recreated_pptx/build/components/slide_NNN.js`
  (`renderBase(pptx, slide, opts)`; house chrome via `components/house_chrome.js`).
  Child builds `require` the parent component and draw ONLY their own delta at their
  own measured geometry — never copy-paste a parent's geometry. Chains compose
  transitively (30 imports 29's component, which imports 26's).
- **Components are certified single-source-of-truth artifacts**: never edit one
  after certification (cascade law: an edit re-opens every descendant — rebuild +
  re-judge the subtree); copy-then-modify into a new module instead.
- Full contract: `.agents/skills/slide-recreation/references/dependencies.md` and the
  DEPENDENCY-GATED section of `scripts/17_worker_instructions.md`.

**Figure family**: slides 14, 15, 16, 17, 18, 19 all draw on the founder-downloaded
paper figures in `slide_18_source/` (dir name is HISTORICAL — it dates from the
pre-curation numbering; resolve any "slide N" through `unique_slides/new2old_mapping.json`
before assuming a pre-curation artifact belongs to the same-numbered slide). Slides
14 and 15 MUST use the downloaded images (founder explicit). Vision-verified
(2026-10-11): per-figure use — 14/15/16/17 show Figure 1 only; 18/19 show Figure 1 +
Figure 2 left + Figure 2 right; slides 38 and 44 ALSO embed Figure 2 left/right
respectively as course-style insets. Every slide in this list carries a SOURCES.md
entry referencing the figure bank.

**Curation record (2026-10-11)**: founder curated 123 → 45 (dense renumbering;
`new2old_mapping.json` maps new→old, including 6 founder-swapped frames and the
old-group-14 split into new slides 7/8). Pre-curation artifacts kept:
`slides_index_old123.json`, `slides_progress_old123.db.bak`.


## Worked example — the attention/transformer figure family (founder-provided, 2026-10-11)

- The founder downloaded the original figures of **"Attention Is All You Need"**
  (Vaswani et al., 2017) from https://arxiv.org/html/1706.03762v7 into
  `slide_18_source/` (the dir name is historical — it dates from the pre-curation
  numbering; the exact frame originally analyzed was culled in curation):
  - `The Transformer - model architecture..png` = Figure 1 (full encoder–decoder)
  - `slide18 scaled dot-production attention figure.png` = Figure 2 left
    (Scaled Dot-Product Attention)
  - `slide18 Multi-Head Attention\n\n.png` = Figure 2 right (Multi-Head Attention)
    — filename contains literal newline characters: always quote it in shell, or
    copy-rename; never delete or rename the founder's original.
- These are the source images for **slides 14–19** (see the figure-family note
  above): the course redraws them in its own style/colors — topology and labels
  are the paper's, pixel style is the slide's. Slides 14 and 15 MUST use the
  downloaded images (founder explicit); the rest of the family references them for
  legibility/data confirmation and recreation QA.
- Full provenance record: `slide_18_source/SOURCES.md`.

## Fidelity law (unchanged — binds web research too)

- The ORIGINAL VIDEO FRAME is ground truth for what the slide shows (layout,
  verbatim text, drawn content). Web sources confirm/correct DATA and explain
  provenance; they never license inventing or "improving" content the slide
  doesn't show.
- If source and slide disagree: record the discrepancy in SOURCES.md — the slide
  wins for recreation, the source wins for understanding.
- Specs keep `[?]` markers; a web confirmation may remove a `[?]` only with the
  confirming URL recorded in SOURCES.md.

## HARD STOP (founder directive 2026-10-10 — non-negotiable, binds every NEW extraction)

This video's frame-set review is **COMPLETE**: the founder reviewed the 123-frame
packet and curated the deck to **45 slides** on 2026-10-11 (dense renumbering, founder
frame swaps, dependency graph — all recorded in `unique_slides/slides_index.json`,
`unique_slides/new2old_mapping.json`, `slide_dependencies.json`). That curated set is
the state of record; the per-slide research pattern in this file is ACTIVE for it.

The law itself still binds every future extraction (the remaining playlist lectures):
after `11_unique_slides.py` produces `unique_slides/`, STOP — no script 12/13, no
builds, no subagent fan-out on those frames, no bulk per-slide research, and nothing
marked approved, until the founder has reviewed and approved the set. The machine may
prepare the review packet only.
