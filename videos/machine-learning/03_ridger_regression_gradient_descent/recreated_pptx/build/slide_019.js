// Build slide 019 — "Test Data" — Ridge Regression gradient descent
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent
// Attempt 2 — same measurements; the attempt-1 textBox() helper passed
// lineSpacing as a multiplier, which pptxgenjs emits as POINTS (1.2pt), so
// LibreOffice dropped every body text run (only the badge numeral survived).
// Attempt 2 derives line spacing in points from the run's fontSize.
//
// ═══════════════════════════════════════════════════════════════════════════════
// GROUND TRUTH: unique_slides/slide_019.jpg — 960x540, exactly 72 px/in
//                (verified: 960/13.3333 = 72.0001) => 1 frame px == 1 pt == 1/72 in.
// All geometry below is in FRAME PX == POINTS. Converted to inches by px().
// Measurement bank: recreated_pptx/qa/slide019/
// ═══════════════════════════════════════════════════════════════════════════════
//
// CONTENT (all PIL-verified):
//   * Title bar: blue-bordered box "Test Data" at x68..434, y66..159
//   * Badge: yellow circle "19" centered at (876,73)px, d≈35px, purple ring
//   * Test point reference: "z₁=(30,15), y=60; z₂=(40,20), y=80; z₃=(50,25), y=100"
//     at y=80..99, x=433..895
//   * Outlier column: x=60..124, y=169..524
//     - Blue header "Outlier X_s" at y=170
//     - Three black text rows: "11, 3, 22", "30, 3, 22", "60, 3, 22"
//   * Three main columns with blue bold headers at y=170..199:
//     - NO REG (λ=0): x=124..380
//     - RIDGE λ=3: x=384..640
//     - RIDGE λ=10: x=644..900
//   * Each main column has 3 row groups (one per outlier scenario), each with:
//     - Red: W vector + ||W||²
//     - Black: x₁,x₂ for Test1/Test2/Test3
//     - Green: predicted y for Test1/Test2/Test3
//   * Two black right-pointing arrows between columns at mid-height
//   * Color hierarchy: Blue headers > Red W/||W||² > Green y-preds > Black x-values
// ═══════════════════════════════════════════════════════════════════════════════

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_019_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches (1 frame px == 1 pt)

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top stroke on this deck), badge with numeral 19.
drawHouseChrome(pptx, slide, { numeral: 19 });

// ── COLOR PALETTE ──────────────────────────────────────────────────────────────
const BLUE   = "0000FF";  // headers, title
const RED    = "FF0000";  // W vectors, ||W||²
const GREEN  = "008000";  // predicted y values
const BLACK  = "000000";  // x values, labels, arrows
const FONT   = "Arial";

// ── HELPERS ────────────────────────────────────────────────────────────────────
function textBox(x, y, w, h, runs, opts = {}) {
  // pptxgenjs emits lineSpacing as POINTS (spcPts), not a multiplier: a bare
  // 1.2 becomes a 1.2pt line height and LibreOffice drops the text entirely.
  const first = Array.isArray(runs) ? runs[0] : runs;
  const size = (first && first.options && first.options.fontSize) || 12;
  const defaults = {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, lineSpacing: size * 1.2,
  };
  slide.addText(runs, { ...defaults, ...opts });
}

// ── TITLE BAR ──────────────────────────────────────────────────────────────────
// Blue-bordered box at x68..434, y66..159 with "Test Data" in bold blue
// The box border is blue, text is blue bold
slide.addShape(pptx.ShapeType.rect, {
  x: px(68), y: px(66), w: px(434 - 68), h: px(159 - 66),
  line: { color: BLUE, width: 2 },
  fill: { color: "FFFFFF" }, // white interior
});
textBox(76, 72, 350, 90, [
  { text: "Test Data", options: { bold: true, color: BLUE, fontSize: 24 } }
]);

// Badge drawn by house_chrome (drawHouseChrome) — circle at (876,73) with "19"

// ── TEST POINT REFERENCE LINE ──────────────────────────────────────────────────
// y=80..99, x=433..895 — black text
textBox(433, 80, 462, 20, [
  { text: "z₁=(30, 15), y=60;  z₂=(40, 20), y=80;  z₃=(50, 25), y=100", options: { color: BLACK, fontSize: 12 } }
]);

// ── OUTLIER COLUMN ─────────────────────────────────────────────────────────────
// x=60..124, y=169..524
// Header at y=170 (blue bold)
textBox(60, 170, 64, 30, [
  { text: "Outlier Xₛ", options: { bold: true, color: BLUE, fontSize: 13 } }
]);

// Three outlier rows - measured y positions from frame
// Row 1: "11, 3, 22" around y=201..230
textBox(60, 205, 64, 60, [
  { text: "11, 3, 22", options: { color: BLACK, fontSize: 12 } }
]);

// Row 2: "30, 3, 22" around y=291..320
textBox(60, 295, 64, 60, [
  { text: "30, 3, 22", options: { color: BLACK, fontSize: 12 } }
]);

// Row 3: "60, 3, 22" around y=415..444
textBox(60, 420, 64, 60, [
  { text: "60, 3, 22", options: { color: BLACK, fontSize: 12 } }
]);

// ── MAIN CONTENT COLUMNS ───────────────────────────────────────────────────────
// Column definitions: [name, x_start, x_end, header_text]
const columns = [
  { name: "NO REG", x0: 124, x1: 380, header: "NO Regularizer with (as if λ=0)" },
  { name: "RIDGE 3", x0: 384, x1: 640, header: "Ridge Regularizer with λ=3" },
  { name: "RIDGE 10", x0: 644, x1: 900, header: "Ridge Regularizer with λ=10" },
];

// Column widths
const colW = { "NO REG": 380-124, "RIDGE 3": 640-384, "RIDGE 10": 900-644 };

// Data for each column: 3 row groups (one per outlier)
// Each row group: { w: "W=(...)", norm: "||W||²=...", tests: [{x1,x2,y}, {x1,x2,y}, {x1,x2,y}] }
const columnData = {
  "NO REG": [
    {
      w: "W=(2, 0), ||W||²=4",
      tests: [
        { x1: 30, x2: 15, y: 60 },
        { x1: 40, x2: 20, y: 80 },
        { x1: 50, x2: 25, y: 100 },
      ]
    },
    {
      w: "W=(2.7, 0.67), ||W||²=8.11",
      tests: [
        { x1: 30, x2: 15, y: 60 },
        { x1: 40, x2: 20, y: 80 },
        { x1: 50, x2: 25, y: 100 },
      ]
    },
    {
      w: "W=(4, 0.29), ||W||²=16.7",
      tests: [
        { x1: 30, x2: 15, y: 60 },
        { x1: 40, x2: 20, y: 80 },
        { x1: 50, x2: 25, y: 100 },
      ]
    },
  ],
  "RIDGE 3": [
    {
      w: "W=(0.1, 1.95), ||W||²=3.8",
      tests: [
        { x1: 30, x2: 15, y: 59 },
        { x1: 40, x2: 20, y: 78.7 },
        { x1: 50, x2: 25, y: 98.4 },
      ]
    },
    {
      w: "W=(1.2, 0.72), ||W||²=2.45",
      tests: [
        { x1: 30, x2: 15, y: 34.1 },
        { x1: 40, x2: 20, y: 45.1 },
        { x1: 50, x2: 25, y: 56.1 },
      ]
    },
    {
      w: "W=(1.77, 0.32), ||W||²=4.2",
      tests: [
        { x1: 30, x2: 15, y: 26.2 },
        { x1: 40, x2: 20, y: 34.4 },
        { x1: 50, x2: 25, y: 42.5 },
      ]
    },
  ],
  "RIDGE 10": [
    {
      w: "W=(0.13, 1.87), ||W||²=3.5",
      tests: [
        { x1: 30, x2: 15, y: 57.4 },
        { x1: 40, x2: 20, y: 76.5 },
        { x1: 50, x2: 25, y: 95.6 },
      ]
    },
    {
      w: "W=(0.54, 0.73), ||W||²=1.48",
      tests: [
        { x1: 30, x2: 15, y: 34.6 },
        { x1: 40, x2: 20, y: 46 },
        { x1: 50, x2: 25, y: 57.4 },
      ]
    },
    {
      w: "W=(0.82, 0.33), ||W||²=1.92",
      tests: [
        { x1: 30, x2: 15, y: 26.8 },
        { x1: 40, x2: 20, y: 35.4 },
        { x1: 50, x2: 25, y: 44.1 },
      ]
    },
  ],
};

// Row group y-positions (measured from frame)
// NO REG: group1 y~201..266, group2 y~271..310, group3 y~320..372
// RIDGE 3: group1 y~307..310, group2 y~320..326, group3 y~332..374
// RIDGE 10: group1 y~404..405, group2 y~415..417, group3 y~427..434
// These vary by column - use measured positions per column

const rowGroupsY = {
  "NO REG": [205, 275, 345],    // y position for W line of each group
  "RIDGE 3": [310, 325, 355],
  "RIDGE 10": [405, 420, 435],
};

for (const col of columns) {
  const x0 = col.x0;
  const w = col.x1 - col.x0;
  const data = columnData[col.name];
  const yPositions = rowGroupsY[col.name];
  
  // Column header (blue bold) at y=170..199
  textBox(x0, 170, w, 30, [
    { text: col.header, options: { bold: true, color: BLUE, fontSize: 12 } }
  ], {});
  
  // Each row group
  for (let gi = 0; gi < 3; gi++) {
    const gy = yPositions[gi];
    const group = data[gi];
    
    // W vector + ||W||² (red) - single line
    textBox(x0, gy, w, 18, [
      { text: group.w, options: { color: RED, fontSize: 11 } }
    ], {});
    
    // Three test boxes: Test1, Test2, Test3
    // Layout: "Test1: x₁=30,x₂=15,y=60" etc.
    // Black for x values, green for y
    // Position: each test in roughly equal third of column width
    const testW = w / 3;
    for (let ti = 0; ti < 3; ti++) {
      const test = group.tests[ti];
      const tx = x0 + ti * testW;
      const ty = gy + 18; // below W line
      
      // Build runs: "Test1: x₁=30,x₂=15,y=60" with x-values black, y green
      const runs = [
        { text: `Test${ti+1}: `, options: { color: BLACK, fontSize: 10 } },
        { text: `x₁=${test.x1},`, options: { color: BLACK, fontSize: 10 } },
        { text: `x₂=${test.x2},`, options: { color: BLACK, fontSize: 10 } },
        { text: `y=${test.y}`, options: { color: GREEN, fontSize: 10 } },
      ];
      textBox(tx, ty, testW, 16, runs, {});
    }
  }
}

// ── INTER-COLUMN ARROWS ────────────────────────────────────────────────────────
// Two right-pointing arrows between columns at mid-height (~y=320)
// Gap 1: between NO REG (ends at x=380) and RIDGE 3 (starts at x=384) -> center ~382
// Gap 2: between RIDGE 3 (ends at x=640) and RIDGE 10 (starts at x=644) -> center ~642
// Arrow: simple line with triangle head
const arrowY = 320;
const arrowLen = 20;

// Arrow 1: between NO REG and RIDGE 3
slide.addShape(pptx.ShapeType.line, {
  x: px(380), y: px(arrowY), w: px(arrowLen), h: 0,
  line: { color: BLACK, width: 1.5, endArrowType: "triangle" },
});

// Arrow 2: between RIDGE 3 and RIDGE 10
slide.addShape(pptx.ShapeType.line, {
  x: px(640), y: px(arrowY), w: px(arrowLen), h: 0,
  line: { color: BLACK, width: 1.5, endArrowType: "triangle" },
});

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));