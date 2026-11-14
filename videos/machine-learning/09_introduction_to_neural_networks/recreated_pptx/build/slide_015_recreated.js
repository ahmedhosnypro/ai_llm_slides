const pptxgen = require("pptxgenjs");

const NUM = 15;
const FONT = "Arial";
const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const BG = "E8E8E8";
const RED = "C00000";
const NAVY = "000080";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const CYAN = "00FFFF";
const LIGHT_GREEN = "90EE90";
const LIGHT_YELLOW = "FFFFE0";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText([
  { text: "Using Two Perceptron Layers with ", options: { color: NAVY, bold: true, fontSize: 28, fontFace: FONT } },
  { text: "non-Linearity", options: { color: "FF0000", bold: true, fontSize: 28, fontFace: FONT } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top", margin: 0,
});

const px = v => v / 72;
s.addImage({
  path: BUILD + "/slide_015_main_diagram.png",
  x: px(64.0), y: px(84.3), w: px(658.4), h: px(255.0),
});

const TT_X = px(674), TT_Y = px(123), TT_W = px(218), TT_H = px(170);
s.addShape(pres.shapes.RECTANGLE, {
  x: TT_X, y: TT_Y, w: TT_W, h: TT_H,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
const truthCols = [674, 744, 814, 891];
["X1", "X2", "O/P"].forEach((h, i) => {
  s.addText(h, {
    x: px(truthCols[i]), y: px(124), w: px(truthCols[i + 1] - truthCols[i]), h: px(36),
    align: "center", valign: "middle", fontSize: 14, bold: true,
    color: BLACK, fontFace: FONT, margin: 0,
  });
});
const truthRows = [
  ["0", "0", "0"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"],
];
const truthRowY = [160, 197, 231, 262];
const truthRowH = [37, 34, 31, 30];
const truthMarks = [CYAN, LIGHT_GREEN, LIGHT_GREEN, CYAN];
truthRows.forEach((row, r) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(840), y: px(truthRowY[r] + 2), w: px(24), h: px(27),
    fill: { color: truthMarks[r] }, line: { type: "none" },
  });
  row.forEach((v, c) => {
    s.addText(v, {
      x: px(truthCols[c]), y: px(truthRowY[r]), w: px(truthCols[c + 1] - truthCols[c]), h: px(truthRowH[r]),
      align: "center", valign: "middle", fontSize: 14, color: BLACK,
      fontFace: FONT, margin: 0,
    });
  });
});

const DT_X = px(92), DT_Y = px(344), DT_W = px(557), DT_H = px(147);
s.addShape(pres.shapes.RECTANGLE, {
  x: DT_X, y: DT_Y, w: DT_W, h: DT_H,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
[378, 405, 433, 463, 491].forEach(y => {
  s.addShape(pres.shapes.LINE, {
    x: DT_X, y: px(y), w: DT_W, h: 0,
    line: { color: RED, width: 0.75 },
  });
});
[210, 339, 472].forEach(x => {
  s.addShape(pres.shapes.LINE, {
    x: px(x), y: DT_Y, w: 0, h: DT_H,
    line: { color: RED, width: 1.5 },
  });
});
const dtCenters = [126, 167, 260, 306, 393, 437, 521, 565];
["x2", "x1", "S1", "Z1", "S2", "Z2", "S3", "Z3"].forEach((h, i) => {
  s.addText(h, {
    x: px(dtCenters[i] - 25), y: px(345), w: px(50), h: px(32),
    align: "center", valign: "middle", fontSize: 14, bold: true,
    color: BLACK, fontFace: FONT, margin: 0,
  });
});
const dataRows = [
  ["0", "0", "0", "0", "0", "1", "1", "1"],
  ["0", "1", "-1", "0", "-1", "0", "0", "0"],
  ["1", "0", "1", "1", "1", "1", "0", "0"],
  ["1", "1", "0", "0", "0", "1", "1", "1"],
];
const dataRowY = [379, 406, 434, 464];
const dataRowH = [26, 27, 29, 27];
const dataMarks = [CYAN, LIGHT_GREEN, LIGHT_GREEN, CYAN];
const dataMarkY = [380, 408, 435, 464];
const dataMarkH = [25, 24, 27, 26];
dataRows.forEach((row, r) => {
  s.addShape(pres.shapes.RECTANGLE, {
    x: px(553), y: px(dataMarkY[r]), w: px(24), h: px(dataMarkH[r]),
    fill: { color: dataMarks[r] }, line: { type: "none" },
  });
  row.forEach((v, c) => {
    s.addText(v, {
      x: px(dtCenters[c] - 25), y: px(dataRowY[r]), w: px(50), h: px(dataRowH[r]),
      align: "center", valign: "middle", fontSize: 14, color: BLACK,
      fontFace: FONT, margin: 0,
    });
  });
});

const CB_X = px(658), CB_Y = px(381), CB_W = px(238), CB_H = px(80);
s.addShape(pres.shapes.RECTANGLE, {
  x: CB_X, y: CB_Y, w: CB_W, h: CB_H,
  fill: { color: LIGHT_YELLOW }, line: { color: "AAAAAA", width: 0.75 },
});
s.addText("Adding Non-Linearity", {
  x: px(666), y: px(384), w: px(222), h: px(28),
  align: "center", valign: "middle", fontSize: 18, color: NAVY,
  fontFace: FONT, margin: 0,
});
s.addText("Solves the", {
  x: px(666), y: px(410), w: px(222), h: px(28),
  align: "center", valign: "middle", fontSize: 18, color: BLACK,
  fontFace: FONT, margin: 0,
});
s.addText([
  { text: "XOR", options: { color: "FF0000", fontSize: 18, bold: true, fontFace: FONT } },
  { text: " Problem", options: { color: BLACK, fontSize: 18, fontFace: FONT } },
], {
  x: px(666), y: px(434), w: px(222), h: px(28),
  align: "center", valign: "middle", margin: 0,
});

pres.writeFile({ fileName: BUILD + "/slide_015_recreated.pptx" })
  .then(() => console.log("wrote slide_015_recreated.pptx"));
