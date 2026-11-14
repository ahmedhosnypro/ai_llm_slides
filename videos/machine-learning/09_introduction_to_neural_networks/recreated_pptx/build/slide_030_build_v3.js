// Slide 030 v3: measured from unique_slides/slide_030.jpg (960x540, 72 px/in).
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };
const FONT = "Arial";
const SERIF = "Times New Roman";
const IN = 1 / 72; // original frame px -> inches

function px(v) { return v * IN; }
function text(str, x, y, w, h, o) {
  s.addText(str, Object.assign({
    x, y, w, h, fontFace: FONT, color: "000000", margin: 0,
  }, o));
}
function rect(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w, h,
    fill: fill ? { color: fill } : { type: "none" },
    line: lineColor ? { color: lineColor, width: lineW || 1 } : { type: "none" },
  });
}
function oval(cx, cy, d, fill, lineColor, lineW) {
  s.addShape(pres.shapes.OVAL, {
    x: cx - d / 2, y: cy - d / 2, w: d, h: d,
    fill: { color: fill }, line: { color: lineColor, width: lineW || 1 },
  });
}
function line(x1, y1, x2, y2, color, width, dash) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  s.addShape(pres.shapes.LINE, {
    x, y, w, h,
    flipV: y2 < y1,
    line: { color, width, dashType: dash || "solid", endArrowType: "triangle" },
  });
}
function bar(x, y, h, color) {
  s.addShape(pres.shapes.RECTANGLE, {
    x, y, w: 0.018, h, fill: { color }, line: { type: "none" },
  });
}

// House chrome (overrides all other geometry for these elements).
rect(0.15, 0.15, W - 0.3, H - 0.3, null, "C00000", 1.5);
oval(12.73, 0.55, 0.5, "FFF9C4", "FFF9C4", 1.5);
text("30", 12.48, 0.30, 0.5, 0.5, { align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333" });
text("Example", 0.6, 0.28, 12.13, 0.45, { align: "left", valign: "top", fontSize: 24, bold: true, color: "C00000", fontFace: SERIF });

// Title lozenge block, measured x=73..177 y=57..99 in the original.
rect(0.60, 0.28, 1.85, 0.85, null, "C00000", 1.2);
s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
  x: 0.66, y: 0.79, w: 1.65, h: 0.27,
  fill: { color: "F8CBAD" }, line: { color: "000000", width: 0.75 },
});
text("Bad Weights", 0.66, 0.79, 1.65, 0.27, { align: "center", valign: "middle", fontSize: 11 });

// Network panel: original x=187..847, y=57..250.
rect(px(187), px(57), px(660), px(193), "FFFFFF", "C00000", 1.5);

// Input labels, values, and straight vector bars (x=219/248, y=123..203).
text("x1", px(192), px(129), px(18), px(12), { fontSize: 12, italic: true, color: "0000FF", fontFace: SERIF });
text("x2", px(192), px(184), px(18), px(12), { fontSize: 12, italic: true, color: "0000FF", fontFace: SERIF });
bar(px(219), px(123), px(80), "000000");
bar(px(248), px(123), px(80), "000000");
text("7", px(232), px(129), px(12), px(15), { align: "center", fontSize: 14, bold: true });
text("4", px(231), px(181), px(14), px(14), { align: "center", fontSize: 14, bold: true });

// Hidden nodes 3/4/5: centers (423,92), (423,162), (422,230), d~29px.
const hidden = [
  { n: "3", o: "O3", cx: 423, cy: 92, oy: 65 },
  { n: "4", o: "O4", cx: 423, cy: 162, oy: 135 },
  { n: "5", o: "O5", cx: 422, cy: 230, oy: 203 },
];
for (const nd of hidden) {
  oval(px(nd.cx), px(nd.cy), px(29), "FFE699", "C00000", 1.2);
  text(nd.n, px(nd.cx - 15), px(nd.cy - 15), px(30), px(30), { align: "center", valign: "middle", fontSize: 13, bold: true });
  text(nd.o, px(432), px(nd.oy), px(20), px(12), { fontSize: 11, bold: true, italic: true, color: "0000FF", fontFace: SERIF });
}

// Output nodes 6/7: centers (617,135), (617,190), d~29px.
const outputs = [
  { n: "6", o: "O6", cx: 617, cy: 135, oy: 114 },
  { n: "7", o: "O7", cx: 617, cy: 190, oy: 172 },
];
for (const nd of outputs) {
  oval(px(nd.cx), px(nd.cy), px(29), "F4B183", "C00000", 1.2);
  text(nd.n, px(nd.cx - 15), px(nd.cy - 15), px(30), px(30), { align: "center", valign: "middle", fontSize: 13, bold: true });
  text(nd.o, px(664), px(nd.oy), px(24), px(13), { fontSize: 11, bold: true, italic: true, color: "0000FF", fontFace: SERIF });
}
text("Output", px(643), px(83), px(62), px(15), { fontSize: 13, bold: true, italic: true, color: "0000FF", fontFace: SERIF });
text("Target", px(741), px(84), px(51), px(13), { fontSize: 12, bold: true });

// Target vector bars and entries: bars x=751/780 y=120..200; values 0/1; t6/t7.
bar(px(751), px(120), px(80), "000000");
bar(px(780), px(120), px(80), "000000");
text("0", px(763), px(126), px(12), px(14), { align: "center", fontSize: 13, bold: true });
text("1", px(765), px(177), px(10), px(15), { align: "center", fontSize: 13, bold: true });
text("t6", px(799), px(128), px(15), px(14), { fontSize: 11, italic: true, color: "0000FF", fontFace: SERIF });
text("t7", px(799), px(182), px(15), px(13), { fontSize: 11, italic: true, color: "0000FF", fontFace: SERIF });

// Input-to-hidden edges and green input weights.
const inputYs = [136, 188];
const inputWeights = [
  ["0.1", 266, 123], ["0.2", 285, 104], ["0.3", 306, 125],
  ["0.4", 266, 191], ["0.5", 276, 173], ["0.6", 294, 205],
];
for (const hy of [92, 162, 230]) {
  for (const iy of inputYs) line(px(253), px(iy), px(408), px(hy), "404040", 0.8);
}
for (const [w, x, y] of inputWeights) text(w, px(x), px(y), px(22), px(11), { fontSize: 9, color: "008000" });

// Hidden-to-output edges and red weights 0.3/0.4/0.5 (duplicated per output, as in the original).
const hiddenWeights = [["0.3", 475, 104], ["0.4", 488, 161], ["0.5", 475, 213]];
for (const hy of [92, 162, 230]) {
  for (const oy of [135, 190]) line(px(438), px(hy), px(602), px(oy), "404040", 0.8);
}
for (const [w, x, y] of hiddenWeights) {
  text(w, px(x), px(y), px(20), px(10), { fontSize: 9, bold: true, color: "FF0000" });
  text(w, px(x + 22), px(y + 42), px(20), px(10), { fontSize: 9, bold: true, color: "FF0000" });
}

// Dashed output-to-target connectors.
line(px(632), px(135), px(751), px(135), "000000", 0.9, "dash");
line(px(632), px(190), px(751), px(190), "000000", 0.9, "dash");

// Forward header: original x=72..161 y=241..256, blue italic underlined.
text("Forward", px(72), px(241), px(90), px(16), { fontSize: 16, bold: true, italic: true, underline: true, color: "0000FF", fontFace: SERIF });

// Lower panels, measured: blue x=72..357 y=266..405 and x=72..602 y=417..508;
// green x=638..879 y=266..405 and x=638..879 y=417..508.
rect(px(72), px(266), px(285), px(139), "FFFFFF", "0000FF", 1.5);
rect(px(72), px(417), px(530), px(91), "FFFFFF", "0000FF", 1.5);
rect(px(638), px(266), px(241), px(139), "FFFFFF", "00B050", 1.5);
rect(px(638), px(417), px(241), px(91), "FFFFFF", "00B050", 1.5);

// Equation PNGs at exact 600-dpi size, baseline-aligned to the measured rows.
function addEq(name, xIn, baselineIn) {
  const side = JSON.parse(fs.readFileSync(path.join(__dirname, name + ".json"), "utf8"));
  const y = baselineIn - side.baseline_frac * side.h_in;
  s.addImage({ path: path.join(__dirname, name + ".png"), x: xIn, y, w: side.w_in, h: side.h_in });
}
const netRows = [
  ["eq030_net3_label", "eq030_net3_body", 296],
  ["eq030_net4_label", "eq030_net4_body", 343],
  ["eq030_net5_label", "eq030_net5_body", 390],
];
for (const [lab, body, base] of netRows) {
  addEq(lab, px(82), px(base));
  addEq(body, px(132), px(base));
}
const net67Rows = [
  ["eq030_net6_label", "eq030_net6_body", 446],
  ["eq030_net7_label", "eq030_net7_body", 487],
];
for (const [lab, body, base] of net67Rows) {
  addEq(lab, px(79), px(base));
  addEq(body, px(128), px(base));
}
const oRows = [
  ["eq030_o3_label", "eq030_o3_body", 306],
  ["eq030_o4_label", "eq030_o4_body", 351],
  ["eq030_o5_label", "eq030_o5_body", 396],
];
for (const [lab, body, base] of oRows) {
  addEq(lab, px(657), px(base));
  addEq(body, px(683), px(base));
}
const o67Rows = [
  ["eq030_o6_label", "eq030_o6_body", 458],
  ["eq030_o7_label", "eq030_o7_body", 503],
];
for (const [lab, body, base] of o67Rows) {
  addEq(lab, px(659), px(base));
  addEq(body, px(685), px(base));
}

pres.writeFile({ fileName: "slide_030_recreated.pptx" }).then(() => console.log("wrote slide_030_recreated.pptx"));
