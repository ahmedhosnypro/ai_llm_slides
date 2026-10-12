// Probe: verify pptxgenjs arc angleRange orientation + triangle flipV.
// Draws 4 arcs with known angleRange values + 2 triangles (normal / flipV),
// plus reference dots at known positions. Render and PIL-check.
const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "FFFFFF" };

const CX = 6.0, CY = 3.5, R = 2.0;
// arc bbox
const ax = CX - R, ay = CY - R, aw = 2 * R;
// Test arcs: angleRange [a,b]. Reference expectations (PowerPoint convention:
// 0 = 3 o'clock, positive angles CLOCKWISE). We test 4 bands:
s.addShape(pres.ShapeType.arc, { x: ax, y: ay, w: aw, h: aw, line: { color: "FF0000", width: 2 }, angleRange: [350, 360], fill: { type: "none" } });
s.addShape(pres.ShapeType.arc, { x: ax, y: ay, w: aw, h: aw, line: { color: "00AA00", width: 2 }, angleRange: [330, 350], fill: { type: "none" } });
s.addShape(pres.ShapeType.arc, { x: ax, y: ay, w: aw, h: aw, line: { color: "0000FF", width: 2 }, angleRange: [270, 330], fill: { type: "none" } });
s.addShape(pres.ShapeType.arc, { x: ax, y: ay, w: aw, h: aw, line: { color: "FF00FF", width: 2 }, angleRange: [300, 360], fill: { type: "none" } });

// reference tick dots at polar positions (deg CCW from 3 o'clock): magenta small circles
function dot(degCCW, rad, color) {
  const a = (degCCW * Math.PI) / 180;
  const x = CX + rad * Math.cos(a);
  const y = CY - rad * Math.sin(a);
  s.addShape(pres.ShapeType.ellipse, { x: x - 0.04, y: y - 0.04, w: 0.08, h: 0.08, fill: { color }, line: { color, width: 0.5 } });
}
dot(0, R, "111111");
dot(30, R, "111111");
dot(60, R, "111111");

// triangles: default vs flipV
s.addShape(pres.ShapeType.triangle, { x: 9.0, y: 1.0, w: 0.3, h: 0.36, fill: { color: "E06010" }, line: { type: "none" } });
s.addShape(pres.ShapeType.triangle, { x: 9.5, y: 1.0, w: 0.3, h: 0.36, fill: { color: "E06010" }, line: { type: "none" }, flipV: true });

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/probe_arcs.pptx" })
  .then(() => console.log("probe written"));
