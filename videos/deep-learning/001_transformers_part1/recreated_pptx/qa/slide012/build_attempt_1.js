// slide_012.js — build "Attention Is All You Need" (arXiv 1706.03762v5 page-1
// screenshot slide) — attempt 1.
//
// STRATEGY (per 001_transformers_part1/AGENTS.md + slide_012_source/SOURCES.md):
// the slide IS the paper's first page as a course screenshot; the founder-banked
// v5 PDF/page raster is the declared ground truth for it. The build therefore
// embeds the banked v5 page-1 raster (rendered 300dpi from
// slide_012_source/1706.03762v5.pdf), CROPPED to exactly the frame's visible
// window (the crop reproduces the original's artifacts by construction:
// "arXiv:1" of the rotated stamp cut at the left/bottom, abstract cut
// mid-sentence at the container bottom edge, running header excluded).
// Instructor markup that is baked into the frame's screenshot region is baked
// into the asset with the measured alpha compositing (PIL, same math as the
// renderer): tan title box + tan stamp-date band (alpha .30 over #EB7C00-family
// fill), 6 pink affiliation boxes (alpha .52 magenta) — measured from the frame
// (interior-over-white AND glyph-core-over-black anchors agree).
// Drawn as shapes: playlist house chrome (shared module) + the container's
// thin red border. Mouse cursor(s) in the frame are capture artifacts — omitted
// per judge ground rule (c).
//
// GEOMETRY PROVENANCE (PIL-measured, scratch/slide012/measure_frame*.py):
//   frame 960x540 (1px = 1pt); container red border x[93.5,796.5] y[52.5,524.5]
//   (stroke ~2pt #C00000); mapping page300->frame: s_x=.28909 ox=97.13,
//   s_y=.28480 oy=-60.52 (least squares over 11 landmarks, max res 1.7px);
//   crop window page x[-13,2419] y[397,2054] (13px white pad left);
//   highlight frame rects: title x[336,599] y[54,84]; pink1 y[171,185]
//   x[261,333]/[388,459]/[496,583]/[610,698]; pink2 y[231,245]
//   x[255,343]/[574,645]; date band x[97.5,137] y[184,312].
//
// LAWS honored: playlist chrome via shared_patterns/house_chrome.js (never
// re-drawn); single-version deliverable; no '#' in hex; no multi-line text
// boxes (explicit lineSpacing n/a); no typed content (all text is in the
// certified source raster — verbatim by construction).

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js"
);

const ASSET = path.join(__dirname, "assets", "slide012_page1.png");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
pres.author = "AI LLM Slides";
pres.title = "Attention Is All You Need";

const slide = pres.addSlide();

// 1. Playlist house chrome (white canvas, gray E9E9E7 panel, red C00000 border,
//    badge d36 at (893,71) with numeral 12) — shared module, never re-drawn.
drawHouseChrome(pres, slide, { numeral: 12 });

// 2. The paper's page-1 raster cropped to the frame's visible window
//    (highlights pre-baked). Frame rect x[93.37,796.5] y[52.55,524.46] px.
slide.addImage({
  path: ASSET,
  x: 1.29683, y: 0.72980, w: 9.76482, h: 6.55436,
});

// 3. The container's thin red border (the course markup framing the screenshot):
//    rect x[93.5,796.5] y[52.5,524.5] px, ~2pt C00000, no fill.
slide.addShape(pres.ShapeType.rect, {
  x: 1.29861, y: 0.72917, w: 9.76389, h: 6.55556,
  fill: { color: "FFFFFF", transparency: 100 },
  line: { color: "C00000", width: 2 },
});

const OUT = path.join(__dirname, "..", "slide_012_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
