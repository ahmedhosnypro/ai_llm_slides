# Building — pptxgenjs build, render, house template

## Build script

`recreated_pptx/build/slide_NNN.js` using pptxgenjs (4.0.1 quirks below). Run with:
`NODE_PATH=$(npm root -g) node build/slide_NNN.js` from the project root.

- `pres.layout = "LAYOUT_WIDE"` → 13.33 × 7.5 in. Originals at 960×540 px mean
  **1px = 1pt** — every measured original coordinate converts directly.
- Read the spec JSON fully first; honor `verbatim_text`, `layout`, `visual_elements`,
  `colors`, `typography_notes`, `recreation_brief`, and `validation.fixes`.
- Set `fontFace` explicitly on every text element (Arial unless the spec says
  otherwise); `margin: 0` on text boxes that must align with shapes.
- Bullets are manual: prefix `"• "` yourself; pptxgenjs has no auto-bullet here.

## pptxgenjs 4.0.1 pitfalls (each caused a real bug)

- **NEVER prefix hex colors with `#`** — corrupts the file. No 8-char hex either; use
  the `transparency` property, not alpha hex.
- `addImage` must use exact size for equation/graph assets (see equations.md/graphs.md)
  — rescaling blurs glyphs.
- Images are PNG only for precision assets; LibreOffice rasterizes SVG unpredictably.

## Rendering for QA

```
soffice --headless --convert-to pdf --outdir <qa_dir> <pptx>   # private profile!
pdftoppm -png -r 150 <pdf> <qa_dir>/render_K
```

- Use a **private LibreOffice profile** (`-env:UserInstallation=file:///tmp/...`) —
  shared/first-run profiles cause inconsistent renders and blocked locks.
- 150 dpi render of a 960×540-original slide → scale factor ×2000/960 when comparing
  to original-frame pixel measurements.

## House template law (overrides spec AND judge)

When a deck shares one outer template (founder directive), it is a hard rule — a
per-slide analysis, recreation brief, or judge finding that disagrees about these
elements is overridden, never a fix trigger:

- Slide size `LAYOUT_WIDE` 13.33 × 7.5 in; background `E8E8E8` (no `#`).
- Outer frame rectangle: `x:0.15, y:0.15, w:13.03, h:7.2`, line `C00000` 1.5pt, no fill.
- Slide-number badge: yellow circle `x:12.48, y:0.30, w:0.5, h:0.5` (fill+line
  `FFF9C4`), bold 18pt centered numeral, color `333333`.
- Title text box: `y:0.28`, `x:0.6`, `w:12.13`, centered. An intentionally empty
  title (`[No title ...]` in the spec) is conformant.

**Badge numeral = the number printed on the ORIGINAL slide image** — in a curated deck
the slide file is named by that printed number, so the badge reads exactly `N`
(unpadded). A badge not matching the original's printed number is WRONG even if a
judge never complained. Accept computed widths (e.g. `w: W - 0.3`).

## Copy-then-modify discipline

- Never edit a certified build in place: `cp build/slide_NNN.js
  build/slide_NNN_<variant>.js` and modify only the copy.
- Before ANY change, bank the current state: `cp build/slide_NNN.js
  qa/slideNNN/build_pre_<change>.js`. Every attempt keeps `build_attempt_K.js`,
  `render_K.png`, `probe_K.txt`, `judge_prompt_K.txt`, `judge_attempt_K.txt`.
- Never delete banked evidence, including old-numbered builds from previous curations.

## Cheap self-checks (corroboration only)

PIL color sampling at known coordinates, text-fit sanity, ink-edge measurement —
useful before spending a vision call, but they NEVER substitute for the visual judge.
The closed-loop ink-edge check (equations.md) is mandatory; the judge alone is not.
