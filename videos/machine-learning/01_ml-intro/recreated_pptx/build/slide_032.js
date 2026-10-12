// Slide 032 recreation — "Feature Extraction" — attempt 1 (new numbering)
// Spec: videos/ml-intro/analysis/slide_032_final.json (validated, PASS_WITH_FIXES, score 8)
// Started from old-deck build/slide_040.js (old id 40); badge numeral corrected 40 -> 32,
// output filename renumbered; all content re-verified against the corrected spec.
//
// HOUSE FRAME RULE (founder, 2026-10-09) — overrides spec/judge for these elements:
//   bg E8E8E8; outer frame rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 w1.5, fill E8E8E8;
//   badge oval x:12.48 y:0.30 w:0.5 h:0.5, fill FFF9C4 line FFF9C4 w0.5, numeral "32"
//   (the number PRINTED on the original slide image — matches the slide id here) bold 18pt 333333;
//   title text box starts y:0.28, x:0.6, w:12.13, align center.
//
// Title-box handling (slide_006 precedent): the spec's light-blue title box is a spec
// visual element, but its GEOMETRY differs from the house title geometry, so house
// wins: the box is moved to y:0.28 and centered horizontally so the house centered
// title text lands inside it (same resolution as slide 006's black banner).
//
// BULLET IMPLEMENTATION NOTE (pptxgenjs 4.0.1 bug workaround): no `bullet` options
// anywhere — bullets are manual "• " glyphs, one text box per line. Multi-run
// paragraphs carry no paragraph-level options so they emit a single clean pPr.
//
// VERBATIM content rules honored: subtitle keeps the duplicated "are is"; bullet
// "Geometrical Features ," keeps the space before the comma; last two items carry no
// trailing comma; the "........." placeholder item is kept (NINE dots — pixel-verified
// against the original frame: nine evenly-spaced ink runs after the bullet marker;
// a spot-check vision read claiming seven dots was refuted by the pixel evidence).
// The mouse cursor noted in animation_state is a lecture-capture artifact and is NOT recreated.

const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const BG = "E8E8E8", RED = "C00000", TEXT = "000000", INK = "333333";
const TITLEBOX_FILL = "CFE8EF", TITLEBOX_LINE = "1F3864", BADGE = "FFF9C4", WHITE = "FFFFFF";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE outer frame: red rectangle, 0.15in inset from every edge ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// ---- Content frame (spec region 2): white area, red border, x 7-93%, y 23-97% ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.933, y: 1.725, w: 11.464, h: 5.55,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// ---- Spec title highlight box: light blue fill, dark blue outline ----
// Spec geometry x 8-38% / y 15-27% conflicts with house title geometry -> house wins:
// moved to y:0.28, centered horizontally (w kept from spec, 30% of slide width).
const TB = { w: 4.0, h: 0.9, y: 0.28 };
TB.x = (W - TB.w) / 2;
s.addShape(pptx.shapes.RECTANGLE, {
  x: TB.x, y: TB.y, w: TB.w, h: TB.h,
  fill: { color: TITLEBOX_FILL }, line: { color: TITLEBOX_LINE, width: 1.25 },
});

// ---- HOUSE title text box: starts y:0.28, x:0.6, w:12.13, centered ----
s.addText("Feature Extraction", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "middle",
  fontSize: 28, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});

// ---- HOUSE slide-number badge — numeral is the number printed on the original slide image ("32") ----
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("32", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Subtitle (verbatim, including the "are is" duplication) ----
// 'Features Types are is' red bold + ' Problem dependent' black italic underlined.
// Single paragraph, two runs, NO paragraph-level options (bullet-bug hygiene).
s.addText(
  [
    { text: "Features Types are is", options: { bold: true, color: RED } },
    { text: " Problem dependent", options: { italic: true, underline: true, color: TEXT } },
  ],
  {
    x: 1.6, y: 2.15, w: 10.5, h: 0.5, align: "left", valign: "middle",
    fontSize: 20, fontFace: FONT, margin: 0,
  }
);

// ---- Bold lead-in ----
s.addText("Features may include:", {
  x: 1.6, y: 2.8, w: 10.5, h: 0.45, align: "left", valign: "middle",
  fontSize: 20, bold: true, color: TEXT, fontFace: FONT, margin: 0,
});

// ---- Bullet list: manual "• " glyphs, one text box per line (9 items, verbatim) ----
const BULLETS = [
  "Center of Gravity location,",
  "Aspect Ratio,",
  "Length and Width,",
  "Number of intersections,",
  "Moments,",
  "Geometrical Features ,",   // space before comma preserved (spec)
  "Colors,",
  "Transformations",
  ".........",                // placeholder item, nine dots, no trailing comma
];
const BULLET_X = 1.85, BULLET_Y0 = 3.35, BULLET_DY = 0.38;
BULLETS.forEach((t, i) => {
  s.addText("• " + t, {
    x: BULLET_X, y: BULLET_Y0 + i * BULLET_DY, w: 10.0, h: 0.38,
    align: "left", valign: "middle", fontSize: 20, color: TEXT, fontFace: FONT, margin: 0,
  });
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_032_recreated.pptx" })
  .then(() => console.log("done"));
