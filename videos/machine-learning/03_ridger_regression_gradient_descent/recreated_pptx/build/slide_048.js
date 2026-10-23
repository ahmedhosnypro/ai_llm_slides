const pptxgenpkg = require("pptxgenjs");
const { CHROME, drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";  // 13.333 x 7.5 in
const W = 13.333, H = 7.5;

let s = pptx.addSlide();

// ---- HOUSE CHROME ----
drawHouseChrome(pptx, s, { numeral: "48" });

// ---- FONT & COLOR CONSTANTS ----
const FONT = "Arial";
const BLACK = "000000";
const RED = "FF0000";
const MAROON = "8B0000";
const GREEN = "1E8449";
const BLUE_FILL = "E9F2F9";
const BLUE_BORDER = "8FB3CC";

// ---- HELPER: convert frame px to PPTX inches ----
// Frame: 960x540, 1px = 1pt = 1/72 in
// Panel origin: x=54, y=45 in frame px
const PANEL_X_IN = 54/72;
const PANEL_Y_IN = 45/72;
function fx(px) { return PANEL_X_IN + px/72; }
function fy(px) { return PANEL_Y_IN + px/72; }
function fw(px) { return px/72; }
function fh(px) { return px/72; }

// ---- 1. TOP-LEFT: Input Data Table ----
// Frame: cols 69-289, rows 46-129
// Panel-rel: x=15..235, y=1..84
// Table: 4 rows (3 feature + 1 class) x 6 cols (x1..x6)
const table1_x = fx(15);
const table1_y = fy(1);
const table1_w = fw(220);
const table1_h = fh(83);

const table1_rows = [
  // Header row: x1 x2 x3 x4 x5 x6
  [
    { text: "x\u2081", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2082", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2083", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2084", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2085", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2086", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Row 1: 1 2 1 5 6 6
  [
    { text: "1", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "2", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "5", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Row 2: 1 1 2 4 5 6
  [
    { text: "1", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "2", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "4", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "5", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Row 3: 1 2 2 4 5 6
  [
    { text: "1", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "2", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "2", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "4", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "5", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Class row: C1 C1 C1 C2 C2 C2 (red)
  [
    { text: "C1", options: { fontFace: FONT, fontSize: 12, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C1", options: { fontFace: FONT, fontSize: 12, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C1", options: { fontFace: FONT, fontSize: 12, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C2", options: { fontFace: FONT, fontSize: 12, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C2", options: { fontFace: FONT, fontSize: 12, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C2", options: { fontFace: FONT, fontSize: 12, bold: true, color: RED, align: "center", valign: "middle" } },
  ],
];

s.addTable(table1_rows, {
  x: table1_x, y: table1_y, w: table1_w, h: table1_h,
  fontFace: FONT,
  border: { pt: 0.75, color: "CCCCCC" },
  fill: { color: "FFFFFF" },
  rowH: 0.23,
});

// ---- 2. TOP-CENTER: Initial W = [4; -2; -2] ----
// Frame: cols 300-619, rows 46-124
// Panel-rel: x=246..565, y=1..79
// "Initial W =" text left of equation image
const init_w_x = fx(246);
const init_w_y = fy(1);
const init_w_w = fw(320);

// Add "Initial W =" text
s.addText("Initial W =", {
  x: init_w_x, y: init_w_y, w: fw(100), h: fh(30),
  fontFace: FONT, fontSize: 14, color: BLACK, bold: false,
  align: "left", valign: "middle", margin: 0,
});

// Add equation image: Initial W = [4; -2; -2]
// Image: w_in=2.48667, h_in=0.225, baseline_frac=0.80741
const eq_initial_w = {
  path: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_initial_w.png",
  w_in: 2.48667, h_in: 0.225, baseline_frac: 0.80741
};
// Place so baseline aligns with text baseline
// Text baseline is at y + h/2 (valign middle). Image baseline is at baseline_frac * h from top.
// So image y = text_y + text_h/2 - baseline_frac * h_in
const text_y = init_w_y;
const text_h = fh(30);
const img_y = text_y + text_h/2 - eq_initial_w.baseline_frac * eq_initial_w.h_in;
s.addImage({
  path: eq_initial_w.path,
  x: init_w_x + fw(100), y: img_y,
  w: eq_initial_w.w_in, h: eq_initial_w.h_in,
});

// REPEAT using Step η = 1 (red)
// Panel-rel: x=246+320=566..800, y=1..40 (approx)
s.addText("REPEAT using Step \u03b7 = 1", {
  x: fx(566), y: fy(1), w: fw(230), h: fh(40),
  fontFace: FONT, fontSize: 14, color: RED, bold: true,
  align: "left", valign: "top", margin: 0,
});

// ---- 3. TOP-RIGHT: Check classes of ----
// Frame: cols 615-879, rows 46-129
// Panel-rel: x=561..825, y=1..84
const check_x = fx(561);
const check_y = fy(1);

s.addText("Check classes of", {
  x: check_x, y: check_y, w: fw(264), h: fh(25),
  fontFace: FONT, fontSize: 13, color: BLACK, bold: false,
  align: "left", valign: "top", margin: 0,
});

// Z1 Z2 Z3 table (2 rows)
// Frame: cols 615-719 and 856-879 (gap at 719-856), rows 55-129
// Panel-rel: x=561..665 and 802..825, y=10..84
// Table at x=561, y=check_y+25
const ztable_x = check_x;
const ztable_y = check_y + fh(25);
const ztable_w = fw(264);
const ztable_h = fh(60);

const ztable_rows = [
  // Header
  [
    { text: "Z1", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "Z2", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "Z3", options: { fontFace: FONT, fontSize: 12, bold: true, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Row 1: 0 7 3
  [
    { text: "0", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "7", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "3", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Row 2: 0 6 2
  [
    { text: "0", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
    { text: "2", options: { fontFace: FONT, fontSize: 12, color: BLACK, align: "center", valign: "middle" } },
  ],
];

s.addTable(ztable_rows, {
  x: ztable_x, y: ztable_y, w: ztable_w, h: ztable_h,
  fontFace: FONT,
  border: { pt: 0.75, color: "CCCCCC" },
  fill: { color: "FFFFFF" },
  rowH: 0.2,
});

// "C1 positive, C2 negative, Zero is unaccepted" with C1, C2, Zero in red
// Use multiple text runs for coloring
const note_y = ztable_y + ztable_h + fh(5);
s.addText([
  { text: "C1", options: { fontFace: FONT, fontSize: 12, color: RED, bold: false } },
  { text: " positive, ", options: { fontFace: FONT, fontSize: 12, color: BLACK } },
  { text: "C2", options: { fontFace: FONT, fontSize: 12, color: RED, bold: false } },
  { text: " negative, ", options: { fontFace: FONT, fontSize: 12, color: BLACK } },
  { text: "Zero", options: { fontFace: FONT, fontSize: 12, color: RED, bold: false } },
  { text: " is unaccepted", options: { fontFace: FONT, fontSize: 12, color: BLACK } },
], {
  x: check_x, y: note_y, w: fw(264), h: fh(30),
  fontFace: FONT, margin: 0,
});

// ---- 4. MID-LEFT: "Ugmented Vectors (from Top)" header ----
// Frame: cols 60-290, rows 148-159 (header band)
// Panel-rel: x=6..235, y=103..114
const aug_header_x = fx(6);
const aug_header_y = fy(103);
s.addText("Ugmented Vectors (from Top)", {
  x: aug_header_x, y: aug_header_y, w: fw(230), h: fh(20),
  fontFace: FONT, fontSize: 13, color: BLACK, bold: false,
  align: "left", valign: "top", margin: 0,
});

// ---- 5. MID-LEFT: Augmented Vectors Matrix ----
// Frame: cols 70-289, rows 166-304
// Panel-rel: x=16..235, y=121..259
// Matrix: 4 rows (bias + 2 feature + class) x 6 cols (x1..x6)
const aug_x = fx(16);
const aug_y = fy(121);
const aug_w = fw(219);
const aug_h = fh(138);

const aug_rows = [
  // Header row: x1..x6
  [
    { text: "x\u2081", options: { fontFace: FONT, fontSize: 11, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2082", options: { fontFace: FONT, fontSize: 11, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2083", options: { fontFace: FONT, fontSize: 11, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2084", options: { fontFace: FONT, fontSize: 11, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2085", options: { fontFace: FONT, fontSize: 11, bold: true, color: BLACK, align: "center", valign: "middle" } },
    { text: "x\u2086", options: { fontFace: FONT, fontSize: 11, bold: true, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Bias row: 1 1 1 1 1 1
  [
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Feature row 1: 1 2 1 5 6 6
  [
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "2", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "5", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Feature row 2: 1 1 2 4 5 6
  [
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "1", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "2", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "4", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "5", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
    { text: "6", options: { fontFace: FONT, fontSize: 11, color: BLACK, align: "center", valign: "middle" } },
  ],
  // Class row: C1 C1 C1 C2 C2 C2 (red)
  [
    { text: "C1", options: { fontFace: FONT, fontSize: 11, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C1", options: { fontFace: FONT, fontSize: 11, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C1", options: { fontFace: FONT, fontSize: 11, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C2", options: { fontFace: FONT, fontSize: 11, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C2", options: { fontFace: FONT, fontSize: 11, bold: true, color: RED, align: "center", valign: "middle" } },
    { text: "C2", options: { fontFace: FONT, fontSize: 11, bold: true, color: RED, align: "center", valign: "middle" } },
  ],
];

s.addTable(aug_rows, {
  x: aug_x, y: aug_y, w: aug_w, h: aug_h,
  fontFace: FONT,
  border: { pt: 0.75, color: "CCCCCC" },
  fill: { color: "FFFFFF" },
  rowH: 0.276,
});

// ---- 6. MID-LEFT: Iteration 1 red box ----
// Frame: cols 274-289, rows 338-372
// Panel-rel: x=220..235, y=293..327
const iter_x = fx(220);
const iter_y = fy(293);
const iter_w = fw(15);
const iter_h = fh(34);

s.addShape(pptx.ShapeType.rect, {
  x: iter_x, y: iter_y, w: iter_w, h: iter_h,
  fill: { color: "FFFFFF" },
  line: { color: RED, width: 1.5 },
});
s.addText("Iteration 1", {
  x: iter_x, y: iter_y, w: iter_w, h: iter_h,
  fontFace: FONT, fontSize: 12, color: RED, bold: true,
  align: "center", valign: "middle", margin: 0,
});

// ---- 7. CALCULATION PANEL: 6 stacked light-blue boxes ----
// Frame: cols 300-852, rows 149-528
// Panel-rel: x=246..798, y=104..483
// 6 rows with measured y positions:
const calc_x = fx(246);
const calc_w = fw(552);  // 798-246

const calc_rows_data = [
  {
    y: fy(104), h: fh(44),  // row 1: 149-192
    eq1: "eq_dx1.png", eq1_w: 3.08333, eq1_h: 0.205, eq1_base: 0.78862,
    arrow: true,
    action: "Update Weight",
    eq2: "eq_w1.png", eq2_w: 4.305, eq2_h: 0.2, eq2_base: 0.80833,
  },
  {
    y: fy(185), h: fh(28),  // row 2: 230-258
    eq1: "eq_dx2.png", eq1_w: 3.07667, eq1_h: 0.205, eq1_base: 0.78862,
    arrow: false,
    action: "Keep same Weight",
    eq2: "eq_w2.png", eq2_w: 1.63, eq2_h: 0.2, eq2_base: 0.80833,
  },
  {
    y: fy(236), h: fh(40),  // row 3: 281-321
    eq1: "eq_dx3.png", eq1_w: 3.07667, eq1_h: 0.20667, eq1_base: 0.78226,
    arrow: false,
    action: "Keep same Weight",
    eq2: "eq_w2.png", eq2_w: 1.63, eq2_h: 0.2, eq2_base: 0.80833,
  },
  {
    y: fy(305), h: fh(40),  // row 4: 350-390
    eq1: "eq_dx4.png", eq1_w: 3.24833, eq1_h: 0.205, eq1_base: 0.78862,
    arrow: false,
    action: "Keep same Weight",
    eq2: "eq_w2.png", eq2_w: 1.63, eq2_h: 0.2, eq2_base: 0.80833,
  },
  {
    y: fy(368), h: fh(40),  // row 5: 413-453
    eq1: "eq_dx5.png", eq1_w: 3.24667, eq1_h: 0.20667, eq1_base: 0.78226,
    arrow: false,
    action: "Keep same Weight",
    eq2: "eq_w2.png", eq2_w: 1.63, eq2_h: 0.2, eq2_base: 0.80833,
  },
  {
    y: fy(434), h: fh(40),  // row 6: 479-519
    eq1: "eq_dx6.png", eq1_w: 3.24167, eq1_h: 0.20667, eq1_base: 0.78226,
    arrow: false,
    action: "Keep same Weight",
    eq2: "eq_w2.png", eq2_w: 1.63, eq2_h: 0.2, eq2_base: 0.80833,
  },
];

const assetBase = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/";

for (let i = 0; i < calc_rows_data.length; i++) {
  const r = calc_rows_data[i];
  const box_y = r.y;
  const box_h = r.h;

  // Light-blue box background
  s.addShape(pptx.ShapeType.rect, {
    x: calc_x, y: box_y, w: calc_w, h: box_h,
    fill: { color: BLUE_FILL },
    line: { color: BLUE_BORDER, width: 1 },
  });

  // Layout inside box: eq1 | ⇒ | action | eq2
  // eq1 left-aligned with some margin
  const margin_x = 0.15;
  let cur_x = calc_x + margin_x;

  // Equation 1 (d(x_i) = ...)
  const eq1_img = `${assetBase}${r.eq1}`;
  const eq1_y = box_y + box_h/2 - r.eq1_base * r.eq1_h;
  s.addImage({ path: eq1_img, x: cur_x, y: eq1_y, w: r.eq1_w, h: r.eq1_h });
  cur_x += r.eq1_w + 0.15;

  // ⇒ arrow
  s.addText("\u21d2", {
    x: cur_x, y: box_y, w: 0.3, h: box_h,
    fontFace: FONT, fontSize: 16, color: BLACK,
    align: "center", valign: "middle", margin: 0,
  });
  cur_x += 0.4;

  // Action text (Update Weight / Keep same Weight)
  const action_color = (i === 0) ? RED : MAROON;
  s.addText(r.action, {
    x: cur_x, y: box_y, w: 1.5, h: box_h,
    fontFace: FONT, fontSize: 12, color: action_color, bold: (i===0),
    align: "left", valign: "middle", margin: 0,
  });
  cur_x += 1.6;

  // Equation 2 (W = ...)
  const eq2_img = `${assetBase}${r.eq2}`;
  const eq2_y = box_y + box_h/2 - r.eq2_base * r.eq2_h;
  s.addImage({ path: eq2_img, x: cur_x, y: eq2_y, w: r.eq2_w, h: r.eq2_h });

  // Green double arrow ⇐ at far right of row 1 only
  if (r.arrow) {
    const arrow_x = calc_x + calc_w - 0.4;
    const arrow_y = box_y + box_h/2 - 0.12;
    // Use a text character for the double-lined left arrow
    s.addText("\u21d0", {
      x: arrow_x, y: arrow_y, w: 0.4, h: 0.24,
      fontFace: FONT, fontSize: 18, color: GREEN, bold: true,
      align: "center", valign: "middle", margin: 0,
    });
  }
}

// ---- WRITE FILE ----
const outPath = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_048_recreated.pptx";
pptx.writeFile({ fileName: outPath }).then(() => console.log("done: " + outPath));