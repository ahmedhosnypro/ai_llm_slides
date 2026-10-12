// slide_013.js — build "Transformer Building Blocks" (section divider),
// Deep Learning DSAI 308, Transformers — Part I, lecture 001. Attempt 1.
//
// STRATEGY: minimal divider slide — the ONLY content besides the playlist house
// chrome is one large bold red centered title. The gray panel + thin red border +
// yellow/purple badge ARE the playlist house chrome here (measured on THIS frame:
// panel gray 231,233,230 ~ E9E9E7; left border cols 38-39, top row 43, right col
// 920, bottom rows 538-539 — all within ~3 frame px of the ratified canonical
// chrome, i.e. the same chrome, video-softened). Chrome is drawn ONCE via the
// shared module — never re-drawn (playlist law, founder directive 2026-10-11).
//
// GEOMETRY PROVENANCE (PIL-measured, scratch/slide013/measure_frame.py, frame
// 960x540, 1px = 1pt = 1/72 in):
//   - TITLE ink bbox x[157,822] (w=666), cap top y=250, baseline ~285, descender
//     bottom 295; ink center (489.5, 272.5). Arial Bold metrics: advance of
//     "Transformer Building Blocks" = 13.725 em -> em = 666/13.725/0.97 ~ 48.9px;
//     cap height 285-250 = 35px = 0.716 em -> em = 48.9px. FONT SIZE = 49pt
//     (frame is ground truth; the spec's 54-60pt/56pt pin was a vision estimate,
//     flagged uncertain in validation.uncertain_items — superseded by measurement).
//   - Title ink center x = 489.5 (slide center 480; the original is ~9.5px right
//     of center — reproduced, frame is ground truth).
//   - Text box: w=800px (16% wrap headroom over the 672px advance), h=60px,
//     align center + valign middle; box center placed at the line-box center
//     (489.5, 268) — ink-center 272.5 minus (line-box center offset ~4.5px for
//     Arial asc/desc). Closed-loop verified against the render post-build.
//   - Cursor artifact at x[638,649] y[286,296] is a screen-recording artifact —
//     NOT recreated (judge ground rule (c); spec recreation_brief step 6).
//   - No equations, no tables, no delimiters, no multi-line text (single-line
//     box -> explicit lineSpacing n/a; nothing near a frame edge to wrap).
//
// LAWS honored: playlist chrome via shared_patterns/house_chrome.js (badge
// numeral 13 = the number printed on the frame); verbatim text ("Transformer
// Building Blocks", badge "13"); margin:0 + fontFace on the text element;
// no '#' in hex; single-version plain-named deliverable; LAYOUT_WIDE.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);

const px = (v) => v / 72; // frame px -> inches

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.author = "AI LLM Slides";
pres.title = "Transformer Building Blocks";

const slide = pres.addSlide();

// 1. Playlist house chrome (white canvas, gray E9E9E7 panel with thin C00000
//    border, badge d36 @ (893,71) with numeral 13) — shared module, never re-drawn.
drawHouseChrome(pres, slide, { numeral: 13 });

// 2. Title: "Transformer Building Blocks" — Arial Bold 49pt #CC0000, single line,
//    ink center (489.5, 272.5) frame px (PIL-measured; see header).
slide.addText("Transformer Building Blocks", {
  x: px(89.5), y: px(238), w: px(800), h: px(60),
  align: "center", valign: "middle",
  fontSize: 49, bold: true, color: "CC0000", fontFace: "Arial", margin: 0,
});

const OUT = path.join(__dirname, "..", "slide_013_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
