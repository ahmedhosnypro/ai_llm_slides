const pptxgen = require("pptxgenjs");
const fs = require("fs");

// Slide 022: Derivatives of some Activation Functions.
// Geometry measured from unique_slides/slide_022.jpg at 960x540 (1 px = 1 pt = 1/72 in).
const NUM = 22;
const TITLE = "Derivatives of some Activation Functions";
const FONT = "Arial";
const BUILD = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const EQ = JSON.parse(fs.readFileSync(BUILD + "/equations_slide022/manifest.json", "utf8"));
const eq = Object.fromEntries(EQ.equations.map(e => [e.name, e]));

const BG = "E8E8E8";
const RED = "C00000";
const BLUE = "2B3FC4";
const GREEN = "1E8B1E";
const BLACK = "000000";
const YELLOW = "FFF9C4";
const PINK = "FAE9D7";
const PINK_LINE = "F09090";
const CREAM = "FEFFE8";
const CREAM_LINE = "8D89C6";
const P = (px) => px / 72;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// House chrome (overrides per-slide analysis/judge on frame, badge, title).
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
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Original inner blue frame and bottom capture bar.
s.addShape(pres.shapes.RECTANGLE, {
  x: P(70), y: P(108), w: P(824), h: P(397),
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 2 },
});
s.addShape(pres.shapes.RECTANGLE, {
  x: P(35), y: P(502), w: P(855), h: P(38),
  fill: { color: BLACK }, line: { type: "none" },
});

// Measured rounded panels: left definitions, right derivatives.
const rows = [
  { y: 122, h: 58, leftW: 397, rightW: 227, leftEq: "eq_relu_f", rightEq: "eq_relu_df", labelY: 132, arrowY: 153 },
  { y: 210, h: 58, leftW: 397, rightW: 227, leftEq: "eq_prelu_f", rightEq: "eq_prelu_df", labelY: 220, arrowY: 241 },
  { y: 297, h: 63, leftW: 397, rightW: 227, leftEq: "eq_elu_f", rightEq: "eq_elu_df", labelY: 307, arrowY: 328 },
  { y: 400, h: 52, leftW: 246, rightW: 145, leftEq: "eq_softplus_f", rightEq: "eq_softplus_df", labelY: 410, arrowY: 431 },
];
for (const r of rows) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: P(82), y: P(r.y), w: P(r.leftW), h: P(r.h),
    fill: { color: PINK }, line: { color: PINK_LINE, width: 1.5 },
  });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: P(598), y: P(r.y), w: P(r.rightW), h: P(r.h),
    fill: { color: CREAM }, line: { color: CREAM_LINE, width: 1.5 },
  });
  for (const [name, px, pw] of [[r.leftEq, 82, r.leftW], [r.rightEq, 598, r.rightW]]) {
    const e = eq[name];
    s.addImage({
      path: BUILD + "/equations_slide022/" + e.image,
      x: P(px) + (P(pw) - e.w_in) / 2,
      y: P(r.y) + (P(r.h) - e.h_in) / 2,
      w: e.w_in, h: e.h_in,
    });
  }
  s.addText("Derivative", {
    x: P(506), y: P(r.labelY), w: P(80), h: P(14),
    align: "center", valign: "middle", fontSize: 14, bold: false, italic: true,
    color: RED, fontFace: FONT, margin: 0,
  });
  s.addText("\u21d2", {
    x: P(528), y: P(r.arrowY), w: P(32), h: P(20),
    align: "center", valign: "middle", fontSize: 24, bold: true,
    color: RED, fontFace: FONT, margin: 0,
  });
}

pres.writeFile({ fileName: BUILD + "/slide_022_recreated.pptx" })
  .then(() => console.log("wrote slide_022_recreated.pptx"));
