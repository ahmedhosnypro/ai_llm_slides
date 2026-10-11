// slide_014.js — build "Encoder – Decoder Transformer" (attempt 1).
//
// The composition lives in components/slide_014.js (block-granular, dependency
// contract: slide 15 composes from it). This wrapper just instantiates the deck.
const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase } = require(path.join(__dirname, "components", "slide_014.js"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.author = "AI LLM Slides";
pres.title = "Encoder - Decoder Transformer";

const slide = pres.addSlide();
renderBase(pres, slide, { numeral: 14 });

const OUT = path.join(__dirname, "..", "slide_014_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
