// Slide 050 — machine-learning/03_ridger_regression_gradient_descent
// "Iteration 2" (Perceptron) — built from PIL measurement of
// unique_slides/slide_050.jpg (960x540 frame, 1px = 1pt).
//
// MEASURED GEOMETRY (frame px; all banked in scratch/slide050_measurements.json,
// produced by scratch/measure_050_chart_full.py + scratch/verify_050_*.py):
//
//   chrome          : panel x54..903 y45..540 (E9E9E7), C00000 1pt strokes
//                     LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 (NO top stroke),
//                     badge d35 centred (876,73), numeral "50"
//   top navy box    : x68..719 y54..130, navy 2pt border (30,26,118), CREAM fill
//                     (254,255,232) — the box encloses BOTH the data table
//                     (x68..245) and the math zone (x246..719)
//   data table      : col centres 94/117/139/162/185/208 (pitch 22.6),
//                     header x1..x6 y63..74, rows [1,2,1,5,6,6] y80..89 and
//                     [1,1,2,4,5,6] y96..105 (each cell a bracketed 1x1 digit),
//                     class row C1 C1 C1 C2 C2 C2 y112..125 (red / blue)
//   caption box     : x66..240 y134..248, WHITE fill, 1pt grey border
//                     (161,171,183), "Augmented Vectors (from Top)" navy y147..160
//   vectors table   : same 6 columns; THREE rows (augmented, leading 1s) with
//                     TALL per-column parens (042-aug pattern, ink y179..223):
//                     [1,1,1,1,1,1] c187, [1,2,1,5,6,6] c203,
//                     [1,1,2,4,5,6] c218, class row y231..244
//   math zone       : x246..717 inside the navy box; 3 lines
//                       L1 y59..83 : "Initial W" (W underlined) = 3-row column
//                                    vector (4/-2/-2, parens x330..353 y62..102)
//                                    + "REPEAT" (dark, x366..421 y61..70,
//                                    underlined y71..72) + "using Step η = 1" (red
//                                    ink x425..530)
//                       L3 y86..120: "Check classes of" (x542..626) + Z1 Z2 Z3 labels/vectors
//                                    (x640..702; labels y74..85, vectors y86..120)
//                       L4 y110..124: key caption "C1 positive  C2 negative  Zero is unaccepted"
//                                    (x240..510; C1 red / C2 blue / Zero green / rest black)
//   pink box        : x743..830 y58..171, fill (249,232,250), underlined W = (5/-1/-1)
//   red box         : x84..213 y278..305, fill (201,0,4), white bold "Iteration 2"
//   stop text       : "No change in W" y350..371 (W underlined), "Stop Iterations"
//                     y375..394 with "Stop" in red
//   chart           : x312..824 y173..481, red border (146,22,33) 3px, white fill.
//                     axis map x_px=362.7+52.725*x, y_px=428.7-30.671*y.
//                     gridlines at data y = 7,6,5,3,2,1,0 (NO gridline at y=4 —
//                     measured; the magenta diamond (5,4) sits on that row).
//                     vertical spines x362 (left) and x784 (right).
//                     x ticks 0..8 at px 362,415,468,521,574,627,680,732,784;
//                     y ticks 7..0 at px 215,245,276,306,337,368,399,430.
//                     decision line: least-squares on 1935 red px ->
//                     y_data = -1.00417*x + 4.90556, ink from (-0.51,5.42) to
//                     (6.19,-1.31); both ends taper to a point.
//                     markers: blue squares (1,1),(2,1),(1,2); magenta diamonds
//                     (5,4),(6,5),(6,6); red triangle (7,6); red wedge (0,0).
//                     "+ve" red text at data (0.56,3.84) with two small red arrows.

const pptxgenpkg = require("pptxgenjs");
const path = require("path");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in == 960x540 px at 1px=1pt
const s = pptx.addSlide();

drawHouseChrome(pptx, s, { numeral: "50" });

// ---------- helpers: frame px -> inches (absolute frame coordinates) ----------
const fx = (px) => px / 72;
const fw = (px) => px / 72;

const FONT = "Arial";
const BLACK = "000000";
const WHITE = "FFFFFF";
const NAVY = "1E1A76";        // measured navy ink
const RED = "FF0000";
const BLUE = "0000FF";
const RED_DARK = "C90004";    // measured red-box fill (201,0,4)
const CHART_RED = "92211B";   // measured chart border/line red (~146,22,33 / 200,48,60)
const GRID = "DEE0DD";        // measured gridline grey
const CREAM = "FFFFE8";       // measured table fill
const PINK = "F9E8FA";        // measured pink box fill
const MARK_BLUE = "1C3D5E";   // measured blue marker (28,61,94)
const MARK_MAG = "E03FEB";    // measured magenta marker (224,63,235)
const MARK_RED = "D2000F";    // measured red triangle / blob (210,0,15)
const GREEN = "008000";       // measured "Zero" green in the L4 key caption

// chart axis mapping (measured least squares over the 7 marker centres)
const X2PX = (x) => 362.7 + 52.725 * x;
const Y2PY = (y) => 428.7 - 30.671 * y;

const EQ = (name) => path.join(__dirname, "assets", name);
// sidecars are "<basename>.png" + "<basename>.json" written by render_eq.py
function eqInfo(name) { return require(EQ(name.replace(/\.png$/, "") + ".json")); }

// ================= 1. TOP NAVY BOX (encloses table + math zone) =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(68), y: fx(54), w: fw(719 - 68), h: fw(130 - 54),
  fill: { color: CREAM }, line: { color: NAVY, width: 2 },
});

// NOTE: the frame shows NO divider between the data table (x68..245) and the
// math zone (x246..717) — the only vertical strokes in the navy box are its
// own border columns x68..70 and x718..720 (measured). Nothing is drawn here.

// ================= 2. TOP-LEFT DATA TABLE =================
// 049-certified top-table composition ported verbatim (XOR slide_049.jpg vs
// slide_050.jpg over x80..240 y60..130 = 0 px: identical original geometry;
// the per-cell "(v)" text rows were a judged MAJOR — the original shows tall
// Bezier parens spanning both digit rows, qa/slide050/crop_18_tableeq_judge.txt)
// header y64..73; bracketed 2-stacks y77..107 (digit rows y78..88 / y97..107);
// class tag row y113..124 (outside the brackets). Column centres 96.2..208.2.
{
  const centres = [96.2, 118.6, 141.0, 163.4, 185.8, 208.2];
  const cellW = 22.4;
  const trow = function (texts, top, h, o) {
    for (let i = 0; i < 6; i++) {
      s.addText(texts[i], Object.assign({
        x: fx(centres[i] - cellW / 2), y: fx(top), w: fw(cellW), h: fx(h),
        fontFace: FONT, fontSize: 11, color: BLACK, align: "center",
        valign: "middle", margin: 0,
      }, o || {}));
    }
  };
  trow(["x\u2081", "x\u2082", "x\u2083", "x\u2084", "x\u2085", "x\u2086"],
    64, 10, { bold: true });
  trow(["1", "2", "1", "5", "6", "6"], 78, 10.5);
  trow(["1", "1", "2", "4", "5", "6"], 97, 10);
  // class tags C1 C1 C1 C2 C2 C2 at y113..124 (below the brackets); C2 ink
  // 211776 per 049's certified measurement (same pixels, XOR = 0)
  const cls = ["C\u2081", "C\u2081", "C\u2081", "C\u2082", "C\u2082", "C\u2082"];
  for (let i = 0; i < 6; i++) {
    s.addText(cls[i], {
      x: fx(centres[i] - cellW / 2), y: fx(113), w: fw(cellW), h: fx(12),
      fontFace: FONT, fontSize: 11, bold: true, italic: true,
      color: i < 3 ? RED : "211776",
      align: "center", valign: "middle", margin: 0,
    });
  }
  // tall parentheses around the 2-stack rows (ink y77..107): measured Bezier
  // PNGs (fix 15: font parens -> 909090 class, same as Z; bows = sub-pixel
  // centroids, qa/slide049/parenA_15c.out)
  const ptL = eqInfo("parens049/paren_top2_lp");
  const ptR = eqInfo("parens049/paren_top2_rp");
  const PPPT = 72 / 600;
  const topLP = [89.78, 111.18, 133.45, 155.89, 178.84, 201.21];
  const topRP = [102.42, 124.72, 147.12, 170.07, 192.45, 214.74];
  for (let i = 0; i < 6; i++) {
    s.addImage({
      path: EQ("parens049/paren_top2_lp.png"),
      x: fx(topLP[i] - (ptL.ink_left_px * PPPT + ptL.S_pt / 2)),
      y: fx(77 - ptL.ink_top_px * PPPT),
      w: ptL.px_w * PPPT / 72, h: ptL.px_h * PPPT / 72,
    });
    s.addImage({
      path: EQ("parens049/paren_top2_rp.png"),
      x: fx(topRP[i] + 0.5 - ((ptR.ink_right_px + 1) * PPPT - ptR.S_pt / 2)),
      y: fx(77 - ptR.ink_top_px * PPPT),
      w: ptR.px_w * PPPT / 72, h: ptR.px_h * PPPT / 72,
    });
  }
}

// ================= 3. MATH ZONE (right half of the navy box) =================
// L1: "Initial W =" (W NOT underlined — the x366..421 band y71..72 belongs to
//     the Step text below-right; the old read_initialw misattribution drew a
//     phantom W-underline) + 3-row column vector (4/-2/-2) drawn
//     042-cert pattern: text + bowed paren PNGs (tips 330.5/353.5, ink
//     y62..102) + re-centred bare digits; the mathtext asset could not
//     carry the underline or the third row.
s.addText([
  { text: "Initial " },
  { text: "W", options: { bold: true, italic: true } },
  { text: " =" },
], {
  x: fx(262), y: fx(71), w: fw(70), h: fw(18),
  fontFace: FONT, fontSize: 14, color: BLACK,
  align: "left", valign: "middle", margin: 0,
});
(function () {
  const P = path.join(__dirname, "assets", "parens042");
  const fs2 = require("fs");
  const sc = 40 / 39.96;
  [[`${P}/paren_tall_lp.png`, `${P}/paren_tall_lp.json`, 330.5, "lp"],
   [`${P}/paren_tall_rp.png`, `${P}/paren_tall_rp.json`, 353.5, "rp"]]
    .forEach(function ([img, meta, tipX, side]) {
      const j = JSON.parse(fs2.readFileSync(meta, "utf8"));
      const ink = side === "lp" ? j.ink_right_px : j.ink_left_px;
      s.addImage({
        path: img,
        x: fx(tipX - ink * j.pt_per_px * sc),
        y: fx(62 - j.ink_top_px * j.pt_per_px * sc),
        w: (j.px_w * j.pt_per_px * sc) / 72,
        h: (j.px_h * j.pt_per_px * sc) / 72,
      });
    });
})();
// bare digits re-centred on the frame's ink (minus bars x336..341 -> cell
// centre 342.5; rows y62..70 / y78..86 / y93..102)
s.addText("4", { x: fx(335.5), y: fx(59), w: fw(14), h: fw(14),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle", margin: 0 });
s.addText("-2", { x: fx(333.5), y: fx(75), w: fw(18), h: fw(14),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle", margin: 0 });
s.addText("-2", { x: fx(333.5), y: fx(90.5), w: fw(18), h: fw(14),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle", margin: 0 });

// L1 instruction line (att18, pixel-adjudicated: att17 judges + glyph
// forensics — six uniform caps-height glyphs x366..421 y61..70, no
// descenders = "REPEAT" black italic, underlined bar y71..72 x366..419;
// red ink x425..530 y60..74 with i-dot at x442 and descenders g/p/η at
// x452/481/508 = "using Step η = 1", core (152,38,41) ≈ CHART_RED.
// The earlier "dark Step η = 1 + red REPEAT using Step" reading was the
// misattributed-underline chain's other half — both att17 judges and the
// bitmap agree on REPEAT-first.)
s.addText("REPEAT", {
  x: fx(365), y: fx(56), w: fw(64), h: fw(18),
  fontFace: FONT, fontSize: 14, color: BLACK, italic: true, underline: true,
  align: "left", valign: "middle", margin: 0,
});

s.addText("using Step \u03B7 = 1", {
  x: fx(424.5), y: fx(57), w: fw(112), h: fw(17),
  fontFace: FONT, fontSize: 14, color: CHART_RED, bold: true, italic: true,
  align: "left", valign: "middle", margin: 0,
});

// L3: "Check classes of" caption (measured ink x542..626, y86..96)
s.addText("Check classes of", {
  x: fx(542), y: fx(84), w: fw(110), h: fw(15),
  fontFace: FONT, fontSize: 11, color: BLACK, align: "left", valign: "middle", margin: 0,
});

// L3/L4: the three Z column vectors with subscript labels (measured Z labels + parens).
// Measured: label x641..656 / x664..678 / x684..702 y74..85; vector x640..658 /
// x663..680 / x684..702 y86..120 (pitch 23).
const ZVEC = [
  { label: "Z", sub: "1", img: "eq_050_Z1.png", x: 641 },
  { label: "Z", sub: "2", img: "eq_050_Z2.png", x: 664 },
  { label: "Z", sub: "3", img: "eq_050_Z3.png", x: 686 },
];
ZVEC.forEach(function (z) {
  s.addText([
    { text: "Z", options: { fontSize: 12, color: BLACK, italic: true } },
    { text: z.sub, options: { fontSize: 9, color: BLACK, italic: true, subscript: true } },
  ], {
    x: fx(z.x), y: fx(74), w: fw(16), h: fw(12),
    fontFace: FONT, align: "left", valign: "middle", margin: 0,
  });
  const m = eqInfo(z.img);
  s.addImage({ path: EQ(z.img), x: fx(z.x), y: fx(86), w: m.w_in, h: m.h_in });
});

// L4: the key caption under the math lines — measured x240..510 y110..124:
// "C1 positive  C2 negative  Zero is unaccepted" with C1 red (x240..253),
// C2 blue, Zero green (x394..423), remainder black.
s.addText([
  { text: "C", options: { color: RED, bold: true } },
  { text: "1", options: { color: RED, bold: true, subscript: true } },
  { text: " positive   ", options: { color: BLACK } },
  { text: "C", options: { color: BLUE, bold: true } },
  { text: "2", options: { color: BLUE, bold: true, subscript: true } },
  { text: " negative   ", options: { color: BLACK } },
  { text: "Zero", options: { color: GREEN } },
  { text: " is unaccepted", options: { color: BLACK } },
], {
  x: fx(240), y: fx(106), w: fw(280), h: fw(20),
  fontFace: FONT, fontSize: 13, align: "left", valign: "middle", margin: 0,
});

// ================= 4. PINK WEIGHT BOX (top-right) =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(743), y: fx(58), w: fw(830 - 743), h: fw(171 - 58),
  fill: { color: PINK }, line: { color: PINK, width: 1 },
});
(function () {
  const m = eqInfo("eq_050_finalW.png");   // underlined W = (5/-1/-1) column vector
  s.addImage({ path: EQ("eq_050_finalW.png"), x: fx(743), y: fx(67), w: m.w_in, h: m.h_in });
})();

// ================= 5. RED "Iteration 2" BOX =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(84), y: fx(278), w: fw(213 - 84), h: fw(305 - 278),
  fill: { color: RED_DARK }, line: { color: RED_DARK, width: 1 },
});
s.addText("Iteration 2", {
  x: fx(84), y: fx(278), w: fw(213 - 84), h: fw(305 - 278),
  fontFace: FONT, fontSize: 13, color: WHITE, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ================= 6. STOP TEXT =================
// "No change in W" — W underlined (measured underline y365..370)
s.addText([
  { text: "No change in ", options: { color: BLACK } },
  { text: "W", options: { color: BLACK, italic: true, underline: true } },
], {
  x: fx(77), y: fx(348), w: fw(160), h: fw(23),
  fontFace: FONT, fontSize: 20, align: "left", valign: "middle", margin: 0,
});
// "Stop Iterations" — "Stop" red, "Iterations" black (measured Stop ink x83..121)
s.addText([
  { text: "Stop", options: { color: CHART_RED, bold: true } },
  { text: " Iterations", options: { color: BLACK } },
], {
  x: fx(83), y: fx(373), w: fw(160), h: fw(22),
  fontFace: FONT, fontSize: 20, align: "left", valign: "middle", margin: 0,
});

// ================= 7. CHART =================
// 7a. white plot panel with the measured 3px red border
s.addShape(pptx.ShapeType.rect, {
  x: fx(312), y: fx(173), w: fw(824 - 312), h: fw(481 - 173),
  fill: { color: WHITE }, line: { color: CHART_RED, width: 3 },
});

// 7b. horizontal gridlines (data y = 7,6,5,3,2,1,0 — measured; no line at y=4)
[7, 6, 5, 3, 2, 1, 0].forEach(function (gy) {
  s.addShape(pptx.ShapeType.line, {
    x: fx(363), y: fx(Y2PY(gy)), w: fw(784 - 363), h: 0,
    line: { color: GRID, width: 1 },
  });
});

// 7c. vertical spines: left axis (x=0) and right (x=8)
[0, 8].forEach(function (sx) {
  s.addShape(pptx.ShapeType.line, {
    x: fx(X2PX(sx)), y: fx(Y2PY(7)), w: 0, h: fw(Y2PY(0) - Y2PY(7)),
    line: { color: GRID, width: 1 },
  });
});

// 7d. x tick labels 0..8
[0, 1, 2, 3, 4, 5, 6, 7, 8].forEach(function (tx) {
  s.addText(String(tx), {
    x: fx(X2PX(tx) - 10), y: fx(438), w: fw(20), h: fw(8),
    fontFace: FONT, fontSize: 8, color: BLACK, align: "center", valign: "middle", margin: 0,
  });
});
// 7e. y tick labels 7..0
[7, 6, 5, 4, 3, 2, 1, 0].forEach(function (ty) {
  s.addText(String(ty), {
    x: fx(348), y: fx(Y2PY(ty) - 5), w: fw(12), h: fw(10),
    fontFace: FONT, fontSize: 8, color: BLACK, align: "center", valign: "middle", margin: 0,
  });
});

// 7f. decision line y = -1.00417x + 4.90556 from (-0.51,5.42) to (6.19,-1.31).
//     The original's line ends taper to a point with NO arrowhead (measured:
//     end window carries a single taper, no head) — plain thick line.
(function () {
  const x0d = -0.51, y0d = -1.00417 * x0d + 4.90556;
  const x1d = 6.19, y1d = -1.00417 * x1d + 4.90556;
  const ax = X2PX(x0d), ay = Y2PY(y0d);
  const bx = X2PX(x1d), by = Y2PY(y1d);
  // flipY: pptxgenjs lines measure from (x,y) by w/h, and negative h is invalid,
  // so express the line top-left to bottom-right.
  const lx = ax, ly = ay, lw = bx - ax, lh = by - ay;
  s.addShape(pptx.ShapeType.line, {
    x: fx(lx), y: fx(ly), w: fw(lw), h: fw(lh),
    line: { color: CHART_RED, width: 3.5 },
  });
})();

// 7g. blue squares (class C1) — original cluster reads (1,1),(2,1),(1,2)
//     (w050_adjud5: orig blue at data (1.01,2.00),(1.01,0.98),(2.02,0.98))
[[1, 1], [2, 1], [1, 2]].forEach(function (p) {
  const cx = X2PX(p[0]), cy = Y2PY(p[1]);
  s.addShape(pptx.ShapeType.rect, {
    x: fx(cx - 4), y: fx(cy - 4), w: fw(8), h: fw(8),
    fill: { color: MARK_BLUE }, line: { color: MARK_BLUE, width: 1 },
  });
});
// 7h. magenta diamonds (class C2)
[[5, 4], [6, 5], [6, 6]].forEach(function (p) {
  const cx = X2PX(p[0]), cy = Y2PY(p[1]);
  s.addShape(pptx.ShapeType.diamond, {
    x: fx(cx - 5.5), y: fx(cy - 5.5), w: fw(11), h: fw(11),
    fill: { color: MARK_MAG }, line: { color: MARK_MAG, width: 1 },
  });
});
// 7i. red triangle at (7,6) — measured downward (widest rows y241-245, taper
//     to y249); all three z-markers point down in the frame
(function () {
  const cx = X2PX(7), cy = Y2PY(6);
  s.addShape(pptx.ShapeType.triangle, {
    x: fx(cx - 4.5), y: fx(cy - 4.5), w: fw(9), h: fw(9),
    fill: { color: MARK_RED }, line: { color: MARK_RED, width: 1 },
    flipV: true, rotate: 0,
  });
})();
// 7i2. red triangle at (3,2) — z3 marker merged into the decision line in the
//      frame (bulge to 17px at x509..525 y364..371); downward like the others
(function () {
  const cx = X2PX(3), cy = Y2PY(2);
  s.addShape(pptx.ShapeType.triangle, {
    x: fx(cx - 4.5), y: fx(cy - 4.5), w: fw(9), h: fw(9),
    fill: { color: MARK_RED }, line: { color: MARK_RED, width: 1 },
    flipV: true, rotate: 0,
  });
})();
// 7j. red origin marker at (0,0) — measured downward wedge 9x9 px (apex top,
//     widest rows 426-427, taper to y432); a circle is a judged MAJOR deviation
(function () {
  const cx = X2PX(0), cy = Y2PY(0);
  s.addShape(pptx.ShapeType.triangle, {
    x: fx(cx - 4.5), y: fx(cy - 4.5), w: fw(9), h: fw(9),
    fill: { color: MARK_RED }, line: { color: MARK_RED, width: 1 },
    flipV: true, rotate: 0,
  });
})();

// 7k. "+ve" red annotation at data (0.56,3.84) with ONE small red arrow.
//     Att19 pixel re-measure (qa/slide050/adjud_chart_20261026.md): the orig
//     has a single arrow branching off the decision line at ~(415,309) frame
//     px, running DOWN-LEFT to a V-head at (398..409, 318..326) — no second
//     arrow, no parallel stroke (the old two-arrow measurement had misread
//     the fork+head; the long "arrow 1" it produced hugged the line and
//     shipped as a spurious on-line blob — att13+att19 MAJORs).
//     "+ve" glyph group spans x374..396 (centre 385), y306..315.
s.addText("+ve", {
  x: fx(364), y: fx(Y2PY(3.84) - 6), w: fw(42), h: fw(12),
  fontFace: FONT, fontSize: 11, color: CHART_RED, bold: true,
  align: "center", valign: "middle", margin: 0,
});
s.addShape(pptx.ShapeType.line, {
  x: fx(399), y: fx(309), w: fw(16), h: fw(17),
  flipH: true,
  line: { color: CHART_RED, width: 3, endArrowType: "triangle" },
});

// ================= 9. CAPTION BOX + AUGMENTED-VECTORS TABLE =================
s.addShape(pptx.ShapeType.rect, {
  x: fx(66), y: fx(134), w: fw(240 - 66), h: fw(248 - 134),
  fill: { color: WHITE }, line: { color: "A1ABB5", width: 1 },
});
s.addText("Augmented Vectors (from Top)", {
  x: fx(82), y: fx(145), w: fw(155), h: fw(15),
  fontFace: FONT, fontSize: 10, color: NAVY, bold: true,
  align: "left", valign: "middle", margin: 0,
});

// header x1..x6 (same 6 columns as the top table)
const V_HDR = [["x1", 93], ["x2", 114], ["x3", 137], ["x4", 159], ["x5", 182], ["x6", 204]];
V_HDR.forEach(function (c) {
  s.addText([
    { text: "x", options: { fontSize: 11, color: BLACK, italic: true } },
    { text: c[0][1], options: { fontSize: 8, color: BLACK, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(164), w: fw(20), h: fw(12),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

// three augmented rows: bare digits re-centred between the tall per-column
// parens (measured digit bands y184..190/199..207/214..222 -> centres
// 187/203/218); parens drawn below as bowed PNG pairs (042-cert pattern)
const V_ROWS = [
  { y: 182, vals: ["1", "1", "1", "1", "1", "1"] },
  { y: 198, vals: ["1", "2", "1", "5", "6", "6"] },
  { y: 213, vals: ["1", "1", "2", "4", "5", "6"] },
];
const V_CENTRES = [99, 121, 143, 166, 188, 211];
V_ROWS.forEach(function (r) {
  r.vals.forEach(function (v, i) {
    s.addText(v, {
      x: fx(V_CENTRES[i] - 5), y: fx(r.y), w: fw(11), h: fw(10),
      fontFace: FONT, fontSize: 10, color: BLACK,
      align: "center", valign: "middle", margin: 0,
    });
  });
});
// tall per-column parens spanning all three digit rows (measured: continuous
// strokes y179..~y223 at the 042-aug stem positions; per-cell parens were a
// judged MAJOR deviation)
(function () {
  const P = path.join(__dirname, "assets", "parens042");
  const fs2 = require("fs");
  const sc = 44 / 39.96;
  [[93, 107], [115, 128], [137, 150], [159, 173], [182, 196], [205, 218]]
    .forEach(function ([xl, xr]) {
      [[`${P}/paren_tall_lp.png`, `${P}/paren_tall_lp.json`, xl, "lp"],
       [`${P}/paren_tall_rp.png`, `${P}/paren_tall_rp.json`, xr, "rp"]]
        .forEach(function ([img, meta, tipX, side]) {
          const j = JSON.parse(fs2.readFileSync(meta, "utf8"));
          const ink = side === "lp" ? j.ink_right_px : j.ink_left_px;
          s.addImage({
            path: img,
            x: fx(tipX - ink * j.pt_per_px * sc),
            y: fx(179 - j.ink_top_px * j.pt_per_px * sc),
            w: (j.px_w * j.pt_per_px * sc) / 72,
            h: (j.px_h * j.pt_per_px * sc) / 72,
          });
        });
    });
})();

// class row beneath the augmented table
const V_CLS = [["C1", 93, RED], ["C1", 114, RED], ["C1", 137, RED],
               ["C2", 159, BLUE], ["C2", 182, BLUE], ["C2", 204, BLUE]];
V_CLS.forEach(function (c) {
  s.addText([
    { text: "C", options: { fontSize: 10, color: c[2], bold: true } },
    { text: c[0][1], options: { fontSize: 8, color: c[2], bold: true, subscript: true } },
  ], {
    x: fx(c[1]), y: fx(231), w: fw(20), h: fw(13),
    fontFace: FONT, align: "center", valign: "middle", margin: 0,
  });
});

// ================= OUTPUT =================
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_050_recreated.pptx";
pptx.writeFile({ fileName: OUT }).then(function () { console.log("wrote " + OUT); });
