// verify_component_refresh_9.js — rebuild slide 009 from the REFRESHED
// components/slide_009.js (attempt-7 annotation geometry) and prove it is
// pixel-identical to the certified render_7. Pass the output pptx path as argv[2].
const path = require("path");
const pptxgen = require("pptxgenjs");
const base = require(path.resolve(__dirname, "components", "slide_009.js"));

const OUT = process.argv[2];
if (!OUT) throw new Error("usage: node verify_component_refresh_9.js <out.pptx>");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
base.renderBase(pptx, slide, { numeral: 9 });

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
