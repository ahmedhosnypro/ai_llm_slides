// slide_020.js — "Self Attention Mechanism" section divider
// (Deep Learning DSAI 308, Transformers — Part I)
//
// Spec: analysis/slide_020_final.json (PASS_WITH_FIXES; score 9 per DB). Course-authored
// section divider — the slide's ONLY content is the house chrome + the centered red
// title + the badge numeral "20" (SOURCES.md: no external source, no figures, cursor
// artifact excluded per judge GROUND RULES (c)).
//
// Chrome law (founder directive 2026-10-11, playlist-wide, MANDATORY): the outer chrome
// is the SHARED module videos/deep-learning/shared_patterns/house_chrome.js —
// white FFFFFF canvas, gray E9E9E7 panel x 42..918px / y 45px..slide bottom (bottom
// stroke half-visible at the slide edge), badge circle d36px at center (893,71)px,
// FDFD96 fill + 6A5ACD ~2pt ring, bold 18pt 333333 numeral. The bottom rule the spec
// lists as a separate element (measured rows 538-539, x 38..921 in the frame) IS the
// panel's half-visible bottom border stroke in this template — certified precedent
// slide_001 relies on the chrome stroke alone; the chrome's x-extent (42..918 vs
// 38..921, ~0.055in/side) is house law and overrides.
//
// Content measurements (unique_slides/slide_020.jpg, 960x540 px, 1px = 1pt = 1/72 in):
//   title ink  x=[184,774] (width 591px, center 479px = 6.653in — panel/slide-centered),
//     band y=[261,297]; 'S' cap rows 263..297 (cap 35px), 'l' ascender rows 261..297
//     (37px); baseline y=297px=4.125in; ink-color core (192,15,33) = C00000 family
//     (spec: C00000, same core as certified slide_001 title).
//   Font size: advance-derived 591px/12.224em = 48.35pt; cap-derived ~51pt; slide_002
//     measured LO Arial-bold ~2% narrow vs frame -> authored 50pt start, closed-loop
//     calibrated against the 150dpi render (width + cap height).
//   Vertical: valign-middle box centered on ink-center 279px = 3.875in, with the
//     line-box/ink offset pre-corrected (+0.105em, ~5.3pt @50pt) -> first-guess box
//     center 3.949in; closed-loop corrected on the render.
//   Mouse-cursor artifact over the title (~x520,y280): screen-capture artifact, OMITTED
//     (spec brief step 7; judge GROUND RULES (c)).
//
// pptxgenjs laws: no '#' in hex, fontFace everywhere, margin:0, writeFile({fileName}).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in

const RED = "C00000"; // title (frame-measured core (192,15,33); certified-slide precedent C00000)
const FONT = "Arial";

const TITLE = "Self Attention Mechanism"; // verbatim, title case, one line

// closed-loop calibration knobs (measured on scratch render #1 @50pt: width 604 vs 591
// frame-px, ink center y 285.7 vs 279 -> font 49, cy -0.093in)
const TITLE_FONT = 49;   // advance-derived 48.35 + LO-narrow correction; cap-derived ~51
const TITLE_BOX_CY = 3.856; // closed-loop: render#1 ink-center 285.7 frame-px vs orig 279
const TITLE_BOX_H = 1.2;

const s = pres.addSlide();

// ---- 1. playlist house chrome: white canvas, gray panel + red border
//       (bottom stroke = the slide's bottom rule), badge "20"
drawHouseChrome(pres, s, { numeral: 20 });

// ---- 2. centered red title at its MEASURED position (fidelity law; the ml-intro
//       title-box y=0.28 rule is superseded for this playlist)
s.addText(TITLE, {
  x: CHROME.panel.x, w: CHROME.panel.w,
  y: TITLE_BOX_CY - TITLE_BOX_H / 2, h: TITLE_BOX_H,
  align: "center", valign: "middle",
  fontSize: TITLE_FONT, bold: true, color: RED, fontFace: FONT, margin: 0,
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_020_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
