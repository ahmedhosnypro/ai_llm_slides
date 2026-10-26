// Build: slide 003 — "Matrix Notation for Linear Regression and Classification (N- Samples)"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Reference frame: unique_slides/slide_003.jpg (960x540, 1px=1pt=1/72in)
// Spec: analysis/slide_003_final.json
//
// ATTEMPT 8 rebuild (banked pre-change build: qa/slide003/build_attempt_8.js).
// Judge attempts 5/6/7 + crop_5 FAILed (judged on a STALE render_5.png — verified
// by PIL: the 01:01 pptx contains the full fixed build, the render does not).
// take-6 PIL census (census_6.py + adjudicate_6.py) settled the findings against
// the ORIGINAL frame:
//   - top box bands DO carry interior entry lines (dark ink y160..174, y189..198
//     inside all three bands) -> entries added per the verbatim equation;
//   - ellipsis column between cyan and pink (gray dots x415..479, header y119..137)
//     -> added ("..." header, parens, dot stack);
//   - separator line under the entries at y297 -> added;
//   - bl box interior: three colored ROW bands (yellow y368..390, cyan y397..423,
//     pink y456..478) + white ellipsis row, gray "]" after the matrix, w-vector at
//     the right, three dimension labels -> restructured (was a 4-row text matrix);
//   - dimension label "N x d+1" under the matrix -> added (judge finding CONFIRMED
//     by absent ink in the old render + present gray text in the original);
//   - arrow is a THIN gray line (original), not the tall chevron -> replaced;
//   - title is ONE line at ~21pt (26pt wraps in LO — the stale render wrapped).
//
// MEASURMENTS (frame px, PIL on unique_slides/slide_003.jpg 2026-10-24):
//   Chrome: house_chrome.js (deck law) — canvas FFFFFF, panel E9E9E7 x54..903
//     y45..540, C00000 1pt LEFT x58.5 / RIGHT x901 / BOTTOM y538.5 ONLY (no top
//     stroke), badge d35 at (876,73) FDFD96 ring 6A5ACD numeral 3.
//   Title ink x82..832 y68..90 ONE line; "Matrix" #0000FF, rest RED #FF0000.
//   N Training Samples: red, x81..272 y177..199.
//   Top box: x271..596 y107..301 blue border, white fill. Bands y141..296:
//     yellow x294..336, cyan x370..417, pink x513..557. Headers black y119..137.
//     Ellipsis column x415..479 (header + gray dot stack in parens).
//     Separator line y297. Red y-labels y277..293 inside band bottoms.
//   Remember box: x649..874 y153..221, pale-blue fill, blue border, red bold
//     italic "Remember", blue underlined eq y=W^T X=X^T W.
//   In General box: x659..850 y268..294, border #6C5B3D.
//   Bottom-left box: x79..533 y323..517, RED border, white fill, ROW-band matrix.
//   Bottom-right box: x572..752 y323..517, RED border, white fill.
//   Arrow: thin gray line x~538..572 y~392.

const pptxgen = require("pptxgenjs");
const fs = require("fs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const ASSET_DIR = __dirname + "/assets";
const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_003_recreated.pptx";

const px = (v) => v / 72;
const A = "Arial";
const GRAY = "808080";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// ---- HOUSE CHROME (shared deck module — badge numeral = file number 3) -----
drawHouseChrome(pptx, slide, { numeral: 3 });

// ---- TITLE: ONE line (23pt — cap-height 16.8px measured vs 15px at 21pt;
// box widened to 800px so 23pt (advance 761.8px) cannot wrap) ---------------
slide.addText([
  { text: "Matrix", options: { fontFace: A, fontSize: 23, bold: true, color: "0000FF" } },
  { text: " Notation for Linear Regression and Classification ", options: { fontFace: A, fontSize: 23, bold: true, color: "FF0000" } },
  { text: "(N-", options: { fontFace: A, fontSize: 23, bold: true, color: "0000FF" } },
  { text: " Samples)", options: { fontFace: A, fontSize: 23, bold: true, color: "FF0000" } },
], {
  x: px(70), y: px(62), w: px(800), h: px(32),
  align: "center", valign: "top", margin: 0,
});

// ---- LEFT LABEL: "N Training Samples" (measured x81..272 y177..199) --------
slide.addText("N Training Samples", {
  x: px(80), y: px(173), w: px(200), h: px(30),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "FF0000",
});

// ---- TOP MATRIX BOX (measured x271..596 y107..301, blue border) -----------
slide.addShape(pptx.ShapeType.rect, {
  x: px(271), y: px(107), w: px(325), h: px(194),
  fill: { color: "FFFFFF" }, line: { color: "0000FF", width: 1 },
});

// Three full-height column bands, measured y141..296
const band_defs = [
  { cx: 315, w: 43, fill: "FFFF99", label: "X_1", entries: ["11", "12", "...", "1d"] },
  { cx: 393.5, w: 48, fill: "CCFFFF", label: "X_2", entries: ["21", "22", "...", "2d"] },
  { cx: 535, w: 45, fill: "F0A0F0", label: "X_n", entries: ["n1", "n2", "...", "nd"] },
];
for (const b of band_defs) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(b.cx - b.w / 2), y: px(141), w: px(b.w), h: px(155),
    fill: { color: b.fill },
  });
}
// Column headers above the bands (measured glyph height 19.7px incl. subscript
// vs the render's 14.4px at 13pt => ~18pt; the subscript carries the digit, so
// the base X is what sets the visual size)
for (const b of band_defs) {
  slide.addText([
    { text: "X", options: { fontFace: A, fontSize: 18, bold: true, italic: true, color: "000000" } },
    { text: b.label.split("_")[1], options: { fontFace: A, fontSize: 18, bold: true, italic: true, subscript: true, color: "000000" } },
  ], {
    x: px(b.cx - 24), y: px(115), w: px(48), h: px(24),
    align: "center", valign: "middle", margin: 0,
  });
}
// Interior entry stacks (frame-measured): glyph column inside each band with
// four stacked entries at rows y160..174, y189..203, y226, y243..257 (glyph
// height 15px => ~11pt). Each entry is its own text box at its measured row —
// LibreOffice ignores lineSpacing on inline runs, which collapsed the earlier
// 4-row stack to 2.
const entry_rows = [156, 185, 224, 240];
for (const b of band_defs) {
  for (let i = 0; i < b.entries.length; i++) {
    const e = b.entries[i];
    const isDots = (e === "...");
    slide.addText([
      ...(isDots ? [{ text: "...", options: { fontFace: A, fontSize: 11, italic: true, color: "000000" } }] : [
        { text: "x", options: { fontFace: A, fontSize: 11, italic: true, color: "000000" } },
        { text: e, options: { fontFace: A, fontSize: 11, italic: true, subscript: true, color: "000000" } },
      ]),
    ], {
      x: px(b.cx - b.w / 2), y: px(entry_rows[i]), w: px(b.w), h: px(18),
      align: "center", valign: "middle", margin: 0,
    });
  }
}
// Column delimiters, left+right per column — att34 PIL adjudication
// (adjudication_att34_topbox.md): the originals are SHALLOW PARENS (sagitta
// 1.0-1.5px, all six bowing in the paren direction; render control was 0.0),
// not straight bars. Replaced the line shapes with generated arc PNGs
// (parens/col{1,2,4}_{L,R}.png, same mechanism as the midcol arcs, ink colors
// sampled from the frame strokes). Measured bulge cores:
// yellow L296.5/R331.5, cyan L373.5/R409 (NOT 414.5 — att31 mis-measured),
// pink L517.5/R552.5 (NOT 556.5); spans y146..263 (th210; the y141..296 the
// att31 fix used was FILL extent — threshold pollution; strokes stop at 263).
const col_delims = [
  { img: "col1_L", x: 296.2 }, { img: "col1_R", x: 327.96 },
  { img: "col2_L", x: 373.2 }, { img: "col2_R", x: 405.46 },
  { img: "col4_L", x: 517.2 }, { img: "col4_R", x: 548.96 },
];
for (const d of col_delims) {
  slide.addImage({
    path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/" + d.img + ".png",
    x: px(d.x), y: px(146), w: px(3.8), h: px(117),
  });
}
// Separator line under the entries, measured y297
slide.addShape(pptx.ShapeType.line, {
  x: px(272), y: px(297.5), w: px(323), h: 0,
  line: { color: "000000", width: 1 },
});
// Red y-labels inside the bands, measured glyph h=16.3px => ~12pt (was 11pt)
const y_labels = ["y_1", "y_2", "y_n"];
for (let c = 0; c < 3; c++) {
  slide.addText([
    { text: "y", options: { fontFace: A, fontSize: 12, italic: true, color: "FF0000" } },
    { text: y_labels[c].split("_")[1], options: { fontFace: A, fontSize: 12, italic: true, subscript: true, color: "FF0000" } },
  ], {
    x: px(band_defs[c].cx - 20), y: px(274), w: px(40), h: px(18),
    align: "center", valign: "middle", margin: 0,
  });
}
// red "..." continuing the y-sequence between y_2 and y_n — measured red ink
// x466..479 y285..287 on the frame (the render previously had none)
slide.addText("...", {
  x: px(462), y: px(278), w: px(24), h: px(16),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 11, italic: true, color: "FF0000",
});
// Ellipsis column between cyan and pink (measured x449..479: gray parens
// spanning y159..249 with FOUR horizontal "..." rows at y171/198/222/249).
slide.addText("...", {
  x: px(420), y: px(115), w: px(56), h: px(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 18, bold: true, italic: true, color: "000000",
});
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_midcol_L.png", x: px(451), y: px(157), w: px(3.8), h: px(94) });
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_midcol_R.png", x: px(468), y: px(157), w: px(3.8), h: px(94) });
for (const dy of [163, 190, 214, 241]) {
  slide.addText("...", {
    x: px(448), y: px(dy), w: px(30), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: A, fontSize: 12, bold: true, italic: true, color: GRAY,
  });
}

// ---- REMEMBER BOX (measured x649..874 y153..221, blue border, pale fill) ---
const rb_x = 649, rb_y = 153, rb_w = 225, rb_h = 68;
slide.addShape(pptx.ShapeType.rect, {
  x: px(rb_x), y: px(rb_y), w: px(rb_w), h: px(rb_h),
  fill: { color: "E5FEFA" }, line: { color: "0000FF", width: 1.5 },
});
// red bold italic "Remember" — measured ink x656..689 y160..176
slide.addText("Remember", {
  x: px(rb_x + 7), y: px(rb_y + 4), w: px(120), h: px(22),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 18, bold: true, color: "FF0000", italic: true,
});
// "y = W^T X = X^T W" — blue underlined W/X per the frame (ink x699..867 y185..214)
const eq_size = 18;
slide.addText([
  { text: "y", options: { fontFace: A, fontSize: eq_size, italic: true, bold: true, color: "0000FF", underline: true } },
  { text: " = ", options: { fontFace: A, fontSize: eq_size, color: "000000" } },
  { text: "W", options: { fontFace: A, fontSize: eq_size, bold: true, color: "0000FF", underline: true } },
  { text: "T", options: { fontFace: A, fontSize: eq_size, italic: true, superscript: true, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: eq_size, bold: true, color: "FF0000", underline: true } },
  { text: " = ", options: { fontFace: A, fontSize: eq_size, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: eq_size, bold: true, color: "FF0000", underline: true } },
  { text: "T", options: { fontFace: A, fontSize: eq_size, italic: true, superscript: true, color: "000000" } },
  { text: "W", options: { fontFace: A, fontSize: eq_size, bold: true, color: "0000FF", underline: true } },
], {
  x: px(697), y: px(184), w: px(180), h: px(30),
  align: "left", valign: "middle", margin: 0,
});
// Sidecar for the post-certification OMML wrap (orchestrator pass).
fs.writeFileSync(ASSET_DIR + "/eq_003_remember.json", JSON.stringify({
  rel_id: null, image: "assets/eq_003_remember.png",
  mathtext: "y = W^{T}X = X^{T}W", font_size_pt: eq_size, color: "000000",
  blue_runs: ["W", "X", "X", "W"], underline: true,
  note: "native text runs with underline; PNG superseded by the measured build",
}, null, 2));

// ---- IN GENERAL BOX (measured x659..850 y268..294, border #6C5B3D) ---------
const ig_x = 659, ig_y = 268, ig_w = 191, ig_h = 26;
slide.addShape(pptx.ShapeType.rect, {
  x: px(ig_x), y: px(ig_y), w: px(ig_w), h: px(ig_h),
  fill: { color: "FFFFFF" }, line: { color: "6C5B3D", width: 1 },
});
slide.addText([
  { text: "In General: ", options: { fontFace: A, fontSize: 15, color: "000000" } },
  { text: "N", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
  { text: " >>> ", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
  { text: "d", options: { fontFace: A, fontSize: 15, bold: true, color: "FF0000" } },
], {
  x: px(ig_x + 6), y: px(ig_y + 2), w: px(ig_w - 12), h: px(ig_h - 4),
  align: "left", valign: "middle", margin: 0,
});

// ---- BOTTOM-LEFT BOX (measured x79..533 y323..517, RED border, white fill) -
// The frame draws the expanded equation as ROW BANDS (yellow y368..390,
// cyan y397..423, white ellipsis row y427..452, pink y456..478) with the
// y-vector left, "=" , the w-vector right, a gray "]" after the matrix, and
// three dimension labels below (N x 1, N x d+1, d+1 x 1).
slide.addShape(pptx.ShapeType.rect, {
  x: px(79), y: px(323), w: px(454), h: px(194),
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
});

// Row bands: measured x196..393 (matrix width only, from left paren to the
// right curve) for yellow/cyan/orchid.
const row_bands = [
  { y: 368, h: 22, fill: "FFFF99" },
  { y: 397, h: 26, fill: "CCFFFF" },
  { y: 456, h: 22, fill: "F0A0F0" },
];
for (const rb of row_bands) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(196), y: px(rb.y), w: px(197), h: px(rb.h),
    fill: { color: rb.fill },
  });
}

// y-vector chips: pale fills behind each entry (measured x108..136,
// y368..391 / y399..423 / y455..479 — same palette as the matrix row bands;
// the ellipsis row carries NO chip).
for (const chip of [
  { y: 368, h: 23, fill: "FFFF99" },
  { y: 399, h: 24, fill: "CCFFFF" },
  { y: 455, h: 24, fill: "F0A0F0" },
]) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(108), y: px(chip.y), w: px(28), h: px(chip.h),
    fill: { color: chip.fill },
  });
}

// y-vector: bracket pair + y_1 (gold), y_2 (teal), ... (red), y_n (magenta)
// — label colors measured from the frame (match the chip palette, darker).
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_yvec_L.png", x: px(107), y: px(358), w: px(3.8), h: px(128) });
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_yvec_R.png", x: px(129), y: px(358), w: px(3.8), h: px(128) });
const y_entries = ["y_1", "y_2", "...", "y_n"];
const y_colors = ["C8963C", "46A0A8", "C00000", "CC3FB0"];
const y_ys = [368, 397, 427, 456];
const y_hs = [22, 26, 25, 24];
for (let i = 0; i < y_entries.length; i++) {
  const e = y_entries[i];
  const runs = e === "..."
    ? [{ text: "...", options: { fontFace: A, fontSize: 15, italic: true, color: y_colors[i] } }]
    : [
        { text: "y", options: { fontFace: A, fontSize: 15, italic: true, color: y_colors[i] } },
        { text: e.split("_")[1], options: { fontFace: A, fontSize: 15, italic: true, subscript: true, color: y_colors[i] } },
      ];
  slide.addText(runs, {
    x: px(109), y: px(y_ys[i]), w: px(34), h: px(y_hs[i]),
    align: "center", valign: "middle", margin: 0,
  });
}
slide.addText("N × 1", {
  x: px(140), y: px(462), w: px(60), h: px(18),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "C00000",
});

slide.addText("=", {
  x: px(144), y: px(387), w: px(24), h: px(30),
  align: "center", valign: "middle", margin: 0,
  fontFace: A, fontSize: 24, color: "000000", bold: true,
});

// Matrix: four rows. The ORIGINAL has a leading "1" (bias) column — serif
// "1" glyphs at x210 per row — inside tall parentheses (left vertical
// x196 y366..481, right curve x358..368), then x11 x12 x1d. The middle
// (white) row draws "1" in column 1 and ellipsis dots under the three
// x-columns (measured dots at x254..270, x283..300, x329..344); it has NO
// dots column of its own.
const mx_x = 192;
const row_defs = [
  { y: 368, h: 22, fill: "FFFF99", cells: [["1", ""], ["x", "11"], ["x", "12"], ["...", ""], ["x", "1d"]] },
  { y: 397, h: 26, fill: "CCFFFF", cells: [["1", ""], ["x", "21"], ["x", "22"], ["...", ""], ["x", "2d"]] },
  { y: 427, h: 25, fill: "FFFFFF", cells: [["1", ""], ["...", ""], ["...", ""], ["...", ""], ["...", ""]] },
  { y: 456, h: 22, fill: "F0A0F0", cells: [["1", ""], ["x", "n1"], ["x", "n2"], ["...", ""], ["x", "nd"]] },
];
const cell_cols = [17, 53, 98, 138, 173];
for (const r of row_defs) {
  for (let c = 0; c < r.cells.length; c++) {
    const [txt, sub] = r.cells[c];
    slide.addText([
      { text: txt, options: { fontFace: A, fontSize: 10, italic: true, color: "000000" } },
      ...(sub ? [{ text: sub, options: { fontFace: A, fontSize: 10, italic: true, subscript: true, color: "000000" } }] : []),
    ], {
      x: px(mx_x + cell_cols[c]), y: px(r.y), w: px(40), h: px(r.h),
      align: "left", valign: "middle", margin: 0,
    });
  }
}
// tall parentheses spanning all matrix rows (original: left vertical x196
// y366..481, right curve x358..368)
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_matrix_L.png", x: px(194), y: px(362), w: px(3.8), h: px(122) });
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_matrix_R.png", x: px(388), y: px(362), w: px(3.8), h: px(122) });
// nested double-paren inner verticals — measured on the frame at x198.5 and
// x394.5 spanning y~366..477; the arcs carry the other two paren sides
slide.addShape(pptx.ShapeType.line, {
  x: px(198.5), y: px(366), w: 0, h: px(111),
  line: { color: "000000", width: 0.75 },
});
slide.addShape(pptx.ShapeType.line, {
  x: px(394.5), y: px(366), w: 0, h: px(111),
  line: { color: "000000", width: 0.75 },
});
// "N x d+1" dimension label — measured right of the matrix's right bracket
// (glyphs x399..460, y468..486), near-black 333333 as measured.
slide.addText("N × d+1", {
  x: px(399), y: px(468), w: px(110), h: px(20),
  align: "left", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "333333",
});

// w-vector: bracket pair + b (red), w_1, w_2, ..., w_d (blue)
// The ORIGINAL draws the entries at measured rows y352(b, blue), y390(w_1),
// y418(w_2), y455(ellipsis), y472(w_d) — explicit boxes per entry (LO ignores
// line spacing/stretch on inline runs, which scattered the earlier stacked
// build). Measured glyph height 26px => ~13pt for the entries.
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_wvec_L.png", x: px(458), y: px(348), w: px(3.8), h: px(130) });
slide.addImage({ path: "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/parens/arc_wvec_R.png", x: px(516), y: px(348), w: px(3.8), h: px(130) });
const w_rows = [
  { y: 350, isB: true },
  { y: 388, isB: false, sub: "1" },
  { y: 416, isB: false, sub: "2" },
  { y: 453, dots: true },
  { y: 470, isB: false, sub: "d" },
];
for (const w of w_rows) {
  const size = w.isB ? 13 : 13;
  slide.addText([
    ...(w.dots ? [{ text: "...", options: { fontFace: A, fontSize: size, italic: true, color: "000000" } }] : [
      { text: w.isB ? "b" : "w",
        options: { fontFace: A, fontSize: size, bold: w.isB, italic: !w.isB,
                   color: w.isB ? "FF0000" : "0000FF" } },
      ...(w.sub ? [{ text: w.sub, options: { fontFace: A, fontSize: size, italic: true, subscript: true, color: "0000FF" } }] : []),
    ]),
  ], {
    x: px(462), y: px(w.y), w: px(56), h: px(24),
    align: "center", valign: "middle", margin: 0,
  });
}
slide.addText("d+1 × 1", {
  x: px(452), y: px(486), w: px(76), h: px(18),
  align: "center", valign: "top", margin: 0,
  fontFace: A, fontSize: 11, bold: true, color: "4D429E",
});

// ---- ARROW: the original is a thin gray line (ink x531..533 spanning the
// whole zone, x569..572 for the head) drawn from the bottom-left box to the
// bottom-right box; measured at x532..572, head y402..407 ----------------
slide.addShape(pptx.ShapeType.line, {
  x: px(543), y: px(408), w: px(34), h: 0,
  line: { color: GRAY, width: 1.5, endArrowType: "triangle" },
});

// ---- BOTTOM-RIGHT BOX (measured x585..886 y323..517, RED border, white) ----
const br_x = 585, br_y = 323, br_w = 301, br_h = 194;
slide.addShape(pptx.ShapeType.rect, {
  x: px(br_x), y: px(br_y), w: px(br_w), h: px(br_h),
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
});

// Original layout (measured): heading "Y = X W" glyphs y362..383 with the Y
// underline y380..383 (x604..620) — X is BLUE, W is RED; "Where:" line-1
// glyphs at y398..431 with X + its subscript in BLUE; line-2 at y446..470
// with Y + subscript in RED, indented to align under the X.
slide.addText([
  { text: "Y", options: { fontFace: A, fontSize: 16, bold: true, color: "000000", underline: true } },
  { text: " = ", options: { fontFace: A, fontSize: 16, bold: true, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: 16, bold: true, color: "0000FF", underline: true } },
  { text: " ", options: { fontFace: A, fontSize: 16, bold: true, color: "000000" } },
  { text: "W", options: { fontFace: A, fontSize: 16, bold: true, color: "FF0000", underline: true } },
], {
  x: px(br_x + 20), y: px(356), w: px(br_w - 40), h: px(30),
  align: "left", valign: "top", margin: 0,
});

slide.addText([
  { text: "Where: ", options: { fontFace: A, fontSize: 13, color: "000000" } },
  { text: "X", options: { fontFace: A, fontSize: 13, color: "0000FF", underline: true, italic: true } },
  { text: "N×d+1", options: { fontFace: A, fontSize: 13, color: "0000FF", italic: true, subscript: true } },
  { text: " is a matrix", options: { fontFace: A, fontSize: 13, color: "000000", bold: true } },
], {
  x: px(br_x + 20), y: px(398), w: px(br_w - 40), h: px(22),
  align: "left", valign: "top", margin: 0,
});

slide.addText([
  { text: "Y", options: { fontFace: A, fontSize: 13, color: "FF0000", underline: true, italic: true } },
  { text: "N×1", options: { fontFace: A, fontSize: 13, color: "FF0000", italic: true, subscript: true } },
  { text: " is labels vector", options: { fontFace: A, fontSize: 13, color: "000000", bold: true } },
], {
  x: px(br_x + 83), y: px(446), w: px(br_w - 103), h: px(22),
  align: "left", valign: "top", margin: 0,
});

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE " + OUT);
}).catch(err => {
  console.error("ERROR:", err);
});
