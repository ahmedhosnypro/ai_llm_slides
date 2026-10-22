// House chrome for the machine-learning lecture 02 deck
// (02_linear-regression-classification-MSSE) — measured 2026-10-13 from the
// reference frame unique_slides/slide_003.jpg and verified identical on the
// parent slides 001/004/009/018/025/028/031 (badge bbox constant across all).
//
// LAW: EVERY recreated slide in THIS video uses EXACTLY this outer frame
// size/position and this badge position/size (960x540 frame, 1px = 1pt = 1/72 in).
// Per-slide content varies; the chrome does not. After building, run
// shared_patterns/house_chrome_check.py against the 150dpi render (closed loop).
//
// TEMPLATE FAMILY: same family as the deep-learning DSAI 308 playlist (white
// canvas + gray E9E9E7 panel + red C00000 border + yellow FDFD96 badge with
// purple ring) — but the MEASURED GEOMETRY DIFFERS from the DL playlist values
// (DL: panel x42..918, badge center (893,71) d36; THIS deck: panel x61..899,
// badge center (876,73) d35). Use THIS deck's values here, never DL's.
// NOTE: 01_ml-intro (lecture 01 of this playlist) uses the OLD ml-intro chrome
// (E8E8E8 canvas, C00000 0.15in frame, outline-less FFF9C4 badge) — a different
// template. Do not mix either of those into this deck.
//
// Colors (JPEG-soft samples; nominal values follow the certified deep-learning
// family precedent):
//   canvas FFFFFF | panel E9E9E7 | border C00000 | badge fill FDFD96
//   badge ring 6A5ACD (~2pt) | numeral 333333, bold, Arial
//   (measured ring core on thin-stroke frames is darker, ~(57,19,78) — same
//   measurement as the certified DL renders' originals; the founder-ratified
//   family nominal 6A5ACD is what the certified DL builds draw and judges PASS.)

const CHROME = {
  slide: { w: 13.333, h: 7.5, layout: "LAYOUT_WIDE" },
  canvas: "FFFFFF",
  // gray panel: gray interior x 61..899 px, top border stroke at y≈46, bottom
  // red stroke at rows 538-539 half-visible at the slide edge (reproduce by
  // letting the rect's bottom edge sit at the slide bottom).
  panel: { x: 61 / 72, y: 46 / 72, w: (899 - 61 + 1) / 72, h: (540 - 46) / 72, fill: "E9E9E7" },
  border: { color: "C00000", width: 1 },
  // badge circle: center (876, 73) px, diameter ~35 px
  badge: {
    cx: 876 / 72, cy: 73 / 72, d: 35 / 72,
    fill: "FDFD96", ring: "6A5ACD", ringWidth: 2,
    numeralColor: "333333", numeralSize: 18, fontFace: "Arial",
  },
};

/**
 * Draw the deck house chrome onto a slide.
 * @param {object} pptx   the pptxgenjs instance (for ShapeType)
 * @param {object} slide  the slide returned by pptx.addSlide()
 * @param {object} opts   { numeral: string|number } — the badge numeral (printed
 *                        number on the ORIGINAL slide image; no zero-padding)
 */
function drawHouseChrome(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? "" : String(opts.numeral);
  slide.background = { color: CHROME.canvas };
  slide.addShape(pptx.ShapeType.rect, {
    x: CHROME.panel.x, y: CHROME.panel.y, w: CHROME.panel.w, h: CHROME.panel.h,
    fill: { color: CHROME.panel.fill },
    line: { color: CHROME.border.color, width: CHROME.border.width },
  });
  if (numeral !== "") {
    const bx = CHROME.badge.cx - CHROME.badge.d / 2;
    const by = CHROME.badge.cy - CHROME.badge.d / 2;
    slide.addShape(pptx.ShapeType.ellipse, {
      x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
      fill: { color: CHROME.badge.fill },
      line: { color: CHROME.badge.ring, width: CHROME.badge.ringWidth },
    });
    slide.addText(numeral, {
      x: bx, y: by, w: CHROME.badge.d, h: CHROME.badge.d,
      align: "center", valign: "middle", bold: true,
      fontSize: CHROME.badge.numeralSize, color: CHROME.badge.numeralColor,
      fontFace: CHROME.badge.fontFace, margin: 0,
    });
  }
}

module.exports = { CHROME, drawHouseChrome };
