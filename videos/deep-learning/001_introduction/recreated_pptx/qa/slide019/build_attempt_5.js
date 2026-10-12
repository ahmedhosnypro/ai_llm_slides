// build/slide_019.js — slide 019 "The Complete Deep Learning Model" (001_introduction).
//
// DEPENDENCY BUILD (founder directive 2026-10-11/12; slide_dependencies.json edge 19←9):
// imports the CERTIFIED parent composition components/slide_009.js via renderBase() and
// draws only this slide's measured delta. Never re-derives or copy-pastes parent geometry.
// Inherited blocks: chrome (numeral overridden to "19" — PENDING-VETO badge law: numeral =
// slide file number), panel, blackbar (slide 19's original panel x69..895 y99..465 and
// black bar x38..921 y519..539 match the parent's drawn geometry within ~1px).
// Skipped parent blocks: title, training_ellipse, all chain boxes/arrows, curves, gray
// labels, final ellipse — slide 19 redraws all of them at ITS measured geometry.
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_019.jpg (960x540, 1px=1pt,
// in = px/72) — qa/slide019/measure_original{1..5}.py + probe_build{1..3}.py (this build).
// Delta asset PNGs (600dpi transparent, exact-size embed): qa/slide019/gen_assets_019.py
// (peer-banked: bluefan_019, greenfan_019; container redrawn NATIVE — the peer's container
// PNG extended to x658, but dashes measure only to x629 hidden behind the Classification
// box, so the peer asset's right tail would be wrong vs the original). Pencil glyph is a
// faithful pixel crop of the original (build/assets/pencil_crop_019.png, gen_pencil_crop.py).
//
// Measured palette (JPEG-core modals; spec hexes lose to ink per deck law):
//   title A00000 (core 980818) | arrows C00000 | container dash A00000, fill F6DEC2
//   input/samples D9C0A1 + 76522E border | pre FAFED8 + 000080 | extraction E2FEFC + 000080
//   selection F2FEEA + 44784A | classification A00000 + 720418, white text
//   predicted FFCCFF + 711E76 | verr F5B4B8 (NO border stroke measured), text 902028
//   ellipse F6DEC2 + 999999 ring | annot ECFBDE + B8C8B0, text 205028 | blue 1A1078, green 0B7C33
// Chain text 14pt bold black pitch 16; classification 12pt white; verr text 6.5pt bold
// rotated 270 (bottom-to-top); annot 14pt pitch 18; title 26pt (ink adv 433 → ~26pt).
//
// LAWS honored: playlist chrome via shared shared_patterns module (through the certified
// parent component); verbatim text incl. the unclosed "(" and "Samples Labels" (sic);
// margin:0 + explicit fontFace + explicit lineSpacing everywhere; no '#' in hex;
// mouse-cursor/video artifacts omitted; single-version deliverable (no suffix).

const path = require("path");
const { renderBase } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_009.js"
);

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

const px = (v) => v / 72;
const SANS = "Arial";

const C = {
  red: "A00000",        // title, container dashes (frame-measured family)
  arrowRed: "C00000",   // chain arrows (core B/C0000)
  black: "000000", white: "FFFFFF",
  tan: "D9C0A1", brown: "76522E",
  paleYellow: "FAFED8", navy: "000080",
  cyan: "E2FEFC", paleGreen: "F2FEEA", green: "44784A",
  darkRed: "A00000", maroon: "720418",
  pink: "FFCCFF", purple: "711E76",
  verrPink: "F5B4B8", verrText: "902028",
  peach: "F6DEC2", grayRing: "999999",
  annotFill: "ECFBDE", annotEdge: "B8C8B0", annotText: "205028",
};

// chain band: boxes outer y196..274 (borders 196-198 / 272-274), two-line 14pt pitch 16
const BOX_Y = 196, BOX_H = 78;

// ---- delta blocks ----------------------------------------------------------------

function drawContainer(pptx, slide) {
  // dashed peach container around nodes 2-5: fill+zone x194..630 y196..273, corner r10;
  // dash rows 196-198 / ~273 (3.5on/3.5off), left border x194, RIGHT border omitted —
  // hidden behind the Classification box in the original (dashes measure only to x~620-629).
  // 600dpi PNG with EXPLICIT dash segments (container_v3_019, gen_container_v3.py):
  // matplotlib ignores linestyle on FancyBboxPatch (v1/v2 rendered solid, duty=1.00
  // measured) and LO's native dash preset renders a ~24px period (selfcheck attempt 1/2).
  slide.addImage({
    path: path.join(ASSETS, "container_v3_019.png"),
    x: px(191), y: px(193), w: px(633 - 191), h: px(276 - 193),
  });
}

function chainBox(pptx, slide, x0, x1, fill, edge, line1, line2, y0, y1, ty0, ty1) {
  // rect band [y0..y1]; text block centered on [ty0..ty1] (the original's text sits at
  // y222..250 in EVERY box while rect bands differ: 205..274 inside the container,
  // 212..258 for the terminal Input/Samples boxes)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(x0), y: px(y0), w: px(x1 - x0), h: px(y1 - y0),
    fill: { color: fill }, line: { color: edge, width: 2 },
  });
  slide.addText(
    [
      { text: line1, options: { breakLine: true } },
      { text: line2, options: {} },
    ],
    {
      x: px(x0), y: px(ty0), w: px(x1 - x0), h: px(ty1 - ty0),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 15, bold: true, color: C.black,
      lineSpacing: 16,
    }
  );
}

function drawBoxes(pptx, slide) {
  // terminal boxes are SHORT: borders y212-213/257 (probe_borders.py: no ink 194..211 or
  // 260..277 in their interiors); container'd boxes y205..274 (continuous top border
  // rows 205-207; container dash row 196-198 passes ABOVE them)
  chainBox(pptx, slide, 80, 157, C.tan, C.brown, "Input", "Samples", 212, 258, 221, 251);      // borders 79-81/156-158
  chainBox(pptx, slide, 806, 884, C.tan, C.brown, "Samples", "Labels", 212, 258, 221, 251);    // node 8: borders 805-807/883-885
  chainBox(pptx, slide, 204, 280, C.paleYellow, C.navy, "Pre", "processing", 205, 274, 220, 250);    // borders 203-205/279-281
  chainBox(pptx, slide, 321, 404, C.cyan, C.navy, "Feature", "Extraction", 205, 274, 220, 250);      // borders 320-322/403-405
  chainBox(pptx, slide, 426, 514, C.paleGreen, C.green, "Feature", "Selection", 205, 274, 220, 250); // borders 426-429/511-515
  // Classification: dark red, white single-line 12pt (text band y231..239, cols 539..621)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(532), y: px(205), w: px(630 - 532), h: px(274 - 205),
    fill: { color: C.darkRed }, line: { color: C.maroon, width: 2 },
  });
  slide.addText("Classification", {
    x: px(532), y: px(225), w: px(98), h: px(20),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 12, bold: true, color: C.white,
    lineSpacing: 14,
  });
  chainBox(pptx, slide, 658, 737, C.pink, C.purple, "Predicted", "Labels", 212, 259, 221, 251); // smaller box
}

// straight chain arrows: 2px ink at y235, triangle head at the target box border
function arrow(pptx, slide, x0, x1, opts = {}) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x0), y: px(235), w: px(x1 - x0), h: 0,
    line: {
      color: C.arrowRed, width: 1.75,
      ...(opts.begin ? { beginArrowType: "triangle" } : { endArrowType: "triangle" }),
    },
  });
}
function drawArrows(pptx, slide) {
  arrow(pptx, slide, 160, 193);            // Input Samples -> container left border (ink 166..194)
  arrow(pptx, slide, 283, 318);            // Pre -> Feature Extraction (ink 291..315)
  arrow(pptx, slide, 408, 425);            // Extraction -> Selection (ink 411..427)
  arrow(pptx, slide, 517, 531);            // Selection -> Classification (stub, ink 526..531)
  arrow(pptx, slide, 632, 655);            // Classification -> Predicted Labels (ink 635..655)
  arrow(pptx, slide, 740, 751);            // Predicted -> Prediction Error (ink 740..750)
  arrow(pptx, slide, 790, 803, { begin: true }); // Samples Labels -> Prediction Error, LEFTWARD (ink 793..809)
}

function drawBluefan(pptx, slide) {
  // peer-banked 600dpi PNG: solid curve ellipse-left -> Input Samples top + dashed curve
  // ellipse-right -> Samples Labels top, navy 1A1078, heads included. bbox (103,126)-(858,215)
  slide.addImage({
    path: path.join(ASSETS, "bluefan_019.png"),
    x: px(103), y: px(126), w: px(858 - 103), h: px(215 - 126),
  });
}

function drawVerr(pptx, slide) {
  // pink vertical box x752..789 y171..298, NO border stroke measured
  slide.addShape(pptx.ShapeType.rect, {
    x: px(752), y: px(171), w: px(789 - 752), h: px(298 - 171),
    fill: { color: C.verrPink }, line: { color: C.verrPink, width: 0 },
  });
  // rotated label reads bottom-to-top: ink x774..786 (center 780), y183..286 (len ~103).
  // Box w=130 > the ~110px string: w=104 wrapped the text into vertical columns
  // (selfcheck attempt 4: bimodal column profile 775-778/781-786 + stray 790-802).
  slide.addText("Prediction Error (Loss Function)", {
    x: px(780 - 65), y: px(234.5 - 7), w: px(130), h: px(14),
    align: "center", valign: "middle", margin: 0, rotate: 270,
    fontFace: SANS, fontSize: 7, bold: true, color: C.verrText,
    lineSpacing: 8,
  });
}

function drawGreenfan(pptx, slide) {
  // peer-banked 600dpi PNG: origin dot at verr bottom (770,303) + 4 dashed beziers with
  // up-heads into Pre/Extraction/Selection/Classification bottoms. bbox (205,253)-(790,330)
  slide.addImage({
    path: path.join(ASSETS, "greenfan_019.png"),
    x: px(205), y: px(253), w: px(790 - 205), h: px(330 - 253),
  });
}

function drawPencil(pptx, slide) {
  // peer-drawn glyph (gen_assets_019.py): tip lower-left (246.5,233), body up-right -42deg
  // — matches the measured ink x245..263 y213..233 (probe_borders.py: the ASCII "bar" and
  // "vertical" are the pre box's top/right borders, not pencil parts)
  slide.addImage({
    path: path.join(ASSETS, "pencil_019.png"),
    x: px(243), y: px(211), w: px(266 - 243), h: px(236 - 211),
  });
}

function drawEllipse(pptx, slide) {
  // Training Data ellipse: ring x342..500 y99..159 (touches panel top border), gray ring
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(342), y: px(99), w: px(500 - 342), h: px(159 - 99),
    fill: { color: C.peach }, line: { color: C.grayRing, width: 1 },
  });
  // two-line bold label: bands y122..134 / y138..147 (pitch 16), centered on x421
  slide.addText(
    [
      { text: "Training", options: { breakLine: true } },
      { text: "Data", options: {} },
    ],
    {
      x: px(371), y: px(116), w: px(100), h: px(36),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 14, bold: true, color: C.black,
      lineSpacing: 16,
    }
  );
}

function drawTitle(pptx, slide) {
  // ink x221..654 y69..91, center 437.5 (OFF slide-center in the original — match ink),
  // ~26pt (adv 433px / 17.0em), baseline ~86-87
  slide.addText("The Complete Deep Learning Model", {
    x: px(87.5), y: px(60), w: px(700), h: px(36),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 25.5, bold: true, color: C.red,
    lineSpacing: 30,
  });
}

function drawAnnot(pptx, slide) {
  // rounded annotation box x262..741 y340..377 (h38), pale-green fill, faint sage border
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(262), y: px(340), w: px(741 - 262), h: px(377 - 340), rectRadius: 0.07,
    fill: { color: C.annotFill }, line: { color: C.annotEdge, width: 0.75 },
  });
  // two centered 15pt lines (orig ink line1 w392 x305..697, line2 w397), pitch 18;
  // MINIMIZE bold; unclosed "(" verbatim (sic). FLAT run list — breakLine on the LAST
  // run of line 1 (nested run arrays silently drop trailing runs — measured attempt 1).
  slide.addText(
    [
      { text: "Update Model Parameters in order to ", options: {} },
      { text: "MINIMIZE", options: { bold: true } },
      { text: " error", options: { breakLine: true } },
      { text: "(difference between model prediction and Actual labels", options: {} },
    ],
    {
      x: px(266), y: px(342), w: px(741 - 266 - 4), h: px(33),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 16.5, color: C.annotText,
      lineSpacing: 18,
    }
  );
}

// ---- composition -----------------------------------------------------------------

const pptxgen = require("pptxgenjs");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();

// 1) certified parent base: chrome (numeral 19) + panel + blackbar; skip all else
renderBase(pptx, slide, {
  numeral: "19",
  skip: [
    "title", "training_ellipse", "box_pre", "box_extraction", "box_selection",
    "box_classification", "box_post", "arrow1", "arrow2", "arrow3", "arrow4",
    "curve1", "curve2", "label_cleaned", "label_vectors", "label_features",
    "label_predicted", "final_ellipse",
  ],
});

// 2) this slide's measured delta (z-order: container under boxes; ellipse UNDER the blue
// fan — the original shows both curves' starts over the ellipse fill)
drawContainer(pptx, slide);
drawEllipse(pptx, slide);
drawBoxes(pptx, slide);
drawArrows(pptx, slide);
drawBluefan(pptx, slide);
drawVerr(pptx, slide);
drawGreenfan(pptx, slide);
drawPencil(pptx, slide);
drawTitle(pptx, slide);
drawAnnot(pptx, slide);

pptx.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_019_recreated.pptx" })
  .then(() => console.log("WROTE slide_019_recreated.pptx"));
