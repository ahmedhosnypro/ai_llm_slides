# Worker report — slide 012 (Attention Is All You Need, arXiv 1706.03762v5 page-1 screenshot)

Video: `videos/deep-learning/001_transformers_part1` · Slide id 12 (NNN=012) · Attempts used: **1 of 6**
Final verdict: **PASS** (real comparison transcript) · DB: `gen_status=passed`, `visual_check=PASS`, `visual_attempts=1`

## Deliverable

- PPTX (single-version law, no suffix): `videos/deep-learning/001_transformers_part1/recreated_pptx/slide_012_recreated.pptx` (343 KB)
- Build script: `videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_012.js` (banked copy: `qa/slide012/build_attempt_1.js`)
- Asset: `recreated_pptx/build/assets/slide012_page1.png` (2432×1657)

## Build strategy (and why)

The slide IS a screenshot of the paper's first page; per `001_transformers_part1/AGENTS.md`
and `slide_012_source/SOURCES.md` the founder-banked v5 artifacts
(`slide_012_source/1706.03762v5.pdf` + page-1 PNG) are the declared reference-grade ground
truth for exactly this content (same precedent as the certified figure-family slide 014,
which embeds the founder-downloaded paper images). The build therefore:

1. Rendered the banked v5 PDF page 1 at 300 dpi (`pdftoppm`).
2. Fit the frame↔page mapping by least squares over 11 landmarks (title, rule, 3 author
   rows, Abstract heading, abstract lines): `s_x=0.28909 ox=97.13`, `s_y=0.28480 oy=-60.52`
   (max residual 1.7 px) — the original screenshot is slightly anisotropic.
3. Cropped the raster to exactly the frame's visible window (page x[-13,2419] y[397,2054],
   13 px white pad left). The crop reproduces the original's own crop artifacts by
   construction: rotated stamp loses its leading "arXiv:1", abstract cut mid-sentence
   ("…training costs of the") at the container bottom, running header excluded.
4. Baked the instructor markup into the raster with the measured alpha compositing
   (identical math to the renderer): tan title box + tan stamp-date band
   (α=0.30 over fill (235,124,0)) and 6 pink affiliation boxes (α=0.52 over (226,86,230)).
   The parameters reproduce ALL measured anchors: white→(249,215,178), black title
   glyph→(63,28,0), gray stamp glyph→(165,132,94) — all within 1–5 of the frame's samples.
   Highlight rects are the profile-measured frame rects (title x[336,599] y[54,84];
   pink1 y[171,185] ×4; pink2 y[231,245] ×2; date band x[97.5,137] y[184,312]).
5. Drew as shapes only: the playlist house chrome via the shared
   `videos/deep-learning/shared_patterns/house_chrome.js` module (`drawHouseChrome`,
   numeral 12) and the container's thin red border (rect x[93.5,796.5] y[52.5,524.5] px,
   2pt C00000, transparent fill). Mouse cursor(s) in the frame are capture artifacts —
   omitted per judge ground rule (c). No text boxes (all text is the certified raster —
   verbatim by construction), so the explicit-lineSpacing law is trivially satisfied.

## Evidence chain (attempt 1)

| Check | Result | Evidence |
|---|---|---|
| house_chrome_check.py (mandatory) | **PASS** | "panel x 89-1913, y 95-bottom; badge center (1860,148) d=70; all within tol 8" |
| Pre-judge self-check (17 checks: chrome, container border, containment, margins, highlight interiors, watermark ink, 12-line abstract pitch 12.95 vs 12.9 frame px) | **PASS** | `qa/slide012/selfcheck_attempt_1.py` + `selfcheck_attempt_1_out.txt` |
| Dense crop: author block (×4.16 zoom, full judge params) | **PASS** | `qa/slide012/crops/cropcmp_authors.txt` — all 7 blocks verbatim, 6 pink boxes, Toronto unhighlighted; MINOR box-width nuances only |
| Dense crop: rotated arXiv stamp + tan date band (×5 zoom) | **PASS** | `qa/slide012/crops/cropcmp_watermark.txt` — stamp verbatim, designed crop in both; MINOR date-centering nuance |
| Dense crop: abstract block (×4.16 zoom) | **PASS** | `qa/slide012/crops/cropcmp_abstract.txt` — 12 lines verbatim, identical breaks/hyphenation, pitch ~12.9 both; MINOR rule-weight note |
| **Full-slide judge comparison** (`--thinking high --max-tokens 65536`, default route) | **PASS — FINAL VERDICT: PASS** | `qa/slide012/judge_attempt_1.txt` — "No BLOCKER or MAJOR defects"; MINOR: title-banner width proportion (medium conf), inter-row gaps ~5% (low), abstract font touch larger (low) |

Judge MINOR rebuttal note: "title banner proportionally slightly narrower" is contradicted
by the pixel measurement — the baked banner rect IS the frame-measured rect
(x[336,599] vs frame cluster x[334,599]); the delta is JPEG edge bleed in the original.
Per the dense-region pattern law ("a claim contradicted by ~1px centers is a rebuttal,
not a fix trigger") this is documented, not fixed. The other two MINORs are explicitly
within-tolerance cosmetic notes at low confidence.

## Gateway conditions encountered

- The probe (short wall, per law) hung 3× (EXIT=124; the first two with a wall-racing
  wrapper produced no transcript, the third logged `ABORT HangError @150s` — fleet
  congestion from ~6 concurrent slide workers, not a dead route; gateway answered 401
  on unauth liveness probes throughout).
- Per §R pacing, dispatch moved to the mandated wide-wall crop comparisons
  (1650/600), which landed in ~1 min each — the window was open at wide walls.
  The judge comparison (540/420) then landed on first dispatch.
- Certificate labeling: **single-read** full-slide judge, default route (images, no
  --models), glm leg DEFERRED/BLOCKED; corroborated by 3 dense-region crop PASSes.
- **Judge procedure executed by the worker** (documented 17 §7 self-execution
  fallback — no Agent/Task spawn tool in this environment); prompts banked verbatim at
  `qa/slide012/judge_prompt_1.txt` + `qa/slide012/judge_p_body.txt` before dispatch.

## Transcripts and provenance

- `qa/slide012/judge_attempt_1.txt` — full-slide comparison (deciding verdict)
- `qa/slide012/crops/cropcmp_{authors,watermark,abstract}.txt` — dense-region crops
- `qa/slide012/crops/{authors,watermark,abstract}_{render,orig}.png` — crop pairs
- `qa/slide012/render_1.png` — 150dpi render (2001×1125)
- `qa/slide012/build_attempt_1.js`, `qa/slide012/judge_prompt_1.txt` — attempt-1 provenance
- Measurement scripts: `scratch/slide012/measure_frame*.py`, `measure_page.py`,
  `gen_asset*.py`; page raster `scratch/slide012/page300-01.png`

## Dependency status

Slide 12 is a ROOT with NO dependents in `slide_dependencies.json` — no component export
required. Nothing shared was modified; the shared `house_chrome.js` was imported, not edited.
