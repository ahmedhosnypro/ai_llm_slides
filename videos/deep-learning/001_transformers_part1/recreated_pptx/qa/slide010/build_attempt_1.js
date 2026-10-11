// build/slide_010.js — slide 010 "RNN  Seq2Seq model [with Attention]"
//
// DEPENDENCY-GATED CHILD BUILD (founder directive 2026-10-11; edge 10 <- 6):
// slide 10 = slide 6's judge-certified composition + REMOVE/REPLACE delta. The base
// comes from the certified component components/slide_006.js — never re-derived.
// INHERITED blocks (frame-verified within the ~4px closed-loop tolerance):
//   dec_container (117..281 vs measured 117..283), enc_container (306..496 vs
//   307..498), ctx_arc + dec_dot + enc_dot (dots within 2px of measured).
// REPLACED/REDRAWN at slide-010 measured geometry (PIL + vision, scratch/slide010/):
//   title (2 lines), decoder content (column pitch fans 555.5/690/824 vs parent
//   554/685/815.5; o-labels -6.5px), encoder content (bars x -10/-5/-2, lower half
//   +5..+10px), captions "Decoder"/"Encoder" (shortened), pink callout (moved up
//   30px) + bezier connector, green callout + sage connector, both lavender
//   attention boxes + node + converging arrow-lines, dashed pink attention fan
//   with olive arrowheads, gray "Decoder Utilizes:" summary box, white backdrop
//   card (measured x36.5..921.5 y116.5..500; drawn INSET x43..917 so the mandated
//   chrome side borders stay visible — playlist chrome law overrides).
//
// LAWS honored: verbatim text incl. double spaces ("RNN  Seq2Seq", "[ To overcome");
// underline ONLY under "Bottleneck" (frame-measured x433..535); "with Attention" and
// the whole subtitle line are BLUE (frame-measured); mouse-cursor artifact omitted;
// margin:0 + explicit fontFace everywhere; no '#' in hex; single-version deliverable.

const path = require("path");
const pptxgen = require("pptxgenjs");
const parent = require(path.join(__dirname, "components", "slide_006.js"));

const px = parent.px; // frame px -> inches (v/72); 1 frame px = 1 pt
const ASSETS = path.join(__dirname, "assets");
const C = parent.C;   // certified palette (red/decInk/encInk/fills/edges)

// ---- delta palette (JPEG-core measured from slide_010.jpg) -------------------
const D = {
  blue: "060084",       // title blue words + subtitle + Attention captions
  cardWhite: "FFFFFF",
  boxFill: "EFF1FD",    // both lavender attention boxes (measured cores 239,241,253)
  leftEdge: "C3CCD5",   // left box border (measured #c3ccd5)
  rightEdge: "C8CCD5",  // right box border (measured #c8ccd5)
  nodeFill: "D6D8E4",   // attention node fill (NOT white — measured)
  nodeEdge: "A9ACB8",
  nodeText: "44444C",
  lineDark: "404040",   // 3 thin node-to-cell lines
  greenFill: "DDFFE8",  // green callout fill (221,255,232)
  greenEdge: "8FBF9A",  // green callout border (sage)
  sage: "8FAE90",       // green connector stroke
  calloutFill: "F8DCDD",// pink callout fill (248,220,221 — parent F6DCDD family)
  grayFill: "EAE6DD",   // summary box fill (234,230,221)
  grayEdge: "99A0A6",   // summary box border
  bodyInk: "1A1A1A",
};

const SANS = "Arial";
const MATH = "Times New Roman";

// ---- measured decoder geometry (column pitch fans right: +1.5/+5/+8.5) --------
const DECCOL = [px(555.5), px(690), px(824)];
const DECBAR = [
  { x: px(517), w: px(77) }, { x: px(651.5), w: px(77) }, { x: px(785.5), w: px(77) },
];
// ---- measured encoder geometry (bars shift left: -10/-5/-2; lower half +5..+10)
const ENCBAR = [
  { x: px(113.5), w: px(77) }, { x: px(248.5), w: px(77) }, { x: px(382), w: px(77) },
];
const ENCCOL = [px(152), px(287), px(420.5)];

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) chrome only (playlist law; badge numeral 10) --------------------------
parent.renderBase(pres, slide, { numeral: 10, only: [] });

// ---- 2) white backdrop card (measured x36.5..921.5 y116.5..500; inset for the
//         mandated chrome side borders — see header comment) ----------------------
slide.addShape(pres.ShapeType.rect, {
  x: px(43), y: px(116.5), w: px(874), h: px(383.5),
  fill: { color: D.cardWhite }, line: { type: "none" },
});

// ---- 3) inherited containers ---------------------------------------------------
parent.renderBase(pres, slide, { chrome: false, only: ["dec_container", "enc_container"] });

// ---- 4) decoder content (slide-010 geometry) -----------------------------------
function drawSegBar(x, y, w, h, fill, edge) {
  slide.addShape(pres.ShapeType.rect, {
    x, y, w, h, fill: { color: fill }, line: { color: edge, width: 1 },
  });
  for (let k = 1; k <= 3; k++) {
    slide.addShape(pres.ShapeType.line, {
      x: x + (w * k) / 4, y, w: 0, h, line: { color: edge, width: 1 },
    });
  }
}

// green top-row bars y196..216 (parent 199..219)
for (const b of DECBAR) drawSegBar(b.x, px(196), b.w, px(20), C.greenFill, C.greenEdge);
// hidden bottom-row bars y254..274 (parent 255..275)
for (const b of DECBAR) drawSegBar(b.x, px(254), b.w, px(20), C.hidFill, C.hidEdge);

// up-arrows y144..196, heads at top
for (const cx of DECCOL) {
  slide.addShape(pres.ShapeType.line, {
    x: cx, y: px(144), w: 0, h: px(52),
    line: { color: C.decInk, width: 1.75, beginArrowType: "triangle" },
  });
}

// o1 o2 o3 labels: ink y124..133 (parent 131..139) -> box y117 h24
for (let i = 0; i < 3; i++) {
  slide.addText(
    [
      { text: "o", options: { italic: true, fontSize: 17 } },
      { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
    ],
    {
      x: DECCOL[i] - 0.4, y: px(114), w: 0.8, h: px(24),
      align: "center", valign: "middle", margin: 0, fontFace: MATH, color: C.decInk,
    }
  );
}

// softmax labels: ink y167..181 (parent 171..184); right edges 548.5/683/817
const smRight = [px(548.5), px(683), px(817)];
for (let i = 0; i < 3; i++) {
  slide.addText("softmax", {
    x: smRight[i] - 1.4, y: px(164), w: 1.4, h: px(16),
    align: "right", valign: "middle", margin: 0,
    fontFace: MATH, fontSize: 18.5, italic: true, color: C.decInk,
  });
}

// down-arrows y217..254, heads at bottom
for (const cx of DECCOL) {
  slide.addShape(pres.ShapeType.line, {
    x: cx, y: px(217), w: 0, h: px(37),
    line: { color: C.decInk, width: 1.75, endArrowType: "triangle" },
  });
}

// s-chain arrows [[600,651],[735,786],[870,901]] at y264
const sSpans = [[px(600), px(651)], [px(735), px(786)], [px(870), px(901)]];
for (const [x0, x1] of sSpans) {
  slide.addShape(pres.ShapeType.line, {
    x: x0, y: px(264), w: x1 - x0, h: 0,
    line: { color: C.decInk, width: 1.75, endArrowType: "triangle" },
  });
}

// s1 s2 s3 labels: ink centers 621.5/757/892 (+1.5 italic lean)
const sCx = [px(623), px(758.5), px(893.5)];
for (let i = 0; i < 3; i++) {
  slide.addText(
    [
      { text: "s", options: { italic: true, fontSize: 17 } },
      { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
    ],
    {
      x: sCx[i] - 0.4, y: px(266), w: 0.8, h: px(19),
      align: "center", valign: "middle", margin: 0, fontFace: MATH, color: C.decInk,
    }
  );
}

// recurrent hooks: regenerated 600dpi PNGs at the fanned columns
slide.addImage({ path: path.join(ASSETS, "curve_a10.png"), x: px(551), y: px(184), w: 1.4444, h: 1.0139 });
slide.addImage({ path: path.join(ASSETS, "curve_b10.png"), x: px(685), y: px(184), w: 1.4444, h: 1.0139 });
// small diagonal tails under hidden bars 2 and 3 (parent pattern, +4.5/+8 shift)
slide.addShape(pres.ShapeType.line, {
  x: px(657.5), y: px(276), w: px(16), h: px(15), line: { color: C.decInk, width: 1.5 },
});
slide.addShape(pres.ShapeType.line, {
  x: px(792), y: px(276), w: px(16), h: px(15), line: { color: C.decInk, width: 1.5 },
});

// ---- 5) encoder content (slide-010 geometry) -----------------------------------
// pink top-row bars y321..341 (parent 319..338)
for (const b of ENCBAR) drawSegBar(b.x, px(321), b.w, px(20), C.pinkFill, C.pinkEdge);
// tan bottom-row bars y411..432 (parent 406..425)
for (const b of ENCBAR) drawSegBar(b.x, px(411), b.w, px(21), C.tanFill, C.tanEdge);

// h1 h2 labels: ink centers 209/344, y316..329 -> box y310 h25
const hCx = [px(207), px(342)];
for (let i = 0; i < 2; i++) {
  slide.addText(
    [
      { text: "h", options: { italic: true, fontSize: 17 } },
      { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
    ],
    {
      x: hCx[i] - 0.4, y: px(310), w: 0.8, h: px(25),
      align: "center", valign: "middle", margin: 0, fontFace: MATH, color: C.encInk,
    }
  );
}

// h-chain arrows [[51,108],[196,243],[330,377]] at y331.5
const hSpans = [[px(51), px(108)], [px(196), px(243)], [px(330), px(377)]];
for (const [x0, x1] of hSpans) {
  slide.addShape(pres.ShapeType.line, {
    x: x0, y: px(331.5), w: x1 - x0, h: 0,
    line: { color: C.encInk, width: 1.75, endArrowType: "triangle" },
  });
}

// embedding up-arrows y346..407, heads at top
for (const cx of ENCCOL) {
  slide.addShape(pres.ShapeType.line, {
    x: cx, y: px(346), w: 0, h: px(61),
    line: { color: C.encInk, width: 1.75, beginArrowType: "triangle" },
  });
}

// "embedding xN" labels: right-aligned, right edges 144/280/414, ink y369..383
const embRight = [px(144), px(280), px(414)];
for (let i = 0; i < 3; i++) {
  slide.addText(
    [
      { text: "embedding x", options: { italic: true, fontSize: 17.5 } },
      { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
    ],
    {
      x: embRight[i] - 1.6, y: px(366), w: 1.6, h: px(17),
      align: "right", valign: "middle", margin: 0, fontFace: MATH, color: C.encInk,
    }
  );
}

// '+' glyph between the first two embedding labels (measured center 210,401)
slide.addShape(pres.ShapeType.line, {
  x: px(210), y: px(394), w: 0, h: px(14), line: { color: C.encInk, width: 1.75 },
});
slide.addShape(pres.ShapeType.line, {
  x: px(204), y: px(401), w: px(13), h: 0, line: { color: C.encInk, width: 1.75 },
});

// x up-arrows y436..479, heads at top
for (const cx of ENCCOL) {
  slide.addShape(pres.ShapeType.line, {
    x: cx, y: px(436), w: 0, h: px(43),
    line: { color: C.encInk, width: 1.75, beginArrowType: "triangle" },
  });
}

// x1 x2 x3 labels: ink centers 151.5/286/420.5, y484..493 -> box y478 h21
for (let i = 0; i < 3; i++) {
  slide.addText(
    [
      { text: "x", options: { italic: true, fontSize: 17 } },
      { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
    ],
    {
      x: ENCCOL[i] - 0.4, y: px(476), w: 0.8, h: px(21),
      align: "center", valign: "middle", margin: 0, fontFace: MATH, color: C.encInk,
    }
  );
}

// ---- 6) attention assembly ------------------------------------------------------
// left lavender box x109..469 y226..303
slide.addShape(pres.ShapeType.roundRect, {
  x: px(109), y: px(226), w: px(360), h: px(77), rectRadius: 0.1,
  fill: { color: D.boxFill }, line: { color: D.leftEdge, width: 1 },
});
// attention node (small rect, gray-lavender fill, dark italic label)
slide.addShape(pres.ShapeType.rect, {
  x: px(246), y: px(253), w: px(83), h: px(24),
  fill: { color: D.nodeFill }, line: { color: D.nodeEdge, width: 1 },
});
slide.addText("attention", {
  x: px(246), y: px(253), w: px(83), h: px(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: MATH, fontSize: 20, italic: true, color: D.nodeText,
});
// 3 thin lines converging at the node's bottom-center (287,278), heads at the top
slide.addShape(pres.ShapeType.line, {
  x: px(152), y: px(278), w: px(135), h: px(40), flipV: true,
  line: { color: D.lineDark, width: 1, endArrowType: "triangle" },
});
slide.addShape(pres.ShapeType.line, {
  x: px(287), y: px(278), w: 0, h: px(40),
  line: { color: D.lineDark, width: 1, beginArrowType: "triangle" },
});
slide.addShape(pres.ShapeType.line, {
  x: px(287), y: px(278), w: px(134), h: px(40),
  line: { color: D.lineDark, width: 1, beginArrowType: "triangle" },
});
// left caption "Attention" (ink x245..331 y203..216)
slide.addText("Attention", {
  x: px(208), y: px(200), w: px(160), h: px(18),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 19.5, bold: true, italic: true, color: D.blue,
});
// right lavender box x495..853 y292..341
slide.addShape(pres.ShapeType.roundRect, {
  x: px(495), y: px(292), w: px(358), h: px(49), rectRadius: 0.08,
  fill: { color: D.boxFill }, line: { color: D.rightEdge, width: 1 },
});
// dashed pink attention fan (single 600dpi asset; S-curve + 3 hooks)
slide.addImage({ path: path.join(ASSETS, "dash_fan.png"), x: px(328), y: px(172), w: 6.8889, h: 2.3333 });
// three olive up-arrowheads beneath the decoder's hidden bars (tips ~y277)
for (const hx of [557, 684, 820]) {
  slide.addShape(pres.ShapeType.line, {
    x: px(hx), y: px(277), w: 0, h: px(12),
    line: { color: C.decInk, width: 1.75, beginArrowType: "triangle" },
  });
}
// right caption "Attention" (ink x727..799 y346..358)
slide.addText("Attention", {
  x: px(683), y: px(343), w: px(160), h: px(18),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 16.5, bold: true, italic: true, color: D.blue,
});

// ---- 7) inherited context-vector treatment (arc + dots, certified pixels) ------
parent.renderBase(pres, slide, { chrome: false, only: ["ctx_arc", "dec_dot", "enc_dot"] });

// ---- 8) callouts + connectors + summary box -------------------------------------
// pink connector (bezier PNG): arc lower end -> pink callout's left edge
slide.addImage({ path: path.join(ASSETS, "pink_conn.png"), x: px(486), y: px(339), w: 1.0417, h: 0.7361 });
// pink callout: measured x558..839 y371..411 (parent's was y402..444 — moved up 30px)
slide.addShape(pres.ShapeType.rect, {
  x: px(558), y: px(371), w: px(281), h: px(40),
  fill: { color: D.calloutFill }, line: { color: C.red, width: 1 },
});
slide.addText("Context Vector (of Whole Inputs)", {
  x: px(558), y: px(371), w: px(281), h: px(40),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 15.5, bold: true, color: C.red,
});
// green callout: measured x68..351 y145..187
slide.addShape(pres.ShapeType.rect, {
  x: px(68), y: px(145), w: px(284), h: px(43),
  fill: { color: D.greenFill }, line: { color: D.greenEdge, width: 1 },
});
slide.addText("weighted sum of the hidden states", {
  x: px(68), y: px(145), w: px(284), h: px(43),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 15.5, bold: true, italic: true, color: D.blue,
});
// gray summary box: measured x521..902 y432..527
slide.addShape(pres.ShapeType.rect, {
  x: px(521), y: px(432), w: px(381), h: px(96),
  fill: { color: D.grayFill }, line: { color: D.grayEdge, width: 1 },
});
slide.addText("Decoder Utilizes:", {
  x: px(534), y: px(438), w: px(330), h: px(20),
  align: "left", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 19.5, bold: true, color: C.red,
});
slide.addShape(pres.ShapeType.ellipse, {
  x: px(533.25), y: px(469.75), w: px(6.5), h: px(6.5),
  fill: { color: D.bodyInk }, line: { type: "none" },
});
slide.addShape(pres.ShapeType.ellipse, {
  x: px(533.25), y: px(495.75), w: px(6.5), h: px(6.5),
  fill: { color: D.bodyInk }, line: { type: "none" },
});
slide.addText("Context Vector", {
  x: px(552), y: px(465), w: px(300), h: px(19),
  align: "left", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 18, color: D.bodyInk,
});
slide.addText("Weighted sum of hidden states", {
  x: px(552), y: px(490), w: px(340), h: px(22),
  align: "left", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 18, color: D.bodyInk,
});

// ---- 9) captions (shortened) + title (2 lines, red/blue) ------------------------
slide.addText("Decoder", {
  x: px(648), y: px(87), w: px(160), h: px(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 20.5, bold: true, italic: true, color: C.red,
});
slide.addText("Encoder", {
  x: px(182.5), y: px(505), w: px(160), h: px(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 20.5, bold: true, italic: true, color: C.red,
});
// title line 1: ink x244..688 y59..81; "RNN  Seq2Seq model " red + "[with Attention]" blue
slide.addText(
  [
    { text: "RNN  Seq2Seq model ", options: { color: C.red } },
    { text: "[with Attention]", options: { color: D.blue } },
  ],
  {
    x: px(216), y: px(52), w: px(500), h: px(30),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 25.25, bold: true,
  }
);
// title line 2 (subtitle): all blue, underline ONLY under "Bottleneck" (measured x433..535)
slide.addText(
  [
    { text: "[ To overcome ", options: {} },
    { text: "Bottleneck", options: { underline: { style: "sng" } } },
    { text: " challenge]", options: {} },
  ],
  {
    x: px(215.5), y: px(80), w: px(500), h: px(26),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 20, bold: true, color: D.blue,
  }
);

// ---- output (SINGLE-VERSION law: one plain-named deliverable) -------------------
const OUT = path.join(__dirname, "..", "slide_010_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
