# Retro-bank verification — components/slide_033.js (001_transformers_part1 slide 33)

**Result: ALL CHECKS PASS. GATE MET: 0 differing pixels vs the certified render.**

## What was banked

- **Component**: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_033.js`
  (NEW, additive — the certified deliverable/QA evidence were NOT touched by this run;
  md5 pinned at bank time in `component_hash_at_bank.txt` = `1d40b0fd9b6cb40197346a7b80c1622e`,
  re-checked unchanged after all verification).
- **Why**: playlist-scoped banking obligation (dependencies.md v2). Slide 33 certified
  (DB: `gen_status=passed`, `visual_check=PASS`, attempt 3, 2026-10-12T01:10) before the
  law landed; `videos/deep-learning/002_transformers_part2/slide_dependencies.json` lists
  edges `8 -> deep-learning/001_transformers_part1:33` AND
  `13 -> deep-learning/001_transformers_part1:33`. Both children can now import by
  absolute path.
- **No certified state changed by this run**: no DB writes, no judge, no edits to
  `qa/slide033/*`. The certified drawing code was copied VERBATIM from
  `qa/slide033/build_attempt_3.js` (byte-identical to the pre-refactor certified
  `build/slide_033.js`); only restructuring was applied (per-block functions, module-scope
  palette/geometry, `(pptx, slide)` params).

## Component contract

`renderBase(pptx, slide, opts)` draws the FULL certified slide-33 composition in the
certified z-order, chrome drawn ONCE via `components/house_chrome.js`:

- `opts.skip` / `opts.only` — block selectors (array or Set); **unknown names THROW**.
- `opts.chrome` — default true. `opts.numeral` — badge numeral, default 33
  (explicit numeral always passed; drawHouseChrome suppresses the badge on empty).
- Exports: `{ renderBase, BLOCKS, C, px, GEO }` (GEO = DOTC, LINEY, DOTX, CIRC,
  KVEC, ROWY, BOXY — frame-pt geometry for children's closed-loop self-checks).

**BLOCKS (certified z-order, 18)**: panel, sentence, connectors, containers, dotproduct,
flowlines, wboxes, kvlabels, softmax, faintarrows, sigma, query, y2, pills, legend,
orangeheads, overlays, title.

## Verification (machine-only, all in this dir)

Driver `verify_build.js` (child-style: `new pptxgen()` + LAYOUT_WIDE + addSlide +
`renderBase(pres, slide, opts)`), rendered 150 dpi LibreOffice headless (`TMPDIR` +
LO profile under this dir's `tmp/` — /tmp is quota-blocked), `pdftoppm -r 150`.
Output: `verify_build_output.txt`, `verify_compare_output.txt`, `house_chrome_check_output.txt`;
renders in `renders/`.

| check | result |
|---|---|
| **GATE**: `component_full` render vs certified reference `qa/slide033/render_3.png` (both 2001×1125) | **0 differing pixels** |
| certified deliverable pptx re-rendered this session vs banked reference | 0 differing pixels (pipeline deterministic) |
| component render vs certified deliverable render (same session) | 0 differing pixels |
| `skip:["sigma"]` smoke | 23,712 px differ, 100% inside the sigma zone (bbox x[1074,1356] y[403,796] render-px = the Sigma box + circles + stems + stubs); stray outside = 0 |
| `only:[all-but-sigma]` vs `skip:["sigma"]` | 0 differing pixels (skip ≡ only complement) |
| `numeral: 99` override | badge crop == chrome-only(99) (0), default == chrome-only(33) (0), 33≠99 crops (non-vacuous, |diff|=123960); whole-slide diff 524 px confined to the badge |
| `chrome: false` | badge center + gray-panel probe points read canvas-white; same points are chrome on the full build |
| unknown block names | throws for bogus names in `skip`/`only` and mixed valid+bogus lists; positive control: all 18 real names accepted |
| `house_chrome_check.py` on component render (numeral 33) | PASS (panel x 89–1913, badge center (1860,148) d=70, tol 8) |

No AA-noise caveats — the GATE held at exactly 0 (as with the slide-015 retro-bank):
the component's element sequence (order + content) is exactly the certified build's.

## Parallel-worker observation (for the record, not caused by this run)

While this verification ran, ANOTHER worker retro-banked the same slide concurrently:
it updated an earlier draft of `components/slide_033.js` (01:20), refactored the certified
`build/slide_033.js` into a thin wrapper that `require`s the component (01:19, git `M`),
and regenerated `slide_033_recreated.pptx` (01:20). Cross-checks with the final state:
- The regenerated deliverable (wrapper + component) re-rendered this session is
  **0-pixel-diff vs the certified reference** — the refactor is pixel-true.
- The banked certified provenance `qa/slide033/build_attempt_3.js` is intact
  (23,441 bytes, mtime 01:02, pre-dating both workers).
- This run's component (md5 pinned above) was written 01:21, verified 01:29, and
  re-hashed unchanged after verification; the two components are render-equivalent
  (both 0-diff vs the reference), but THIS file is the one meeting the sibling
  contract (per-block functions + BLOCKS table + only/chrome opts + unknown-name
  throws + full exports) that 002:8/13 must import.

## Caveats / notes for children (002 slides 8 and 13)

- Block names are **slide-33-scoped**: skip/only must name blocks from this module's
  `BLOCKS`; anything else throws (there is no parent composition here — slide 33 is a
  ROOT slide; its only "chrome" is the house chrome via `opts.chrome`/`opts.numeral`).
- Recap-style children: `renderBase(pptx, slide, { numeral: <your printed badge number> })`
  + your measured delta. Never re-draw house chrome on top (drawn once inside).
- The 0-diff reference is the certified 150 dpi LO render; PowerPoint-vs-LO divergence
  notes from the certified run (explicit lineSpacing on title/Dot-Product boxes) are
  already baked into the component.
