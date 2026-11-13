const pptxgen = require("pptxgenjs");
const fs = require("fs");
const path = require("path");
const NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries";
const OUT = NS + "/recreated_pptx/slide_027_recreated.pptx";
const EQ = path.join(NS, "recreated_pptx/build/eq_027");
const MAN = JSON.parse(fs.readFileSync(path.join(EQ, "fix2_manifest.json"), "utf8"));
const W = 13.33, H = 7.5;
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// house chrome (overrides spec)
s.addShape(pres.shapes.RECTANGLE, { x: 0.15, y: 0.15, w: 13.03, h: 7.2, fill: { type: "none" }, line: { color: "C00000", width: 1.5 } });
s.addShape(pres.shapes.OVAL, { x: 12.48, y: 0.30, w: 0.5, h: 0.5, fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 } });
s.addText("27", { x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle", fontSize: 18, bold: true, color: "333333", fontFace: "Arial", margin: 0 });
s.addText("Polynomial Kernel", { x: 0.6, y: 0.28, w: 12.13, h: 0.55, align: "center", valign: "top", fontSize: 24, bold: true, color: "C00000", fontFace: "Times New Roman", margin: 0 });

const nx = r => ({ x: r[0] * W, y: r[1] * H, w: (r[2] - r[0]) * W, h: (r[3] - r[1]) * H });
function img(name, r) {
  const m = MAN[name], b = nx(r);
  s.addImage({ path: path.join(EQ, m.image), x: b.x, y: b.y + (b.h - m.h_in) / 2, w: m.w_in, h: m.h_in });
}

// inner content frame
s.addShape(pres.shapes.RECTANGLE, Object.assign(nx([0.063, 0.190, 0.934, 0.906]), { fill: { type: "none" }, line: { color: "7A1A1A", width: 1.5 } }));

// top-left vector definitions (2 stacked lines)
img("f2_def", [0.067, 0.216, 0.315, 0.290]);
img("f2_def2", [0.067, 0.290, 0.315, 0.335]);

// gray Remember panel with the remembered equation inside
s.addShape(pres.shapes.ROUNDED_RECTANGLE, Object.assign(nx([0.345, 0.224, 0.923, 0.344]), { fill: { color: "D5D5D5" }, line: { color: "D5D5D5" } }));
img("f2_rem", [0.350, 0.228, 0.920, 0.282]);
img("f2_rem2", [0.350, 0.282, 0.920, 0.340]);

// peach expansion block (3 lines)
s.addShape(pres.shapes.RECTANGLE, Object.assign(nx([0.073, 0.352, 0.885, 0.458]), { fill: { color: "FFE7C2" }, line: { color: "FFE7C2" } }));
img("f2_l1", [0.080, 0.356, 0.880, 0.386]);
img("f2_l2", [0.080, 0.388, 0.880, 0.418]);
img("f2_l3", [0.150, 0.420, 0.720, 0.452]);

// lower block: tan label + red phi(a) row + blue phi(b) column + = phi(a)^T phi(b)
s.addShape(pres.shapes.RECTANGLE, Object.assign(nx([0.073, 0.545, 0.230, 0.620]), { fill: { color: "FFE7C2" }, line: { color: "FFE7C2" } }));
img("f2_tan", [0.078, 0.560, 0.225, 0.610]);
img("f2_arow", [0.240, 0.560, 0.500, 0.610]);
img("f2_bcol", [0.510, 0.500, 0.640, 0.780]);
img("f2_eq", [0.650, 0.560, 0.800, 0.610]);

// Where lines + right x-column
img("f2_whereab", [0.312, 0.798, 0.520, 0.836]);
img("f2_wherex", [0.520, 0.798, 0.790, 0.836]);
img("f2_xcol", [0.800, 0.500, 0.930, 0.780]);

// red 2D => 6D
s.addText("2D \u21d2 6D", { x: 0.770 * W, y: 0.833 * H, w: 0.115 * W, h: 0.05 * H, fontSize: 13, bold: true, color: "C00000", fontFace: "Arial", margin: 0, align: "center", valign: "middle" });

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT)).catch(e => { console.error(e); process.exit(1); });
