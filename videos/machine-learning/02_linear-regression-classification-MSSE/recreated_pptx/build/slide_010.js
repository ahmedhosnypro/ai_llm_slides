// slide_010.js — "Classification – Two Dimensional Case" + decision boundary (ML lecture 02, MSSE deck)
// CHILD of slide 9 (founder graph: 10 > 9). COMPOSITION (dependency law):
//   base   = parent's judge-certified component videos/machine-learning/02_linear-regression-classification-MSSE/
//            recreated_pptx/build/components/slide_009.js — renderBase(pptx, slide, {numeral: 10})
//            imported, NOT re-derived; house chrome drawn ONCE inside it (badge numeral via opts.numeral).
//   delta  = this slide's own additions ONLY, measured on unique_slides/slide_010.jpg
//            (960x540, 1px=1pt; measurements banked in scratch/ml02/slide010/):
//     1. drawDecisionLine — navy 000080 straight line, butt ends, no arrowheads,
//        from (172, 432.5) to (548, 168.5) frame px; stroke ~2.75pt (measured core 2.6px,
//        +AA 3.3px); slope fit y = -0.7021x + 553.4 (closed-loop fit over 376 columns).
//        Separates Steel cluster (above) from Wood cluster (below).
//     2. drawConclusion — 2-line block INSIDE the plot frame, lower-right, CENTER-aligned
//        at cx=682 (line1 ink x570..794 center 682; line2 x564..800 center 682):
//          "Data is linearly separable"      red 8B0000, cap top y404, baseline ~417.5
//          "Linear Classifier is sufficient" navy 000080, cap top y427, baseline ~439.5
//        17pt Arial bold italic (word-width closed-loop: "Classifier" predicted 76.5px @17pt
//        bold vs 77.5px measured; cap 13 rows between certified 17pt=12 / 19pt=14 refs),
//        line pitch 23px (cap-top 404 -> 427).
//   badge  = numeral 10 (printed on the original; renderBase opts.numeral).
// Inheritance verification (scratch/ml02/slide010/diff2_out.txt + measure_2_out.txt): every
// parent block is pixel-identical between slide_009.jpg and slide_010.jpg (title/plot frame/
// axes/labels/caption/legend/model box: 0 px>70 diff; x-axis + Weight label differ by 1px =
// sub-pixel frame noise, inherited as certified). Cluster-band diffs are the line crossing.
// No parent blocks are skipped, replaced or removed.

const pptxgen = require("pptxgenjs");
const path = require("path");
const parent = require(path.resolve(__dirname, "components/slide_009.js"));

const PL = 1 / 72; // px -> inch
const NAVY = "000080";   // decision line + conclusion line 2 (measured core (0,0,122..126))
const RED = "8B0000";    // conclusion line 1 (measured core (130,14,37) ≈ 8B0000)

// ---- delta draws -------------------------------------------------------------

// Decision boundary: navy straight line (172,432.5)->(548,168.5).
function drawDecisionLine(pptx, slide, opts = {}) {
  slide.addShape(pptx.ShapeType.line, {
    x: 172 * PL, y: 168.5 * PL, w: (548 - 172) * PL, h: (432.5 - 168.5) * PL,
    flipV: true, // rising diagonal: bottom-left -> top-right
    line: { color: NAVY, width: 2.75 },
  });
}

// Conclusion block: 2 center-aligned bold italic lines at cx=682, cap tops y404/y427.
// Box top y=397 (closed-loop attempt 1: y392 rendered cap tops 399.4/421.9 -> +4.6px shift
// measured; selfcheck_1_out.txt).
function drawConclusion(pptx, slide, opts = {}) {
  slide.addText(
    [
      { text: "Data is linearly separable", options: { color: RED, breakLine: true } },
      { text: "Linear Classifier is sufficient", options: { color: NAVY } },
    ],
    {
      x: (682 - 140) * PL, y: 397 * PL, w: 280 * PL, h: 60 * PL,
      align: "center", valign: "top", bold: true, italic: true, fontSize: 17,
      fontFace: "Arial", margin: 0, lineSpacing: 23,
    }
  );
}

// ---- build -------------------------------------------------------------------
function render(pptx, slide, opts = {}) {
  parent.renderBase(pptx, slide, { numeral: 10 });
  drawDecisionLine(pptx, slide, opts);
  drawConclusion(pptx, slide, opts);
}

function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  render(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "../slide_010_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { render, drawDecisionLine, drawConclusion, NAVY, RED };
