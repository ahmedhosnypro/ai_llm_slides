// Slide 017 recreation — "Data Overfit and Underfit"
// Spec: analysis/slide_017_final.json (verbatim text, [?] markers kept, validation fixes applied)
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// Colors from the spec (never prefixed with '#')
const TITLE_RED = "CC0000";
const BODY_BLACK = "000000";
const BULLET1_RED = "8B0000";
const BULLET2_BLUE = "0000CC";
const GREEN_LEAD = "00AA00";
const FRAME_RED = "B03040";
const BADGE_FILL = "FFFACD";
const BADGE_OUTLINE = "4B0082";
const DOT_BLUE = "0000FF";
const CURVE_GREEN = "90EE90";
const CURVE_RED = "FF0000";
const AXIS_BLACK = "000000";

const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: "E8E8E8" };

// ---------------------------------------------------------------- frames
// HOUSE FRAME rule (2026-10-09, overrides spec JSON): outer red frame =
// x:0.15 y:0.15 w:13.03 h:7.2, line C00000 width 1.5, background E8E8E8
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: "E8E8E8", transparency: 100 },
  line: { color: "C00000", width: 1.5 },
});

// ---------------------------------------------------------------- title
// HOUSE FRAME rule: title box y:0.28, x:0.6, w:12.13, align center
s.addText("Data Overfit and Underfit", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.85, align: "center", valign: "middle",
  fontSize: 32, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

// ------------------------------------------------- slide number badge
// HOUSE FRAME rule: oval x:12.48 y:0.30 w:0.5 h:0.5, fill FFF9C4 line FFF9C4,
// slide's own number, bold 18pt, color 333333
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 1 },
});
s.addText("17", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// ------------------------------------------------------- inner content box
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.67, y: 1.35, w: 11.99, h: 5.4,
  fill: { color: "FFFFFF", transparency: 100 },
  line: { color: FRAME_RED, width: 1.5 },
});

// ------------------------------------------------------------ questions block
s.addText("Questions:-", {
  x: 1.3, y: 1.72, w: 5.6, h: 0.4, fontSize: 22, bold: true,
  color: BODY_BLACK, fontFace: FONT, margin: 0,
});

const bu = () => ({ code: "2022", indent: 12 });

// Bullet 1 — dark red; ONE round bullet, second line unbulleted (per original).
// Same pptxgenjs/LibreOffice quirk as Q2: literal glyph bullet, \n inside a
// bulleted run renders a second bullet in LibreOffice, so use two paragraphs.
s.addText([
  { text: "• ", options: { breakLine: false } },
  { text: "Which of the four red curves fits the data", options: { breakLine: true } },
  { text: "(blue dots) best?", options: { breakLine: false } },
], {
  x: 1.55, y: 2.35, w: 5.7, h: 0.85, fontSize: 17, color: BULLET1_RED,
  fontFace: FONT, margin: 0, valign: "top", paraSpaceAfter: 4,
});

// Bullet 2 — blue, 'generalize' underlined (hyperlink style); wraps after "the"
// per the original. NOTE: pptxgenjs starts a NEW paragraph for any run carrying
// bullet options, and LibreOffice honors the LAST per-run <a:pPr> (buNone kills
// the bullet), so the round bullet is drawn as a literal glyph run.
s.addText([
  { text: "• ", options: { breakLine: false } },
  { text: "Which curve is expected to ", options: { breakLine: false } },
  { text: "generalize", options: { underline: true, breakLine: false } },
  { text: " the", options: { breakLine: true } },
  { text: "best?", options: { breakLine: false } },
], {
  x: 1.55, y: 3.25, w: 5.7, h: 0.85, fontSize: 17, color: BULLET2_BLUE,
  fontFace: FONT, margin: 0, valign: "top", paraSpaceAfter: 4,
});

// Follow-up line — bold green lead-in + black regular text
s.addText([
  { text: "Are they both the same?", options: { bold: true, color: GREEN_LEAD } },
  { text: " If yes, why? If no, why not?", options: { color: BODY_BLACK, breakLine: false } },
], {
  x: 1.55, y: 4.35, w: 5.8, h: 0.85, fontSize: 16, color: BODY_BLACK,
  fontFace: FONT, margin: 0, valign: "top",
});

// ---------------- graphed: native plot approximation replaced by the
// generated graph image (build/assets/graphs/s017_graph_v1.png; 300dpi, baked
// container border + axes + fits; placed at the original frame's measured
// region, 1px = 1pt). Everything else is byte-identical to the certified build.
s.addImage({ path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s017_graph_v1.png",
               x: 7.66667, y: 1.81944, w: 4.44444, h: 2.59722 });

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_017_recreated.pptx" }).then(() => console.log("done"));
