// slide_035.js — REBUILD WAVE 3 rb4, from qa/reanalysis2/slide_035_analysis.txt only.
// Spec coords are normalized to the ORIGINAL capture frame [0.059,0.067,0.893,0.846];
// they are remapped onto the house red frame so content fills the slide like the original.
const pptxgen = require("pptxgenjs");
const path = require("path");

const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const EQ = path.join(NS, "recreated_pptx/build/eq_035/");
const W = 13.33, H = 7.5;
const FONT = "Arial", MATH = "Times New Roman";

const FX = [0.059, 0.067, 0.893, 0.846];
const HX = [0.15 / 13.33, 0.15 / 7.5, (0.15 + 13.03) / 13.33, (0.15 + 7.2) / 7.5];
const SX = (HX[2] - HX[0]) / (FX[2] - FX[0]);
const SY = (HX[3] - HX[1]) / (FX[3] - FX[1]);
const RM = (x0, y0, x1, y1) => ({
  x: (HX[0] + (x0 - FX[0]) * SX) * 13.33,
  y: (HX[1] + (y0 - FX[1]) * SY) * 7.5,
  w: (x1 - x0) * SX * 13.33,
  h: (y1 - y0) * SY * 7.5,
});
const imgInfo = (f) => require(path.join(EQ, f.replace(/\.png$/, ".json")));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// House chrome (mandatory, overrides spec)
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
});
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("35", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});
s.addText("How to Kernelize SVM", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: "C00000", fontFace: FONT, margin: 0,
});

// Three content panels: upper cream, middle white, lower cream (thin blue borders)
const pU = RM(0.071, 0.137, 0.875, 0.387);
const pM = RM(0.071, 0.394, 0.875, 0.580);
const pL = RM(0.071, 0.589, 0.875, 0.837);
s.addShape(pres.shapes.RECTANGLE, { ...pU, fill: { color: "F7F7DE" }, line: { color: "0000FF", width: 1 } });
s.addShape(pres.shapes.RECTANGLE, { ...pM, fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 } });
s.addShape(pres.shapes.RECTANGLE, { ...pL, fill: { color: "F7F7DE" }, line: { color: "0000FF", width: 1 } });

// White blue-bordered boxes holding the w and b equations (upper + lower)
const wB_U = RM(0.090, 0.228, 0.240, 0.311), bB_U = RM(0.347, 0.226, 0.736, 0.313);
const wB_L = RM(0.090, 0.680, 0.240, 0.763), bB_L = RM(0.347, 0.676, 0.736, 0.763);
for (const b of [wB_U, bB_U, wB_L, bB_L]) {
  s.addShape(pres.shapes.RECTANGLE, { ...b, fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 } });
}

// Peach callout boxes (upper + lower)
const cU = RM(0.125, 0.324, 0.486, 0.376), cL = RM(0.125, 0.774, 0.486, 0.830);
for (const c of [cU, cL]) {
  s.addShape(pres.shapes.RECTANGLE, { ...c, fill: { color: "FBE5D6" }, line: { color: "E8A87C", width: 1 } });
}
// Green highlight ovals (lower panel) drawn BEFORE the equation images so the
// transparent-PNG glyphs stay readable on top of the translucent-looking highlight
const lagU = RM(0.098, 0.157, 0.439, 0.233), lagLbox = RM(0.098, 0.611, 0.454, 0.689);
const idb = RM(0.281, 0.467, 0.590, 0.515);
const place = (file, box, align) => {
  const info = imgInfo(file);
  const aspect = info.w_px / info.h_px;
  let h = box.h * 0.98, w = h * aspect;
  if (w > box.w) { w = box.w; h = w / aspect; }
  const x = align === "right" ? box.x + box.w - w : align === "left" ? box.x : box.x + (box.w - w) / 2;
  const y = box.y + (box.h - h) / 2;
  return { x, y, w, h };
};
const imgLagL = place("fix_lag_lower.png", lagLbox, "right");
const imgB_L = place("fix_b_lower.png", bB_L, "center");
const oval = (x, y, w, h) => s.addShape(pres.shapes.OVAL, {
  x, y, w, h, fill: { color: "A6F3A6" }, line: { color: "2E9E2E", width: 1.25 },
});
const segOval = (r, info, label) => {
  const g = info.segments[label];
  oval(r.x + g[0] / 600 * r.w / (info.w_px / 600) - 0.03,
       r.y + g[2] / 600 * r.h / (info.h_px / 600) - 0.02,
       (g[1] - g[0]) / 600 * r.w / (info.w_px / 600) + 0.06,
       (g[3] - g[2]) / 600 * r.h / (info.h_px / 600) + 0.04);
};
segOval(imgLagL, imgInfo("fix_lag_lower.png"), "tail");
oval(imgB_L.x + 0.34 * imgB_L.w, imgB_L.y + 0.12 * imgB_L.h, 0.14 * imgB_L.w, 0.76 * imgB_L.h);
oval(imgB_L.x + 0.76 * imgB_L.w, imgB_L.y + 0.12 * imgB_L.h, 0.14 * imgB_L.w, 0.76 * imgB_L.h);
// around W^T Z in the lower callout
{
  const o = RM(0.345, 0.778, 0.385, 0.826);
  oval(o.x, o.y, o.w, o.h);
}

// Equation images at their rendered size (never rescaled aspect)
const img = (f, box, align) => {
  const r = place(f, box, align);
  s.addImage({ path: path.join(EQ, f), x: r.x, y: r.y, w: r.w, h: r.h });
};
img("fix_lag_upper.png", lagU, "left");
img("fix_lag_lower.png", lagLbox, "right");
img("fix_w.png", wB_U, "center");
img("fix_w.png", wB_L, "center");
img("fix_b_upper.png", bB_U, "center");
img("fix_b_lower.png", bB_L, "center");
img("rb4_ident.png", idb, "center");
// Middle panel texts (font sizes scaled by SY ~1.23)
const tU = (runs, box) => s.addText(runs, {
  x: box.x, y: box.y, w: box.w, h: box.h, align: "left", valign: "middle", margin: 0,
});
tU([{ text: "Remember :", options: { fontSize: 15, bold: true, italic: true, color: "0000FF", fontFace: FONT } }],
   RM(0.081, 0.400, 0.172, 0.428));
img("fix_mapping.png", RM(0.081, 0.433, 0.707, 0.467), "left");
img("fix_mapping2.png", RM(0.270, 0.475, 0.707, 0.515), "left");
img("fix_kernel.png", RM(0.081, 0.530, 0.813, 0.561), "left");
// Callout texts: "Class of vector Z ⇒ sign(W^T Z + b)" (upper: black/green/red/blue; lower: red/black)
const callout = (c, runs) => s.addText(runs, {
  x: c.x, y: c.y, w: c.w, h: c.h, align: "center", valign: "middle", margin: 0,
});
callout(cU, [
  { text: "Class of vector ", options: { fontSize: 16, color: "000000", fontFace: MATH } },
  { text: "Z", options: { fontSize: 16, bold: true, color: "2E9E2E", fontFace: MATH } },
  { text: " ⇒ ", options: { fontSize: 16, color: "FF0000", fontFace: MATH } },
  { text: "sign(", options: { fontSize: 16, italic: true, color: "FF0000", fontFace: MATH } },
  { text: "W", options: { fontSize: 16, color: "0000FF", fontFace: MATH } },
  { text: "T", options: { fontSize: 16, color: "0000FF", fontFace: MATH, superscript: true } },
  { text: " Z + b)", options: { fontSize: 16, color: "0000FF", fontFace: MATH } },
]);
callout(cL, [
  { text: "Class of vector ", options: { fontSize: 16, color: "000000", fontFace: MATH } },
  { text: "Z", options: { fontSize: 16, bold: true, color: "FF0000", fontFace: MATH } },
  { text: " ⇒ ", options: { fontSize: 16, color: "FF0000", fontFace: MATH } },
  { text: "sign(", options: { fontSize: 16, italic: true, color: "000000", fontFace: MATH } },
  { text: "W", options: { fontSize: 16, color: "000000", fontFace: MATH } },
  { text: "T", options: { fontSize: 16, color: "000000", fontFace: MATH, superscript: true } },
  { text: " Z + b)", options: { fontSize: 16, color: "000000", fontFace: MATH } },
]);

pres.writeFile({ fileName: path.join(NS, "recreated_pptx/slide_035_recreated.pptx") })
  .then(() => console.log("wrote slide_035_recreated.pptx"))
  .catch((err) => console.error(err));
