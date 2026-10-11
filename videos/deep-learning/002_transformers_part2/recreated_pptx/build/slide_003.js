// slide_003.js — SECTION DIVIDER "Review of Part I / Self Attention Mechanism"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 3)
//
// CONTENT SPEC: analysis/slide_003_final.json (validated PASS_WITH_FIXES). Original
// frame: unique_slides/slide_003.jpg (960x540, 1px = 1pt). Web provenance:
// slide_003_source/SOURCES.md (course-authored divider; no external source needed).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the SHARED
// module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF canvas,
// gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border, badge
// circle d36px at (893,71)px, FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral.
// Badge numeral = 3 (the number printed on THIS original frame; verified in-frame
// numeral "3" inside a yellow circle at top-right, yellow-bbox center (875.5, 71.0)).
// The ml-intro house values are SUPERSEDED for this playlist.
//
// FRAME->SLIDE MAPPING (measured 2026-10-11, scratch/slide003/measure_refined_output.txt):
// video 002's capture shows the slide zoomed OUT (~0.958 scale) with a black
// video-letterbox strip BELOW the slide bottom. Fitted from THIS frame's four chrome
// border landmarks (stroke centers: left 58.5, right 901.5, top 42.5, bottom-border
// 516.5 <-> slide chrome 42, 919, 45, 540):
//   frame_x = 18.128 + 0.961232 * slide_x ;  frame_y = -0.591 + 0.957576 * slide_y
// (matches certified slide_002's fit 18.63/0.96123, 0.95556 within JPEG-stroke noise).
// Badge cross-check: frame yellow-fill bbox center (875.5, 71.0) -> slide (891.8, 74.8)
// vs house badge (893, 71) — same ~1-4px JPEG-bbox offset class as certified slide_002
// (891.4, 73.8), confirming this frame uses the SAME playlist template.
//
// TITLE INK (slide pts, from CC analysis scratch/slide003/cc_analysis_output.txt):
// mixed-size single line on ONE baseline (frame baseline y=216 -> slide 226.0):
//   "Review of"  ink x 286..549 (cx 417.5 -> slide 416.0), R cap top frame 174
//                (slide 182.4). Ink width 264px -> 273.6pt slide; Arial Bold advance
//                fit ("Review of" 4.585em ink) -> em = 59.7pt -> 60pt bold.
//   "Part I"     ink x 569..674 (cx 621.5 -> slide 628.0 -> box 627.5), P cap top
//                frame 183 (slide 191.5). Ink width 106px -> 109.2pt slide; Arial
//                Bold advance fit ("Part I" 2.316em ink) -> em = 47.2pt -> 47pt bold.
//   Both runs share baseline slide ~226.0 (measured); spec typography_notes' ~54/~40pt
//   were estimates — the frame-measured fits above win (fidelity law).
//   "Review of" ink center slide 415.6, "Part I" 628.0; the FULL line center
//   (frame 480.0 -> slide 480.6) is centered like every 002 title; the two runs are
//   placed as separate centered boxes at their MEASURED centers (slide_002 per-line
//   precedent) so each run's ink lands exactly.
//   Subtitle "Self Attention Mechanism" ink x 209..748 (cx 478.5 -> slide 478.9),
//   S cap top frame 285 (slide 298.5), baseline frame 318.5 (slide 333.2).
//   Ink width 541px -> 562.8pt slide; Arial Bold advance fit (12.21em ink) ->
//   em = 46.1pt (cap fit 47.4) -> 46.5pt bold. Color: spec #1C1CC8 (frame core
//   RGB(6,0,196) = royal blue + JPEG noise; spec value kept per fidelity law).
// Box y positions use the LO ascent-lead estimate (0.267em, slide_002-calibrated) and
// are CORRECTED by the mandatory closed-loop PIL check (render ink vs mapped targets,
// tolerance ~4px @150dpi = 1.92pt) before judging.
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c), spec's own recreation
// brief step 8 + imagery note):
//   * pen/stylus annotation cursor frozen at frame (440..445, 363..370)px dark strokes,
//     just below the subtitle — the presenter's annotation pointer, not slide content.
//   * black bottom strip, frame rows 519..539 full-width — video player letterbox
//     below the slide bottom (at slide y >= 541 under the fitted mapping), not part
//     of the PPT design.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const BLUE = "1C1CC8"; // spec title/subtitle royal blue (frame core ~(6,0,196) + JPEG noise)
const FONT = "Arial";

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border, badge "3"
drawHouseChrome(pres, s, { numeral: 3 });

// ---- 2. title line "Review of Part I": two runs of DIFFERENT sizes on one shared
// baseline, placed as two centered single-line boxes at the measured ink centers
// (slide pts -> inches = pt/72). valign top + margin 0.
// CLOSED-LOOP CORRECTED (attempt 1 -> 2, scratch/slide003/closed_loop_attempt1.txt):
// A re-fit 60 -> 59.3pt (rendered ink 276.96pt vs 273.7 target) and box center
// 416.0 -> 413.23 (measured ink-center bias +2.32pt); B 47 -> 46.5 (110.88 vs 109.15),
// center 627.5 -> 628.06 (bias -0.38); C center 479.0 -> 480.05 (bias -1.16);
// y leads re-calibrated from the attempt-1 render (0.2828 / 0.2777 / 0.2686 em).
// Box A "Review of" — 59.3pt bold, target ink cx 415.55pt, cap top slide 182.43
s.addText("Review of", {
  x: 413.23 / 72 - 3.0, y: (182.43 - 0.2828 * 59.3) / 72, w: 6.0, h: (1.5 * 59.3) / 72,
  align: "center", valign: "top",
  fontSize: 59.3, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// Box B "Part I" — 46.5pt bold, target ink cx 627.69pt; cap top slide 191.51 so the
// baseline lands on the same line as Box A (both ~224.8-224.9 rendered)
s.addText("Part I", {
  x: 628.06 / 72 - 2.0, y: (191.51 - 0.2777 * 46.5) / 72, w: 4.0, h: (1.5 * 46.5) / 72,
  align: "center", valign: "top",
  fontSize: 46.5, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 3. subtitle "Self Attention Mechanism" — 46.5pt bold, target ink cx 478.91pt
s.addText("Self Attention Mechanism", {
  x: 480.05 / 72 - 4.25, y: (298.5 - 0.2686 * 46.5) / 72, w: 8.5, h: (1.5 * 46.5) / 72,
  align: "center", valign: "top",
  fontSize: 46.5, bold: true, color: BLUE, fontFace: FONT, margin: 0,
});

// ---- 4. everything below the subtitle stays EMPTY (spec step 7): no bullets,
// charts, images; the pen cursor and letterbox are omitted artifacts.

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_003_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
