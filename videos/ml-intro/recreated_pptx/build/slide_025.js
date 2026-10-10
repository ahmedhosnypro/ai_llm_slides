// Slide 025 recreation — "Data Representation"
// Spec: videos/ml-intro/analysis/slide_025_final.json (verbatim text, layout, colors)
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

const WHITE = "FFFFFF", GRAY = "E0E0E0", RED = "C62828", INK = "212121",
      GREEN = "4CAF50", YELLOW = "FFF9C4", BLACK = "000000",
      BG = "E8E8E8", FRAME = "C00000";
const FONT = "Arial";
const HH = 1.0; // header band height

let s = pptx.addSlide();
s.background = { color: BG };

// 2. HOUSE FRAME (founder rule 2026-10-09): outer red frame, 0.15in inset, no visible fill
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME, width: 1.5 },
});

// 3. Light gray header band, full width inside the frame, top ~13% of slide height
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.16, y: 0.16, w: 13.01, h: HH,
  fill: { color: GRAY }, line: { color: GRAY, width: 0.5 },
});

// 4. Green doodle icons at far left of header: notepad, small plus sign, coffee cup
// Notepad body
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.50, y: 0.48, w: 0.42, h: 0.36,
  fill: { color: GRAY }, line: { color: GREEN, width: 2 },
});
// Notepad spiral rings (small green ovals straddling the top edge)
for (let i = 0; i < 4; i++) {
  s.addShape(pptx.shapes.OVAL, {
    x: 0.56 + i * 0.10, y: 0.44, w: 0.07, h: 0.06,
    fill: { color: GRAY }, line: { color: GREEN, width: 1.25 },
  });
}
// Small plus sign between the icons
s.addText("+", {
  x: 1.02, y: 0.38, w: 0.22, h: 0.52, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: GREEN, fontFace: FONT, margin: 0,
});
// Coffee cup: handle (ring) drawn first, then cup body over its left half
s.addShape(pptx.shapes.DONUT, {
  x: 1.62, y: 0.57, w: 0.15, h: 0.15,
  fill: { color: GRAY }, line: { color: GREEN, width: 1.5 },
});
s.addShape(pptx.shapes.TRAPEZOID, {
  x: 1.32, y: 0.52, w: 0.36, h: 0.32, flipV: true,
  fill: { color: GRAY }, line: { color: GREEN, width: 2 },
});
// Coffee cup steam (two short green lines above the cup)
s.addShape(pptx.shapes.LINE, {
  x: 1.42, y: 0.34, w: 0.03, h: 0.13,
  line: { color: GREEN, width: 1.5 },
});
s.addShape(pptx.shapes.LINE, {
  x: 1.54, y: 0.34, w: 0.03, h: 0.13,
  line: { color: GREEN, width: 1.5 },
});

// 5. Title: HOUSE FRAME title box (x:0.6 y:0.28 w:12.13, align center), bold red per spec
s.addText("Data Representation", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 6. HOUSE FRAME slide-number badge: oval x:12.48 y:0.30 w:0.5 h:0.5, fill/line FFF9C4,
//    slide's own number centered, bold 18pt, color 333333
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 1 },
});
s.addText("25", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 7. White content box with thin red border (~5-95% width, 15-95% height), rounded corners
//    (judge: original boxes are rounded-corner)
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.667, y: 1.125, w: W - 2 * 0.667, h: 6.0, rectRadius: 0.08,
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// 8-13. Bullets (verbatim text; subscripts via subscript runs; 'features' bold)
// NOTE (pptxgenjs): paragraph properties in the emitted XML are taken from the
// LAST run of each paragraph (LibreOffice honors the final <a:pPr>), so the
// bullet option must be present on every run of a bulleted paragraph.
const mainBu = { code: "2022", indent: 14 };       // round bullet
const subBu  = { code: "2013", indent: 12 };       // dash marker
const mainFs = 22, subFs = 18;

const runs = [];
// Bullet 1 (with subscripts on x1, y1, xN, yN)
runs.push({ text: "Data has form: {(x", options: { bullet: mainBu, fontSize: mainFs, breakLine: false } });
runs.push({ text: "1", options: { bullet: mainBu, subscript: true, fontSize: mainFs, breakLine: false } });
runs.push({ text: " , y", options: { bullet: mainBu, breakLine: false } });
runs.push({ text: "1", options: { bullet: mainBu, subscript: true, fontSize: mainFs, breakLine: false } });
runs.push({ text: "), . . . , (x", options: { bullet: mainBu, breakLine: false } });
runs.push({ text: "N", options: { bullet: mainBu, subscript: true, fontSize: mainFs, breakLine: false } });
runs.push({ text: " , y", options: { bullet: mainBu, breakLine: false } });
runs.push({ text: "N", options: { bullet: mainBu, subscript: true, fontSize: mainFs, breakLine: false } });
runs.push({ text: ")} (labeled), or {x", options: { bullet: mainBu, breakLine: false } });
runs.push({ text: "1", options: { bullet: mainBu, subscript: true, fontSize: mainFs, breakLine: false } });
runs.push({ text: " , . . . , x", options: { bullet: mainBu, breakLine: false } });
runs.push({ text: "N", options: { bullet: mainBu, subscript: true, fontSize: mainFs, breakLine: false } });
runs.push({ text: "} (unlabeled)", options: { bullet: mainBu, breakLine: true, paraSpaceAfter: 12 } });

// Bullet 2 ('features' bold)
runs.push({ text: "Each example X is a set of (numeric) ", options: { bullet: mainBu, fontSize: mainFs, breakLine: false } });
runs.push({ text: "features", options: { bullet: mainBu, bold: true, breakLine: false } });
runs.push({ text: " / attributes / dimensions", options: { bullet: mainBu, breakLine: true, paraSpaceAfter: 12 } });

// Bullet 3
runs.push({ text: "X is commonly represented as a D \u00D7 1 vector", options: { bullet: mainBu, fontSize: mainFs, breakLine: true, paraSpaceAfter: 8 } });

// Sub-bullet 1 (indented, dash, smaller)
runs.push({ text: "Representing a 28 \u00D7 28 image: x can be a 784 \u00D7 1 vector of pixel values", options: { bullet: subBu, indentLevel: 1, fontSize: subFs, breakLine: true, paraSpaceAfter: 8 } });

// Sub-bullet 2
runs.push({ text: "Representing a text document: x can be a vector of word-counts of words appearing in that document", options: { bullet: subBu, indentLevel: 1, fontSize: subFs } });

s.addText(runs, {
  x: 1.05, y: 1.55, w: 10.0, h: 5.2, align: "left", valign: "top",
  color: INK, fontFace: FONT, margin: 0, paraSpaceAfter: 10,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_025_recreated.pptx" })
  .then(() => console.log("done"))
  .catch((e) => { console.error(e); process.exit(1); });
