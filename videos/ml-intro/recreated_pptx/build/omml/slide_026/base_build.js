// Slide 026 recreation — "Some Notations" (ml-intro, new numbering; old deck id 34)
// Spec: videos/ml-intro/analysis/slide_026_final.json (validated, PASS_WITH_FIXES, score 9).
// House frame (founder directive 2026-10-09) overrides spec for outer chrome:
//   bg E8E8E8, red frame 0.15in inset, badge oval x12.48 y0.30 w0.5 h0.5 fill FFF9C4,
//   title box y0.28 x0.6 w12.13 centered. Badge numeral reads exactly "26".
//
// MATH REWORK (founder directive 2026-10-09, professional-2D rule): every stacked
// math cluster on this notation-dense slide is a matplotlib-mathtext PNG
// (600dpi, transparent, exact pt size) embedded via the CERTIFIED mechanism from
// qa/scratch_math/ (render_eq.py + scratch_build.js pattern, vision-PASS 2026-10-09):
//   R^D, x ∈ R^D, x^T, R^{N×D}, X ∈ R^{N×D} (18pt), the highlighted set fragment
//   {(x1,y1), …, (xN,yN)} as (X,Y) (18pt), x_ij (13pt), the diagram chip labels
//   x_1/x_N/y_1/y_N (14pt), the matrix row labels x_11…x_1D / x_N1…x_ND (13pt),
//   and the diagram lead-ins X =, =, Y = (18pt) and the vdots glyphs (9pt).
// Prose, dimension phrases ("D × 1", "N × D"), and single non-stacked letters stay
// native text.
//
// CORRECTIVE PASS (founder EQUATION ALIGNMENT LAW, 2026-10-10, after judge attempt 5
// PASS was withheld): vertical placement of every equation image now uses the
// BASELINE LAW  y = baseline_in − baseline_frac × h_in  (sidecar baseline_frac),
// never center-on-line; horizontal placement is PIL-measured from the original
// frame (videos/ml-intro/unique_slides/slide_026.jpg, 960×540, 1px = 1pt):
// every equation's ink left edge / center and every text baseline is taken from
// the original pixel forensics. Closed-loop PIL verification against render_6.png
// at 150dpi (scale 150/72) is mandatory before the re-judge.
const pptxgenpkg = require("pptxgenjs");
const fs = require("fs");
const path = require("path");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// House template colors
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE = "FFF9C4", INK = "333333";
// Spec content colors
const RED = "C00000", TEXT = "000000", TAN = "E8D9B5",
      YELLOW = "F4E04D", GREEN = "7BE8A0", MAGENTA = "E86DE8", CYAN = "5FE8E8";
const FONT = "Arial";
const BUL = "2020A0"; // blue lecture bullet markers (judge, attempt 3: original's are blue)

// ---------- equation embedding contract (certified, qa/scratch_math) ----------
// EQUATION ALIGNMENT LAW (founder 2026-10-10): the math baseline of the image sits
// on the surrounding text baseline: y = baseline_in - baseline_frac * h_in.
const ASSETS = path.join(__dirname, "assets");
const PAD = 8 / 600; // PNG pad baked by render_eq.py (8px @ 600dpi)
function loadEq(name) {
  const eq = JSON.parse(fs.readFileSync(path.join(ASSETS, "eq_026_" + name + ".json"), "utf8"));
  eq.path = path.join(ASSETS, "eq_026_" + name + ".png"); // absolute, cwd-independent
  return eq;
}
function addEq(slide, eq, xIn, baselineIn) {          // baseline-anchored (the LAW)
  slide.addImage({ path: eq.path, x: xIn,
    y: baselineIn - eq.baseline_frac * eq.h_in,
    w: eq.w_in, h: eq.h_in });                        // NEVER rescale: exact pt size
}
function addEqInkTop(slide, eq, xIn, inkTopIn) {      // ink-top-anchored (chip labels)
  slide.addImage({ path: eq.path, x: xIn, y: inkTopIn - PAD, w: eq.w_in, h: eq.h_in });
}
function addEqCenter(slide, eq, cxIn, cyIn) {         // center-anchored (vdots)
  slide.addImage({ path: eq.path, x: cxIn - eq.w_in / 2, y: cyIn - eq.h_in / 2,
    w: eq.w_in, h: eq.h_in });
}

// Rendered equations (all ink #000000; pt sizes match the surrounding native text)
const EQ_RD      = loadEq("rd");      // \mathbb{R}^D                        18pt
const EQ_XIN_RD  = loadEq("xin_rd");  // \mathbf{x} \in \mathbb{R}^D         18pt
const EQ_XT      = loadEq("xT");      // \mathbf{x}^T                       18pt
const EQ_RND     = loadEq("rnd");     // \mathbb{R}^{N\times D}             18pt
const EQ_XIN_RND = loadEq("xin_rnd"); // \mathbf{X} \in \mathbb{R}^{N\times D} 18pt
const EQ_SET     = loadEq("set18");   // {(x1,y1),…,(xN,yN)} as (X,Y)       18pt
const EQ_XIJ     = loadEq("xij");     // \mathbf{x}_{ij}                    13pt
const EQ_X1      = loadEq("x1_14");   // \mathbf{x}_1                        14pt
const EQ_XN      = loadEq("xN_14");   // \mathbf{x}_N                        14pt
const EQ_Y1      = loadEq("y1_14");   // \mathbf{y}_1                        14pt
const EQ_YN      = loadEq("yN_14");   // \mathbf{y}_N                        14pt
const EQ_ROW1    = loadEq("row1_13"); // \mathbf{x}_{11} \cdots \mathbf{x}_{1D} 13pt
const EQ_ROWN    = loadEq("rowN_13"); // \mathbf{x}_{N1} \cdots \mathbf{x}_{ND} 13pt
const EQ_XEQ     = loadEq("Xeq");     // \mathbf{X}\;=                       18pt
const EQ_MIDEQ   = loadEq("mideq");   // =                                   18pt
const EQ_YEQ     = loadEq("Yeq");     // \mathbf{Y}\;=                       18pt
const EQ_VDOTS   = loadEq("vdots");   // \vdots                              9pt

// Arial valign-top margin-0 calibration (baselines measured on render_5):
// 18pt -> baseline = boxY + 0.247 ; 13pt -> boxY + 0.178
const OFF18 = 0.247, OFF13 = 0.178;

let s = pptx.addSlide();
s.background = { color: BG };

// ---------- House chrome ----------
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: FRAME_RED, width: 1.5 },
});
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("26", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
s.addText("Some Notations", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.85, align: "center", valign: "middle",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---------- Content box (judge-passed chrome from attempt 4; height extended to
// contain the original-measured diagram positions, bottom 7.20in) ----------
s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.67, y: 1.50, w: 11.99, h: 5.70, rectRadius: 0.06,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// ---------- helpers ----------
const mth = (t) => ({ text: t, options: { bold: true, italic: true } }); // math letter
const t   = (t) => ({ text: t, options: {} });
function prose18(x, y, runs, w) {
  s.addText(runs, { x: x, y: y, w: w || 9.9, h: 0.40, align: "left", valign: "top",
    fontSize: 18, color: TEXT, fontFace: FONT, margin: 0 });
}
function prose13(x, y, runs, w, h) {
  s.addText(runs, { x: x, y: y, w: w, h: h || 0.30, align: "left", valign: "top",
    fontSize: 13, color: TEXT, fontFace: FONT, margin: 0 });
}
// Bullet markers as OVAL shapes, PIL-matched to the original: top markers 11px
// centered at (113px, base-4px); sub markers 9px centered at (162px, base-4px).
function topMarker(centerYin) {
  s.addShape(pptx.shapes.OVAL, {
    x: 1.4925, y: centerYin - 0.0765, w: 0.153, h: 0.153,
    fill: { color: BUL }, line: { color: BUL, width: 0.25 },
  });
}
function subMarker(centerYin) {
  s.addShape(pptx.shapes.OVAL, {
    x: 2.1875, y: centerYin - 0.0625, w: 0.125, h: 0.125,
    fill: { color: BUL }, line: { color: BUL, width: 0.25 },
  });
}

// ---------- Five notation bullets (baselines/ink edges PIL-measured, 1px = 1pt) ----------
// b1: R^D (ink 132px) | prose from 172px | baseline 158px
topMarker(2.1597);
addEq(s, EQ_RD, 132 / 72 - PAD, 158 / 72);
prose18(2.381, 158 / 72 - OFF18, [t("denotes the set of all D \u00D7 1 real-valued column vectors")]);

// b2: x ∈ R^D (ink 132px) | prose from 213px | baseline 187px  (∈ baked into the PNG)
topMarker(2.5556);
addEq(s, EQ_XIN_RD, 132 / 72 - PAD, 187 / 72);
prose18(2.950, 187 / 72 - OFF18, [t("denotes a D \u00D7 1 real-valued column vector")]);

// b3: x^T (ink 132px) | prose from 167px | baseline 215px
topMarker(2.9306);
addEq(s, EQ_XT, 132 / 72 - PAD, 215 / 72);
prose18(2.311, 215 / 72 - OFF18,
  [t("denotes the transpose of "), mth("x"), t(", a 1 \u00D7 D row vector")]);

// b4: R^{N×D} (ink 133px) | prose from 201px | baseline 242px
topMarker(3.3194);
addEq(s, EQ_RND, 133 / 72 - PAD, 242 / 72);
prose18(2.783, 242 / 72 - OFF18, [t("denotes the set of all N \u00D7 D real-valued matrices")]);

// b5: X ∈ R^{N×D} (ink 132px) | prose from 230px | baseline 271px
topMarker(3.7083);
addEq(s, EQ_XIN_RND, 132 / 72 - PAD, 271 / 72);
prose18(3.186, 271 / 72 - OFF18, [t("denotes an N \u00D7 D real-valued matrix")]);

// ---------- b6: Supervised Learning bullet with tan highlight + set fragment ----------
// prefix ink 132..505px | tan box 503..853 x 285..307px | baseline 299px
topMarker(4.0972);
prose18(1.823, 299 / 72 - OFF18,
  [{ text: "Supervised Learning:", options: { bold: true } }, t(" Often, we write")], 5.15);
s.addShape(pptx.shapes.RECTANGLE, {
  x: 505 / 72, y: 285 / 72, w: 347 / 72, h: 22 / 72,
  fill: { color: TAN }, line: { color: TAN, width: 0.25 },
});
addEq(s, EQ_SET, 512 / 72 - PAD, 299 / 72); // fragment ink left edge 512px

// ---------- Four indented sub-bullets (13pt; wrap points PIL-matched) ----------
// sub1: baseline 328px, text from 180px
subMarker(4.5000);
prose13(2.490, 328 / 72 - OFF13, [mth("X"), t(" is an N \u00D7 D matrix")], 3.2);

// sub2: L1 baseline 354px from 180px; L2 baseline 377px from 179px
subMarker(4.8889);
prose13(2.490, 354 / 72 - OFF13,
  [t("Each row of "), mth("X"), t(" denotes an example,")], 4.65);
prose13(2.480, 377 / 72 - OFF13, [t("each column denotes a feature")], 4.0, 0.28);

// sub3: x_ij PNG (ink 180px, baseline 405px) | prose from 203px | L2 "i-th example" from 180px, baseline 423px
subMarker(5.5694);
addEq(s, EQ_XIJ, 180 / 72 - PAD, 405 / 72);
prose13(2.811, 405 / 72 - OFF13, [t("denotes the j-th feature of the")], 3.6, 0.28);
prose13(2.490, 423 / 72 - OFF13, [t("i-th example")], 2.0, 0.28);

// sub4: L1 baseline 453px from 179px; L2 baseline 472px from 179px
subMarker(6.2361);
prose13(2.480, 453 / 72 - OFF13,
  [mth("Y"), t(" is an N \u00D7 1 vector. Row i denotes")], 4.65);
prose13(2.480, 472 / 72 - OFF13, [t("the label of the i-th example")], 3.2, 0.28);

// ---------- Matrix diagrams (all geometry PIL-measured from the original) ----------
function stackElem(x, y, w, h, color) {
  s.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: x, y: y, w: w, h: h, rectRadius: 0.04,
    fill: { color: color }, line: { color: color, width: 0.5 },
  });
}
// Tall thin parenthesis = 180-degree ARC (tested: [90,270] = "(", [270,90] = ")").
// Arc ink: left extreme at box x (for "("), right extreme at box x+w (for ")").
function paren(ch, xLeftExtremeIn, yIn, hIn) {
  const wArc = 0.19;
  s.addShape(pptx.shapes.ARC, {
    x: ch === "(" ? xLeftExtremeIn : xLeftExtremeIn - wArc,
    y: yIn, w: wArc, h: hIn,
    line: { color: TEXT, width: 1.75 },
    angleRange: ch === "(" ? [90, 270] : [270, 90],
  });
}

// ----- X diagram (upper):  X = (col stack) = (matrix rows) -----
addEq(s, EQ_XEQ, 523 / 72 - PAD, 378 / 72);          // "X =" ink 523px, baseline 378px
// column stack: x1 (yellow), green, magenta, vdots, xN (cyan); chips 597..632px
const CH_W = 35 / 72, CH_H = 16 / 72, COLX = 597 / 72;
const xYs = [339, 357, 375, 396].map((r) => r / 72);
paren("(", 578 / 72, 334 / 72, 77 / 72);
stackElem(COLX, xYs[0], CH_W, CH_H, YELLOW); addEqInkTop(s, EQ_X1, 8.5417 - EQ_X1.w_in / 2, 340 / 72);
stackElem(COLX, xYs[1], CH_W, CH_H, GREEN);
stackElem(COLX, xYs[2], CH_W, CH_H, MAGENTA);
addEqCenter(s, EQ_VDOTS, 8.5417, 394 / 72);
stackElem(COLX, xYs[3], CH_W, CH_H, CYAN);   addEqInkTop(s, EQ_XN, 8.5625 - EQ_XN.w_in / 2, 398 / 72);
paren(")", 657 / 72, 334 / 72, 77 / 72);
// middle equals (bars 672..687px, baseline 377px)
addEq(s, EQ_MIDEQ, 672 / 72 - PAD, 377 / 72);
// matrix: yellow row x11…x1D, green, magenta, vdots, cyan row xN1…xND; rows 724..846px
const RW_X = 724 / 72, RW_W = 122 / 72;
paren("(", 702 / 72, 334 / 72, 77 / 72);
stackElem(RW_X, xYs[0], RW_W, CH_H, YELLOW); addEqInkTop(s, EQ_ROW1, 10.8889 - EQ_ROW1.w_in / 2, 343 / 72);
stackElem(RW_X, xYs[1], RW_W, CH_H, GREEN);
stackElem(RW_X, xYs[2], RW_W, CH_H, MAGENTA);
addEqCenter(s, EQ_VDOTS, 10.9028, 394 / 72);
stackElem(RW_X, xYs[3], RW_W, CH_H, CYAN);   addEqInkTop(s, EQ_ROWN, 10.8819 - EQ_ROWN.w_in / 2, 400 / 72);
paren(")", 863 / 72, 334 / 72, 77 / 72);

// ----- Y diagram (lower):  Y = (col stack) -----
addEq(s, EQ_YEQ, 605 / 72 - PAD, 479 / 72);          // "Y =" ink 605px, baseline 479px
const YCOLX = 682 / 72;
const yYs = [440, 458, 476, 497].map((r) => r / 72);
paren("(", 661 / 72, 435 / 72, 77 / 72);
stackElem(YCOLX, yYs[0], CH_W, CH_H, YELLOW); addEqInkTop(s, EQ_Y1, 9.7083 - EQ_Y1.w_in / 2, 443 / 72);
stackElem(YCOLX, yYs[1], CH_W, CH_H, GREEN);
stackElem(YCOLX, yYs[2], CH_W, CH_H, MAGENTA);
addEqCenter(s, EQ_VDOTS, 9.7500, 495 / 72);
stackElem(YCOLX, yYs[3], CH_W, CH_H, CYAN);   addEqInkTop(s, EQ_YN, 9.7153 - EQ_YN.w_in / 2, 500 / 72);
paren(")", 739 / 72, 435 / 72, 77 / 72);

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_026_recreated.pptx" })
  .then(() => console.log("done"));
