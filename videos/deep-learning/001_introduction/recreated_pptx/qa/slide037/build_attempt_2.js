// slide_037.js — 001_introduction slide 37 "How many filter can we apply on the image"
// (Deep Learning DSAI 308) — CHILD of certified slide 36 (dependency edge 37<-36).
//
// DEPENDENCY CONTRACT: requires the CERTIFIED parent component by absolute path and calls
// renderBase for the shared chrome + the white-panel construct (opts.geom override to this
// frame's measured panel geometry). The parent's other blocks are SKIPPED — slide 37's
// frame REPLACES the filter/neuron/question/equation right side and REDRAWS the slab unit
// smaller under its own yellow explanation box (template-match of the parent's slab tiles
// against this frame failed: meanDiff 62-95 — different drawing/geometry; per the
// dependency law the child's frame is ground truth for every element, inherited included,
// so the diagram is cropped from THIS frame — imagery law, slide-034/036 precedent).
//
// FOUNDER CROWDING DIRECTIVE (2026-10-12): the original slide 37 is content-crowded
// (founder note; it crams 36's diagram under an added explanation box). Resolution:
//   FIXED (deliberate spacing deviation, documented): the red equation ink is placed 8
//     frame-px LOWER than the original (ink top 479 -> 487). The original's equation band
//     (y479..494) interleaves the question's descender band (to y483); the shift gives the
//     caption pair a clean 4px band gap and keeps 9px clearance to the panel border
//     (original had 16px; the pair's "directly below" intent is preserved).
//   REPRODUCED at measured geometry (tight but non-overlapping in the original):
//     question ascenders 4px under the cube's bottom stroke; yellow-box text pads
//     (13 top / 5 bottom, 9 left); 'RGB' label 7px under the panel border.
//   INSEPARABLE (reproduced faithfully via frame crops, documented): filter-cluster
//     overlap density, tiny '7' labels on the dashed lines, dashed-line clutter,
//     'Depth=5 dims' flush against the cube's top edge.
//
// Measured constants (frame 960x540, 1px = 1pt, in = px/72) — scratch/slide037/
// measure1-5.py + fit_fonts_037.py (banked):
//   title   one line, ink x128..837 (cx 482.5) y80..112 (cap 24-25px) — Arial Bold 35pt
//           (adv fit 714 vs 709, deck title precedent 036=35pt), red C00000
//   ybox    fill x66..903 y138..242; borders TOP rows 136-137 / BOTTOM rows 243-244 /
//           LEFT cols 64-65, modal ~(185,186,170) — 3-sided muted border #B7BAAB
//           (measured: NO right border stroke — right edge is a plain yellow-to-gray
//           fade; reproduced as 3 line shapes). Fill FFFFE1 (spec; modal FBFDE5 = JPEG
//           read of the same).
//   ytext   3 visual lines, Times New Roman 26pt (mixed-run adv fit: L1 812/803,
//           L2 344/336, L3 727/718 — consistent +1%), pitch 33 (measured 34/32),
//           ink left x75 all lines; bold runs: 'multiple filters', FIRST 'same
//           location' bold #990000 (spec-validated segment color), 'detect edges',
//           'detect lines', 'detect curves' — verbatim wrap after 'filters on'
//   panel   white panel: border cols x65/x896, top row y262, bottom row y511
//           (stroke (142,34,49) = JPEG-darkened C00000; frame 36 has NO x65/x896 lines
//           -> real borders of THIS frame). x58 dark line exists in BOTH frames 36/37
//           -> video artifact, not recreated (certified 036 precedent).
//   diagram tile (68,266)-(894,451) 826x185 — edge-safety verified (top row 266 clean,
//           bottom crop boundary on clean row 451; cube bottom stroke 448-450 fully in).
//   question ink x73..583 (cx 328) y453..483 — Comic Sans MS 27.5pt (adv 510.5 vs 510)
//   equation ink x196..417 y479..494 (222x16) — mathtext '5 \; \cdot \; 7 \; \cdot \;
//           7 \; \cdot \; 3 \; = \; 735' 22.5pt #D42A2A (certified 036 equation red),
//           ink 220.6x17.2 vs 222x16 within tolerance; sidecar eq_735_037.json
//   letterbox black strip rows 519..539 = video-player artifact — NOT recreated
//           (ground rule (c); certified 034/040/036 precedent)
//
// LAWS honored: playlist chrome via the parent's shared module (numeral "37" = file
// number, assumption PENDING FOUNDER VETO per 001_introduction/AGENTS.md); verbatim text
// incl. 'filter' singular, 'We can Apply', double space after 'location.', '[... ...etc)'
// mismatched brackets; margin:0 + explicit fontFace + explicit lineSpacing everywhere;
// no '#' in pptxgenjs hex; single-version deliverable; equation professional-format law
// (matplotlib mathtext PNG, exact size, never rescaled).

const pptxgen = require("pptxgenjs");
const {
  renderBase, px, ASSETS,
} = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_036.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_037_recreated.pptx";

// ---- measured palette / geometry (this frame) ------------------------------------
const RED = "C00000";
const BLACK = "000000";
const YBOX_FILL = "FFFFE1";
const YBOX_BORDER = "B7BAAB";
const EQ_RED = "D42A2A";
const SEG_RED = "990000"; // bold 'same location' — spec-validated segment color
const SANS = "Arial";
const SERIF = "Times New Roman";
const SCRIPT = "Comic Sans MS";

const TITLE = { cx: 482.5, cy: 96, centerShift: -3, text: "How many filter can we apply on the image" };
const YBOX = { x: 64, y: 136, w: 841, h: 109 };           // rect incl. border strokes
const YTEXT = { x: 74, y: 136, w: 828, h: 109, pitch: 33, size: 26, centerShift: -1 };
const PANEL = { x: 65, y: 262, w: 832, h: 250 };          // -> parent content_box geom
const DIAGRAM = { x: 68, y: 266, wIn: 826 / 72, hIn: 185 / 72, img: "diagram037.png" };
const QUESTION = { cx: 328, cy: 468, centerShift: -4, text: "How many weights for these 5 neurons?" };
const EQ = { inkLeft: 196, inkTopPlaced: 487, padIn: 8 / 600, wIn: 3.09, hIn: 0.265,
             img: "eq_735_037.png" };

// ---- delta blocks -----------------------------------------------------------------

function drawTitle(pptx, slide) {
  slide.addText(TITLE.text, {
    x: px(TITLE.cx) - 6, y: px(TITLE.cy + TITLE.centerShift) - 0.4, w: 12, h: 0.8,
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 35, bold: true, color: RED, lineSpacing: 39,
  });
}

function drawYellowBox(pptx, slide) {
  // fill (no outline) ...
  slide.addShape(pptx.ShapeType.rect, {
    x: px(YBOX.x), y: px(YBOX.y), w: px(YBOX.w), h: px(YBOX.h),
    fill: { color: YBOX_FILL },
  });
  // ... plus the measured 3-sided border (2px strokes rows/cols 136-137/243-244/64-65;
  // NO right stroke in the frame — right edge is a plain yellow-to-gray fade)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(YBOX.x), y: px(YBOX.y), w: px(YBOX.w), h: px(2),
    fill: { color: YBOX_BORDER }, line: { color: YBOX_BORDER, width: 0.25 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(YBOX.x), y: px(YBOX.y + YBOX.h - 2), w: px(YBOX.w), h: px(2),
    fill: { color: YBOX_BORDER }, line: { color: YBOX_BORDER, width: 0.25 },
  });
  slide.addShape(pptx.ShapeType.rect, {
    x: px(YBOX.x), y: px(YBOX.y), w: px(2), h: px(YBOX.h),
    fill: { color: YBOX_BORDER }, line: { color: YBOX_BORDER, width: 0.25 },
  });
}

function drawYellowText(pptx, slide) {
  const t = YTEXT;
  const reg = { fontFace: SERIF, fontSize: t.size, color: BLACK };
  slide.addText(
    [
      // L1 — verbatim wrap after 'filters on'; FIRST 'same location' bold dark-red
      { text: "We can Apply ", options: { ...reg } },
      { text: "multiple filters", options: { ...reg, bold: true } },
      { text: " on the ", options: { ...reg } },
      { text: "same location", options: { ...reg, bold: true, color: SEG_RED } },
      { text: " (e.g. 5 different filters on", options: { ...reg, breakLine: true } },
      // L2 — double space after 'location.' verbatim; second 'same location' regular
      { text: "the same location.  For Example:", options: { ...reg, breakLine: true } },
      // L3 — verbatim mismatched '[ ... ...etc)'
      { text: "[ one to ", options: { ...reg } },
      { text: "detect edges", options: { ...reg, bold: true } },
      { text: ", one to ", options: { ...reg } },
      { text: "detect lines", options: { ...reg, bold: true } },
      { text: ", one to ", options: { ...reg } },
      { text: "detect curves", options: { ...reg, bold: true } },
      { text: ", ...etc)", options: { ...reg } },
    ],
    {
      x: px(t.x), y: px(t.y + t.centerShift), w: px(t.w), h: px(t.h),
      align: "left", valign: "middle", margin: 0, lineSpacing: t.pitch,
    }
  );
}

function drawDiagram(pptx, slide) {
  slide.addImage({
    path: ASSETS + "/" + DIAGRAM.img,
    x: px(DIAGRAM.x), y: px(DIAGRAM.y), w: DIAGRAM.wIn, h: DIAGRAM.hIn,
  });
}

function drawQuestion(pptx, slide) {
  slide.addText(QUESTION.text, {
    x: px(QUESTION.cx) - 6, y: px(QUESTION.cy + QUESTION.centerShift) - 0.4, w: 12, h: 0.8,
    align: "center", valign: "middle", margin: 0,
    fontFace: SCRIPT, fontSize: 27.5, color: BLACK, lineSpacing: 34,
  });
}

function drawEquation(pptx, slide) {
  // CROWDING FIX: inkTop placed 487 = original 479 + 8 (see header note)
  slide.addImage({
    path: ASSETS + "/" + EQ.img,
    x: px(EQ.inkLeft) - EQ.padIn, y: px(EQ.inkTopPlaced) - EQ.padIn,
    w: EQ.wIn, h: EQ.hIn,
  });
}

// ---- composition -------------------------------------------------------------------

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Parent's certified composition: playlist chrome (numeral "37") + white-panel
// construct at THIS frame's measured geometry. Everything else is this slide's delta.
renderBase(pres, slide, {
  numeral: "37",
  skip: ["title", "slab_top", "slab_body", "filter_unit", "equals", "plus",
         "neuron", "arrow_neuron", "question", "equation"],
  geom: { content_box: { x: PANEL.x, y: PANEL.y, w: PANEL.w, h: PANEL.h } },
});

drawTitle(pres, slide);
drawYellowBox(pres, slide);
drawYellowText(pres, slide);
drawDiagram(pres, slide);
drawQuestion(pres, slide);
drawEquation(pres, slide);

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
