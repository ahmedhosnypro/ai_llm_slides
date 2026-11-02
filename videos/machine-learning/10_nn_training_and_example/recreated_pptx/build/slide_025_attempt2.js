// Slide 25: Vanishing and Exploding Gradients (house-chrome ML family)
const pptxgen = require("pptxgenjs");
const PptxGenJS = pptxgen.default || pptxgen;
const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const NUM = 25;
const FONT = "Arial";
const ASSETS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/qa/slide025/assets";

let s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("Vanishing and Exploding Gradients", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 28, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Blue section header
s.addText("Long Chain of Derivatives", {
  x: 0.87, y: 1.72, w: 3.4, h: 0.3,
  align: "left", valign: "middle",
  fontSize: 18, bold: true, color: "0000FF", fontFace: FONT, margin: 0,
});

// Equation boxes (peach + cream) with 2D mathtext PNGs
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.66, y: 2.25, w: 3.34, h: 0.95,
  fill: { color: "FFE6CC" }, line: { color: "E8C9A0", width: 0.75 },
});
s.addImage({ path: `${ASSETS}/eq25_1.png`, x: 0.74, y: 2.35, w: 3.15 });
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.66, y: 3.30, w: 3.01, h: 0.87,
  fill: { color: "FFF2CC" }, line: { color: "E8DFA0", width: 0.75 },
});
s.addImage({ path: `${ASSETS}/eq25_2.png`, x: 0.74, y: 3.39, w: 2.85 });

// ---- Neural network diagram ----
// Mirrors original: input dots -> Sigma -> f(box) -> Net/O -> Sigma -> f -> Net/O -> Sigma -> f -> O outputs,
// with red backward error-propagation arrows (curved) above each stage and w_ij labels.
const ROWY = [2.06, 2.78, 3.61];       // node row centers (in)
const IN_X = 4.42, H1_X = 5.42, F1_X = 6.12, NO1_X = 6.86, H2_X = 7.86, F2_X = 8.56, NO2_X = 9.30, H3_X = 10.30, F3_X = 11.00, OUT_X = 11.66;
const YEL = "FFD966", GRN = "00AA00", ORG = "FF9900", PUR = "800080", BLU = "0000FF";
const PANEL = "DAD0C4";
s.addShape(pres.shapes.RECTANGLE, {
  x: 4.05, y: 1.62, w: 8.42, h: 2.62,
  fill: { color: PANEL }, line: { color: "B0A695", width: 0.75 },
});

function circle(cx, cy, d, fill, lineColor) {
  s.addShape(pres.shapes.OVAL, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d,
    fill: { color: fill }, line: { color: lineColor || "000000", width: 1 },
  });
}
function box(cx, cy, w, h, fill) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: cx - w / 2, y: cy - h / 2, w, h,
    fill: { color: fill }, line: { color: "000000", width: 0.75 },
  });
}
function link(x1, y1, x2, y2) {
  // pptxgenjs LINE draws a diagonal across its bounding box
  s.addShape(pres.shapes.LINE, {
    x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: { color: "9A9A9A", width: 0.75 },
  });
}
function backArrow(x1, y1, x2, y2) {
  // red backward (error-propagation) arc: block ARC flipped vertically, open at top
  const x = Math.min(x1, x2), w = Math.abs(x2 - x1);
  s.addShape(pres.shapes.BLOCK_ARC, {
    x, y: y1 - 0.22, w: Math.max(w, 0.3), h: 0.3,
    fill: { type: "none" }, line: { color: "C00000", width: 1.25 },
    flipV: true, flipH: x2 < x1,
  });
}
function nodeLabel(txt, cx, cy, color) {
  s.addText(txt, {
    x: cx - 0.3, y: cy - 0.09, w: 0.6, h: 0.18, align: "center", valign: "middle",
    fontSize: 7, bold: true, color: color || "000000", fontFace: FONT, margin: 0,
  });
}

// columns: inputs, Sigma, f, Net/O(grn), Sigma, f, Net/O(org), Sigma, f, O(blue)
for (const y of ROWY) {
  circle(IN_X, y, 0.16, PUR);
  circle(H1_X, y, 0.42, YEL);
  box(F1_X, y, 0.30, 0.30, "FFFFFF");
  circle(NO1_X, y, 0.34, GRN, "006600");
  circle(H2_X, y, 0.42, YEL);
  box(F2_X, y, 0.30, 0.30, "FFFFFF");
  circle(NO2_X, y, 0.34, ORG, "CC6600");
  circle(H3_X, y, 0.42, YEL);
  box(F3_X, y, 0.30, 0.30, "FFFFFF");
  circle(OUT_X, y, 0.32, BLU, "000066");
  nodeLabel("Σ", H1_X, y); nodeLabel("f", F1_X, y);
  nodeLabel("Net", NO1_X, y - 0.24, "000000"); nodeLabel("O", NO1_X, y + 0.05, "000000");
  nodeLabel("Σ", H2_X, y); nodeLabel("f", F2_X, y);
  nodeLabel("Net", NO2_X, y - 0.24, "000000"); nodeLabel("O", NO2_X, y + 0.05, "000000");
  nodeLabel("Σ", H3_X, y); nodeLabel("f", F3_X, y); nodeLabel("O", OUT_X, y, "FFFFFF");
}
const stageX = [[IN_X, H1_X], [H1_X, F1_X], [F1_X, NO1_X], [NO1_X, H2_X],
                [H2_X, F2_X], [F2_X, NO2_X], [NO2_X, H3_X], [H3_X, F3_X], [F3_X, OUT_X]];
for (let i = 0; i < 3; i++) {
  for (let j = 0; j < 3; j++) {
    for (const [a, b] of stageX) link(a + 0.1, ROWY[i], b - 0.1, ROWY[j]);
  }
}
// red backward arrows along the top of each stage (error propagation)
for (const [a, b] of stageX) backArrow(b, ROWY[0] - 0.21, a, ROWY[0] - 0.21);
// w_ij labels on middle inter-layer links
const WLAB = ["w_ij", "w_ji", "w_kj"];
let wi = 0;
for (const [a, b] of [[NO1_X, H2_X], [NO2_X, H3_X]]) {
  for (let j = 0; j < 3; j++) {
    s.addText(WLAB[wi % 3], {
      x: (a + b) / 2 - 0.15, y: ROWY[j] - 0.02, w: 0.34, h: 0.14,
      align: "center", valign: "middle", fontSize: 7, italic: true, color: "404040", fontFace: FONT, margin: 0,
    });
  }
  wi++;
}
const OUTL = ["Output 1", "Output 2", "Output m"];
ROWY.forEach((y, i) => {
  s.addText(OUTL[i], {
    x: OUT_X + 0.18, y: y - 0.1, w: 0.85, h: 0.22,
    align: "left", valign: "middle",
    fontSize: 10, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
});

// weight labels "w" on a representative subset of input connections
for (let i = 0; i < 3; i++) {
  s.addText("w", {
    x: (IN_X + H1_X) / 2 - 0.1, y: ROWY[i] + 0.14, w: 0.2, h: 0.16,
    align: "center", valign: "middle",
    fontSize: 8, italic: true, color: "606060", fontFace: FONT, margin: 0,
  });
}

// vertical red Error bar + Class labels (right of panel, inside frame)
s.addShape(pres.shapes.RECTANGLE, {
  x: 12.02, y: 1.70, w: 0.20, h: 2.30, fill: { color: "C00000" }, line: { color: "C00000", width: 0.5 },
});
s.addText("Error  Error  Error", {
  x: 11.94, y: 1.78, w: 0.36, h: 2.1,
  align: "center", valign: "middle",
  fontSize: 8, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
const CLS = ["Class 1", "Class 2", "Class m"];
ROWY.forEach((y, i) => {
  box(12.28, y, 0.62, 0.24, "C6EFCE");
  s.addText(CLS[i], {
    x: 12.28, y: y - 0.12, w: 0.62, h: 0.24,
    align: "center", valign: "middle",
    fontSize: 9, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
});

// Node Bias icon + label; red 1.0 annotation
circle(4.45, 3.98, 0.30, PUR);
s.addText("1", {
  x: 4.45 - 0.15, y: 3.98 - 0.10, w: 0.30, h: 0.20, align: "center", valign: "middle",
  fontSize: 9, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
});
s.addText("Node Bias", {
  x: 4.82, y: 3.88, w: 1.0, h: 0.22,
  align: "left", valign: "middle",
  fontSize: 10, bold: true, color: "000000", fontFace: FONT, margin: 0,
});
s.addText("1.0", {
  x: 8.55, y: 3.86, w: 0.5, h: 0.22,
  align: "left", valign: "middle",
  fontSize: 11, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
// circled "1" bias markers under first and third hidden Sigma columns
for (const y of [ROWY[2] + 0.34]) {
  circle(H1_X, y, 0.24, PUR);
  s.addText("1", {
    x: H1_X - 0.12, y: y - 0.10, w: 0.24, h: 0.20, align: "center", valign: "middle",
    fontSize: 8, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
  circle(H3_X, y, 0.24, PUR);
  s.addText("1", {
    x: H3_X - 0.12, y: y - 0.10, w: 0.24, h: 0.20, align: "center", valign: "middle",
    fontSize: 8, bold: true, color: "FFFFFF", fontFace: FONT, margin: 0,
  });
}

// ---- Bottom charts ----
s.addText("Exploding Gradients", {
  x: 1.43, y: 4.46, w: 2.2, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addImage({ path: `${ASSETS}/chart25_relu.png`, x: 0.75, y: 4.83, w: 3.6, h: 2.4 });

s.addText("Vanishing Gradients", {
  x: 7.65, y: 4.68, w: 2.2, h: 0.25,
  align: "left", valign: "middle",
  fontSize: 16, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});
s.addImage({ path: `${ASSETS}/chart25_sigtanh.png`, x: 5.10, y: 5.05, w: 7.26, h: 2.04 });

pres.writeFile({ fileName: "slide_025_attempt2.pptx" })
  .then(() => console.log("wrote slide_025_attempt2.pptx"));
