// slide_018_attempt5.js — Neural Net ∂E/∂w_ji ?  (slide 18 rebuild, b09 attempt5)
// Patterns: house-chrome, equations-mathtext-png
// Geometry measured from unique_slides/slide_018.jpg (960x540 px; x*13.33/960, y*7.5/540)
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5, FONT = "Arial", NUM = 18;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const X = (px) => px * 13.33 / 960;
const Y = (py) => py * 7.5 / 540;

// ---------- HOUSE CHROME ----------
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

// ---------- NETWORK DIAGRAM (single measured PNG, graph-panel-generated) ----------
s.addImage({
  path: "slide_018_diagram.png",
  x: X(358), y: Y(55), w: X(400), h: Y(153),
});

// ---------- ERROR COLUMN (measured red x760..773, y66..187; pink fill) ----------
s.addShape(pres.shapes.RECTANGLE, {
  x: X(761), y: Y(66), w: X(13), h: Y(121),
  fill: { color: "FFBAC3" }, line: { color: "C00000", width: 1 },
});
s.addText("Error Error Error", {
  x: X(760), y: Y(70), w: X(16), h: Y(113),
  align: "center", valign: "middle", rot: 270,
  fontSize: 8, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// ---------- EQUATION ∂E/∂w_ji ? (measured ink x831..866, y107..149 in orig) ----------
// eq_s18b.png is 199x223 px @600dpi with intrinsic ink bbox (8,8)-(191,215).
const TGT_H_IN = 42 / 540 * 7.5;
const INK_H_IN = 208 / 600;
const EQ_S = TGT_H_IN / INK_H_IN;
s.addImage({
  path: "eq_s18b.png",
  x: 831 / 960 * 13.33 - 8 / 600 * EQ_S,
  y: 107 / 540 * 7.5 - 8 / 600 * EQ_S,
  w: 199 / 600 * EQ_S, h: 223 / 600 * EQ_S,
});
// red "?" — target ink bbox (875,113)-(886,135) in the original
s.addText("?", {
  x: 879.5 / 960 * 13.33 - 0.114, y: 124 / 540 * 7.5 - 0.26, w: 0.34, h: 0.52,
  align: "center", valign: "middle",
  fontSize: 28, bold: true, color: "C00000", fontFace: "Cambria Math", margin: 0,
});

// ---------- CLASS LABELS (green text right of error bar) ----------
const CLASSES = ["Class 1", "Class 2", "Class m"];
const CLASS_Y = [85, 125, 171];
for (let r = 0; r < 3; r++) {
  s.addText(CLASSES[r], {
    x: X(776), y: Y(CLASS_Y[r] - 8), w: X(42), h: Y(16),
    align: "left", valign: "middle",
    fontSize: 11, bold: true, color: "3E7A28", fontFace: FONT, margin: 0,
  });
}

pres.writeFile({ fileName: "slide_018_recreated.pptx" })
  .then(() => console.log("wrote " + ("slide_018_recreated.pptx")))
  .catch(err => { console.error(err); process.exit(1); });
