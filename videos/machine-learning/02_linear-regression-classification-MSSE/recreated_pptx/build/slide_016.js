// Slide 016 — "Vector Notation for Linear Regression and Classification (One Sample)"
// Deck: machine-learning/02_linear-regression-classification-MSSE (39 slides)
// Worker: ml02-w016-a4, 2026-10-13. ROOT slide (no parents). Shares the trio 14/15/16
// OMML equation component (shared asset minted by ml02-w015-a3; this slide derives
// eq_016_core.png per the shared-component protocol — see worker_report.md).
//
// Ground truth: unique_slides/slide_016.jpg (960x540, 1px = 1pt = 1/72 in).
// PIL measurement passes (scratch/ml02/slide016/measure*.py) + 12 gate crop reads:
//   - TITLE (frame overrides spec): one line, Arial bold ~22pt, tri-color runs:
//     "Vector " 00008B (x95..162) + "Notation for Linear Regression and
//     Classification" 8B0000 (x170..692) + " (One Sample)" 00008B (x701..843);
//     ink band y68..85, NO underline (spec's "blue underlined title" is wrong —
//     frame + gate crop read agree).
//   - model1 box x75..372 y109..154 FFFFCC: "Model" red italic bold; I/P row:
//     "I/P:" black + red "( x1 x2 x3 ..... xn )"; "O/P:" black + red "( y )".
//   - model2 box x75..353 y199..242 FFFFCC: "Model" red italic; equation line
//     y223..241 per-column color RLE: y 00008B, = 00008B, w's 8B0000 (+ red subs),
//     x's 00008B (+ blue subs), +'s 00008B, dots 44448C, b 008000. Verbatim DUP
//     "w2 x2 + w2 x2" + tail index n (gate-verified on crops, 6x zoom).
//   - compact box x74..183 y260..291 FAFCE6: y = W^T X + b (W blue uln, T blue sup,
//     X red uln, b green).
//   - vecbox x424..788 y102..290 FFFFFF border 333399: "Input:" red; "X =" red
//     (X underlined); red column vector x1,x2,x3,...,...,xd (SIX rows, two
//     ellipsis rows — frame-verified) in tall red parens x531..534/x555..558
//     y132..280; "W =" blue + blue column vector w1..w_d in periwinkle parens
//     x634..636/x663..666 y132..274; "Output: ( y )" black.
//   - step1 x75..346 y320..425 FFFFCC: w-row (blue w1 w2 .... wn, navy-ish parens
//     x116..119 / x259..263 y326..349) floats TOP; "y =" black mid-left (baseline
//     ~375); column vector x1,...,xn (THREE rows — frame-verified) in salmon-red
//     parens x274..276 y348..412 / x299..301 y348..400; "+ b" (+ dark x314..326,
//     b green x336..345) baseline ~374.
//   - step2 x420..681 y318..448 E4FFEF border 555599: "y =" black (baseline ~350);
//     row vector: teal "(" x464..467 y336..358, b green x470..479, blue w1 w2 ....
//     w_d, teal ")" x636..640 y336..346 (SHORT close — frame quirk); augmented
//     column: green 1, red x1, x2, ..., xd with ONLY a right salmon paren
//     x674..676 y350..445 (no left paren in frame — PIL-verified).
//   - result box x758..880 y354..396 roundRect 00008B border: y = W^T X (y black,
//     W 00008B uln, T 00008B sup, X C00000 uln; underlines at y390).
//   - note x72..381 y437..527 FAE9D7 border CC9999: "Note:" red underlined;
//     "b"/"1" GREEN bold in quotes; begin/end underlined.
//   - augmented x436..641 y458..524 E4FFEF border 555599: L1 y = W^T X; L2 Where X
//     is Augmented vector (X red uln); L3 W is(d+1) dimension (W red uln, gap).
//   - parambox x655..884 y493..523 F8FFC0 border 666699: "Model Parameter is"
//     00008B italic bold + red underlined W (underline x855..882 wider than W).
//   - arrows: white-filled pink-outlined block arrows x358..408 / x696..746, y368..384.
// Equations: STIX mathtext -> 600dpi transparent PNG runs at measured x on measured
// baselines (per-run single colors — frame RLE); sizes frame-calibrated per slot.
// Chrome: shared_patterns/house_chrome.js, numeral 16.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(__dirname, "..", "..", "shared_patterns", "house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches
const A = (n) => path.join(__dirname, "assets", n);
const EQ = JSON.parse(fs.readFileSync(path.join(__dirname, "assets", "eq_016_manifest.json"), "utf8"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "slide-recreation";
pres.title = "Vector Notation for Linear Regression and Classification (One Sample)";
const slide = pres.addSlide();

drawHouseChrome(pres, slide, { numeral: 16 });
// Supplemental red bottom stroke: the frame shows it at rows 538-539 (half-visible at the
// slide edge); LO clips the shared panel rect's bottom border at the slide boundary, so
// draw it explicitly (copy-then-modify; shared_patterns/house_chrome.js untouched).
// y=538.0 (not 537.6): gray must survive through row 537 like the original; a 537.6
// start painted row 537 red and failed house_chrome_check's gray-bottom rule by 1px.
slide.addShape(pres.ShapeType.rect, {
  x: px(61), y: px(538), w: px(839), h: px(2),
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});

// ---------- helper: equation PNG run at measured ink-left x and baseline ----------
function eqRun(name, xLeft, baselineY) {
  const s = EQ[name];
  slide.addImage({
    path: A(name),
    x: px(xLeft - 1), // PNG has ~1 frame-px transparent pad
    y: px(baselineY - s.baseline_frac * s.h_px * 0.12),
    w: s.w_in, h: s.h_in,
  });
}
// helper: tall delimiter as ONE half-turn ARC (pattern: delimiters-spanning-arc)
function tallParen(side, xStroke, y0, y1, color, widthPt) {
  const CURL = 4; // frame px bbox width (tip curl)
  slide.addShape(pres.ShapeType.arc, {
    x: px(side === "lp" ? xStroke : xStroke - CURL),
    y: px(y0), w: px(CURL), h: px(y1 - y0),
    angleRange: side === "lp" ? [90, 270] : [270, 450],
    fill: { color: "FFFFFF", transparency: 100 },
    line: { color, width: widthPt },
  });
}

// ---------- boxes (fills + thin borders) ----------
function box(x0, y0, x1, y1, fill, border, bw, round) {
  slide.addShape(pres.ShapeType[round ? "roundRect" : "rect"], {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: fill }, line: { color: border, width: bw },
    rectRadius: round ? 0.05 : undefined,
  });
}
box(75, 109, 372, 154, "FFFFCC", "9999CC", 0.75);            // model1
box(75, 199, 353, 242, "FFFFCC", "9999CC", 0.75);            // model2
box(74, 260, 183, 291, "FAFCE6", "9999CC", 0.75);            // compact
box(424, 102, 788, 290, "FFFFFF", "333399", 1);              // vecbox
box(75, 320, 346, 425, "FFFFCC", "9999CC", 0.75);            // step1
box(420, 318, 681, 448, "E4FFEF", "555599", 1);              // step2
box(758, 354, 880, 396, "FFFFFF", "00008B", 1.5, true);      // result (rounded)
box(72, 437, 381, 527, "FAE9D7", "CC9999", 0.75);            // note
box(436, 458, 641, 524, "E4FFEF", "555599", 1);              // augmented
box(655, 493, 884, 523, "F8FFC0", "666699", 1);              // parambox

// ---------- title (measured tri-color, no underline) ----------
slide.addText([
  { text: "Vector ", options: { color: "00008B" } },
  { text: "Notation for Linear Regression and Classification", options: { color: "8B0000" } },
  { text: " (One Sample)", options: { color: "00008B" } },
], {
  x: px(469.5 - 380), y: px(62), w: px(760), h: px(30),
  align: "center", valign: "middle", bold: true, fontFace: "Arial",
  fontSize: 22.5, margin: 0,
});

// ---------- model1 ----------
slide.addText("Model", {
  x: px(75), y: px(108), w: px(120), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 17, color: "C00000", margin: 0,
});
// wait: model1's Model header sits at y110..125 inside model1 box (y199 one is model2's)
slide.addText("I/P:", {
  x: px(77), y: px(134), w: px(42), h: px(18),
  align: "left", valign: "middle", bold: true,
  fontFace: "Times New Roman", fontSize: 15, color: "000000", margin: 0,
});
slide.addText("O/P:", {
  x: px(311), y: px(134), w: px(42), h: px(18),
  align: "left", valign: "middle", bold: true,
  fontFace: "Times New Roman", fontSize: 15, color: "000000", margin: 0,
});
slide.addText("( y )", {
  x: px(350), y: px(131), w: px(40), h: px(23),
  align: "left", valign: "middle", italic: true,
  fontFace: "Times New Roman", fontSize: 19, color: "C00000", margin: 0,
});
eqRun("eq_016_m1x1.png", 121, 150);
eqRun("eq_016_m1x2.png", 152, 150);
eqRun("eq_016_m1x3.png", 183, 150);
eqRun("eq_016_m1dots.png", 213, 150);
eqRun("eq_016_m1xn.png", 255, 150);
// I/P row parentheses (red, span y134..153)
slide.addText("(", {
  x: px(112), y: px(133), w: px(14), h: px(21),
  align: "left", valign: "middle", fontFace: "Times New Roman",
  fontSize: 24, color: "C00000", margin: 0,
});
slide.addText(")", {
  x: px(274), y: px(133), w: px(14), h: px(21),
  align: "left", valign: "middle", fontFace: "Times New Roman",
  fontSize: 24, color: "C00000", margin: 0,
});

// ---------- model2 (core equation; runs at measured x, baseline 236.5) ----------
slide.addText("Model", {
  x: px(75), y: px(198), w: px(120), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 17, color: "C00000", margin: 0,
});
eqRun("eq_016_y.png", 77, 236.5);
eqRun("eq_016_eq.png", 91, 236.5);
eqRun("eq_016_w1.png", 105, 236.5);
eqRun("eq_016_x1.png", 128, 236.5);
eqRun("eq_016_plus.png", 145, 236.5);
eqRun("eq_016_w2.png", 157, 236.5);
eqRun("eq_016_x2.png", 180, 236.5);
eqRun("eq_016_plus.png", 198, 236.5);
eqRun("eq_016_w2.png", 210, 236.5);
eqRun("eq_016_x2.png", 232, 236.5);
eqRun("eq_016_plus.png", 250, 236.5);
eqRun("eq_016_ldots.png", 261, 236.5);
eqRun("eq_016_plus.png", 279, 236.5);
eqRun("eq_016_wn.png", 290, 236.5);
eqRun("eq_016_xn.png", 314, 236.5);
eqRun("eq_016_plus.png", 332, 236.5);
eqRun("eq_016_b.png", 344, 236.5);

// ---------- compact: y = W^T X + b ----------
slide.addText("y", {
  x: px(74), y: px(268), w: px(20), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 20, color: "000000", margin: 0,
});
slide.addText("=", {
  x: px(92), y: px(268), w: px(20), h: px(20),
  align: "left", valign: "middle", bold: true,
  fontFace: "Times New Roman", fontSize: 20, color: "000000", margin: 0,
});
slide.addText("W", {
  x: px(106), y: px(266), w: px(20), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true, underline: true,
  fontFace: "Times New Roman", fontSize: 21, color: "00008B", margin: 0,
});
slide.addText("T", {
  x: px(125), y: px(256), w: px(16), h: px(14),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 12, color: "00008B", margin: 0,
});
slide.addText("X", {
  x: px(135), y: px(266), w: px(20), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true, underline: true,
  fontFace: "Times New Roman", fontSize: 21, color: "C00000", margin: 0,
});
slide.addText("+", {
  x: px(154), y: px(268), w: px(18), h: px(20),
  align: "left", valign: "middle", bold: true,
  fontFace: "Times New Roman", fontSize: 20, color: "000000", margin: 0,
});
slide.addText("b", {
  x: px(166), y: px(266), w: px(20), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 21, color: "008000", margin: 0,
});

// ---------- vecbox ----------
slide.addText("Input:", {
  x: px(441), y: px(190), w: px(60), h: px(18),
  align: "left", valign: "middle", bold: true,
  fontFace: "Times New Roman", fontSize: 16, color: "C00000", margin: 0,
});
slide.addText([
  { text: "X", options: { underline: true } },
  { text: " =", options: { color: "C00000" } },
], {
  x: px(498), y: px(187), w: px(48), h: px(23),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 24, color: "C00000", margin: 0,
});
eqRun("eq_016_vx1.png", 538, 146);
eqRun("eq_016_vx2.png", 538, 172);
eqRun("eq_016_vx3.png", 538, 198);
eqRun("eq_016_vldots.png", 541, 224);
eqRun("eq_016_vldots.png", 541, 247);
eqRun("eq_016_vxd.png", 538, 271);
slide.addText([
  { text: "W", options: { underline: true } },
  { text: " =", options: { color: "00008B" } },
], {
  x: px(598), y: px(187), w: px(48), h: px(23),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 24, color: "00008B", margin: 0,
});
eqRun("eq_016_vw1.png", 641, 151);
eqRun("eq_016_vw2.png", 641, 175);
eqRun("eq_016_vw3.png", 641, 197);
eqRun("eq_016_vwldots.png", 643, 224);
eqRun("eq_016_vwldots.png", 643, 244);
eqRun("eq_016_vwd.png", 641, 265);
slide.addText("Output:", {
  x: px(687), y: px(192), w: px(68), h: px(18),
  align: "left", valign: "middle", bold: true,
  fontFace: "Times New Roman", fontSize: 16, color: "000000", margin: 0,
});
slide.addText("( y )", {
  x: px(750), y: px(184), w: px(44), h: px(25),
  align: "left", valign: "middle", italic: true,
  fontFace: "Times New Roman", fontSize: 20, color: "000000", margin: 0,
});
tallParen("lp", 531, 132, 280, "C00000", 1.25);
tallParen("rp", 558, 132, 280, "C00000", 1.25);
tallParen("lp", 634, 132, 274, "9999CC", 1.25);
tallParen("rp", 666, 132, 274, "9999CC", 1.25);

// ---------- step1 ----------
slide.addText("y =", {
  x: px(76), y: px(360), w: px(42), h: px(19),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 19, color: "000000", margin: 0,
});
// w-row (top): parens + blue tokens, baseline 343
tallParen("lp", 116, 326, 349, "8A8AB0", 1.5);
tallParen("rp", 262, 326, 349, "8A8AB0", 1.5);
eqRun("eq_016_p1w1.png", 124, 343);
eqRun("eq_016_p1w2.png", 161, 343);
eqRun("eq_016_p1dots.png", 202, 343);
eqRun("eq_016_p1wn.png", 240, 343);
// column vector (3 rows) + salmon parens
tallParen("lp", 274, 348, 412, "C00000", 1.25);
tallParen("rp", 301, 348, 400, "C00000", 1.25);
eqRun("eq_016_s1x1.png", 281, 365);
eqRun("eq_016_s1dots.png", 283, 393);
eqRun("eq_016_s1xn.png", 284, 417);
eqRun("eq_016_s1plus.png", 313, 374);
eqRun("eq_016_s1b.png", 335, 374);

// ---------- step2 ----------
slide.addText("y =", {
  x: px(424), y: px(369), w: px(42), h: px(19),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 19, color: "000000", margin: 0,
});
// row vector: teal parens, green b, blue w's (baseline 352)
tallParen("lp", 464, 336, 358, "8FB4C8", 1.5);
tallParen("rp", 639, 336, 346, "8FB4C8", 1.5);
eqRun("eq_016_p2b.png", 469, 352);
eqRun("eq_016_p2w1.png", 498, 352);
eqRun("eq_016_p2w2.png", 535, 352);
eqRun("eq_016_p2dots.png", 576, 352);
eqRun("eq_016_p2wd.png", 615, 352);
// augmented column: green 1, red rows; ONLY right paren (frame-verified)
tallParen("rp", 676, 350, 445, "C00000", 1.25);
eqRun("eq_016_s2one.png", 661, 340);
eqRun("eq_016_s2x1.png", 658, 362);
eqRun("eq_016_s2x2.png", 658, 387);
eqRun("eq_016_s2dots.png", 657, 416);
eqRun("eq_016_s2xd.png", 658, 436);

// ---------- result box ----------
slide.addText("y =", {
  x: px(766), y: px(370), w: px(48), h: px(24),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 26, color: "000000", margin: 0,
});
slide.addText("W", {
  x: px(804), y: px(364), w: px(36), h: px(28),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 31, color: "00008B", margin: 0,
});
slide.addShape(pres.ShapeType.line, {
  x: px(805), y: px(390), w: px(29), h: 0,
  line: { color: "00008B", width: 1.25 },
});
slide.addText("T", {
  x: px(837), y: px(355), w: px(22), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 22, color: "00008B", margin: 0,
});
slide.addText("X", {
  x: px(854), y: px(366), w: px(30), h: px(26),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 31, color: "C00000", margin: 0,
});
slide.addShape(pres.ShapeType.line, {
  x: px(854), y: px(390), w: px(23), h: 0,
  line: { color: "C00000", width: 1.25 },
});

// ---------- note ----------
slide.addText("Note:", {
  x: px(79), y: px(446), w: px(50), h: px(17),
  align: "left", valign: "middle", bold: true, underline: true,
  fontFace: "Times New Roman", fontSize: 16, color: "C00000", margin: 0,
});
slide.addText([
  { text: "\u201Cb\u201D", options: { color: "008000", bold: true } },
  { text: " may be added at ", options: { color: "000000" } },
  { text: "begin", options: { color: "000000", underline: true } },
  { text: " of the vector", options: { color: "000000" } },
], {
  x: px(79), y: px(463), w: px(280), h: px(17),
  align: "left", valign: "middle", fontFace: "Times New Roman",
  fontSize: 17, margin: 0,
});
slide.addText([
  { text: "or at ", options: { color: "000000" } },
  { text: "end", options: { color: "000000", underline: true } },
  { text: " of the vector", options: { color: "000000" } },
], {
  x: px(79), y: px(483), w: px(200), h: px(16),
  align: "left", valign: "middle", fontFace: "Times New Roman",
  fontSize: 17, margin: 0,
});
slide.addText([
  { text: "Same for ", options: { color: "000000" } },
  { text: "\u201C1\u201D", options: { color: "008000", bold: true } },
  { text: " added to input vector", options: { color: "000000" } },
], {
  x: px(79), y: px(503), w: px(285), h: px(16),
  align: "left", valign: "middle", fontFace: "Times New Roman",
  fontSize: 17, margin: 0,
});

// ---------- augmented ----------
slide.addText("y =", {
  x: px(442), y: px(468), w: px(42), h: px(18),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 19, color: "000000", margin: 0,
});
slide.addText("W", {
  x: px(469), y: px(464), w: px(24), h: px(22),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 25, color: "00008B", margin: 0,
});
slide.addShape(pres.ShapeType.line, {
  x: px(470), y: px(485.5), w: px(15), h: 0,
  line: { color: "00008B", width: 1.25 },
});
slide.addText("T", {
  x: px(489), y: px(458), w: px(17), h: px(15),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 15, color: "00008B", margin: 0,
});
slide.addText("X", {
  x: px(502), y: px(464), w: px(18), h: px(21),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 20, color: "C00000", margin: 0,
});
slide.addShape(pres.ShapeType.line, {
  x: px(503), y: px(483.5), w: px(14), h: 0,
  line: { color: "C00000", width: 1.25 },
});
slide.addText([
  { text: "Where ", options: { color: "000000" } },
  { text: "X", options: { color: "C00000", underline: true } },
  { text: " is Augmented vector", options: { color: "000000" } },
], {
  x: px(441), y: px(489), w: px(210), h: px(18),
  align: "left", valign: "middle", fontFace: "Times New Roman",
  fontSize: 15.5, margin: 0,
});
slide.addText("W", {
  x: px(477), y: px(498), w: px(20), h: px(33),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 13, color: "C00000", margin: 0,
});
slide.addText("is", {
  x: px(503), y: px(498), w: px(20), h: px(33),
  align: "left", valign: "middle",
  fontFace: "Times New Roman", fontSize: 13, color: "000000", margin: 0,
});
slide.addText("d+1 dimension", {
  x: px(537), y: px(509.5), w: px(120), h: px(14),
  align: "left", valign: "middle",
  fontFace: "Times New Roman", fontSize: 14, color: "000000", margin: 0,
});
slide.addShape(pres.ShapeType.line, {
  x: px(484), y: px(519.5), w: px(15), h: 0,
  line: { color: "C00000", width: 1.25 },
});

// ---------- parambox ----------
slide.addText("Model Parameter is", {
  x: px(662), y: px(499), w: px(190), h: px(20),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 22.5, color: "00008B", margin: 0,
});
slide.addText("W", {
  x: px(862), y: px(503), w: px(26), h: px(17),
  align: "left", valign: "middle", bold: true, italic: true,
  fontFace: "Times New Roman", fontSize: 18, color: "C00000", margin: 0,
});
slide.addShape(pres.ShapeType.line, {
  x: px(855), y: px(520), w: px(27), h: 0,
  line: { color: "C00000", width: 1.25 },
});

// ---------- arrows (white fill, pink outline; custGeom block arrows) ----------
function blockArrow(x0, x1, yTop, yBot) {
  const midY = (yTop + yBot) / 2;
  const bodyEnd = x0 + (x1 - x0) * 0.72; // head base
  slide.addShape(pres.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,
    fill: { color: "FFFFFF" }, line: { color: "FFCCCC", width: 1 },
    points: [
      { x: px(x0), y: px(yTop + 2), moveTo: true },
      { x: px(bodyEnd), y: px(yTop + 2) },
      { x: px(bodyEnd), y: px(yTop) },
      { x: px(x1), y: px(midY) },
      { x: px(bodyEnd), y: px(yBot) },
      { x: px(bodyEnd), y: px(yBot - 2) },
      { x: px(x0), y: px(yBot - 2) },
      { x: px(x0), y: px(yTop + 2), close: true },
    ],
  });
}
blockArrow(358, 408, 368, 384);
blockArrow(696, 746, 368, 384);

const OUT = path.join(__dirname, "..", "slide_016_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
