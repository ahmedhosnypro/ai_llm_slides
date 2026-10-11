// slide_050.js — SECTION DIVIDER "Transformer Decoder"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 50; old extraction 121)
//
// CONTENT SPEC: analysis/slide_050_final.json (validated PASS_WITH_FIXES; a plain
// section-divider: title + badge ONLY, everything else empty). Original frame:
// unique_slides/slide_050.jpg (960x540, 1px = 1pt frame space). Web provenance:
// slide_050_source/SOURCES.md — BANKED course-authored divider (no external source;
// precedents 002 slide 003 / 001 dividers recorded house-made).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the SHARED
// module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border (bottom
// stroke half-visible at the slide edge), badge circle d36px at (893,71)px, FDFD96
// fill + 6A5ACD ~2pt ring, bold 333333 numeral. Badge numeral = 50 (the number printed
// on THIS original frame; verified in-frame numeral "50" inside the yellow circle,
// yellow-fill bbox center (875.5, 71.0)). The spec's badge colors (#FFFF66/#6666CC)
// and frame fill (#EBEBEB) estimates are SUPERSEDED by the house chrome per the
// playlist chrome law (measured frame interior (231,233,230) = E9E9E7 + JPEG noise;
// canvas (254,255,253) = FFFFFF — matches the house template exactly).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide050/measure_landmarks*.py):
// video 002's capture is zoomed OUT with a black letterbox strip below the slide
// bottom. Fitted from THIS frame's four chrome border landmarks (stroke centers:
// left 58.50, right 901.48, top 43.00, bottom-border 516.50 <-> slide chrome 42, 919,
// 45, 540):
//   slide_x = (frame_x - 18.128) / 0.961235 ;  slide_y = (frame_y + 0.045) / 0.956566
// (scale_x 0.961235 matches certified slide_002/003/056's 0.96123 exactly; scale_y
// within 0.1% of 003's 0.957576). Badge cross-check: frame yellow-bbox center
// (875.5, 71.0) maps to slide (891.8, 74.8) vs house badge (893, 71) — the same
// 1-4px JPEG-bbox offset class as certified 002 (891.4, 73.8) and 003 (891.8, 74.8),
// confirming this frame uses the SAME playlist template. All content ink below is
// mapped to TRUE slide coordinates through this transform before building.
//
// TITLE INK (slide pts, from PIL probes scratch/slide050/probe_title_output.txt):
// single line "Transformer Decoder", Arial Bold, color C00000 (frame core census
// (184,16,32)/(176,16,32)/(188,13,30) = C00000 + JPEG noise, slide_002 precedent):
//   ink x 238..710 frame -> slide 228.75..719.76 (w 491.0pt), ink cx 474.26.
//   cap top (T) frame 270 -> slide 282.37; baseline frame 302 -> slide 315.90
//   ('>=20 ink px' row rule, like-for-like with the render; 'd'-ascender frame 268).
//   Ink cx 474.26pt sits 5.6pt LEFT of the house title-box
//   center (479.88) — measured, reproduced as measured (slide_002 per-line precedent;
//   consistent with a trailing-space advance in the original box — ink is ground truth).
//   Font size start: width fit em = 491.0 / 10.169 (Arial Bold advance sum for
//   "Transformer Decoder") = 48.3pt; cap fit = 33.98 / 0.716 = 47.5pt -> 48pt.
// Box y uses the LO ascent-lead estimate (0.273em, slide_002/003-calibrated band
// 0.267..0.283em).
//
// CLOSED-LOOP CORRECTED (attempt 1 -> 2, scratch/slide050/closed_loop_attempt1.txt):
// attempt-1 render (48pt) ink w 1009px vs target 1022.9px (-14.0px, LO/Liberation
// advance fit) -> fs re-fit 48 * 1022.9/1009 = 48.7pt; cap -0.3px, baseline +1.9px,
// cx +0.5px all within tolerance on attempt 1 (lead 0.273em and box center 474.26pt
// confirmed); y recomputed as capTop - 0.273 * fs for the new size.
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c); spec recreation_brief
// steps 6-7 mark both conditional; SOURCES.md confirms both):
//   * pen/stylus annotation cursor frozen at frame (511..525, 407..422)px gray strokes
//     near bottom-center — the presenter's annotation pointer, not slide content.
//   * black bottom letterbox strip, frame rows 519..539 full-width — maps to slide
//     y >= 542.7 (BELOW the 540pt slide bottom under the fitted mapping) = video
//     player/letterbox strip, not part of the PPT design.
//
// Layout notes: single-line title -> the multi-line line-spacing law is not
// triggered; no equations (color law N/A beyond the title census); no tables,
// delimiters, or charts. Everything below the title stays EMPTY (spec step 8).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const PT = 1 / 72; // slide pt -> inches
const FONT = "Arial";
const RED = "C00000";

// ---- measured constants (slide pt) ------------------------------------------
const TITLE = {
  text: "Transformer Decoder",
  cx: 474.26,       // measured ink center (slide pt)
  capTop: 282.37,   // measured T cap top (slide pt)
  inkW: 491.0,      // measured ink width (slide pt)
  lead: 0.273,      // ascent lead (em) — closed-loop confirmed on attempt 1
  fs: 48.7,         // Arial Bold pt — closed-loop re-fit from rendered ink width
  boxW: 560,        // box width pt: >= ink*1.1 so the single line never wraps
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "50"
drawHouseChrome(pres, s, { numeral: 50 });

// ---- 2. title: one single-line centered text box at the MEASURED ink center
// (slide pts -> inches = pt/72). valign top + margin 0. Closed-loop corrected.
s.addText(TITLE.text, {
  x: (TITLE.cx - TITLE.boxW / 2) * PT,
  y: (TITLE.capTop - TITLE.lead * TITLE.fs) * PT,
  w: TITLE.boxW * PT,
  h: (1.5 * TITLE.fs) * PT,
  align: "center", valign: "top",
  fontSize: TITLE.fs, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// ---- 3. everything else stays EMPTY (spec step 8; artifacts omitted above).

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_050_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
