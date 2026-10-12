// slide_031.js — "Self Attention Mechanism (Linear Transformation of Inputs)"
// Deep Learning DSAI 308, Transformers — Part I. Build worker attempt 1, 2026-10-12.
//
// FRAME-TRUE build: all geometry PIL-measured from unique_slides/slide_031.jpg
// (960x540, 1px = 1pt = 1/72 in) — scratch/slide031/ measure_mine1..5.py, plus the
// predecessor's measure1..12.py and the gated crop reads banked in scratch/slide031/crops/
// (read_qout6x/vout6x/kout6x.txt, read_callouts6x.txt, read_qincap/qoutcap/vpanel/kpanel/
// boxes/callouts.txt). HOUSE CHROME via components/house_chrome.js (playlist law) —
// badge numeral 31 = the number printed on the frame.
//
// FRAME-VS-SPEC corrections (frame is ground truth; spec deviations documented):
//   1. Matrix W-cell text is color-coded BY ROW (blue/magenta/orange/green) in ALL
//      three panels (measure8 cores + 3 crop reads) — NOT red/blue/green per panel.
//   2. Output-capsule outlines are DARK RED/crimson in all three panels (6x reads),
//      not per-panel colored; fills rose/lavender/mint per panel.
//   3. Output-capsule tile labels read X_Q21..X_Q24 / X_V21..X_V24 / X_K21..X_K24:
//      large dark X + subscript = RED role letter + dark digits (3 independent gated
//      6x reads; matches slide 032's frame-validated convention; the spec's
//      "x21..x24" was carried as an unresolved [?] flagged for build-time re-check —
//      re-check done, role-lettered labels confirmed).
//   4. Input capsules: pink pill + dark-red [ ] brackets + four circles (lavender-gray
//      fill, dark-red outline) holding x21..x24 — not "pink squares".
//   5. Callout 1 border is dashed GREEN (perimeter-band scan: green dashes; the spec
//      was right; the "red" hypothesis came from the Q-panel corner inside the window).
//      Callout fills are TINTED (pink / periwinkle / mint), not white.
//   6. Subtitle keywords Query/Keys/Values AND X2 are red (no blue ink anywhere in
//      the subtitle band; red x-clusters at 115-171, 238-256, 305-351, 764-826).
//   7. "1xd" sits at the pill's right end, "X2" below-left — both dark red/maroon;
//      "dxd" dark red-brown at the matrix bottom-right; "=" is dark red-maroon.
//   8. Emphasis element = white box + run-level yellow highlight behind
//      "Generate Three Variants" and "of X2" only (read_boxes; yellow n=4228 in a
//      237x50 window is NOT a solid fill).
//   9. Role letters Q/V/K sit above the output capsules (Q/V on the gray/peach seam,
//      K overlapping the K panel's top border), colored red/blue-violet/green.
//  10. Peach canvas F7E2CD x46..901 y92..536 on the chrome gray panel; title and
//      subtitle sit on the gray above it.
//  11. Mouse-cursor artifact (bottom-right of the W_Q matrix / dxd area) OMITTED
//      (spec recreation_brief step 26; GROUND RULES (c)).

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);

const px = (v) => v / 72; // frame px -> inches (1 frame px = 1 pt)
const FONT = "Arial";

// ---- palette (frame-measured cores, JPEG-softened) ------------------------------
const C = {
  peach: "F7E2CD",
  panelQ: "A03038", panelV: "2E2390", panelK: "4E8B58",
  pillFill: "FFD0F6", pillLine: "B060A8",
  circFill: "D8D4EC",
  labelRed: "9E1B28",            // X2 / W_x / 1xd / brackets
  dxd: "6B3A1A",                 // dimension label at matrix bottom-right
  eqRed: "A02030",               // the big '='
  roleQ: "A03038", roleV: "3A2E96", roleK: "5E9066",
  outcapLine: "9E2B3E",          // dark-red outline on ALL three output capsules
  outQ: "F0C4C4", outV: "BCBCF2", outK: "C9F0D8",
  matQ: "F2C7CA", matV: "BCBCF2", matK: "C9F0D8",
  chip: "F5F0BE", chipLine: "8A7A50",
  wRow1: "1A2A8C", wRow2: "8B1A6E", wRow3: "A05010", wRow4: "1E7A1E",
  cellInk: "303030", subRed: "B02030",
  callGreen: "3E8B50", callBlue: "2E2390",
  callFill1: "F2C8D4", callFill2: "BCBCF2", callFill3: "DFF2E4",
  navy: "1F2470", noteRed: "A01515",
  boxLine: "C8C0CC",
};

// ---- measured geometry (frame px) ------------------------------------------------
// matrix chip grid centers (measured pale-yellow runs)
const QCOLS = [235.5, 274, 312.5, 351];
const QROWS = [135.5, 175.5, 220.5, 260];
const WROWCOLORS = [C.wRow1, C.wRow2, C.wRow3, C.wRow4];

// one 4x4 weight matrix: container + panel-tinted grid lines + 16 chips + row-coded W labels
function drawMatrix(pptx, slide, ox, oy, fill, gridColor) {
  const H = oy === 112 ? 179 : 176;
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(ox), y: px(oy), w: px(157), h: px(H),
    rectRadius: 0.1, fill: { color: fill }, line: { type: "none" },
  });
  const cols = QCOLS.map((v) => v + ox - 218);
  const rows = QROWS.map((v) => v + oy - 112);
  // internal grid lines (frame-measured: panel-tinted, ~2px)
  for (let i = 1; i < 4; i++) {
    slide.addShape(pptx.ShapeType.line, {
      x: px((cols[i - 1] + cols[i]) / 2), y: px(oy + 4), w: 0, h: px(H - 8),
      line: { color: gridColor, width: 1 },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: px(ox + 4), y: px((rows[i - 1] + rows[i]) / 2), w: px(149), h: 0,
      line: { color: gridColor, width: 1 },
    });
  }
  for (let r = 0; r < 4; r++) {
    for (let cIdx = 0; cIdx < 4; cIdx++) {
      const cx = cols[cIdx], cy = rows[r];
      slide.addShape(pptx.ShapeType.rect, {
        x: px(cx - 13), y: px(cy - 10), w: px(26), h: px(20),
        fill: { color: C.chip }, line: { color: C.chipLine, width: 0.5 },
      });
      slide.addText(
        [
          { text: "W", options: {} },
          { text: `${cIdx + 1}${r + 1}`, options: { subscript: true } },
        ],
        {
          x: px(cx - 15), y: px(cy - 10), w: px(30), h: px(20),
          align: "center", valign: "middle", margin: 0, wrap: false,
          fontFace: FONT, fontSize: 9, bold: true, color: WROWCOLORS[r],
        }
      );
    }
  }
}

// one input capsule: pink pill + [ ] + 4 circles with x2n labels
function drawInputPill(pptx, slide, ox, oy) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(ox), y: px(oy), w: px(138), h: px(36), rectRadius: 0.25,
    fill: { color: C.pillFill }, line: { color: C.pillLine, width: 1 },
  });
  const cy = oy + 18;
  slide.addText("[", {
    x: px(ox + 2), y: px(cy - 13), w: px(10), h: px(26),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 15, bold: true, color: C.labelRed,
  });
  slide.addText("]", {
    x: px(ox + 126), y: px(cy - 13), w: px(10), h: px(26),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 15, bold: true, color: C.labelRed,
  });
  for (let i = 0; i < 4; i++) {
    const cx = ox + 24 + i * 31; // circle centers 98/129/160/191 (Q frame coords)
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(cx - 13), y: px(cy - 13), w: px(26), h: px(26),
      fill: { color: C.circFill }, line: { color: C.panelQ, width: 1.25 },
    });
    slide.addText(
      [
        { text: "x", options: { italic: true } },
        { text: `2${i + 1}`, options: { subscript: true } },
      ],
      {
        x: px(cx - 14), y: px(cy - 10), w: px(28), h: px(20),
        align: "center", valign: "middle", margin: 0, wrap: false,
        fontFace: FONT, fontSize: 10, bold: true, color: C.cellInk,
      }
    );
  }
}

// labels under the input pill: big X2 (left) + small 1xd (right)
// frame-measured offsets from the pill origin: X2 center rel (+54.5,+62.5), 1xd rel (+96,+31)
function drawPillLabels(pptx, slide, ox, oy) {
  slide.addText(
    [
      { text: "X", options: {} },
      { text: "2", options: { subscript: true } },
    ],
    {
      x: px(ox + 31), y: px(oy + 42), w: px(46), h: px(40),
      align: "center", valign: "middle", margin: 0, wrap: false,
      fontFace: FONT, fontSize: 24, bold: true, italic: true, color: C.labelRed,
    }
  );
  slide.addText("1xd", {
    x: px(ox + 96), y: px(oy + 31), w: px(36), h: px(16),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 13, bold: true, color: C.labelRed,
  });
}

// one output capsule: dark-red-outlined pill + 4 pale-yellow tiles with
// X + red role letter + digits subscripts
function drawOutcap(pptx, slide, ox, oy, w, h, fill, role, digits) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(ox), y: px(oy), w: px(w), h: px(h), rectRadius: 0.22,
    fill: { color: fill }, line: { color: C.outcapLine, width: 1.75 },
  });
  const tileH = 27, gap = (h - 14 - 4 * tileH) / 3;
  for (let i = 0; i < 4; i++) {
    const ty = oy + 7 + i * (tileH + gap);
    slide.addShape(pptx.ShapeType.rect, {
      x: px(ox + 3), y: px(ty), w: px(w - 9), h: px(tileH),
      fill: { color: C.chip }, line: { color: C.chipLine, width: 0.75 },
    });
    slide.addText(
      [
        { text: "X", options: { fontSize: 11 } },
        { text: role, options: { subscript: true, fontSize: 6.5, color: C.subRed } },
        { text: digits[i], options: { subscript: true, fontSize: 6.5 } },
      ],
      {
        x: px(ox + 3), y: px(ty), w: px(w - 9), h: px(tileH),
        align: "center", valign: "middle", margin: 0, wrap: false,
        fontFace: FONT, bold: true, color: C.cellInk,
      }
    );
  }
}

// role letter near an output capsule (frame-measured spots; regular weight)
function drawRoleLetter(pptx, slide, x, y, letter, color) {
  slide.addText(letter, {
    x: px(x), y: px(y), w: px(28), h: px(26),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 22, color,
  });
}

// W_Q / W_V / W_K label left of the matrix bottom row (frame: x182..211, y236..265)
function drawWLabel(pptx, slide, x, y, sub) {
  slide.addText(
    [
      { text: "W", options: {} },
      { text: sub, options: { subscript: true } },
    ],
    {
      x: px(x), y: px(y), w: px(56), h: px(40),
      align: "center", valign: "middle", margin: 0, wrap: false,
      fontFace: FONT, fontSize: 20, bold: true, italic: true, color: C.labelRed,
    }
  );
}

// dxd dimension label at the matrix bottom-right
function drawDxd(pptx, slide, x, y) {
  slide.addText("dxd", {
    x: px(x), y: px(y), w: px(40), h: px(18),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 11, bold: true, color: C.dxd,
  });
}

// the big '=' between matrix and output capsule
function drawEquals(pptx, slide, x, y) {
  slide.addText("=", {
    x: px(x), y: px(y), w: px(26), h: px(22),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 16, bold: true, color: C.eqRed,
  });
}

// dashed callout pill with mixed-style text
function drawCallout(pptx, slide, x, y, w, h, borderColor, fill, tail) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(x), y: px(y), w: px(w), h: px(h), rectRadius: 0.18,
    fill: { color: fill },
    line: { color: borderColor, width: 1.5, dashType: "dash" },
  });
  slide.addText(
    [
      { text: "X", options: { italic: true, color: C.labelRed } },
      { text: "2", options: { subscript: true, color: C.labelRed } },
      { text: " variant ", options: { italic: true, color: C.labelRed } },
      { text: tail, options: { italic: true, bold: true, color: C.navy, underline: true } },
    ],
    {
      x: px(x + 4), y: px(y), w: px(w - 8), h: px(h),
      align: "center", valign: "middle", margin: 0, wrap: false,
      fontFace: FONT, fontSize: 13,
    }
  );
}

// one full role panel (Q/V/K) at its measured frame position
// (NO role letters above the output capsules — judge attempt 1 + six gated crop reads
// confirm the original has none; the earlier "role letter" PIL blobs were the outcap
// fill/cap AA. drawRoleLetter kept for reference but not called.)
function drawRolePanel(pptx, slide, p) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(p.x), y: px(p.y), w: px(p.w), h: px(p.h), rectRadius: 0.1,
    fill: { color: "FFFFFF" }, line: { color: p.border, width: 2 },
  });
  drawInputPill(pptx, slide, p.pillX, p.pillY);
  drawPillLabels(pptx, slide, p.pillX, p.pillY);
  drawMatrix(pptx, slide, p.matX, p.matY, p.matFill, p.gridColor);
  drawWLabel(pptx, slide, p.wX, p.wY, p.wSub);
  drawDxd(pptx, slide, p.dxdX, p.dxdY);
  drawEquals(pptx, slide, p.eqX, p.eqY);
  drawOutcap(pptx, slide, p.outX, p.outY, p.outW, p.outH, p.outFill, p.role, p.digits);
}

// ---- build -----------------------------------------------------------------------

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pres.addSlide();

drawHouseChrome(pres, slide, { numeral: 31 });

// peach canvas on the chrome panel
slide.addShape(pres.ShapeType.roundRect, {
  x: px(46), y: px(92), w: px(855), h: px(444), rectRadius: 0.14,
  fill: { color: C.peach }, line: { type: "none" },
});

// title: black + yellow-highlighted parenthetical (ink x186..747, y50..68)
slide.addText(
  [
    { text: "Self Attention Mechanism ", options: { color: "000000" } },
    { text: "(Linear Transformation of Inputs)", options: { color: "1B1878", highlight: "FFFF00" } },
  ],
  {
    x: px(66), y: px(44), w: px(800), h: px(28),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 20, bold: true,
  }
);

// subtitle: red keywords on black bold text (ink y72..92; frame width x108..826)
slide.addText(
  [
    { text: "(", options: { color: "000000" } },
    { text: "Query", options: { color: C.labelRed } },
    { text: " using ", options: { color: "000000" } },
    { text: "X", options: { color: C.labelRed } },
    { text: "2", options: { subscript: true, color: C.labelRed } },
    { text: " All ", options: { color: "000000" } },
    { text: "Keys", options: { color: C.labelRed } },
    { text: " in Dictionary and retrieve Corresponding ", options: { color: "000000" } },
    { text: "Values", options: { color: C.labelRed } },
  ],
  {
    x: px(100), y: px(70), w: px(770), h: px(24),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 19, bold: true, charSpacing: 0.8,
  }
);

// three role panels (frame-measured)
drawRolePanel(pres, slide, {
  name: "Q", x: 56, y: 97, w: 411, h: 203, border: C.panelQ,
  pillX: 74, pillY: 136,
  matX: 218, matY: 112, matFill: C.matQ, gridColor: "D3AFB9",
  wX: 170, wY: 230, wSub: "Q",
  dxdX: 334, dxdY: 276,
  eqX: 382, eqY: 192,
  outX: 411, outY: 117, outW: 42, outH: 172, outFill: C.outQ,
  role: "Q", digits: ["21", "22", "23", "24"],
  roleX: 437, roleY: 96, roleColor: C.roleQ,
});
drawRolePanel(pres, slide, {
  name: "V", x: 479, y: 98, w: 409, h: 201, border: C.panelV,
  pillX: 492, pillY: 136,
  matX: 635, matY: 112, matFill: C.matV, gridColor: "8A94C9",
  wX: 587, wY: 230, wSub: "V",
  dxdX: 752, dxdY: 276,
  eqX: 800, eqY: 192,
  outX: 826, outY: 116, outW: 46, outH: 173, outFill: C.outV,
  role: "V", digits: ["21", "22", "23", "24"],
  roleX: 836, roleY: 114, roleColor: C.roleV,
});
drawRolePanel(pres, slide, {
  name: "K", x: 58, y: 311, w: 410, h: 218, border: C.panelK,
  pillX: 76, pillY: 352,
  matX: 221, matY: 330, matFill: C.matK, gridColor: "9CCBAF",
  wX: 173, wY: 444, wSub: "K",
  dxdX: 332, dxdY: 486,
  eqX: 385, eqY: 410,
  outX: 413, outY: 332, outW: 44, outH: 173, outFill: C.outK,
  role: "K", digits: ["21", "22", "23", "24"],
  roleX: 446, roleY: 308, roleColor: C.roleK,
});

// three dashed callouts (green / blue / green; tinted fills)
// c2 (690,300,196) and c3 (461,332,220) per judge attempt 1 + fill/border scans:
// c3 must start clear of the K output capsule (right edge x456); c2 sits x686..886.
drawCallout(pres, slide, 445, 272, 235, 42, C.callGreen, C.callFill1, "to QUERY with");
drawCallout(pres, slide, 690, 300, 196, 41, C.callBlue, C.callFill2, "used as Value");
drawCallout(pres, slide, 461, 332, 220, 42, C.callGreen, C.callFill3, "used as KEY");

// emphasis box: white box + yellow highlight behind line 1 and "of X2"
slide.addShape(pres.ShapeType.roundRect, {
  x: px(632), y: px(383), w: px(262), h: px(55), rectRadius: 0.08,
  fill: { color: "FFFFFF" }, line: { type: "none" },
});
slide.addText(
  [
    { text: "Generate Three Variants", options: { highlight: "FFFF00", breakLine: true } },
    { text: "of ", options: { highlight: "FFFF00" } },
    { text: "X", options: { highlight: "FFFF00" } },
    { text: "2", options: { subscript: true, highlight: "FFFF00" } },
    { text: " (Based on its Role)", options: {} },
  ],
  {
    x: px(632), y: px(383), w: px(262), h: px(55),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 20, bold: true, italic: true,
    color: C.noteRed, lineSpacing: 21,
  }
);

// note box: white, thin border; W-terms RED bold (frame), rest navy blue
slide.addShape(pres.ShapeType.rect, {
  x: px(491), y: px(448), w: px(412), h: px(71),
  fill: { color: "FFFFFF" }, line: { color: C.boxLine, width: 0.75 },
});
slide.addText(
  [
    { text: "W", options: { bold: true, color: C.subRed } },
    { text: "Q", options: { subscript: true, bold: true, color: C.subRed } },
    { text: "  W", options: { bold: true, color: C.subRed } },
    { text: "K", options: { subscript: true, bold: true, color: C.subRed } },
    { text: "  W", options: { bold: true, color: C.subRed } },
    { text: "V", options: { subscript: true, bold: true, color: C.subRed } },
    { text: "       are    controllable    parameters", options: { color: C.navy, breakLine: true } },
    { text: "(Trainable),", options: { bold: true, color: C.subRed } },
    { text: "   allows   to   modify   the   incoming", options: { color: C.navy, breakLine: true } },
    { text: "vectors to suit the three roles they must play", options: { color: C.navy } },
  ],
  {
    x: px(497), y: px(451), w: px(400), h: px(65),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 16, lineSpacing: 21,
  }
);

// ---- output (SINGLE-VERSION law: one plain-named deliverable) --------------------
const OUT = path.join(__dirname, "..", "slide_031_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
