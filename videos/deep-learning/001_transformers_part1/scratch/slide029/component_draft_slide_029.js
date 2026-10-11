// components/slide_029.js — CERTIFIED-CANDIDATE composition of slide 29
// "Self Attention Mechanism (as Query and {Key-Value} Dictionary)" (Deep Learning
// DSAI 308, Transformers Part I). Built by the slide-029 build worker, 2026-10-11.
//
// DEPENDENCY CONTRACT (references/dependencies.md): this module is the shared base for
// dependent slide 30 (30<-29). It composes the CERTIFIED slide-026 component
// (renderBase, blocks canvas/dotProduct/stackLeft/softmax/sigma/flowLines/arrowsGreen/
// yOutput/stackRight/strip — slide 29's frame drops the parent's title/labels/
// queryArrows/feedCurves) and adds slide 29's own delta blocks at THIS frame's measured
// geometry. renderBase(pptx, slide, opts) with opts.skip / opts.only (arrays of delta
// block names; the inherited ten blocks are always drawn through the parent component).
// House chrome is NOT drawn here — the child build draws it ONCE via
// components/house_chrome.js.
//
// GEOMETRY PROVENANCE — PIL pixel forensics on unique_slides/slide_029.jpg (960x540,
// 1px = 1pt = 1/72 in): frame-diff vs slide_026.jpg + scanline/ASCII maps (scratch/
// slide029/, banked in qa/slide029/). All coordinates are frame pixels:
//   title L1 ink x163..770 y58..76 (20pt bold), SATURATED yellow FFFF00 highlight
//     x411..773 y53..78 (NOT the parent's pale FBF29B)
//   subtitle ink x108..826 y79..101 (20.5pt bold; closed-loop: 19.5pt rendered 5.6%
//     narrow); red 9E101E words = Query / X2 / Keys / Values ("All" is BLACK, core
//     000100 — spec's "All Keys red" corrected by the frame)
//   callout1 x315..490 y140..184: pale-cyan EDFBFB fill + dark-green 3B7A40 DASHED
//     border (dash cores 46785B/5D7B61); text 12pt bold italic CC00CC LEFT-aligned at
//     x326, pitch 15 ("Matched KEYS with" / "Relevance Percentage"), noun "KEYS" RED
//     C00000 (x384..420)
//   callout2 x634..846 y145..188: same style, text CENTER-aligned (both lines center
//     x738.5), pitch 16 ("Retrieve VALUES" / "Weighted by their Relevance"), noun
//     "VALUES" RED C00000 (x741..794)
//   tan label boxes: "KEYs" x64..134 y190..214, "Values" x762..835 y193..218, fill
//     E8C79A, 11pt bold 990000, centered
//   badges (red C00000 circles d24, WHITE bold 13pt letters — letter cores FFF2F3):
//     K center (163,342) right of left stack; V center (747.5,342.5) left of right
//     stack; Q center (258.5,439) right of the query box
//   query box x111..240 y420..460: fill F2C699, border CFB69B 1pt; "Query" 17pt bold
//     990000 / "ALL Keys with X2" 10.5pt bold 990000 (subscripted 2), centered, pitch 16
//   result box x557..827 y433..502: white fill, 0000CC 1pt border, 3 centered lines
//     13pt pitch 19 — "Values"(red C00000 bi) " of Matched "(blue 0000CC) "Keys"(red
//     bi) / "are returned"(blue) / "when Running "(blue) "Query"(red bi)
//   LEFT feed curve RED C00000 dashed (path pixel AC5D59; parent's was gray AC9F90)
//     + RED head triangle (97,399) 9x12 (parent's was green); same certified path
//     (170,472)-(130,468)-(112,460)-(104,448)-(102,430)-(102,409). RIGHT curve + green
//     head REMOVED in this frame (probes at (497,494)/(530,492)/(795,416)/(801,404)).
//   chunky red C5000F diagonal (266,526)->(284,512) KEPT from the parent; the parent's
//     thin red x298 arrow REMOVED (0 red px in x272..500 y404..470).
//   Strip incl. the magenta 5-cell X2 highlight: pixel-identical to the parent frame
//     (probe parity at x263..330 y476..497) — inherited via the parent component.

var PX = 1 / 72; // frame px -> inches

var C = {
  highlight: "FFFF00",
  calloutFill: "EDFBFB",
  calloutBorder: "3B7A40",
  magenta: "CC00CC",
  red: "C00000",
  darkRed: "990000",
  queryFill: "F2C699",
  queryBorder: "CFB69B",
  blue: "0000CC",
  tanBox: "E8C79A",
  white: "FFFFFF",
  redBlock: "C5000F",
};

var FONT = "Arial";

// ---- delta blocks ------------------------------------------------------------

function drawTitle(pptx, slide) {
  slide.addText(
    [
      { text: "Self Attention Mechanism ", options: {} },
      { text: "(as Query and {Key-Value} Dictionary)", options: { highlight: C.highlight } },
    ],
    {
      x: 0.41417, y: 0.725, w: 12.13, h: 0.42, align: "center", valign: "top",
      fontSize: 20, bold: true, color: "000000", fontFace: FONT, margin: 0,
    }
  );
  var red = { color: "9E101E" };
  slide.addText(
    [
      { text: "(", options: {} },
      { text: "Query", options: red },
      { text: " using ", options: {} },
      { text: "X", options: red }, { text: "2", options: { subscript: true, color: "9E101E" } },
      { text: " All ", options: {} },
      { text: "Keys", options: red },
      { text: " in Dictionary and retrieve Corresponding ", options: {} },
      { text: "Values", options: red },
    ],
    {
      x: 0.42111, y: 1.052, w: 12.13, h: 0.36, align: "center", valign: "top",
      fontSize: 20.5, bold: true, color: "000000", fontFace: FONT, margin: 0,
    }
  );
}

function drawLeftCurve(pptx, slide) {
  var L = [[170, 472], [130, 468], [112, 460], [104, 448], [102, 430], [102, 409]];
  for (var i = 0; i < L.length - 1; i++) {
    var o = {
      x: Math.min(L[i][0], L[i + 1][0]) * PX, y: Math.min(L[i][1], L[i + 1][1]) * PX,
      w: Math.abs(L[i + 1][0] - L[i][0]) * PX, h: Math.abs(L[i + 1][1] - L[i][1]) * PX,
      line: { color: C.red, width: 1, dashType: "dash" },
    };
    if (L[i + 1][0] < L[i][0]) o.flipH = true;
    if (L[i + 1][1] < L[i][1]) o.flipV = true;
    slide.addShape(pptx.ShapeType.line, o);
  }
  slide.addShape(pptx.ShapeType.triangle, {
    x: 97 * PX, y: 399 * PX, w: 9 * PX, h: 12 * PX,
    fill: { color: C.red }, line: { type: "none" },
  });
}

function drawQueryBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 111 * PX, y: 420 * PX, w: 129 * PX, h: 40 * PX, rectRadius: 0.06,
    fill: { color: C.queryFill },
    line: { color: C.queryBorder, width: 1 },
  });
  slide.addText(
    [
      { text: "Query", options: { fontSize: 17, breakLine: true } },
      { text: "ALL Keys with X", options: { fontSize: 10.5 } },
      { text: "2", options: { fontSize: 10.5, subscript: true } },
    ],
    {
      x: 111 * PX, y: 421 * PX, w: 129 * PX, h: 38 * PX,
      align: "center", valign: "middle", bold: true, color: C.darkRed,
      fontFace: FONT, lineSpacing: 16, margin: 0,
    }
  );
}

function badge(pptx, slide, cx, cy, letter) {
  slide.addShape(pptx.ShapeType.ellipse, {
    x: (cx - 12) * PX, y: (cy - 12) * PX, w: 24 * PX, h: 24 * PX,
    fill: { color: C.red }, line: { type: "none" },
  });
  slide.addText(letter, {
    x: (cx - 12) * PX, y: (cy - 12) * PX, w: 24 * PX, h: 24 * PX,
    align: "center", valign: "middle", bold: true, fontSize: 13,
    color: C.white, fontFace: FONT, margin: 0,
  });
}

function drawBadges(pptx, slide) {
  badge(pptx, slide, 163, 342, "K");
  badge(pptx, slide, 747.5, 342.5, "V");
  badge(pptx, slide, 258.5, 439, "Q");
}

function drawTanBoxes(pptx, slide) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 64 * PX, y: 190 * PX, w: 70 * PX, h: 24 * PX, rectRadius: 0.06,
    fill: { color: C.tanBox }, line: { type: "none" },
  });
  slide.addText("KEYs", {
    x: 64 * PX, y: 190 * PX, w: 70 * PX, h: 24 * PX,
    align: "center", valign: "middle", bold: true, fontSize: 11,
    color: C.darkRed, fontFace: FONT, margin: 0,
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 762 * PX, y: 193 * PX, w: 73 * PX, h: 25 * PX, rectRadius: 0.06,
    fill: { color: C.tanBox }, line: { type: "none" },
  });
  slide.addText("Values", {
    x: 762 * PX, y: 193 * PX, w: 73 * PX, h: 25 * PX,
    align: "center", valign: "middle", bold: true, fontSize: 11,
    color: C.darkRed, fontFace: FONT, margin: 0,
  });
}

function drawCallouts(pptx, slide) {
  // c1: LEFT-aligned text (measured L1 x325..451, L2 x329..469)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 315 * PX, y: 140 * PX, w: 175 * PX, h: 44 * PX, rectRadius: 0.07,
    fill: { color: C.calloutFill },
    line: { color: C.calloutBorder, width: 1, dashType: "dash" },
  });
  slide.addText(
    [
      { text: "Matched ", options: { color: C.magenta } },
      { text: "KEYS", options: { color: C.red } },
      { text: " with", options: { color: C.magenta, breakLine: true } },
      { text: "Relevance Percentage", options: { color: C.magenta } },
    ],
    {
      x: 326 * PX, y: 145 * PX, w: 160 * PX, h: 34 * PX,
      align: "left", valign: "middle", bold: true, italic: true, fontSize: 12,
      fontFace: FONT, lineSpacing: 15, margin: 0,
    }
  );
  // c2: CENTER-aligned text (measured L1/L2 both centered on x738.5)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 634 * PX, y: 145 * PX, w: 212 * PX, h: 43 * PX, rectRadius: 0.07,
    fill: { color: C.calloutFill },
    line: { color: C.calloutBorder, width: 1, dashType: "dash" },
  });
  slide.addText(
    [
      { text: "Retrieve ", options: { color: C.magenta } },
      { text: "VALUES", options: { color: C.red, breakLine: true } },
      { text: "Weighted by their Relevance", options: { color: C.magenta } },
    ],
    {
      x: 634 * PX, y: 150 * PX, w: 212 * PX, h: 33 * PX,
      align: "center", valign: "middle", bold: true, italic: true, fontSize: 12,
      fontFace: FONT, lineSpacing: 16, margin: 0,
    }
  );
}

function drawResultBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 557 * PX, y: 433 * PX, w: 270 * PX, h: 69 * PX,
    fill: { color: C.white },
    line: { color: C.blue, width: 1 },
  });
  slide.addText(
    [
      { text: "Values", options: { color: C.red, bold: true, italic: true } },
      { text: " of Matched ", options: { color: C.blue } },
      { text: "Keys", options: { color: C.red, bold: true, italic: true, breakLine: true } },
      { text: "are returned", options: { color: C.blue, breakLine: true } },
      { text: "when Running ", options: { color: C.blue } },
      { text: "Query", options: { color: C.red, bold: true, italic: true } },
    ],
    {
      x: 559 * PX, y: 437 * PX, w: 266 * PX, h: 61 * PX,
      align: "center", valign: "middle", fontSize: 13, color: C.blue,
      fontFace: FONT, lineSpacing: 19, margin: 0,
    }
  );
}

function drawChunkyArrow(pptx, slide) {
  var o = {
    x: 266 * PX, y: 512 * PX, w: 18 * PX, h: 14 * PX,
    line: { color: C.redBlock, width: 4, endArrowType: "triangle" },
  };
  o.flipV = true; // from (266,526) up-right to (284,512)
  slide.addShape(pptx.ShapeType.line, o);
}

function drawDotFeeds(pptx, slide) {
  // four red up-arrowheads below the Dot-Product dots (judge attempt-1 BLOCKER fix;
  // present in BOTH frames, omitted by the certified parent component — redrawn as
  // this slide's delta). Measured blobs under dots
  // (330.5,246.5)(314.5,287.5)(295.5,328)(276.5,372.5).
  var DOTFEEDS = [
    { x: 329.5, y: 255, w: 8, h: 10 },
    { x: 308, y: 297, w: 9.5, h: 10 },
    { x: 290.5, y: 337, w: 7.5, h: 10 },
    { x: 276.5, y: 381, w: 8, h: 8 },
  ];
  for (var i = 0; i < DOTFEEDS.length; i++) {
    slide.addShape(pptx.ShapeType.triangle, {
      x: DOTFEEDS[i].x * PX, y: DOTFEEDS[i].y * PX, w: DOTFEEDS[i].w * PX, h: DOTFEEDS[i].h * PX,
      fill: { color: C.red }, line: { type: "none" },
    });
  }
}

// ---- composition ------------------------------------------------------------

var BLOCKS = {
  leftCurve: drawLeftCurve,
  queryBox: drawQueryBox,
  badges: drawBadges,
  tanBoxes: drawTanBoxes,
  callouts: drawCallouts,
  resultBox: drawResultBox,
  chunkyArrow: drawChunkyArrow,
  dotFeeds: drawDotFeeds,
  title: drawTitle,
};

// canonical z-order for the delta (after the inherited base, before nothing):
// leftCurve sits UNDER queryBox (frame shows canvas at (112,460) — the box covers
// the curve's edge); title last, matching the parent's convention.
var ORDER = ["leftCurve", "queryBox", "badges", "tanBoxes", "callouts",
  "resultBox", "chunkyArrow", "dotFeeds", "title"];

/**
 * Draw the slide-29 composition: the certified slide-026 base (minus the blocks
 * slide 29's frame drops) + this slide's delta, at block granularity.
 * @param {object} pptx  pptxgenjs instance (ShapeType source)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip: [deltaBlock...], only: [deltaBlock...] }
 */
function renderBase(pptx, slide, opts) {
  var base = require(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_026.js"
  );
  base.renderBase(pptx, slide, { skip: ["title", "labels", "queryArrows", "feedCurves"] });
  opts = opts || {};
  var skip = opts.skip || [];
  var names = opts.only && opts.only.length ? opts.only.slice() : ORDER.slice();
  names.forEach(function (name) {
    if (skip.indexOf(name) !== -1) return;
    if (!BLOCKS[name]) throw new Error("slide_029 component: unknown block '" + name + "'");
    BLOCKS[name](pptx, slide);
  });
}

module.exports = {
  COLORS: C,
  FONT: FONT,
  BLOCKS: BLOCKS,
  ORDER: ORDER,
  renderBase: renderBase,
};
