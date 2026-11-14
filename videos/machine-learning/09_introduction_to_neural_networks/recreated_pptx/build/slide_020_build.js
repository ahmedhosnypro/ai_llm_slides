const pptxgen = require("pptxgenjs");

// Slide 020: Saturation Problem in Activation Functions
// Geometry measured from unique_slides/slide_020.jpg (960x540 px, 1px = 1/72in).
const NUM = 20;
const TITLE = "Saturation Problem in Activation Functions";
const FONT = "Arial";

const BG = "E8E8E8";
const RED = "C00000";
const RED_BRIGHT = "FF0000";
const BLUE = "0000FF";
const GREEN = "00B050";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFF9C4";
const GRID = "D9D9D9";

const BUILD_DIR = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build";
const GRAPH_DIR = BUILD_DIR + "/graphs_slide_020";

// px -> inches (540 px tall = 7.5 in)
const P = (px) => px / 72.0;

// Measured chart panel boxes (px x0,y0,x1,y1)
const TOP_PANEL = { x: P(338), y: P(116), w: P(616 - 338), h: P(277 - 116) };
const PRELU_PANEL = { x: P(83), y: P(335), w: P(320 - 83), h: P(474 - 335) };
const ELU_PANEL = { x: P(362), y: P(336), w: P(592 - 362), h: P(473 - 336) };
const SOFTPLUS_PANEL = { x: P(638), y: P(336), w: P(876 - 638), h: P(473 - 336) };

// ReLU definition box (upper-left), measured red outline px 71..336 x 102..141
const DEFBOX = { x: P(71), y: P(102), w: P(336 - 71), h: P(141 - 102) };
// Saturation Problem callout, measured ink px 117..289 x 189..239
const CALLOUT = { x: P(117), y: P(189), w: P(289 - 117), h: P(239 - 189) };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: BG };

// 1. Outer red house frame (0.15in inset from every edge) - HOUSE CHROME LAW
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: RED, width: 1.5 },
});

// 2. Slide-number badge - HOUSE CHROME LAW
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: YELLOW }, line: { color: YELLOW, width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. Title - HOUSE CHROME LAW (starts y=0.28, x=0.6, w=12.13, centered)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.55,
  align: "center", valign: "top",
  fontSize: 24, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// Professional-format equation assets (600 dpi mathtext PNGs + sidecars).
const EQ_DIR = BUILD_DIR + "/equations_slide_020";
const EQS = require(EQ_DIR + "/eq_020_segments.json");
const eq = (name, x, baselineIn) => {
  const m = EQS[name];
  return {
    path: EQ_DIR + "/eq_020_" + name + ".png",
    x, y: baselineIn - m.baseline_frac * m.h_in,
    w: m.w_in, h: m.h_in,
  };
};
const eqRun = (names, x, baselineIn, gap = 0.04) => {
  let cx = x;
  for (const n of names) {
    s.addImage(eq(n, cx, baselineIn));
    cx += EQS[n].w_in + gap;
  }
  return cx - gap - x;
};

// 4. ReLU definition box (red-outlined white rectangle, upper-left).
//    The bottom video-player bar in the source frame is a capture artifact and is omitted.
const DEFB = { x: P(71), y: P(102), w: P(336 - 71), h: P(141 - 102) };
s.addShape(pres.shapes.RECTANGLE, {
  ...DEFB,
  fill: { color: WHITE }, line: { color: RED_BRIGHT, width: 1 },
});
eqRun(["def_lhs", "def_name", "def_eq"], DEFB.x + 0.08, P(126));
s.addShape(pres.shapes.LINE, {
  x: DEFB.x + 2.45, y: DEFB.y + 0.05, w: 0, h: DEFB.h - 0.10,
  line: { color: BLACK, width: 0.75 },
});
eqRun(["def_zero", "def_cond_lt"], DEFB.x + 2.52, P(112));
eqRun(["def_x", "def_cond_gt"], DEFB.x + 2.52, P(129));

// 5. "F(x) = ReLU" heading above the top chart (measured px 330..615, rows 91..117)
const HEAD = { x: P(330), y: P(88), w: P(290), h: 0.34 };
const headW = EQS.head_lhs.w_in + 0.04 + EQS.head_relu.w_in;
eqRun(["head_lhs", "head_relu"], HEAD.x + (HEAD.w - headW) / 2, P(105));

// 6. Four activation-function charts (generated PNGs with baked blue borders)
s.addImage({ path: GRAPH_DIR + "/graph_relu.png", ...TOP_PANEL });
s.addImage({ path: GRAPH_DIR + "/graph_prelu.png", ...PRELU_PANEL });
s.addImage({ path: GRAPH_DIR + "/graph_elu.png", ...ELU_PANEL });
s.addImage({ path: GRAPH_DIR + "/graph_softplus.png", ...SOFTPLUS_PANEL });

// 7. Saturation Problem callout (red-outlined white box, middle-left)
const CALL = { x: P(95), y: P(185), w: P(285 - 95), h: P(245 - 185) };
s.addShape(pres.shapes.RECTANGLE, {
  ...CALL,
  fill: { color: WHITE }, line: { color: RED_BRIGHT, width: 1 },
});
s.addText("Saturation Problem", {
  x: CALL.x, y: CALL.y + 0.02, w: CALL.w, h: 0.24,
  align: "center", valign: "middle",
  fontSize: 13, bold: true, color: RED_BRIGHT, fontFace: FONT, margin: 0,
});
s.addText("Same Output value", {
  x: CALL.x, y: CALL.y + 0.26, w: CALL.w, h: 0.22,
  align: "center", valign: "middle",
  fontSize: 11, color: BLUE, underline: true, fontFace: FONT, margin: 0,
});
s.addText([
  { text: "for ", options: { color: BLUE } },
  { text: "Different", options: { color: BLUE, underline: true } },
  { text: " Input values", options: { color: BLUE } },
], {
  x: CALL.x, y: CALL.y + 0.48, w: CALL.w, h: 0.22,
  align: "center", valign: "middle",
  fontSize: 11, fontFace: FONT, margin: 0,
});

// 8. Curved solid red leader from the callout into the yellow ellipse.
s.addShape(pres.ShapeType.custGeom, {
  x: 0, y: 0, w: 13.333, h: 7.5,
  line: { color: RED_BRIGHT, width: 2 },
  points: [
    { x: P(285), y: P(212), moveTo: true },
    { x: P(388), y: P(241), curve: { type: "cubic", x1: P(325), y1: P(238), x2: P(358), y2: P(248) } },
  ],
});
s.addShape(pres.shapes.RIGHT_ARROW, {
  x: P(386), y: P(236), w: P(12), h: P(8),
  fill: { color: RED_BRIGHT }, line: { color: RED_BRIGHT, width: 0.5 },
});

// 9. Three dashed red connector arrows from the top chart down to the bottom row.
function dashedArrow(x0, y0, x1, y1) {
  s.addShape(pres.shapes.LINE, {
    x: x0, y: y0, w: x1 - x0, h: y1 - y0,
    line: { color: RED_BRIGHT, width: 1.5, dashType: "dash", endArrowType: "triangle" },
  });
}
dashedArrow(P(477), P(279), P(201), P(333));
dashedArrow(P(477), P(279), P(477), P(334));
dashedArrow(P(477), P(279), P(757), P(334));

// 10. Captions below the bottom charts (measured row band 470..500)
const CAP_BASE = P(493);
const capRun = (names, panel) => {
  const total = names.reduce((a, n) => a + EQS[n].w_in, 0) + 0.04 * (names.length - 1);
  eqRun(names, panel.x + (panel.w - total) / 2, CAP_BASE);
};
capRun(["cap_prelu_lhs", "cap_prelu_parametric", "cap_prelu_relu"], PRELU_PANEL);
capRun(["cap_elu_lhs", "cap_elu_name"], ELU_PANEL);
capRun(["cap_softplus_lhs", "cap_softplus_name"], SOFTPLUS_PANEL);

const outPptx = BUILD_DIR + "/slide_020_recreated.pptx";
pres.writeFile({ fileName: outPptx }).then(() => console.log("wrote " + outPptx));
