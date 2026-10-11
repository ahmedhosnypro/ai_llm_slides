// slide_035.js — "Building Transformer Block" (transition/agenda slide)
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 35)
//
// CONTENT SPEC: analysis/slide_035_final.json (PASS_WITH_FIXES; recreation_brief
// steps applied). Original frame: unique_slides/slide_035.jpg (960x540, 1px = 1pt).
// Provenance: slide_035_source/SOURCES.md (paper 1706.03762v7 §3.1/§3.3 confirm the
// three component names; text-only slide, no figures/equations).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the SHARED
// module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..919px / y 45px..slide bottom, thin C00000 border, badge
// circle d36px at (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral.
// Badge numeral = 35 (the number printed on THIS original frame; measured badge
// yellow-fill bbox center (875.5, 71.0) — same landmark set as certified slide_002).
// The ml-intro house values are SUPERSEDED for this playlist.
//
// FRAME->SLIDE MAPPING (measured 2026-10-11, scratch/slide035/measure_*.py):
// video 002's capture shows the slide zoomed OUT (~0.958 scale) with a black
// video-letterbox strip below the slide bottom. Fitted from the four chrome border
// landmarks in THIS frame (left border col 59, right border col ~902, top border row
// 43, bottom-border row 516 <-> slide chrome 42, 919, 45, 540) — identical to the
// certified slide_002 fit:
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Cross-check: frame badge yellow-fill bbox (859..892, 57..85) center (875.5, 71.0)
// maps to slide (891.4, 74.3) vs house badge center (893, 71) — within ~3px of the
// house position (fill bbox excludes the purple ring), confirming the shared template.
// All content ink below is mapped to TRUE slide coordinates through this transform.
//
// MEASURED INK (frame px -> slide pts):
//   TITLE "Building Transformer Block": ink x 172..781 (mapped L 159.5, R 793.1,
//      bbox cx 476.3 — the original title is genuinely ~3.7pt LEFT of slide center
//      480; reproduced as measured), cap top 156.5 -> 163.8, baseline 190.3 -> 199.1.
//      Arial Bold: advance 13.169em, ink ~13.04em -> em = 630.5/13.04 = 48.3pt;
//      cap-derived 49.4 (JPEG-halo inflated). Start 48.5, closed-loop corrected.
//   "Adding": ink x 120..233 (mapped L 105.4), asc top 292.5 -> 306.1, baseline
//      317.5 -> 332.3. Advance 3.444em, ink ~3.37em -> em = 115.5/3.37 = 34.3pt.
//   "Residual Connections": ink x 213..566 (L 202.2, R 569.6), cap top 340.5 -> 356.4,
//      baseline 365.5 -> 382.5. em = 365.4/10.374 = 35.2pt.
//   "Layer Normalization": ink x 213..533 (L 202.2, R 535.0), cap top 379.5 -> 397.1,
//      baseline 403.5 -> 422.3. em = 330.7/9.388 = 35.2pt.
//   "Feed Forward Network": ink x 213..576 (L 202.2, R 579.8), cap top 417.5 -> 436.9,
//      baseline 441.5 -> 462.0. em = 375.6/10.620 = 35.4pt.
//   Baseline pitch of the three list lines: 39.8 / 39.7 slide pt (measured). Rendered
//   as three SINGLE-LINE boxes at their own measured ink positions (certified
//   slide_002 pattern), so no multi-line auto-pitch is trusted anywhere.
//
// COLORS (PIL-census of the saturated ink, scratch/slide035/measure_*.py):
//   title red core (185,7,24) = C00000-family (matches certified 002/031 choice).
//   body blue deep cores (4,0,149)..(5,0,165) with R=G=0 — a PURE deep blue, darker
//   than the spec's #1A1AB8 (R,G=26 would show R,G cores ~15-30; measured 0-5).
//   Per the measured-color law (EQUATION COLOR LAW extension; certified 039 precedent
//   of overriding spec color guesses with measured cores) body blue = 0000A8.
//   (Spec colors.background E9E9E9/FFFFFF -> chrome law E9E9E7 panel / FFFFFF canvas.)
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c); spec flags both):
//   * mouse cursor at ~frame (365,400) over "Layer Normalization" — recording artifact.
//   * black letterbox strip, frame rows 519..539 — below the slide bottom under the
//     fitted mapping (slide y >= 543), i.e. the video player strip, not slide content.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const RED = "C00000";   // title (measured core (185,7,24), C00000-family)
const BLUE = "0000A8";  // body (measured deep cores (4,0,149)..(5,0,165), R=G=0)
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "35"
drawHouseChrome(pres, s, { numeral: 35 });

// ---- 2. title: single-line centered box at the MEASURED ink position.
// Target ink: bbox cx 476.3pt, cap top 163.8pt. Box center = ink bbox center minus
// glyph bias (LSB(B)-RSB(k))/2 = +0.0175em = +0.85pt -> box cx 475.45.
// y_box = capTop - 0.27em lead (LO-measured lead family 0.267-0.277; closed-loop
// corrected below against the 150dpi render).
s.addText("Building Transformer Block", {
  x: (475.45 - 436.68) / 72, y: (163.78 - 0.27 * 48.5) / 72, w: 12.13, h: (1.5 * 48.5) / 72,
  align: "center", valign: "top",
  fontSize: 48.5, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- 3. lead-in word "Adding": single-line left-aligned box at measured ink.
// Target ink L 105.4pt (box x = inkL - LSB(A)*F = 105.4 - 0.032*34), cap/asc top 306.1.
s.addText("Adding", {
  x: (105.4 - 0.032 * 34) / 72, y: (306.11 - 0.27 * 34) / 72, w: 2.6, h: (1.5 * 34) / 72,
  align: "left", valign: "top",
  fontSize: 34, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 4. the three list lines: one single-line box EACH at its own measured ink
// position (left edge x 202.2pt shared; cap tops 356.4 / 397.1 / 436.9). Sizes 35pt.
s.addText("Residual Connections", {
  x: (202.21 - 0.083 * 35) / 72, y: (356.35 - 0.27 * 35) / 72, w: 6.2, h: (1.5 * 35) / 72,
  align: "left", valign: "top",
  fontSize: 35, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Layer Normalization", {
  x: (202.21 - 0.083 * 35) / 72, y: (397.06 - 0.27 * 35) / 72, w: 6.2, h: (1.5 * 35) / 72,
  align: "left", valign: "top",
  fontSize: 35, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});
s.addText("Feed Forward Network", {
  x: (202.21 - 0.111 * 35) / 72, y: (436.87 - 0.27 * 35) / 72, w: 6.2, h: (1.5 * 35) / 72,
  align: "left", valign: "top",
  fontSize: 35, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_035_recreated.pptx" })
  .then(() => console.log("WROTE slide_035_recreated.pptx"));
