// Slide 017 — "Matrix Notation for Linear Regression and Classification (N- Samples)"
// Deck: machine-learning/02_linear-regression-classification-MSSE. Worker: ml02-w017-gen11.
// ROOT slide (dependency graph: 17 is root).
//
// Ground truth: unique_slides/slide_017.jpg (960x540, 1px = 1pt = 1/72 in).
// PIL measurement passes (scratch/ml02/slide017/measure1..16 + targeted art dumps):
//   - TITLE: one line Arial bold ~22.5pt tri-color, ink x87..831 y68..90, center x459:
//     "Matrix " 00008B + "Notation for Linear Regression and Classification (" 8B0000
//     + "N" 00008B + "- Samples)" 8B0000 (blue N inside the red paren group, verbatim
//     spacing "N- Samples)" — frame-verified).
//   - green squiggles 008000 under title ends: left 3 arcs x80..141 y94..101,
//     right 2 arcs x697..729 y99..118.
//   - NTS line: "N Training Samples" Times 20 REGULAR C00000, red ink x82..256 y180..198.
//   - VBOX x271..597 y107..301 FFFFFF border 00008B 2.25: three colored column chips
//     (fill only): chipY x294..337 FDFFB4, chipC x372..416 B8FFFF, chipM x514..558 F9A5FB,
//     each y142..295. Column labels X1/X2/Xn dark at y120; chip rows x11,x21,...,xd dark;
//     y-label row y1,y2,yn RED at y277 (y2 reads dark on cyan but chroma analysis says
//     C00000 — JPEG blur artifact). Mid column between chipC/chipM: 2 faint gray vbars
//     x451/x474 y150..259 (8A8A8A) flanking 4 dark dot rows (row3 only 2 dots) + red
//     dot row at y-label height y285 + dark dots at X-label height y132.
//   - REMEMBER box x649..875 y153..220 E5FEFA border 00008B 1.5: "Remember" Times
//     italic 21 C00000 + red underline; blue cursor bar x649 y181 h40 + black arrowhead;
//     equation row y = W1.T1 + W2.T2 as stamped tokens with 4 underlines y213
//     (W1 0000CC, X1 C00000, X2 C00000, W2 0000CC).
//   - BEIGE box x660..847 y267..294 FBFCE8 border 5A4031 1.25: "In General:" Times 19
//     black + "N" Times 20 C00000 + ">>>" Arial 22 0000CC (text run; PNG aspect mismatch)
//     + "d" Times 21 C00000.
//   - BL box x80..533 y322..516 FFFFFF border 8B0000 1.5: y column vector (y1,y2,..,yn
//     red + N x 1 label) in tall red parens x106/x136; "=" as two dark rects x174;
//     4-row matrix (ones column + x11..xnd, row3 = big dots) in dark parens x192/x396
//     with row highlight fills r1 FDFFB4 / r2 B8FFFF / r4 F9A5FB (r3 none) drawn UNDER
//     the parens; label "N x (d+1)" x397 y472.
//   - WVEC x456..489 y360..479 (blue): column [1, w2, w2(dup CONFIRMED by subscript
//     glyph shape — w_d never appears), dots] + label "(d+1) x 1" blue x463 y473;
//     wvec parens blue-ish x456..457 / x488..489.
//   - ARROW white-filled salmon-outlined rightArrow x532..586 y399..433 (outline
//     FF9999; strong-red scan is empty — faint blurred outline).
//   - BR box x586..885 y322..516 FFFFFF border 8B0000 1.5:
//     L1 "Y = X W": Y black underlined (602,382 uln), = dark, big X blue (651,355),
//     W red underlined (682,382 uln). No T superscript (frame-verified).
//     L2 "Where: X_{N x d+1} is a matrix" — X blue + wide blue sub.
//     L3 "Y_{N x 1} is labels vector" — Y red + red sub.
// Equations: STIX mathtext -> 600dpi transparent PNGs stamped from
// assets/eq017_placements.json (ink-anchored: target ink top-left from banked
// measurements minus PNG ink bbox*0.12; sizes = manifest w_in/h_in, never rescaled).
// Chrome: shared_patterns/house_chrome.js, numeral 17 + supplemental bottom stroke.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(__dirname, "..", "..", "shared_patterns", "house_chrome.js"));

const px = (v) => v / 72; // frame px -> inches
const A = (n) => path.join(__dirname, "assets", n);
const PL = JSON.parse(fs.readFileSync(path.join(__dirname, "assets", "eq017_placements.json"), "utf8"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "slide-recreation";
pres.title = "Matrix Notation for Linear Regression and Classification (N- Samples)";
const slide = pres.addSlide();

drawHouseChrome(pres, slide, { numeral: 17 });
// Supplemental red bottom stroke (rows 538-539 at frame scale; LO clips the shared
// panel's bottom border at the slide edge). Same pattern as slide_016.js.
slide.addShape(pres.ShapeType.rect, {
  x: px(61), y: px(538), w: px(839), h: px(2),
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});

// ---------- helpers ----------
function box(x0, y0, x1, y1, fill, border, bw) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: fill }, line: { color: border, width: bw },
  });
}
function fillOnly(x0, y0, w, h, fill) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x0), y: px(y0), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: fill, width: 0 },
  });
}
function tallParen(side, xStroke, y0, y1, color, widthPt, CURL) {
  CURL = CURL || 4;
  slide.addShape(pres.ShapeType.arc, {
    x: px(side === "lp" ? xStroke : xStroke - CURL),
    y: px(y0), w: px(CURL), h: px(y1 - y0),
    angleRange: side === "lp" ? [90, 270] : [270, 450],
    fill: { color: "FFFFFF", transparency: 100 },
    line: { color, width: widthPt },
  });
}
function squiggle(x, y, w, h, a0, a1) {
  slide.addShape(pres.ShapeType.arc, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    angleRange: [a0, a1],
    fill: { color: "FFFFFF", transparency: 100 },
    line: { color: "008000", width: 1.25 },
  });
}
function txt(str, o) {
  slide.addText(str, Object.assign({ margin: 0, valign: "middle", align: "left" }, o));
}

// ---------- boxes (draw order: containers, then fills, then strokes) ----------
box(271, 107, 597, 301, "FFFFFF", "00008B", 2.25);   // VBOX
fillOnly(294, 142, 43, 153, "FDFFB4");               // chipY
fillOnly(372, 142, 44, 153, "B8FFFF");               // chipC
fillOnly(514, 142, 44, 153, "F9A5FB");               // chipM
box(649, 153, 875, 220, "E5FEFA", "00008B", 1.5);    // REMEMBER
box(660, 267, 847, 294, "FBFCE8", "5A4031", 1.25);   // BEIGE
box(80, 322, 533, 516, "FFFFFF", "8B0000", 1.5);     // BL
// matrix row highlights UNDER parens/tokens (r3 has none)
fillOnly(198, 368, 194, 22, "FDFFB4");               // r1
fillOnly(196, 399, 197, 24, "B8FFFF");               // r2
fillOnly(196, 456, 197, 24, "F9A5FB");               // r4
// y-vector entry highlights (frame rects x~111..135, 24px tall, same bands as r1/r2/r4)
fillOnly(112, 368, 24, 24, "FDFFB4");                // behind y1
fillOnly(111, 399, 24, 24, "B8FFFF");                // behind y2
fillOnly(111, 456, 25, 24, "F9A5FB");                // behind yn
box(586, 322, 885, 516, "FFFFFF", "8B0000", 1.5);    // BR

// ---------- title (tri-color, centered on ink center x459) ----------
slide.addText([
  { text: "Matrix ", options: { color: "00008B" } },
  { text: "Notation for Linear Regression and Classification (", options: { color: "8B0000" } },
  { text: "N", options: { color: "00008B" } },
  { text: "- Samples)", options: { color: "8B0000" } },
], {
  x: px(59), y: px(62), w: px(800), h: px(30),
  align: "center", valign: "middle", bold: true, fontFace: "Times New Roman",
  fontSize: 25, margin: 0,
});

// ---------- green squiggles ----------
squiggle(77, 94, 23, 7, 180, 360);
squiggle(100, 94, 20, 7, 0, 180);
squiggle(119, 94, 22, 7, 180, 360);
// right squiggle: frame shows FOUR separate horizontal strokes (vision read
// title_squiggle_read.txt), not an ellipse — draw as flat rects
[[697, 100, 31, 2.5], [698, 104, 27, 2], [700, 114, 8, 2], [716, 116, 5, 2]]
  .forEach(([x0, y0, w, h]) => slide.addShape(pres.ShapeType.rect, {
    x: px(x0), y: px(y0), w: px(w), h: px(h),
    fill: { color: "008000" }, line: { color: "008000", width: 0 },
  }));

// ---------- NTS line ----------
txt("N Training Samples", {
  x: px(79), y: px(171), w: px(250), h: px(30),
  fontFace: "Times New Roman", fontSize: 22, color: "C00000",
});

// ---------- REMEMBER interior ----------
txt("Remember", {
  x: px(654), y: px(155), w: px(110), h: px(26),
  italic: true, fontFace: "Times New Roman", fontSize: 21, color: "C00000",
});
slide.addShape(pres.ShapeType.rect, { // Remember underline
  x: px(652), y: px(176), w: px(93), h: px(2.5),
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});
slide.addShape(pres.ShapeType.rect, { // blue cursor bar
  x: px(649), y: px(181), w: px(2.5), h: px(40),
  fill: { color: "00008B" }, line: { color: "00008B", width: 0 },
});
// (no arrowhead: judge attempt 1 + frame art show the original has only the
// equation "y" descender hook there — a filled triangle reads as a stray artifact)
// equation-row underlines y213 (W1 blue, X1 red, X2 red, W2 blue)
[[699, 27, "0000CC"], [743, 19, "C00000"], [805, 20, "C00000"], [843, 25, "0000CC"]]
  .forEach(([x0, w, c]) => slide.addShape(pres.ShapeType.rect, {
    x: px(x0), y: px(213), w: px(w), h: px(2.5),
    fill: { color: c }, line: { color: c, width: 0 },
  }));

// ---------- BEIGE interior ----------
txt("In General:", {
  x: px(663), y: px(266), w: px(92), h: px(28),
  fontFace: "Times New Roman", fontSize: 19, color: "000000",
});
txt("N", {
  x: px(758), y: px(266), w: px(20), h: px(28),
  fontFace: "Times New Roman", fontSize: 20, color: "C00000",
});
txt(">>>", {
  x: px(783), y: px(266), w: px(42), h: px(28),
  fontFace: "Arial", fontSize: 22, color: "0000CC",
});
txt("d", {
  x: px(828), y: px(266), w: px(18), h: px(28),
  fontFace: "Times New Roman", fontSize: 21, color: "C00000",
});

// ---------- BL interior ----------
// "=" as two dark bars (frame art: bar1 x173..183 y415.5..417.5, bar2 x173..183 y420..421.8)
[[415.5, 2.4], [420, 2.2]].forEach(([yy, hh]) => slide.addShape(pres.ShapeType.rect, {
  x: px(173.5), y: px(yy), w: px(10.5), h: px(hh),
  fill: { color: "333333" }, line: { color: "333333", width: 0 },
}));
// thin gray vertical between "=" and matrix LP (frame: x193..195, core y373..476, halo ~362..484)
slide.addShape(pres.ShapeType.rect, {
  x: px(193.8), y: px(362), w: px(1.5), h: px(122),
  fill: { color: "929292" }, line: { color: "929292", width: 0 },
});
// y vector parens (red; frame lp stroke x106 y366..479, rp bulge x135 y376..478)
tallParen("lp", 106, 366, 479, "C00000", 1.25, 3);
tallParen("rp", 135, 376, 478, "C00000", 1.25, 5);
// matrix parens (dark; lp stroke x201..202 y363..482; rp is a double stroke:
// bulge x394 + straight second stroke x387, both y~366..479 -> arc + supplemental line)
tallParen("lp", 201, 363, 482, "333333", 1.25, 7);
tallParen("rp", 394, 366, 479, "333333", 1.25, 15);
slide.addShape(pres.ShapeType.rect, {
  x: px(386.9), y: px(367), w: px(1.2), h: px(112),
  fill: { color: "333333" }, line: { color: "333333", width: 0 },
});
// w vector parens (periwinkle; lp stroke x456 y358..479, rp stroke x488..489 y368..479)
tallParen("lp", 456, 358, 479, "9999CC", 1.25, 2);
tallParen("rp", 489, 368, 479, "9999CC", 1.25, 3);

// ---------- ARROW (white fill, faint salmon outline) ----------
slide.addShape(pres.ShapeType.rightArrow, {
  x: px(532), y: px(399), w: px(54), h: px(34),
  fill: { color: "FFFFFF" }, line: { color: "FF9999", width: 1 },
});

// ---------- BR interior ----------
txt("Where:", {
  x: px(601), y: px(401), w: px(70), h: px(28),
  fontFace: "Times New Roman", fontSize: 21.5, color: "000000",
});
txt("is a matrix", {
  x: px(774), y: px(401), w: px(110), h: px(28),
  fontFace: "Times New Roman", fontSize: 23, color: "000000",
});
txt("is labels vector", {
  x: px(730), y: px(442), w: px(145), h: px(28),
  fontFace: "Times New Roman", fontSize: 22.4, color: "000000",
});
// L1 underlines: Y dark, W red
slide.addShape(pres.ShapeType.rect, {
  x: px(602), y: px(382), w: px(20), h: px(2.5),
  fill: { color: "333333" }, line: { color: "333333", width: 0 },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(680), y: px(382), w: px(27), h: px(2.5),
  fill: { color: "C00000" }, line: { color: "C00000", width: 0 },
});

// ---------- mid column gray vbars ----------
[[451], [474]].forEach(([x0]) => slide.addShape(pres.ShapeType.rect, {
  x: px(x0), y: px(150), w: px(1.5), h: px(109),
  fill: { color: "8A8A8A" }, line: { color: "8A8A8A", width: 0 },
}));

// ---------- equation stamps (ink-anchored placements; exact sizes) ----------
for (const p of PL) {
  slide.addImage({ path: A(p.file), x: p.x, y: p.y, w: p.w, h: p.h });
}

const OUT = path.join(__dirname, "..", "slide_017_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
