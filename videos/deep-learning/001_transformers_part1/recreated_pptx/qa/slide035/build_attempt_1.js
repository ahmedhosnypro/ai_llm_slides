// slide_035.js — build the single-version deliverable slide_035_recreated.pptx
// (SINGLE-VERSION law: one plain-named pptx).
//
// CHILD of slide 034 (dependency 35←34, founder directive 2026-10-11):
// the composition is slide 34's CERTIFIED component (renderBase, frozen) with
// numeral 35, plus THIS slide's delta — the light-blue "Scale down Weights"
// callout box. Verified by frame diff (scratch/slide035/diff34_35): the only
// changes vs slide_034.jpg are the blue box (x403..916, y122..243 px) and the
// badge numeral 34→35 — pure addition, nothing removed/replaced.
//
// DELTA GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_035.jpg
// (960x540, 1px = 1pt, in = px/72). Box: navy border x 403/916, y 122/243,
// rounded corners r≈13px; fill D4E4FB (measured core; spec's #CCE0F5 is the
// approx-hex — measured wins per the parent's palette precedent). Four text
// lines, all ~18pt navy (ink core (2,2,132)≈#000080), centered on x≈653:
//   L1 'Scale down "Weights" Values'  bold italic   cap y131..144 (center ~138)
//   L2 'before applying SoftMax'      italic        asc y153..168 (center ~161)
//   (blank gap ~45px = 2 line pitches)
//   L3 'Scaling Factor should be related to' ('Scaling Factor' bold italic)
//                                                   cap y198..211 (center ~205)
//   L4 'Embedding Dimension "d"'      italic        cap y220..233 (center ~227)
// Line pitch 22-23px. Quotes around Weights/d are literal characters.
// The mouse cursor over 'Embedding' in the original is a recording artifact —
// omitted (judge ground rule c).
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//        videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_035.js
const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase, px, C } = require(path.join(__dirname, "components", "slide_034.js"));

// delta palette (measured from slide_035.jpg)
const NAVY = "000080";   // callout border + text (measured ink core (2,2,132))
const BLUE_FILL = "D4E4FB"; // callout fill (measured median (212,228,251))

const SANS = "Arial";

function drawScaleBox(pptx, slide) {
  // rounded callout: border x 403..916, y 122..243, corner r≈13px
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(403), y: px(122), w: px(514), h: px(122), rectRadius: 0.18,
    fill: { color: BLUE_FILL }, line: { color: NAVY, width: 1.25 },
  });
  // four centered text lines (separate boxes at measured line centers;
  // box w 500 centered on ink center x≈653 → x 403, w 500)
  const lineBox = { x: px(403), w: px(500), align: "center", valign: "middle", margin: 0, fontFace: SANS };
  // L1 — bold italic
  slide.addText('Scale down "Weights" Values', {
    ...lineBox, y: px(126), h: px(24), fontSize: 20, bold: true, italic: true, color: NAVY,
  });
  // L2 — italic
  slide.addText("before applying SoftMax", {
    ...lineBox, y: px(149), h: px(24), fontSize: 20, italic: true, color: NAVY,
  });
  // L3 — 'Scaling Factor' bold italic + rest italic
  slide.addText(
    [
      { text: "Scaling Factor ", options: { bold: true, italic: true } },
      { text: "should be related to", options: { italic: true } },
    ],
    { ...lineBox, y: px(193), h: px(24), fontSize: 20, color: NAVY }
  );
  // L4 — italic
  slide.addText('Embedding Dimension "d"', {
    ...lineBox, y: px(215), h: px(24), fontSize: 20, italic: true, color: NAVY,
  });
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pres.author = "slide-recreation pipeline";
pres.title = "Self Attention Mechanism (Embedding Vector Dimension and Softmax Sensitivity)";

const slide = pres.addSlide();
// base = parent's certified composition (chrome included; badge numeral 35)
renderBase(pres, slide, { numeral: 35 });
// delta
drawScaleBox(pres, slide);

const OUT = path.join(__dirname, "..", "slide_035_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
