> NOTE 2026-10-10: qa/ evidence paths cited below were REMOVED at founder directive after program completion — the knowledge stands; the cited transcripts/renders no longer exist on disk.
# Confirmed-working patterns (reusable, mandatory checklist)

Every recreation MUST read this file first and reuse the patterns below instead of
improvising. A pattern lands here only after it is vision-certified working; when your
own fix confirms a NEW pattern, append it here (code + the measurement that proves it).

Legend: [CERTIFIED] = proven by a judge PASS + closed-loop checks. [PENDING] = being
confirmed by the current rework program — use, then confirm or amend.

## P1. House chrome [CERTIFIED]

pptxgenjs, LAYOUT_WIDE (W=13.33, H=7.5). Exact values — never deviate:

```js
// outer red frame
s.addShape(pptx.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
// slide-number badge (numeral = printed number on the ORIGINAL image = file id, no padding)
s.addShape(pptx.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText(String(N), { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0 });
// title box
s.addText(title, { x: 0.6, y: 0.28, w: 12.13, align: "center", ... });
```

## P2. Inner-frame budget (content must fit) [CERTIFIED for slides 5, 15, 62, 64-graphed, 2026-10-10]

An inner frame is a content container drawn as a rectangle; ALL its content must sit
inside with clearance. Budget rule: measure first, draw second.

1. PIL-measure the ORIGINAL frame's region in the 960x540 frame (1px=1pt): frame edges
   AND the ink bbox of the contained content.
2. Compute the content-to-frame margins on every side; your recreation must reproduce
   the frame at the original's geometry (or the spec's measured one) and keep ink inside.
3. Closed loop at 150 dpi: render → PIL ink bbox per frame region → assert
   `ink_top > frame_top`, `ink_bottom < frame_bottom`, same for left/right
   (scale 2000/960 between coordinate spaces; px = in × 150.075 in the 2001×1125 render).
4. If content genuinely needs more room than the frame gives, ENLARGE THE FRAME
   (increase h, move y up if the space above allows) and shift content up with it —
   never let ink cross the frame (founder fix directive for slide 5).

### Certified inner-frame fix pattern (slide 5, 2026-10-10 — judge PASS attempt 4)

Founder defect on the final deck: "Content overflows outside the inner frame" — seen in
POWERPOINT (the deck's consumption medium), while the 150dpi LO render of the SAME bytes
measured all ink inside the frame. Lesson: LO bare-fit containment is NOT containment in
PowerPoint (no text-box clipping + taller font line boxes on some systems). Budget for the
tallest plausible renderer, not for the one you measure with.

The fix (founder directive: "increase inner frame height and y start, move inner content
up as well"), with the house frame as the hard ceiling:

- OLD frame (render-verified): x 1.199–11.981in, y 1.906–7.256in (h 5.371in); content ink
  2.032–6.970in; clearances T 0.100 / B 0.280 / L 0.193 / R 0.913in — legal in LO, but
  only ~0.28in of bottom slack for a 12-row text block.
- NEW frame: y start 1.92 → 1.62in (raised 0.30in), h 5.35 → 5.65in; bottom edge
  UNCHANGED at 7.27in — the bottom is pinned by the house frame: its bottom stroke sits at
  7.35in and is untouchable chrome, so the height gain must come from the top (0.08in
  daylight kept between inner-frame bottom and house stroke).
- Content shifted RIGIDLY up by the same 0.30in (lead-in y 1.95→1.65, bullets
  2.77→2.47): preserves every certified internal margin and row pitch — all 14 text
  bands moved exactly 45px, pitch deltas identical to the prior PASS layout.
- Verified (selfcheck_attempt_4, banked in qa/slide005/): clearances T 0.100 / B 0.580 /
  L 0.193 / R 0.913in; ZERO ink on/beyond any inner-frame edge; zero ink between frame
  bottom and house-frame bottom stroke; judge PASS (updated GROUND RULES incl. FRAME
  CONTAINMENT clause): "All content sits within the inner red-bordered panel with
  comfortable margins; no ink touches or crosses any boundary."
- Founder-ordered geometry deviations from the original (original frame top 1.92in,
  fixed frame top 1.62in) are legitimate: the founder directive overrides the original's
  geometry, and the judge accepted the layout ("placement is equivalent").

### Certified graph-image containment + bottom-stack pattern (slide 64 graphed founder fix, 2026-10-10 — judge PASS attempt 5, `qa/slide064/graphgen/`)

When a NATIVE plot is replaced by a full-region IMAGE placed at the ORIGINAL's measured
geometry, re-verify EVERY surrounding frame against the image's ink — the base build's
frames were tuned to the native plot's smaller extent. Slide 64: graph image at x3.208
y1.278 w6.778 h5.569 (baked panel border ink to 6.854in) silently CROSSED the
base-inherited main frame bottom (6.60in), and the caption box (top 6.80in) MASKED the
crossing — z-order masking that per-element bbox checks cannot see; judge attempt 4 FAIL
("the inner frame's bottom red line disappears behind the caption box").

- Fix (P2 "enlarge the frame" law): main frame h 5.42→5.75 (bottom edge 6.93in — 13
  render-px below the panel border ink, 8 px above the caption top); caption box
  y 6.80→6.99, h 0.46→0.32 (top = the ORIGINAL's caption top 503px EXACTLY, preserving
  its 10px gap below the panel; bottom 7.31in keeps 5px daylight to the house stroke
  at 7.34in).
- The original's caption-INSIDE-frame stack (panel 493 → caption 503..533 → frame
  bottom ~538 → slide edge 540) is UNREPRODUCIBLE under the house frame stroke
  (7.34..7.36in): house chrome wins. Place the frame bottom BETWEEN panel and caption,
  keep every adjacent-pair gap ≥5 render-px, and never let an element serve as a mask.
- PowerPoint-pitch interaction: an 18pt caption line needs ~0.30in (1.2×font) of box
  height in PowerPoint; h=0.32 holds it. NEVER compress a text-bearing box below the
  1.2×fontSize line pitch to "gain" frame room — that trades a LO PASS for a
  PowerPoint overflow.
- Closed loop (`bottomstack_check.py` + `selfcheck.py`, banked in `qa/slide064/graphgen/`):
  assert vertical order + gaps panel-ink < frame-line < caption-top < caption-bottom <
  house-stroke, nothing crossing the frame line outside its extent, caption text
  inside its box — PLUS gap-band assertions (the x226..229px-orig band between the
  PCA box right border and the image left edge must be 0 non-bg px). Gap bands are how
  you catch z-order masking; bbox containment alone does not.

### Certified inner-frame re-fit for a graph-image panel (slide 15 graphed, 2026-10-10 — judge PASS attempt 3, `qa/slide015/graphgen/`)

Founder defect on the final deck: "The bottom left graph box is overflowing outside the
inner frame, fix it the same way [as slide 5]". Root cause measured: the recreation's
inner frame bottom (7.10in) sat ABOVE the original's measured frame bottom (7.258in)
while the embedded graph image sat at the original's exact position (panel bottom
7.157in) → panel ink crossed the frame line by 7 render-px (~4 orig-px). A frame that is
SHORTER than the original's cannot contain content placed at the original's geometry.

The fix (founder recipe verbatim: frame height up + y start up + content up):

- Frame: y 1.68 → 1.58 (start UP 0.10in), h 5.42 → 5.68 (UP 0.26in), bottom 7.10 →
  7.26in == the ORIGINAL's measured frame-rect bottom (522.5/72 = 7.258in, 1px=1pt).
  Unlike slide 5 (bottom pinned by the house stroke, gain from the top only), slide 15
  had 0.25in of daylight between old bottom and house stroke — so the height gain came
  from BOTH ends and the new bottom REPRODUCES the original's own containment geometry
  (original panel-to-frame margin 7.2 orig-px = 0.100in).
- Content: panel image moved UP 0.05in (y 5.044 → 4.994; bottom 7.107in), giving
  22 render-px = 0.147in = 10.6 orig-px clearance ≥ the original's 7.2px margin.
  Image asset unchanged (same algorithm/data — only placement moved).
- Verified (selfcheck_graphed_attempt_3.py, ALL 32 CHECKS PASSED): frame edges at build
  values; zero content ink outside/below/left/right of the inner frame; graph closed
  loop intact (border ≤1.35px, green trace mean 0.59/max 2.02px, 22/22 circles ≤2.0px);
  judge PASS attempt 3 — attempt-2 judge had already confirmed "no containment defect;
  no ink crosses any boundary" for the re-fit itself.
- Companion lesson (this fix's second act): a founder-fix judge PASS can still FAIL on
  elements the fix UNCOVERED attention on — here the inherited classification
  mini-plots (left MAJOR, right MINOR). Fix judge-flagged diagram geometry by MEASURING
  the original (5 dots + 5 X's per plot at per-component centroids; left separator a
  single steep straight segment, normalized trace (0.217,0.838)→(0.472,0.119) slope
  −2.8; right boundary a smooth two-armed arc sampled per-column, drawn as ~25 short
  seg() calls), then closed-loop the re-fit against those measured normalized targets
  (slope −2.81 measured in render, endpoint err 0.007; all markers ≤0.2× tolerance;
  teaching geometry asserted: every dot left of the separator, every X right of it).

## P3. Multi-line delimiters (parens/brackets across N lines) [CERTIFIED for 63 + 64 graphed + 54 Bézier adoption, 2026-10-10 — 53 PENDING]

Delimiters enclosing a multi-line block must span ALL enclosed lines with clearance.
Pattern: draw each delimiter as a TEXT GLYPH (Arial "(") in its own box vertically sized
to the full block, or a shape whose extent is measured from the block:

1. PIL-measure the enclosed block in the original: topmost ink line, bottommost ink
   line, and the horizontal position of each delimiter stroke.
2. Delimiter vertical extent = [topmost_line_top - pad, bottommost_line_bottom + pad]
   — it must cover every line, and its stroke must not overlap the enclosed text
   (keep the original's stroke-to-text gap).
3. Closed loop: measure delimiter ink extent in the render vs computed extent (~4px
   tolerance at 150 dpi), and assert no enclosed-text ink lies within the delimiter
   stroke columns.
4. NEVER compose multi-line parens from per-line glyph parens stacked by the text
   engine (this produced the slide-53 "inner curve top+bottom" garbage and the
   slide-53 founder defect) — a delimiter spanning N lines is one glyph/shape sized
   to N lines, not N line-height glyphs.

### Certified spanning-ARC construction (slide 63 founder fix, 2026-10-10 — judge PASS attempt 5 + crop-comparison PASS, `qa/slide63/graphgen/`)

For delimiters that must look like TALL NEAR-STRAIGHT strokes (a "(" text glyph at
100+ pt renders a huge round bowl), use ONE ARC shape per side, a HALF TURN each:
`angleRange: [90, 270]` for "(" / `[270, 450]` for ")", `h` = the original's measured
paren ink extent, `w` = 2–4 orig-px (the tip curl), bbox `x` placed so the stroke
BULGE (bbox outer edge) lands on the original's measured stroke columns (the tips sit
at the bbox's horizontal center); `fill: {transparency: 100}`, `line: {width: 2.25,
color: measured stroke gray ~B3B3B3}`. NEVER partial-sweep fat-ellipse arcs
(`[135,225]`/`[315,405]`, wide bbox): OOXML draws only the middle ~52% of the bbox
height for those sweeps and the elliptical curvature swings the tips ~19 px inward
onto the text — exactly the slide-63 founder defect ("not expanding across the 4
lines… over the text between them"), confirmed DEFECT PRESENT by zoomed crop
comparison (`cropcheck_defect_vs_original.txt`).

Slide-63 measured inputs (orig 960×540, 1px=1pt): LEFT vector (W₁ L₁ W₂ L₂) parens
ink y 147..252, strokes x 77..81 / 109..113, lines 154..244; RIGHT vector (Z₁ Z₂)
parens y 173..227, strokes 189..193 / 215..219, lines 180..218. Closed loop at
150 dpi (`selfcheck_attempt_5.py`): extents 146.4..252.0 / 172.3..227.0, per-line
stroke-to-text gaps 4.3..10.6 px, coverage pads ≥ 5 px.

Two adjudication riders (both bit us on 63):

- **Ink-role colors come from the ORIGINAL's pixels, not the spec's prose.** The ×3
  crop comparison caught what two 1× full-slide judges PASSed: the original's LEFT
  vector is ALL-BLUE ink (main letters darkest-40% median B−R +87 on all 4 lines —
  the spec said only "blue subscripts"), the RIGHT vector all-neutral (letters −1,
  subscripts −2), parens neutral gray (a +18..+24 B−R read on the left-side strokes
  was JPEG blue bleed — the far-side control stroke measured ~0). Test per glyph:
  darkest-40%-median chroma vs a far-side control, then apply per-vector main/sub
  colors (`color_adjudication*.txt`).
- **A superscript glyph inside the stroke-column set pollutes extent measurement.**
  Exclude it by a COLUMN ceiling (< the foreign glyph's box left edge), never a row
  band — the arc's own tip rows must stay in the union. And if the original shows NO
  ink for the superscript at any threshold (63's T: 0 dark AND 0 faint px at both
  suspected positions — earlier forensics had misread the paren tips as "T"), keep
  the spec's ᵀ for content verbatim but never "move it to the original's T" from a
  smudge; there is no ground truth to move it to.

### Certified stretched-GLYPH-PNG construction (slide 64 graphed founder fix, 2026-10-10 — judge PASS attempt 5 + 3/3 region crop comparisons MATCH, `qa/slide064/graphgen/`)

Alternative to the P3 arc for near-straight video parens: render the "(" / ")" text
glyph ONCE huge (Liberation Sans Bold, font size 1000), tight-crop the ink, anisotropic
LANCZOS-resize to (stroke-width px × target-span px) at 600 dpi, recolor via the alpha
channel (gray→alpha composited over the measured ink color), save transparent PNG, then
`addImage` at EXACT px/600 size — w = 21/600 = 0.035in (2.5 orig-px stroke), h = px/600
(never rescale horizontally; a vertical-only stretch keeps the hairline hairline).
Verified end-to-end: judge attempt 5 — "Delimiters on the equation span all four rows
correctly"; all 3 post-fix region crop comparisons MATCH (`region_postfix_{a,b,c}.txt`).

- Slide-64 measured inputs (orig 960×540, 1px=1pt): W/L (W₁ L₁ W₂ L₂) parens ink
  x78..80 y148..253 (left) / x110..112 y149..252 (right), blue 0000CC; Z (Z₁ Z₂ Z₃)
  parens x190..192 y162..239 (left) / x216..218 y161..238 (right), black. Asserted
  0 text-ink px inside the stroke columns (stroke-to-text clearance per P3).
- SIZE PARENS TO THE SUBSCRIPT DESCENDER, not the letter band: the last line's
  subscript (Z₃'s ₃) hangs ~1.5 orig-px BELOW the letters — a paren sized to the
  measured letter band leaves the descender poking out past the paren tip (caught in
  calibration; +2px span on the left paren fixed it).
- Pin `lineSpacing` explicitly on the enclosed multi-line column (PowerPoint pitch
  law): 26pt = the original's band pitch → measured render pitch 54.0..54.5px at
  150dpi vs the 54.2 (26pt) target. Assert pitch AND "paren ink covers the
  bottom-most INK row of the block".
- Self-check pitfalls that produced FALSE FAILs before the build was actually wrong
  (fix the check, not the build): (a) color masks need AA-loose bounds (blue:
  b>r+40 & b>90; dark: <130 on all channels) or 2.5px hairline strokes vanish
  entirely; (b) a superscript T inside the paren-column band pollutes extent groups
  and bbox deltas — exclude it by its own row/col band, not by eyeballing groups;
  (c) a full-region IMAGE bakes its own borders — exclude those columns from
  frame-border scans; (d) row cuts are directional — `mask[y0:,:]=False` zeroes
  BELOW y0, `mask[:y1,:]=False` zeroes ABOVE y1 (an inverted title-exclusion cut
  zeroed the whole vector block once).

### Certified quadratic-Bézier-PNG construction (slide 054 founder fix "not aligned / gaps bad", 2026-10-10 — judge PASS attempt 6 + att9 crop re-verify, `qa/slide054/`)

The slide-053 certified construction, adopted VERBATIM per the 2026-10-10 coordinator
directive ("reuse slide 53's construction; do not invent a third variant for this
defect class"). Each delimiter = ONE smooth quadratic-Bézier centerline stroke
rasterized at 600 dpi with linewidth S on a transparent canvas, tight-cropped, sidecar
JSON stores the ink bbox, `addImage` at EXACT size (w = px/600 in, never rescaled).
Anchors: side "lp" lands the ink LEFT edge (= stroke bulge outer edge) on the measured
stroke column; "rp" lands the ink RIGHT edge; y so ink_top = measured block top.
Stroke depth beyond the bulge D=2.5pt, PAD=0.5pt; full ink span (bulge edge to tip
edge) = S+D+AA ≈ 4.92 (S=2.5) / 5.42 (S=3.0) / 5.88 (S=3.5). NEVER font-glyph tall
parens, NEVER ARC presets (LO renders ARC presets as double strokes with merged caps
— the 053 founder screenshot defect).

- Slide-054 measured inputs (orig 960×540, 1px=1pt): feature parens ink y215-263
  (h 48) S=2.5 in class colors (CC0000/0000CC/2E8B22) per column; norm red y324-359
  (35) / norm blue y324-361 (37) / norm green y328-363 (35), S=2.5; test y328-372
  (44.5) S=3.0 black; Mean y217-259 (42.5) / S.D y216-259 (43) S=2.5 FAINT GRAY
  B3B3B3; conclusion y446-503 (57) S=3.5 black — geometry identical to 053's
  certified callout so its PNGs are REUSED (`assets/parens53`). Generator:
  `build/gen_parens54.py` (per-class CLASSES entries carry S, inkH, color).
- **INK-STRENGTH HIERARCHY LAW (054):** in the original frame, SOLID strokes ≥~2pt
  survive video/JPEG encoding dark — same-frame controls: Mean digit '8' core lum 57,
  S.D '4' 43, test paren 48, conclusion paren 32. A stroke whose window contains
  ZERO sub-170-lum pixels was genuinely FAINT paint in the source, NOT JPEG erosion
  (the 054 Mean/S.D parens: darkest lum 155-181, neutral gray, zero sub-170 px).
  Adjudicate every "stroke too light/heavy" vision claim against same-frame control
  digits before touching the build. Per-class measured COLOR is a legitimate
  parameter of this construction: the 054 Mean/S.D parens paint B3B3B3 (lum 179,
  inside the original's 155-181 band) while the enclosed digits stay solid black;
  sidecar geometry is byte-identical between colors, so recoloring = zero
  repositioning risk (render diff confined to the 4 strokes, 2345 px at 150 dpi).
- **Faint-paint-extends trap:** a faint stroke's VISIBLE extent is shorter than its
  true extent (JPEG erodes faint tips). Before believing a "paren too short" claim,
  rescan the original at looser thresholds (lum<225): the 054 faint Mean/S.D paint
  extends to the full measured band — the heights were a refuted claim.
- **Vision flip-flop on identical pixels needs PIL:** att8 C1 read the content
  border "same hue within tolerance; thickness matches"; att9 C1 read the SAME
  pixels "2-3× too thick, too saturated bright red vs dark maroon-brown". PIL
  settles it: original border core (144,56,68) == same-frame red digit cores
  (138,53,74)/(164,45,64) → same CC0000-class paint degraded uniformly by the
  video JPEG; original loose-ink band 5.0pt ≥ render's crisp 3.4pt (the claim is
  inverted). Never fix from a single vision reading that a prior round
  contradicted — banked transcripts are the control.
- **Threshold-geometry trap:** comparing ink px-counts between a 1px=1pt JPEG and
  a 150dpi render at the same lum threshold is invalid (AA profiles differ by
  scale). Use luminance transects at native resolution + coverage reasoning
  (paint vs blur); convert px→pt with the calibrated scale (÷ax), never PX() on
  counts.
- **Text-free measurement bands:** measure stroke waist in the inter-line gap band
  (line-1 cap-bottom+AA → line-2 ink-top) and stroke spans in tip bands clear of
  enclosed text — digit AA fringe can reach ~1.5pt below the cap-bottom and
  pollutes tighter windows.
- **Empirical mixed-face font matching (054 alignment law):** when the original is
  a mixed serif/sans slide, match per element from ink metrics (advance widths,
  cap heights, line pitch), not per box: 054 = Times New Roman for feature
  values 22 / norm values 15.5-16.5 / test 17 / triplets 17 / conclusion 20 /
  row labels 13 bold / section label 25.5; Arial for FT/NT headers 15 bold,
  Mean/S.D values 16, sq-dist 16 bold, "Belongs to" 13 bold+charSpacing 1.7.
  Box-top→cap-ink-top offsets: TOFF(sans)=0.25·fs, TOFFS(serif)=0.29·fs. Zero
  multi-line text boxes — one absolutely-positioned box per line (also satisfies
  the explicit-lineSpacing law). U+2212 minus via a glyph-mapping helper.


## P4. Equations (matplotlib mathtext → PNG → addImage) [CERTIFIED]

1. `python3 scripts/render_eq.py '<mathtext>' out.png <pt> '<hex>'`
   (600 dpi, transparent, sidecar JSON with px w/h + baseline_frac). Bank PNGs under
   `build/assets/eq_<slide>_<name>.png` + sidecars; never delete.
2. Embed at EXACT size `w = px/600` in — never rescale.
3. ALIGNMENT LAW: `y_image = target_baseline_in − baseline_frac × h_image_in`;
   horizontal from the ORIGINAL's PIL-measured ink left edge; closed-loop 150 dpi
   ink-edge check within ~4px before judging.
4. Wide equations clip → `render_eq_wide.py`; serif originals → `render_eq_stix.py`.
5. `\frac` renders script-size → `\dfrac` for display-size.
6. Dual representation: wrap post-certification with `scripts/18_omml_wrapper.py`
   (mc:Choice OMML + mc:Fallback = the certified PNG). PowerPoint-native equation
   markup pattern: see P9 [CERTIFIED v2]. NEVER LO-resave a wrapped deck.

## P5. Highlight boxes around text (e.g. tan/yellow frames) [CERTIFIED — slide 52]

A highlight box must clear its text on every side. Rule: box width = longest line's
PIL-measured advance + margin (do NOT size to the spec's guess); at 150 dpi assert the
rightmost text ink is at least the original's gap inside the box's right edge. Text
boxes wrap at BOX width, not ink width — always budget boxes ~20% beyond the longest
line (Arial advance ≈ 0.556 em/digit).

### Certified highlight-box clearance pattern (slide 52 founder fix, 2026-10-10 — judge PASS attempt 4, qa/slide052/judge_attempt_4.txt)

- Founder-visible overflow threshold: when the longest line's closing glyph clears the
  fill edge by <2pt (slide 52 line-1 ')' at 1.44pt to fill / ~1.9pt to the 1pt border
  stroke), it reads as "touching the border" even though nothing is clipped. Fix:
  widen the box +0.05in on the RIGHT only (x/y/h unchanged) → clearance 4.80pt to
  fill edge / 5.28pt to stroke inner edge. Right-clearance target: **≥4.5pt to the
  fill edge** for an 18pt-serif line ending in a tall paren (original's own left
  margin is 6pt, so ~5pt is faithful).
- Widening only shifts the box's right border stroke (1px column); every other pixel,
  including all embedded equation PNGs, stays byte-identical — certification of
  untouched regions is inherited per W5, no re-judging of them required.
- Text-box caveat: widening a LEFT-ALIGNED pptxgenjs text box does not move its ink,
  but LibreOffice re-lays-out the text RUN — expect ≤1px glyph-AA shifts across the
  run (slide 52 green run: 105px of ≤1px AA diffs; ink bands/extents unchanged).
  Keep every text box ~20% wider than its longest line so a later box widening never
  re-wraps (slide 52: W_REPLACE 1.0931→box 1.31in, W_GREEN 3.1528→box 3.78in).
- Verification bank: qa/slide052/measure_gap_attempt_4.py (clearance pre/post) +
  measure_line_extents_4.py (full-line extents vs original: L1 598.6 vs 602.0pt,
  L2 442.6 vs 427.0pt, L3 521.8 vs 524.0pt — a judge "nearly double length" claim
  on pixel-identical certified content was refuted by PIL and overridden).

## P6. Native graph/plot panels [CERTIFIED — graph program 18/18]

1. Generate the plot with the topic-correct library running the SAME algorithm on the
   REAL data (graphgen venv; per-slide lib/function choices banked in each
   `qa/slideNNN/graphgen/GRAPH_WORKER_REPORT.md`).
2. Match measured colors/geometry to the ORIGINAL frame, closed-loop PIL alignment,
   graph-vision leg, slide-judge leg — all three required.
3. **Single version per slide (founder directive 2026-10-10, supersedes the old
   two-version rule):** the generated graph is embedded IN the slide's own pptx —
   `slide_NNN_recreated.pptx`, NO `_graphed` suffix (same for OMML: no `_omml`
   suffix). Superseded builds live only in QA evidence dirs, never as parallel
   deliverables.

## P7. Canonical datasets (tables + graphs must share one source) [CERTIFIED — slide 62, iris, judge PASS attempt 4, 2026-10-10]

Known datasets used by a slide (e.g. IRIS for slides 60-64) have ONE canonical file:
`videos/ml-intro/datasets/iris.csv` (150 rows, header
`sepal_length,sepal_width,petal_length,petal_width,species`; values = sklearn
load_iris round-trip — already banked, never download again). Every table cell and
every graph script reads THAT file — never hardcoded sample rows from the spec,
never a different snapshot. Cross-slide consistency check: values shown on 60-64
must be derivable from this one file.

### Certified table-from-dataset pattern (slide 62 founder fix "table data incorrect and not complete", qa/slide62/)

1. **Build reads the CSV live.** `fs.readFileSync("videos/ml-intro/datasets/iris.csv")`
   → validate header → index rows 1-150; every displayed cell is `IRIS[serial].field`
   verbatim (sklearn convention: whole numbers show WITHOUT trailing ".0", matching
   the original). Only the DISPLAYED serial set is hardcoded in the build.
2. **When the original's row set is ambiguous** (spec said "~45-56"; an earlier judge
   guessed 44), derive it from geometry + class-color forensics, not guesses: PIL
   text-band counts per block, each block's Class-column color composition, and
   iris.csv's class boundaries (setosa 1-50, versicolor 51-100, virginica 101-150)
   uniquely determined slide 62's set as 1-8, 45-56, 96-104, 148-150 (+3 red "..."
   rows). The old build had serials 50-56 printing iris rows 51-57's VALUES — a
   7-row shift that looked plausible and passed a lenient judge; only canonical-file
   assertion catches it.
3. **Self-check asserts every cell from the canonical file**: extract the table from
   the built PPTX XML (`zipfile`+ElementTree, find `.//a:tbl` — pptxgenjs nests it
   deeper than `graphicFrame/a:tbl`), assert row count, header verbatim, EVERY data
   cell == the CSV value for that serial, class/ellipsis cell colors, serial order,
   and row/column counts vs the original's measured band count. Banked:
   `qa/slide62/selfcheck_attempt_4.py` (+ `selfcheck_iter2_render5.py`).
4. **Zoomed crop vision leg BEFORE the full judge on dense tables**: crop the table
   region from render and original at the SAME effective scale (150dpi render crop
   825px vs original crop upscaled ×2 to 826px), run the cropped pair through the
   vision gate. The full-slide call cannot resolve 8pt cells; the crop leg read
   every serial/value verbatim (and settled the old "44 vs 45" ambiguity at 45)
   before attempt 4 was spent. Banked: `qa/slide62/tablecrop_4.txt` (+ the two
   `tablecrop_*_4.png`).

## P8. Judge invocation budgets [CERTIFIED]

- Outer wrapper `timeout 1700` → gate `timeout 1650` → `--timeout 600`
  (measured: gate's internal ladder needs >2x the call wall).
- Degenerate garbage = FAIL; ≤3 garbage re-invokes per attempt, ≤6 attempts per slide,
  then park for manual review. Never certify from a degenerate body.
- When a judge FAIL contradicts pixel forensics, retry carrying the measured facts in
  the `--view`/`--capture` context fields — never edit the mandatory -p template.

## P9. PowerPoint-native equation markup (OMML in mc:Choice) [CERTIFIED v2 — 2026-10-10, slides 26/42/55 rewrapped]

`scripts/18_omml_wrapper.py` v2 wraps each certified equation PNG in
mc:AlternateContent: PowerPoint renders the native EDITABLE equation from the
Choice; LibreOffice renders the Fallback PNG — LO render stays pixel-identical
(0 of 2,251,225 px, re-verified per slide after v2).

**Why v1 failed (measured, not guessed):** v1 emitted
`mc:Choice > p:sp > a:p > a14:m > BARE m:oMath` with theme-font runs, zero
`m:ctrlPr`, and a fresh shape id — PowerPoint honored the Choice and rendered
NOTHING (founder report 2026-10-10: slides 42/52/54/55, slide 26 same
mechanism) while LO rendered the Fallback fine. The v1 pattern was modeled on
LibreOffice's own OMML writer — LO's writer output is what LO renders, not
what PowerPoint requires. Never take the LO writer as the authoring oracle for
PowerPoint-only features.

**Research sample (banked):** a REAL PowerPoint (Macintosh)-authored .pptx
containing slide equations lives at
`videos/ml-intro/recreated_pptx/qa/omml_v2/research/real_office_sample/loadAndSave.pptx`
(extracted markup: `slide2.xml` + `unzipped/`; source URL
https://raw.githubusercontent.com/plutext/docx4j/VERSION_17_2_1/docx4j-core-tests/src/test/resources/loadAndSave.pptx),
cross-checked against [MS-ODRAWXML] 2.3.1 and real-PowerPoint integrations
(all sources banked under `qa/omml_v2/research/`, notes in RESEARCH_NOTES.md).

**EXACT v2 markup skeleton (per equation):**

```xml
<mc:AlternateContent>
  <mc:Choice xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main" Requires="a14">
    <p:sp>
      <p:nvSpPr>
        <p:cNvPr id="{SAME id as the Fallback p:pic}" name="Equation OMML" descr="{mathtext}"/>
        <p:cNvSpPr txBox="1"/><p:nvPr/>
      </p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x=".." y=".."/><a:ext cx=".." cy=".."/></a:xfrm>  <!-- == the pic frame -->
        <a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/>
      </p:spPr>
      <p:txBody>
        <a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"><a:noAutofit/></a:bodyPr>
        <a:lstStyle/>
        <a:p>
          <a:pPr algn="ctr"><a:buNone/></a:pPr>
          <a14:m>
            <m:oMathPara xmlns:m="{NS_M}" xmlns:a="{NS_A}">
              <m:oMathParaPr><m:jc m:val="centerGroup"/></m:oMathParaPr>
              <m:oMath xmlns:m="{NS_M}">…runs and constructs…</m:oMath>
            </m:oMathPara>
          </a14:m>
          <a:endParaRPr lang="en-US" dirty="0"/>
        </a:p>
      </p:txBody>
    </p:sp>
  </mc:Choice>
  <mc:Fallback>{original p:pic VERBATIM — the certified PNG}</mc:Fallback>
</mc:AlternateContent>
```

Every text run: `<m:r>[<m:rPr><m:sty m:val="p|b"/></m:rPr>]<a:rPr lang="en-US"
i="0|1" smtClean="0" sz="{pt*100}"><a:solidFill><a:srgbClr val="XXXXXX"/>
</a:solidFill><a:latin typeface="Cambria Math" panose="02040503050406030204"
pitchFamily="18" charset="0"/></a:rPr><m:t xml:space="preserve">…</m:t></m:r>`.
Every construct property element (`m:fPr`, `m:radPr`, `m:naryPr`, `m:sSubPr`,
`m:sSupPr`, `m:sSubSupPr`, `m:dPr`, `m:barPr`, `m:accPr`) embeds
`<m:ctrlPr>` carrying the SAME `a:rPr`.

**Mandatory deltas v1→v2** (each measured against the real Office file — full
diff table in `qa/omml_v2/markup_identity_output.txt`): oMathPara display form
with `m:jc=centerGroup`; Cambria Math + panose on every run; `m:ctrlPr` in
every construct *Pr; same cNvPr id as the Fallback pic; explicit `i` +
`smtClean="0"`; `a:lstStyle` + `a:pPr(algn=ctr+buNone)` + `a:endParaRPr`.
Kept as documented schema-legal deviations (with precedent): per-run
`sz`+`solidFill` (real slides do size/color equations), zero-inset
`bodyPr`+`noAutofit` (pins the frame to the pic's), explicit `m:limLoc`,
`xml:space="preserve"`.

**Validation chain per rewrap** (26/42/55/52 all PASS, evidence under
`qa/omml_v2/slide{026,042,052,055}/`): LO 150dpi private-profile render 0-px-diff
vs the certified base; only `ppt/slides/slide1.xml` differs in the zip;
Fallback pics verbatim; Choice structure element-for-element == this pattern;
idempotent re-run byte-identical; base-deck md5 unchanged. Choice-only scratch
render (Fallback stripped) converts in LO without error — the Choice markup is
well-formed. Unit suites: `qa/omml_v2/unit/`. Invocation contract:
`qa/omml_v2/WRAPPER_V2_READY.txt`. NEVER LO-resave a wrapped deck (LO drops
the OMML it never understood — measured). The wrap is applied to the slide's
own single plain-named pptx (no `_omml` variants). Open: slide 54 wrap once its
content-fixed base lands.

## P10. All-in-one deck merge [CERTIFIED]

`scripts/19_build_final_deck.py`: byte-verbatim slide XML copy + retargeted .rels +
renamed media + shared skeleton; gate = render merged deck AND all sources in one
soffice session, pixel-diff page N vs source N, 0/64 mismatches required.
Post-consolidation (single-version naming) the merge reads the plain-named
`slide_NNN_recreated.pptx` files directly — one per slide.

### P2 amendment — EXPLICIT LINE SPACING (PowerPoint-vs-LO divergence) [CERTIFIED — slide 5 founder re-fix, judge PASS attempt 6, 2026-10-10]

LO auto line pitch UNDERESTIMATES PowerPoint's for the same font size. Slide-5 MEASURED
numbers (founder PowerPoint screenshot, scale anchored on the inner-frame stroke
centers = 79.66px/in; LO render 150dpi): bullets auto band pitch LO 25.61pt vs
POWERPOINT 31.64pt (ratio 1.235 — the 12-row stack ended ONE FULL bullet-row lower in
PowerPoint; last bullet "and many more" ink top +0.132in BELOW the inner-frame bottom
while the LO render of the same bytes showed 0.586in clearance; a visual judge formally
confirmed this divergence on the founder evidence). Lead-in auto pitch: LO 28.79pt vs
PowerPoint 36.16pt. Rule: every multi-line text box sets explicit `lineSpacing: <pt>`
(pptxgenjs → `a:lnSpc > a:spcPts`, honored identically by both renderers); prefer a
SINGLE knob — drop `paraSpaceAfter` and pin the FULL pitch on lineSpacing, so the
render's band pitch == pinned value exactly. With explicit spacing both renderers use
the same pitch and the LO containment check predicts PowerPoint (residual first-line
anchoring difference between renderers ≤0.08in — covered by clearance). Verify
post-build: re-measure the render's band pitch == pinned value. Blocks near a frame
bottom additionally keep ≥0.4in bottom clearance in the LO render (slide 5 shipped
0.526in; the judge found ~1 line of clearance insufficient to absorb the divergence
while pitch was UNpinned).

Confirmed slide 52 (2026-10-10, qa/slide052/linespacing_check_5.py): only multi-line
box = wrapped Example bullet (Arial 20pt, 3 lines). Pinned `lineSpacing: 24` = the LO
render's measured auto pitch (band tops 455/505/555px = 24.00pt exactly) → post-pin
render **pixel-identical to the judged render (n=0 diffs)**, so the prior judge PASS
carried per W5 at zero vision cost; `spcPts val="2400"` verified in slide1.xml. This
no-op-pin variant is the preferred application when the current render is already
certified: measure the LO pitch FIRST, pin exactly that, pixel-diff to prove n=0.
(The original's own 31pt pitch is a judge-passed MINOR — do not "improve" it during a
compliance pin; that would move certified ink and force a re-judge.)

Confirmed slide 5 defect-fix variant (2026-10-10, qa/slide005/, judge PASS attempt 6):
DIFFERENT from the slide-52 compliance pin — slide 5 was RE-OPENED by a founder defect
(overflow in PowerPoint), so a re-judge was mandatory anyway and the pin value was free
to move ink. Pin-value law for that case: pin to the ORIGINAL's measured band pitch,
not to LO's auto pitch — judge attempt 5 FAILED the LO-auto pin (lead-in 28.8pt) as too
tight vs the original's measured 30.0pt (a 4% real gap the judge eyeballed as 30%; PIL
forensics gave the true numbers). Final slide-5 pins: lead-in `lineSpacing: 30`
(original 30px@72dpi = 30.0pt), bullets `lineSpacing: 25.6` (original LSQ 25.57pt);
post-fix render measured 30.23pt / 25.59pt; clearances T 0.113 / B 0.526 / L 0.193 /
R 0.913in; zero ink on any frame edge. Judge attempt 6 settled the pinned values,
founder-ordered frame geometry, and spec color #0000CC in its GROUND RULES
acknowledgment and PASSED.

Confirmed slide 62 (2026-10-10, qa/slide62/selfcheck_attempt_4.py, judge PASS attempt
4): info box = 9 paragraphs (3 blank spacer lines included) pinned per-paragraph
`lineSpacing` 24/10/24/19/19/19/10/24/17pt with `paraSpaceAfter` only where the
original has a visible gap (150S→spacer 36pt, Vir→spacer 31pt composite pitch).
Pitfall measured: pptxgenjs EMPTY text runs (`""`) DROP their fontSize options — the
XML gets `endParaRPr sz=2000` → a "blank line" renders as a 20pt-tall band and the
anchor=ctr box overflows BOTH edges (the founder's "top and bottom overflow"). Fix:
single-SPACE runs `" "` at 10pt. Post-pin render band pitches measured
36.0/23.0/19.2/19.2/32.2/24.5pt vs pinned 36/24/19/19/31/26 (≤1.5pt, within the ±2pt
assert); box clearances T 0.573in / B 0.507in (≥0.4in law), 9 `a:lnSpc > a:spcPts`
entries verified in slide1.xml.

Confirmed slide 043 graphed rework round 2 (2026-10-10, qa/slide43/graphgen/, judge
PASS attempt 2, full-deck merge pixel-identical 0/2,251,225): FOUR new laws.
(1) MARKER EDGE INFLATION: matplotlib "o" markers draw the markeredge stroke (default
lw 1.5pt) HALF OUTSIDE the nominal radius — a disc of markersize d renders with solid
radius d/2 + ~0.75pt. When a dot is sized from ABSOLUTE measured radii, pass
`markeredgewidth=0` (slide 043's v3 query dot: nominal r8 rendered solid ~8.7 vs the
original's 7.5 — the closeup judge correctly called it "visibly larger"). Banked
cluster dots whose INK d was calibrated THROUGH rendered pixels already include the
edge — never mix the two calibration styles blindly; transect the render (radial color
walk at 45-degree steps) before certifying size.
(2) GLOSSY BALL = 3 STACKED DISCS: a top-lit shaded dot (original: bright center
(232,0,0), top rims bright, bottom rims dark maroon) is reproduced exactly by
base disc (dark rim tone, full solid radius, z) + mid disc (brighter, d-2.4, offset
up ~0.5, z+0.05) + core disc (brightest, d-5, slight offset, z+0.1) — sample tones
land within a few RGB units of the original's measured rim quadrants. Calibrate from
multi-threshold angular-coverage radii (solid edge = 100% coverage; strong-ink edge =
50% at a tight mask; the faded JPEG halo beyond is blur, NOT paint — omit it).
(3) SMALL-GLYPH PAINT DE-BLUR: a small red glyph on a white bg measures
measured = paint*p + white*(1-p); solve p from the G channel (p = 1 - G/255) and
recover the paint. Slide 043's '?' resolved to the deck's maroon #8B1A1A (the spec's
#E02020 was the blurred read). Crisp vector ink must sit INSIDE the original's
blurred ink extent (~1px inset/side), never match the blurred bbox — measure the
blurred extent with a loose mask, the crisp render with a tight one, and target
containment, not equality.
(4) TINY-CANVAS VISION COMPARISONS FABRICATE GEOMETRY: a 201x108 crop pair produced
two contradictory judge bodies on the SAME original (v3: "strong dimensional
shading, glossy"; v4: "nearly flat") and size claims off 2x vs direct pixel counts.
Dense-region crop pairs must be >= ~400px wide (x4-x6 upscale) AND run at FULL judge
params (thinking high, max-tokens 65536); ALWAYS pixel-measure both crop PNGs first
(mask area, block-reduce ASCII map) so a fabricated body can be rebutted with
numbers, banked as defective evidence, and re-run at better conditioning — never
"fixed" against made-up numbers. The c5 x6 re-run at full params: PASS with 4 MINORs.
Judge template's own clause list (frame containment, missing elements, delimiter
geometry, table data) must come from the CURRENT 17_worker_instructions.md template
extracted programmatically — older banked prompts (e.g. judge_graphed_prompt_1.txt)
predate clauses (5)-(8) and the 1650/600 walls; do not copy them for new attempts.

### Certified deep-verify fix patterns (slide 044 graphed, 2026-10-10 — judge PASS attempt 2 + 6/6 crop comparisons PASS, `qa/slide44/graphgen/`)

(1) MATPLOTLIB PATCH DASH SPECS ARE SCALED BY LINE WIDTH: `Circle(..., lw=1.8,
linestyle=(0,(2,3.5)))` renders EFFECTIVE (3.6, 6.3) pt — 8 dashes at r=12.5 instead
of the intended 14 (measured: 720-sample circle walk, run lengths prove period x1.78
= lw). To get true on/off of a pt: divide the spec by lw (`(0,(2/1.8, 3.5/1.8))` →
measured 14 dashes, ~2pt ink). Plot/Line2D dash handling differs from Patch — always
count the dashes in the rendered PNG, never trust the spec.
(2) HOUSE FRAME BEATS THE ORIGINAL'S OWN BOX GEOMETRY: slide 044's original
content-box border measures left 70-71 / right 884-886 / top 116-117 but BOTTOM
532-533 slide px — which would cross the recreation's house-frame line at 529.2
(`orig_content_box_044` in forensics_v4b_044_out.json). House rule wins: clip the
image region bottom to keep ~0.1in daylight inside the frame (region (70,116,885,522))
and draw the native border rect AT the clipped image edge (0.9792, 1.6181,
11.3125 x 5.6319 in, after addImage so the stroke renders over the image).
(3) SINGLE-LINE lineSpacing PINS LO==POWERPOINT, BUT PLACE EMPIRICALLY: captions
valign bottom + lineSpacing 22 landed baselines at 509.3/509.3 slide px where the
font-descent formula predicted 508.6/507.7 — nudge the BOX y by the measured delta
(-0.024in), re-render, re-measure (final 507.4/507.9 vs original targets 508/507.2,
within 0.7px). Never trust a baseline formula over the render; measure, nudge,
re-measure. Wrap-safety for single-line boxes: PIL-measure the string advance
(Liberation Sans Bold = Arial metrics) and keep box width >= width + 0.1in.
(4) SELF-CHECK ASSERTIONS IN ONE UNIT: three false FAILs in one self-check run came
from mixing render-px targets with slide-px measurements (caption height 13.9 slide
px asserted against 29.2 render px) and measurement windows that clipped the ink
(right-caption window 1180..1660 render px vs actual ink 1082..1749). State every
assertion in slide px (divide render px by 150/72 once, at print time), and make
measurement windows 2x the expected ink extent on every side.
(5) A coherent judge body can still mis-state sizes at zoom: qmarkzoom attempt-2
claimed the query dot renders "1.3-1.5x larger" and the '?' "raised" — measuring the
dot+'?' composite red-ink span in BOTH crop PNGs gave 87x33 (orig) vs 88x34 (render),
centers 1px apart. Bank the numeric rebuttal next to the transcript; a PASS with a
measured-rebuttable MAJOR note is still a PASS.
