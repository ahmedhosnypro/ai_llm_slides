// slide_002.js — TITLE SLIDE "Transformers / Part II / Aug. 2020"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 2)
//
// CONTENT SPEC: analysis/slide_002_final.json (verbatim_text bullets = the three
// stacked title lines; validated PASS_WITH_FIXES). Original frame:
// unique_slides/slide_002.jpg (960x540, 1px = 1pt).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the
// SHARED module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF
// canvas, gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border
// (bottom stroke half-visible at the slide edge), badge circle d36px at (893,71)px,
// FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral. Badge numeral = 2 (the number
// printed on THIS original frame; verified in-frame numeral "2" inside a yellow
// circle at top-right). The ml-intro house values are SUPERSEDED for this playlist.
//
// FRAME->SLIDE MAPPING (measured 2026-10-11, scratch/slide002/measure_original*.py):
// video 002's capture shows the slide zoomed OUT to ~0.958 scale with a black
// video-letterbox strip BELOW the slide bottom. Fitted from the four chrome border
// landmarks (frame panel left 59, right 902, top 43, bottom-border 516 <-> slide
// chrome 42, 919, 45, 540):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Cross-check: the frame's badge (yellow-bbox center 875.5, 70.5) maps to slide
// (891.4, 73.8) vs the house badge (893, 71) — within JPEG-bbox noise, confirming
// this frame uses the SAME playlist template. All content ink below is therefore
// mapped to TRUE slide coordinates through this transform before building.
//
// TITLE INK (slide pts, from the frame measurement):
//   L1 "Transformers"  ink x 246.9..709.9 (w 462.9)  y 197.8..252.2  cx 478.4
//      -> Arial Bold: advance sum 6.611em -> em = 462.9/6.611 = 70.0pt (width match
//      exact); T-cap 51.3pt -> em = 71.6 (consistent within JPEG halo). 70pt bold.
//   L2 "Part II"       ink x 409.2..549.7 (w 140.4)  y 278.4..316.0  cx 479.5
//      -> Arial Bold advance 2.778em -> em = 50.5pt -> 51pt bold.
//   L3 "Aug. 2020"     ink x 436.3..545.5 (w 109.2)  y 339.1..361.0  cx 490.9
//      -> Arial Bold (Italic) advance 4.779em -> em = 22.9pt -> 23pt bold ITALIC
//      (spec typography_notes: bold italic; italic slant visible in the frame).
//      NOTE: L3's ink center sits at 490.9pt, ~10.9pt RIGHT of the slide center the
//      other two lines share (478.4/479.5) — measured, reproduced as measured.
// Box y positions use the Arial ascent-minus-cap lead estimate (0.22em) and are
// CORRECTED by the mandatory closed-loop PIL check (render ink vs mapped targets,
// tolerance ~4px @150dpi = 1.92pt) before judging.
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c), founder artifact law;
// the spec itself flags both in validation.uncertain_items):
//   * pen/stylus annotation cursor frozen at frame (437..473, 345..374)px just below
//     "Aug. 2020" — the presenter's annotation pointer, not slide content.
//   * black bottom strip, frame rows 517..539 full-width — sits at slide y >= 541.0
//     (BELOW the 540pt slide bottom under the fitted mapping), i.e. the video
//     player/letterbox strip outside the slide, not part of the PPT design.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const RED = "C00000"; // title lines (frame-measured core ~(187,16,32) = C00000 + JPEG noise)
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "2"
drawHouseChrome(pres, s, { numeral: 2 });

// ---- 2. title block: three single-line centered text boxes at the MEASURED ink
// positions (slide pts -> inches = pt/72). Each line its own box so each line's
// measured center is reproduced exactly (L3 is genuinely right-of-center).
// valign top + margin 0. CLOSED-LOOP CORRECTED (attempt 1 -> 2, closed_loop_attempt1.txt):
// sizes re-fit from rendered ink width (L1 70->73pt: 442.6pt rendered vs 463 target;
// L2 51->53pt: 134.9 vs 140.5), y from the MEASURED ascent lead (0.267/0.277/0.250em),
// box centers shifted by the measured glyph-asymmetry bias (-1.5/-0.5/-0.6pt) so the
// INK centers land on the mapped targets. L1 uses the house title box (x 0.6, w 12.13).

// L1 "Transformers" — 73pt bold, target ink cx 478.4pt (house box center 479.88pt
// minus measured -1.56pt glyph bias -> ink 478.3)
s.addText("Transformers", {
  x: 0.6, y: (197.8 - 0.2671 * 73) / 72, w: 12.13, h: (1.5 * 73) / 72,
  align: "center", valign: "top",
  fontSize: 73, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// L2 "Part II" — 53pt bold, target ink cx 479.5pt (box center 480.0 - 0.5 bias)
s.addText("Part II", {
  x: 6.6667 - 6.0, y: (278.4 - 0.2769 * 53) / 72, w: 12.0, h: (1.5 * 53) / 72,
  align: "center", valign: "top",
  fontSize: 53, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// L3 "Aug. 2020" — 23pt bold italic, target ink cx 490.9pt (box center 491.5 - 0.6
// italic/glyph bias); measured right-of-center offset KEPT as measured
s.addText("Aug. 2020", {
  x: 6.8264 - 6.0, y: (339.1 - 0.2504 * 23) / 72, w: 12.0, h: (1.5 * 23) / 72,
  align: "center", valign: "top",
  fontSize: 23, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_002_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
