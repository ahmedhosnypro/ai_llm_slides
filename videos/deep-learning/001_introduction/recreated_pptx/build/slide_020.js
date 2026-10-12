// slide_020.js — 001_introduction slide 20 "The Complete Deep Learning Model".
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_020.jpg (960x540, 1px = 1pt).
// Measurement scripts: scratch/slide020_work/{regions,structure,comps,flood,rowscan,
//   trace,measure2..6}.py. Curved strokes are 600dpi transparent PNGs (matplotlib,
//   scratch/slide020_work/gen_curves_020.py) embedded at exact size — certified slide_009
//   pattern. Straight arrows are native LINE shapes with triangle heads (2px ink).
//
// Chrome: playlist house chrome via shared_patterns/house_chrome.js — imported, NEVER
// re-drawn. Badge numeral = "20" (file number; assumption PENDING FOUNDER VETO,
// 001_introduction/AGENTS.md 2026-10-12 — frames carry no printed badge).
// The frame's own slide region sits inset (x58..901) vs the canonical playlist chrome;
// the chrome law draws canonical values (judge ground rules cover the difference).
//
// Measured palette (JPEG cores; spec hexes lose to ink per deck law):
//   title/arrows/dashes/canvas border C00000 | container fill FDE9D9 (spec) dashes C00000
//   Input/Samples boxes DBBFA1 + 735432 | Pre FAFED8 + 000080 | Extraction E2FEFC + 000080
//   Selection F2FEEA + 397541 | Classification A00000 fill + 720418 border, white text
//   Predicted Labels F5DBF5 + 8E2F91 | error box F6B3B8 + C0A4B2 | ellipse F6DEC2 + 999999
//   dots/arcs 0C05A8 | green fan 1E8244 | green box EEFADA + C9C9B7, text 339933
//   block arrows BD3F4B | starburst FFFFCC + C00000 | black bar 000000
// Fonts (metric-solved start, closed-loop tuned): title 26pt bold; chain boxes 13pt bold
//   (baselines 233/247, pitch 14); Classification 12.5pt white; ellipse 13pt (pitch 15);
//   error box 13pt vert270 (line pitch 17); green box 14pt (pitch 19); starburst 11pt.
//
// LAWS honored: playlist chrome via shared module; verbatim text (incl. the unbalanced
// "(difference ... Actual labels" paren, "Pre processing", "Samples Labels"); margin:0 +
// explicit fontFace + explicit lineSpacing everywhere; no '#' in hex; black progress bar
// drawn per certified slide_009 precedent (x38..922, y518..537.5 — 2-frame-px short so the
// chrome bottom stroke stays visible and house_chrome_check.py passes).

const path = require("path");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_020_recreated.pptx";

// ---- palette -------------------------------------------------------------------
const C = {
  red: "C00000", white: "FFFFFF", black: "000000",
  tanFill: "DBBFA1", tanEdge: "735432",
  box1Fill: "FAFED8", box2Fill: "E2FEFC", box3Fill: "F2FEEA",
  box4Fill: "A00000", box5Fill: "F5DBF5",
  navy: "000080", greenEdge: "397541", maroon: "720418", purple: "8E2F91",
  peach: "FDE9D9", pinkFill: "F6B3B8", pinkEdge: "C0A4B2",
  ellipseFill: "F6DEC2", ellipseEdge: "999999",
  blue: "0C05A8", green: "1E8244",
  greenBoxFill: "EEFADA", greenBoxEdge: "C9C9B7", greenText: "339933",
  blockArrow: "BD3F4B", starFill: "FFFFCC",
};
const SANS = "Arial";
const px = (v) => v / 72;

const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1. house chrome (frame + badge numeral 20) --------------------------------
drawHouseChrome(pres, slide, { numeral: "20" });

// ---- 2. white diagram canvas with red border (outer x70..895, y100..466) --------
slide.addShape(pres.ShapeType.rect, {
  x: px(70), y: px(100), w: px(825), h: px(366),
  fill: { color: C.white }, line: { color: C.red, width: 1.5 },
});

// ---- 3. black progress bar (certified slide_009 precedent) ----------------------
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(518), w: px(884), h: px(19.5),
  fill: { color: C.black }, line: { color: C.black, width: 0 },
});

// ---- 4. title (ink x219..655 center 437, cap top 68, baseline 88) ---------------
slide.addText("The Complete Deep Learning Model", {
  x: px(87), y: px(57), w: px(700), h: px(40),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 26, bold: true, color: C.red,
  lineSpacing: 30,
});

// ---- 5. dashed red container (x194..637, y195..273, rounded, peach) -------------
slide.addShape(pres.ShapeType.roundRect, {
  x: px(194), y: px(195), w: px(443), h: px(78), rectRadius: 0.13,
  fill: { color: C.peach },
  line: { color: C.red, width: 1.75, dashType: "dash" },
});

// ---- 6. chain boxes (text baselines 233/247, pitch 14) --------------------------
function boxText(x, w, line1, line2) {
  slide.addText(
    [
      { text: line1, options: { breakLine: true } },
      { text: line2, options: {} },
    ],
    {
      x: px(x), y: px(222), w: px(w), h: px(28),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 13.5, bold: true, color: C.black,
      lineSpacing: 14,
    }
  );
}
// Input Samples (x79.5..158.5, y212..258)
slide.addShape(pres.ShapeType.rect, {
  x: px(79.5), y: px(212), w: px(79), h: px(46),
  fill: { color: C.tanFill }, line: { color: C.tanEdge, width: 1.75 },
});
boxText(79.5, 79, "Input", "Samples");
// Pre processing (x204..281, y206..264)
slide.addShape(pres.ShapeType.rect, {
  x: px(204), y: px(206), w: px(77), h: px(58),
  fill: { color: C.box1Fill }, line: { color: C.navy, width: 1.75 },
});
boxText(204, 77, "Pre", "processing");
// Feature Extraction (x330..404, y206..264)
slide.addShape(pres.ShapeType.rect, {
  x: px(330), y: px(206), w: px(74), h: px(58),
  fill: { color: C.box2Fill }, line: { color: C.navy, width: 1.75 },
});
boxText(330, 74, "Feature", "Extraction");
// Feature Selection (x427..514, y206..264)
slide.addShape(pres.ShapeType.rect, {
  x: px(427), y: px(206), w: px(87), h: px(58),
  fill: { color: C.box3Fill }, line: { color: C.greenEdge, width: 1.75 },
});
boxText(427, 87, "Feature", "Selection");
// Classification (x533.5..630, y207.5..263.5) — white single line, baseline ~239.5
slide.addShape(pres.ShapeType.rect, {
  x: px(533.5), y: px(207.5), w: px(96.5), h: px(56),
  fill: { color: C.box4Fill }, line: { color: C.maroon, width: 2 },
});
slide.addText("Classification", {
  x: px(533.5), y: px(226), w: px(96.5), h: px(20),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 12.5, bold: true, color: C.white,
  lineSpacing: 15,
});
// Predicted Labels (x656.5..741.5, y211.5..261)
slide.addShape(pres.ShapeType.rect, {
  x: px(656.5), y: px(211.5), w: px(85), h: px(49.5),
  fill: { color: C.box5Fill }, line: { color: C.purple, width: 1.75 },
});
boxText(656.5, 85, "Predicted", "Labels");
// Samples Labels (x807..887.5, y212..258)
slide.addShape(pres.ShapeType.rect, {
  x: px(807), y: px(212), w: px(80.5), h: px(46),
  fill: { color: C.tanFill }, line: { color: C.tanEdge, width: 1.75 },
});
boxText(807, 80.5, "Samples", "Labels");

// ---- 7. Training Data ellipse + dots (x374..465, y110..159) ---------------------
slide.addShape(pres.ShapeType.ellipse, {
  x: px(374), y: px(110), w: px(91), h: px(49),
  fill: { color: C.ellipseFill }, line: { color: C.ellipseEdge, width: 0.75 },
});
slide.addText(
  [
    { text: "Training", options: { breakLine: true } },
    { text: "Data", options: {} },
  ],
  {
    x: px(374), y: px(119.75), w: px(91), h: px(31),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 13, bold: true, color: C.black,
    lineSpacing: 15,
  }
);
// connector dots on the ellipse's left/right edges (d~11)
slide.addShape(pres.ShapeType.ellipse, {
  x: px(362), y: px(129.5), w: px(11), h: px(11),
  fill: { color: C.blue }, line: { color: C.blue, width: 0.5 },
});
slide.addShape(pres.ShapeType.ellipse, {
  x: px(469), y: px(129.5), w: px(11), h: px(11),
  fill: { color: C.blue }, line: { color: C.blue, width: 0.5 },
});

// ---- 8. Prediction Error (Loss Function) vertical box (x752..791, y170..298) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(752), y: px(170), w: px(39), h: px(128),
  fill: { color: C.pinkFill }, line: { color: C.pinkEdge, width: 1 },
});
slide.addText(
  [
    { text: "Prediction Error", options: { breakLine: true } },
    { text: "(Loss Function)", options: {} },
  ],
  {
    x: px(752), y: px(170), w: px(39), h: px(128),
    align: "center", valign: "middle", margin: 0,
    vert: "vert270", fontFace: SANS, fontSize: 14, bold: true, color: C.red,
    lineSpacing: 17,
  }
);

// ---- 9. straight red chain arrows (2px ink, triangle heads) ---------------------
function arrow(x0, x1, opts = {}) {
  slide.addShape(pres.ShapeType.line, {
    x: px(x0), y: px(235), w: px(x1 - x0), h: 0,
    line: {
      color: C.red, width: 2,
      endArrowType: opts.begin ? undefined : "triangle",
      beginArrowType: opts.begin ? "triangle" : undefined,
    },
  });
}
arrow(159, 193);          // Input Samples -> container
arrow(282, 320);          // Pre -> Feature Extraction
arrow(406, 429);          // Feature Extraction -> Feature Selection
arrow(514, 530);          // Feature Selection -> Classification
arrow(635, 657);          // Classification -> Predicted Labels
arrow(740, 750);          // Predicted Labels -> Prediction Error box
arrow(792, 806, { begin: true }); // Samples Labels -> into Prediction Error (leftward)

// ---- 10. curved strokes (600dpi PNGs, exact-size embed) --------------------------
slide.addImage({
  path: path.join(ASSETS, "arc_left_020.png"),
  x: px(108), y: px(128), w: 3.6944, h: 1.2222,   // ellipse left dot -> Input Samples
});
slide.addImage({
  path: path.join(ASSETS, "arc_right_020.png"),
  x: px(468), y: px(128), w: 5.3889, h: 1.2222,   // ellipse right dot -> Samples Labels
});
slide.addImage({
  path: path.join(ASSETS, "green_fan_020.png"),
  x: px(232), y: px(256), w: 7.6389, h: 1.0278,   // error-box bottom -> four box bottoms
});

// ---- 11. thick red block arrows (both point up) ----------------------------------
slide.addShape(pres.ShapeType.upArrow, {
  x: px(593), y: px(385), w: px(22), h: px(41),
  fill: { color: C.blockArrow }, line: { color: C.blockArrow, width: 0.5 },
});
slide.addShape(pres.ShapeType.upArrow, {
  x: px(768), y: px(309), w: px(22), h: px(41),
  fill: { color: C.blockArrow }, line: { color: C.blockArrow, width: 0.5 },
});

// ---- 12. green annotation box (x261..743, y338..379) -----------------------------
slide.addShape(pres.ShapeType.roundRect, {
  x: px(261), y: px(338), w: px(482), h: px(41), rectRadius: 0.06,
  fill: { color: C.greenBoxFill }, line: { color: C.greenBoxEdge, width: 1 },
});
slide.addText(
  [
    { text: "Update Model Parameters in order to ", options: {} },
    { text: "MINIMIZE", options: { bold: true } },
    { text: " error", options: { breakLine: true } },
    { text: "(difference between model prediction and Actual labels", options: {} },
  ],
  {
    x: px(263), y: px(340.5), w: px(478), h: px(36),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 16.5, color: C.greenText,
    lineSpacing: 19,
  }
);

// ---- 13. starburst + text (spikes x709..881, y378..436) ---------------------------
slide.addShape(pres.ShapeType.star16, {
  x: px(709), y: px(378), w: px(172), h: px(58),
  fill: { color: C.starFill }, line: { color: C.red, width: 1.5 },
});
slide.addText(
  [
    { text: "The BIG", options: { breakLine: true } },
    { text: "challenge", options: {} },
  ],
  {
    x: px(735.5), y: px(395), w: px(106), h: px(28),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 12.5, bold: true, color: C.red,
    lineSpacing: 13,
  }
);

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
