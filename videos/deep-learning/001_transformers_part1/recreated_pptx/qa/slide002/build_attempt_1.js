// Slide 002 — "Transformers / Part I / Aug. 2020" section title slide
// (Deep Learning DSAI 308, Transformers — Part I)
//
// Geometry: ALL values PIL-measured from unique_slides/slide_002.jpg (960x540 px,
// 1 px = 1 pt = 1/72 in). This deck's house chrome (shared by slides 1/2/3, per the
// frame = ground truth law in the video AGENTS.md) is: white outer canvas, light-gray
// content panel with a thin dark-red border (panel bottom edge sits at the slide
// bottom, bleeding off — bottom stroke half-visible), yellow badge with a PURPLE
// outline top-right inside the panel, numeral = the number printed on the original.
// The ml-intro house values (E8E8E8 full-bleed bg, frame inset 0.15in all around,
// outline-less badge) do NOT match this deck's shared template; spec colors/geometry
// and frame measurements win here (SOURCES.md: badge outline hue confirmed from frame).
//
// Omitted: the small gray '+' crosshair at ~(40%, 68%) — flagged by the spec as a
// likely cursor/alignment artifact (judge GROUND RULES (c); spec brief step 7 "omit").
//
// pptxgenjs laws: no '#' in hex, fontFace everywhere, margin:0, single-line boxes.

const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const FONT = "Arial";

// spec colors (validated slide_002_final.json)
const RED = "C00000";        // panel border + all text
const PANEL = "E9E9E7";      // panel fill (frame-measured #E8E8E8 family)
const BADGE_FILL = "FDFD96"; // badge fill (frame-measured #FFFF9B family)
const BADGE_LINE = "6A5ACD"; // badge outline purple (spec; SOURCES.md frame-confirm)
const NUM_INK = "333333";    // badge numeral

const s = pres.addSlide();
s.background = { color: "FFFFFF" };

// 1) Panel — measured: left stroke center 39.5px=0.549in, top 43px=0.597in,
//    right 920.5px=12.785in, bottom path ~539px=7.49in (stroke half-visible at edge).
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.549, y: 0.597, w: 12.236, h: 6.893,
  fill: { color: PANEL }, line: { color: RED, width: 1.5 },
});

// 2) Badge — outer bbox x 872..914, y 53..90 px -> center (12.403, 0.993)in,
//    path size ~42x37 px = 0.583x0.514 in. Numeral '2' digit-height ~11px -> 16pt.
s.addShape(pres.shapes.OVAL, {
  x: 12.112, y: 0.736, w: 0.583, h: 0.514,
  fill: { color: BADGE_FILL }, line: { color: BADGE_LINE, width: 2 },
});
s.addText("2", {
  x: 12.112, y: 0.736, w: 0.583, h: 0.514,
  align: "center", valign: "middle", fontSize: 16, color: NUM_INK,
  fontFace: FONT, margin: 0,
});

// 3) Title "Transformers" — band y 196..249px (center 222.75px = 3.094in),
//    width 466px -> em ~72pt (6.446em advance). Box centered on panel width.
//    Calibrated on the 150dpi render: 73.5pt matches the measured ink width AND
//    cap height (LO Arial-bold rendering is ~2% narrow vs the frame at 72pt).
s.addText("Transformers", {
  x: 0.549, y: 2.454, w: 12.236, h: 1.2,
  align: "center", valign: "middle", fontSize: 73.5, bold: true,
  color: RED, fontFace: FONT, margin: 0,
});

// 4) Subtitle "Part I" — band y 276.5..312.5px (center 294.5px = 4.090in).
//    Cap height matches 50pt exactly but the frame glyphs run ~6.7% wider than
//    LO Arial-bold at that size -> reproduce with charSpacing 1.4pt (measured:
//    +17.5px @150dpi over 6 glyphs), NOT a larger font (that would overshoot height).
s.addText("Part I", {
  x: 0.549, y: 3.610, w: 12.236, h: 0.9,
  align: "center", valign: "middle", fontSize: 50, bold: true,
  charSpacing: 1.4, color: RED, fontFace: FONT, margin: 0,
});

// 5) Date "Aug. 2020" — band y 338..358.5px, line center ~346.5px = 4.813in;
//    measured text center x 490.5px = 6.812in (sits right of panel center in the
//    original frame — reproduced, not "fixed").
s.addText("Aug. 2020", {
  x: 5.812, y: 4.518, w: 2.0, h: 0.55,
  align: "center", valign: "middle", fontSize: 23, bold: true, italic: true,
  color: RED, fontFace: FONT, margin: 0,
});

pres
  .writeFile({
    fileName:
      "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_002_recreated.pptx",
  })
  .then(() => console.log("OK slide_002_recreated.pptx"));
