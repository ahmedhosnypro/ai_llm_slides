// slide_024.js — "Objective of Self attention" (Deep Learning DSAI 308, lecture 001)
// Built from PIL-measured geometry of unique_slides/slide_024.jpg (960x540, 1px = 1pt = 1/72in).
// Chrome: PLAYLIST house chrome (videos/deep-learning/shared_patterns/house_chrome.js,
// founder directive 2026-10-11) — supersedes the ml-intro values in 17_worker_instructions.md.
//
// Content decisions (frame is ground truth; see qa/slide024/worker_report.md):
// - 6 word nodes, 9 measured attention edges + in<->the per validated spec (faint shaft,
//   heads present at both measured endpoints) = 10 edges.
// - in<->Boy [?] and climbs<->tree [?] OMITTED: pixel forensics of the corridors shows no
//   stroke (the spec itself conditions them on "match the captured frame exactly").
// - Sentence box fill measured = same pale cyan as the big circle (EEFEFB), dashed blue border.
// - Block arrow: hatched fill is beyond native pptxgenjs -> generated PNG at exact size.
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const px = (v) => v / 72; // 72dpi frame px -> inches

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- playlist house chrome (white canvas, gray panel, red border, badge "24") ----
drawHouseChrome(pres, slide, { numeral: 24 });

const FONT = "Arial";
const RED = "EE0000";

// ---- title (measured ink x[414,766] y[60,86] -> 29pt bold (352px ink / 12.34em bold advance),
//      center (590,73)px; box wide enough that 29pt-bold never wraps) ----
slide.addText("Objective of Self attention", {
  x: px(372), y: px(46), w: px(436), h: px(54),
  align: "center", valign: "middle",
  fontSize: 29, bold: true, color: "000000", fontFace: FONT, margin: 0,
});

// ---- big attention circle (border ring x[44,512] y[57,525], dashed 2233CC 2pt) ----
slide.addShape(pres.shapes.OVAL, {
  x: px(44), y: px(57), w: px(469), h: px(469),
  fill: { color: "EEFEFB" },
  line: { color: "2233CC", width: 2, dashType: "dash" },
});

// ---- attention edges (drawn under the nodes; endpoints at measured circle boundaries) ----
// helper: straight connector between two points, double-headed
function edge(x1, y1, x2, y2, width) {
  slide.addShape(pres.shapes.LINE, {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    flipH: x2 < x1, flipV: y2 < y1,
    line: { color: RED, width: width, beginArrowType: "triangle", endArrowType: "triangle" },
  });
}
// thin ~2pt edges
edge(230, 108, 329, 131, 2);    // in<->garden
edge(203, 192, 156, 255, 1.75); // in<->the (spec-certain; faint shaft in frame, heads measured)
edge(306, 164, 155, 256, 2);    // the<->garden [?] — confirmed by forensics
edge(167, 292, 216, 291, 2);    // the<->Boy
edge(158, 330, 389, 396, 2);    // the<->tree (long diagonal across the circle)
// thick ~4pt edges
edge(306, 258, 326, 190, 4);    // Boy<->garden
edge(318, 290, 386, 364, 4);    // Boy<->tree
edge(264, 336, 258, 403, 4);    // Boy<->climbs (near-vertical)
edge(391, 197, 431, 318, 4);    // garden<->tree (along right edge)

// ---- word nodes ----
function node(cx, cy, d, label, fill, lineColor, lineW) {
  slide.addShape(pres.shapes.OVAL, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: lineColor, width: lineW },
  });
  slide.addText(label, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    align: "center", valign: "middle",
    fontSize: 20, bold: true, color: "000000", fontFace: FONT, margin: 0,
  });
}
const YEL = "FEFFE5", YEL_LINE = "8C8C8C";
const GRN = "D5FFAF", GRN_LINE = "4C9A2A";
node(202.5, 143.5, 92, "in", YEL, YEL_LINE, 1);        // in
node(359.5, 163, 92, "garden", YEL, YEL_LINE, 1);      // garden
node(119, 294.5, 93, "the", YEL, YEL_LINE, 1);         // the
node(268, 288, 97, "Boy", GRN, GRN_LINE, 1.5);         // Boy (in circle, the only green node)
node(432, 366, 95, "tree", YEL, YEL_LINE, 1);          // tree
node(253, 449.5, 92, "climbs", YEL, YEL_LINE, 1);      // climbs

// ---- embedding-vector icons (rounded rect + 4 bars) ----
function vectorIcon(x, y, w, h, outline, barColor, barInsetX, barW, barH, barPitch, firstTop) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: "FFFFFF" }, line: { color: outline, width: 1.25 }, rectRadius: 0.06,
  });
  for (let i = 0; i < 4; i++) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: px(x + barInsetX), y: px(y + firstTop + i * barPitch), w: px(barW), h: px(barH),
      fill: { color: barColor }, line: { type: "none" },
    });
  }
}
// blue icons: outer ~25x51px, bars 15x6px, pitch 12px, first bar +4px
const B_OUT = "4472C4", B_BAR = "8FBCE6";
vectorIcon(125, 147, 25, 50, B_OUT, B_BAR, 5, 15, 6, 12.3, 4);   // beside 'in'
vectorIcon(85, 347, 25, 51, B_OUT, B_BAR, 5, 15, 6, 12.3, 4);    // beside 'the'
vectorIcon(309, 315, 25, 53, B_OUT, B_BAR, 5, 15, 6, 12.3, 5);   // beside 'Boy' (in circle)
vectorIcon(309, 451, 25, 51, B_OUT, B_BAR, 5, 15, 6, 12.3, 4);   // beside 'climbs'
vectorIcon(381, 411, 26, 51, B_OUT, B_BAR, 5.5, 15, 6, 12.3, 4); // beside 'tree'
// orange contextual icon (output Boy): taller, bars 16x7.5 pitch 21.3
vectorIcon(794, 331, 25, 86, "FF4000", "FF6600", 4, 16, 7.5, 21.3, 8);
// blue input icon (input Boy)
vectorIcon(630, 471, 25, 53, B_OUT, B_BAR, 5, 15, 6, 12.3, 5);

// ---- example-sentence callout (outer x[475,902] y[106,144], dashed blue, pale-cyan fill) ----
slide.addShape(pres.shapes.RECTANGLE, {
  x: px(475), y: px(106), w: px(427), h: px(38),
  fill: { color: "EEFEFB" },
  line: { color: "2233CC", width: 1.5, dashType: "dash" },
});
slide.addText([
  { text: "The ", options: {} },
  { text: "boy", options: { bold: true } },
  { text: " climbs the tree in the garden", options: {} },
], {
  x: px(475), y: px(106), w: px(427), h: px(38),
  align: "center", valign: "middle",
  fontSize: 20, color: "000000", fontFace: FONT, margin: 0,
});

// ---- hatched block arrow (generated PNG at exact size; pptxgenjs has no pattern fill) ----
slide.addImage({
  path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/blockarrow_024.png",
  x: px(518), y: px(281), w: 1367 / 600, h: 300 / 600,
});

// ---- mapping link: input Boy's blue vector -> orange vector (thin red DASHED) ----
slide.addShape(pres.shapes.LINE, {
  x: px(657), y: px(383), w: px(789 - 657), h: px(502 - 383),
  flipV: true,
  line: { color: RED, width: 1.5, dashType: "dash", endArrowType: "triangle" },
});

// ---- output Boy + input Boy (green, right side) ----
node(743, 290.5, 100, "Boy", GRN, GRN_LINE, 1.5);   // output Boy (top right)
node(607.5, 445, 97, "Boy", GRN, GRN_LINE, 1.5);    // input Boy (bottom)

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_024_recreated.pptx" })
  .then(() => console.log("wrote slide_024_recreated.pptx"));
