// slide_059.js — "Transformer Encoder" classifier stack (002_transformers_part2)
// Deep Learning DSAI 308 — STANDALONE build (59←38 is a PATTERN-level dependency:
// family grammar of 8-column token rows / colored dimension cells / 5-dot ellipsis /
// red ⊕ / color-coded left annotations — NOT 38's composition).
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js, numeral 59.
// All geometry below is PIL-MEASURED on THIS slide's own frame
// (scratch/slide059/m1..m13, v1..v4 scans, 2026-10-12; frame→slide mapping identical
// to certified 038: slide_x = (fx-18.63)/0.96123, slide_y = fy/0.95556).
// Spec deltas found by PIL (raw ran on fallback glm-5.3-flash): SIX head columns per
// token row (X_1..X_6 / Vector_P0..P5; raw said five), Y labels RED like X (raw said
// blue), ellipsis columns between encoder bars are DARK-RED 3-dot columns (raw said
// white), input container fill is lilac ~F5DCF6 (raw said FADBD8), green dashed band
// has a pale-mint fill (raw said no fill), pooled row = 20 pastel cells (raw said ~30).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const pt = (v) => v / 72; // slide pts -> inches

const FONT = "Arial";
const SERIF = "Times New Roman";

// ---- palette (measured cores / family standards) ----
const LILAC = "F5DCF6";   // input container fill (measured 246,220,247)
const MINT = "F0FEE4";    // green dashed band fill (measured 242,255,222)
const PEACH = "FDEBD0";   // orange dashed band fill (spec + measured)
const LBLUE = "D6EAF8";   // Y band fill (spec + measured)
const ROSE = "CD5C5C";    // encoder container (spec + measured 205,92,92)
const BARRED = "A00000";  // bars + ellipsis dots + plus disc (measured 150-160,0,0)
const NAVY = "00008B";    // softmax circles, Vector labels
const RIMRED = "C00000";  // softmax circle bottom rim / base (measured 196,0,4)
const GREEN = "00B050";   // green dashes, X/V dots, word-emb annotation
const BLUE = "0000CC";    // Y dots, C labels, Output Classes, position annotation
const LBLUELN = "2E64FE"; // Y band dashed border
const ORANGE = "E67E22";  // Softmax Layer text, orange dashes
const TAN = "F5CBA7";     // softmax bar
const CELL_LINE = "7F7F7F";
const POOL_LINE = "A6A6A6";
const TOKRED = "9C2020";  // X/Y label serif ink (measured core ~128,32,33)
const ARW_OUT = "20208F"; // block-arrow outline (measured ~24,20,115)
const ARW_FILL = "EDEFFF";
const FAN = "FFB3B1";     // fan lines (measured 255,179,177)

function lead(size) { return 0.273 * size; }

// line segment helper: renders (x1,y1)->(x2,y2)
function seg(slide, pptx, x1, y1, x2, y2, color, width) {
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  const flipV = (x2 - x1) * (y2 - y1) < 0; // up-right / down-left
  slide.addShape(pptx.ShapeType.line, {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h), flipV,
    line: { color, width },
  });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel, red border, badge 59) ----
drawHouseChrome(pres, s, { numeral: 59 });

// ---- 2. input-sequence container (lilac, rounded) ----
s.addShape(pres.ShapeType.roundRect, {
  x: pt(49.3), y: pt(402.9), w: pt(858.3), h: pt(132.8),
  fill: { color: LILAC }, line: { type: "none" }, rectRadius: 0.06,
});

// ---- 3. token-row bands ----
// green dashed band (word-embedding row) with pale-mint fill
s.addShape(pres.ShapeType.roundRect, {
  x: pt(154.3), y: pt(428.9), w: pt(747.6), h: pt(33.4),
  fill: { color: MINT }, line: { color: GREEN, width: 1, dashType: "dash" }, rectRadius: 0.05,
});
// orange dashed band (position-vector row) with peach fill
s.addShape(pres.ShapeType.roundRect, {
  x: pt(154.3), y: pt(491.7), w: pt(747.6), h: pt(37.6),
  fill: { color: PEACH }, line: { color: ORANGE, width: 1, dashType: "dash" }, rectRadius: 0.05,
});
// Y band: light-blue fill, blue dashed border
s.addShape(pres.ShapeType.roundRect, {
  x: pt(154.3), y: pt(236.5), w: pt(750.7), h: pt(34.5),
  fill: { color: LBLUE }, line: { color: LBLUELN, width: 1, dashType: "dash" }, rectRadius: 0.05,
});

// ---- 4. token columns (shared grid) ----
// X/Y rows: 5-cell groups (yellow, mint, pink, lavender, pink-lilac), 61.4pt wide
const CELLW = 61.4 / 5;
const CELL_COLORS = ["FCFCD4", "F0FEE4", "FFB6B6", "DCDFF2", "F2D9F4"];
const HEAD_LEFTS = [0, 1, 2, 3, 4, 5].map((i) => 174.1 + 76.46 * i);
const TAIL_LEFTS = [751.6, 829.6];
const GROUP_LEFTS = HEAD_LEFTS.concat(TAIL_LEFTS);
const X_SUBS = ["0", "1", "2", "3", "4", "5", "N-2", "N-1"];

function drawTokenRow(cellY, cellH, letter, labelColor, dotColor, dotCy) {
  for (const L of GROUP_LEFTS) {
    for (let c = 0; c < 5; c++) {
      s.addShape(pres.ShapeType.rect, {
        x: pt(L + c * CELLW), y: pt(cellY), w: pt(CELLW), h: pt(cellH),
        fill: { color: CELL_COLORS[c] }, line: { color: CELL_LINE, width: 0.75 },
      });
    }
  }
  // labels: serif bold italic + subscript, centered on the group
  for (let i = 0; i < 8; i++) {
    const L = GROUP_LEFTS[i];
    s.addText(
      [
        { text: letter, options: {} },
        { text: X_SUBS[i], options: { subscript: true } },
      ],
      {
        x: pt(L), y: pt(cellY - 1.5), w: pt(61.4), h: pt(cellH + 3),
        align: "center", valign: "middle", margin: 0,
        fontFace: SERIF, fontSize: 11, bold: true, italic: true, color: labelColor,
      }
    );
  }
  // 5 ellipsis dots between col6 and the tail
  for (const dx of [642.9, 661.5, 680.3, 699.0, 715.1]) {
    s.addShape(pres.ShapeType.ellipse, {
      x: pt(dx - 3.1), y: pt(dotCy - 3.1), w: pt(6.2), h: pt(6.2),
      fill: { color: dotColor },
    });
  }
}

drawTokenRow(244.9, 16.8, "Y", TOKRED, BLUE, 253.3);   // output row (Y labels red, like X)
drawTokenRow(440.5, 16.8, "X", TOKRED, GREEN, 448.9);  // embedding row

// ---- 5. V row (position vectors): 2-cell bars, navy labels + red-orange subs ----
for (let i = 0; i < 8; i++) {
  const L = i < 6 ? HEAD_LEFTS[i] : [749.4, 827.4][i - 6];
  s.addShape(pres.ShapeType.rect, {
    x: pt(L), y: pt(495.9), w: pt(51.4), h: pt(25.2),
    fill: { color: "FBF0D2" }, line: { color: CELL_LINE, width: 0.75 },
  });
  s.addShape(pres.ShapeType.rect, {
    x: pt(L + 51.4), y: pt(495.9), w: pt(22.6), h: pt(25.2),
    fill: { color: "F2D8C8" }, line: { color: CELL_LINE, width: 0.75 },
  });
}
const V_SUBS = ["P0", "P1", "P2", "P3", "P4", "P5", "PN-2", "PN-1"];
for (let i = 0; i < 8; i++) {
  const L = i < 6 ? HEAD_LEFTS[i] : [749.4, 827.4][i - 6];
  s.addText(
    [
      { text: "Vector", options: { color: NAVY } },
      { text: V_SUBS[i], options: { subscript: true, color: NAVY } },
    ],
    {
      x: pt(L - 3), y: pt(495.9), w: pt(46), h: pt(25.2),
      align: "center", valign: "middle", margin: 0,
      fontFace: SERIF, fontSize: 9.5, bold: true, italic: true,
    }
  );
}
// V-row dots (green)
for (const dx of [642.9, 661.5, 680.3, 699.0, 715.1]) {
  s.addShape(pres.ShapeType.ellipse, {
    x: pt(dx - 3.1), y: pt(510.7 - 3.1), w: pt(6.2), h: pt(6.2),
    fill: { color: GREEN },
  });
}

// ---- 6. red plus circle between the two input sub-rows ----
s.addShape(pres.ShapeType.ellipse, {
  x: pt(500.3 - 11.45), y: pt(477.2 - 11.45), w: pt(22.9), h: pt(22.9),
  fill: { color: BARRED },
});
s.addText("+", {
  x: pt(500.3 - 11.45), y: pt(477.2 - 11.45), w: pt(22.9), h: pt(22.9),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 13, bold: true, color: "FFFFFF",
});

// ---- 7. transformer encoder container + 3 bars + ellipsis columns + title ----
s.addShape(pres.ShapeType.rect, {
  x: pt(130.4), y: pt(288.8), w: pt(762.6), h: pt(99.4),
  fill: { color: ROSE },
});
const BARS = [[292.0, 18.8], [314.0, 18.8], [368.4, 18.8]];
for (const [by, bh] of BARS) {
  s.addShape(pres.ShapeType.rect, {
    x: pt(147.1), y: pt(by), w: pt(723.0), h: pt(bh),
    fill: { color: BARRED },
  });
  s.addText("Transformer Block", {
    x: pt(427.3), y: pt(by), w: pt(150), h: pt(bh),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 10.5, bold: true, color: "FFFFFF",
  });
}
// six dark-red 3-dot ellipsis columns between bar2 and bar3
for (const cx of [248.5, 308.8, 377.9, 626.1, 701.6, 771.8]) {
  for (const cy of [340.6, 350.0, 360.0]) {
    s.addShape(pres.ShapeType.ellipse, {
      x: pt(cx - 3.15), y: pt(cy - 3.15), w: pt(6.3), h: pt(6.3),
      fill: { color: BARRED },
    });
  }
}
s.addText("Transformer Encoder", {
  x: pt(351.5), y: pt(342.2 - lead(20.5)), w: pt(300), h: pt(26),
  align: "center", valign: "top", margin: 0,
  fontFace: FONT, fontSize: 20.5, bold: true, color: "FFFFFF", lineSpacing: 24,
});

// ---- 8. GAP box ----
s.addShape(pres.ShapeType.rect, {
  x: pt(159.7), y: pt(192.6), w: pt(743.2), h: pt(24.0),
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1 },
});
s.addText("Global Average Pooling", {
  x: pt(159.7), y: pt(192.6), w: pt(743.2), h: pt(24.0),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 17, bold: true, color: "000000",
});

// ---- 9. pooled single-vector row: 20 pastel cells ----
const POOL_COLORS = ["FEFFC5", "E3FFCB", "EDE4C1", "F8DBC1", "E2DCF3", "F5D6EE"];
for (let i = 0; i < 20; i++) {
  s.addShape(pres.ShapeType.rect, {
    x: pt(384.4 + i * 12.6), y: pt(153.8), w: pt(12.6), h: pt(18.9),
    fill: { color: POOL_COLORS[i % 6] }, line: { color: POOL_LINE, width: 0.5 },
  });
}

// ---- 10. fan lines: pooled row -> three softmax bases ----
const BASE_CX = [438.5, 514.0, 589.3];
const FAN_STARTS = [
  [386, 408, 430, 452, 474, 496],
  [452, 474, 496, 518, 540, 562],
  [518, 540, 562, 584, 606, 628],
];
for (let b = 0; b < 3; b++) {
  for (const xs of FAN_STARTS[b]) {
    seg(s, pres, xs, 153.8, BASE_CX[b], 130.5, FAN, 0.75);
  }
}

// ---- 11. softmax bar + three navy circles ----
s.addShape(pres.ShapeType.rect, {
  x: pt(163.7), y: pt(95.2), w: pt(715.9), h: pt(20.9),
  fill: { color: TAN },
});
s.addText("Softmax Layer", {
  x: pt(168.5), y: pt(97.0), w: pt(120), h: pt(16),
  align: "left", valign: "top", margin: 0,
  fontFace: FONT, fontSize: 14, bold: true, color: ORANGE,
});
for (const cx of BASE_CX) {
  // red bottom rim: red circle behind, shifted down ~3pt
  s.addShape(pres.ShapeType.ellipse, {
    x: pt(cx - 18.85), y: pt(109.3 - 18.85), w: pt(37.7), h: pt(37.7),
    fill: { color: RIMRED },
  });
  s.addShape(pres.ShapeType.ellipse, {
    x: pt(cx - 18.85), y: pt(106.2 - 18.85), w: pt(37.7), h: pt(37.7),
    fill: { color: NAVY },
  });
  s.addText("Softmax", {
    x: pt(cx - 18), y: pt(95.5), w: pt(36), h: pt(9),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 7.5, bold: true, color: "F7DC6F",
  });
  s.addText("\u03A3", {
    x: pt(cx - 12), y: pt(104.0), w: pt(24), h: pt(19),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, color: "FFFFFF",
  });
  // thin stem up to the class label
  s.addShape(pres.ShapeType.line, {
    x: pt(cx), y: pt(76.5), w: 0, h: pt(10.8),
    line: { color: LBLUELN, width: 1, beginArrowType: "triangle" },
  });
}

// ---- 12. class labels + Output Classes ----
for (let i = 0; i < 3; i++) {
  s.addText(
    [
      { text: "C", options: {} },
      { text: String(i + 1), options: { subscript: true } },
    ],
    {
      x: pt(BASE_CX[i] - 15), y: pt(58.4), w: pt(30), h: pt(16),
      align: "center", valign: "top", margin: 0,
      fontFace: SERIF, fontSize: 12, bold: true, italic: true, color: BLUE,
    }
  );
}
s.addText("Output Classes", {
  x: pt(312.4), y: pt(55.0), w: pt(120), h: pt(18),
  align: "left", valign: "top", margin: 0,
  fontFace: FONT, fontSize: 13, bold: true, color: BLUE,
});

// ---- 13. four block arrows (up, blue outline, pale fill), centerline x=511 ----
const ARROWS = [[387.2, 25.0], [271.0, 18.9], [213.5, 22.0], [172.7, 19.9]];
for (const [ay, ah] of ARROWS) {
  s.addShape(pres.ShapeType.upArrow, {
    x: pt(511.0 - 7.8), y: pt(ay), w: pt(15.6), h: pt(ah),
    fill: { color: ARW_FILL }, line: { color: ARW_OUT, width: 1 },
  });
}

// ---- 14. left annotations ----
s.addText(
  [
    { text: "Single vector representing", options: { breakLine: true } },
    { text: "the whole sequence", options: {} },
  ],
  {
    x: pt(70.1), y: pt(147.6 - lead(13.5)), w: pt(200), h: pt(32),
    align: "left", valign: "top", margin: 0,
    fontFace: SERIF, fontSize: 13.5, italic: true, color: "C00000", lineSpacing: 15.7,
  }
);
s.addText(
  [
    { text: "Output", options: { breakLine: true } },
    { text: "Sequence", options: {} },
  ],
  {
    x: pt(64.9), y: pt(240.7 - lead(14)), w: pt(100), h: pt(32),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, italic: true, color: "C00000", lineSpacing: 14.6,
  }
);
s.addText("Input Sequence", {
  x: pt(49.3), y: pt(405.0 - lead(14)), w: pt(120), h: pt(18),
  align: "left", valign: "top", margin: 0,
  fontFace: FONT, fontSize: 14, bold: true, italic: true, color: "C00000",
});
s.addText(
  [
    { text: "Word", options: { breakLine: true } },
    { text: "Embedding", options: { breakLine: true } },
    { text: "Vectors", options: {} },
  ],
  {
    x: pt(66.2), y: pt(429.1 - lead(13)), w: pt(110), h: pt(46),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, italic: true, color: GREEN, lineSpacing: 13.6,
  }
);
s.addText(
  [
    { text: "Position", options: { breakLine: true } },
    { text: "Information", options: { breakLine: true } },
    { text: "Vectors", options: {} },
  ],
  {
    x: pt(66.0), y: pt(485.6 - lead(13)), w: pt(110), h: pt(46),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 13, bold: true, italic: true, color: BLUE, lineSpacing: 13.6,
  }
);

// ---- write ----
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_059_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
