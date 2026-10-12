// Slide 043 recreation — "Nearest Neighbors (NN) Example"
// Spec: videos/ml-intro/analysis/slide_043_final.json (validated, PASS_WITH_FIXES, score 7).
// House chrome per founder directive 2026-10-09 overrides spec frame/badge/title geometry
// (bg E8E8E8, outer red frame, badge oval FFF9C4 with numeral "43", title box y:0.28).
// NOTE: this file previously held the pre-curation id-43 "Classification" build (now new
// slide 034); those bytes are banked at qa/slide043/build_attempt_1.js and build/slide_034.js.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE";
const W = 13.33, H = 7.5;

// Palette (from spec; hex WITHOUT '#')
const BG = "E8E8E8", FRAME_RED = "C00000", BADGE_YELLOW = "FFF9C4", INK = "333333";
// Band color: measured from unique_slides/slide_043.jpg (230,232,230) — the
// 2026-10-10 founder deep-verify found the spec's D3D3D3 too dark vs the frame.
const BAND = "E6E8E6", TITLE_RED = "B00020", TITLE_BLUE = "0000CC";
const MAROON = "8B1A1A", WHITE = "FFFFFF", GREEN = "7ED957", CYAN = "2FE0E0";
const BEIGE = "E8C9A0", RED = "E02020", YELLOW = "FFFF00";
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- HOUSE CHROME (overrides spec) ----
// Light-gray header band, full inner width, ~0-15% of slide height
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 1.0, fill: { color: BAND }, line: { color: BAND, width: 0 },
});

// Outer red frame, 0.15in inset from every edge (drawn over the band edges)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG, transparency: 100 }, line: { color: FRAME_RED, width: 1.5 },
});

// Slide-number badge: yellow oval top-right, numeral exactly "43"
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("43", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// Title: centered, two-color runs (dark red + blue), house geometry
s.addText([
  { text: "Nearest Neighbors", options: { color: TITLE_RED } },
  { text: " (NN) Example", options: { color: TITLE_BLUE } },
], {
  x: 0.6, y: 0.28, w: 12.13, h: 0.75, align: "center", valign: "middle",
  fontSize: 30, bold: true, fontFace: FONT, margin: 0,
});

// ---- CONTENT (per spec) ----
// White content area below the header band, thin maroon border
// (inset 0.15in inside the house frame so both borders stay visible)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.3, y: 1.15, w: 12.73, h: 6.05, fill: { color: WHITE }, line: { color: MAROON, width: 1.5 },
});

// ---- GRAPHED VERSION: matplotlib-generated graph embedded as image ----
// Native dot/axes approximation (banked in build/slide_043.js, certified) replaced by
// a graph generated per the advanced-graph rule: scripts running the same NN-example
// scene on measured triage data (graphgen/slide_043_044_nn_scene.py),
// closed-loop PIL-verified against the original frame.
//
// 2026-10-10 FOUNDER DEEP-VERIFY REWORK (graph_v3):
//   - dots are now shaded 3D balls (bright core + darker rim) at the measured
//     ink diameters — the flat single-color v2 dots read dull and mis-sized
//     (judge attempt 1 MINOR, PIL radial profiles);
//   - z-order corrected: big red ON TOP of the greens, v-axis ON TOP of the
//     big red's left rim (both seams measured on the original);
//   - axes lw 3.5 (measured ~3.5-4 px; v2 used 2.5), '?' Arial bold 20pt at the
//     measured ink bbox (v2 rendered 7x12.5 vs original 11x15).
//   Evidence: qa/slide43/graphgen/graphcheck_v3_043_out.json (all checks PASS).
//
// 2026-10-10 FOUNDER DEEP-VERIFY REWORK round 2 (graph_v4 — c5 x3-closeup
// judge read the query dot "larger and flatter", the '?' "too tall/large and
// brighter than the original's darker/brick-red"; probe_qmark_v1 re-measures):
//   - query dot is now a GLOSSY top-lit ball (3 stacked discs, marker edge
//     stroke zeroed): solid r 7.5 (v3 effective was ~8.7 vs the original's 7.5),
//     center (232,0,0), top rims (196,0,4), bottom rims (163,0,11);
//   - '?' shrunk 20pt -> 16pt and re-anchored: crisp ink 329.6..337.5 x
//     347.9..359.4 sits inside the original's blurred 329..338 x 347..360;
//   - '?' color #8B1A1A (blur-corrected paint ~= the deck's accent maroon;
//     spec's #E02020 read brighter than the original's brick-red glyph).
//   Evidence: qa/slide43/graphgen/graphcheck_v4_043_out.json (all checks PASS).
// Image region: slide px x92..452, y160..484 (1px = 1pt = 1/72in).
s.addImage({
  path: "videos/ml-intro/recreated_pptx/build/assets/graphs/s43_graph_v4.png",
  x: 1.2778, y: 2.2222, w: 5.0, h: 4.5,
});

// Caption, bottom-left inside the content area, dark red on the original's
// absolute geometry (glyph band x98..517, y494..511; highlight x346..449,
// y489..512 — measured on unique_slides/slide_043.jpg).
// 2026-10-10 fix: regular weight (bold Arial advances ~4.7% wider than the
// original's measured runs; only the highlighted "ONE TEST" is bold), and the
// box moved from x0.7/y6.6 to x1.34/y6.71 so the glyphs land on the original.
// lineSpacing pinned (24pt exact) per the 2026-10-10 PowerPoint-pitch law;
// single-line box — no wrap possible (text ~5.9in in a 7.1in box).
s.addText([
  { text: "Data of Three Classes   and ", options: { color: MAROON } },
  { text: "ONE TEST", options: { color: MAROON, bold: true, highlight: YELLOW } },
  { text: " sample", options: { color: MAROON } },
], {
  x: 1.34, y: 6.71, w: 7.1, h: 0.45, align: "left", valign: "middle",
  fontSize: 20, fontFace: FONT, margin: 0, lineSpacing: 24,
});

pptx
  .writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_043_recreated.pptx" })
  .then(() => console.log("done"));
