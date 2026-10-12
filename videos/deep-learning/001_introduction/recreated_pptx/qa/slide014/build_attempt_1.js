// slide_014.js — 001_introduction slide 14 "How Training Takes Place to learn the model ?"
// Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_014.jpg (960x540, 1px = 1pt = 1/72 in).
// Measurement scripts banked in qa/slide014/measure_original{,2..7}.py (2026-10-12).
//   Measured structure (frame px):
//   per-slide red outer frame = an "L" (same object as certified slide_007 — identical
//     darkest-core pixels (106,45,53)): top line y42..44 x57..899 + left line x57..59 y42..517.
//   flowchart container: white rect, navy border — strokes: left col x74, right x885..886,
//     top rows y134..135, bottom y371..372 -> rect x74..886.5 y134..372.5; border ~1.5pt
//     #000080 (cores (33,23,122)/(33,27,101)/(21,27,105)); fill white (254,255,253).
//   node boxes (fill modal colors, PIL):
//     green  x99..263  y223..281  fill (9,134,58)=09863A, no border; text "Training Sample"
//            white bold, ink y247..260 x114..245 (131px -> 17pt), single line.
//     darkred x304..521.5 y195..308.5 fill (159,0,0)=9F0000, no border; THREE text lines
//            (spec said 2 — PIL col400 runs show 3 fill bands): "Classification" ink
//            y224..236 x343..475 (132px -> 20pt bold), "Model" y247..261 x384..440
//            (56px -> 20pt bold), "(with  Model Parameters)" rows 270..285 x309..514
//            (205px -> 17pt italic white; verbatim DOUBLE space kept). Pitch 24/22 -> lineSpacing 23.
//     ice    x559.5..656.5 y214.5..292.5 fill (226,255,251)=E2FFFB, NAVY border all 4 sides
//            (top core y215 (21,27,105), right x656 (22,26,100), bottom y291..293, left x559
//            JPEG-faded (170,169,209)); ~1.25pt. Text "Predicted/Class/(Label)" black bold
//            16pt ("Predicted" 72px -> 15.8), pitch 19/18 -> lineSpacing 18.5, centered (cx 608).
//     tan    x691..726.5 y159..347 fill (246,222,194)=F6DEC2 with a thin warm-gray border
//            (cores ~(173,170,165) all sides) ~1.25pt A69C90. Text "Error" black bold,
//            ROTATED reading bottom-to-top: ink x705..715 (cap ~11-14px -> 19pt), length
//            y228..277 (49px; "Error" 2.445em -> 19pt=46.5), centered (708.5, 253), rotate 270.
//     yellow x757..862 y225..282 fill (250,254,217)=FAFED9, NAVY border all 4 sides (left core
//            x757 (37,33,83), right x862 (32,25,93), bottom y282 (33,26,96), top y224..225
//            faded (84,80,139)); ~1.25pt. Text "True Label/of the/Sample" black bold 14.5pt
//            (widths 74/39/51px -> 14.3-14.6pt), pitch 17/17 -> lineSpacing 17, centered (cx 809.5).
//   arrows: FOUR thin line arrows (NOT block arrows — measured shafts 1-2px + small
//     triangular heads ~11.5px long, ~9.5px tall, all centered cy≈253), red C00000 family
//     (cores (176,0,16)): a1 green->darkred x268..302 tip RIGHT; a2 darkred->ice x522..558
//     tip RIGHT; a3 ice->tan x666..687 tip RIGHT; a4 yellow->tan x730..753 tip LEFT
//     (pointing INTO Error). Drawn shaft rect (h 1.5px) + rotated triangle head.
//   title: red bold, ink x162..776 (center 469) y77..102, cap y78..95 (18px). Font size
//     reconciled by width: 22.06em -> 27pt = 596px (measured 614; cap 19.3 vs 18) — start
//     27pt, closed-loop refine. C00000 (JPEG cores (168,15,33) = chroma-subsampled C00000,
//     consistent with the certified slide_007 red family).
//   takeaway: red bold single line, ink x108..815 (center 461.5) y437..452, cap y437..448
//     (12px). Width 37.34em -> 19pt = 709px (measured 707) — 19pt, closed-loop refine.
//     Verbatim double space in "error  (Loss Function)" kept.
//   black bottom strip: x38..921 y519..539 fully black (y518 AA) -> drawn y519..537.5 so the
//     chrome bottom stroke (rows 538-539, required by house_chrome_check.py) stays visible —
//     same 2-frame-px deviation documented on the certified slide_002/slide_007 builds.
//   gray cursor icon below the ice box (~(650,300)-(665,320)): screen-recording artifact,
//     NOT recreated (spec recreation_brief step 16 "optional, omit"; certified slide_007 precedent).
//
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn, NEVER ml-intro values. Badge numeral = 14 (slide file number;
//   the ORIGINAL frames of this lecture carry no badge — 001_introduction/AGENTS.md 2026-10-12,
//   assumption pending founder veto).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_014_recreated.pptx";

const px = (v) => v / 72;

// ---- palette (PIL modal measurements) ----
const RED = "C00000";        // arrows, title, takeaway, L-frame (slide_007-certified family)
const NAVY = "000080";       // panel border + ice/yellow box borders (cores b 90..128)
const BLACK = "000000";
const WHITE = "FFFFFF";
const GREEN = "09863A";      // (9,134,58)
const DARKRED = "9F0000";    // (159,0,0)
const ICE = "E2FFFB";        // (226,255,251)
const TAN = "F6DEC2";        // (246,222,194)
const TAN_BORDER = "A69C90"; // warm-gray border cores ~(173,170,165)
const YELLOWF = "FAFED9";    // (250,254,217)

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 14)
drawHouseChrome(pres, slide, { numeral: "14" });

// Per-slide red outer frame — the original shows ONLY top + left lines (an "L"),
// same object as certified slide_007 (identical darkest-core pixels).
slide.addShape(pres.ShapeType.line, {
  x: px(57), y: px(43), w: px(842), h: 0,
  line: { color: RED, width: 2.5 },
});
slide.addShape(pres.ShapeType.line, {
  x: px(58), y: px(42.5), w: 0, h: px(474.5),
  line: { color: RED, width: 2.5 },
});

// Black bottom strip (stops at y537.5 so the chrome bottom stroke stays visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(883), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Flowchart container — white rect, navy border ~1.5pt (strokes x74/x885-886, y134-135/y371-372)
slide.addShape(pres.ShapeType.rect, {
  x: px(74), y: px(134), w: px(813), h: px(239),
  fill: { color: WHITE }, line: { color: NAVY, width: 1.5 },
});

// ---- node boxes ----
// Node 1: green "Training Sample" (white bold 17pt, single line)
slide.addText("Training Sample", {
  shape: pres.ShapeType.rect,
  x: px(99), y: px(223.5), w: px(164), h: px(58),
  fill: { color: GREEN }, line: { color: GREEN, width: 0 },
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 17, bold: true, color: WHITE,
});

// Node 2: dark-red "Classification / Model / (with  Model Parameters)"
slide.addText(
  [
    { text: "Classification", options: { breakLine: true } },
    { text: "Model", options: { breakLine: true } },
    { text: "(with  Model Parameters)", options: { italic: true, fontSize: 17 } },
  ],
  {
    shape: pres.ShapeType.rect,
    x: px(304), y: px(195.5), w: px(217.5), h: px(113),
    fill: { color: DARKRED }, line: { color: DARKRED, width: 0 },
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 20, bold: true, color: WHITE,
    lineSpacing: 23,
  }
);

// Node 3: ice "Predicted / Class / (Label)" (black bold 16pt, navy border)
slide.addText(
  [
    { text: "Predicted", options: { breakLine: true } },
    { text: "Class", options: { breakLine: true } },
    { text: "(Label)" },
  ],
  {
    shape: pres.ShapeType.rect,
    x: px(559.5), y: px(214.5), w: px(97), h: px(78),
    fill: { color: ICE }, line: { color: NAVY, width: 1.25 },
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 16, bold: true, color: BLACK,
    lineSpacing: 18.5,
  }
);

// Node 4: tan tall "Error" box (black bold, rotated reading bottom-to-top)
slide.addShape(pres.ShapeType.rect, {
  x: px(691), y: px(159), w: px(35.5), h: px(188.5),
  fill: { color: TAN }, line: { color: TAN_BORDER, width: 1.25 },
});
slide.addText("Error", {
  x: px(673.5), y: px(242), w: px(70), h: px(22),
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 19, bold: true, color: BLACK,
  rotate: 270,
});

// Node 5: yellow "True Label / of the / Sample" (black bold 14.5pt, navy border)
slide.addText(
  [
    { text: "True Label", options: { breakLine: true } },
    { text: "of the", options: { breakLine: true } },
    { text: "Sample" },
  ],
  {
    shape: pres.ShapeType.rect,
    x: px(757), y: px(225), w: px(105), h: px(57),
    fill: { color: YELLOWF }, line: { color: NAVY, width: 1.25 },
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 14.5, bold: true, color: BLACK,
    lineSpacing: 17,
  }
);

// ---- four thin red arrows (shaft rect + rotated triangle head), cy = 253 ----
const arrow = (shaftX0, shaftX1, headCx, dir) => {
  slide.addShape(pres.ShapeType.rect, {
    x: px(shaftX0), y: px(252.25), w: px(shaftX1 - shaftX0), h: px(1.5),
    fill: { color: RED }, line: { color: RED, width: 0 },
  });
  slide.addShape(pres.ShapeType.triangle, {
    x: px(headCx - 4.75), y: px(247.25), w: px(9.5), h: px(11.5),
    fill: { color: RED }, line: { color: RED, width: 0 },
    rotate: dir === "right" ? 90 : 270,
  });
};
arrow(268, 291, 296.75, "right");  // green -> darkred
arrow(522, 547, 552.75, "right");  // darkred -> ice
arrow(666, 677, 682.25, "right");  // ice -> tan (Error)
arrow(742, 753, 735.75, "left");   // yellow -> tan (Error), pointing LEFT

// ---- title (red bold, ink center x469, cap top y78) ----
slide.addText("How Training Takes Place to learn the model ?", {
  x: px(48), y: px(75), w: px(842), h: px(27),
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 27, bold: true, color: RED,
});

// ---- takeaway sentence (red bold, ink center x461.5, cap top y437) ----
slide.addText("Try to update model parameters (Iteratively) to minimize error  (Loss Function)", {
  x: px(41.5), y: px(431), w: px(840), h: px(27),
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 19, bold: true, color: RED,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
