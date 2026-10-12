// slide_032.js — "Linear Transformation (= Fully connected Layer)"
// Deep Learning DSAI 308, Transformers — Part I. Build worker, attempt 2, 2026-10-12.
// (Attempt 1 was built + rendered pre-judge before a provider outage interrupted the
// worker; resumed. Attempt-2 fixes from the closed-loop render-vs-frame checks:
// eq-panel/matrix/net-panel frame-true edges, title/subtitle charSpacing to the
// frame's measured ink widths, band labels bold-italic + ccw tilt, connection lines
// drawn OVER the gray band per the frame's col-scan + crop reads.)
//
// Frame-true build: all geometry PIL-measured from unique_slides/slide_032.jpg
// (960x540, 1px = 1pt = 1/72 in) — scratch/slide032/measure/ (m1..m14 passes) plus
// gated crop reads banked in scratch/slide032/crops/ (band labels, eq panel, navy
// mark, network panel). FRAME-VS-SPEC corrections applied per the fidelity law and
// recorded in slide_032_source/SOURCES.md ("Build-time frame re-check"):
//   - matrix cells are PINK (#F7C7CB) holding pale-yellow text chips (#F6F7C1,
//     thin brown border) — NOT pale-yellow cells with orange borders;
//   - matrix text color is UNIFORM PER ROW: blue / magenta / orange / green;
//   - red square brackets [ ] flank the pill's four circles;
//   - the band's blue staircase reads W_21 FOUR times (raw's W_22 / W_23[?] closed);
//   - the "dark-navy arrowhead" mid-diagram is recreated as the spec's small dark
//     arrowhead (crop read: pencil/cursor-like mark; ground rule (c) applies if so).
//
// LAWS honored: playlist chrome via shared house_chrome.js (badge numeral 32 = the
// number printed on the frame); verbatim text; margin:0 + explicit fontFace on every
// text element; explicit lineSpacing on every multi-line box (none here — all boxes
// are single-line); no '#' in hex; single-version plain-named deliverable.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt)
const FONT = "Arial";

// ---- palette (PIL-measured cores, see scratch/slide032/measure/m14_cores.py) ----
const C = {
  eqPanelFill: "FEFFFD", eqPanelBorder: "8A212E",
  pillFill: "F2C9EF", pillRing: "8F1B48", bracket: "952333",
  circFill: "D2C2EA",
  dimLabel: "862B39", xwLabel: "952333",
  cellFill: "F7C7CB", cellBorder: "D5AAB3",
  chipFill: "F6F7C1", chipBorder: "9C7857",
  mRow1: "1C1A78", mRow2: "8A1670", mRow3: "B08136", mRow4: "55902D",
  outFill: "F7C7C9", outBorder: "7A1E2C", outText: "5E3620",
  chipOutFill: "F6F7C1", chipOutBorder: "A8A887",
  qSub: "7A2028",
  equals: "8C1221",
  title: "8B101E", subtitle: "08008C",
  arrowLine: "CA596B",
  netBorder: "1C1383",
  outRing: "22147E", outCircFill: "F8FAE6",
  inRing: "802334", inCircFill: "D2E2EC",
  bandFill: "E7E9E6",
  lblRed: "A8404E", lblBlue: "32259E", lblGreen: "4E8E4D", bandWQ: "962331",
  nodeText: "1F1F1F",
  lineRed: "C34A58", lineBlue: "3A2DA0", lineFaint: "D9C0C6", lineGreen: "4E8E4D",
  navy: "141452",
};

// ---- measured geometry (frame px) ------------------------------------------------
const OUT_X = [540, 648, 757, 861];   // output circle centers (top row)
const OUT_CY = 277;
const IN_X = [540, 648, 757, 861];    // input circle centers (bottom row)
const IN_CY = 465;
const MAT_X = [240, 278, 316, 353];   // matrix chip column centers
const MAT_Y = [110, 148.5, 192.5, 231]; // matrix chip row centers

// subscripted label helper: parts = [["W","Q"], ...] as [text, opts] runs
function label(pptx, slide, cx, cy, w, h, runs, opts = {}) {
  slide.addText(
    runs.map(([t, o]) => ({ text: t, options: o || {} })),
    {
      x: px(cx - w / 2), y: px(cy - h / 2), w: px(w), h: px(h),
      align: "center", valign: "middle", margin: 0, wrap: false,
      fontFace: FONT, fontSize: opts.size || 10, bold: opts.bold !== false,
      color: opts.color || C.nodeText, italic: opts.italic || false,
      rotate: opts.rotate || 0,
    }
  );
}
// thin colored connection line
function conn(pptx, slide, x1, y1, x2, y2, color, width) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color, width: width || 1 },
  });
}

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// 1) playlist house chrome (white canvas, gray panel, red border, badge "32")
drawHouseChrome(pptx, slide, { numeral: 32 });

// 2) equation panel (top-left): white rounded rect, dark-red border
// (attempt-4 fix: frame right stroke at x≈466-468 (stroke-column scan rows 168-174;
//  the bbox "474" was net-panel-corner contamination) -> w 409.5. Bottom stroke
//  verified y≈270 in both (attempt 3); left/top verified attempt 2.)
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(57.5), y: px(65.5), w: px(409.5), h: px(205.5), rectRadius: 0.18,
  fill: { color: C.eqPanelFill }, line: { color: C.eqPanelBorder, width: 2.5 },
});

// 3) input pill: pink-lavender rounded pill + red [ ] + four red-ringed circles
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(71), y: px(108), w: px(136), h: px(36), rectRadius: 0.17,
  fill: { color: C.pillFill }, line: { type: "none" },
});
label(pptx, slide, 77, 126.5, 14, 30, [["[", {}]], { size: 17, color: C.bracket });
label(pptx, slide, 200, 126.5, 14, 30, [["]", {}]], { size: 17, color: C.bracket });
const PILL_CX = [97, 122, 148, 173];
PILL_CX.forEach((cx, i) => {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - 11), y: px(126.5 - 11), w: px(22), h: px(22),
    fill: { color: C.circFill }, line: { color: C.pillRing, width: 1.25 },
  });
  label(pptx, slide, cx, 126.5, 20, 12,
    [["X", {}], ["2" + (i + 1), { subscript: true }]],
    { size: 7, color: C.nodeText });
});

// 4) pill captions: X_2 below pill; 1xd at pill lower-right; W_Q below-right
label(pptx, slide, 129, 170, 34, 30, [["X", {}], ["2", { subscript: true }]],
  { size: 20, color: C.xwLabel });
label(pptx, slide, 194.5, 146.5, 26, 12, [["1xd", {}]], { size: 9, color: C.dimLabel });
label(pptx, slide, 194.5, 221.5, 40, 30, [["W", {}], ["Q", { subscript: true }]],
  { size: 20, color: C.xwLabel });

// 5) weight matrix: pink rounded grid + separators + 16 yellow chips with W labels
// (attempt-2 fix: frame pink fill spans x221..372, y86..259 — attempt-1 was 220..375 / 84..259)
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(221), y: px(86), w: px(151), h: px(173), rectRadius: 0.1,
  fill: { color: C.cellFill }, line: { color: C.cellBorder, width: 1 },
});
[259, 297, 335].forEach((x) =>
  slide.addShape(pptx.ShapeType.line, {
    x: px(x), y: px(87), w: 0, h: px(171),
    line: { color: C.cellBorder, width: 1 },
  })
);
[129, 170, 211].forEach((y) =>
  slide.addShape(pptx.ShapeType.line, {
    x: px(222), y: px(y), w: px(149), h: 0,
    line: { color: C.cellBorder, width: 1 },
  })
);
const ROWCOL = [C.mRow1, C.mRow2, C.mRow3, C.mRow4];
for (let i = 0; i < 4; i++) {          // row i (0-based) -> second digit
  for (let j = 0; j < 4; j++) {        // col j (0-based) -> first digit
    const cx = MAT_X[j], cy = MAT_Y[i];
    slide.addShape(pptx.ShapeType.rect, {
      x: px(cx - 10.5), y: px(cy - 7), w: px(21), h: px(14),
      fill: { color: C.chipFill }, line: { color: C.chipBorder, width: 0.75 },
    });
    label(pptx, slide, cx, cy, 21, 14,
      [["W", {}], [(j + 1) + "" + (i + 1), { subscript: true }]],
      { size: 8.5, color: ROWCOL[i] });
  }
}
label(pptx, slide, 352, 245, 30, 12, [["dxd", {}]], { size: 9, color: C.dimLabel });

// 6) equals sign
label(pptx, slide, 393, 174, 20, 26, [["=", {}]], { size: 20, color: C.equals });

// 7) output column: ONE tall pink capsule (frame: no internal borders — gap rows are
// plain pink, pixel-scanned) + 4 pale-yellow chips behind the X_Q labels (crop-compare
// finding, pixel-confirmed #FBFFC4) + dark-maroon labels with reddish Q subscripts
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(410.5), y: px(86), w: px(41), h: px(171.5), rectRadius: 0.12,
  fill: { color: C.outFill }, line: { color: C.outBorder, width: 1.25 },
});
const OUTL_CY = [111, 149, 192, 234];
OUTL_CY.forEach((cy, i) => {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(415), y: px(cy - 7), w: px(31), h: px(14),
    fill: { color: C.chipOutFill }, line: { color: C.chipOutBorder, width: 0.75 },
  });
  label(pptx, slide, 430.5, cy, 30, 14,
    [["X", {}], ["Q", { subscript: true, color: C.qSub }], ["2" + (i + 1), { subscript: true }]],
    { size: 10, color: C.outText });
});

// 8) title + subtitle (centered on the same axis at x=702.5)
// (attempt-2 fix: frame ink widths 253px/290px vs attempt-1's 228px/239px at matching
//  heights -> character spacing, not font size; also nudged to the frame's ink centers
//  131 / 158)
slide.addText("Linear Transformation", {
  x: px(552.5), y: px(118.5), w: px(300), h: px(24),
  align: "center", valign: "middle", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 22, bold: true, color: C.title, charSpacing: 1.25,
});
slide.addText("(= Fully connected Layer)", {
  x: px(542.5), y: px(142), w: px(320), h: px(28),
  align: "center", valign: "middle", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 20, bold: true, italic: true, color: C.subtitle, charSpacing: 2.1,
});

// 9) elbow block arrow: white fills + unified red outline (7 segments)
slide.addShape(pptx.ShapeType.rect, {   // horizontal tail
  x: px(485), y: px(146.5), w: px(66), h: px(30.5),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});
slide.addShape(pptx.ShapeType.rect, {   // vertical shaft
  x: px(524), y: px(177), w: px(27), h: px(27.5),
  fill: { color: "FFFFFF" }, line: { type: "none" },
});
slide.addShape(pptx.ShapeType.triangle, { // arrowhead pointing down
  x: px(524), y: px(204), w: px(27), h: px(33.5), rotate: 180,
  fill: { color: "FFFFFF" }, line: { type: "none" },
});
const AR = "CA596B";
[[485, 146.5, 551, 146.5], [551, 146.5, 551, 204.5], [551, 204.5, 538, 237.5],
 [538, 237.5, 524, 204.5], [524, 204.5, 524, 177], [524, 177, 485, 177],
 [485, 177, 485, 146.5]].forEach(([x1, y1, x2, y2]) =>
  slide.addShape(pptx.ShapeType.line, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: AR, width: 2.25 },
  })
);

// 10) network panel: white rounded rect, deep-blue border
// (attempt-3 fix: frame top stroke at y≈246-249 with corner radius ≈20px (pixel scans
//  at x=600/700 + corner profile) -> y 247, h 261, rectRadius 0.28; left/right/bottom
//  verified frame-true in attempt 2)
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(473.5), y: px(247), w: px(436), h: px(261), rectRadius: 0.28,
  fill: { color: "FFFFFF" }, line: { color: C.netBorder, width: 2.5 },
});

// 12) gray weight band — drawn UNDER the lines (attempt-2 fix: the frame shows the
//  connection lines visibly crossing the band; corroborated by frame col x=648 ink
//  257..486 continuous + crop reads). attempt-3: subtle darker gray border (frame
//  edge #C9D3DC / #CCD0D1 measured at top + right).
slide.addShape(pptx.ShapeType.roundRect, {
  x: px(490), y: px(307), w: px(400), h: px(121), rectRadius: 0.12,
  fill: { color: C.bandFill }, line: { color: "C9CDD2", width: 1 },
});

// 11) 16 connection lines (colored by SOURCE input; drawn OVER the band)
const LINECOL = [C.lineRed, C.lineBlue, C.lineFaint, C.lineGreen];
IN_X.forEach((ix, i) => {
  OUT_X.forEach((ox) => conn(pptx, slide, ix, IN_CY - 21, ox, OUT_CY + 20, LINECOL[i], 0.75));
});

// 13) band labels: large W_Q + three staircases (blue reads W_21 four times — frame)
// (attempt-5: W_Q italic per both crop reads; nudged right to the frame's inset)
label(pptx, slide, 512, 381, 44, 34, [["W", { italic: true }], ["Q", { subscript: true, italic: true }]],
  { size: 21, color: C.bandWQ });
function stair(cx, cy, sub, color) {
  label(pptx, slide, cx, cy, 30, 17, [["W", { italic: true }], [sub, { subscript: true, italic: true }]],
    { size: 10, color, rotate: -10 });
}
stair(525, 321, "11", C.lblRed);  stair(583, 333, "12", C.lblRed);
stair(626, 350, "13", C.lblRed);  stair(700, 381, "14", C.lblRed);
stair(639, 322, "21", C.lblBlue); stair(680, 340, "21", C.lblBlue);
stair(717, 359, "21", C.lblBlue); stair(765, 387, "21", C.lblBlue);
stair(771, 331, "41", C.lblGreen); stair(797, 347, "42", C.lblGreen);
stair(825, 366, "43", C.lblGreen); stair(858, 391, "44", C.lblGreen);

// 14) small FILLED lens marks tucked under outputs 1 (red), 2 (blue), 4 (green)
// (attempt-5: frame shows filled blobs, not open arcs — crop-compare; each colored
// ellipse is drawn BEFORE the output circles so the circle fill masks its top half)
[[OUT_X[0], C.lineRed], [OUT_X[1], C.lineBlue], [OUT_X[3], C.lineGreen]].forEach(([cx, col]) =>
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - 10), y: px(291), w: px(20), h: px(11),
    fill: { color: col }, line: { type: "none" },
  })
);

// 15) pencil-like annotation mark between blue labels 2 and 3 (attempt-5: elongated
// light body + dark tip per crop reads c1/c3 + band crop-compare MAJOR finding)
slide.addShape(pptx.ShapeType.rect, {
  x: px(685), y: px(350.5), w: px(15), h: px(4.5), rotate: -30,
  fill: { color: "FDFDF8" }, line: { color: "2A2A2A", width: 0.75 },
});
slide.addShape(pptx.ShapeType.triangle, {
  x: px(681.5), y: px(348.5), w: px(5), h: px(5), rotate: -30,
  fill: { color: "2A2A2A" }, line: { type: "none" },
});

// 16) output circles (top row): pale-cream fill, deep-blue rings, dark labels
// (attempt-5: reddish Q subscripts per netpanel + eqpanel crop reads)
OUT_X.forEach((cx, i) => {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - 19.5), y: px(OUT_CY - 19.5), w: px(39), h: px(39),
    fill: { color: C.outCircFill }, line: { color: C.outRing, width: 2 },
  });
  label(pptx, slide, cx, OUT_CY + 2, 34, 14,
    [["X", {}], ["Q", { subscript: true, color: C.qSub }], ["2" + (i + 1), { subscript: true }]],
    { size: 10, color: C.nodeText });
});

// 17) input circles (bottom row): light-blue fill, dark-red rings, dark labels
IN_X.forEach((cx, i) => {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(cx - 21), y: px(IN_CY - 21), w: px(42), h: px(42),
    fill: { color: C.inCircFill }, line: { color: C.inRing, width: 2 },
  });
  label(pptx, slide, cx, IN_CY + 1, 30, 14,
    [["X", {}], ["2" + (i + 1), { subscript: true }]],
    { size: 10, color: C.nodeText });
});

// ---- output (SINGLE-VERSION law: one plain-named deliverable) ----------------
const OUT = path.join(__dirname, "..", "slide_032_recreated.pptx");
pptx.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
