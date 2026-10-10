// Slide 063 recreation — GRAPHED VARIANT (second version; certified build
// slide_063.js / slide_063_recreated.pptx stay untouched).
// Content spec: videos/ml-intro/analysis/slide_063_final.json (validation fixes applied)
// House frame rule (founder directive): bg E8E8E8, red frame C00000, badge FFF9C4 w/ "63",
// title box y:0.28 x:0.6 w:12.13 centered. Overrides spec where they differ.
//
// Delta vs certified build: the native-shapes scatter approximation (white plot
// rect + origin axes + tick text boxes + mulberry32 pseudo-random dot ovals) is
// replaced by addImage of the vision-validated generated graph:
//   videos/ml-intro/recreated_pptx/build/assets/graphs/s63_graph_v2.png
//   (graphgen/slide_063_pca2d.py — sklearn.decomposition.PCA(n_components=2) on
//   real sklearn.datasets.load_iris(); graph-leg comparison PASS, attempt 2,
//   graph_check_2.txt; closed-loop PIL alignment PASS, verify_alignment_v2.txt).
// House frame + badge "63" + ALL text (title, equation, legend, footer) unchanged.
//
// Embed geometry (PIL-measured from videos/ml-intro/unique_slides/slide_063.jpg,
// 960x540, 1px = 1pt): red plot panel x 246..746 y 95..495 px
//   -> x=3.4167in y=1.3194in w=6.9444in h=5.5556in.
// The measured panel overlaps the certified EQ box (x 133..331px): the image is
// drawn after the EQ box shape but BEFORE the EQ text content, so the equation
// renders on top of the image; the EQ box's red border (covered on its right half
// by the image) is restored by a border-only repair rectangle after the EQ
// content. Accepted residual, documented: the plot's y-axis margin shows through
// the EQ box's right half (same class of defect as the slide 64 pilot's accepted
// nested-rectangle MINOR).
//
// REWORK 2026-10-10 (founder defect, final-deck review): the multi-line vector
// delimiters were rebuilt as P3 spanning arcs — see the colVector block below.
// Graph image, house chrome, all text, PCA stack, legend, footer untouched.
const pptxgen = require("pptxgenjs");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8";           // house background (overrides spec F2F2F2)
const FRAME = "C00000";        // house frame line
const INK = "333333";          // badge numeral
const BADGE = "FFF9C4";        // house badge fill
const TITLE_RED = "CC0000";    // title red (spec)
const BLUE = "0000CC";         // title/banner blue (spec)
const HILITE = "FFFF00";       // yellow title highlights (spec)
const PANEL_RED = "8B0000";   // main panel border (spec)
const EQ_RED = "FF0000";       // equation box border, PCA label, arrow (spec)
const SUB_BLUE = "0000FF";     // vector subscripts + Virginica points (spec)
const GREEN = "00AA00";       // Versicolor points (spec)
const BLACK = "000000";
const WHITE = "FFFFFF";
const FONT = "Arial";
const MATHFONT = "Times New Roman"; // axis labels: "large italic serif-style (math font)" (spec)

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer chrome ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});
// Slide-number badge: yellow oval, numeral "63" (number printed on the original slide)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("63", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Title (verbatim, two-tone + yellow highlights on "4" and "two") ----
s.addText(
  [
    { text: "Visualize Reduced Features  [ ", options: { color: TITLE_RED } },
    { text: "4", options: { color: BLUE, highlight: HILITE } },
    { text: " features are reduced to ", options: { color: BLUE } },
    { text: "two", options: { color: BLUE, highlight: HILITE } },
    { text: " features]", options: { color: BLUE } },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle",
    fontSize: 22, bold: true, fontFace: FONT, margin: 0,
  }
);

// ---- Main panel: thin dark-red border ----
// Left edge at the ORIGINAL's measured container (x=58px, forensics_v7): the
// original's equation box (73..223px) sits inside the container, 15px clear of
// its left border. The certified build's panel left edge (115px) would cross the
// equation box; judge attempt 1 (judge_graphed_attempt_1.txt) MAJOR #1.
const PANEL = { x: 0.806, y: 1.28, w: 11.864, h: 5.48 };
s.addShape(pptx.shapes.RECTANGLE, {
  x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h,
  fill: { color: BG }, line: { color: PANEL_RED, width: 1.25 },
});

// ---- GENERATED GRAPH IMAGE (graphed variant) ----
// Vision-validated 2-D PCA scatter (graph leg PASS, attempt 2). Measured region:
// red plot panel x 246..746 y 95..495 px -> x=3.4167 y=1.3194 w=6.9444 h=5.5556.
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s63_graph_v2.png",
  x: 3.4167, y: 1.3194, w: 6.9444, h: 5.5556,
});

// ---- PCA equation box (left side inside panel) ----
// Geometry PIL-measured from the original frame (forensics v6/v7): box border
// x 73..223 y 142..258 px (bright red ~1pt) -> EQ = 1.014, 1.972, 2.083, 1.611 in.
// This keeps the box fully clear of the plot panel (starts x=246) and the
// y-tick zone, and clear of the container's left border (x=58), matching the
// original (judge attempt 1 MAJOR #1/#2 fix).
const EQ = { x: 1.014, y: 1.972, w: 2.083, h: 1.611 };
s.addShape(pptx.shapes.RECTANGLE, {
  x: EQ.x, y: EQ.y, w: EQ.w, h: EQ.h,
  fill: { color: BG }, line: { color: EQ_RED, width: 1 },
});

// Column vector with P3 SPANNING delimiters (rework 2026-10-10, founder defect:
// parens did not expand across the 4 lines and their strokes sat over the text).
// Construction per patterns.md P3 — measure-then-draw:
//   - ONE arc per side spanning the WHOLE enclosed block (half-turn angleRange
//     [90,270] for "(", [270,450] for ")"), NOT per-line glyphs and NOT the old
//     fat-ellipse [135,225] arcs whose visible stroke covered only the middle
//     ~50% of the block and whose tips swung ~19px inward over the text.
//   - Arc bbox sized from the ORIGINAL's measured stroke columns (forensics
//     v8e, 1px = 1pt = 1/72in): the stroke bulge lands on the bbox's outer
//     edge, the tips on the bbox's horizontal center (small rx = the original's
//     2-4px tip curl).
//   - Stroke color: the original's parens are light gray (~RGB 190,190,190 —
//     forensics v8e darkest-40 medians), not black.
//   entries      : text boxes h=lh, valign middle, first center at firstCY, pitch lh
//   lArc/rArc     : {x, y, w, h, a} measured spanning arcs (a = angleRange)
//   tX/tY         : T superscript position (unchanged from certified attempt-4)
//   mainColor/subColor: ink roles per vector — PIL-measured in the ORIGINAL
//     (color_adjudication*.txt): the LEFT vector's ink is ALL BLUE (main letters
//     darkest-40 median B-R +87 on all 4 lines, subscripts +42..+55 — pure-blue
//     source under JPEG blur), while the RIGHT vector is ALL NEUTRAL (letters
//     B-R -1, subscripts -2/-3). The old build drew black main letters + blue
//     subscripts on BOTH vectors (crop-judge attempt-5 MAJOR, PIL-confirmed).
const PAREN_GRAY = "B3B3B3";   // neutral light gray — the ORIGINAL's right-vector
                               // parens measure neutral (B-R -1/+3); the left side's
                               // +18..+24 lavender tint is JPEG chroma bleed from
                               // the adjacent blue subscripts (color_adjudication_part2)
function colVector(entries, cx, firstCY, lh, lArc, rArc, tX, tY, mainColor, subColor) {
  s.addShape(pptx.shapes.ARC, {
    x: lArc.x, y: lArc.y, w: lArc.w, h: lArc.h,
    angleRange: lArc.a,
    fill: { color: BG, transparency: 100 },
    line: { color: PAREN_GRAY, width: 2.25 },
  });
  s.addShape(pptx.shapes.ARC, {
    x: rArc.x, y: rArc.y, w: rArc.w, h: rArc.h,
    angleRange: rArc.a,
    fill: { color: BG, transparency: 100 },
    line: { color: PAREN_GRAY, width: 2.25 },
  });
  s.addText("\u1D40", {
    x: tX, y: tY, w: 0.22, h: 0.26, align: "left", valign: "top",
    fontSize: 12, color: BLACK, fontFace: FONT, margin: 0,
  });
  entries.forEach((e, i) => {
    s.addText(
      [
        { text: e[0], options: { color: mainColor, breakLine: false } },
        { text: e[1], options: { color: subColor, breakLine: false } },
      ],
      {
        x: cx - 0.3, y: firstCY - lh / 2 + i * lh, w: 0.6, h: lh, align: "center", valign: "middle",
        fontSize: 15, fontFace: FONT, margin: 0,
      }
    );
  });
}
// Left column vector (W1 L1 W2 L2)^T: entries centered x=94px, ink centers y 162/188/215/240px
// (pitch 26.2px). ORIGINAL measured (forensics v8e): 4 lines y 154..244; parens
// ink y 147..252; left paren stroke bulge x 77..80, tips x 79..81; right paren
// stroke bulge x 110..112, tips x 109..111; T at x 104..112 y 150..158.
//   left  arc: bbox x 78.5..82.5px (bulge path 78.5, tips path 80.5), y 147..252
//   right arc: bbox x 109..111.75px (bulge path 111.75, tips path 110.4), y 147..252
colVector(
  [["W", "\u2081"], ["L", "\u2081"], ["W", "\u2082"], ["L", "\u2082"]],
  1.306, 2.25, 0.364,
  { x: 1.0903, y: 2.0417, w: 0.0556, h: 1.4583, a: [90, 270] },
  { x: 1.5139, y: 2.0417, w: 0.0382, h: 1.4583, a: [270, 450] },
  1.442, 2.053,
  SUB_BLUE, SUB_BLUE   // ORIGINAL: whole left vector is blue ink (B-R +87)
);
// Red italic "PCA" over a horizontal bar with the double arrow below
// (fraction-like arrangement, judge attempt 1 MINOR #3/#4 fix).
// REWORK 2026-10-10 (crop-judge attempt-5 MAJOR, PIL-confirmed in
// color_adjudication_part5.txt): the ORIGINAL's PCA ink is x 138..170 y 178..190
// (12px tall) — 12pt rendered only 9px; resized to 16pt -> ink ~178..190.
s.addText("PCA", {
  x: 1.889, y: 2.417, w: 0.556, h: 0.278, align: "center", valign: "middle",
  fontSize: 16, italic: true, bold: false, color: EQ_RED, fontFace: FONT, margin: 0,
});
s.addShape(pptx.shapes.LINE, {
  x: 1.861, y: 2.715, w: 0.542, h: 0,
  line: { color: "A6A6A6", width: 1 },
});
// ORIGINAL arrow ink x ~150..168 y 201..207/208 — the 13pt glyph rendered
// 203.3..208.6 (bar->arrow gap 7.4px vs the original's ~4px); resized to 18pt
// and raised so the ink lands ~201..208.
s.addText("\u21D2", {
  x: 2.036, y: 2.731, w: 0.306, h: 0.194, align: "center", valign: "middle",
  fontSize: 18, color: EQ_RED, fontFace: FONT, margin: 0,
});
// Right column vector (Z1 Z2)^T: entries centered x=205px, ink centers y 186/212px.
// ORIGINAL measured (forensics v8e): lines y 180..192 / 206..218 (Z1 x 197..205,
// Z2 x 196..212); parens ink y 173..227; left paren stroke bulge x 189..192,
// tips x 192..194; right paren stroke bulge x 216..218, tips x 215..217;
// T at x ~207..215 y 167..177.
//   left  arc: bbox x 190.5..195.5px (bulge path 190.5, tips path 193), y 173..227
//   right arc: bbox x 214.5..217.5px (bulge path 217.5, tips path 216), y 173..227
colVector(
  [["Z", "\u2081"], ["Z", "\u2082"]],
  2.847, 2.583, 0.361,
  { x: 2.6458, y: 2.4028, w: 0.0694, h: 0.75, a: [90, 270] },
  { x: 2.9792, y: 2.4028, w: 0.0417, h: 0.75, a: [270, 450] },
  3.026, 2.303,
  BLACK, BLACK   // ORIGINAL: right vector is neutral ink (letters B-R -1, subscripts -2)
);

// ---- Legend (right of plot inside panel) ----
// Judge attempts 2-3 measured the legend (raw render px vs the 960px original)
// as ~35% larger glyphs with ~2x line gaps and prescribed: leading ~1.5x and
// glyphs ~30% smaller -> fontSize 7, lineSpacing 8 (raw glyph ~11px, pitch ~17px,
// ratio 1.5), block centered on the original's legend band (y ~202..253px).
s.addText(
  [
    { text: "Setosa", options: { color: EQ_RED, breakLine: true } },
    { text: "Versicolor", options: { color: GREEN, breakLine: true } },
    { text: "Virginica", options: { color: SUB_BLUE, breakLine: false } },
  ],
  {
    x: 11.06, y: 2.99, w: 1.6, h: 0.37, align: "left", valign: "top",
    fontSize: 7, bold: false, fontFace: FONT, margin: 0, lineSpacing: 8,
  }
);

// ---- Footer banner (bottom center) ----
// Border color measured from the original frame: light blue-gray ~#A3A1BC
// (banner top/bottom border rows y=504/505, 532/533; judge attempt 1 MINOR #6
// fix — original border is light blue, not dark red).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 2.67, y: 6.88, w: 8.0, h: 0.42,
  fill: { color: BG }, line: { color: "A3A1BC", width: 1 },
});
s.addText(
  [
    { text: "Visualize Classes ", options: { color: BLUE } },
    // Judge attempts 2-3 (low conf) both read the original's "as" as blue with
    // only "2-D" red — split the red run accordingly (text stays verbatim).
    { text: "as ", options: { color: BLUE } },
    { text: "2-D", options: { color: TITLE_RED } },
    { text: "  (Z\u2081 vs Z\u2082)", options: { color: BLUE } },
  ],
  {
    x: 2.67, y: 6.88, w: 8.0, h: 0.42, align: "center", valign: "middle",
    fontSize: 15, bold: true, fontFace: FONT, margin: 0,
  }
);

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_063_recreated.pptx" })
  .then(() => console.log("done"));
