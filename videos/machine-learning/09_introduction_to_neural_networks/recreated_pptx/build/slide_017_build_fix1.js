const pptxgen = require("pptxgenjs");

const NUM = 17;
const TITLE = "Linear and Unit Step Activation Functions";
const FONT = "Arial";
const BG = "E8E8E8";
const FRAME_RED = "C00000";
const BLACK = "000000";
const RED = "FF0000";
const TITLE_RED = "8B0000";
const BLUE = "4169E1";
const YELLOW = "FFF9C4";
const BADGE_TEXT = "333333";
const CREAM = "FAE9D7";
const SALMON = "C59C98";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

function px(v) { return v / 72; }
function line(x0, y0, x1, y1, color, width, arrow) {
  const opts = { x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0), line: { color, width } };
  if (arrow === "end") opts.line.endArrowType = "triangle";
  if (arrow === "start") opts.line.startArrowType = "triangle";
  s.addShape(pres.shapes.LINE, opts);
}
function text(str, x, y, w, h, size, color, opts = {}) {
  s.addText(str, Object.assign({ x: px(x), y: px(y), w: px(w), h: px(h), fontSize: size, color, fontFace: FONT, margin: 0 }, opts));
}
function panel(x, y, w, h) {
  s.addShape(pres.shapes.RECTANGLE, { x: px(x), y: px(y), w: px(w), h: px(h), fill: { type: "none" }, line: { color: BLUE, width: 1.5 } });
}
function callout(x, y, w, h) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: px(x), y: px(y), w: px(w), h: px(h), fill: { color: CREAM }, line: { color: SALMON, width: 2.25 } });
}

s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3, fill: { type: "none" }, line: { color: FRAME_RED, width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 } });
text(String(NUM), 12.48 * 72, 0.30 * 72, 36, 36, 18, BADGE_TEXT, { align: "center", valign: "middle", bold: true });
text(TITLE, 0.6 * 72, 0.28 * 72, 12.13 * 72, 0.55 * 72, 28, TITLE_RED, { align: "center", valign: "top", bold: true });

const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";

panel(309, 120, 286, 148);
line(334, 199, 576, 199, BLACK, 1, "end");
line(445, 132, 445, 260, BLACK, 1, "start");
text("f(x)", 375, 130, 36, 18, 12, BLACK, { align: "center", valign: "middle" });
text("x", 524, 198, 13, 19, 12, RED, { align: "left", valign: "top" });
line(398, 246, 562, 138, RED, 2);

callout(605, 176, 277, 26);
s.addImage({ path: BUILD_DIR + "/eq_017_linear.png", x: px(605), y: px(176), w: 2325 / 600, h: 225 / 600 });

panel(137, 289, 287, 148);
line(162, 369, 404, 369, BLACK, 1, "end");
line(273, 302, 273, 430, BLACK, 1, "start");
text("f(x)", 225, 288, 38, 19, 12, BLACK, { align: "center", valign: "middle" });
text("x", 368, 371, 14, 16, 12, RED, { align: "left", valign: "top" });
line(162, 369, 273, 369, RED, 2);
line(273, 369, 273, 324, RED, 2);
line(273, 324, 399, 324, RED, 2);
callout(115, 457, 300, 51);
s.addImage({ path: BUILD_DIR + "/eq_017_unipolar.png", x: px(117), y: px(459), w: 2475 / 600, h: 400 / 600 });

panel(487, 289, 287, 148);
line(512, 369, 757, 369, BLACK, 1, "end");
line(630, 304, 630, 430, BLACK, 1, "start");
text("f(x)", 558, 288, 33, 19, 12, BLACK, { align: "center", valign: "middle" });
text("x", 705, 371, 13, 16, 12, RED, { align: "left", valign: "top" });
line(519, 386, 630, 386, RED, 2);
line(630, 386, 630, 326, RED, 2);
line(630, 326, 757, 326, RED, 2);
callout(494, 457, 306, 51);
s.addImage({ path: BUILD_DIR + "/eq_017_bipolar.png", x: px(496), y: px(459), w: 2525 / 600, h: 400 / 600 });

pres.writeFile({ fileName: BUILD_DIR + "/slide_017_fix1.pptx" }).then(() => console.log("wrote fix1"));
