// slide_008.js — "Self Attention Mechanism (Linear Transformation of Inputs)" /
// "(Self Attention of word X₂ w.r.t All words in Sentence ( X₁, X₂, X₃, X₄ )"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 8)
// ATTEMPT 2 (2026-10-12) — see qa/slide008/collision_notice.txt for the dual-dispatch
// resolution; attempt 1 (Worker A: build_attempt_1.js / render_1.png) stays banked.
//
// CROSS-VIDEO CHILD (founder directive 2026-10-11): parent = 001:33 (CERTIFIED in
// 001's own DB: gen_status=passed + visual_check=PASS). The parent's certified
// component is required by ABSOLUTE PATH and drawn via renderBase with this slide's
// delta blocks skipped; deltas are drawn at THIS frame's measured geometry.
//
// FRAME->SLIDE MAPPING (video-002 letterboxed renderer; landmarks re-measured on
// THIS frame: left border 58.5, right 902, top 42, bottom stroke ~516.5):
//   frame_x = 17.628 + 0.961232 * slide_x ;  frame_y = 0.955556 * slide_y
// (scratch/slide008/measure_*.py + zoomread_orig/zoom8.txt through the gate).
//
// MEASURED DELTAS (frame wins over spec/audit hexes — COLOR LAW):
//   * wboxes: NO yellow bands; 4+4 narrow boxes (W_k x160.6 w35.4 LIGHT-GREEN
//     D4FCDC / border 51A363; W_v x706.5 w34.6 PALE-BLUE D2ECFF / navy 1F2C6B;
//     rows y 235.5/277.3/318.1/362.1 h25.5); BLACK bold labels (frame cores
//     (0,7,0)) with the parent's tan "(r)" superscript (8x zoom P/Q: "(r)", black).
//   * flowlines: container->W-box connectors RED WITH ARROWHEADS ending at the box
//     edges (heads measured frame x 167..170 / 731..737 on the parent centerlines);
//     NO orange triangles anywhere in this frame (attempt 1's orange tris refuted);
//     long box->dot arrows start at the narrower box edge (197).
//   * dotproduct: parent geometry + dots at the verified +2/+3 drift (DOTC8),
//     K.q moved to the measured ink (frame x 352..373, y 192..203 -> 13pt at
//     slide ~(348..370, 201..212); parent's certified spot is 14px left).
//   * sigma: multiply rings d~36.5 (frame arcs 33-35px, x4 consistent; parent d19)
//     at centers (534.5,240),(564.5,290.5),(592.5,325.5),(623,371.5), stroke ~3,
//     fill NONE (peach interiors measured), '*' 14pt red; NO stems and NO side
//     stubs (windowed scan y188..212 x505..645: ZERO red between Sigma and rings).
//   * query: W_q box (275,432,47,48) yellow band fill (blend-solved #FFFD79;
//     NOT purple — spec hex refuted), parent label style; q2 label + mini-vector
//     at parent positions (frame ink + zoom reads confirm both exist); W_q->DP
//     arrow parent; X2->W_q arrow head at slide ~(299,471) per frame ink (307..309,450).
//   * y2: output strip = plain "Y" (dark green 2E8530) — NO subscript (the 8x
//     "subscript" mark = cell dividers + border dashes); 5 cells 3 green B3DF9F +
//     2 gray-green B0C4BD, dividers 7DA076, strip (548,124.5,69,22); green block
//     arrow + red head + gray guide verbatim.
//   * overlays: translucent BLUE circle — blend-solved #4583C9 @ ~58% over
//     peach/dp/green (validated on the red-arrow cross-check); center slide
//     (300,445) d~109.5 (frame bbox x 254..358, y 374..479); red block arrow at
//     X2 at Worker-A's verified geometry (268,514,22,13,rot326).
//   * sentence: container top +4 (y477 h41, Worker-A verified); widgets verbatim;
//     X2 highlight MAGENTA FF00FF (blend-solved; parent BE4148 refuted: frame
//     highlight pixels require bg B>149).
//   * title: L1 at y56 (+3px, Worker-A verified ink rows), L2 verbatim y81.
//   * legend: W square border tan C3B285 (frame (199,181,133); parent orange
//     C87A2A refuted) — overlay at the same rect.
//
// CHROME LAW: badge numeral 8 (printed on THIS frame) via the parent's
// drawHouseChrome chain. Verbatim text; margin:0 + explicit fontFace; explicit
// lineSpacing on the two-line Dot/Product box; no '#' in hex; single plain-named
// deliverable; never writes outside this video's namespace.

const pptxgen = require("pptxgenjs");
const P = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_033.js"
);

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const px = P.px;
const FONT = "Arial";
const C = P.C;

// ---- measured 002:8 geometry (true slide px) --------------------------------------
const LINEY = P.GEO.LINEY;                      // [247.5,288,329,372.5] (head rows verify ±1)
const DOTC8 = [[332, 249], [316, 290], [298, 331], [279, 375]]; // dots (+2/+3 drift, verified)
const DOTX8 = [332, 316, 298, 279];
const NODES = [[534.5, 240], [564.5, 290.5], [592.5, 325.5], [623, 371.5]]; // ring centers
const BOXY8 = [235.5, 277.3, 318.1, 362.1];
const BOXH8 = 25.5;

const s = pres.addSlide();

// ---- 1. parent certified composition (delta blocks skipped; numeral 8) -------------
P.renderBase(pres, s, {
  numeral: 8,
  skip: ["wboxes", "flowlines", "orangeheads", "dotproduct", "sigma", "query", "y2", "sentence", "overlays", "title"],
});

function redArrow(x1, y1, x2, y2, width, opts = {}) {
  s.addShape(pres.ShapeType.line, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: {
      color: opts.color || C.red, width: width || 1.25,
      endArrowType: opts.head === false ? undefined : "triangle",
      dashType: opts.dash,
    },
  });
}

// ---- 2. sentence row (container y477 h41; X2 highlight FF00FF) ----------------------
s.addShape(pres.ShapeType.roundRect, {
  x: px(177), y: px(477), w: px(315), h: px(41), rectRadius: 0.06,
  fill: { color: C.containerFill },
  line: { color: C.containerBorder, width: 1.25, dashType: "sysDot" },
});
function embedWidget8(x, y, w, h, label, cells) {
  const cw = w / 5;
  const fills = cells || [C.cell1, C.cell2, C.cell3, C.cell4, C.cell5];
  for (let i = 0; i < 5; i++) {
    s.addShape(pres.ShapeType.rect, {
      x: px(x + i * cw), y: px(y), w: px(cw), h: px(h),
      fill: { color: fills[i] }, line: { color: C.divider, width: 0.5 },
    });
  }
  if (label) {
    s.addText(
      [
        { text: "X", options: {} },
        { text: label, options: { subscript: true } },
      ],
      {
        x: px(x + 1.5 * cw), y: px(y - 2), w: px(2 * cw), h: px(h + 4),
        align: "center", valign: "middle", margin: 0,
        fontFace: FONT, fontSize: 11, bold: true, color: C.labelRed,
      }
    );
  }
}
embedWidget8(189, 481, 66, 24, "1");
embedWidget8(257, 481, 75, 24, "2", [C.x2c1, C.x2c2, C.x2c3, C.x2c4, C.x2c5]);
s.addShape(pres.ShapeType.roundRect, {
  x: px(255), y: px(479), w: px(79), h: px(28), rectRadius: 0.04,
  fill: { type: "none" },
  line: { color: "FF00FF", width: 1.5, dashType: "sysDot" },
});
embedWidget8(335, 481, 66, 24, "3");
embedWidget8(403, 481, 66, 24, "4");

// ---- 3. Dot Product box (parent geometry; dots +2/+3; K.q at measured ink) ----------
s.addShape(pres.ShapeType.rect, {
  x: px(255), y: px(194), w: px(87), h: px(208),
  fill: { color: C.dpFill }, line: { color: C.dpBorder, width: 1 },
});
s.addText(
  [
    { text: "Dot", options: { breakLine: true } },
    { text: "Product", options: {} },
  ],
  {
    x: px(262), y: px(196), w: px(72), h: px(34),
    align: "center", valign: "top", margin: 0,
    fontFace: FONT, fontSize: 11, bold: true, color: C.dpTitle, lineSpacing: 13,
  }
);
s.addText("K.q", {
  x: px(347), y: px(197.5), w: px(32), h: px(20),
  align: "left", valign: "top", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 13, bold: true, color: C.kq,
});
DOTC8.forEach(([cx, cy]) => {
  s.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 6.5), y: px(cy - 6.5), w: px(13), h: px(13),
    fill: { color: C.dotHalo }, line: { color: "6F8FC0", width: 0.5 },
  });
  s.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 3.5), y: px(cy - 3.5), w: px(7), h: px(7),
    fill: { color: C.dotCore }, line: { type: "none" },
  });
});

// ---- 4. flow lines (red arrowheads at the narrow box edges; no orange) --------------
LINEY.forEach((y) => redArrow(140, y, 159, y, 1.5));              // container -> W_k
LINEY.forEach((y, i) => redArrow(197, y, DOTX8[i] - 8, y, 1.25)); // W_k -> dot
LINEY.forEach((y) => redArrow(763, y, 749, y, 1.5));              // container -> W_v
DOTC8.forEach(([cx, cy]) => {                                     // converging lines
  s.addShape(pres.ShapeType.line, {
    x: px(Math.min(cx, 300)), y: px(cy), w: px(Math.abs(cx - 300)), h: px(399 - cy),
    flipV: cx > 300,
    line: { color: C.red, width: 1 },
  });
});

// ---- 5. color-coded W boxes (no bands; measured geometry) ---------------------------
function wBox8(x, y, w, sub, fill, border) {
  s.addShape(pres.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(BOXH8),
    fill: { color: fill }, line: { color: border, width: 1 },
  });
  s.addText(
    [
      { text: "W", options: {} },
      { text: sub, options: { subscript: true } },
      { text: "(r)", options: { superscript: true, color: "A08A28", fontSize: 6.5 } },
    ],
    {
      x: px(x), y: px(y), w: px(w), h: px(BOXH8),
      align: "center", valign: "middle", margin: 0, wrap: false,
      fontFace: FONT, fontSize: 10.5, bold: true, color: "000000",
    }
  );
}
BOXY8.forEach((y) => wBox8(160.6, y, 35.4, "k", "D4FCDC", "51A363"));
BOXY8.forEach((y) => wBox8(706.5, y, 34.6, "v", "D2ECFF", "1F2C6B"));

// ---- 6. sigma block: Sigma box (parent geometry) + multiply rings --------------------
// (rings d36.5, peach interiors, no stems/stubs — all verified on this frame)
s.addShape(pres.ShapeType.rect, {
  x: px(516), y: px(194), w: px(135), h: px(25),
  fill: { color: C.sigmaFill }, line: { color: C.sigmaBorder, width: 1 },
});
s.addText("\u03A3", {
  x: px(516), y: px(194), w: px(135), h: px(25),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 16, bold: true, color: C.sigmaText,
});
NODES.forEach(([cx, cy]) => {
  s.addShape(pres.ShapeType.ellipse, {
    x: px(cx - 18.25), y: px(cy - 18.25), w: px(36.5), h: px(36.5),
    fill: { type: "none" }, line: { color: C.red, width: 3 },
  });
  s.addText("*", {
    x: px(cx - 10), y: px(cy - 10), w: px(20), h: px(20),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 14, bold: true, color: C.red,
  });
});

// ---- 7. query path (W_q yellow at measured geometry; q2/vector/arrows parent) --------
s.addShape(pres.ShapeType.rect, {
  x: px(275), y: px(432), w: px(47), h: px(48),
  fill: { color: C.band }, line: { color: C.boxBorder, width: 1 },
});
s.addText(
  [
    { text: "W", options: {} },
    { text: "q", options: { subscript: true } },
    { text: "(r)", options: { superscript: true, color: "A08A28", fontSize: 6.5 } },
  ],
  {
    x: px(275), y: px(432), w: px(47), h: px(48),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 11, bold: true, color: C.olive,
  }
);
s.addText(
  [
    { text: "q", options: {} },
    { text: "2", options: { subscript: true } },
  ],
  {
    x: px(277), y: px(407), w: px(26), h: px(22),
    align: "left", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 12, bold: true, color: C.qRed,
  }
);
// q2 mini vector (parent geometry — present in frame per zoom reads)
(function () {
  const cw = 34 / 5;
  for (let i = 0; i < 5; i++) {
    s.addShape(pres.ShapeType.rect, {
      x: px(304 + i * cw), y: px(414), w: px(cw), h: px(12),
      fill: { color: [C.cell1, C.cell2, C.cell3, C.cell4, C.cell5][i] },
      line: { color: C.divider, width: 0.5 },
    });
  }
})();
redArrow(299, 433, 299, 407, 1.5);  // W_q -> DP (through q2)
redArrow(299, 478, 299, 467, 1.25); // X2 -> W_q (head ~471 per frame ink)

// ---- 8. output strip: plain Y (no subscript), measured strip -------------------------
const YX = 548, YY = 124.5, YW = 69, YH = 22;
const cellW = YW / 5;
const yCells = ["B3DF9F", "B3DF9F", "B3DF9F", "B0C4BD", "B0C4BD"];
for (let i = 0; i < 5; i++) {
  s.addShape(pres.ShapeType.rect, {
    x: px(YX + i * cellW), y: px(YY + 2), w: px(cellW), h: px(YH - 4),
    fill: { color: yCells[i] }, line: { color: "7DA076", width: 0.5 },
  });
}
s.addShape(pres.ShapeType.rect, {
  x: px(YX), y: px(YY), w: px(YW), h: px(YH),
  fill: { type: "none" }, line: { color: C.y2Border, width: 1, dashType: "sysDot" },
});
s.addText("Y", {
  x: px(564), y: px(YY + 1), w: px(26), h: px(YH - 2),
  align: "center", valign: "middle", margin: 0, wrap: false,
  fontFace: FONT, fontSize: 12, bold: true, color: "2E8530",
});
// green block arrow (Sigma -> Y), red head + gray guide (parent verbatim)
s.addShape(pres.ShapeType.rightArrow, {
  x: px(548), y: px(149), w: px(30), h: px(16), rotate: 315,
  fill: { color: C.greenArrow }, line: { color: C.greenArrowLine, width: 0.75 },
});
s.addShape(pres.ShapeType.triangle, {
  x: px(579), y: px(146), w: px(8), h: px(8),
  fill: { color: C.triRed }, line: { type: "none" },
});
s.addShape(pres.ShapeType.line, {
  x: px(583), y: px(156), w: 0, h: px(38),
  line: { color: C.grayLine, width: 0.75 },
});

// ---- 9. overlays: translucent BLUE circle over q2/W_q + red block arrow at X2 -------
s.addShape(pres.ShapeType.ellipse, {
  x: px(245.25), y: px(390.25), w: px(109.5), h: px(109.5),
  fill: { color: "4583C9", transparency: 58 }, line: { type: "none" },
});
s.addShape(pres.ShapeType.rightArrow, {
  x: px(268), y: px(514), w: px(22), h: px(13), rotate: 326,
  fill: { color: C.redDark }, line: { type: "none" },
});

// ---- 10. title (L1 y56 per measured ink rows; L2 verbatim) ---------------------------
s.addText(
  [
    { text: "Self Attention Mechanism ", options: { color: "000000" } },
    { text: "(Linear Transformation of Inputs)", options: { color: C.titleBlue } },
  ],
  {
    x: px(183), y: px(56), w: px(650), h: px(24),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 20, bold: true,
  }
);
s.addText(
  [
    { text: "(Self Attention of word ", options: { color: "000000" } },
    { text: "X", options: { color: C.titleRed } },
    { text: "2", options: { subscript: true, color: C.titleRed } },
    { text: " w.r.t All words in Sentence ( ", options: { color: "000000" } },
    { text: "X", options: { color: C.titleRed } },
    { text: "1", options: { subscript: true, color: C.titleRed } },
    { text: ", ", options: { color: C.titleRed } },
    { text: "X", options: { color: C.titleRed } },
    { text: "2", options: { subscript: true, color: C.titleRed } },
    { text: ", ", options: { color: C.titleRed } },
    { text: "X", options: { color: C.titleRed } },
    { text: "3", options: { subscript: true, color: C.titleRed } },
    { text: ", ", options: { color: C.titleRed } },
    { text: "X", options: { color: C.titleRed } },
    { text: "4", options: { subscript: true, color: C.titleRed } },
    { text: " )", options: { color: "000000" } },
  ],
  {
    x: px(183), y: px(81), w: px(650), h: px(24),
    align: "center", valign: "middle", margin: 0, wrap: false,
    fontFace: FONT, fontSize: 20, bold: true,
  }
);

// ---- 11. legend W square: tan border (measured) — overlay at the same rect -----------
s.addShape(pres.ShapeType.rect, {
  x: px(798), y: px(472), w: px(29), h: px(29),
  fill: { color: C.legW }, line: { color: "C3B285", width: 1.5 },
});
s.addText("W", {
  x: px(798), y: px(472), w: px(29), h: px(29),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 14, bold: true, color: "000000",
});

// ---- write ---------------------------------------------------------------------------
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_008_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
