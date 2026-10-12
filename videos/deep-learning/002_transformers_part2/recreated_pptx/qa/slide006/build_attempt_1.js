// slide_006.js — AGENDA SLIDE "Transformers – Part II" (six blue topic lines)
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 6)
//
// CONTENT SPEC: analysis/slide_006_final.json (validated PASS_WITH_FIXES; verbatim
// text incl. the two double-space lines and "What is Next ?" spacing — frame truth,
// per slide_006_source/SOURCES.md do NOT "fix" them). Original frame:
// unique_slides/slide_006.jpg (960x540, 1px = 1pt at frame scale).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the SHARED
// module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border, badge
// circle d36px at (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral.
// Badge numeral = 6 (the number printed on THIS original frame; verified in-frame
// numeral "6" inside the yellow circle, yellow-fill bbox center (876.0, 70.7) frame px).
// The ml-intro house values are SUPERSEDED for this playlist.
//
// FRAME->SLIDE MAPPING (measured 2026-10-11, scratch/slide006/measure_border*.py):
// video 002's capture shows the slide zoomed OUT (~0.96 scale) with a black
// video-letterbox strip BELOW the slide bottom. Fitted from THIS frame's four chrome
// border landmarks (stroke centers: left 58.5, right 901.5, top 42.5, bottom-border
// 516.5 <-> slide chrome 42, 919, 45, 540) — residuals 0.00:
//   frame_x = 18.128 + 0.961232 * slide_x ;  frame_y = -0.591 + 0.957576 * slide_y
// (identical to certified slide_003's fit 18.128/0.961232, -0.591/0.957576; slide_002's
// 18.63/0.96123, 0.95556 within JPEG-stroke noise). Badge cross-check: frame
// yellow-fill bbox center (876.0, 70.7) -> slide (892.5, 74.5) vs house badge (893, 71)
// — the same ~1-4px JPEG-bbox offset class as certified slide_002 (891.4, 73.8) and
// slide_003 (891.8, 74.8), confirming this frame uses the SAME playlist template.
//
// TITLE INK (slide pts, scratch/slide006/measure_ink.py):
//   "Transformers – Part II" ink x 223.5..631.3 (w 407.8, cx 427.4) y 71.6..100.9.
//   NOT slide-centered (cx 427.4 vs 480) — matches the spec region 24%..66% horizontal
//   (center ~45%); reproduced AT the measured center. Arial Bold advance fit
//   ("Transformers – Part II" ~10.30em ink) -> em = 39.6pt; cap fit (28.2pt/0.716) ->
//   39.4pt -> 39.5pt bold. Color: core census mode (168-176, 8-16, 24-32) = C00000
//   family (same reconciliation as certified slide_002 title (187,16,32) -> C00000).
//
// AGENDA INK (slide pts, six single-line left-aligned blocks):
//   L1 "Parallelization  Implementation Issues"  left 113.3  cap-top 154.1  w 357.9
//   L2 "Positional Information"                  left 113.3  cap-top 195.9  w 208.1
//   L3 "Building Transformer Block"              left 110.1  cap-top 239.8  w 260.1
//   L4 "Transformer Decoder"                     left 114.3  cap-top 281.5  w 198.7
//   L5 "Transformer Encoder  as a Classifier"    left 113.3  cap-top 323.3  w 344.3
//   L6 "What is Next ?"                          left 114.3  cap-top 369.3  w 136.3
//   Pitch top-to-top (slide pt): 41.8 / 43.9 / 41.8 / 41.8 / 45.9 — slightly irregular,
//   reproduced per-line at the MEASURED positions (six single-line boxes, slide_002/003
//   per-line precedent). Size: Arial Bold advance fits L1 17.96em / L6 6.84em ink ->
//   em = 19.9 / 19.9pt; cap fit 14.3/0.716 = 20.0 -> 20pt bold, no bullet glyphs.
//   COLOR: measured blue census (scratch/slide006/blue_census.py): near-pure ink cores
//   R 0-8, G 0-8, B 96-128 (densest B~96-112, darkest-1/8 mean (12.8, 6.0, 104.3)) —
//   pure deep blue with R=G=0. The spec's #1414B8 is a validator estimate; per this
//   deck's certified precedent (slide_032: cores B~100-110 -> "000080"; slide_035:
//   cores (4,0,149)..(5,0,165) -> "0000A8"; measured cores override spec guesses)
//   body blue = 000080 (PowerPoint standard Dark Blue; core deficit ~20-25 B on thin
//   strokes from 4:2:0 chroma subsampling, slide_032-calibrated).
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c), spec imagery note +
// recreation_brief step 8 optional):
//   * white mouse-cursor arrow frozen at frame ~(336, 324)px just below-left of "as a"
//     on line 5 — screen-recording artifact, not slide content.
//   * black bottom strip, frame rows 518..539 (cols 38..921) — video player letterbox;
//     strip top maps to slide y 541.7 (BELOW the 540pt slide bottom), not PPT design.
//
// Closed-loop note: box y use the LO ascent-lead estimate (0.27em, slide_002/003
// calibrated) and box x use +1.0pt LSB guesses; both are CORRECTED by the mandatory
// PIL closed-loop check (render ink vs mapped targets, tolerance ~4px @150dpi = 1.92pt)
// before judging.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const RED = "C00000";   // title (core census mode = C00000 family, spec title_text)
const BLUE = "000080";  // agenda lines (measured cores R~0 G~0 B~96-112; slide_032 calibration)
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "6"
drawHouseChrome(pres, s, { numeral: 6 });

// ---- 2. title "Transformers – Part II" — 40pt bold, centered box at the MEASURED
// ink center cx 429.1pt (NOT the slide center — measured, matches spec's 24%..66% box;
// +1.7pt glyph-bias correction from the attempt-1 closed loop, rendered ink cx lands
// on target 427.4), cap top slide 71.6pt. valign top + margin 0.
// CLOSED-LOOP CORRECTED (attempt 1 -> 2, scratch/slide006/closed_loop_attempt1*.txt):
// em re-fit 39.5 -> 40.0 (rendered ink 838.2px vs 849.8 target at 150dpi); box center
// 427.4 -> 429.1 (measured glyph-asymmetry bias -1.68pt); the six agenda lines PASSED
// attempt 1 within tolerance (worst real deltas <= 1.6px after matched loose-mask
// measurement; L4/L5 +5..7px right-edge residuals are JPEG-fade/AA noise floor).
s.addText("Transformers \u2013 Part II", {
  x: 429.1 / 72 - 4.0, y: (71.6 - 0.27 * 40.0) / 72, w: 8.0, h: (1.5 * 40.0) / 72,
  align: "center", valign: "top",
  fontSize: 40.0, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- 3. agenda list: six single-line LEFT-ALIGNED boxes at the measured ink-left
// (box x = ink_left - 1.0pt LSB guess) and cap tops (box y = cap_top - 0.27*20em lead).
// 20pt bold, 000080, verbatim incl. double spaces and "What is Next ?" spacing.
const LINES = [
  ["Parallelization  Implementation Issues", 113.3, 154.1],
  ["Positional Information",                 113.3, 195.9],
  ["Building Transformer Block",             110.1, 239.8],
  ["Transformer Decoder",                    114.3, 281.5],
  ["Transformer Encoder  as a Classifier",   113.3, 323.3],
  ["What is Next ?",                         114.3, 369.3],
];
for (const [txt, inkLeft, capTop] of LINES) {
  s.addText(txt, {
    x: (inkLeft - 1.0) / 72, y: (capTop - 0.27 * 20) / 72, w: 7.0, h: (1.5 * 20) / 72,
    align: "left", valign: "top",
    fontSize: 20, bold: true, color: BLUE, fontFace: FONT, margin: 0,
  });
}

// ---- 4. everything else stays EMPTY (spec step 7): no bullets, charts, images;
// the mouse cursor and letterbox are omitted artifacts.

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_006_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
