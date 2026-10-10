# Equations — professional 2D format, alignment law, OMML dual-representation

Founder rule (binding): any equation on a recreated slide is rendered in **Professional
Format (2D / non-linear)** — never linear/typed notation:

- **Fractions**: stacked with a horizontal fraction bar — never inline `a/b`.
- **Summation `∑`**: large glyph with limits above/below (or stacked to the right,
  matching how the ORIGINAL shows them) — never `sum from i=1 to n`.
- **Sub/superscripts**: spatially aligned with math-font spacing — never `x^2`/`x_1`
  text or Unicode look-alike approximations.

The equation's CONTENT stays verbatim from the spec; only the rendering is 2D.

## Certified mechanism: matplotlib mathtext → PNG → addImage

1. Render: `python3 <skill>/render_eq.py '<mathtext>' <out.png> <fontsize_pt> '<hex>'`
   (skill-local copies in this skill's `scripts/`: `render_eq.py` = base certified
   helper; `render_eq_wide.py` = overlap-guarded variant for wide equations;
   `render_eq_stix.py` = STIX-serif `\dfrac` variant for full-size stacked fractions.
   Originals banked under the deck's `qa/math/`, `qa/slide042/`,
   `qa/slide054/` — copies, never replacements) — 600 dpi, tight bbox, transparent
   background; prints a JSON sidecar with exact pixel w/h and `baseline_frac`.
2. Embed at EXACT size: `w = px/600` inches, `h = py/600` — NEVER rescale (blurs
   glyphs). Size and color are baked at render time.
3. PNG only (never SVG). Mathtext is a LaTeX subset; DejaVu math look is acceptable
   (vision-validated). STIX serif is available when matching a serif original.
4. Bank every generated PNG + sidecar (e.g. `build/assets/eq_NNN_*.png/json`); never
   delete them.

### render_eq.py failure modes (measured)

- **Wide expressions (>~7in ink) get their LEFT edge silently clipped** — the baseline
  probe collides with the left tail. Use the overlap-guarded wide variant
  (`qa/slide042/render_eq_wide.py` pattern) for wide equations.
- **`\frac` renders numerator/denominator at SCRIPT size** (~10pt when the line is
  14pt) and compresses the stack — if the original shows full-size stacked operands,
  use `\dfrac` and/or a serif font (STIX), re-rendered at the size that matches the
  original's measured stack height (slide-54 fix: 24.7pt stack → 43.7pt vs original
  42pt).

## EQUATION ALIGNMENT LAW (founder feedback — overrides a judge PASS)

Placement defects (horizontal/vertical) are fix triggers EVEN WHEN THE JUDGE PASSED.
Original geometry wins; the recreation adapts (shrink/shift the bullet column if
needed — but verify a collision actually exists before deviating: one worker shifted
equations +73px right "to avoid collision" that PIL measurement proved nonexistent).

- **Vertical**: put the image's math BASELINE on the text baseline:
  `y_image = target_baseline_in − baseline_frac × h_image_in`.
  "Center the image on the line" (`lineY − h/2`) is WRONG for anything taller than
  the line.
- **Horizontal**: PIL-measure the equation's ink LEFT EDGE in the original frame
  (1px = 1pt) and match it, accounting for the PNG's tight-bbox inset (~8px/600dpi).
  Beware font-width differences: DejaVu is wider than some originals, shifting the
  bar position inside a boxed equation — re-render, don't just nudge.
- **Closed-loop verification (mandatory before judging)**: render, then PIL-compare
  the equation's ink band in the 150dpi render against the original's measured region
  (scale ×2000/960): top/bottom/left/right ink edges within ~4px. Iterate placement
  until within tolerance. Residual glyph-metric differences (a mathtext superscript
  sitting ~2pt higher, a radical descending less) are inherent — document them, don't
  chase them by breaking the baseline law.

## OMML dual-representation (post-certification pass, wrapper v2 + single-version naming)

Raw OMML in a PPTX does NOT render in LibreOffice headless (it shows the linear
fallback — measured; OnlyOffice/Aspose/Gotenberg are no better). The validated
solution keeps the certified PNG pixels and adds editable PowerPoint equations:

- `scripts/18_omml_wrapper.py <input.pptx> <manifest.json> [-o out.pptx]` wraps each
  equation `<p:pic>` in `mc:AlternateContent`: `mc:Choice Requires="a14"` → real OMML,
  `mc:Fallback` → the original PNG pic verbatim.
- **Wrapper v2 (2026-10-10, founder-reported fix): the Choice must carry the
  PowerPoint-AUTHORED pattern** — v1 emitted `a:p > a14:m > bare m:oMath` (the
  LibreOffice-writer pattern): PowerPoint honored the Choice and rendered NOTHING
  (equations invisible on the wrapped slides). v2 emits
  `a:pPr(algn=ctr+buNone) + a14:m > m:oMathPara(jc=centerGroup) > m:oMath + endParaRPr`,
  Cambria Math typeface + `i`/`smtClean="0"` on every run, `m:ctrlPr` in every
  construct, Choice shape id = the Fallback pic's id, zero-inset `bodyPr
  anchor=ctr noAutofit` pinned to the pic frame. Proven by mirroring a real
  PowerPoint-authored sample (`qa/omml_v2/research/real_office_sample/`) — see
  `qa/omml_v2/OMML_V2_REPORT.md`.
- LibreOffice render is pixel-identical (validated 0/2.25M px per wrapped slide);
  PowerPoint shows editable native equations. No re-judge needed.
- Manifest per slide: `{"slides":[{"slide":1,"equations":[{"rel_id":"rId1","image":
  "eq.png","mathtext":"...","font_size_pt":22.0,"color":"#C00000"}]}]}` — values come
  straight from the render sidecars; `rel_id` is RE-DERIVED from the actual pptx rels
  after any rebuild (never assume it survives).
- Rules: apply ONLY after visual certification; apply to the slide's own pptx (the
  single plain-named deliverable — no `_omml.pptx` variants per the single-version
  law); verify 0-pixel-diff before accepting; **never LibreOffice-resave a wrapped
  deck** (the LO writer drops OMML it never understood).
- Converter supports m:f, m:rad, m:nary (∑∏∫; `undOvr` or right-stacked `subSup`
  limits), m:sSub/sSup/sSubSup, m:bar, m:acc, m:d, Greek + operators, `\text`,
  `\mathbb{}` (double-struck ℝ/𝕀), `\dfrac`/`\tfrac`, `\Vert`, `\mathbf`, `\vdots`,
  the `x{}_1` empty-group idiom; anything else fails loud — never hand-patch OMML.
  Mathtext provenance: sidecars don't carry the mathtext string — take it from the
  slide's math report, then RE-RENDER it with the slide's exact helper and PIL-verify
  0 pixel diff vs the banked PNG before wrapping (the OMML must provably match the
  fallback image).

## Renderer verdicts (researched, don't re-derive)

No better headless Linux PPTX renderer exists than LibreOffice: OnlyOffice drops OMML
and is HTTP-only; WPS/Calligra have no headless CLI; Gotenberg is LO-in-Docker; Aspose
watermarks, costs ~$999, and renders the image fallback anyway; PowerPoint COM is
Windows-only. A LibreOffice extension cannot fix equation rendering for headless
convert-to-pdf. LO itself saves equations as the same AlternateContent pattern the
wrapper emits — which is why the wrapper mirrors it.
