// slide_007.js — SECTION HEADER "Parallelization / Implementation Issues"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 7)
//
// CONTENT SPEC: analysis/slide_007_final.json (PASS_WITH_FIXES; two-line red title,
// no bullets/body; cursor + black bottom strip flagged as capture artifacts).
// Original frame: unique_slides/slide_007.jpg (960x540, 1px = 1pt).
// Provenance: slide_007_source/SOURCES.md (course-authored header; Vaswani §3.2 +
// Table 1 is background for the FOLLOWING slides only — nothing sourced enters here).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the SHARED
// module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border, badge
// circle d36px at (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral.
// Badge numeral = 7 (the number printed on THIS original frame; verified in-frame
// numeral "7" in the yellow badge at top-right). The spec's #F2F2F2 background /
// white top strip / #C00000 5%-95% frame / #FFFF99 badge readings describe the
// ~0.958-zoomed video capture of the playlist chrome and are SUPERSEDED by it
// (measured: frame canvas (254,255,253), panel (231,233,230) — identical to the
// certified slide_002 frame).
//
// FRAME->SLIDE MAPPING (measured 2026-10-11, scratch/slide007/measure_original.py):
// video 002's capture is zoomed OUT (~0.958) with a black letterbox strip BELOW the
// slide. Fitted from this frame's four chrome border landmarks (stroke centers:
// left 58.5, right 901.5, top 42.5, bottom-border 516.5 <-> slide chrome 42, 919,
// 45, 540):
//   frame_x = 18.13 + 0.96123 * slide_x ;  frame_y = -0.591 + 0.95758 * slide_y
// Cross-check: badge yellow-bbox center (875.5, 71.0) frame -> slide (891.5, 74.9)
// vs house badge (893, 71) — same ~3px JPEG-bbox jitter slide_002 accepted; same
// playlist template confirmed. All content ink below is mapped to TRUE slide coords
// through this transform before building.
//
// TITLE INK (slide pts, core-red PIL census + halo-inclusive extents):
//   L1 "Parallelization"        ink x 307.8..627.2 (w 319.4)  y 237.7..274.2  cx 467.5
//      -> Arial Bold advance 6.725em -> em = 47.5; L2 em = 517.1/10.781 = 48.0.
//      48pt bold (spec's "40-44pt" was a zoomed-frame estimate; measured wins).
//   L2 "Implementation Issues"  ink x 216.2..733.3 (w 517.1)  y 292.0..337.9  cx 474.7
//   Line ink centers are genuinely OFF slide center (467.5 / 474.7 vs 480; measured,
//   reproduced as measured — same law as slide_002 L3). Title color census mode
//   (184..193, 13..16, 29..35) = C00000 + JPEG noise (identical to slide_002's).
//
// Box y positions use the ascent-minus-cap lead estimate (0.27em) and are CORRECTED
// by the mandatory closed-loop PIL check (render ink vs mapped targets, tolerance
// ~4px @150dpi = 1.92pt) before judging.
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c); spec flags both):
//   * mouse-cursor arrow frozen at frame ~(328..362, 289..340)px (dark pixels
//     measured) just below "Parallelization" — recording artifact, not slide content.
//   * black bottom letterbox strip, frame rows ~517..539 full-width — sits at slide
//     y >= 539.5 (below/at the slide bottom edge under the fitted mapping), i.e. the
//     video player strip outside the slide, not part of the PPT design.

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const RED = "C00000"; // title (frame census = C00000 + JPEG noise; spec title_text)
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "7"
drawHouseChrome(pres, s, { numeral: 7 });

// ---- 2. title block: two single-line centered text boxes at the MEASURED ink
// positions (slide pts -> inches = pt/72). Each line its own box so each line's
// measured center is reproduced exactly (L1 12.5pt left of center, L2 5.3pt).
// valign top + margin 0. No equations, no body text, nothing else (spec step 7).
// CLOSED-LOOP CORRECTED (attempt 1 -> 2, scratch/slide007/closed_loop_attempt1.txt):
// em re-fit 48 -> 48.5 (rendered ink w 315.4pt vs target 319.4 L1, 511.2 vs 517.1 L2);
// box centers shifted by the measured glyph-asymmetry bias (+1.5/+0.5pt) so the INK
// centers land on the mapped targets (467.5/474.7); y_box trimmed by the measured
// +0.8/+0.7px render lead bias.

// L1 "Parallelization" — 48.5pt bold, target ink cx 467.5pt (box center 469.0 + bias)
s.addText("Parallelization", {
  x: 469.0 / 72 - 6.0, y: (237.7 - 0.27 * 48.5) / 72 - 0.00533, w: 12.0, h: (1.5 * 48.5) / 72,
  align: "center", valign: "top",
  fontSize: 48.5, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// L2 "Implementation Issues" — 48.5pt bold, target ink cx 474.7pt (box center 475.2 + bias)
s.addText("Implementation Issues", {
  x: 475.2 / 72 - 6.0, y: (292.0 - 0.27 * 48.5) / 72 - 0.00467, w: 12.0, h: (1.5 * 48.5) / 72,
  align: "center", valign: "top",
  fontSize: 48.5, bold: true, color: RED, fontFace: FONT, margin: 0,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_007_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
