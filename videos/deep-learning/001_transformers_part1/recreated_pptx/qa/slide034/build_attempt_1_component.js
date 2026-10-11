// components/slide_034.js — slide 034 "Self Attention Mechanism
// (Embedding Vector Dimension and Softmax Sensitivity)" composition.
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slide 35 ("Scale down Weights"
// blue box) builds on this composition. It MUST require() this module and call
// renderBase(pptx, slide, opts) (or cherry-pick blocks) — NEVER re-derive or
// copy-paste this geometry.
//
// Block granularity: every visual block is its own function; renderBase accepts
//   opts.skip   — array of block names to OMIT
//   opts.only   — array of block names to DRAW exclusively
//   opts.chrome — draw house chrome (default true; via components/house_chrome.js)
//   opts.numeral— badge numeral (default 34)
// Block names: chrome, title, subtitle, concept_box, concept_eq_large, concept_xi,
//   concept_dup, concept_uparrow, concept_eq_small, concept_annot, panel,
//   header_emb, header_softmax, header_eq, header_warning, col_headers,
//   col_inputs, col_arrows, col_outputs, col_captions.
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_034.jpg (960x540,
// 1px = 1pt, in = px/72) — scanline runs, color-class maps, ink component bboxes
// (scratch/slide034/measure*.py). Equations are 600dpi transparent STIX-mathtext
// PNGs embedded at exact sidecar size (ink-left/baseline placement law); the tall
// stack parens use the delimiters-stretched-glyph pattern; the softmax fraction is
// composed from wij/exp/exp2 PNGs + a native line bar to match the original's
// tight proportions.
//
// LAWS honored: playlist chrome via shared module (drawn once here); verbatim text
// incl. quoted "d"/"w" runs; margin:0 + fontFace everywhere; explicit lineSpacing on
// the multi-line annotation; no '#' in hex; mouse-cursor artifact omitted.

const fs = require("fs");
const path = require("path");
const { drawHouseChrome } = require(path.join(__dirname, "house_chrome.js"));

const ASSETS = path.join(__dirname, "..", "assets");

// ---- palette (measured cores; video-compression reconciled with the validated spec)
const C = {
  ink: "000000",
  red: "990000",        // block arrows, parens, input borders, emb-box border, [X_i], "SoftMax", annot red
  subRed: "FF0000",     // subtitle "(Embedding", " and ", ")"
  blue: "0000CC",       // annotation text, warning text + border
  outBlue: "0033CC",    // output box borders + blue parens
  greenDark: "008000",  // "d" letters, green 1xd subscripts
  greenArrow: "00A500", // arrow glyphs (up/down), green block arrow
  boxGreen: "00A651",   // concept box outline
  yellowHL: "FFFF00",   // subtitle + annotation "d" highlight
  orangeHL: "FFA500",   // SoftMax arrow labels + annotation highlight
  orangeTxt: "FFA500",
  fillYellow: "FFFFCC", // input value boxes
  peach: "FCE4D4",      // demo panel fill
  eqBorder: "808080",   // white equation-box borders
};
const SANS = "Arial";
const px = (v) => v / 72;

// ---- asset helpers -----------------------------------------------------------
const sideCache = {};
function side(name) {
  if (!sideCache[name]) {
    sideCache[name] = JSON.parse(fs.readFileSync(path.join(ASSETS, name.replace(/\.png$/, ".json")), "utf8"));
  }
  return sideCache[name];
}
// place a 600dpi equation PNG so its INK top-left lands at (inkX, inkY) pt-units
// (the renderer pads the tight crop by 8px@600 = 2px@150 on every side)
function imgInk(slide, name, inkX, inkY) {
  const s = side(name);
  slide.addImage({
    path: path.join(ASSETS, name),
    x: px(inkX - 2), y: px(inkY - 2), w: s.w_in, h: s.h_in,
  });
}
// place by math BASELINE (alignment law): y_img = baseline_pt/72 - baseline_frac*h_in
function imgBase(slide, name, inkX, baselinePt) {
  const s = side(name);
  slide.addImage({
    path: path.join(ASSETS, name),
    x: px(inkX - 2), y: px(baselinePt) - s.baseline_frac * s.h_in, w: s.w_in, h: s.h_in,
  });
}
// stretched-glyph parens: tight crop, place ink top-left exactly
function paren(slide, name, inkX, inkY) {
  const s = side(name);
  slide.addImage({ path: path.join(ASSETS, name), x: px(inkX), y: px(inkY), w: s.w_in, h: s.h_in });
}

// ---- block functions ---------------------------------------------------------

function drawTitle(pptx, slide) {
  // ink measured x 371..613, y 57..72 (center 492)
  slide.addText("Self Attention Mechanism", {
    x: px(242), y: px(51), w: px(500), h: px(27),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 20, bold: true, color: C.ink,
  });
}

function drawSubtitle(pptx, slide) {
  // ink x 232..771, y 79..98; yellow highlight blocks x 351..522 and x 558..762 (y 77..99)
  slide.addText(
    [
      { text: "(Embedding ", options: { color: C.subRed } },
      { text: "Vector Dimension", options: { color: C.ink, highlight: C.yellowHL } },
      { text: " and ", options: { color: C.subRed } },
      { text: "Softmax Sensitivity", options: { color: C.ink, highlight: C.yellowHL } },
      { text: ")", options: { color: C.subRed } },
    ],
    {
      x: px(145), y: px(72), w: px(700), h: px(30),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 20.5, bold: true,
    }
  );
}

function drawConceptBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(47), y: px(103), w: px(346), h: px(166), rectRadius: 0.08,
    fill: { color: "FFFFFF" }, line: { color: C.boxGreen, width: 1.25 },
  });
}

function drawConceptEqLarge(pptx, slide) {
  // white eq box x 69..193, y 115..157; eq ink x 81..179, y 122..148
  slide.addShape(pptx.ShapeType.rect, {
    x: px(69), y: px(115), w: px(124), h: px(42),
    fill: { color: "FFFFFF" }, line: { color: C.eqBorder, width: 1 },
  });
  imgInk(slide, "eq34_large.png", 81, 121);
}

function drawConceptXi(pptx, slide) {
  // [X_i] with green 1xd subscript: brackets ink x 311..317 / 340..346, y 118..162;
  // X ink x 318..334 (cap 18px, baseline 145), subscript i ink x 331..335 y 146..153;
  // subscript "1xd" ink x 346..363, y 156..165
  imgInk(slide, "eq34_bracket_l.png", 311, 118);
  imgBase(slide, "eq34_xonly.png", 318, 145);
  imgBase(slide, "eq34_isub.png", 331, 153);
  imgInk(slide, "eq34_bracket_r.png", 340, 118);
  slide.addText("1×d", {
    x: px(344), y: px(150), w: px(34), h: px(19),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 14, color: C.greenDark,
  });
}

function drawConceptDup(pptx, slide) {
  // "d" ink x 62..73 y 184..198 + thin up-arrow ink x 77..92, y 177..205
  slide.addText("d", {
    x: px(58), y: px(180), w: px(20), h: px(21),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 15, bold: true, color: C.greenDark,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(84.5), y: px(178), w: 0, h: px(26),
    line: { color: C.greenArrow, width: 4.5, beginArrowType: "triangle" },
  });
}

function drawConceptUparrow(pptx, slide) {
  // green block up-arrow ink x 207..222, y 176..206
  slide.addShape(pptx.ShapeType.upArrow, {
    x: px(206), y: px(176), w: px(16), h: px(30),
    fill: { color: C.greenArrow }, line: { type: "none" },
  });
}

function drawConceptEqSmall(pptx, slide) {
  // white eq box x 228..355, y 176..206; eq ink x 243..302, y 184..200
  slide.addShape(pptx.ShapeType.rect, {
    x: px(228), y: px(176), w: px(127), h: px(30),
    fill: { color: "FFFFFF" }, line: { color: C.eqBorder, width: 1 },
  });
  imgInk(slide, "eq34_small.png", 243, 184);
}

function drawConceptAnnot(pptx, slide) {
  // VISION-READ (qa/slide034/annot_read_1.txt): both lines bold ITALIC navy; line1 =
  // 'As Dimension of Embedding "d" Increases' with the trailing span '"d" Increases' on a
  // yellow highlight ("d" itself red); line2 = 'the Calculated weight value "w" increases'
  // with '"w" increases' red on an orange highlight. Width fitting: line1 ~16pt, line2 14pt.
  slide.addText(
    [
      { text: "As Dimension of Embedding ", options: { color: C.blue } },
      { text: "\"d\"", options: { color: C.red, highlight: C.yellowHL } },
      { text: " Increases", options: { color: C.blue, highlight: C.yellowHL } },
    ],
    {
      x: px(68), y: px(220), w: px(310), h: px(21),
      align: "left", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 14, bold: true, italic: true,
    }
  );
  slide.addText(
    [
      { text: "the Calculated weight value ", options: { color: C.blue } },
      { text: "\"w\" increases", options: { color: C.red, highlight: C.orangeHL } },
    ],
    {
      x: px(76), y: px(238.5), w: px(310), h: px(20),
      align: "left", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 14, bold: true, italic: true,
    }
  );
}

function drawPanel(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(48), y: px(276), w: px(820), h: px(254), rectRadius: 0.12,
    fill: { color: C.peach }, line: { type: "none" },
  });
}

function drawHeaderEmb(pptx, slide) {
  // white box red border x 52..127, y 282..347; red brackets ink x 57..58 / 87..88,
  // y 288..319; X ink x 60..86 (baseline ~305); green "1xd" ink x 91..121, y 322..337
  slide.addShape(pptx.ShapeType.rect, {
    x: px(52), y: px(282), w: px(75), h: px(65),
    fill: { color: "FFFFFF" }, line: { color: C.red, width: 1.5 },
  });
  imgInk(slide, "eq34_bracket_l_sm.png", 56, 288);
  imgBase(slide, "eq34_xonly_sm.png", 64, 306);
  imgBase(slide, "eq34_isub_sm.png", 78, 306);
  imgInk(slide, "eq34_bracket_r_sm.png", 86, 288);
  slide.addText("1×d", {
    x: px(91), y: px(317), w: px(38), h: px(20),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 14, color: C.greenDark,
  });
}

function drawHeaderSoftmax(pptx, slide) {
  // "SoftMax" ink x 174..240, y 301..316
  slide.addText("SoftMax", {
    x: px(167), y: px(297), w: px(80), h: px(24),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 16.5, bold: true, color: C.red,
  });
}

function drawHeaderEq(pptx, slide) {
  // white eq box x 247..391, y 281..341. LHS w_ij= ink x 260..300 (baseline ~315);
  // bar x 304..384 y 310.5; numerator ink x 320..372 y 288..307; denominator ink x 308..386 y 317..338
  slide.addShape(pptx.ShapeType.rect, {
    x: px(247), y: px(281), w: px(144), h: px(60),
    fill: { color: "FFFFFF" }, line: { color: C.eqBorder, width: 1 },
  });
  imgBase(slide, "eq34_wij.png", 259, 315);
  imgInk(slide, "eq34_exp1.png", 320, 287);
  slide.addShape(pptx.ShapeType.line, {
    x: px(304), y: px(311), w: px(80), h: 0,
    line: { color: C.ink, width: 1.5 },
  });
  imgInk(slide, "eq34_exp2.png", 307, 316);
}

function drawHeaderWarning(pptx, slide) {
  // white strip x 378..864, y 284..315, thin blue border; bold italic blue text
  slide.addShape(pptx.ShapeType.rect, {
    x: px(378), y: px(284), w: px(486), h: px(31),
    fill: { color: "FFFFFF" }, line: { color: C.blue, width: 1 },
  });
  slide.addText("High Weight Values kill the gradient, and slow down learning", {
    x: px(425), y: px(282), w: px(445), h: px(31),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 14.3, bold: true, italic: true, color: C.blue,
  });
}

// three demo columns: input-stack left paren, boxes, right paren / arrows / outputs
const COLS = [
  { // column 1 — small d
    inParenL: 129, inParenR: 168, inBoxX: 134,
    outParenL: 250, outParenR: 308, outBoxX: 256,
    arrowX: 179, labelX: 166, dTextX: 132, headerArrowX: 158.5, headerArrowY: [323, 351], headerDir: "down",
    captionEqX: 137, captionTxtX: 183, captionWBase: 511,
  },
  { // column 2 — medium d
    inParenL: 398, inParenR: 438, inBoxX: 403,
    outParenL: 519, outParenR: 576, outBoxX: 524,
    arrowX: 448, labelX: 434, dTextX: 396, headerArrowX: 422.5, headerArrowY: [320, 348], headerDir: "up",
    captionEqX: 406, captionTxtX: 446, captionWBase: 513,
  },
  { // column 3 — large d
    inParenL: 666, inParenR: 706, inBoxX: 671,
    outParenL: 787, outParenR: 844, outBoxX: 792,
    arrowX: 716, labelX: 702, dTextX: 668, headerArrowX: 703, headerArrowY: [321, 348], headerDir: "double",
    captionEqX: 677, captionTxtX: 719, captionWBase: 514,
  },
];
const INPUT_VALS = [["1", "2", "3", "4"], ["5", "10", "15", "20"], ["10", "20", "30", "40"]];
const OUTPUT_VALS = [
  ["0.0321", "0.0871", "0.2369", "0.6439"],
  ["0.0000", "0.0000", "0.0067", "0.9933"],
  ["0.0000", "0.0000", "0.0000", "1.0000"],
];
const IN_ROWS = [369, 395, 429, 460];   // input box y-tops, h 17
const OUT_ROWS = [369, 398, 428, 459];    // output box y-tops, h 17

function drawColHeaders(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    const col = COLS[i];
    slide.addText("d", {
      x: px(col.dTextX), y: px(330), w: px(20), h: px(19),
      align: "left", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 15, bold: true, color: C.greenDark,
    });
    const [y0, y1] = col.headerArrowY;
    if (col.headerDir === "down") {
      slide.addShape(pptx.ShapeType.line, {
        x: px(col.headerArrowX), y: px(y0), w: 0, h: px(y1 - y0),
        line: { color: C.greenArrow, width: 4, endArrowType: "triangle" },
      });
    } else if (col.headerDir === "up") {
      slide.addShape(pptx.ShapeType.line, {
        x: px(col.headerArrowX), y: px(y0), w: 0, h: px(y1 - y0),
        line: { color: C.greenArrow, width: 4, beginArrowType: "triangle" },
      });
    } else {
      // d up-up: two parallel thin up arrows
      slide.addShape(pptx.ShapeType.line, {
        x: px(col.headerArrowX - 8), y: px(y0), w: 0, h: px(y1 - y0),
        line: { color: C.greenArrow, width: 4, beginArrowType: "triangle" },
      });
      slide.addShape(pptx.ShapeType.line, {
        x: px(col.headerArrowX + 8), y: px(y0), w: 0, h: px(y1 - y0),
        line: { color: C.greenArrow, width: 4, beginArrowType: "triangle" },
      });
    }
  }
}

function drawColInputs(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    const col = COLS[i];
    paren(slide, "paren_red_l.png", col.inParenL, 361);
    paren(slide, "paren_red_r.png", col.inParenR, 361);
    for (let k = 0; k < 4; k++) {
      slide.addShape(pptx.ShapeType.roundRect, {
        x: px(col.inBoxX), y: px(IN_ROWS[k]), w: px(32), h: px(17), rectRadius: 0.035,
        fill: { color: C.fillYellow }, line: { color: C.red, width: 1 },
      });
      slide.addText(INPUT_VALS[i][k], {
        x: px(col.inBoxX), y: px(IN_ROWS[k]), w: px(32), h: px(17),
        align: "center", valign: "middle", margin: 0,
        fontFace: SANS, fontSize: 12, bold: true, color: C.ink,
      });
    }
  }
}

function drawColArrows(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    const col = COLS[i];
    // thick red block arrow ink x..x+63, y 422..437
    slide.addShape(pptx.ShapeType.rightArrow, {
      x: px(col.arrowX), y: px(422), w: px(63), h: px(15),
      fill: { color: C.red }, line: { type: "none" },
    });
    // orange SoftMax label centered above the arrow
    slide.addText("SoftMax", {
      x: px(col.labelX), y: px(400), w: px(80), h: px(21),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 14, bold: true, color: C.orangeTxt,
    });
  }
}

function drawColOutputs(pptx, slide) {
  for (let i = 0; i < 3; i++) {
    const col = COLS[i];
    paren(slide, "paren_blue_l.png", col.outParenL, 365);
    paren(slide, "paren_blue_r.png", col.outParenR, 365);
    for (let k = 0; k < 4; k++) {
      slide.addShape(pptx.ShapeType.roundRect, {
        x: px(col.outBoxX), y: px(OUT_ROWS[k]), w: px(47), h: px(17), rectRadius: 0.035,
        fill: { color: "FFFFFF" }, line: { color: C.outBlue, width: 1 },
      });
      slide.addText(OUTPUT_VALS[i][k], {
        x: px(col.outBoxX), y: px(OUT_ROWS[k]), w: px(47), h: px(17),
        align: "center", valign: "middle", margin: 0,
        fontFace: SANS, fontSize: 11, bold: true, color: C.ink,
      });
    }
  }
}

function drawColCaptions(pptx, slide) {
  // measured: big italic w (ink ~14x12, baseline col-specific) + small '{ij}' beside it,
  // then the black caption text; e.g. col1 w ink x 137..150 y 499..511, 'ij 152..164
  const txt = ["For small \"d\"", "For medium \"d\"", "For large \"d\""];
  for (let i = 0; i < 3; i++) {
    const col = COLS[i];
    imgBase(slide, "eq34_w.png", col.captionEqX, col.captionWBase);
    imgBase(slide, "eq34_prij.png", col.captionEqX + 15, col.captionWBase - 1);
    slide.addText(txt[i], {
      x: px(col.captionTxtX), y: px(col.captionWBase - 17), w: px(140), h: px(19),
      align: "left", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 13, bold: false, color: C.ink,
    });
  }
}

// ---- composition -------------------------------------------------------------

const BLOCKS = {
  title: drawTitle,
  subtitle: drawSubtitle,
  concept_box: drawConceptBox,
  concept_eq_large: drawConceptEqLarge,
  concept_xi: drawConceptXi,
  concept_dup: drawConceptDup,
  concept_uparrow: drawConceptUparrow,
  concept_eq_small: drawConceptEqSmall,
  concept_annot: drawConceptAnnot,
  panel: drawPanel,
  header_emb: drawHeaderEmb,
  header_softmax: drawHeaderSoftmax,
  header_eq: drawHeaderEq,
  header_warning: drawHeaderWarning,
  col_headers: drawColHeaders,
  col_inputs: drawColInputs,
  col_arrows: drawColArrows,
  col_outputs: drawColOutputs,
  col_captions: drawColCaptions,
};

/**
 * Draw the full slide-034 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 34 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px, COLS, IN_ROWS, OUT_ROWS };
