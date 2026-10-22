// COMPONENT (banked post-certification) — slide 008 "Linear Classification" (ML lecture 02).
// Copy of build/slide_008.js with the chrome require re-pointed to this dir
// (build/components/house_chrome.js, depth-independent) per the DL-deck precedent.
// Root slide (no parents, no children in this deck's dep graph; banked as a
// playlist-scoped component after PASS).
//
// Ground truth (PIL-measured from unique_slides/slide_008.jpg, 960x540, 1px=1pt):
//   - title ink "Linear Classification": x 282..690, y 248..280 (center 486,264;
//     essentially slide-centered), bold Arial, red (spec-validated #C8102E)
//   - badge = house chrome canon (876,73) d35, numeral 8
//   - ONLY other ink is the screen-recording cursor at ~(622..638, 416..431) —
//     an artifact, excluded per judge GROUND RULES clause (c). Never draw it.
//
// House chrome: shared_patterns/house_chrome.js (THIS deck's measured geometry:
// white canvas, gray E9E9E7 panel x61..899 y46->bottom, C00000 1pt border,
// bottom red stroke rows 538-539, badge FDFD96 + 6A5ACD ring, numeral 333333).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.join(__dirname, "house_chrome.js"));

// ---- content constants (measured) -----------------------------------------
const TITLE_TEXT = "Linear Classification";
const TITLE_COLOR = "C8102E"; // spec-validated title_text color
const TITLE_SIZE = 45;        // ink height 33px over caps/ascenders -> ~45pt (closed-loop verified)
// Original ink width 409px (x 282..690) vs LO's 45pt Arial-Bold render at 433px:
// the original is tighter-tracked. -1.15pt x 21 chars ~= -24px closed-loop match
// (attempt 2 fix; height stays 33px so the size is right, only tracking differs).
const TITLE_CHARSP = -1.15;
// title box spans the gray panel horizontally, offset +6px right: the ORIGINAL
// ink center is x=486 (not panel-center 480; consistent with a leading space in
// the source deck's centered text). Closed-loop: ink 281..691 vs GT 282..690.
const TITLE_BOX = {
  x: 67 / 72,            // panel left edge + 6px measured-center offset
  y: (264 / 72) - 0.75,  // center 264px minus half box height
  w: (899 - 61 + 1) / 72, // panel width
  h: 1.5,
};

// ---- per-block draws (component exports) ----------------------------------
function drawTitle(pptx, slide, opts = {}) {
  slide.addText(opts.text || TITLE_TEXT, {
    x: TITLE_BOX.x, y: TITLE_BOX.y, w: TITLE_BOX.w, h: TITLE_BOX.h,
    align: "center", valign: "middle",
    fontSize: opts.size || TITLE_SIZE, bold: true, color: TITLE_COLOR,
    fontFace: "Arial", margin: 0,
    charSpacing: opts.charSpacing === undefined ? TITLE_CHARSP : opts.charSpacing,
  });
}

// renderBase: full slide composition (chrome + title). Children would import
// this and pass { numeral: <their printed number> }.
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 8 : opts.numeral });
  drawTitle(pptx, slide, opts);
}

// ---- build ----------------------------------------------------------------
function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "../slide_008_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawTitle, TITLE_BOX, TITLE_COLOR, TITLE_SIZE, TITLE_TEXT, TITLE_CHARSP };
