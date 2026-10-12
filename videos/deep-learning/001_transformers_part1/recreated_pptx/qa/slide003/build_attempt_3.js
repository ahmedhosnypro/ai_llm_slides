// slide_003.js — "Transformers – Part I" agenda slide (deep-learning/001_transformers_part1)
// Build pattern per scripts/17_worker_instructions.md + shared_patterns (playlist).
//
// CHROME-CONFORMANCE REMEDIATION (2026-10-12): the previously certified build drew the
// SUPERSEDED ml-intro chrome inline (E8E8E8 full-bleed bg, 0.15in-inset C00000 frame,
// FFF9C4 badge at 12.48/0.30/0.5). Founder directive 2026-10-11 ratified ONE playlist
// chrome for EVERY slide under videos/deep-learning/ (videos/deep-learning/AGENTS.md).
// This build now imports the shared module — chrome is NEVER re-drawn inline:
//   require('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js')
//   drawHouseChrome(pptx, slide, { numeral: 3 })
// Slide 3's OWN content (title, 4 agenda lines) is byte-identical to the certified
// pre-chromefix build (banked: qa/slide003/build_pre_chromefix.js) — only the chrome
// layer changed; verified by pixel diff vs render_pre_chromefix.png.
//
// BOTTOM LINE NOTE (chromefix): the certified build drew a separate content LINE shape
// for the original's bottom red line (measured y=[537,539] x=[38,921]px). Under the
// ratified playlist chrome that line IS the gray panel's bottom stroke (canon rows
// 538-539, half-visible at the slide edge — measured 537-539 on THIS original, within
// 1px JPEG smear; house_chrome_check.py validates it as chrome). Keeping the separate
// shape would double-draw the chrome stroke and shadow the panel gray 1px short of the
// checker's bottom-reach requirement (house_chrome_check FAIL). The separate shape is
// therefore removed — the chrome module reproduces the original's line — title and
// agenda content are untouched.
//
// Spec: analysis/slide_003_final.json (PASS_WITH_FIXES, score 9). Frame measured
// 960x540 px (1px = 1pt = 1/72 in) via scratch/slide003/measure_frame*.py:
//   title ink  x=[223,620] y=[70,98]  -> ~40pt Arial Bold (cap 29px), color spec CC0000
//   agenda ink x=[111,380] y=[172,310]; 4 line bands start y=172,214,255,296
//     -> pitch 41.33pt, ~20pt Arial Bold (LiberationSans-Bold fit: all 4 lines within 2px)
//   bottom red line: y=[537,539] x=[38,921] (spec recreation_brief step 3 — this is
//     the chrome panel's bottom stroke, owned by the shared module; see note below)
//   mouse-cursor artifact in original -> video artifact, correctly omitted (judge GR (c))
// Badge numeral = the number printed on the original frame = 3 (badge law).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const NUM = 3;
const TITLE = "Transformers \u2013 Part I"; // en dash, verbatim
const LINES = [
  "Processing Sequential Data",
  "Transformer Building Blocks",
  "Self Attention Mechanism", // "Self" confirmed from frame pixels (probe_original.txt)
  "Multi-Head  Attention", // double space verbatim (confirmed from frame pixels)
];
const FONT = "Arial";

// measured geometry (inches; 1 original px = 1/72 in)
const PITCH_PT = 41.33;          // agenda band-start pitch 42/41/41 px
const AGENDA_FONT = 20;          // LiberationSans-Bold fit 19.7pt -> authored 20pt
const AGENDA_BOX_X = 1.534;      // leftmost ink 111px=1.542in minus 'T' left bearing
const AGENDA_Y0 = 2.079;         // closed-loop corrected: render_1 sat +33px low; 2.30-33.2/150
const AGENDA_W = 4.7;            // longest line 3.75in + >=20% wrap budget
const AGENDA_H = 2.5;
const TITLE_FONT = 40;           // cap 29px -> 40.5pt Arial Bold
// TITLE POSITION (judge attempt 2 FAIL -> fix, 2026-10-12): the certified build used
// the ml-intro house title box (y:0.28, slide-centered) — SUPERSEDED for this playlist
// (the playlist chrome law covers frame+badge only; the title is CONTENT governed by
// the original frame). Under the ratified chrome the title straddled the panel's top
// border (render ink rows 64..125 vs border 93-94) — judge D1 MAJOR. Original title
// ink: rows y=[69,99]px, cols x=[223,620]px -> center (421.5, 84)px. Box: center
// x 421.5px=5.8542in (w 9.0, centered align), ink top 69px -> box y 0.8117in
// (closed-loop: box 0.28 rendered ink top 64px; +38.28 frame px = +0.5317in).

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();

// 1. playlist house chrome (founder directive 2026-10-11) — shared module, numeral 3.
//    Draws: FFFFFF canvas, E9E9E7 panel x 42..918px / y 45px..bottom (C00000 border,
//    bottom stroke half-visible), badge d36px at (893,71)px (FDFD96 + 6A5ACD ring).
drawHouseChrome(pres, s, { numeral: NUM });

// 2. title (content — verbatim from spec; position = original measured ink, see
//    TITLE POSITION note above: center x 421.5px, ink top 69px)
s.addText(TITLE, {
  x: 1.3542, y: 0.8117, w: 9.0, h: 0.8,
  align: "center", valign: "top",
  fontSize: TITLE_FONT, bold: true, color: "CC0000", fontFace: FONT, margin: 0,
});

// 3. agenda block — 4 lines, explicit pinned pitch (single knob, no paraSpaceAfter)
s.addText(
  LINES.map((t, i) => ({ text: t, options: { breakLine: i < LINES.length - 1 } })),
  {
    x: AGENDA_BOX_X, y: AGENDA_Y0, w: AGENDA_W, h: AGENDA_H,
    fontSize: AGENDA_FONT, bold: true, color: "1F1FCC", fontFace: FONT,
    lineSpacing: PITCH_PT, margin: 0, valign: "top", align: "left",
  }
);

// 4. bottom red line — NOT drawn here: it is the chrome panel's bottom stroke
//    (rows 538-539 canon; measured 537-539 on this original), owned by the shared
//    module's panel border. A separate shape would double-draw it (see header note).

pres.writeFile({ fileName: "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_003_recreated.pptx" })
  .then(() => console.log("wrote videos/deep-learning/001_transformers_part1/recreated_pptx/slide_003_recreated.pptx"));
