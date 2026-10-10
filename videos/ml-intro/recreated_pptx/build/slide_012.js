const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

const BG = "E8E8E8";           // house-template background (founder rule 2026-10-09)
const HOUSE_RED = "C00000";    // house outer frame line
const RED = "C03028";          // title part 1 / red emphasis (spec colors.title_text)
const BLUE = "0000C8";         // 'Classification' + section headers — dark navy, corroborated by
                               // two vision reads of the original (old-deck judge ~#00008B,
                               // adjudication #0000C8; now also spec colors.accents)
const BORDER = "B03030";       // content box border (spec visual_elements)
const TEXT = "000000";         // body text
const WHITE = "FFFFFF";        // content box fill (spec colors.background)
const BADGE_YELLOW = "FFF9C4"; // house badge fill (founder rule)
const INK = "333333";          // house badge digit color (founder rule)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE FRAME (founder directive 2026-10-09 — overrides spec JSON):
// outer red frame = rectangle 0.15in inset from every edge, line C00000 width 1.5,
// fill E8E8E8 (invisible over background)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 },
});

// HOUSE FRAME: title text box starts y:0.28, x:0.6, w:12.13, align center.
// Spec: 'Supervised Learning:' red (#C03028), 'Classification' blue (#0000C8), underlined.
s.addText([
  { text: "Supervised Learning: ", options: { color: RED } },
  { text: "Classification", options: { color: BLUE, underline: true } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 1.15, align: "center", valign: "middle",
  fontSize: 40, bold: true, fontFace: FONT, margin: 0,
});

// HOUSE FRAME: slide-number badge = oval x:12.48 y:0.30 w:0.5 h:0.5,
// fill FFF9C4 line FFF9C4, numeral = SLIDE ID "12", bold 18pt, color 333333
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("12", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Content box: white fill, thin dark-red (#B03030) border, middle band of the
// slide (~15-95% height), spanning most of the slide width, below the title,
// inside the outer frame
s.addShape(pptx.shapes.RECTANGLE, {
  x: 1.07, y: 1.8, w: 11.2, h: 5.3,
  fill: { color: WHITE }, line: { color: BORDER, width: 1.5 },
});

// Single-column list inside the content box — 8 lines exactly per recreation_brief:
// 3 header lines (no bullet dots) + 4 content lines (round bullet dots) + 1 trailing
// empty bullet dot (mid-build state). Sub-bullets use round bullet dots.
const bu = () => ({ code: "2022", indent: 12 });
const body = [
  // Header 1: bold black, no bullet
  { text: "Problem Types:", options: { bold: true, color: TEXT, breakLine: true } },
  // Header 2: bold blue, no bullet — capital C per corroborated verbatim reads of the
  // original (old-deck judge attempt 1 + original adjudication read, both high-confidence)
  { text: "[1] Binary Classification:", options: { bold: true, color: BLUE, breakLine: true } },
  // Bullet: 'y is binary' red, remainder black. Bullet option on EVERY run of the
  // paragraph (pptxgenjs takes paragraph props from the breakLine-carrying run — a
  // bullet on only the first run of a multi-run line renders WITHOUT a dot, per
  // old-deck attempt 1 probe/judge evidence).
  { text: "y is binary", options: { color: RED, bullet: bu() } },
  { text: " (two classes: 0/1 or -1/+1)", options: { color: TEXT, bullet: bu(), breakLine: true } },
  // Bullet: all black
  { text: "Example: Spam Filtering (tell whether this email is spam or legitimate)",
    options: { color: TEXT, bullet: bu(), breakLine: true } },
  // Header 3: bold blue, no bullet — capital C per corroborated verbatim reads
  { text: "[2] Multi-class Classification:", options: { bold: true, color: BLUE, breakLine: true } },
  // Bullet: 'y is discrete' red, remainder black (bullet on every run, see above)
  { text: "y is discrete", options: { color: RED, bullet: bu() } },
  { text: " with one of K > 2 possible values", options: { color: TEXT, bullet: bu(), breakLine: true } },
  // Bullet: all black — grade list includes the plain "A," token per corroborated
  // verbatim reads of the original (old-deck judge attempt 1 + adjudication read)
  { text: "Example: Predicting your class grade (e.g., A, A\u2212, B+, B, B\u2212, other)",
    options: { color: TEXT, bullet: bu(), breakLine: true } },
  // Trailing empty bullet: round bullet dot with no text (mid-build state)
  { text: " ", options: { color: TEXT, bullet: bu() } },
];

s.addText(body, {
  x: 1.45, y: 2.05, w: 10.5, h: 4.8,
  align: "left", valign: "top",
  fontSize: 24, fontFace: FONT, margin: 0,
  paraSpaceAfter: 6,
});

// NOTE: the black mouse-cursor arrow from the video frame is deliberately NOT
// recreated (video-capture overlay, not slide artwork — recreation_brief step 15).

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_012_recreated.pptx" })
  .then(() => console.log("written: videos/ml-intro/recreated_pptx/slide_012_recreated.pptx"));
