// slide_042.js — "Batch Data (Feature Vectors)" (Deep Learning DSAI 308, video 002, slide 42)
// P3 pattern-group HEAD ([42,43,44]) — cube-tensor diagram family.
//
// CONTENT SPEC: analysis/slide_042_final.json (verbatim labels). Frame-of-record wins where
// the spec's vision estimates disagreed with pixels (documented in qa/slide042/worker_report.md):
//   * middle grid = 4 cols x 5 rows (pixel-measured pitch 31px, x379..512) — the banked
//     transcript's "5x5" was wrong; spec right.
//   * right block layer colors front->back = MAGENTA, GREEN, ORANGE, YELLOW, BLUE
//     (side strips + top strips pixel-measured); spec's "yellow,orange,green" order wrong.
//   * label run colors pixel-measured: count words GREEN ("One Input Sample", "FIVE Input
//     Samples"), "(Using ... filters ...)" phrases BLUE, "[...]" brackets MAGENTA
//     ("[ 4 Channels]", "[mini-Batch]"), rest RED. Spec's red/blue assignments corrected.
//   * NO white/gray "stacking arrow": the whitish pixels are the background wedge between the
//     staircase slabs (pixel-verified x636-670/y280-305 pure white). Omitted (ground rule (c)).
//   * "Batch size (5 samples)" label + diagonal double-headed arrow at measured positions.
//
// CHROME LAW: shared playlist module drawHouseChrome (badge numeral 42).
// FRAME->SLIDE MAPPING (fitted from this frame's four chrome landmarks: left x59, right x901,
// top y43, bottom stroke y516 <-> slide 42/919/45/539.5):
//   frame_x = 18.66 + 0.96055 * slide_x ;  frame_y = 0.95556 * slide_y
// All ink below is in TRUE slide coordinates through this transform. Letterbox (y>=518) and
// video artifacts omitted (judge ground rule (c)).
//
// DIAGRAMS: the three cube illustrations are PIL-generated PNGs (build/assets/s042_*.png,
// generator scratch/slide042/gen_final.py; universal measured cube-wall model: flat front
// rects with bright right-edge zones + sheared dark top bands with bright gaps), embedded at
// exact size (frame px / scale / 72 in). Closed-loop PIL checks before judging.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_042_recreated.pptx";

const RED = "C00000", GREEN = "66CC00", BLUE = "0000CC", MAGENTA = "CC00CC";
const FONT = "Arial";
const pt = (v) => v / 72;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();

// ---- 1. playlist house chrome (badge 42) ----
drawHouseChrome(pres, s, { numeral: 42 });

// ---- 2. title: measured ink center x 492.2pt, cap top 77.4pt -> 43pt bold ----
s.addText("Batch Data (Feature Vectors)", {
  x: (492.2 - 432) / 72, y: (77.4 - 0.25 * 43) / 72, w: 12, h: pt(1.5 * 43),
  align: "center", valign: "top",
  fontSize: 43, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- 3. blue content frame: frame px x69..889.5, y134.5..510 ----
s.addShape(pres.ShapeType.rect, {
  x: pt((69 - 18.66) / 0.96055), y: pt(134.5 / 0.95556),
  w: pt((889.5 - 69) / 0.96055), h: pt((510 - 134.5) / 0.95556),
  fill: { type: "none" }, line: { color: BLUE, width: 2.5 },
});

// ---- 4. label boxes (white fill, thin red border) ----
// LEFT: frame x77..330, y195..236 ; MID: x341..598, y193..235 ; RIGHT: x627..882, y165..227
const box = (fx0, fy0, fx1, fy1) => ({
  x: pt((fx0 - 18.66) / 0.96055), y: pt(fy0 / 0.95556),
  w: pt((fx1 - fx0) / 0.96055), h: pt((fy1 - fy0) / 0.95556),
});
s.addShape(pres.ShapeType.rect, { ...box(77, 195, 330, 236), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });
s.addShape(pres.ShapeType.rect, { ...box(341, 193, 598, 235), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });
s.addShape(pres.ShapeType.rect, { ...box(627, 165, 882, 227), fill: { color: "FFFFFF" }, line: { color: RED, width: 1 } });

// ---- 5. label box texts (verbatim runs, pixel-measured colors) ----
const R = (t) => ({ text: t, options: { color: RED } });
const G = (t) => ({ text: t, options: { color: GREEN } });
const B = (t) => ({ text: t, options: { color: BLUE } });
const M = (t) => ({ text: t, options: { color: MAGENTA } });
const FS = 14, LSB = 18; // label font size / line spacing (measured pitch 17.8pt)

// LEFT box: two lines centered at frame cx 188 -> slide 176.3
s.addText([
  R("Feature Vector of "), G("One Input"), { text: "", options: { breakLine: true } },
  G("Sample "), B("(Using one filter)"),
], {
  x: (176.3 - 273.6/2) / 72, y: (210.4 - 0.25 * FS) / 72, w: 3.8, h: 2.2 * LSB / 72,
  align: "center", valign: "top", fontSize: FS, bold: true, fontFace: FONT,
  lineSpacing: LSB, margin: 0,
});

// MID box: two lines centered at frame cx 469 -> slide 468.9
s.addText([
  R("Feature Vectors of "), G("One Input Sample"), { text: "", options: { breakLine: true } },
  B("(Using 4 filters)  "), M("[ 4 Channels]"),
], {
  x: (468.9 - 273.6/2) / 72, y: (210.4 - 0.25 * FS) / 72, w: 3.8, h: 2.2 * LSB / 72,
  align: "center", valign: "top", fontSize: FS, bold: true, fontFace: FONT,
  lineSpacing: LSB, margin: 0,
});

// RIGHT box: three lines, left-aligned at frame x~632 -> slide 638.2
s.addText([
  R("Feature Vectors of :"), { text: "", options: { breakLine: true } },
  G("FIVE Input Samples "), M("[mini-Batch]"), { text: "", options: { breakLine: true } },
  B("Using 4 filters "), M("[ 4 Channels]"),
], {
  x: 638.2 / 72, y: (180.0 - 0.25 * FS) / 72, w: 3.4, h: 3.2 * LSB / 72,
  align: "left", valign: "top", fontSize: FS, bold: true, fontFace: FONT,
  lineSpacing: LSB, margin: 0,
});

// ---- 6. the three cube diagrams (PIL-generated, exact placement) ----
// left stack: frame (168,262) 43x167 ; mid grid: (379,254) 139x165 ; right block: (640,228) 236x250
s.addImage({ path: `${A}/s042_left_stack.png`,
  x: pt((168 - 18.66) / 0.96055), y: pt(262 / 0.95556), w: pt(43 / 0.96055), h: pt(167 / 0.95556) });
s.addImage({ path: `${A}/s042_mid_grid.png`,
  x: pt((379 - 18.66) / 0.96055), y: pt(254 / 0.95556), w: pt(139 / 0.96055), h: pt(165 / 0.95556) });
s.addImage({ path: `${A}/s042_right_block.png`,
  x: pt((637 - 18.66) / 0.96055), y: pt(225 / 0.95556), w: pt(236 / 0.96055), h: pt(250 / 0.95556) });

// ---- 7. red dimension arrows (double-headed, native) ----
const AR = { color: RED, width: 2.25, beginArrowType: "triangle", endArrowType: "triangle" };
// vertical: frame (643,325)..(643,467)
s.addShape(pres.ShapeType.line, {
  x: pt((643 - 18.66) / 0.96055), y: pt(325 / 0.95556), w: 0, h: pt((467 - 325) / 0.95556),
  line: { ...AR },
});
// horizontal: frame (641,461)..(820,461)
s.addShape(pres.ShapeType.line, {
  x: pt((641 - 18.66) / 0.96055), y: pt(461 / 0.95556), w: pt((820 - 641) / 0.96055), h: 0,
  line: { ...AR },
});
// diagonal: frame (818,463)..(864,405) (bottom-left -> top-right)
s.addShape(pres.ShapeType.line, {
  x: pt((818 - 18.66) / 0.96055), y: pt(405 / 0.95556), w: pt((864 - 818) / 0.96055), h: pt((463 - 405) / 0.95556),
  flipV: true, line: { ...AR },
});

// ---- 8. axis labels ----
// "Feature Vector": rotated 90 CCW (reads bottom-to-top), center frame (633.5, 391)
s.addText("Feature Vector", {
  x: 639.4/72 - 0.75, y: 409.2/72 - 0.14, w: 1.5, h: 0.28,
  align: "center", valign: "middle", rotate: 270,
  fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// "Channels" / "(4 Filters)" under the horizontal arrow (measured centers)
s.addText("Channels", {
  x: 704.5/72 - 0.7, y: (493.8 - 0.25 * 12) / 72, w: 1.4, h: 0.26,
  align: "center", valign: "top", fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("(4 Filters)", {
  x: 695.5/72 - 0.7, y: (510.7 - 0.25 * 12) / 72, w: 1.4, h: 0.26,
  align: "center", valign: "top", fontSize: 12, bold: true, color: RED, fontFace: FONT, margin: 0,
});
// diagonal labels, rotated 315 (reading along the depth diagonal)
s.addText("Batch size", {
  x: 858.2/72 - 0.55, y: 440.6/72 - 0.11, w: 1.1, h: 0.22,
  align: "center", valign: "middle", rotate: 315,
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});
s.addText("(5 samples)", {
  x: 836.3/72 - 0.55, y: 457.3/72 - 0.11, w: 1.1, h: 0.22,
  align: "center", valign: "middle", rotate: 315,
  fontSize: 10, bold: true, color: RED, fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
