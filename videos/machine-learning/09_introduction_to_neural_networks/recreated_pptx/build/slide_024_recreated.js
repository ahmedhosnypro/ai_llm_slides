const path = require("path");
const pptxgen = require("pptxgenjs");

const NUM = 24;
const BUILD = __dirname;
const EQ = require(path.join(BUILD, "eq_s024_manifest.json"));

const W = 13.33, H = 7.5;
const BG = "E8E8E8";
const FRAME_RED = "C00000";
const TITLE_RED = "A80000";
const UNDERLINE_RED = "FF0000";
const BLACK = "000000";
const DARK = "333333";
const RED = "CC0000";
const BLUE = "0000CC";
const ORANGE_BORDER = "ED7D31";
const PINK_BORDER = "FF7C80";
const BLUE_BORDER = "4472C4";
const GRAY_BORDER = "BFBFBF";
const PEACH = "FDEADA";
const WHITE = "FFFFFF";
const BADGE = "FFF9C4";

const P = (px) => px / 72;

function panel(s, x, y, w, h, fill, border) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: P(x), y: P(y), w: P(w), h: P(h),
    fill: { color: fill }, line: { color: border, width: 1 },
  });
}

function eq(s, name, inkX, inkY) {
  const e = EQ.equations[name];
  s.addImage({
    path: path.join(BUILD, e.image),
    x: P(inkX) - e.ink_bbox_px[0] / 600,
    y: P(inkY) - e.ink_bbox_px[1] / 600,
    w: e.width_in, h: e.height_in,
  });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: BG };

s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: FRAME_RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 18, bold: true,
  color: "333333", fontFace: "Arial", margin: 0,
});
s.addText("For Sigmoid Function", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "left", valign: "top", fontSize: 24, bold: true, italic: true,
  color: TITLE_RED, fontFace: "Liberation Serif", margin: [0, 0, 0, 47],
});
s.addShape(pres.shapes.RECTANGLE, {
  x: P(90), y: 0.78, w: P(221), h: 0.025,
  fill: { color: UNDERLINE_RED }, line: { color: UNDERLINE_RED, width: 0.25 },
});

panel(s, 83, 101, 246, 58, PEACH, PINK_BORDER);
eq(s, "sigmoid", 93, 108);
panel(s, 627, 104, 220, 48, WHITE, BLUE_BORDER);
eq(s, "remember", 637, 105);
panel(s, 85, 162, 607, 75, WHITE, GRAY_BORDER);
eq(s, "step1", 90, 165);
panel(s, 85, 243, 524, 148, WHITE, GRAY_BORDER);
eq(s, "step2a", 95, 245);
eq(s, "step2b", 170, 305);
panel(s, 638, 248, 218, 127, PEACH, ORANGE_BORDER);
s.addText("Sigmoid (aka Logistic function)", {
  x: P(646), y: P(258), w: P(200), h: P(22),
  align: "left", valign: "top", fontSize: 16, bold: true,
  color: RED, fontFace: "Liberation Serif", margin: 0,
});
s.addText([
  { text: "It is a ", options: { color: BLACK, fontSize: 15, fontFace: "Liberation Serif" } },
  { text: "squashing", options: { color: BLACK, fontSize: 15, bold: true, fontFace: "Liberation Serif" } },
  { text: " function used to\n", options: { color: BLACK, fontSize: 15, fontFace: "Liberation Serif" } },
  { text: "convert an ", options: { color: BLACK, fontSize: 15, fontFace: "Liberation Serif" } },
  { text: "unbounded", options: { color: RED, fontSize: 15, underline: true, fontFace: "Liberation Serif" } },
  { text: " values to a\n", options: { color: BLACK, fontSize: 15, fontFace: "Liberation Serif" } },
  { text: "bounded", options: { color: RED, fontSize: 15, underline: true, fontFace: "Liberation Serif" } },
  { text: " ", options: { color: BLACK, fontSize: 15, fontFace: "Liberation Serif" } },
  { text: "probabilistic", options: { color: BLUE, fontSize: 15, bold: true, fontFace: "Liberation Serif" } },
  { text: " space", options: { color: BLACK, fontSize: 15, fontFace: "Liberation Serif" } },
], {
  x: P(646), y: P(293), w: P(200), h: P(78),
  align: "left", valign: "top", margin: 0, lineSpacing: 22,
});
s.addText("(from 0 to 1)", {
  x: P(638), y: P(348), w: P(218), h: P(20),
  align: "center", valign: "top", fontSize: 13, italic: true,
  color: RED, fontFace: "Liberation Serif", margin: 0,
});
panel(s, 85, 412, 412, 60, WHITE, GRAY_BORDER);
eq(s, "step3", 96, 426);
panel(s, 525, 429, 331, 43, PEACH, ORANGE_BORDER);
eq(s, "final", 527, 432);

pres.writeFile({ fileName: path.join(BUILD, "slide_024_recreated.pptx") })
  .then(() => console.log("wrote slide_024_recreated.pptx"));
