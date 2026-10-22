// components/slide_027.js — CERTIFIED composition of slide 027
// ("Follow Negative Direction of Gradient with Selected Learning Rate"),
// ML lecture 03 (03_ridger_regression_gradient_descent). BANKED post-PASS
// (playlist-scoped component-banking obligation, 17_worker_instructions.md):
// no slide in THIS video depends on 027 (root, no children per the founder
// dependency graph), but a future lecture's recap/variant may import it.
//
// CERTIFICATION (2026-10-20/21, worker w8-s027-20261020T2330):
//   full-slide Template A judge PASS — judge_attempt_3.txt (on render_3.png);
//   Template B crop certificates: title / axis_top / axis_right / lower_left /
//   min_cluster PASS; dot_sequence FAIL x3 (attempt-2 BLOCKER, attempt-3 + re-roll
//   MAJOR, "inter-dot arrowheads") PIL-ADJUDICATED as fabricated — five
//   independent measurements refute it (0 extra unexplained inter-dot px; 1px
//   ASCII maps; chain-band ink budget 237 vs 241 px; annulus 89 vs 84 px;
//   perpendicular width profile 0 widenings) — banked in
//   qa/slide027/adjudication_attempt_3.md + variance transcripts
//   crop_2_dot_sequence_judge.txt / crop_3_dot_sequence_judge.txt /
//   crop_3_dot_sequence_judge_reroll.txt.
//   Geometry PIL-measured from unique_slides/slide_027.jpg (960x540, 1px = 1pt);
//   full dossier: qa/slide027/measured_geometry.md.
//
// CONTRACT: renderBase(pptx, slide, opts) draws the FULL slide (house chrome with
// numeral 27 + title + red graph box + axes/arrowheads + dashed leaders + parabola
// custGeom + 9 violet dots + yellow minimum dot + labels + theta glyphs + gray plus
// + theta-hat caret). opts:
//   { numeral }            — override the badge numeral (a recap variant passes its
//                            own number; the badge numeral is ALWAYS the number
//                            printed on the VARIANT's own original frame)
//   { skip: { ... } }      — omit any block: chrome, title, graphBox, axes, dashes,
//                            curve, dots, labels, plus, thetahatCaret
//   { only: { ... } }      — draw ONLY the listed blocks (a child composes its delta)
// Never edit this certified module in place — copy-then-modify (cascade law).

const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../../shared_patterns/house_chrome.js"));

const pptx_ShapeType = null; // resolved per-call from the pptxgen instance

const px = (v) => v / 72; // frame px -> inches

// ---- measured constants (frame px / pt) — see qa/slide027/measured_geometry.md ----
const TITLE = [
  { t: "Follow Negative Direction of Gradient with", base: 92.75, cx: 467.5, boxW: 660, dy: -2.9 },
  { t: "Selected Learning Rate", base: 127.75, cx: 471.0, boxW: 400, dy: -3.4 },
];
const T_S = 31.5, T_LS = 1.2 * T_S, T_BASE_FRAC = 0.849;

const TRACE = [
  [253, 230], [254, 236], [255, 242], [256, 246], [259, 252], [262, 272], [268, 280],
  [270, 286], [272, 292], [274, 296], [276, 300], [278, 302], [288, 318], [290, 322],
  [291, 324], [293, 326], [294, 328], [296, 330], [297, 332], [299, 334], [313, 350],
  [316, 352], [318, 354], [320, 356], [322, 358], [324, 360], [363, 386], [365, 388],
  [383, 395], [400, 400], [420, 404], [436, 406], [445, 408],
  [463, 406], [479, 404], [497, 400], [525, 390], [543, 380], [561, 368], [571, 360],
  [584, 348], [595, 336], [604, 324], [612, 312], [619, 300], [624, 288], [628, 280],
  [632, 268], [635, 260], [637, 252], [638, 248], [639, 244], [640, 240], [641, 236],
];
const BLUE = "5F41C4"; // w8 adjudicated dot fill (PIL core of the original frame)
const BLUE_DOTS = [
  [262.0, 263.5], [283.0, 310.5], [306.5, 342.0], [332.0, 366.5], [354.5, 380.5],
  [374.5, 390.0], [392.0, 396.5], [411.0, 403.5], [426.5, 403.5],
];
const DASHES = [
  { x: 262.5, rows: [[272, 278], [286, 292], [300, 306], [314, 320], [328, 335],
                     [343, 348], [357, 363], [371, 377], [385, 391], [400, 406],
                     [414, 420], [428, 434]] },
  { x: 444.5, rows: [[415, 422], [430, 436]] },
];
const L_ASC = 0.913, L_EXT = 1.138;
const LABELS = [
  ["Cost",           18.88, 189.0, 219.0, 39],
  ["Learning step",  17.62, 284.1, 350.5, 107],
  ["Minimum",        16.88, 375.6, 462.5, 69],
  ["Random",         17.12, 455.8, 262.5, 65],
  ["initial value",  17.62, 478.0, 262.5, 87],
];

function catmullRomPoints(P) {
  const phantom0 = { x: 2 * P[0][0] - P[1][0], y: 2 * P[0][1] - P[1][1] };
  const phantomN = { x: 2 * P[P.length - 1][0] - P[P.length - 2][0],
                     y: 2 * P[P.length - 1][1] - P[P.length - 2][1] };
  const Q = [phantom0, ...P.map((p) => ({ x: p[0], y: p[1] })), phantomN];
  const out = [{ x: px(Q[1].x), y: px(Q[1].y), moveTo: true }];
  for (let i = 1; i < Q.length - 2; i++) {
    const P0 = Q[i - 1], P1 = Q[i], P2 = Q[i + 1], P3 = Q[i + 2];
    out.push({
      x: px(P2.x), y: px(P2.y),
      curve: { type: "cubic",
               x1: px(P1.x + (P2.x - P0.x) / 6), y1: px(P1.y + (P2.y - P0.y) / 6),
               x2: px(P2.x - (P3.x - P1.x) / 6), y2: px(P2.y - (P3.y - P1.y) / 6) },
    });
  }
  return out;
}

function drawTitle(pptx, slide) {
  for (const L of TITLE) {
    slide.addText(L.t, {
      x: px(L.cx - L.boxW / 2),
      y: px(L.base - T_BASE_FRAC * T_S + (L.dy || 0)),
      w: px(L.boxW), h: px(52),
      align: "center", valign: "top", margin: 0,
      fontFace: "Calibri", fontSize: T_S, bold: true, color: "8B0000",
      lineSpacing: T_LS,
    });
  }
}

function drawGraphBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(193.5), y: px(167), w: px(522.5), h: px(340),
    fill: { color: "E9E9E7" },
    line: { color: "FF0000", width: 2 },
  });
}

function triShape(pptx, slide, pts) {
  const p = pts.map((q, i) =>
    i === 0 ? { x: px(q[0]), y: px(q[1]), moveTo: true } : { x: px(q[0]), y: px(q[1]) });
  p.push({ close: true });
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,
    fill: { color: "000000" }, line: { color: "000000", width: 0 },
    points: p,
  });
}

function drawAxes(pptx, slide) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(222.5), y: px(222), w: 0, h: px(214),
    line: { color: "000000", width: 2 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(222), y: px(436), w: px(448), h: 0,
    line: { color: "000000", width: 2 },
  });
  triShape(pptx, slide, [[223, 206], [218, 222], [228, 222]]);
  triShape(pptx, slide, [[686, 436], [670, 431], [670, 442]]);
}

function drawDashes(pptx, slide) {
  for (const d of DASHES) {
    for (const [y0, y1] of d.rows) {
      slide.addShape(pptx.ShapeType.line, {
        x: px(d.x), y: px(y0), w: 0, h: px(y1 - y0 + 1),
        line: { color: "000000", width: 2 },
      });
    }
  }
}

function drawCurve(pptx, slide) {
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,
    line: { color: "000000", width: 2 },
    points: catmullRomPoints(TRACE),
  });
}

function drawDots(pptx, slide) {
  for (const [cx, cy] of BLUE_DOTS) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: px(cx - 6.5), y: px(cy - 6.5), w: px(13), h: px(13),
      fill: { color: BLUE }, line: { color: BLUE, width: 0 },
    });
  }
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(444.5 - 6.25), y: px(407 - 6.25), w: px(12.5), h: px(12.5),
    fill: { color: "FFFF00" }, line: { color: "FFFF00", width: 0 },
  });
}

function drawLabels(pptx, slide) {
  for (const [t, S, base, cx, inkW] of LABELS) {
    const L = 1.2 * S;
    slide.addText(t, {
      x: px(cx - inkW * 1.25 / 2),
      y: px(base - ((L - L_EXT * S) / 2 + L_ASC * S)),
      w: px(inkW * 1.25), h: px(34),
      align: "center", valign: "top", margin: 0,
      fontFace: "Arial", fontSize: S, color: "000000",
      lineSpacing: L,
    });
  }
  addTheta(pptx, slide, "\u03b8", 22.0, 443.4, 703.0);
  addTheta(pptx, slide, "\u03b8", 22.0, 504.0, 444.0);
}

function addTheta(pptx, slide, t, S, base, cx) {
  const L = 1.2 * S;
  slide.addText(t, {
    x: px(cx - 12.3 * 1.25 / 2),
    y: px(base - ((L - L_EXT * S) / 2 + L_ASC * S)),
    w: px(12.3 * 1.25), h: px(34),
    align: "center", valign: "top", margin: 0,
    fontFace: "Arial", fontSize: S, color: "000000",
    lineSpacing: L,
  });
}

function drawPlus(pptx, slide) {
  const PLUS = "8C8C8C";
  slide.addShape(pptx.ShapeType.rect, {
    x: px(410), y: px(446), w: px(2), h: px(10),
    fill: { color: PLUS }, line: { color: PLUS, width: 0 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(406), y: px(450), w: px(11), h: px(2),
    fill: { color: PLUS }, line: { color: PLUS, width: 0 },
  });
}

function drawThetahatCaret(pptx, slide) {
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,
    line: { color: "000000", width: 1.5 },
    points: [
      { x: px(440), y: px(484.5), moveTo: true },
      { x: px(444), y: px(480) },
      { x: px(448), y: px(484.5) },
    ],
  });
}

const BLOCKS = {
  chrome: (pptx, slide, opts) => drawHouseChrome(pptx, slide, { numeral: opts.numeral !== undefined ? opts.numeral : 27 }),
  title: drawTitle,
  graphBox: drawGraphBox,
  axes: drawAxes,
  dashes: drawDashes,
  curve: drawCurve,
  dots: drawDots,
  labels: drawLabels,
  plus: drawPlus,
  thetahatCaret: drawThetahatCaret,
};

function renderBase(pptx, slide, opts = {}) {
  const skip = opts.skip || {};
  const only = opts.only || null;
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (only && !only[name]) continue;
    if (!only && skip[name]) continue;
    fn(pptx, slide, opts);
  }
}

module.exports = {
  renderBase, BLOCKS,
  TITLE, TRACE, BLUE_DOTS, BLUE, DASHES, LABELS,
  T_S, T_LS, T_BASE_FRAC,
};
