# Graphs — AI-algorithm-generated chart images, single-version rule

Founder rules: slides whose originals contain advanced graphs (3-D scatters, PCA
projections, learned-model plots, decision regions — anything native pptxgenjs shapes
can only approximate) get a **properly GENERATED graph image**:

- **Single version per slide (founder directive 2026-10-10, supersedes the old
  two-version rule):** the deliverable is ONE pptx per slide named
  `slide_NNN_recreated.pptx` — NO `_graphed`/`_omml` suffixes. A graph slide's own pptx
  HAS the generated graph embedded (the native-shapes approximation is replaced by the
  image in the same build; superseded builds live only in QA evidence dirs).
- Images are produced by the **correct Python library for the slide's topic** running
  the **same AI algorithm on real data** — not hand-drawn dot approximations:
  - PCA slide → `sklearn.decomposition.PCA` on the canonical IRIS file
    (`videos/ml-intro/datasets/iris.csv` == sklearn `load_iris`; never hardcode rows);
  - KNN decision regions → `sklearn.neighbors.KNeighborsClassifier(K=...)` fitted on
    measured training points, prediction over a meshgrid;
  - polynomial overfit/underfit curves → `numpy.polyfit` at the original's degrees on
    the measured training points.
- Library/function/algorithm/data are chosen **per slide**; web research through
  `agy -p "<query>"`.
- Tooling: a dedicated venv subproject (`graphgen/` — `.venv`, pinned requirements).
  Run generation with `graphgen/.venv/bin/python`.

## Workflow per slide (validated pilot: slide 64)

1. **Triage the original**: PIL-measure the graph region (frame, axes, palette, point
   positions). Reused vector art across slides is common in course decks — slides
   43–47 shared one 26-point NN scene, 48/49 and 50/51 shared two more; extract the
   canonical point list ONCE and reuse it across the family (drift ≤2px in practice).
2. **Generate** the image matched to the original's measured region/colors
   (960×540, 1px=1pt). Bank script + PNGs under `qa/slideNNN/graphgen/`.
3. **Closed-loop alignment** (same law as equations): PIL ink-edge match vs the
   original's measured placement within ~4px at 150dpi BEFORE any vision call.
4. **Graph vision leg**: comparison of the generated graph vs the original frame
   through the vision gate (default route, wide wall, scoped to the graph region ONLY
   — house chrome/badges/titles out of scope), ending "FINAL VERDICT: PASS or FAIL for
   'faithful, usable graph match'". Fix loop per the judging law.
5. **Embed**: modify the slide's own build (`build/slide_NNN.js`) — native
   approximation → `addImage` at the measured region; house frame, badge, and ALL text
   unchanged; build `slide_NNN_recreated.pptx` (the single plain-named deliverable);
   render.
6. **Slide judge leg**: full judge comparison of the render vs the original
   with the mandatory ground-rules template. PASS from a winner body only.

## Pilot lessons (paid for — do not relearn)

- **Bake region borders INTO the generated image** rather than drawing pptx shape
  borders on top — overlay misalignment is a defect class of its own.
- Keep superseded builds banked in the QA evidence dir (per-attempt provenance), never
  as parallel deliverables.
- Validate with PIL masks (region shape, palette presence) before spending a vision
  call on the graph leg.
- Match the original's axis tick ranges exactly — e.g. a PCA slide whose spec ranges
  match unscaled-IRIS PCA confirms the dataset choice.
- An "optional" graph slide whose original graph is decorative may be skipped — record
  the skip decision explicitly rather than leaving it ambiguous.
