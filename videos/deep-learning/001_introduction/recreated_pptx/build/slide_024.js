// slide_024.js — 001_introduction slide 24 "Neural Network Model"
// (3-layer Sigma|S network i/j/k with Error bar + Class column) — Deep Learning DSAI 308.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_024.jpg (960x540, 1px = 1pt).
//   5 measurement rounds banked in qa/slide024/measure_*; 4 gate vision reads
//   (vread_A1A3/B1B3/neurons/gap/fan.txt). Constants digest: qa/slide024/build_constants.txt.
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 24 (file number; PENDING FOUNDER VETO).
//
// FRAME-OVER-SPEC CORRECTIONS (frame + x6 vision win; declared in judge ground rules):
//   * NO i->k skip connections and NO w_ki labels exist in the frame: full 3x3 mesh
//     col2->col3 + col3->col4 only (gap vision read). Spec's skip/w_ki claim is a
//     source-analysis artifact; SOURCES.md's RHW86 skip story explains the notation
//     family but the FRAME governs recreation.
//   * Blue labels: A-gap w_ji x3 (rot 0/30/51deg riding their mesh lines), B-gap
//     w_kj x3 (rot 0/30/51deg) — x6 vision transcriptions.
//   * Output boxes are WHITE-filled with BLACK bold text (pixel modal (252,255,248);
//     spec's "black rect / white text" inverted by the pixels).
//   * Neurons: red Sigma (left half) + black sigmoid-CURVE glyph (right half, x5 vision:
//     "drawn glyph, not text") + thin dark divider; per-column border hues
//     (tan/blue/green/orange/tan); fills pale per pixel modals.
//   * Block arrows: pale fills + darker outlines, BLACK letter in the stem (vision).
//   * Rings float with no connecting lines (gap scans clean between strokes).
//   * Video-chrome red rule at x~60 omitted (certified precedent 002/005/021/023).
//   * Mouse-cursor artifact near col3 row2 OMITTED per judge ground rule (c).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_024_recreated.pptx";
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

// ---- palette (measured) ----
const TITLE_RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const PANEL_BEIGE = "DAD0C4";
const MAG_FILL = "FF99FF";
const MAG_LINE = "993366";
const MAG_DARK = "990099";   // dashed line + left arrowhead (measured #980E9F core)
const DOT_MAG = "CC00CC";
const MESH_RED = "C00000";
const FAN_GRAY = "ACA298";
const W_BLUE = "0000CC";
const ERR_FILL = "9E0000";
const ERR_TEXT = "FF0000";
const CLASS_FILL = "E3FFCF";
const OUTBOX_FILL = "FFFFFF";
const DIVIDER = "555555";
const PORT_DARKRED = "8B0000";
// sigmoid glyph sidecar (600dpi, tight): 91x116 px
const SIGMOID = { w: 91 / 600, h: 116 / 600 };

const px = (v) => v / 72;

// ---- diagram constants (frame px) ----
const COL_CX = [160, 261.5, 426.5, 590, 676.5];
const ROW_CY = [211.5, 285.5, 366.5];
const NEURON_FILL = ["EDEDEB", "DCE9F5", "DCFFB5", "F7C99B", "EDEDEB"];
const NEURON_LINE = ["A08C74", "7780AA", "6B9944", "C08850", "A08C74"];
const RINGS_POST1 = [196, 211, 226];
const RINGS_PRE5 = [618, 633, 648];

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 24)
drawHouseChrome(pres, slide, { numeral: "24" });

// Black footer bar (over the panel; chrome bottom stroke kept visible — slide_023 precedent)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(527), w: px(883), h: px(10.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Beige network panel (borderless fill on the gray panel)
slide.addShape(pres.ShapeType.rect, {
  x: px(64), y: px(165), w: px(722), h: px(253),
  fill: { color: PANEL_BEIGE }, line: { color: PANEL_BEIGE, width: 0 },
});

// Title — bold red, ink x328..643 (center 485.5), cap y68..89 (baseline 89)
slide.addText("Neural Network Model", {
  x: px(485.5 - 320), y: px(89 - 32), w: px(640), h: 0.55,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 30.5, bold: true, color: TITLE_RED,
});

// Header strip: dashed magenta line y141 + left arrowhead + two magenta boxes
slide.addShape(pres.ShapeType.line, {
  x: px(140), y: px(141), w: px(680), h: 0,
  line: { color: MAG_DARK, width: 1.25, dashType: "dash" },
});
// left-pointing arrowhead INSIDE the Input Samples box right end (measured tip x118)
slide.addShape(pres.ShapeType.triangle, {
  x: px(129 - 8), y: px(141 - 11), w: px(16), h: px(22), rotate: 270,
  fill: { color: MAG_DARK }, line: { color: MAG_DARK, width: 0 },
});
// magenta boxes (2-line bold black text)
const MAG_BOXES = [
  { x: 64, y: 127, w: 76, h: 28, l1: "Input", l2: "Samples", bl: 141 },
  { x: 820, y: 125, w: 68, h: 29, l1: "Sample", l2: "Label", bl: 139 },
];
for (const b of MAG_BOXES) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
    fill: { color: MAG_FILL }, line: { color: MAG_LINE, width: 0.75 },
  });
  slide.addText(
    [
      { text: b.l1, options: { breakLine: true } },
      { text: b.l2, options: {} },
    ],
    {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 9, bold: true, color: BLACK, lineSpacing: 10.5,
    }
  );
}

// ---- input fan: 4 magenta dots -> 12 thin gray lines -> col1 left rims ----
const DOTS = [[78, 254], [78, 277.5], [78, 300.5], [78, 323.5]];
for (const [dx, dy] of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(dx - 4.5), y: px(dy - 4.5), w: px(9), h: px(9),
    fill: { color: DOT_MAG }, line: { color: DOT_MAG, width: 0 },
  });
  for (const cy of ROW_CY) {
    const up = dy > cy;
    slide.addShape(pres.ShapeType.line, {
      x: px(84), y: px(Math.min(dy, cy)), w: px(54), h: px(Math.abs(cy - dy)),
      flipV: up,
      line: { color: FAN_GRAY, width: 0.75 },
    });
  }
}

// ---- floating rings (no connecting lines — measured) ----
for (const cy of ROW_CY) {
  for (const rx of RINGS_POST1) {
    slide.addShape(pres.ShapeType.ellipse, {
      x: px(rx - 4.5), y: px(cy - 4.5), w: px(9), h: px(9),
      fill: { color: PANEL_BEIGE }, line: { color: "6B6863", width: 1 },
    });
  }
  for (const rx of RINGS_PRE5) {
    slide.addShape(pres.ShapeType.ellipse, {
      x: px(rx - 4.5), y: px(cy - 4.5), w: px(9), h: px(9),
      fill: { color: PANEL_BEIGE }, line: { color: "2E2A20", width: 1 },
    });
  }
}

// ---- red mesh col2->col3 and col3->col4 (9 lines each, arrowheads on target rims,
//      emitted from dark-red output ports at the source rims) ----
function rimPoint(cxFrom, cyFrom, cxTo, cyTo, rFrom, rTo) {
  const dx = cxTo - cxFrom, dy = cyTo - cyFrom;
  const len = Math.sqrt(dx * dx + dy * dy) || 1;
  return [cxFrom + (dx / len) * rFrom, cyFrom + (dy / len) * rFrom,
          cxTo - (dx / len) * (rTo + 1), cyTo - (dy / len) * (rTo + 1)];
}
const MESH = [[1, 2], [2, 3]]; // column index pairs
for (const [c0, c1] of MESH) {
  for (const cy0 of ROW_CY) {
    for (const cy1 of ROW_CY) {
      const [x0, y0, x1, y1] = rimPoint(COL_CX[c0], cy0, COL_CX[c1], cy1, 21, 21);
      slide.addShape(pres.ShapeType.line, {
        x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
        w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
        flipV: y1 < y0,
        line: { color: MESH_RED, width: 0.75, endArrowType: "triangle" },
      });
    }
  }
  // dark-red output ports at the source rims
  for (const cy0 of ROW_CY) {
    slide.addShape(pres.ShapeType.ellipse, {
      x: px(COL_CX[c0] + 17.5), y: px(cy0 - 4), w: px(7), h: px(8),
      fill: { color: PORT_DARKRED }, line: { color: PORT_DARKRED, width: 0 },
    });
  }
}

// ---- 15 neurons: circle + divider + red Sigma (left) + sigmoid glyph (right) ----
for (let c = 0; c < 5; c++) {
  for (const cy of ROW_CY) {
    const cx = COL_CX[c];
    slide.addShape(pres.ShapeType.ellipse, {
      x: px(cx - 20), y: px(cy - 20), w: px(40), h: px(40),
      fill: { color: NEURON_FILL[c] }, line: { color: NEURON_LINE[c], width: 1 },
    });
    slide.addShape(pres.ShapeType.line, {
      x: px(cx), y: px(cy - 20), w: 0, h: px(40),
      line: { color: DIVIDER, width: 0.75 },
    });
    slide.addText("\u03A3", {
      x: px(cx - 19), y: px(cy - 9), w: px(18), h: px(18),
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 13, bold: true, color: TITLE_RED,
    });
    slide.addImage({
      path: ASSETS + "/sigmoid_curve.png",
      x: px(cx + 1.5), y: px(cy - SIGMOID.h * 72 / 2), w: SIGMOID.w, h: SIGMOID.h,
    });
  }
}

// ---- Net labels (red italic + subscript) with small red arrows onto top neurons ----
const sub = (s) => [
  { text: "Net", options: { italic: true, subscript: false } },
  { text: s, options: { italic: true, subscript: true } },
];
const NETS = [
  { runs: sub("i"), left: 203, bl: 184, ax0: 234, ay0: 187, ax1: 249, ay1: 195 },
  { runs: sub("j"), left: 369, bl: 184, ax0: 400, ay0: 187, ax1: 415, ay1: 195 },
  { runs: sub("k"), left: 532, bl: 184, ax0: 563, ay0: 187, ax1: 588, ay1: 196 },
];
for (const n of NETS) {
  slide.addShape(pres.ShapeType.line, {
    x: px(n.ax0), y: px(Math.min(n.ay0, n.ay1)), w: px(n.ax1 - n.ax0), h: px(n.ay1 - n.ay0),
    flipV: n.ay1 < n.ay0,
    line: { color: MESH_RED, width: 1, endArrowType: "triangle" },
  });
  slide.addText(n.runs, {
    x: px(n.left - 1), y: px(n.bl - 14.5), w: px(34), h: 0.3,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 12.5, color: TITLE_RED, lineSpacing: 14,
  });
}

// ---- O activation labels (red italic + subscript, upper-right of each neuron) ----
const OLAB = [
  [280, 205, 2], [278, 274, 2], [275, 355, 2],
  [446, 205, 3], [444, 274, 3], [444, 355, 3],
  [610, 205, 4], [607, 274, 4], [607, 355, 4],
];
const osym = ["i", "j", "k"];
for (const [left, bl, c] of OLAB) {
  slide.addText(
    [
      { text: "O", options: { italic: true, subscript: false } },
      { text: osym[c - 2], options: { italic: true, subscript: true } },
    ],
    {
      x: px(left - 1), y: px(bl - 21), w: px(30), h: 0.42,
      align: "left", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 17, color: TITLE_RED, lineSpacing: 19,
    }
  );
}

// ---- blue weight labels: w_ji x3 (A-gap), w_kj x3 (B-gap), rotated to ride their lines ----
const WLAB = [
  [327, 205, "ji", 0], [321, 240, "ji", 30], [329, 276, "ji", 51],
  [488, 207, "kj", 0], [489, 243, "kj", 30], [490, 276, "kj", 51],
];
for (const [left, bl, s, rot] of WLAB) {
  slide.addText(
    [
      { text: "w", options: { italic: true, subscript: false } },
      { text: s, options: { italic: true, subscript: true } },
    ],
    {
      x: px(left - 1), y: px(bl - 13), w: px(26), h: 0.28,
      align: "left", valign: "middle", margin: 0, rotate: rot,
      fontFace: "Arial", fontSize: 12, color: W_BLUE, lineSpacing: 13,
    }
  );
}

// ---- output arrows col5 -> white Output boxes (black bold text) ----
const OUTBOX = [[723, 206, 58, 13, "Output 1"], [723, 278, 58, 13, "Output 2"], [723, 360, 58, 13, "Output m"]];
for (let r = 0; r < 3; r++) {
  const [bx, by, bw, bh, label] = OUTBOX[r];
  const cy = ROW_CY[r];
  slide.addShape(pres.ShapeType.line, {
    x: px(COL_CX[4] + 21), y: px(cy), w: px(bx - 3 - COL_CX[4] - 21), h: 0,
    line: { color: MESH_RED, width: 1, endArrowType: "triangle" },
  });
  slide.addShape(pres.ShapeType.rect, {
    x: px(bx), y: px(by), w: px(bw), h: px(bh),
    fill: { color: OUTBOX_FILL }, line: { color: "9080C8", width: 1 },
  });
  slide.addText(label, {
    x: px(bx), y: px(by), w: px(bw), h: px(bh),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 10.5, bold: true, italic: true, color: BLACK,
  });
}

// ---- Error bar (dark red) with 3 rotated bright-red Error labels ----
slide.addShape(pres.ShapeType.rect, {
  x: px(797), y: px(180), w: px(21), h: px(213),
  fill: { color: ERR_FILL }, line: { color: ERR_FILL, width: 0 },
});
for (const cy of ROW_CY) {
  slide.addText("Error", {
    x: px(807.5 - 30), y: px(cy - 8), w: px(60), h: px(16), rotate: 270,
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 12, bold: true, color: ERR_TEXT,
  });
}

// ---- Class boxes (light green, black 9pt) ----
const CLASSBX = [[825, 202, 66, 19, "Class 1"], [825, 275, 66, 18, "Class 2"], [825, 357, 66, 17, "Class m"]];
for (const [bx, by, bw, bh, label] of CLASSBX) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(bx), y: px(by), w: px(bw), h: px(bh),
    fill: { color: CLASS_FILL }, line: { color: CLASS_FILL, width: 0 },
  });
  slide.addText(label, {
    x: px(bx), y: px(by), w: px(bw), h: px(bh),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 9, color: BLACK,
  });
}

// ---- bottom strip: block arrows (head triangle + stem rect, black letter in stem) ----
const ARROWS = [
  [240, 384, "D9E2F3", "8FA3CF", "i"],
  [405, 384, "C9E3A8", "7FA85E", "j"],
  [565, 384, "F2CC9D", "C08040", "k"],
];
for (const [ax, ay, fill, outline, letter] of ARROWS) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(ax + 16.5), y: px(ay + 24), w: px(16), h: px(20),
    fill: { color: fill }, line: { color: outline, width: 1 },
  });
  slide.addShape(pres.ShapeType.triangle, {
    x: px(ax), y: px(ay), w: px(49), h: px(26),
    fill: { color: fill }, line: { color: outline, width: 1 },
  });
  slide.addText(letter, {
    x: px(ax + 16.5 - 6), y: px(ay + 24), w: px(28), h: px(20),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 10, color: BLACK,
  });
}

// ---- callout boxes (2-line, thin colored borders) ----
const CALLOUTS = [
  [220, 428, 87, 33, "DEEBF3", "8E96BC", "Previous Layer", "Layer (i)"],
  [384, 428, 87, 33, "DDFFB8", "7FA85E", "Current Layer", "(You are here)"],
  [558, 430, 69, 29, "F2CC9D", "C08040", "Next Layer", "Layer (K)"],
];
for (const [bx, by, bw, bh, fill, line, l1, l2] of CALLOUTS) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(bx), y: px(by), w: px(bw), h: px(bh),
    fill: { color: fill }, line: { color: line, width: 0.75 },
  });
  slide.addText(
    [
      { text: l1, options: { breakLine: true } },
      { text: l2, options: {} },
    ],
    {
      x: px(bx), y: px(by), w: px(bw), h: px(bh),
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 8.5, color: BLACK, lineSpacing: 11,
    }
  );
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
