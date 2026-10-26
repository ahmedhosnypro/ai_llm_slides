// INIT (MODE=placeholder) for the continuous final deck — deck 03.
// Builds <total> placeholder pages in slide order 1..N: minimal house-chrome
// page (shared_patterns/house_chrome.js) + "pending recreation" marker.
// Page count/order are CONSTANT from init (final-deck-merge doctrine).
//
// usage: node make_placeholders.js <out.pptx> [total=51]

const path = require("path");
const fs = require("fs");
const PptxGenJS = require("pptxgenjs");
const { drawHouseChrome } = require("../../../shared_patterns/house_chrome.js");

const out = process.argv[2];
const TOTAL = parseInt(process.argv[3] || "51", 10);
if (!out) {
  console.error("usage: node make_placeholders.js <out.pptx> [total=51]");
  process.exit(2);
}

const pptx = new PptxGenJS();
pptx.layout = "LAYOUT_WIDE"; // the family layout: 13.333x7.5in, 960x540pt — never a custom width
pptx.author = "ai_llm_slides pipeline";
pptx.title = "03 Ridge Regression & Gradient Descent — continuous final deck";

for (let n = 1; n <= TOTAL; n++) {
  const slide = pptx.addSlide();
  drawHouseChrome(pptx, slide, { numeral: n });
  slide.addText("pending recreation", {
    x: 54 / 72, y: 200 / 72, w: (903 - 54) / 72, h: 120 / 72,
    align: "center", valign: "middle",
    fontFace: "Arial", fontSize: 16, italic: true, color: "999999",
  });
}

const tmpOut = out.endsWith(".pptx") ? out + ".tmp" : out + ".tmp.pptx";
pptx.writeFile({ fileName: tmpOut }).then(() => {
  const written = fs.existsSync(tmpOut) ? tmpOut : tmpOut + ".pptx"; // pptxgenjs appends .pptx
  fs.renameSync(written, out);
  const sz = fs.statSync(out).size;
  console.log(`wrote ${out} (${TOTAL} placeholder pages, ${sz} bytes)`);
});
