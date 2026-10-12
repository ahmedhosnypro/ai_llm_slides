// slide_018.js — 001_introduction slide 18 "The Complete Deep Learning Model"
// (the End-To-End / "Deeeeeeep Model" variant of the classification pipeline).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11/12; slide_dependencies.json edge 18←9):
// child of CERTIFIED slide 9. This build requires the parent's certified component by
// ABSOLUTE path and calls renderBase(pptx, slide, opts) — the parent's geometry is NEVER
// re-derived or copy-pasted. The child draws ONLY its measured delta.
//
// Parent blocks INHERITED unchanged (renderBase): panel, blackbar, box_extraction,
//   box_selection, box_classification — PIL-verified on THIS frame to sit at the parent's
//   certified geometry within 1-2 frame px (extraction navy borders x293-294/x408-409,
//   selection green x444/x558, classification fill x589..719 y211..263, white text band
//   y230..244 — all inside the certified bands).
// Parent blocks SKIPPED (replaced/removed by this frame's delta): title (different text,
//   ink center 438.5 vs 467), training_ellipse (taller: y128..208 h80 vs parent h58),
//   box_pre (shifted left: x130..237 vs parent 145.5..250.5), box_post (replaced by the
//   Classifier Output tan box at the SAME path geometry x748,y208,w115,h57 — different
//   fill/text), arrow1-4 (box_pre moved → arrow1 endpoints change; 2-4 re-measured),
//   curve1 (re-traced to the moved box), curve2, label_cleaned/vectors/features/
//   predicted, final_ellipse (all absent from this frame).
//
// Delta blocks (all PIL-measured on unique_slides/slide_018.jpg, 960x540, 1px=1pt;
// measurement scripts qa/slide018/measure_1..13.py):
//   title 26pt bold red, ink x223..654 center 438.5, cap 69 baseline ~87
//   dashed red container x117..725.5, y196.5..268.5 (dash ~4on/4off at 2px ink → 1.5pt)
//   End-To-End chip x343..557 y133..160, fill E2FEFC-family, slate border, NAVY text
//     (measured glyph cores (0,0,110) — spec's "black" loses to ink per deck law)
//   navy dashed arc (600dpi PNG, certified curve technique): (215,158)→(796,196),
//     left head tip (212,158), right head dives to (801,207) into Classifier Output top
//   Classifier Output x748..864 y208..266, tan DABFA1 + black border; text 16pt single
//     line CENTERED AT x814 (measured ink x753..875 — the original's text overflows the
//     box's right edge by ~11px; reproduced via a wider centered text box)
//   deep-model double arrow x115..727 y271..273 (3px ink → 2.25pt, heads both ends)
//   deep label chip x304..517 y281..301 fill ECFBDE + CDCDB4, "Deeeeeeep Model" 14pt
//   callouts (12pt bold, pitch ~16): c1 x86..268 y312..352 ("(Model Choice)" red line 2),
//     c2 x286..438 y308..366 (line 1 red), c3 x453..574 y308..366 (line 1 red),
//     c4 x601..716 y319..351 (all black); gray E6E8E6 + C2C4C2 per certified parent
//   starburst star16 x735..874 y295..343, fill F9FFD9 (measured modal), NO outline
//     (ink: no red at the spike tips), red text "Based on"/"Trained Model" 12pt pitch 14
//   statement box x280..567 y391..445, cream FFFFE6 fill + violet-navy 000090 border,
//     two red bold lines 14pt pitch 22
//
// ARTIFACTS OMITTED (ground rule c): the peach/pink cursor-hover washes around arrow1
//   (x238..292) / arrow2 (x411..429) and the deep-label chip, and the mouse cursor on the
//   label's right edge. The dashed container edge hugging Classification's right border
//   and the ellipse overlapping box_pre's top-left corner are reproduced as measured.
//
// LAWS honored: playlist chrome via the parent's component (delegates to
//   shared_patterns/house_chrome.js) — numeral "18"; verbatim text (incl. "Deeeeeeep
//   Model" 7 e's, "Model choose Best", "End-To-End model" lowercase m); margin:0 +
//   explicit fontFace + explicit lineSpacing everywhere; no '#' in hex; black progress
//   bar inherited from the certified parent (slide_005 precedent).

const path = require("path");

const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_009.js");
const { C: PC, px } = PARENT; // certified parent palette + px() helper

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_018_recreated.pptx";

const SANS = "Arial";

// ---- measured palette (JPEG cores, this frame) ---------------------------------
const M = {
  red: PC.red,                     // C00000 — title, arrows, container, star outline
  black: "000000",
  navy: PC.navy,                   // 000080 — box_pre border, chip text, arc
  slateEdge: "708090",             // End-To-End chip border (measured (128,132,159))
  tanFill: "DABFA1",               // Classifier Output (measured (218,191,161))
  deepFill: "ECFBDE",              // Deeeeeeep Model chip (measured (236,251,222))
  deepEdge: "CDCDB4",              // chip border (measured (205,205,180))
  starFill: "F9FFD9",              // starburst (measured modal (249,255,217))
  stmtFill: "FFFFE6",              // statement box fill (measured (255,255,230))
  stmtEdge: "000090",              // statement border (core sample (17,2,143))
};

const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1. certified parent composition (chrome + panel + blackbar + 3 chain boxes) --
PARENT.renderBase(pres, slide, {
  numeral: "18",
  skip: [
    "title", "training_ellipse", "box_pre", "box_post",
    "arrow1", "arrow2", "arrow3", "arrow4",
    "curve1", "curve2",
    "label_cleaned", "label_vectors", "label_features", "label_predicted",
    "final_ellipse",
  ],
});

// ---- 2. title (replaced: different string, ink center 438.5) ----------------------
slide.addText("The Complete Deep Learning Model", {
  x: px(88.5), y: px(58.5), w: px(700), h: px(40),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 26, bold: true, color: M.red,
  lineSpacing: 30,
});

// ---- 3. Training Data ellipse (taller + higher than parent's; drawn BEFORE the
//         container so the dashed edge crosses its lower-right as in the original) --
slide.addShape(pres.ShapeType.ellipse, {
  x: px(78), y: px(128), w: px(131), h: px(80),
  fill: { color: "F6DEC2" }, line: { color: "999999", width: 0.75 },
});
slide.addText(
  [
    { text: "Training", options: { breakLine: true } },
    { text: "Data", options: {} },
  ],
  {
    x: px(88), y: px(137.7), w: px(111), h: px(40),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 18, bold: true, color: M.black,
    lineSpacing: 20,
  }
);

// ---- 4. dashed red container (rounded, no fill; dashes visible over the ellipse) --
slide.addShape(pres.ShapeType.roundRect, {
  x: px(117), y: px(196.5), w: px(608.5), h: px(72), rectRadius: 0.08,
  fill: { type: "none" },
  line: { color: M.red, width: 1.5, dashType: "dash" },
});

// ---- 5. box_pre at THIS frame's measured position (parent's box style) ------------
slide.addShape(pres.ShapeType.rect, {
  x: px(130), y: px(208), w: px(107), h: px(57),
  fill: { color: "FAFED8" }, line: { color: M.navy, width: 2 },
});
slide.addText(
  [
    { text: "Pre", options: { breakLine: true } },
    { text: "processing", options: {} },
  ],
  {
    x: px(130), y: px(217.6), w: px(107), h: px(38),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 17, bold: true, color: M.black,
    lineSpacing: 19,
  }
);

// ---- 5. Classifier Output (parent box_post path geometry, tan fill, black edge) ---
slide.addShape(pres.ShapeType.rect, {
  x: px(748), y: px(208), w: px(115), h: px(57),
  fill: { color: M.tanFill }, line: { color: M.black, width: 1.5 },
});
slide.addText("Classifier Output", {
  x: px(744), y: px(225.6), w: px(140), h: px(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 16, bold: true, color: M.black,
  lineSpacing: 20,
});

// ---- 6. straight chain arrows (2px ink at y236.5, triangle heads) ------------------
function arrow(x0, x1) {
  slide.addShape(pres.ShapeType.line, {
    x: px(x0), y: px(236.5), w: px(x1 - x0), h: 0,
    line: { color: M.red, width: 1.75, endArrowType: "triangle" },
  });
}
arrow(239, 291);  // Pre processing -> Feature Extraction
arrow(412, 441);  // Feature Extraction -> Feature Selection
arrow(562, 585);  // Feature Selection -> Classification
arrow(722, 746);  // Classification -> Classifier Output

// ---- 7. End-To-End model chip ------------------------------------------------------
slide.addShape(pres.ShapeType.roundRect, {
  x: px(343), y: px(133), w: px(214), h: px(27), rectRadius: 0.07,
  fill: { color: "E2FEFC" }, line: { color: M.slateEdge, width: 1 },
});
slide.addText("End-To-End model", {
  x: px(343), y: px(136), w: px(214), h: px(21),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 16, bold: true, color: M.navy,
  lineSpacing: 17,
});

// ---- 9. navy dashed double-headed arc (600dpi PNG, exact-size embed) ---------------
slide.addImage({
  path: path.join(ASSETS, "arc_018.png"),
  x: px(208), y: px(149), w: 8.3194, h: 0.875,
});

// ---- 10. red feed curve ellipse -> Pre processing (600dpi PNG) ---------------------
slide.addImage({
  path: path.join(ASSETS, "curve1_018.png"),
  x: px(90), y: px(183), w: 0.6111, h: 0.8889,
});

// ---- 11. deep-model double-headed arrow + label chip -------------------------------
slide.addShape(pres.ShapeType.line, {
  x: px(118), y: px(272), w: px(606), h: 0,
  line: {
    color: M.red, width: 2.25,
    beginArrowType: "triangle", endArrowType: "triangle",
  },
});
slide.addShape(pres.ShapeType.roundRect, {
  x: px(304), y: px(281), w: px(213), h: px(20), rectRadius: 0.05,
  fill: { color: M.deepFill }, line: { color: M.deepEdge, width: 1 },
});
slide.addText("Deeeeeeep Model", {
  x: px(304), y: px(282.5), w: px(213), h: px(17),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 15.5, bold: true, color: M.black,
  lineSpacing: 16,
});

// ---- 12. gray annotation callouts ---------------------------------------------------
function callout(x, y, w, h, lines) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: "E6E8E6" }, line: { color: "C2C4C2", width: 1 },
  });
  slide.addText(
    lines.map(([t, color], i) => ({
      text: t,
      options: { color, breakLine: i < lines.length - 1 },
    })),
    {
      x: px(x + 1), y: px(y + 1), w: px(w - 2), h: px(h - 2),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 12, bold: true, color: M.black,
      lineSpacing: 16,
    }
  );
}
callout(86, 312, 182, 40, [
  ["Based on Training Data", "000000"],
  ["(Model Choice)", "C00000"],
]);
callout(286, 308, 152, 58, [
  ["Model choose Best", "C00000"],
  ["feature for given", "000000"],
  ["training data", "000000"],
]);
callout(453, 308, 121, 58, [
  ["Model Reduces", "C00000"],
  ["the features", "000000"],
  ["(if required)", "000000"],
]);
callout(601, 319, 115, 32, [
  ["Classify using", "000000"],
  ["Trained Model", "000000"],
]);

// ---- 13. starburst + red text (measured: NO outline on this frame's star;
//         bbox x735..874 y295..343; text 12pt pitch 14 centered x~808) ---------------
slide.addShape(pres.ShapeType.star16, {
  x: px(735), y: px(295), w: px(139), h: px(48),
  fill: { color: M.starFill }, line: { type: "none" },
});
slide.addText(
  [
    { text: "Based on", options: { breakLine: true } },
    { text: "Trained Model", options: {} },
  ],
  {
    x: px(760), y: px(305), w: px(96), h: px(28),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 12, bold: true, color: M.red,
    lineSpacing: 14,
  }
);

// ---- 14. bottom statement box --------------------------------------------------------
slide.addShape(pres.ShapeType.rect, {
  x: px(280), y: px(391), w: px(287), h: px(54),
  fill: { color: M.stmtFill }, line: { color: "11028F", width: 1 },
});
slide.addText(
  [
    { text: "No Interaction from Human", options: { breakLine: true } },
    { text: "It is Based on Training Data", options: {} },
  ],
  {
    x: px(282), y: px(393), w: px(283), h: px(50),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 14, bold: true, color: M.red,
    lineSpacing: 22,
  }
);

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
