// components/slide_006.js — slide 006 "Traditional RNN  Seq2Seq model" certified composition.
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slides 7, 8, 9, 10 build on this
// composition. They MUST require() this module and call renderBase(pptx, slide, opts)
// (or cherry-pick blocks) — NEVER re-derive or copy-paste this geometry.
//
// Block granularity: every visual block is its own function; renderBase accepts
//   opts.skip   — array of block names to OMIT (child removes inherited blocks)
//   opts.only   — array of block names to DRAW exclusively (child replaces composition)
//   opts.chrome — draw house chrome (default true; chrome via components/house_chrome.js)
//   opts.numeral— badge numeral (default 6)
// Block names: chrome, title, dec_container, dec_olabels, dec_uparrows, dec_softmax,
//   dec_green_bars, dec_downarrows, dec_hidden_bars, dec_sarrows, dec_slabels,
//   dec_feedback, dec_dot, enc_container, enc_pink_bars, enc_hlabels, enc_harrows,
//   enc_embarrows, enc_emblabels, enc_tan_bars, enc_xarrows, enc_xlabels, enc_dot,
//   ctx_arc, leader, callout, dec_caption, enc_caption.
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_006.jpg (960x540, 1px=1pt,
// in = px/72) — scanline runs, exact color modes, ink component bboxes (scratch/slide006/
// measure*.py). Curves are 600dpi transparent PNGs (matplotlib quadratic beziers) embedded
// at exact size; all straight arrows are native LINE shapes with triangle heads.
//
// LAWS honored: playlist chrome (videos/deep-learning/AGENTS.md) via shared module;
// verbatim text incl. double spaces ("Traditional RNN  Seq2Seq model", "Encoder  (RNN)");
// true subscripts via smaller subscript runs; margin:0 + explicit fontFace everywhere;
// no '#' in hex; mouse-cursor artifact omitted.

const path = require("path");
const { drawHouseChrome } = require(path.join(__dirname, "house_chrome.js"));

const ASSETS = path.join(__dirname, "..", "assets");

// ---- palette (JPEG-core measured) -------------------------------------------
const C = {
  red: "A0000E",          // title/captions/callout/arc/dots/leader (cores ~#9d0f1d..#a9000b)
  decInk: "9EA828",       // decoder arrows/labels/curves (olive-yellow cores ~#9ca724)
  encInk: "8F6E44",       // encoder arrows/labels (olive-brown cores ~#8a6740)
  decFill: "FDFF85", decEdge: "E6E17C",
  greenFill: "E8FF6E", greenEdge: "C2D64A",
  hidFill: "FAEC69", hidEdge: "C2C744",
  encFill: "F8D5AD", encEdge: "E6C7A2",
  pinkFill: "F2C7A7", pinkEdge: "C29F77",
  tanFill: "F9D5A3", tanEdge: "C9A87B",
  calloutFill: "F6DCDD",
};
const SANS = "Arial";
const MATH = "Times New Roman";

const px = (v) => v / 72;

// ---- block functions ---------------------------------------------------------

function drawTitle(pptx, slide) {
  slide.addText("Traditional RNN  Seq2Seq model", {
    x: px(252.5), y: px(54.5), w: px(400), h: px(30),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 24, bold: true, color: C.red,
  });
}

function drawDecContainer(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(479), y: px(117), w: px(423), h: px(165), rectRadius: 0.12,
    fill: { color: C.decFill }, line: { color: C.decEdge, width: 0.75 },
  });
}

// three decoder time-step columns share one x-pitch: centers 554 / 685 / 815.5
const DECCOL = [px(554), px(685), px(815.5)];
const DECBAR = [
  { x: px(516), w: px(77) }, { x: px(647), w: px(77) }, { x: px(778), w: px(77) },
];

function drawDecOlabels(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    slide.addText(
      [
        { text: "o", options: { italic: true, fontSize: 17 } },
        { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
      ],
      {
        x: DECCOL[i] - 0.4, y: px(123), w: 0.8, h: px(24),
        align: "center", valign: "middle", margin: 0,
        fontFace: MATH, color: C.decInk,
      }
    );
  }
}

function drawDecUparrows(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.ShapeType.line, {
      x: DECCOL[i], y: px(146), w: 0, h: px(52), // 146..198, head at top
      line: { color: C.decInk, width: 1.75, beginArrowType: "triangle" },
    });
  }
}

function drawDecSoftmax(pptx, slide) {
  const right = [px(546), px(677), px(807.5)];
  for (let i = 0; i < 3; i++) {
    slide.addText("softmax", {
      x: right[i] - 1.4, y: px(170), w: 1.4, h: px(16),
      align: "right", valign: "middle", margin: 0,
      fontFace: MATH, fontSize: 17, italic: true, color: C.decInk,
    });
  }
}

function drawSegBar(pptx, slide, x, y, w, h, fill, edge) {
  slide.addShape(pptx.ShapeType.rect, {
    x, y, w, h, fill: { color: fill }, line: { color: edge, width: 1 },
  });
  for (let k = 1; k <= 3; k++) {
    slide.addShape(pptx.ShapeType.line, {
      x: x + (w * k) / 4, y, w: 0, h,
      line: { color: edge, width: 1 },
    });
  }
}

function drawDecGreenBars(pptx, slide) {
  for (const b of DECBAR) drawSegBar(pptx, slide, b.x, px(199), b.w, px(20), C.greenFill, C.greenEdge);
}

function drawDecDownarrows(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.ShapeType.line, {
      x: DECCOL[i], y: px(219), w: 0, h: px(35), // 219..254, head at bottom
      line: { color: C.decInk, width: 1.75, endArrowType: "triangle" },
    });
  }
}

function drawDecHiddenBars(pptx, slide) {
  for (const b of DECBAR) drawSegBar(pptx, slide, b.x, px(255), b.w, px(20), C.hidFill, C.hidEdge);
}

function drawDecSarrows(pptx, slide) {
  const spans = [
    [px(597), px(648)], [px(728), px(779)], [px(860), px(900)],
  ];
  for (const [x0, x1] of spans) {
    slide.addShape(pptx.ShapeType.line, {
      x: x0, y: px(264.5), w: x1 - x0, h: 0,
      line: { color: C.decInk, width: 1.75, endArrowType: "triangle" },
    });
  }
}

function drawDecSlabels(pptx, slide) {
  const cx = [px(619.5), px(750), px(881)];
  for (let i = 0; i < 3; i++) {
    slide.addText(
      [
        { text: "s", options: { italic: true, fontSize: 17 } },
        { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
      ],
      {
        x: cx[i] - 0.4, y: px(268), w: 0.8, h: px(19),
        align: "center", valign: "middle", margin: 0,
        fontFace: MATH, color: C.decInk,
      }
    );
  }
}

function drawDecFeedback(pptx, slide) {
  // recurrent sweeps: 600dpi PNG bezier arcs from col i up-arrow into cell i+1 top edge
  slide.addImage({ path: path.join(ASSETS, "curve_a.png"), x: px(550), y: px(183), w: px(101), h: px(76) });
  slide.addImage({ path: path.join(ASSETS, "curve_b.png"), x: px(681), y: px(183), w: px(101), h: px(76) });
  // small diagonal tails under hidden bars 2 and 3 (measured 653,276 -> 669,291 etc.)
  slide.addShape(pptx.ShapeType.line, {
    x: px(653), y: px(276), w: px(16), h: px(15),
    line: { color: C.decInk, width: 1.5 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(784), y: px(276), w: px(16), h: px(15),
    line: { color: C.decInk, width: 1.5 },
  });
}

function drawDecDot(pptx, slide) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(510.5), y: px(259.5), w: px(6), h: px(6),
    fill: { color: C.red }, line: { type: "none" },
  });
}

function drawEncContainer(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(46), y: px(306), w: px(442), h: px(190), rectRadius: 0.15,
    fill: { color: C.encFill }, line: { color: C.encEdge, width: 0.75 },
  });
}

const ENCBAR = [
  { x: px(123), w: px(77) }, { x: px(253), w: px(77) }, { x: px(384), w: px(77) },
];
const ENCCOL = [px(161), px(291.5), px(422.5)];

function drawEncPinkBars(pptx, slide) {
  for (const b of ENCBAR) drawSegBar(pptx, slide, b.x, px(319), b.w, px(20), C.pinkFill, C.pinkEdge);
}

function drawEncHlabels(pptx, slide) {
  const cx = [px(217.5), px(349)];
  for (let i = 0; i < 2; i++) {
    slide.addText(
      [
        { text: "h", options: { italic: true, fontSize: 17 } },
        { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
      ],
      {
        x: cx[i] - 0.4, y: px(307), w: 0.8, h: px(25),
        align: "center", valign: "middle", margin: 0,
        fontFace: MATH, color: C.encInk,
      }
    );
  }
}

function drawEncHarrows(pptx, slide) {
  const spans = [
    [px(63), px(119)],   // unlabeled entry arrow from container left area
    [px(204), px(251)],  // h1
    [px(335), px(382)],  // h2
  ];
  for (const [x0, x1] of spans) {
    slide.addShape(pptx.ShapeType.line, {
      x: x0, y: px(329.5), w: x1 - x0, h: 0,
      line: { color: C.encInk, width: 1.75, endArrowType: "triangle" },
    });
  }
}

function drawEncEmbarrows(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.ShapeType.line, {
      x: ENCCOL[i], y: px(342), w: 0, h: px(60), // 342..402, head at top
      line: { color: C.encInk, width: 1.75, beginArrowType: "triangle" },
    });
  }
}

function drawEncEmblabels(pptx, slide) {
  const right = [px(152.5), px(284.5), px(415.5)];
  for (let i = 0; i < 3; i++) {
    slide.addText(
      [
        { text: "embedding x", options: { italic: true, fontSize: 17 } },
        { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
      ],
      {
        x: right[i] - 1.6, y: px(362), w: 1.6, h: px(17),
        align: "right", valign: "middle", margin: 0,
        fontFace: MATH, color: C.encInk,
      }
    );
  }
}

function drawEncTanBars(pptx, slide) {
  for (const b of ENCBAR) drawSegBar(pptx, slide, b.x, px(406), b.w, px(19), C.tanFill, C.tanEdge);
}

function drawEncXarrows(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    slide.addShape(pptx.ShapeType.line, {
      x: ENCCOL[i], y: px(428), w: 0, h: px(42), // 428..470, head at top
      line: { color: C.encInk, width: 1.75, beginArrowType: "triangle" },
    });
  }
}

function drawEncXlabels(pptx, slide) {
  const cx = [px(159.5), px(290.5), px(421.5)];
  for (let i = 0; i < 3; i++) {
    slide.addText(
      [
        { text: "x", options: { italic: true, fontSize: 17 } },
        { text: String(i + 1), options: { italic: true, fontSize: 12, subscript: true } },
      ],
      {
        x: cx[i] - 0.4, y: px(468), w: 0.8, h: px(21),
        align: "center", valign: "middle", margin: 0,
        fontFace: MATH, color: C.encInk,
      }
    );
  }
}

function drawEncDot(pptx, slide) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(466), y: px(323.5), w: px(6), h: px(6),
    fill: { color: C.red }, line: { type: "none" },
  });
}

function drawCtxArc(pptx, slide) {
  // red curved context-vector arrow encoder-dot -> decoder-dot (600dpi PNG with head wedge)
  slide.addImage({ path: path.join(ASSETS, "ctx_arc.png"), x: px(464), y: px(257), w: px(48), h: px(73) });
}

function drawLeader(pptx, slide) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(470), y: px(330), w: px(88), h: px(72),
    line: { color: C.red, width: 1 },
  });
}

function drawCallout(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(557), y: px(402), w: px(282), h: px(42),
    fill: { color: C.calloutFill }, line: { color: C.red, width: 1 },
  });
  slide.addText("Context Vector (of Whole Inputs)", {
    x: px(557), y: px(402), w: px(282), h: px(42),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 15.5, bold: true, color: C.red,
  });
}

function drawDecCaption(pptx, slide) {
  slide.addText("Decoder (RNN)", {
    x: px(672), y: px(87), w: px(160), h: px(24),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 20.5, bold: true, italic: true, color: C.red,
  });
}

function drawEncCaption(pptx, slide) {
  slide.addText("Encoder  (RNN)", {
    x: px(215.5), y: px(505), w: px(160), h: px(24),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 20.5, bold: true, italic: true, color: C.red,
  });
}

// ---- composition -------------------------------------------------------------

const BLOCKS = {
  title: drawTitle,
  dec_container: drawDecContainer,
  dec_olabels: drawDecOlabels,
  dec_uparrows: drawDecUparrows,
  dec_softmax: drawDecSoftmax,
  dec_green_bars: drawDecGreenBars,
  dec_downarrows: drawDecDownarrows,
  dec_hidden_bars: drawDecHiddenBars,
  dec_sarrows: drawDecSarrows,
  dec_slabels: drawDecSlabels,
  dec_feedback: drawDecFeedback,
  dec_dot: drawDecDot,
  enc_container: drawEncContainer,
  enc_pink_bars: drawEncPinkBars,
  enc_hlabels: drawEncHlabels,
  enc_harrows: drawEncHarrows,
  enc_embarrows: drawEncEmbarrows,
  enc_emblabels: drawEncEmblabels,
  enc_tan_bars: drawEncTanBars,
  enc_xarrows: drawEncXarrows,
  enc_xlabels: drawEncXlabels,
  enc_dot: drawEncDot,
  ctx_arc: drawCtxArc,
  leader: drawLeader,
  callout: drawCallout,
  dec_caption: drawDecCaption,
  enc_caption: drawEncCaption,
};

/**
 * Draw the full slide-006 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 6 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px, GEO: { DECCOL, DECBAR, ENCCOL, ENCBAR } };
