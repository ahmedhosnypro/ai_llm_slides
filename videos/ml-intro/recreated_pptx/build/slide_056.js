const pptxgenpkg = require("pptxgenjs");

// Slide 56 — "Choice of K - Neighborhood Size" per analysis/slide_056_final.json.
// Deck was re-curated 2026-10-09 20:39; this slide is the old slide 88.
// Geometry corroborated by direct PIL measurement of unique_slides/slide_056.jpg
// (72 px/in): title band y 1.26-1.65in centered (x 2.89-10.43); content box
// x 0.98-12.31, y 1.94-7.23; main bullets at x 1.50; sub-bullets at x 2.14;
// final line red; trailing empty bullet at y~6.2.
// Styling note: spec claims red-bold emphasis on 'and over-fit'/'under-fit'/
// 'High bias', but pixel measurement of the original shows those bands contain
// NO red text and no underline; both vision passes agree emphasis exists, so
// they are rendered BOLD DARK (#333333) — red ruled out by measurement.
// 'In general, a K too small or too big is bad!' IS measurably red (regular
// weight — same per-char width as the other sub-lines).
// House chrome per founder directive 2026-10-09: E8E8E8 background, red frame
// rect (0.15/0.15/13.03/7.2, C00000 1.5pt), badge oval with numeral "56".

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8", RED = "C00000", BODY_RED = "CC0000", BOX_RED = "B22222",
      INK = "333333", WHITE = "FFFFFF", BADGE_YELLOW = "FFF9C4";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// 1. House outer red frame (founder directive).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// 2. Original slide body: white inside the frame (original bg #FFFFFF).
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.19, y: 0.19, w: 12.95, h: 7.12,
  fill: { color: WHITE }, line: { color: WHITE, width: 0.25 },
});

// 3. House slide-number badge (founder directive geometry, numeral "56").
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("56", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// 4. Title — house box (y 0.28, x 0.6, w 12.13, centered), text anchored to the
//    original position (glyph band 1.26-1.65in) via valign bottom. 35pt bold
//    matches the original's measured 7.54in line width.
s.addText("Choice of K - Neighborhood Size", {
  x: 0.6, y: 0.28, w: 12.13, h: 1.42, align: "center", valign: "bottom",
  fontSize: 35, bold: true, color: BODY_RED, fontFace: FONT, margin: 0,
});

// 5. Content box: rounded rectangle, white fill, thin red/maroon outline.
//    Measured on the original: x 0.98..12.31, y 1.94..7.23.
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.98, y: 1.94, w: 11.33, h: 5.29, rectRadius: 0.08,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 2 },
});

// 6. Bullet list — one text box per line at measured positions.
//    Main bullets: round marker (dark, measured) + red bold text, x 1.50.
//    Sub-bullets: dash marker + dark text, x 2.14.
function mainBullet(label, y) {
  s.addText([
    { text: "\u2022 ", options: { color: INK, bold: true } },
    { text: label, options: { color: BODY_RED, bold: true } },
  ], {
    x: 1.50, y, w: 10.5, h: 0.38, fontSize: 20, color: BODY_RED,
    fontFace: FONT, margin: 0, valign: "top",
  });
}
function subBullet(runs, y) {
  s.addText(runs, {
    x: 2.14, y, w: 10.1, h: 0.28, fontSize: 16.5, color: INK,
    fontFace: FONT, margin: 0, valign: "top",
  });
}

mainBullet("Small K", 2.22);
subBullet([{ text: "- Creates many small regions for each class" }], 2.66);
subBullet([
  { text: "- May lead to non-smooth decision boundaries " },
  { text: "and over-fit", options: { bold: true } },
], 3.00);

mainBullet("Large K", 3.43);
subBullet([{ text: "- Creates fewer larger regions" }], 3.82);
// Wrapped bullet — two separate single-line boxes at the original's measured
// wrap (line 1 ends x 11.36in; line 2 starts "under-fit). High bias ..." at
// x 2.14, no continuation indent, no repeated dash).
subBullet([{ text: "- Usually leads to smoother decision boundaries (caution: too smooth decision boundary can" }], 4.15);
subBullet([
  { text: "under-fit", options: { bold: true } },
  { text: "). " },
  { text: "High bias", options: { bold: true } },
  { text: " to classes with larger members" },
], 4.41);

mainBullet("Choosing K", 4.81);
subBullet([{ text: "- Often data dependent and heuristic based" }], 5.20);
subBullet([{ text: "- Or using cross-validation (using some held-out data)" }], 5.58);
// Final line: measurably all red, regular weight.
subBullet([
  { text: "- " },
  { text: "In general, a K too small or too big is bad!", options: { color: BODY_RED } },
], 5.94);

// 7. Trailing empty bullet (mid-build state, verbatim per spec step 10):
//    tiny dark round marker at x~1.51, y~6.2 on the original.
s.addText("\u2022", {
  x: 1.48, y: 6.15, w: 0.3, h: 0.25, fontSize: 11, color: INK,
  fontFace: FONT, margin: 0, valign: "top",
});

// Cursor artifact (gray '+' cross at top-center of content box) is EXCLUDED
// per recreation_brief step 11 — video-recording artifact, not slide content.

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_056_recreated.pptx" })
  .then(() => console.log("done"));
