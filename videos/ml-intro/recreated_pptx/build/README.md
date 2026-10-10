# Build directory — final builds only (founder directive 2026-10-10)

One build script per slide; one pptx per slide named `../slide_NNN_recreated.pptx`
(single-version law: graphs + OMML baked in, no suffixed variants).

## Per-slide rebuild

```bash
cd /home/ahmed/Projects/ai_llm_slides
NODE_PATH=$(npm root -g) node videos/ml-intro/recreated_pptx/build/slide_NNN.js
# -> videos/ml-intro/recreated_pptx/slide_NNN_recreated.pptx
```

- Slides 15–19, 35, 43–51, 57, 63, 64 embed their AI-generated graph images from
  `assets/graphs/` (relocated from the QA evidence dirs when qa/ was removed).
- Slides 53/54 additionally call `gen_parens53.py` / `gen_parens54.py` (certified
  Bézier delimiters) and slide 54's serif equations render via
  `scripts/render_eq_stix.py`.
- Equation PNGs + sidecars: `assets/eq_*.png|json` (certified; never rescale —
  embed at `w = px/600`).

## Equation slides (26, 42, 52, 54, 55) — dual representation

The delivered pptx is the WRAPPED deck (PowerPoint-editable OMML + certified PNG
fallback). Rebuild chain:

```bash
NODE_PATH=$(npm root -g) node videos/ml-intro/recreated_pptx/build/omml/slide_NNN/base_build.js
python3 videos/ml-intro/recreated_pptx/build/omml_wrapper.py \
  videos/ml-intro/recreated_pptx/slide_NNN_recreated.pptx \
  videos/ml-intro/recreated_pptx/build/omml/slide_NNN/omml_manifest.json
# wrapper v2 = PowerPoint-authored Choice pattern; LO render must stay 0-px identical
```

## Final combined deck

```bash
python3 videos/ml-intro/recreated_pptx/build/build_ml-intro_final.py \
  videos/ml-intro/recreated_pptx videos/ml-intro/recreated_pptx/ml-intro_final.pptx
# byte-verbatim OPC merge (canonical copy: scripts/19_build_final_deck.py);
# gate: render merged deck + all 64 sources in one soffice session, PIL pixel-diff
# page N vs source N -> 0/64 mismatches required (reference render:
# videos/ml-intro/ml-intro_final_render_certified.pdf)
```

## Data dependencies (outside this dir)

- `videos/ml-intro/datasets/iris.csv` — canonical IRIS (slide 62 table + PCA graphs);
  never hardcode rows.
- `videos/ml-intro/unique_slides/slide_NNN.jpg` — originals (some builds reference
  them for measurement comments only).
