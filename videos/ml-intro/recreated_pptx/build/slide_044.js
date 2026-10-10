// Slide 044 recreation — GRAPHED variant (deliverable) — attempt 2 (founder deep-verify fix)
// Content spec: videos/ml-intro/analysis/slide_044_final.json (text VERBATIM)
// House frame rule (founder directive): bg E8E8E8, red frame C00000 @ x0.15 y0.15 w13.03 h7.2,
// badge FFF9C4 w/ numeral "44" at x12.48 y0.30, title box y:0.28 x:0.6 w:12.13 centered.
// Gray cursor arrow in original = video-capture artifact, intentionally NOT recreated.
//
// Attempt-2 changes (founder deep-verify 2026-10-10; evidence in qa/slide44/graphgen/):
//  - removed the D9D9D9 header band + dark-red divider rule: the original's header is
//    continuous E8E8E8 house gray right down to the content-box top border
//    (verify_crop_header_1.txt FAIL; band-bg pixel walks read E8E8E6, not D9D9D9).
//  - title fontSize 30 -> 35: font-metric solve on the original frame — red ink width
//    308px -> 34.6pt, blue ink width 226px -> 34.8pt, cap-height solve 34.9pt.
//  - graph image v3 -> v4 (same algorithm/data: sklearn NearestNeighbors on the measured
//    26-point canonical scene; graphgen/slide_043_044_nn_scene.py) with deep-verify
//    fixes: two-tone 3D-ball dots, Arial-bold '?' at the calibrated bbox, pale EEE1E1
//    web, 26 dark-red junction arrowheads, NN ring r12.5 lw1.8 (14 measured dashes),
//    044 axes lw2.5 — closed-loop verified (graphcheck_v4_044.txt).
//  - image geometry from the v4 region (70,116)-(885,522): the original's content-box
//    border (forensics_v4b_044_out.json orig_content_box_044: left 70-71, right 884-886,
//    top 116-117; bottom house-clipped 522 — the original's 532-533 would cross the
//    recreation's house frame line at 529.2, house rule wins).
//  - content-box border re-added as a native dark-red rect OVER the image edge
//    (8B0000 1.5pt) — attempt 1 had lost it when the band was drawn under the image.
//  - captions: measured centers (left cx 275.0 / right cx 679.5), font-metric sizes
//    19/18pt (orig ink heights 14/17px incl. descender), valign bottom + pinned
//    lineSpacing 22 (PowerPoint-pitch law, worker instructions item 8) -> baselines
//    ~508.6/507.7px vs original 508/507.2. Measured string widths 2.76/4.45in vs box
//    widths 5.34/5.30in — no PowerPoint wrap risk.
const pptxgen = require("pptxgenjs");
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";

const BG = "E8E8E8";        // house background
const FRAME = "C00000";     // house frame line
const DARKRED = "8B0000";   // content-box border, captions, title part 1
const BLUE = "0000CC";      // title part 2
const INK = "333333";       // badge numeral
const BADGE = "FFF9C4";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer chrome (founder rule; untouched) ----
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG, transparency: 100 }, line: { color: FRAME, width: 1.5 },
});
// Slide-number badge: yellow oval, numeral "44" (printed number on the original)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("44", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});
// Title: two-tone ("Nearest Neighbors" dark red + "(NN) Example" blue), centered.
// fontSize 35 = measured original; single line, pinned lineSpacing 42 so LO and
// PowerPoint place the line box identically (pitch law, item 8).
s.addText(
  [
    { text: "Nearest Neighbors ", options: { color: DARKRED } },
    { text: "(NN) Example", options: { color: BLUE } },
  ],
  {
    x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "middle",
    fontSize: 35, bold: true, fontFace: FONT, margin: 0, lineSpacing: 42,
  }
);

// ---- GRAPHED VERSION: matplotlib-generated twin-panel graph embedded as image ----
// Region (70,116)-(885,522) slide px (1px = 1pt = 1/72in); the image's own edge = the
// original's measured content-box border on left/right/top.
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s44_graph_v4.png",
  x: 0.9722, y: 1.6111, w: 11.3194, h: 5.6389,
});

// Content-box border (original: thin dark-red box around the whole plot area),
// drawn OVER the image edge; fill transparent so only the stroke shows.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.9792, y: 1.6181, w: 11.3125, h: 5.6319,
  fill: { color: BG, transparency: 100 }, line: { color: DARKRED, width: 1.5 },
});

// ---- Captions (verbatim; measured centers/sizes; pinned pitch) ----
// y 6.656: measured render baselines at y=6.68 were 509.3/509.3 slide px vs original
// 508/507.2 -> nudge up 0.024in lands both at ~507.6 (selfcheck_v4_044.txt).
s.addText("Data of Three Classes", {
  x: 1.1494, y: 6.656, w: 5.34, h: 0.45, align: "center", valign: "bottom",
  fontSize: 19, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
  lineSpacing: 22,
});
s.addText("Nearest Neighbor is the Orange class", {
  x: 6.7875, y: 6.656, w: 5.30, h: 0.45, align: "center", valign: "bottom",
  fontSize: 18, bold: true, color: DARKRED, fontFace: FONT, margin: 0,
  lineSpacing: 22,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_044_recreated.pptx" })
  .then(() => console.log("done"));
