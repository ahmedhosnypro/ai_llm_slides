// build/slide_008.js — slide 008 "Traditional RNN  Seq2Seq model / (Challenges)".
//
// DEPENDENCY CONTRACT: slide 8 = slide 6's certified composition + delta (pure superset).
// The base is drawn by require()-ing the CERTIFIED parent component — never re-derived:
//   require('./components/slide_006.js') -> renderBase(pptx, slide, opts)
// Delta (PIL-measured on unique_slides/slide_008.jpg, 960x540, 1px=1pt, scratch/slide008/):
//   1. "(Challenges)" second title line (bold blue, s8-only — absent in slide 6).
//   2. Light-blue callout box "[2] Sequential Processing" (underlined) /
//      "Can NOT do processing in Parallel" (line 1 bigger + underlined, measured).
//   3. Two "Wait / Till Processing X₁|X₂" boxes (UPPERCASE X — vision-verified on crops).
//   4. Three thin leader lines: callout right edge -> encoder red dot; wait1 -> vertical
//      drop at x≈207.5 ending on the encoder container top; wait2 -> vertical at x≈368.
//   5. Title block re-drawn +7px right (s8 frame measures the inherited title shifted
//     +7px vs slide 6's frame: per-word runs +6..8px uniform; frame is ground truth).
// Exclusions: scissors cursor artifact at the callout's right edge (recording overlay).
//
// Measured JPEG-core palette (same discipline as the certified parent):
//   callout fill (225,254,253) | box edge wash (163,178,204) | text cores (0,0,~115)
//   leader wash ~(172,170,190). No underline on the Wait boxes (pixel-verified rows empty).
//
// LAWS honored: playlist chrome via components/house_chrome.js (inside renderBase);
// verbatim text incl. double spaces; margin:0; explicit fontFace everywhere; explicit
// lineSpacing on the multi-line wait boxes; no '#' in hex; single-version deliverable.

const path = require("path");
const parent = require(path.join(__dirname, "components", "slide_006.js"));
const pptxgen = require("pptxgenjs");

const px = parent.px; // frame px -> inches (v/72)
const SANS = "Arial";

// delta palette (slide_008.jpg JPEG cores)
const C8 = {
  fill: "E1FEFD",     // light blue-cyan box fill
  edge: "A3B2CC",     // washed navy hairline border on the three boxes
  text: "000076",     // dark blue text cores
  leader: "7A76A0",   // leader hairlines; renders to the frame's washed (185,183,204) core
};

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// ---- BASE: parent certified composition (badge numeral 8; title re-drawn below) ----
parent.renderBase(pptx, slide, { numeral: 8, skip: ["title"] });

// inherited title block, shifted +7px right per s8 frame measurement
slide.addText("Traditional RNN  Seq2Seq model", {
  x: px(259.5), y: px(54.5), w: px(400), h: px(30),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 24, bold: true, color: parent.C.red,
});

// ---- DELTA --------------------------------------------------------------------

// (a) "(Challenges)" — second title line (measured ink x 376..533, rows 87..111)
slide.addText("(Challenges)", {
  x: px(254.5), y: px(79.5), w: px(400), h: px(32),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 26.5, bold: true, color: C8.text,
});

// (b) leader lines FIRST (boxes drawn after occlude their starts, as in the frame)
// callout right edge -> encoder red dot (observed (346.5,228)..(432.5,299), slope 1.211)
slide.addShape(pptx.ShapeType.line, {
  x: px(326), y: px(211), w: px(140), h: px(115.5),
  line: { color: C8.leader, width: 1 },
});
// wait1 leader: diagonal (184.5,271)->(207.5,286) then vertical to container top (305)
slide.addShape(pptx.ShapeType.line, {
  x: px(184.5), y: px(271), w: px(23), h: px(15),
  line: { color: C8.leader, width: 1 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(207.5), y: px(286), w: 0, h: px(19),
  line: { color: C8.leader, width: 1 },
});
// wait2 leader: diagonal (345,268.5)->(368,284) then vertical to container top (305)
slide.addShape(pptx.ShapeType.line, {
  x: px(345), y: px(268.5), w: px(23), h: px(15.5),
  line: { color: C8.leader, width: 1 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(368), y: px(284), w: 0, h: px(21),
  line: { color: C8.leader, width: 1 },
});

// (c) callout box (measured x 44..325, y 169..229)
slide.addShape(pptx.ShapeType.rect, {
  x: px(44), y: px(169), w: px(281), h: px(60),
  fill: { color: C8.fill }, line: { color: C8.edge, width: 0.75 },
});
// line 1 — bigger, underlined (measured ink x 77..293, cap 183..194, underline row 197)
slide.addText([
  { text: "[2] Sequential Processing", options: { underline: true } },
], {
  x: px(45), y: px(177.5), w: px(280), h: px(22),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 17.5, bold: true, color: C8.text,
});
// line 2 (measured ink x 59..313, rows 202..213)
slide.addText("Can NOT do processing in Parallel", {
  x: px(46), y: px(196.5), w: px(280), h: px(22),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 15.5, bold: true, color: C8.text,
});

// (d) wait box 1 (measured x 52..184, y 257..292)
slide.addShape(pptx.ShapeType.rect, {
  x: px(52), y: px(257), w: px(132), h: px(35),
  fill: { color: C8.fill }, line: { color: C8.edge, width: 0.75 },
});
slide.addText(
  [
    { text: "Wait", options: { underline: true, breakLine: true } },
    { text: "Till Processing X", options: {} },
    { text: "1", options: { fontSize: 9, subscript: true } },
  ],
  {
    x: px(52), y: px(257), w: px(132), h: px(35),
    align: "center", valign: "middle", margin: 0, lineSpacing: 16,
    fontFace: SANS, fontSize: 13.4, bold: true, color: C8.text,
  }
);

// (e) wait box 2 (measured x 213..345, y 255..289)
slide.addShape(pptx.ShapeType.rect, {
  x: px(213), y: px(255), w: px(132), h: px(34),
  fill: { color: C8.fill }, line: { color: C8.edge, width: 0.75 },
});
slide.addText(
  [
    { text: "Wait", options: { underline: true, breakLine: true } },
    { text: "Till Processing X", options: {} },
    { text: "2", options: { fontSize: 9, subscript: true } },
  ],
  {
    x: px(213), y: px(255), w: px(132), h: px(34),
    align: "center", valign: "middle", margin: 0, lineSpacing: 16,
    fontFace: SANS, fontSize: 13.4, bold: true, color: C8.text,
  }
);

const OUT = path.join(__dirname, "..", "slide_008_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
