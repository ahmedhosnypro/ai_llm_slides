// House chrome for the Deep Learning DSAI 308 playlist — founder directive 2026-10-11.
//
// LAW: EVERY recreated slide in videos/deep-learning/ (ALL lectures) uses EXACTLY this
// outer frame size/position and this badge position/size — measured from the reference
// frame videos/deep-learning/001_transformers_part1/unique_slides/slide_001.jpg
// (960x540 px, 1px = 1pt = 1/72 in). Per-slide content varies; the chrome does not.
// After building, run house_chrome_check.py against the 150dpi render (closed loop).
//
// Colors (JPEG-soft samples reconciled with the certified slide-002 build):
//   canvas FFFFFF | panel E9E9E7 | border C00000 | badge fill FDFD96
//   badge ring 6A5ACD (~2pt) | numeral 333333, bold, Arial

const CHROME = {
  slide: { w: 13.333, h: 7.5, layout: "LAYOUT_WIDE" },
  canvas: "FFFFFF",
  // gray panel: x 42..918 px, y 45 px .. slide bottom (bottom stroke at rows 538-539,
  // half-visible — reproduce by letting the rect's bottom edge sit at the slide bottom).
  panel: { x: 42 / 72, y: 45 / 72, w: (918 - 42 + 1) / 72, h: (540 - 45) / 72, fill: "E9E9E7" },
  border: { color: "C00000", width: 1 },
  // badge circle: center (893, 71) px, diameter ~36 px
  badge: {
    cx: 893 / 72, cy: 71 / 72, d: 36 / 72,
    fill: "FDFD96", ring: "6A5ACD", ringWidth: 2,
    numeralColor: "333333", numeralSize: 18, fontFace: "Arial",
  },
};

/**
 * Draw the playlist house chrome onto a slide.
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
