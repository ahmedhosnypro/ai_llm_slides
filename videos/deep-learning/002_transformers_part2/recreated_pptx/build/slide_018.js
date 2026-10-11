// slide_018.js — "Adding Position Information" (agenda: [1] Position Encoding /
// [2] Position Embedding) — Deep Learning DSAI 308, video 002_transformers_part2,
// slide 18 (root slide; no dependency edge, no pattern group; badge numeral 18).
//
// CONTENT SPEC: analysis/slide_018_final.json (PASS_WITH_FIXES; recreatability 9).
// Web provenance: slide_018_source/SOURCES.md (BANKED — Vaswani §3.5 "learned and
// fixed" is the paper-level [1]-vs-[2] dichotomy; course-authored agenda, no figure).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): outer chrome is the
// SHARED module videos/deep-learning/shared_patterns/house_chrome.js — white FFFFFF
// canvas, gray E9E9E7 panel x 42..918px / y 45px..slide bottom, thin C00000 border
// (bottom stroke half-visible at the slide edge), badge circle d36px at (893,71)px,
// FDFD96 fill + 6A5ACD ~2pt ring, bold 333333 numeral. Badge numeral = 18 (the
// number printed on THIS original frame; verified in-frame + SOURCES.md).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide018/measure_original.py):
// video 002's capture shows the slide zoomed OUT (~0.958) with a black letterbox
// strip below the slide bottom. Fitted from THIS frame's four chrome border
// landmarks (frame panel left 58.04, right 900.95, top 43.02, bottom-border 516.41
// <-> slide chrome 42, 919, 45, 540):
//   frame_x = 17.674 + 0.96113 * slide_x ;  frame_y = -0.013 + 0.95633 * slide_y
// Badge cross-check: frame badge (yellow-bbox center 875.5, 71.0) maps to slide
// (892.5, 74.3) vs the house badge (893, 71) — dx 0.5 / dy 3.3 px, the SAME accepted
// JPEG-bbox delta as the certified slide_002 build (891.4, 73.8). Same template.
// All content ink below is mapped to TRUE slide coordinates through this transform.
//
// MEASURED INK (slide pts, strict-mask; scratch/slide018/measure_original.json):
//   TITLE "Adding Position Information": ink x 211.6..740.1 (w 528.6, center 475.5;
//      ~5pt LEFT of panel center 480.5 — measured, reproduced as measured),
//      y 211.2..248.9 -> ~40pt Arial Bold (advance-fit 39.6; cap+desc band 37.6pt).
//   WHITE BOX: x 234.4 y 294.9 w 419.3 h 149.5; fill FFFFFF, thin D9D9D9 border,
//      subtle drop shadow (shadow probe: 226.4 just below vs 231.7 panel).
//   LINE 1 "[1] Position Encoding": ink left 265.7 (BOTH lines share the same left
//      edge — LEFT-aligned in the box, per the frame; the spec's validation resolved
//      this to "centered" and flagged it uncertain — frame wins), ink top 318.9,
//      ink w 314.2 -> ~30pt Arial Bold (advance-fit 30.1..31.2 across segments).
//      Runs: "[1] Position " #0000A0 + "Encoding" #CC0000.
//   LINE 2 "[2] Position Embedding": ink left 265.7, top 388.0, ink w 342.3.
//      Runs: "[2] Position " #0000A0 + "Embedding" #CC00CC.
//   Line pitch (ink top -> ink top) 69.0pt — reproduced by per-line placement.
//   Colors: PIL-census cores #B60D1F / #080093 / #AA00B1 sit ~0.83-0.92x BELOW the
//      spec hexes (uniform video/JPEG darkening of saturated dark inks; the light
//      badge yellow measures UNdarkened #FCFF99 ~= FDFD96). Spec hexes win
//      (approx-hex law; precedent: certified slide_002 built C00000 from a measured
//      (187,16,32) core).
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c), founder artifact law;
// both flagged in the spec's imagery/uncertain_items):
//   * presenter mouse cursor at frame (392..401, 239..249) just below the title.
//   * black letterbox strip, frame rows 519..539 full-width — BELOW the 540pt slide
//     bottom under the fitted mapping (video player strip, not slide content).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pt = (v) => v / 72; // slide pts -> inches

// ---- measured targets (slide pts) ---------------------------------------------
const T = {
  title: { inkCx: 475.5, inkTop: 211.24, text: "Adding Position Information" },
  box: { x: 234.44, y: 294.87, w: 419.31, h: 149.55 },
  line1: { inkLeft: 265.65, inkTop: 318.94 },
  line2: { inkLeft: 265.65, inkTop: 387.96 },
};

// ---- initial build parameters (CORRECTED by the closed-loop PIL check,
//      tolerance ~4px @150dpi = 1.92pt, before judging) --------------------------
const P = {
  titleSize: 40,   // pt, Arial Bold
  bodySize: 30,    // pt, Arial Bold
  // lead: ink-top offset below a valign-top margin-0 box top, as a fraction of em
  titleLead: 0.28,
  bodyLead: 0.28,
  titleCx: T.title.inkCx, // text box centered on measured ink center
  line1Left: T.line1.inkLeft - 2.1, // box left = ink left - LSB('[') ~0.07em @30pt
  line2Left: T.line1.inkLeft - 2.1,
};

const BLUE = "0000A0";   // "[1] Position" / "[2] Position"
const RED = "CC0000";    // title + "Encoding"
const MAG = "CC00CC";    // "Embedding"
const BOX_LINE = "D9D9D9";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();

// 1) shared playlist chrome (frame + badge 18) — NEVER hand-drawn
drawHouseChrome(pres, s, { numeral: 18 });

// 2) white content box with thin gray border + subtle shadow
s.addShape(pres.ShapeType.rect, {
  x: pt(T.box.x), y: pt(T.box.y), w: pt(T.box.w), h: pt(T.box.h),
  fill: { color: "FFFFFF" },
  line: { color: BOX_LINE, width: 1 },
  shadow: { type: "outer", angle: 90, blur: 5, offset: 2, color: "000000", opacity: 0.25 },
});

// 3) title — centered on the MEASURED ink center (frame is ground truth)
s.addText(T.title.text, {
  x: pt(P.titleCx - 432), y: pt(T.title.inkTop - P.titleLead * P.titleSize),
  w: pt(864), h: pt(P.titleSize * 1.6),
  align: "center", valign: "top", margin: 0,
  fontFace: FONT, fontSize: P.titleSize, bold: true, color: RED,
});

// 4) content lines — LEFT-aligned at the measured common ink left edge,
//    one single-line box per line (exact measured band placement)
s.addText(
  [
    { text: "[1] Position ", options: { color: BLUE } },
    { text: "Encoding", options: { color: RED } },
  ],
  {
    x: pt(P.line1Left), y: pt(T.line1.inkTop - P.bodyLead * P.bodySize),
    w: pt(420), h: pt(P.bodySize * 1.6),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: P.bodySize, bold: true,
  }
);
s.addText(
  [
    { text: "[2] Position ", options: { color: BLUE } },
    { text: "Embedding", options: { color: MAG } },
  ],
  {
    x: pt(P.line2Left), y: pt(T.line2.inkTop - P.bodyLead * P.bodySize),
    w: pt(420), h: pt(P.bodySize * 1.6),
    align: "left", valign: "top", margin: 0,
    fontFace: FONT, fontSize: P.bodySize, bold: true,
  }
);

pres.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_018_recreated.pptx" })
  .then(() => console.log("wrote slide_018_recreated.pptx"));
