// components/slide_035.js — CERTIFIED COMPONENT for 001_introduction slide 35
// "How to Apply Filter on image" (Deep Learning DSAI 308 playlist).
//
// BANKED per the dependency law (founder directive 2026-10-11/12): slide 41 depends on
// slide 35 (edges 41<-35) and will IMPORT this component and draw only its delta.
// Source of truth: build/slide_035.js (this module is the same draw sequence, exported
// at BLOCK granularity; the live build script requires THIS module and calls renderBase).
//
// Blocks (in certified draw order):
//   panelRect     — white computation panel rect + gray border (379.5..885.5 x 168.5..431.5)
//   leftGrid      — baked crop build/assets/leftgrid035.png at (77,207) 167x131
//   filterTable   — 3x3 yellow table x270 y219 94x72, #8BD33F borders, Verdana Bold 15
//   panelContent  — baked crop build/assets/panelcontent035.png at (398,185) 478x236
//                   (grids + multipliers + curved arrow + output grid + '4' cell baked;
//                   cursor inpainted out)
//   labels        — "Image" / "Filter", Arial Bold 27.5 black
//   title         — "How to Apply Filter on image", Arial Bold 33 C00000, center 489.5
//   captionBox    — light-yellow rect + soft blue border (x67.5 y446 823x61)
//   captionL1     — navy italic line (Arial Italic 23.5)
//   captionL2     — navy paren + red bold span + red bold underlined PERCEPTRON + navy paren
// Chrome is drawn via the shared playlist primitive (shared_patterns/house_chrome.js) —
// never re-drawn here.
//
// opts: { numeral (default "35"), skip: [block names], only: [block names] }.
// Measurement provenance and deviation notes: see build/slide_035.js header +
// qa/slide035/ (measure passes 1-6, self-checks, judge transcript).

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

// ---- palette (measured) ----
const RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const PANEL_BORDER = "BFBFBF";
const FILTER_BORDER = "8BD33F";
const CAP_FILL = "FCFEE9";
const CAP_BORDER = "9797B2";
const NAVY = "0000CC";
const L2RED = "C00000";

const px = (v) => v / 72;

const BLOCKS = {
  panelRect(pptx, slide) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(379.5), y: px(168.5), w: px(506), h: px(263),
      fill: { color: WHITE }, line: { color: PANEL_BORDER, width: 1.5 },
    });
  },
  leftGrid(pptx, slide) {
    slide.addImage({
      path: `${ASSETS}/leftgrid035.png`,
      x: px(77), y: px(207), w: 167 / 72, h: 131 / 72,
    });
  },
  filterTable(pptx, slide) {
    slide.addTable(
      [
        [{ text: "1" }, { text: "0" }, { text: "1" }],
        [{ text: "0" }, { text: "1" }, { text: "0" }],
        [{ text: "1" }, { text: "0" }, { text: "1" }],
      ],
      {
        x: px(270), y: px(219), w: px(94), h: px(72),
        colW: [px(31.33), px(31.33), px(31.34)],
        rowH: [px(24), px(24), px(24)],
        fill: { color: "FFFF00" },
        border: { type: "solid", pt: 1.5, color: FILTER_BORDER },
        align: "center", valign: "middle", margin: 0,
        fontFace: "Verdana", fontSize: 15, bold: true, color: BLACK,
      }
    );
  },
  panelContent(pptx, slide) {
    slide.addImage({
      path: `${ASSETS}/panelcontent035.png`,
      x: px(398), y: px(185), w: 478 / 72, h: 236 / 72,
    });
  },
  labels(pptx, slide) {
    slide.addText("Image", {
      x: px(103), y: px(172), w: px(120), h: 0.5,
      align: "left", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 27.5, bold: true, color: BLACK,
    });
    slide.addText("Filter", {
      x: px(273), y: px(173.5), w: px(120), h: 0.5,
      align: "left", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 27.5, bold: true, color: BLACK,
    });
  },
  title(pptx, slide) {
    slide.addText("How to Apply Filter on image", {
      x: px(489.5) - 6, y: px(51.7), w: 12, h: 0.8,
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 33, bold: true, color: RED,
      lineSpacing: 40,
    });
  },
  captionBox(pptx, slide) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(67.5), y: px(446), w: px(823), h: px(61),
      fill: { color: CAP_FILL }, line: { color: CAP_BORDER, width: 1.5 },
    });
  },
  captionL1(pptx, slide) {
    slide.addText("Apply Filter on Image is a Dot product between image values and filter values", {
      x: px(78.5), y: px(444.5), w: px(815), h: 0.5,
      align: "left", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 23.5, italic: true, color: NAVY,
    });
  },
  captionL2(pptx, slide) {
    slide.addText(
      [
        { text: "(", options: { color: NAVY, bold: false } },
        { text: "can be modeled  by ", options: { color: L2RED, bold: true } },
        { text: "PERCEPTRON", options: { color: L2RED, bold: true, underline: true } },
        { text: " )", options: { color: NAVY, bold: false } },
      ],
      {
        x: px(83.5), y: px(469.5), w: px(500), h: 0.5,
        align: "left", valign: "middle", margin: 0,
        fontFace: "Arial", fontSize: 23.5, italic: true,
      }
    );
  },
};

function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? "35" : opts.numeral;
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  drawHouseChrome(pptx, slide, { numeral });
  for (const name of Object.keys(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    BLOCKS[name](pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, CHROME_COLORS: { RED, BLACK, WHITE, PANEL_BORDER, FILTER_BORDER, CAP_FILL, CAP_BORDER, NAVY, L2RED } };
