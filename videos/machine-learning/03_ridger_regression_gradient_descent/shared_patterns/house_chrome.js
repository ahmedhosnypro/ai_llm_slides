// House chrome for the machine-learning lecture 03 deck
// (03_ridger_regression_gradient_descent) — measured 2026-10-19 from the
// reference frame unique_slides/slide_003.jpg and verified constant across
// slides 001/005/009/018/040 (badge bbox identical on all; strokes present on
// left/right/bottom, ABSENT on top — a structural difference from lecture 02).
//
// LAW: EVERY recreated slide in THIS video uses EXACTLY this outer frame
// size/position and this badge position/size (960x540 frame, 1px = 1pt = 1/72 in).
// Per-slide content varies; the chrome does not. After building, run
// shared_patterns/house_chrome_check.py against the 150dpi render (closed loop).
//
// TEMPLATE FAMILY: same family as lecture 02 (white canvas + gray E9E9E7 panel
// + red border + yellow FDFD96 badge with purple ring) but the MEASURED GEOMETRY
// DIFFERS from 02's ratified values (02: panel x61..899 with a TOP stroke;
// THIS deck: panel x54..903 and NO TOP STROKE). Use THIS deck's values here.
//
// Measured 2026-10-19 (slide_003.jpg, cross-checked 001/005/009/018/040):
//   canvas FFFFFF | panel fill E9E9E7 (measured (231,233,230)), gray band x 54..903,
//   y 45..540 (bottom at slide edge) | strokes: LEFT vertical at x 58-59 (2px),
//   RIGHT vertical at x 901, BOTTOM horizontal rows 537-539 half-visible at the
//   slide edge, spanning cols 58..902; vertical strokes span rows 47..539;
//   NO TOP STROKE (top band red px = 0 on all five measured frames).
//   Stroke cores measure dark-maroon on the JPEG frames — left (114,40,51),
//   right (107,47,56), bottom (125,0,19) — JPEG-darkened C00000 family strokes
//   (same measurement pattern as 02's originals); the founder-ratified family
//   nominal C00000 is what the certified 02 builds draw and judges PASS.
//   badge: center (876, 73.5) px, d ~35 | fill FDFD96 | ring 6A5ACD ~2pt |
//   numeral 333333 bold Arial 18pt — IDENTICAL to 02's measured badge.

const CHROME = {
  slide: { w: 13.333, h: 7.5, layout: "LAYOUT_WIDE" },
  canvas: "FFFFFF",
  // gray panel: NO border line on the rect — the strokes are drawn separately
  // because THIS deck has NO top stroke (rect.line would stroke the top too).
  panel: { x: 54 / 72, y: 45 / 72, w: (903 - 54 + 1) / 72, h: (540 - 45) / 72, fill: "E9E9E7" },
  strokes: { color: "C00000", width: 1 },   // family nominal (see measured note above)
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
 * @param {object} opts   { numeral: string|number } — the badge numeral (= the
 *                        file number N; the originals print it; no zero-padding)
 */
function drawHouseChrome(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? "" : String(opts.numeral);
  slide.background = { color: CHROME.canvas };
  slide.addShape(pptx.ShapeType.rect, {
    x: CHROME.panel.x, y: CHROME.panel.y, w: CHROME.panel.w, h: CHROME.panel.h,
    fill: { color: CHROME.panel.fill },
    // no line: this deck has no top stroke; strokes drawn below
  });
  const st = CHROME.strokes;
  // left vertical stroke: x 58.5, rows 46..539
  slide.addShape(pptx.ShapeType.line, {
    x: 58.5 / 72, y: 46 / 72, w: 0, h: (539 - 46) / 72,
    line: { color: st.color, width: st.width },
  });
  // right vertical stroke: x 901, rows 46..539
  slide.addShape(pptx.ShapeType.line, {
    x: 901 / 72, y: 46 / 72, w: 0, h: (539 - 46) / 72,
    line: { color: st.color, width: st.width },
  });
  // bottom horizontal stroke: y 538.5, cols 58..902 (half-visible at slide edge)
  slide.addShape(pptx.ShapeType.line, {
    x: 58 / 72, y: 538.5 / 72, w: (902 - 58) / 72, h: 0,
    line: { color: st.color, width: st.width },
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
