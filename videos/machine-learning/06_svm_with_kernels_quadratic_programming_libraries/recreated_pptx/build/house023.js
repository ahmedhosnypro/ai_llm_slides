// Shared house chrome for slides 023-033 (house frame rule, overrides spec geometry)
const W = 13.33, H = 7.5;
function house(pres, s, num) {
  s.background = { color: "E8E8E8" };
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
    fill: { type: "none" }, line: { color: "C00000", width: 1.5 },
  });
  s.addShape(pres.shapes.OVAL, {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
  });
  s.addText(String(num), {
    x: 12.48, y: 0.30, w: 0.5, h: 0.5,
    align: "center", valign: "middle",
    fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0,
  });
}
function title(s, text, y, color, size) {
  s.addText(text, {
    x: 0.6, y: y !== undefined ? y : 0.28, w: 12.13, h: 0.55,
    align: "center", fontSize: size || 26, bold: true,
    color: color || "C00000", fontFace: "Arial", margin: 0,
  });
}
// normalized [x1,y1,x2,y2] -> inches
function box(b) { return { x: b[0] * W, y: b[1] * H, w: (b[2] - b[0]) * W, h: (b[3] - b[1]) * H }; }
module.exports = { W, H, house, title, box };
