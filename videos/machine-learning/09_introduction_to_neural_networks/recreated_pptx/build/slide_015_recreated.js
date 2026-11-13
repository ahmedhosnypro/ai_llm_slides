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

// Measured original box x77..664 y94..330, mapped into the house frame.
s.addImage({
  path: BUILD + "/slide_015_main_diagram.png",
  x: 0.46, y: 0.93, w: 9.04, h: 3.58,
});

const TT_X = 9.64, TT_Y = 1.36, TT_W = 3.37, TT_H = 2.57;
s.addShape(pres.shapes.RECTANGLE, {
  x: TT_X, y: TT_Y, w: TT_W, h: TT_H,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
const cellW = TT_W / 3;
const rowH = 0.42;
["X1", "X2", "O/P"].forEach((h, i) => {
  s.addText(h, {
    x: TT_X + i * cellW, y: TT_Y + 0.12, w: cellW, h: rowH,
    align: "center", valign: "middle", fontSize: 14, bold: true,
    color: BLACK, fontFace: FONT, margin: 0,
  });
});
const truthRows = [
  ["0", "0", "0"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"],
];
truthRows.forEach((row, r) => {
  row.forEach((v, c) => {
    const fill = c === 2 ? ((r === 0 || r === 3) ? CYAN : LIGHT_GREEN) : WHITE;
    s.addShape(pres.shapes.RECTANGLE, {
      x: TT_X + c * cellW, y: TT_Y + 0.54 + r * rowH, w: cellW, h: rowH,
      fill: { color: fill }, line: { color: RED, width: 0.75 },
    });
    s.addText(v, {
      x: TT_X + c * cellW, y: TT_Y + 0.54 + r * rowH, w: cellW, h: rowH,
      align: "center", valign: "middle", fontSize: 14, color: BLACK,
      fontFace: FONT, margin: 0,
    });
  });
});

const DT_X = 0.69, DT_Y = 4.72, DT_W = 8.58, DT_H = 2.23;
s.addShape(pres.shapes.RECTANGLE, {
  x: DT_X, y: DT_Y, w: DT_W, h: DT_H,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});
const dtCellW = DT_W / 8;
const dtRowH = 0.38;
["x2", "x1", "S1", "Z1", "S2", "Z2", "S3", "Z3"].forEach((h, i) => {
  s.addText(h, {
    x: DT_X + i * dtCellW, y: DT_Y + 0.08, w: dtCellW, h: dtRowH,
    align: "center", valign: "middle", fontSize: 12, bold: true,
    color: BLACK, fontFace: FONT, margin: 0,
  });
});
[2, 4, 6].forEach(pos => {
  s.addShape(pres.shapes.LINE, {
    x: DT_X + pos * dtCellW, y: DT_Y, w: 0, h: DT_H,
    line: { color: RED, width: 1.5 },
  });
});
const dataRows = [
  ["0", "0", "0", "0", "0", "1", "1", "1"],
  ["0", "1", "-1", "0", "-1", "0", "0", "0"],
  ["1", "0", "1", "1", "1", "1", "0", "0"],
  ["1", "1", "0", "0", "0", "1", "1", "1"],
];
dataRows.forEach((row, r) => {
  row.forEach((v, c) => {
    const fill = c === 7 ? ((r === 0 || r === 3) ? CYAN : LIGHT_GREEN) : WHITE;
    s.addShape(pres.shapes.RECTANGLE, {
      x: DT_X + c * dtCellW, y: DT_Y + 0.46 + r * dtRowH, w: dtCellW, h: dtRowH,
      fill: { color: fill }, line: { color: RED, width: 0.75 },
    });
    s.addText(v, {
      x: DT_X + c * dtCellW, y: DT_Y + 0.46 + r * dtRowH, w: dtCellW, h: dtRowH,
      align: "center", valign: "middle", fontSize: 12, color: BLACK,
      fontFace: FONT, margin: 0,
    });
  });
});

const CB_X = 9.64, CB_Y = 4.90, CB_W = 3.37, CB_H = 1.55;
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: CB_X, y: CB_Y, w: CB_W, h: CB_H,
  fill: { color: LIGHT_YELLOW }, line: { color: "AAAAAA", width: 0.75 },
});
s.addText("Adding Non-Linearity", {
  x: CB_X + 0.12, y: CB_Y + 0.15, w: CB_W - 0.24, h: 0.35,
  align: "center", valign: "middle", fontSize: 14, color: NAVY,
  fontFace: FONT, margin: 0,
});
s.addText("Solves the", {
  x: CB_X + 0.12, y: CB_Y + 0.57, w: CB_W - 0.24, h: 0.35,
  align: "center", valign: "middle", fontSize: 14, color: BLACK,
  fontFace: FONT, margin: 0,
});
s.addText([
  { text: "XOR", options: { color: "FF0000", fontSize: 14, bold: true, fontFace: FONT } },
  { text: " Problem", options: { color: BLACK, fontSize: 14, fontFace: FONT } },
], {
  x: CB_X + 0.12, y: CB_Y + 0.99, w: CB_W - 0.24, h: 0.35,
  align: "center", valign: "middle", margin: 0,
});

pres.writeFile({ fileName: BUILD + "/slide_015_recreated.pptx" })
  .then(() => console.log("wrote slide_015_recreated.pptx"));
