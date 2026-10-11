// slide_003.js — "Transformers – Part I" agenda slide (deep-learning/001_transformers_part1)
// Build pattern per scripts/17_worker_instructions.md + patterns/house-chrome/example.js
// + patterns/explicit-line-spacing/example.js.
//
// Spec: analysis/slide_003_final.json (PASS_WITH_FIXES, score 9). Frame measured
// 960x540 px (1px = 1pt = 1/72 in) via scratch/slide003/measure_frame*.py:
//   title ink  x=[223,620] y=[70,98]  -> ~40pt Arial Bold (cap 29px), color spec CC0000
//   agenda ink x=[111,380] y=[172,310]; 4 line bands start y=172,214,255,296
//     -> pitch 41.33pt, ~20pt Arial Bold (LiberationSans-Bold fit: all 4 lines within 2px)
//   bottom red line: y=[537,539] x=[38,921] (spec recreation_brief step 3)
//   mouse-cursor artifact in original -> video artifact, correctly omitted (judge GR (c))
// House chrome overrides spec/judge: frame 0.15in inset C00000 1.5, badge FFF9C4,
// title box y:0.28 x:0.6 w:12.13 centered. Badge numeral = printed number = 3.

const pptxgen = require("pptxgenjs");

const NUM = 3;
const TITLE = "Transformers \u2013 Part I"; // en dash, verbatim
const LINES = [
  "Processing Sequential Data",
  "Transformer Building Blocks",
  "Self Attention Mechanism", // "Self" confirmed from frame pixels (probe_original.txt)
  "Multi-Head  Attention", // double space verbatim (confirmed from frame pixels)
];
const FONT = "Arial";

// measured geometry (inches; 1 original px = 1/72 in)
const PITCH_PT = 41.33;          // agenda band-start pitch 42/41/41 px
const AGENDA_FONT = 20;          // LiberationSans-Bold fit 19.7pt -> authored 20pt
const AGENDA_BOX_X = 1.534;      // leftmost ink 111px=1.542in minus 'T' left bearing
const AGENDA_Y0 = 2.079;         // closed-loop corrected: render_1 sat +33px low; 2.30-33.2/150
const AGENDA_W = 4.7;            // longest line 3.75in + >=20% wrap budget
const AGENDA_H = 2.5;
const TITLE_FONT = 40;           // cap 29px -> 40.5pt Arial Bold
const BOTTOM_LINE = { x: 38 / 72, w: 884 / 72, yCenter: 538.5 / 72, wpt: 2.25 }; // y=[537,539]px

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;
const s = pres.addSlide();
s.background = { color: "E8E8E8" };

// 1. house outer red frame (0.15in inset from every edge) — house law
s.addShape(pres.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { type: "none" },
  line: { color: "C00000", width: 1.5 },
});

// 2. slide-number badge (house law) — numeral = printed number on original = 3
s.addShape(pres.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText(String(NUM), {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: "333333", fontFace: FONT, margin: 0,
});

// 3. title (house box position; content verbatim from spec)
s.addText(TITLE, {
  x: 0.6, y: 0.28, w: 12.13, h: 0.8,
  align: "center", valign: "top",
  fontSize: TITLE_FONT, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
});

// 4. agenda block — 4 lines, explicit pinned pitch (single knob, no paraSpaceAfter)
s.addText(
  LINES.map((t, i) => ({ text: t, options: { breakLine: i < LINES.length - 1 } })),
  {
    x: AGENDA_BOX_X, y: AGENDA_Y0, w: AGENDA_W, h: AGENDA_H,
    fontSize: AGENDA_FONT, bold: true, color: "1F1FCC", fontFace: FONT,
    lineSpacing: PITCH_PT, margin: 0, valign: "top", align: "left",
  }
);

// 5. bottom red line (spec recreation_brief step 3, measured ink y=[537,539] x=[38,921])
s.addShape(pres.shapes.LINE, {
  x: BOTTOM_LINE.x, y: BOTTOM_LINE.yCenter, w: BOTTOM_LINE.w, h: 0,
  line: { color: "CC0000", width: BOTTOM_LINE.wpt },
});

pres.writeFile({ fileName: "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_003_recreated.pptx" })
  .then(() => console.log("wrote videos/deep-learning/001_transformers_part1/recreated_pptx/slide_003_recreated.pptx"));
