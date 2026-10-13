// components/slide_047.js — slide 047 "Encoder Block" composition
// (002_transformers_part2, Deep Learning DSAI 308).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slide 47 is a CHILD of slide 046
// (47<-46; 46 certified PASS in this video's DB) and the PARENT of slides 48<-47 and
// 57<-47. Children MUST require() this module and call renderBase(pptx, slide, opts) —
// never re-derive this geometry.
//
// COMPOSITION PROVENANCE (resume of the 2026-10-12 19:16 worker; all geometry from the
// banked measurement campaign in scratch/slide047/ — m13c chrome fit, m14 census,
// m15/m17 cell census, m19 targets, gapfill1/2, vision_montage_3 / vision_labels /
// vision_texts / vision_details / vision_zoom_2):
//  * m18_ffdiff.py: frames 046 vs 047 share ONLY the outer margins (cols 0-56/903-959,
//    rows 0-46/518-539) — the diagram is fully re-styled vs 046, so this component does
//    NOT call 046's block functions; it forks the 045/046 strip/unit MECHANISMS with THIS
//    frame's measured colors/geometry (the 046<-045 precedent).
//  * Chrome: m13c_final_fit = the certified 045 mapping (SX=.962329 OX=17.582 SY=.955556)
//    → shared house_chrome.js; badge re-drawn last from CHROME constants (numeral 47;
//    frame badge center is a curation artifact — m13c note).
//  * Structure (bottom→top): X row → MHA plum bar → rowC → dashed u2 [discs cy 380.4 +
//    LN2 bar 326.5] → rowB → FFN box (9 slots, slot 7 empty) → rowA → dashed u1
//    [discs cy 158.5 + LN1 bar 105.7] → output row. Residual curves rise from the
//    residual-source row (u1: rowB behind FFN; u2: X row behind MHA) — 045/046 law.
//  * Labels 0-BASED (Y_0..Y_5, N-2, N-1; X same) — vision-confirmed (vision_labels.txt,
//    "no tildes or prime marks"), same finding as 046's SUBS_46.
//  * Strips: 8 vector strips/row, each 6 pale sub-cells (output/X rows) or 6 warm
//    sub-cells (internal rows on tan), red label centered (Z7/Z8: label cell reads
//    orange because of the orange-red label ink).
//  * Arrows: block arrows (assets s047_blkarrow_A/B from m21_assets.py) in 4 gaps;
//    thin purple row→disc, olive disc→LN-bar, u1 LN→output RED, u2 LN→rowB olive
//    (gapfill2 F: 8 olive clusters LN2→rowB; m19 C: red rows 76..101).
//  * Output row carries a bright-yellow 2-cell block at its clipped right end
//    (m17 far-right scan; frame x 864..896).
//
// opts: { numeral: 47 (default), chrome: true }
// Block granularity for children (48, 57): drawContainer47, drawDashedGroup47,
// drawLNBar47, drawCurves47, drawStripRow47, drawFFN47, drawMHABar47, drawBlockArrows47,
// drawThinArrows47, drawDiscs47, drawIOBox47, drawTitleVertical47, drawRedOutArrows47,
// drawBadge47, COLS, ROWS, U1, U2 — all exported.

const chromeMod = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const CHROME = chromeMod.CHROME;

const pt = (v) => v / 72;
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";
const FONT = "Arial";

// ---- measured palette (frame medians; m14/m15/m19/gapfill1-2) ----
const TAN = "E9B172";          // container/group/FFN fill (#E6B671..#EBB074)
const TAN_LINE = "9E5E1E";     // container border (#9A6231/#A85F1A)
const DASH = "9A8434";         // dashed group border (#A98634 olive-khaki)
const LN_FILL = "EDB671";      // LN bar fill (tan bevel)
const LN_LINE = "B08040";      // LN bar border (#B88745)
const LAYER_C = "DC7D45";      // "Layer" coral orange ([220,125,69])
const NORM_C = "81460E";       // "Normalization" dark brown ([129,70,14])
const PLUM = "854659";         // MHA bar fill ([133,70,89])
const PLUM_TEXT = "F2B7A0";    // MHA bar text ([242,183,160])
const FFN_LINE = "8A4A3C";     // FFN box border (#874C3C/#9F5F44)
const HDR_C = "6E3444";        // FFN header ink (m15 #90564A darkest-decile)
const TILE_FILL = "CFA05C";    // FFN tile fill ([211,161,88]/#CC9C5A)
const TILE_LINE = "C8763A";    // FFN tile border
const GREEN_DOT = "82932A";    // tile green dots (#8E9424 olive)
const PINK_DOT = "F2AE8E";     // tile pink dots ([242,173,127] salmon)
const FAN = "705A28";          // tile fan lines (dark brown/olive)
const RELU_C = "C05A20";       // RELU label (orange-red)
const DISC = "B44414";         // plus-disc fill (core #B43C0C..#CA602D)
const PURPLE = "6B3050";       // thin row→disc arrows (zoom: dark purple)
const OLIVE = "83860F";        // thin disc→bar + LN2→rowB arrows (#85880E)
const RED_OUT = "A01020";      // LN1→output arrows (#A10B1C)
const IO_LINE = "8E2E31";      // Block Output/Input boxes (#903033)
const IO_FILL = "FFF4F0";      // IO box fill (near-white pink-tinged)
const TITLE_C = "9A1626";      // vertical title ink (#9B1728 median)
const YELLOW_BLK = "FEFF9C";   // output-row clipped end block (#FDFF9C)
const YBLK_LINE = "8A7A30";

// ---- measured geometry (slide pt) ----
const COLS = [195.3, 270.8, 347.0, 423.0, 498.5, 574.5, 772.3, 846.9];
const STRIP = { halfW: 35.7, cells: 6 };
const DOTS = { x: [631.1, 649.3, 667.4, 685.6, 703.7], d: 7 };

const ROWS = {
  out: { y: 60.7, h: 17.8, dotColor: "04048C" },
  A: { y: 178.8, h: 17.8, dotColor: "773B42" },
  B: { y: 293.8, h: 17.8, dotColor: "773B42" },
  C: { y: 400.6, h: 17.8, dotColor: "773B42" },
  x: { y: 515.9, h: 16.8, dotColor: "00E87A" },
};

const CELL_PALE = ["FDFDD0", "F2FFDE", "FAFFF2", "EDEDF8", "F6DFF5", "E9E8EC"];
const CELL_WARM = ["DFA05C", "E6A862", "EEB26E", "F4BC7A", "E2A25E", "D89854"];
const LINE_PALE = "A8A898";
const LINE_WARM = "A56A30";
const SUBS = ["0", "1", "2", "3", "4", "5", "N-2", "N-1"];

const CONTAINER = { x: 112.1, y: 91.0, w: 804.0, h: 408.0, lineW: 2.25 };
const U1 = { // top dashed group: rowA -> discs -> LN1 -> output row
  box: { x: 148.0, y: 100.5, w: 752.0, h: 72.7 },
  ln: { x: 159.4, y: 105.7, w: 723.0, h: 31.4, textCx: 515.5 },
  discCy: 158.5, discD: 23.0,
  curves: { y: 152.25, h: 150.0 },
  arrows: {
    purple: { y0: 170.5, y1: 178.0 },   // rowA top -> disc bottom (head up at y0)
    olive: { y0: 138.0, y1: 146.5 },    // disc top -> LN1 bottom
    out: { y0: 80.0, y1: 105.0 },       // LN1 top -> output row (RED)
  },
};
const U2 = { // bottom dashed group: rowC -> discs -> LN2 -> rowB
  box: { x: 148.0, y: 316.0, w: 752.0, h: 80.1 },
  ln: { x: 159.4, y: 326.5, w: 723.0, h: 31.4, textCx: 515.5 },
  discCy: 380.4, discD: 23.0,
  curves: { y: 374.15, h: 150.0 },
  arrows: {
    purple: { y0: 392.5, y1: 400.0 },
    olive: { y0: 358.5, y1: 368.0 },
    out: { y0: 313.0, y1: 326.0 },      // LN2 top -> rowB (olive)
  },
};
const MHA = { x: 154.2, y: 434.3, w: 746.0, h: 58.6, textCx: 526.8 };
const FFN = {
  box: { x: 152.5, y: 214.5, w: 747.6, h: 62.8 },
  header: { text: "Feed Forward Networks [ One Hidden with  RELU Activation]", cx: 527.0, capTop: 220.9, size: 17 },
  tile: { w: 76.0, y: 239.5, h: 30.5, pitch: 81.5, firstCx: 196.1, skipSlot: 6,
          greenD: 5.5, greenCy: 248.0, greenPitch: 7.5,
          pinkD: 5.5, pinkCy: 261.0, pinkPitch: 9.4,
          relu: { size: 7, y: 243.0 } },
};
const BLK = {
  A: { w: 16.0, h: 20.0, y: 496.0 },                    // X -> MHA
  B: { w: 15.0, h: 14.5, mhaRowC: 419.5, ffnRowA: 198.5, rowBFFN: 278.5 },
};
const IO = {
  out: { x: 40.0, y: 54.0, w: 142.0, h: 40.0, text: "Block Output" },
  inp: { x: 40.0, y: 492.0, w: 142.0, h: 46.0, text: "Block Input" },
};
const TITLE = { text: "Encoder Block", cx: 83.5, cy: 283.1, size: 26, charSpacing: 11, boxW: 360, boxH: 44 };
const YBLK = { x: 881.0, y: 60.7, w: 26.0, h: 17.8 };

function lead(size) { return 0.273 * size; }

// ---- vector strip row (045/046 mechanism, THIS frame's 6-cell warm/pale variants) ----
function drawStripRow47(pptx, slide, row, letter, palette, lineColor, labelColor, subColor) {
  const cellW = (STRIP.halfW * 2) / STRIP.cells;
  for (let i = 0; i < 8; i++) {
    const cx = COLS[i];
    const bx = cx - STRIP.halfW;
    for (let c = 0; c < STRIP.cells; c++) {
      slide.addShape(pptx.ShapeType.rect, {
        x: pt(bx + c * cellW), y: pt(row.y), w: pt(cellW), h: pt(row.h),
        fill: { color: palette[c] }, line: { color: lineColor, width: 0.75 },
      });
    }
    slide.addText(
      [
        { text: letter, options: { color: labelColor } },
        { text: SUBS[i], options: { subscript: true, color: subColor } },
      ],
      {
        x: pt(cx - 13), y: pt(row.y - 1.5), w: pt(26), h: pt(row.h + 3),
        align: "center", valign: "middle", margin: 0,
        fontFace: FONT, fontSize: 14, bold: true, italic: true, lineSpacing: 14,
      }
    );
  }
  const dotCy = row.y + row.h / 2;
  for (const dx of DOTS.x) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: pt(dx - DOTS.d / 2), y: pt(dotCy - DOTS.d / 2),
      w: pt(DOTS.d), h: pt(DOTS.d), fill: { color: row.dotColor },
    });
  }
}

// ---- dashed group + LN bar + per-unit arrows/discs ----
function drawDashedGroup47(pptx, slide, u) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(u.box.x), y: pt(u.box.y), w: pt(u.box.w), h: pt(u.box.h),
    fill: { color: TAN }, line: { color: DASH, width: 1.5, dashType: "dashDot" },
    rectRadius: 0.08,
  });
}

function drawLNBar47(pptx, slide, u) {
  const b = u.ln;
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(b.x), y: pt(b.y), w: pt(b.w), h: pt(b.h),
    fill: { color: LN_FILL }, line: { color: LN_LINE, width: 1.25 },
  });
  slide.addText(
    [
      { text: "Layer", options: { color: LAYER_C } },
      { text: " Normalization", options: { color: NORM_C } },
    ],
    {
      x: pt(b.textCx - 220), y: pt(b.y), w: pt(440), h: pt(b.h),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 19, bold: true, italic: true, lineSpacing: 22,
    }
  );
}

function drawCurves47(pptx, slide, u) {
  for (const cx of COLS) {
    slide.addImage({
      path: ASSETS + "s047_curve.png",
      x: pt(cx - 52), y: pt(u.curves.y), w: pt(54), h: pt(u.curves.h),
    });
  }
}

function drawThinArrows47(pptx, slide, u, outColor) {
  for (const cx of COLS) {
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(u.arrows.purple.y0), w: 0,
      h: pt(u.arrows.purple.y1 - u.arrows.purple.y0),
      line: { color: PURPLE, width: 1.5, beginArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(u.arrows.olive.y0), w: 0,
      h: pt(u.arrows.olive.y1 - u.arrows.olive.y0),
      line: { color: OLIVE, width: 1.75, beginArrowType: "triangle" },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(u.arrows.out.y0), w: 0,
      h: pt(u.arrows.out.y1 - u.arrows.out.y0),
      line: { color: outColor, width: 1.75, beginArrowType: "triangle" },
    });
  }
}

function drawDiscs47(pptx, slide, u) {
  for (const cx of COLS) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: pt(cx - u.discD / 2), y: pt(u.discCy - u.discD / 2),
      w: pt(u.discD), h: pt(u.discD), fill: { color: DISC },
    });
    slide.addText("+", {
      x: pt(cx - u.discD / 2), y: pt(u.discCy - u.discD / 2),
      w: pt(u.discD), h: pt(u.discD),
      align: "center", valign: "middle", margin: 0,
      fontFace: FONT, fontSize: 14, bold: true, color: "FFFFFF",
    });
  }
}

// ---- block arrows (assets from m21_assets.py) ----
function drawBlockArrows47(pptx, slide) {
  for (const cx of COLS) {
    slide.addImage({ path: ASSETS + "s047_blkarrow_A.png",
      x: pt(cx - BLK.A.w / 2), y: pt(BLK.A.y), w: pt(BLK.A.w), h: pt(BLK.A.h) });
    slide.addImage({ path: ASSETS + "s047_blkarrow_B.png",
      x: pt(cx - BLK.B.w / 2), y: pt(BLK.B.mhaRowC), w: pt(BLK.B.w), h: pt(BLK.B.h) });
    slide.addImage({ path: ASSETS + "s047_blkarrow_B.png",
      x: pt(cx - BLK.B.w / 2), y: pt(BLK.B.ffnRowA), w: pt(BLK.B.w), h: pt(BLK.B.h) });
    slide.addImage({ path: ASSETS + "s047_blkarrow_B.png",
      x: pt(cx - BLK.B.w / 2), y: pt(BLK.B.rowBFFN), w: pt(BLK.B.w), h: pt(BLK.B.h) });
  }
}

// ---- big blocks ----
function drawContainer47(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(CONTAINER.x), y: pt(CONTAINER.y), w: pt(CONTAINER.w), h: pt(CONTAINER.h),
    fill: { color: TAN }, line: { color: TAN_LINE, width: CONTAINER.lineW },
    rectRadius: 0.06,
  });
}

function drawFFN47(pptx, slide) {
  const f = FFN;
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(f.box.x), y: pt(f.box.y), w: pt(f.box.w), h: pt(f.box.h),
    fill: { color: TAN }, line: { color: FFN_LINE, width: 1.5 }, rectRadius: 0.05,
  });
  slide.addText(f.header.text, {
    x: pt(f.header.cx - 350), y: pt(f.header.capTop - lead(f.header.size)),
    w: pt(700), h: pt(18),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: f.header.size, bold: true, italic: true, color: HDR_C,
  });
  const t = f.tile;
  for (let k = 0; k < 9; k++) {
    if (k === t.skipSlot) continue; // measured empty slot (6 left group + 2 right group)
    const cx = t.firstCx + k * t.pitch;
    slide.addShape(pptx.ShapeType.roundRect, {
      x: pt(cx - t.w / 2), y: pt(t.y), w: pt(t.w), h: pt(t.h),
      fill: { color: TILE_FILL }, line: { color: TILE_LINE, width: 1 }, rectRadius: 0.06,
    });
    // fan lines first (under dots): each green dot -> each pink dot
    const g0 = -2 * t.greenPitch;
    const p0 = -4 * t.pinkPitch;
    for (let g = 0; g < 5; g++) {
      const gdx = g0 + g * t.greenPitch;
      for (let p = 0; p < 9; p++) {
        const pdx = p0 + p * t.pinkPitch;
        slide.addShape(pptx.ShapeType.line, {
          x: pt(cx + gdx), y: pt(t.greenCy), w: pt(pdx - gdx), h: pt(t.pinkCy - t.greenCy),
          line: { color: FAN, width: 0.5 },
        });
      }
    }
    for (let g = 0; g < 5; g++) {
      const gdx = g0 + g * t.greenPitch;
      slide.addShape(pptx.ShapeType.ellipse, {
        x: pt(cx + gdx - t.greenD / 2), y: pt(t.greenCy - t.greenD / 2),
        w: pt(t.greenD), h: pt(t.greenD), fill: { color: GREEN_DOT },
      });
    }
    for (let p = 0; p < 9; p++) {
      const pdx = p0 + p * t.pinkPitch;
      slide.addShape(pptx.ShapeType.ellipse, {
        x: pt(cx + pdx - t.pinkD / 2), y: pt(t.pinkCy - t.pinkD / 2),
        w: pt(t.pinkD), h: pt(t.pinkD), fill: { color: PINK_DOT },
      });
    }
    slide.addText("RELU", {
      x: pt(cx + t.w / 2 - 26), y: pt(t.relu.y), w: pt(22), h: pt(9),
      align: "right", valign: "top", margin: 0,
      fontFace: FONT, fontSize: t.relu.size, bold: true, color: RELU_C,
    });
  }
}

function drawMHABar47(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: pt(MHA.x), y: pt(MHA.y), w: pt(MHA.w), h: pt(MHA.h),
    fill: { color: PLUM },
  });
  slide.addText("Multi Head Self Attention Block", {
    x: pt(MHA.textCx - 330), y: pt(MHA.y), w: pt(660), h: pt(MHA.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 19, bold: true, color: PLUM_TEXT, lineSpacing: 22,
  });
}

function drawIOBox47(pptx, slide, io) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: pt(io.x), y: pt(io.y), w: pt(io.w), h: pt(io.h),
    fill: { color: IO_FILL }, line: { color: IO_LINE, width: 1.75 }, rectRadius: 0.08,
  });
  slide.addText(io.text, {
    x: pt(io.x), y: pt(io.y), w: pt(io.w), h: pt(io.h),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 19, bold: true, italic: true, color: IO_LINE, lineSpacing: 22,
  });
}

function drawTitleVertical47(pptx, slide) {
  slide.addText(TITLE.text, {
    x: pt(TITLE.cx - TITLE.boxW / 2), y: pt(TITLE.cy - TITLE.boxH / 2),
    w: pt(TITLE.boxW), h: pt(TITLE.boxH),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: TITLE.size, bold: true, color: TITLE_C,
    charSpacing: TITLE.charSpacing, rotate: 270,
  });
}

function drawRedOutArrows47(pptx, slide) {
  // u1's LN1 -> output row arrows are RED (m19 C); u2's are olive (drawn in drawThinArrows47)
  for (const cx of COLS) {
    slide.addShape(pptx.ShapeType.line, {
      x: pt(cx), y: pt(U1.arrows.out.y0), w: 0,
      h: pt(U1.arrows.out.y1 - U1.arrows.out.y0),
      line: { color: RED_OUT, width: 1.75, beginArrowType: "triangle" },
    });
  }
}

function drawYellowBlk47(pptx, slide) {
  const cw = YBLK.w / 2;
  for (let c = 0; c < 2; c++) {
    slide.addShape(pptx.ShapeType.rect, {
      x: pt(YBLK.x + c * cw), y: pt(YBLK.y), w: pt(cw), h: pt(YBLK.h),
      fill: { color: YELLOW_BLK }, line: { color: YBLK_LINE, width: 0.75 },
    });
  }
}

function drawBadge47(pptx, slide, numeral = 47) {
  // Shared chrome constants (playlist law); painted LAST so it sits over the
  // output-row clipped end block. Numeral = the number printed on the original frame.
  const bx = CHROME.badge.cx - CHROME.badge.d / 2;
  const by = CHROME.badge.cy - CHROME.badge.d / 2;
  slide.addShape(pptx.ShapeType.ellipse, {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    fill: { color: CHROME.badge.fill }, line: { color: CHROME.badge.ring, width: CHROME.badge.ringWidth },
  });
  slide.addText(String(numeral), {
    x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
    align: "center", valign: "middle", bold: true,
    fontSize: CHROME.badge.numeralSize, color: CHROME.badge.numeralColor,
    fontFace: CHROME.badge.fontFace, margin: 0,
  });
}

function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 47 : opts.numeral;
  if (opts.chrome !== false) chromeMod.drawHouseChrome(pptx, slide, { numeral: null });
  drawContainer47(pptx, slide);
  drawDashedGroup47(pptx, slide, U1);
  drawDashedGroup47(pptx, slide, U2);
  drawLNBar47(pptx, slide, U1);
  drawLNBar47(pptx, slide, U2);
  drawCurves47(pptx, slide, U1);
  drawCurves47(pptx, slide, U2);
  drawStripRow47(pptx, slide, ROWS.C, "Y", CELL_WARM, LINE_WARM, "A85820", "C88A50");
  drawStripRow47(pptx, slide, ROWS.B, "Y", CELL_WARM, LINE_WARM, "A85820", "C88A50");
  drawStripRow47(pptx, slide, ROWS.A, "Y", CELL_WARM, LINE_WARM, "A85820", "C88A50");
  drawFFN47(pptx, slide);
  drawMHABar47(pptx, slide);
  drawBlockArrows47(pptx, slide);
  drawThinArrows47(pptx, slide, U1, RED_OUT);
  drawThinArrows47(pptx, slide, U2, OLIVE);
  drawDiscs47(pptx, slide, U1);
  drawDiscs47(pptx, slide, U2);
  drawStripRow47(pptx, slide, ROWS.out, "Y", CELL_PALE, LINE_PALE, "8E2626", "C47A7A");
  drawStripRow47(pptx, slide, ROWS.x, "X", CELL_PALE, LINE_PALE, "7E1414", "B06060");
  drawYellowBlk47(pptx, slide);
  drawIOBox47(pptx, slide, IO.out);
  drawIOBox47(pptx, slide, IO.inp);
  drawTitleVertical47(pptx, slide);
  if (numeral !== null) drawBadge47(pptx, slide, numeral);
}

module.exports = {
  renderBase, drawContainer47, drawDashedGroup47, drawLNBar47, drawCurves47,
  drawStripRow47, drawFFN47, drawMHABar47, drawBlockArrows47, drawThinArrows47,
  drawDiscs47, drawIOBox47, drawTitleVertical47, drawRedOutArrows47, drawYellowBlk47,
  drawBadge47, COLS, ROWS, U1, U2, MHA, FFN, BLK, IO, TITLE, SUBS,
};
