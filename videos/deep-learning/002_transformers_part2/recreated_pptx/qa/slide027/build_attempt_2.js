// slide_027.js — "Sequence of 5 words / Positions are defined as angles"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 27)
//
// CONTENT SPEC: analysis/slide_027_final.json (verbatim; PASS_WITH_FIXES applied).
// Provenance: slide_027_source/SOURCES.md (Kazemnejad 2-D circle framing confirmed;
// the clock diagram is course-authored — drawn from measured frame geometry, not
// the downloaded figures' pixels).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): shared module
// videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas, gray
// E9E9E7 panel x 42..918px / y 45px..slide bottom, C00000 border (bottom stroke
// half-visible), badge circle d36 at (893,71)px FDFD96 + 6A5ACD ring, numeral 27
// (= number printed on THIS original frame; PIL-verified badge center frame
// (875.7,70.6) d35 -> slide (891.6,73.9), inside house-chrome tolerance).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide027/measure_chrome.py +
// probe_chrome.py): 002 capture zoomed out ~0.958; landmarks left 58.5, right 901.5,
// top 43, bottom 516.5 (identical to slide_002's fit within JPEG noise):
//   frame_x = 18.63 + 0.96123*slide_x ; frame_y = 0.95556*slide_y
//   -> slide_x = (frame_x-18.63)/0.96123 ; slide_y = frame_y/0.95556
// All ink below is mapped to TRUE slide pts through this transform.
//
// MEASURED GEOMETRY (scratch/slide027/measure2.json, probe3/4/5):
// - Title 3 lines: per-line Arial Bold sizes fitted to measured ink widths
//   (L1 "Sequence of 5 words" 240.3pt -> 25pt; L2 "Positions are defined" 242.4pt
//   -> 26pt; L3 "as angles" 108.2pt -> 25pt). Arial/Liberation-metric-exact in both
//   LO and PowerPoint (Verdana would be font-substituted by LO at +9% width).
//   Color C00000/CC0000 red. Ink tops 61.7 / 89.0 / 117.2; L3 indent 65.5pt.
// - Equation box: frame [82,182,216,246] -> slide x 65.9 y 190.5 w 139.5 h 66.9;
//   fill FFFFCC, thin muted gray-olive border (JPEG-faded ~BEC3C3). Text Arial
//   Bold 20pt (width-fit from "t=0,1,2,3,...." ink 96.8pt / 4.809em = 20.1pt),
//   pitch 21pt, per-glyph color runs measured
//   from the frame: "Sin("/"Cos(" BLUE 0000CC, "ω" RED CC0000, "t" GREEN 009900,
//   ")" BLUE, line 3 "t=0,1,2,3,...." GREEN (PIL census: 243 green px, 0 red —
//   overrides the transcript's "maroon" guess; spec green confirmed).
// - Circle: fill r≈130pt center (581.0, 297.2) slide; fill FBFCC9; thin gray-olive
//   ring (JPEG-blended ~C0C3B7). NO dotted spokes exist anywhere in the frame
//   (PIL faint-ink ray scan on all 12 rays found none — the spec's "12 dotted red
//   spokes" is a vision-model hallucination; the only red ink = title, +w labels,
//   border, letterbox).
// - Axis cross (measured, faint): SOLID horizontal line y=296.7 from x 246.9 to
//   905.4 and SOLID vertical line x=581.0 from y 50.2 to 532.8 — visible over the
//   pale fill (olive-darkened columns) and on gray bg (JPEG-faded ~20% gray).
//   Drawn as 6E6E6E @ 60% transparency, 0.75pt.
// - Faint line layer (PIL faint-ink analysis, scratch/slide027/faint_lines.py +
//   polar histograms): DASHED light-gray lines at ALL TWELVE 30-degree spoke
//   positions — the axis cross (0/90/180/270, running through the fill to x
//   246.9..905.4 / y 50.2..532.8) plus eight diagonal spokes from near the
//   center (r~30pt) out to r~240pt (frame r 128..230, 100%/99% of faint annulus
//   ink within 7 deg of 30-degree multiples; NO dotted circles). Dash pattern:
//   frame dashes 9-15px + 1-3px gaps -> 'lgDash' at 0.75pt. Color: JPEG-faded
//   ~20% gray (dips lum 195-209 on bg 231) -> 8C8C8C @ 50% transparency.
// - Word chips: 5 rects 71x24pt centered ON the rim R=182.5 at 0/30/60/90/120 deg
//   (PIL-verified chip centers (762.6,297.2)(738.4,204.6)(672.3,138.6)(581.1,113.3)
//   (490.4,139.9), r 181.6..183.0); fill CCFFCC, border 009933, text Verdana bold
//   italic 12pt 009933; rotations (pptxgenjs cw): 0, -30, -60, -90 (reads
//   bottom-to-top), +60 (reads top-to-bottom per transcript).
// - Arcs: 4 thin orange E06010 curved arrows outside the chips at R≈224 from
//   (src+12deg) to (dst-1.5deg), drawn as 14-segment polylines; solid triangle
//   arrowheads (~9.5pt) just outside each destination chip's outer corner aimed
//   into the chip (PIL head centers slide (776.4,188.4)(692.6,100.5)(585.6,71.2)
//   (473.3,101.5), all r≈224).
// - "+ω" labels ×4 Arial Bold 15pt CC0000 (ink ~21x8px frame), centered at slide
//   (840.2,236.5) L1 W0→W1, (788.8,104.1) L2 W1→W2, (642.8,75.4) L3 W2→W3,
//   (520.6,75.4) L4 W3→W4 — each radially outside its arc midpoint (13/45/75/105
//   deg; PIL red-component bboxes).
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c)):
//   * black letterbox bar frame rows 518..539 (slide y >= 541) — video player strip.
//   * frozen mouse cursor near frame (577..582, 224..230) inside the circle.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const TITLE_RED = "C00000";
const EQ_BLUE = "0000CC", EQ_RED = "CC0000", EQ_GREEN = "009900";
const CIRCLE_FILL = "FBFCC9", CIRCLE_RING = "C0C3B7";
const BOX_FILL = "FFFFCC", BOX_BORDER = "BEC3C3";
const CHIP_FILL = "CCFFCC", CHIP_GREEN = "009933";
const ARC_ORANGE = "E06010";
const ARC_STROKE = "F0C9B0"; // pale salmon — original arc stroke is below the JPEG noise
                             // floor (PIL: no ink at lum<216 along the whole path between
                             // label and head); vision reads converge on "thin pale
                             // salmon/gray delicate curve" (topband a3 + rightband a4)
const LABEL_RED = "CC0000";
const AXIS_GRAY = "993333";  // axis/spoke lines: faded pinkish-red — measured appearance
                             // (209,197,199) on bg 231 / (226,215,185) on fill; three vision
                             // reads call them pinkish/red; 993333 @ 80% transparency
                             // reproduces both measured appearances (computed match)
const TITLE_FONT = "Arial", EQ_FONT = "Arial", CHIP_FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome (panel + border + badge "27")
drawHouseChrome(pres, s, { numeral: 27 });

// ---- 2. circle (fill + thin gray-olive ring), center (581.0, 297.2) r 130.75
s.addShape(pres.ShapeType.ellipse, {
  x: (581.0 - 130.75) / 72, y: (297.2 - 130.75) / 72, w: 261.5 / 72, h: 261.5 / 72,
  fill: { color: CIRCLE_FILL }, line: { color: CIRCLE_RING, width: 1 },
});

// ---- 3. axis cross + 8 diagonal spokes: DASHED light gray (over the fill, as measured)
s.addShape(pres.ShapeType.line, {
  x: 246.9 / 72, y: 296.7 / 72, w: (905.4 - 246.9) / 72, h: 0,
  line: { color: AXIS_GRAY, width: 0.75, transparency: 75, dashType: "lgDash" },
});
s.addShape(pres.ShapeType.line, {
  x: 581.0 / 72, y: 50.2 / 72, w: 0, h: (532.8 - 50.2) / 72,
  line: { color: AXIS_GRAY, width: 0.75, transparency: 75, dashType: "lgDash" },
});
// diagonal spokes: fine dots, r 30..240 pt from the circle center at 30,60,120,150,210,240,300,330 deg
function spoke(deg) {
  const a = (deg * Math.PI) / 180;
  const x1 = 581.0 + 30 * Math.cos(a), y1 = 297.2 - 30 * Math.sin(a);
  const x2 = 581.0 + 240 * Math.cos(a), y2 = 297.2 - 240 * Math.sin(a);
  s.addShape(pres.ShapeType.line, {
    x: Math.min(x1, x2) / 72, y: Math.min(y1, y2) / 72,
    w: Math.abs(x2 - x1) / 72, h: Math.abs(y2 - y1) / 72,
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: AXIS_GRAY, width: 0.75, transparency: 75, dashType: "sysDot" },
  });
}
[30, 60, 120, 150, 210, 240, 300, 330].forEach(spoke);

// ---- 4. word chips (rect+text in one shape, rotated; centers on rim R=182.5)
const chips = [
  { t: "Word 0", cx: 762.6, cy: 297.2, rot: 0 },
  { t: "Word 1", cx: 738.4, cy: 204.6, rot: -30 },
  { t: "Word 2", cx: 672.3, cy: 138.6, rot: -60 },
  { t: "Word 3", cx: 581.1, cy: 113.3, rot: -90 },
  { t: "Word 4", cx: 490.4, cy: 139.9, rot: 60 },
];
for (const c of chips) {
  s.addText(c.t, {
    shape: pres.ShapeType.rect,
    x: (c.cx - 35.5) / 72, y: (c.cy - 12) / 72, w: 71 / 72, h: 24 / 72,
    rotate: c.rot, fill: { color: CHIP_FILL }, line: { color: CHIP_GREEN, width: 0.75 },
    align: "center", valign: "middle", fontFace: CHIP_FONT, fontSize: 12,
    bold: true, italic: true, color: CHIP_GREEN, margin: 0,
  });
}

// ---- 5. arcs: 14-segment polylines at R=224 around center (581.0,297.2)
const AC = { cx: 581.0, cy: 297.2, R: 224 };
function pt(deg) {
  const a = (deg * Math.PI) / 180;
  return [AC.cx + AC.R * Math.cos(a), AC.cy - AC.R * Math.sin(a)];
}
function seg(p1, p2) {
  const x = Math.min(p1[0], p2[0]), y = Math.min(p1[1], p2[1]);
  const w = Math.abs(p2[0] - p1[0]), h = Math.abs(p2[1] - p1[1]);
  s.addShape(pres.ShapeType.line, {
    x: x / 72, y: y / 72, w: w / 72, h: h / 72,
    flipH: p2[0] < p1[0], flipV: p2[1] < p1[1],
    line: { color: ARC_STROKE, width: 0.75 },
  });
}
const arcs = [[12, 28.5], [42, 58.5], [72, 88.5], [102, 118.5]];
for (const [a0, a1] of arcs) {
  const N = 14;
  for (let i = 0; i < N; i++) {
    seg(pt(a0 + ((a1 - a0) * i) / N), pt(a0 + ((a1 - a0) * (i + 1)) / N));
  }
}

// ---- 6. arrowheads: UNROTATED down-pointing triangles (PIL row-profiles of the
// original: all four widen at the top and taper downward — they point screen-DOWN
// regardless of spoke angle), centered at the measured head positions
const heads = [
  { h: [776.4, 188.4] }, // W0 -> W1 (frame 765,180)
  { h: [692.6, 100.5] }, // W1 -> W2 (frame 684.5,96)
  { h: [585.6, 71.2] },  // W2 -> W3 (frame 581.5,68)
  { h: [473.3, 101.5] }, // W3 -> W4 (frame 473.5,97)
];
for (const hd of heads) {
  s.addShape(pres.ShapeType.triangle, {
    x: (hd.h[0] - 5) / 72, y: (hd.h[1] - 5.5) / 72, w: 10 / 72, h: 11 / 72,
    flipV: true, fill: { color: ARC_ORANGE }, line: { color: ARC_ORANGE, width: 0.5 },
  });
}

// ---- 7. "+ω" labels (Arial Bold 15pt CC0000)
const labels = [
  { cx: 840.2, cy: 236.5 }, // W0->W1
  { cx: 788.8, cy: 104.1 }, // W1->W2
  { cx: 642.8, cy: 75.4 },  // W2->W3
  { cx: 520.6, cy: 75.4 },  // W3->W4
];
for (const L of labels) {
  s.addText("+\u03C9", {
    x: (L.cx - 15) / 72, y: (L.cy - 8) / 72, w: 30 / 72, h: 16 / 72,
    align: "center", valign: "middle", fontFace: "Arial", fontSize: 15,
    bold: true, color: LABEL_RED, margin: 0,
  });
}

// ---- 8. equation box + three colored-run lines (Verdana Bold ~17pt)
s.addShape(pres.ShapeType.rect, {
  x: 65.9 / 72, y: 190.5 / 72, w: 139.5 / 72, h: 66.9 / 72,
  fill: { color: BOX_FILL }, line: { color: BOX_BORDER, width: 0.75 },
});
s.addText([
  { text: "Sin(", options: { color: EQ_BLUE } },
  { text: "\u03C9", options: { color: EQ_RED } },
  { text: " t", options: { color: EQ_GREEN } },
  { text: ")", options: { color: EQ_BLUE, breakLine: true } },
  { text: "Cos(", options: { color: EQ_BLUE } },
  { text: "\u03C9", options: { color: EQ_RED } },
  { text: " t", options: { color: EQ_GREEN } },
  { text: ")", options: { color: EQ_BLUE, breakLine: true } },
  { text: "t=0,1,2,3,....", options: { color: EQ_GREEN } },
], {
  x: 70 / 72, y: 194 / 72, w: 132 / 72, h: 60 / 72,
  align: "left", valign: "top", fontFace: EQ_FONT, fontSize: 20, bold: true,
  lineSpacing: 21, margin: 0,
});

// ---- 9. title: three single-line Arial Bold 24.3pt boxes (render-fitted: at
// 25/26pt the Liberation-rendered ink ran 2.9-6.3% wide; 24.3pt matches all three
// measured widths), at measured ink positions (y = ink_top - empirical lead)
s.addText("Sequence of 5 words", {
  x: 55.0 / 72, y: 56.40 / 72, w: 320 / 72, h: 36 / 72,
  align: "left", valign: "top", fontFace: TITLE_FONT, fontSize: 24.3, bold: true,
  color: TITLE_RED, margin: 0,
});
s.addText("Positions are defined", {
  x: 53.9 / 72, y: 82.70 / 72, w: 320 / 72, h: 36 / 72,
  align: "left", valign: "top", fontFace: TITLE_FONT, fontSize: 24.3, bold: true,
  color: TITLE_RED, margin: 0,
});
s.addText("as angles", {
  x: 120.5 / 72, y: 110.76 / 72, w: 160 / 72, h: 36 / 72,
  align: "left", valign: "top", fontFace: TITLE_FONT, fontSize: 24.3, bold: true,
  color: TITLE_RED, margin: 0,
});

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_027_recreated.pptx" })
  .then(() => console.log("WROTE slide_027_recreated.pptx"));
