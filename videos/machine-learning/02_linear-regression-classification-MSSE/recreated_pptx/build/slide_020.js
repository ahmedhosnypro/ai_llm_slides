// slide_020.js — "How to obtain the BEST model parameters (W)"
// Deck: machine-learning/02_linear-regression-classification-MSSE
// House chrome: shared_patterns/house_chrome.js (THIS deck's values) + numeral 20.
// All geometry PIL-measured from unique_slides/slide_020.jpg (960x540, 1px=1pt);
// measurements banked in scratch/ml02/slide020/measurements_banked.json.
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/slide_020.js

const pptxgen = require("pptxgenjs");
const VP = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE";
const { drawHouseChrome } = require(VP + "/shared_patterns/house_chrome.js");

const px = (v) => v / 72; // frame px (1px = 1pt) -> inches

// ---- tunables (calibrated against the 150dpi render, closed loop) ----
const FS = {
  title: 25.5, label: 16, green: 15, drL1: 17, drIt: 16, cyan: 13,
  err: 20, tl: 13, sent: 19.2, note1: 20, note2: 19.5, note3: 19, blue3: 19.5, hand: 28,
};
// vertical nudges (frame px) applied to line-box centers after calibration
const ND = { title: 0, label: 0, green: 0, dr: 0, cyan: 0, err: 0, tl: 0, sent: 0, note1: 0, note2: 0, note3: 0, handX: 0, handY: 0 };

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1. house chrome (panel + red border + badge numeral 20) ----
drawHouseChrome(pres, slide, { numeral: "20" });

// ---- 2. big white container with red border (x70..885, y127..521) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(70), y: px(127), w: px(816), h: px(395),
  fill: { color: "FFFFFF" }, line: { color: "C00000", width: 1 },
});

// ---- 3. beige label box "Training Sample with Label" (x384..607, y139..170) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(384), y: px(139), w: px(224), h: px(32),
  fill: { color: "F4E7D4" }, line: { type: "none" },
});
slide.addText("Training Sample with Label", {
  x: px(384), y: px(137), w: px(224), h: px(32),
  align: "center", valign: "middle", bold: true, fontSize: FS.label,
  color: "C00000", fontFace: "Arial", margin: 0,
});

// ---- 4. flowchart boxes ----
// green Training Sample (x133..266, y235..293), white bold 2 lines, pitch 18
slide.addShape(pres.ShapeType.rect, {
  x: px(133), y: px(235), w: px(134), h: px(59),
  fill: { color: "098839" }, line: { type: "none" },
});
slide.addText([
  { text: "Training", options: { breakLine: true } },
  { text: "Sample", options: {} },
], {
  x: px(133), y: px(233), w: px(134), h: px(59),
  align: "center", valign: "middle", bold: true, fontSize: FS.green,
  color: "FFFFFF", fontFace: "Arial", margin: 0, lineSpacing: 18,
});

// dark-red Classification Model (x324..515, y205..323): L1 bold + 2 italic lines
slide.addShape(pres.ShapeType.rect, {
  x: px(324), y: px(205), w: px(192), h: px(119),
  fill: { color: "9F0000" }, line: { type: "none" },
});
slide.addText([
  { text: "Classification Model", options: { breakLine: true, bold: true, italic: false } },
  { text: "(with Model", options: { breakLine: true, bold: false, italic: true, fontSize: FS.drIt } },
  { text: "Parameters)", options: { bold: false, italic: true, fontSize: FS.drIt } },
], {
  x: px(324), y: px(205), w: px(192), h: px(119),
  align: "center", valign: "middle", fontSize: FS.drL1,
  color: "FFFFFF", fontFace: "Arial", margin: 0, lineSpacing: 18,
});

// light-cyan Predicted Output (Label) (x550..654, y226..302), 3 dark bold lines
slide.addShape(pres.ShapeType.rect, {
  x: px(550), y: px(226), w: px(105), h: px(77),
  fill: { color: "DFFCFB" }, line: { type: "none" },
});
slide.addText([
  { text: "Predicted", options: { breakLine: true } },
  { text: "Output", options: { breakLine: true } },
  { text: "(Label)", options: {} },
], {
  x: px(550), y: px(226), w: px(105), h: px(77),
  align: "center", valign: "middle", bold: true, fontSize: FS.cyan,
  color: "000000", fontFace: "Arial", margin: 0, lineSpacing: 15,
});

// underline under "Predicted" (crop-B check, PIL-confirmed in original: 1px dark
// stroke y255, x573..630; cropB_judge.txt MINOR #1 — fixed pre-judge, attempt 2)
slide.addShape(pres.ShapeType.line, {
  x: px(573), y: px(255.5), w: px(57), h: 0,
  line: { color: "000000", width: 1 },
});

// beige vertical Error box (x691..726, y206..322), dark text rotated 90 CW
slide.addShape(pres.ShapeType.rect, {
  x: px(691), y: px(206), w: px(36), h: px(117),
  fill: { color: "F6DEC6" }, line: { type: "none" },
});
slide.addText("Error", {
  x: px(693.5), y: px(206), w: px(36), h: px(117),
  align: "center", valign: "middle", bold: true, fontSize: FS.err,
  color: "000000", fontFace: "Arial", margin: 0, vert: "vert",
});

// pale-yellow True Label box (x761..859, y238..291), 2 dark bold lines
slide.addShape(pres.ShapeType.rect, {
  x: px(761), y: px(238), w: px(99), h: px(54),
  fill: { color: "FAFFD6" }, line: { type: "none" },
});
slide.addText([
  { text: "True Label", options: { breakLine: true } },
  { text: "of the Sample", options: {} },
], {
  x: px(760), y: px(238), w: px(99), h: px(54),
  align: "center", valign: "middle", bold: true, fontSize: FS.tl,
  color: "000000", fontFace: "Arial", margin: 0, lineSpacing: 15,
});

// ---- 5. red arrows (shaft 1.5pt + explicit measured triangle heads) ----
function arrow(x0, x1, head) {
  slide.addShape(pres.ShapeType.line, {
    x: px(x0), y: px(265), w: px(x1 - x0), h: 0,
    line: { color: "CC0000", width: 1.5 },
  });
  slide.addShape(pres.ShapeType.triangle, {
    x: px(head.x0), y: px(head.y0), w: px(head.x1 - head.x0), h: px(head.y1 - head.y0),
    rotate: head.dir === "left" ? 270 : 90,
    fill: { color: "CC0000" }, line: { color: "CC0000", width: 0 },
  });
}
arrow(268, 313, { x0: 313, y0: 259, x1: 323, y1: 269, dir: "right" });  // green -> darkred
arrow(516, 537, { x0: 537, y0: 260, x1: 545, y1: 269, dir: "right" });  // darkred -> cyan
arrow(659, 679, { x0: 679, y0: 260, x1: 688, y1: 269, dir: "right" });  // cyan -> error
arrow(738, 754, { x0: 728, y0: 260, x1: 737, y1: 269, dir: "left" });   // truelabel -> error (left)

// ---- 6. hand-drawn blue emphasis rects over cyan + truelabel boxes ----
// (omit fill option entirely -> <a:noFill/>; passing fill:{type:'none'} paints theme fill)
slide.addShape(pres.ShapeType.rect, {
  x: px(546), y: px(223), w: px(111), h: px(80),
  line: { color: "0000CC", width: 1 },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(756), y: px(232), w: px(106), h: px(65),
  line: { color: "0000CC", width: 1 },
});

// ---- 7. gray curved arrows from the label (custGeom bezier, pattern law) ----
function curve(P0, C1, C2, P3) {
  slide.addShape(pres.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5,               // full-slide bbox; absolute inch points
    line: { color: "808080", width: 1 },          // NO fill option -> <a:noFill/>
    points: [
      { x: px(P0[0]), y: px(P0[1]), moveTo: true },
      { x: px(P3[0]), y: px(P3[1]),
        curve: { type: "cubic", x1: px(C1[0]), y1: px(C1[1]), x2: px(C2[0]), y2: px(C2[1]) } },
    ],
  });
}
// left: label left side (378,150) down-left to green box top (199,233); LSQ fit err 1.9px
curve([378, 150], [321.6, 160.1], [204.9, 150.5], [199, 233]);
// right: label right corner (609,170) arc right-down to (803,227); LSQ fit err 2.1px
curve([609, 170], [617.7, 156.9], [814.4, 145.4], [803, 227]);
// small gray head triangles at the measured tip bobs
slide.addShape(pres.ShapeType.triangle, {
  x: px(194), y: px(227), w: px(9), h: px(10), rotate: 180,
  fill: { color: "808080" }, line: { color: "808080", width: 0 },
});
slide.addShape(pres.ShapeType.triangle, {
  x: px(799), y: px(221), w: px(9), h: px(10), rotate: 180,
  fill: { color: "808080" }, line: { color: "808080", width: 0 },
});

// ---- 8. handwriting annotations (blue ink) ----
slide.addText("X", {
  x: px(226), y: px(182), w: px(38), h: px(36),
  align: "center", valign: "middle", bold: true, italic: true, fontSize: FS.hand,
  color: "0000CC", fontFace: "Arial", margin: 0,
});
slide.addShape(pres.ShapeType.line, {
  x: px(236), y: px(221), w: px(11), h: 0,
  line: { color: "0000CC", width: 1.5 },
});
// y-hat above Predicted Output: mathtext PNG 600dpi (professional 2D format)
slide.addImage({
  path: VP + "/recreated_pptx/build/assets/eq_yhat_020.png",
  x: px(601.4), y: px(186), w: 176 / 600, h: 300 / 600,   // exact px/600, never rescaled
});
slide.addText("y", {
  x: px(798), y: px(186), w: px(34), h: px(36),
  align: "center", valign: "middle", bold: true, italic: true, fontSize: FS.hand,
  color: "0000CC", fontFace: "Arial", margin: 0,
});

// ---- 9. key sentence (x108..761 ink; box centered on 434.5) ----
slide.addText([
  { text: "Try to obtain model parameters by minimizing the ", options: { color: "CC0000" } },
  { text: "Error", options: { color: "0000CC" } },
  { text: " (Loss Function)", options: { color: "CC0000" } },
], {
  x: px(70.5), y: px(352.5), w: px(729), h: px(28),
  align: "center", valign: "middle", bold: true, fontSize: FS.sent,
  fontFace: "Arial", margin: 0,
});

// ---- 10. note box (x103..869, y402..510) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(103), y: px(402), w: px(767), h: px(109),
  fill: { color: "FFFDE7" }, line: { color: "C00000", width: 0.75 },
});
// three single-line boxes at measured ink bands (left-aligned x112)
// NOTE (attempt 3): original note-box text is SERIF (Times-like) — PIL N-glyph
// test shows 3-4px serif caps on 2px stems (cropC_judge MAJOR #2, confirmed).
slide.addText([
  { text: "Note:", options: { color: "000000", bold: true } },
], {
  x: px(112), y: px(417.5), w: px(750), h: px(22),
  align: "left", valign: "middle", fontSize: FS.note1, fontFace: "Times New Roman", margin: 0,
});
slide.addText([
  { text: "There are three terms that are commonly used interchangeably ", options: { color: "000000" } },
  { text: "(though there is a difference)", options: { color: "C00000", italic: true } },
], {
  x: px(112), y: px(451), w: px(750), h: px(22),
  align: "left", valign: "middle", fontSize: FS.note2, fontFace: "Times New Roman", margin: 0,
});
slide.addText([
  { text: "Loss", options: { color: "C00000", bold: true } },
  { text: " function , ", options: { color: "000000" } },
  { text: "Error", options: { color: "C00000", bold: true } },
  { text: " function, and ", options: { color: "000000" } },
  { text: "Objective", options: { color: "C00000", bold: true } },
  { text: " function ", options: { color: "000000" } },
], {
  x: px(112), y: px(481.5), w: px(460), h: px(26),
  align: "left", valign: "middle", fontSize: FS.note3, fontFace: "Times New Roman", margin: 0,
});
// attempt 6: ")" RESTORED per the spec's verbatim_text "(to be discussed later)"
// (17_worker_instructions: spec text is authoritative; the frame-vs-spec override
// is scoped to GEOMETRY). Judges 3/3 read the ")" in the original; 1px scan of
// x725..755 shows only JPEG ghosting — recorded as an unresolved frame/spec note.
// Original black "function" ends x537, gap x538..556, "(" at x557 (note3 19pt
// reproduces the black width and the gap).
slide.addText([
  { text: "(to be discussed later)", options: { color: "0000CC" } },
], {
  x: px(558), y: px(481.5), w: px(195), h: px(26),
  align: "left", valign: "middle", fontSize: FS.blue3, fontFace: "Times New Roman", margin: 0,
});
// handwritten "Cost" after the blue text (original x756..818, y479..504; blue ink
// — cropC BLOCKER + full-judge MINOR 1, PIL-confirmed via ASCII map)
slide.addText("Cost", {
  x: px(752), y: px(474), w: px(70), h: px(36),
  align: "center", valign: "middle", bold: true, italic: true, fontSize: FS.hand,
  color: "0000CC", fontFace: "Arial", margin: 0,
});

// ---- title LAST so it sits above the panel (house chrome title is per-slide measured here) ----
slide.addText([
  { text: "How to obtain the BEST model parameters ", options: { color: "B22222" } },
  { text: "(W)", options: { color: "0000CC" } },
], {
  x: px(60), y: px(72), w: px(842), h: px(36),
  align: "center", valign: "middle", bold: true, fontSize: FS.title,
  fontFace: "Arial", margin: 0,
});

// hand-drawn blue underline under the "W" of "(W)" (original y101-102, x732-760;
// full-judge MINOR 2, PIL-confirmed contiguous stroke)
slide.addShape(pres.ShapeType.line, {
  x: px(732), y: px(102), w: px(27), h: 0,
  line: { color: "0000CC", width: 1 },
});

pres.writeFile({ fileName: VP + "/recreated_pptx/slide_020_recreated.pptx" })
  .then(() => console.log("wrote slide_020_recreated.pptx"));
