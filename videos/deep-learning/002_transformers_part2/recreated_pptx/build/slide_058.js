// slide_058.js — SECTION DIVIDER "Transformer Encoder / as a Classifier"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 58)
//
// CONTENT SPEC: analysis/slide_058_final.json (divider; PASS_WITH_FIXES; two-line
// title verbatim, no bullets/diagrams/equations). Original frame:
// unique_slides/slide_058.jpg (960x540, 1px = 1pt). Provenance banked:
// slide_058_source/SOURCES.md (course-authored divider; BERT topic anchor only).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the
// SHARED module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF
// canvas, gray E9E9E7 panel x 42..919px / y 45px..slide bottom, thin C00000 border,
// badge circle d36px at (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333
// numeral. Badge numeral = 58 (the number printed on THIS original frame).
// The spec's #8B1A1A border / #F5F27D+6C5CE7 badge estimates are superseded by the
// house chrome (validation.uncertain_items flags all hexes as model estimates).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide058/measure_fit.py):
// capture identical to the certified slide-002 frame (top stroke row 42/750px,
// badge yellow bbox center 875.5,70.5 — byte-similar chrome across frames), so the
// certified slide-002 fit is adopted verbatim:
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Cross-check: frame badge (875.5,70.5) -> slide (891.4, 73.8) vs house (893, 71):
// d = (-1.6, +2.8) px — within the ~3px badge tolerance (slide-002 precedent).
// My own independent 4-landmark least-squares fit (left 58.5, right 902, top 42,
// bottom 516) differs from this mapping by <=1 slide pt — inside the 4px@150dpi
// closed-loop tolerance; the certified mapping is kept for deck consistency.
//
// TITLE INK (frame mask, red threshold; slide pts via the mapping):
//   L1 "Transformer Encoder"  ink x 224..697 (w 474fr = 493.1pt) y 229..264
//      -> cx 459.69pt, ink-top 239.65pt. Arial Bold em fit (PIL, real Arialbd.TTF):
//      width 48.1-48.7 (word-level mean ~48.2), height ~50.9 (halo-inflated).
//   L2 "as a Classifier"      ink x 318..631 (w 314fr = 326.7pt) y 282..317
//      -> cx 474.26pt, ink-top 295.11pt. em fit 48.1-48.4.
//   The two lines' ink centers are NOT coincident (459.7 vs 474.3, dx 14.6pt) and
//   neither sits at slide center 480 — MEASURED, reproduced as measured (slide-002
//   L3 precedent). Two single-line center-aligned boxes pin each line's measured
//   center; sizes refined by the mandatory closed-loop PIL check (mask-to-mask,
//   same thresholds both images, tolerance ~4px @150dpi = 1.92pt).
//
// TITLE COLOR: frame core census (median of most-saturated quartile) = (158,13,28);
// the CERTIFIED C00000 slide-002 title reads (163,13,29) under the identical census
// (luma Y=60 vs C00000's 57; JPEG chroma desaturation on thin strokes — luma is
// preserved under 4:2:0, ruling out B22222 [Y=77] and 8B1A1A). Title = C00000,
// the deck red; the spec's #B22222 is a superseded model estimate [?].
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c); spec imagery +
// animation_state both flag them; SOURCES.md confirms):
//   * presenter's black cursor/pointer at frame ~(650..660, 270..281), right of
//     "Classifier" between the lines — live-cursor artifact, not slide content.
//   * black bottom strip, frame rows 518..539 full-width -> slide y >= 542.3
//     (BELOW the 540pt slide bottom under the mapping): video letterbox, not design.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const RED = "C00000"; // title (frame census matches certified C00000 signature)
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "58"
drawHouseChrome(pres, s, { numeral: 58 });

// ---- 2. title: two single-line center-aligned boxes at the MEASURED ink positions
// (slide pts -> inches = pt/72). valign top + margin 0. Box y = ink_top - 0.25*em
// (Arial ascent-minus-cap lead estimate, slide-002 pattern); box cx = measured ink
// cx (glyph-asymmetry bias corrected by the closed-loop check). Start em 48.5.
const EM = 48.5;
const LEAD = 0.25 * EM; // 12.125pt

// L1 "Transformer Encoder" — target ink cx 459.69pt, ink-top 239.65pt
s.addText("Transformer Encoder", {
  x: 459.69 / 72 - 6.0, y: (239.65 - LEAD) / 72, w: 12.0, h: (1.5 * EM) / 72,
  align: "center", valign: "top",
  fontSize: EM, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// L2 "as a Classifier" — target ink cx 474.26pt, ink-top 295.11pt
s.addText("as a Classifier", {
  x: 474.26 / 72 - 6.0, y: (295.11 - LEAD) / 72, w: 12.0, h: (1.5 * EM) / 72,
  align: "center", valign: "top",
  fontSize: EM, bold: true, color: RED, fontFace: FONT, margin: 0,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_058_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
