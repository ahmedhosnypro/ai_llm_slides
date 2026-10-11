# Retro-bank verification — components/slide_015.js (001_transformers_part1 slide 15)

**Result: ALL CHECKS PASS. GATE MET: 0 differing pixels vs the certified render.**

## What was banked

- **Component**: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_015.js`
  (NEW, additive — the certified deliverable/build/parent/QA evidence were NOT touched).
- **Why**: playlist-scoped banking obligation (dependencies.md v2). Slide 15 certified
  (DB: `gen_status=passed`, `visual_check=PASS`, attempt 1) before 002's graph existed;
  `videos/deep-learning/002_transformers_part2/slide_dependencies.json` now lists slide 4
  with cross-video parent `deep-learning/001_transformers_part1:15`. 002 slide 4 can now
  import the component by absolute path.
- **No certified state changed**: no DB writes, no judge re-run, no edits to
  `build/slide_015.js`, `components/slide_014.js`, `slide_015_recreated.pptx`, or
  `qa/slide015/*` (mtimes all predate this session: 14:29–14:46).

## Component contract

`renderBase(pptx, slide, opts)` draws the FULL certified slide-15 composition in the
certified z-order (chrome → inherited blocks → delta), with:

- `opts.skip` / `opts.only` — block selectors; **unknown names throw** (including
  parent-only names such as `arc`, which is absent from slide 15's composition).
- `opts.chrome` — default true; chrome via `components/house_chrome.js`, drawn once.
- `opts.numeral` — badge numeral, default 15.
- Exports: `{ renderBase, BLOCKS, C, px, GEO }` (GEO = per-block pt geometry for
  children's closed-loop self-checks).

**BLOCKS (z-order)** — 3 inherited + 7 delta:

| block | provenance |
|---|---|
| `title`, `left_panel`, `left_figure` | inherited — direct references to the certified parent's own `slide_014.js` block functions (never re-drawn) |
| `green_card` | delta — white card, 2pt `00B050` border, rect (573,105) 321×419 pt |
| `fig1_recolor` | delta — recolored Figure 1 asset `slide015_fig1_color.png`, 318×416 pt at (575,107) |
| `block_arrow` | delta — gutter arrow asset `slide015_blockarrow.png`, 68×24 pt at (458,295) |
| `up1`, `up2` | delta — small red up-arrow assets, 13×27 pt at (654,487) / 11×25 pt at (740,116) |
| `encoder_header`, `decoder_header` | delta — Arial bold italic 16 pt, `C00000` / `00A651` |

Delta code is copy-then-modify **verbatim** from the certified `build/slide_015.js`
(single source of truth); assets resolve from `components/` via `path.join(__dirname, "..", "assets")`.

## Verification (machine-only, all in this dir)

Driver `verify_build.js` (child-style: `new pptxgen()` + LAYOUT_WIDE + addSlide +
`renderBase(pres, slide, opts)`), rendered 150 dpi with LibreOffice 26.8 headless
(`TMPDIR` + LO profile under `scratch/tmp` — /tmp is quota-blocked), `pdftoppm -r 150`.
Full output: `verify_build_output.txt`, `verify_compare_output.txt`; renders in `renders/`.

| check | result |
|---|---|
| **GATE**: `component_full` render vs certified reference `qa/slide015/render_1.png` (both 2001×1125) | **0 differing pixels** |
| certified pptx re-rendered this session vs banked reference | 0 differing pixels (pipeline deterministic) |
| component render vs certified pptx render (same session) | 0 differing pixels |
| `skip:["block_arrow"]` smoke | 4,281 px differ, 100% inside the arrow zone (bbox x[954,1094] y[614,663]); stray outside = 0 — render banked |
| `only:[all-but-block_arrow]` vs `skip:["block_arrow"]` | 0 differing pixels (skip ≡ only complement) |
| `numeral: 99` override | badge crop == chrome-only(99) badge (0), default == chrome-only(15) (0), 15≠99 crops (non-vacuous); whole-slide diff 668 px confined to the badge |
| `chrome: false` | badge-center and gray-panel probe points read canvas-white; same points are chrome on the full build |
| unknown block names | throws for bogus names in `skip`/`only`, mixed valid+bogus lists, and parent-only `arc`; positive control: all 10 real names accepted |
| `house_chrome_check.py` on component render | PASS (panel x 89–1913, badge center (1860,148) d=70, tol 8) |

## Caveats / notes for children (002 slide 4)

- Block names are **slide-15-scoped**: skipping a parent-only block name (`arc`,
  `right_panel`, …) throws — those blocks do not exist in this composition. Skip/only
  must name blocks from this module's `BLOCKS`.
- The shared `drawHouseChrome` primitive suppresses the badge when the numeral is
  empty/undefined; this component always passes an explicit numeral (default 15).
- The 0-diff gate held without AA-noise caveats — the component's element sequence
  (order + content) is exactly the certified build's, so LO renders it identically.
- `scratch/tmp/` holds only the LibreOffice profile + temp from this verification run;
  everything else is under `scratch/slide015_component_verify/`.
