// Slide 023 — "Review: Cosine Similarity" (Deep Learning DSAI 308, Transformers — Part I)
//
// Geometry: ALL values PIL-measured from unique_slides/slide_023.jpg (960x540 px,
// 1 px = 1 pt = 1/72 in). House chrome = playlist shared module (founder directive
// 2026-10-11): white FFFFFF canvas, gray E9E9E7 panel x42..918 y45..540 with thin
// C00000 border, badge d36 at (893,71) FDFD96/6A5ACD ring, bold 333333 numeral.
// The ml-intro house values are superseded for this playlist.
//
// Equations: professional 2D format via matplotlib mathtext (STIX serif) -> 600dpi
// transparent PNG -> addImage at EXACT size, placed at the original's measured ink
// bbox (PAD 8px@600dpi subtracted from the image origin). cos_red placed at its own
// measured ink top; cos_black (taller \dfrac stack) centered on the original band
// center y=391px. Equation alignment closed-loop check runs before judging.
//
// Omitted: the gray pencil/pen presenter annotation inside the right circle
// (spec imagery + GROUND RULES (c): presenter artifact, not slide content).
//
// pptxgenjs laws: no '#' in hex, fontFace everywhere, margin:0, explicit
// lineSpacing on multi-line boxes (callout 20pt, cyan bar 22pt — measured pitch).

const pptxgen = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const IN = (px) => px / 72;              // 960x540 frame px -> inches
const PAD = 8 / 600;                     // render_eq.py transparent pad per side (in)

// measured palette (validated spec + frame samples)
const RED = "C00000", BLUE = "0000CC", BLACK = "000000", GREEN = "009900";
const CIRCLE_FILL = "FFFFCC", CYAN = "CCFFFF", PINK = "FFCCCC", MAXYEL = "FFFFCC";
const FONT = "Arial";

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();

// ---- 1) house chrome (panel + badge "23") ------------------------------------
// Panel via the shared module (numeral "" = badge skipped here). The badge is
// drawn AFTER the content below: this slide's top-right equations box (measured
// top y80) underlaps the playlist badge (bottom y89) exactly as in the original
// frame, where the badge sits ON TOP of the box corner. The badge re-emit at the
// end uses the module's own CHROME constants + badge branch verbatim — no
// hand-invented geometry (ml-intro values never used).
drawHouseChrome(pres, s, { numeral: "" });

// ---- 2) pale-yellow circle diagrams ------------------------------------------
// left circle fill x76..311 y133..368 -> center (193.5, 250.5) r 118
// right circle fill x518..753 y132..368 -> center (635.5, 250) r 118
s.addShape(pres.shapes.OVAL, {
  x: IN(75.5), y: IN(132.5), w: IN(236), h: IN(236),
  fill: { color: CIRCLE_FILL },
  line: { color: CIRCLE_FILL, width: 0, transparency: 100 },  // measured: no visible outline
});
s.addShape(pres.shapes.OVAL, {
  x: IN(517.5), y: IN(132), w: IN(236), h: IN(236),
  fill: { color: CIRCLE_FILL },
  line: { color: CIRCLE_FILL, width: 0, transparency: 100 },  // measured: no visible outline
});

// ---- 3) black double-headed axes (extend past the circles) --------------------
// L-horiz x72..314 @y250.5 | L-vert y110..393 @x194 | R-horiz x483..800 @y250.5 |
// R-vert y110..393 @x636.5
s.addShape(pres.shapes.LINE, {
  x: IN(72), y: IN(250.5), w: IN(242), h: 0,
  line: { color: BLACK, width: 1, beginArrowType: "triangle", endArrowType: "triangle" },
});
s.addShape(pres.shapes.LINE, {
  x: IN(194), y: IN(110), w: 0, h: IN(283),
  line: { color: BLACK, width: 1, beginArrowType: "triangle", endArrowType: "triangle" },
});
s.addShape(pres.shapes.LINE, {
  x: IN(483), y: IN(250.5), w: IN(317), h: 0,
  line: { color: BLACK, width: 1, beginArrowType: "triangle", endArrowType: "triangle" },
});
s.addShape(pres.shapes.LINE, {
  x: IN(636.5), y: IN(110), w: 0, h: IN(283),
  line: { color: BLACK, width: 1, beginArrowType: "triangle", endArrowType: "triangle" },
});

// ---- 4) (no green arc: the frame's only green ink is the theta glyph itself —
// dense-region crop comparison confirmed no separate arc in the original) --------

// ---- 5) vectors (origin -> measured tip; arrowhead = line end) ----------------
// L-b (194,250.5)->(231.5,186.5) 59.6deg | L-a ->(356,206) 15.4deg
// R-b (636.5,250.5)->(696,150) 59.4deg  | R-a ->(752,221.5) 14.1deg
function vec(x0, y0, x1, y1, color) {
  s.addShape(pres.shapes.LINE, {
    x: IN(x0), y: IN(y1), w: IN(x1 - x0), h: IN(y0 - y1), flipV: true,
    line: { color, width: 1.5, endArrowType: "triangle" },
  });
}
vec(194, 250.5, 231.5, 186.5, BLUE);
vec(194, 250.5, 356, 206, RED);
vec(636.5, 250.5, 696, 150, BLUE);
vec(636.5, 250.5, 752, 221.5, RED);

// ---- 6) vector labels (bold italic, at measured blob centers) -----------------
function label(txt, cx, cy, color, size, underline, serif) {
  s.addText(txt, {
    x: IN(cx) - 0.3, y: IN(cy) - 0.25, w: 0.6, h: 0.5,
    align: "center", valign: "middle", fontSize: size, bold: false, italic: true,
    underline: underline, color, fontFace: serif ? "Times New Roman" : FONT, margin: 0,
  });
}
label("b", 206.5, 201.5, BLUE, 17, true, false);   // L b  (blob 202..211, 194..209)
label("a", 285, 213.5, RED, 15, true, false);      // L a  (blob 280..290, 208..219)
label("b", 649, 201.5, BLUE, 17, true, false);     // R b  (blob 644..654, 194..209)
label("a", 727.5, 213.5, RED, 15, true, false);    // R a  (blob 722..733, 208..219)
// theta rendered as STIX mathtext PNG (round glyph, W:H~0.75, matches the frame's
// theta blob 14x17px; Times/Arial thetas are too narrow or too heavy - crop verdicts)
// ink centers at the measured blob centers (214.5,233.5) and (659.5,233)
s.addImage({ path: `${ASSETS}/eq_theta.png`,
  x: IN(214.5 - 11.3 / 2) - PAD, y: IN(233.5 - 16.6 / 2) - PAD, w: 0.18333, h: 0.25667 });
s.addImage({ path: `${ASSETS}/eq_theta.png`,
  x: IN(659.5 - 11.3 / 2) - PAD, y: IN(233 - 16.6 / 2) - PAD, w: 0.18333, h: 0.25667 });

// ---- 7) Normalize block arrow between the circles -----------------------------
// red outline bbox x390..487 y227..275; white fill; red italic text
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: IN(390), y: IN(227), w: IN(97), h: IN(48),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2.5 },
});
// 'Normalize' centered on the SHAFT (orig ink y246..255, shaft center x~420),
// not the whole-shape center (the head shifts the shape centroid right)
s.addText("Normalize", {
  x: IN(420) - 0.6, y: IN(250.5) - 0.2, w: 1.2, h: 0.4,
  align: "center", valign: "middle", fontSize: 14, italic: true,
  color: RED, fontFace: FONT, margin: 0,
});

// ---- 8) white blue-bordered boxes ---------------------------------------------
function wbox(x, y, w, h) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: IN(x), y: IN(y), w: IN(w), h: IN(h),
    fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 },
  });
}
// callout x294..535 y102..177
wbox(294, 102, 241, 75);
// top-right equations box x740..916 y80..187
wbox(740, 80, 176, 107);
// bottom-center equations box x294..529 y322..427
wbox(294, 322, 235, 105);
// after-normalization box x748..909 y314..380
wbox(748, 314, 161, 66);

// callout text: 3 centered lines, pitch 20px (lineSpacing 20pt), 'normalized' bold blue
s.addText(
  [
    { text: "Vectors must be ", options: { color: BLUE, charSpacing: 0.5 } },
    { text: "normalized", options: { color: BLUE, bold: true, charSpacing: 0.5, breakLine: true } },
    { text: "before calculate similarity", options: { color: BLUE, charSpacing: 0.5, breakLine: true } },
    { text: "Their Lengths = 1", options: { color: BLUE, charSpacing: 0.5 } },
  ],
  {
    x: IN(296), y: IN(104), w: IN(237), h: IN(71),
    align: "center", valign: "middle", fontSize: 16.5, fontFace: FONT,
    lineSpacing: 20, margin: 0,
  }
);

// ---- 9) equations (mathtext PNGs at exact measured ink positions) --------------
// ink(px) -> image origin = ink/72 - PAD
function eq(name, inkX, inkY, wIn, hIn) {
  s.addImage({
    path: `${ASSETS}/${name}.png`,
    x: IN(inkX) - PAD, y: IN(inkY) - PAD, w: wIn, h: hIn,
  });
}
eq("eq_a", 747, 84, 2.27833, 0.61167);     // Normalized a = a/|a|   (band 84..125)
eq("eq_b", 747, 133, 2.27833, 0.68333);    // Normalized b = b/|b|   (band 133..179)
eq("eq_dot", 302, 336, 3.135, 0.37);       // a.b = a^T b = |a||b|cos(th) (336..358)
eq("cos_red", 317, 379, 0.87667, 0.33);    // cos(th) red bold       (379..401)
// cos_black: taller \dfrac stack (56.2px vs orig 51) -> centered on band center 391
eq("cos_black", 383, 391 - 56.2 / 2, 1.79, 0.80667);  // = frac = a^T b (366..416)
eq("eq_unit", 760, 348, 1.41333, 0.34);    // |a| = |b| = 1 underlined (348..368)

// 'After Normalization' text line (ink y329..340, center x ~831)
s.addText("After Normalization", {
  x: IN(751), y: IN(334.5) - 0.25, w: IN(161), h: 0.5,
  align: "center", valign: "middle", fontSize: 16.8, color: BLACK,
  fontFace: "Times New Roman", margin: 0,
});

// ---- 10) cyan summary bar x53..865 y432..490 -----------------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: IN(53), y: IN(432), w: IN(812), h: IN(58),
  fill: { color: CYAN }, line: { color: BLUE, width: 1.5 },
});
// text left-aligned at x64, two lines, pitch 22px (lineSpacing 22pt), blue
s.addText(
  [
    { text: "Cosine Similarity is between ", options: { charSpacing: 1.95 } },
    { text: "-1 , +1", options: { bold: true, charSpacing: 1.5, breakLine: true } },
    { text: "It is a ", options: { charSpacing: 1.85 } },
    { text: "dot product", options: { underline: true, charSpacing: 1.85 } },
    { text: " between two Normalized vectors ", options: { charSpacing: 1.85 } },
    { text: "a", options: { bold: true, charSpacing: 1.85 } },
    { text: " and ", options: { charSpacing: 1.85 } },
    { text: "b", options: { bold: true, charSpacing: 1.85 } },
  ],
  {
    x: IN(64), y: IN(434), w: IN(780), h: IN(54),
    align: "left", valign: "middle", fontSize: 16, color: BLUE,
    fontFace: FONT, lineSpacing: 22, margin: 0,
  }
);

// ---- 11) bottom accent boxes ----------------------------------------------------
// Maximize x110..526 y496..533 (yellow fill, red border, black text)
s.addShape(pres.shapes.RECTANGLE, {
  x: IN(110), y: IN(496), w: IN(416), h: IN(37),
  fill: { color: MAXYEL }, line: { color: RED, width: 1.5 },
});
s.addText("Maximize [Similarity] = Minimize -[Similarity]", {
  x: IN(110), y: IN(496), w: IN(416), h: IN(37),
  align: "center", valign: "middle", fontSize: 20, color: BLACK,
  fontFace: FONT, margin: 0,
});
// Loss x567..766 y497..534 (pink fill, red border, red bold text)
s.addShape(pres.shapes.RECTANGLE, {
  x: IN(567), y: IN(497), w: IN(199), h: IN(37),
  fill: { color: PINK }, line: { color: RED, width: 1.5 },
});
s.addText("Loss = -[Similarity]", {
  x: IN(567), y: IN(497), w: IN(199), h: IN(37),
  align: "center", valign: "middle", fontSize: 19.5, bold: true, color: RED,
  fontFace: FONT, margin: 0,
});

// ---- 12) title (ink x248..597 y67..94, center x 422.5) --------------------------
s.addText("Review: Cosine Similarity", {
  x: IN(422.5) - 3.8, y: 0.741, w: 7.6, h: 0.66,
  align: "center", valign: "middle", fontSize: 29, bold: true,
  color: RED, fontFace: FONT, margin: 0,
});

// ---- 13) badge ON TOP (z-order fix; constants verbatim from house_chrome.js) ----
{
  const bx = CHROME.badge.cx - CHROME.badge.d / 2;
  const by = CHROME.badge.cy - CHROME.badge.d / 2;
  s.addShape(pres.shapes.OVAL, {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    fill: { color: CHROME.badge.fill },
    line: { color: CHROME.badge.ring, width: CHROME.badge.ringWidth },
  });
  s.addText("23", {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    align: "center", valign: "middle", bold: true,
    fontSize: CHROME.badge.numeralSize, color: CHROME.badge.numeralColor,
    fontFace: CHROME.badge.fontFace, margin: 0,
  });
}

pres.writeFile({
  fileName:
    "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_023_recreated.pptx",
}).then(() => console.log("OK slide_023_recreated.pptx"));
