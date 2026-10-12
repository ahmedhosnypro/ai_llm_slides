// build/slide_042.js — slide 042 "Multi-Head Self Attention" (Deep Learning DSAI 308,
// 001_transformers_part1). Root slide (no dependents — 15_progress deps; nothing in any
// video's graph references 42).
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_042.jpg (960x540, 1px=1pt,
// in = px/72) — scratch/slide042/measure.py + measure2.py scanline runs and color medians,
// cross-read with 2 banked pre-build vision-crop transcripts (qa/slide042/origcrop_*.txt):
//   - line 2 math runs: each group is bold blue W -> RED superscript r FIRST -> GREEN
//     subscript q/k/v SECOND (vision-confirmed staggered order, NOT the spec's linear
//     "Wq^r" reading); W blue bold; commas/period base blue.
//   - line 1: curly quotes are BLUE (body color); only the r is bold red, full-size.
//
// LAWS honored: playlist chrome via shared module (numeral = printed 42); verbatim text
// (spaces before commas, double space in subtitle, "Each Head"/"Each head"/"All Output"
// capitalization); true sub/superscript runs (professional 2D — no caret/underscore text);
// margin:0 + fontFace everywhere; no '#' hex; explicit lineSpacing on multi-line boxes;
// mouse-cursor artifact omitted (recording overlay, excluded by spec).

const path = require("path");
const { drawHouseChrome } = require(path.join(
  "/home/ahmed/Projects/ai_llm_slides",
  "videos/deep-learning/shared_patterns/house_chrome.js"
));

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_042_recreated.pptx";

// ---- palette (spec colors; JPEG cores consistent) -----------------------------
const RED = "C00000";      // title, subtitle, red math (X, Y, r)
const BLUE = "0000CC";     // body text, bold-blue "linear transformation", blue quotes
const GREEN = "00A000";    // green subscripts q, k, v
const BOXBORDER = "990000";// content box border
const BOXFILL = "E9E9E7";  // content box fill = panel gray (chrome panel E9E9E7)
const SANS = "Arial";

const px = (v) => v / 72;

// ---- text helper --------------------------------------------------------------
function text(slide, str, o) {
  slide.addText(str, Object.assign({ fontFace: SANS, margin: 0 }, o));
}

// W math group: bold blue W -> red superscript r -> green subscript letter
// (order vision-certified from the original frame, qa/slide042/origcrop_line2.txt).
// Run size = base 24: LibreOffice's automatic escapement renders baseline-shifted
// runs at 58% -> 13.9pt glyphs, matching the original's measured ~14pt sub/sup
// (closed-loop render_1: 16pt runs rendered ~9.3pt — too small). Superscript raise
// is corrected to 43% by build/slide_042_postpass.py (LO 30% default sat ~3px low).
function wGroup(letter) {
  return [
    { text: "W", options: { bold: true, color: BLUE } },
    { text: "r", options: { color: RED, superscript: true, fontSize: 24 } },
    { text: letter, options: { color: GREEN, subscript: true, fontSize: 24 } },
  ];
}

// ---- blocks ---------------------------------------------------------------------

// Title: ink x 299..663 (center 481), y 81..103 -> box center (481, 92); 31pt bold red
// (closed-loop render_1: 30pt gave ink w 351 vs original 365 -> 31pt)
function drawTitle(pptx, slide) {
  text(slide, "Multi-Head Self Attention", {
    x: px(72), y: px(72), w: px(818), h: px(40),
    align: "center", valign: "middle", bold: true, fontSize: 31, color: RED,
  });
}

// Subtitle: two centered lines, ink centers x=470; line1 top 151, line2 top 174
// (pitch 22.5px -> explicit lineSpacing 22.5); 20pt bold red; double space preserved
function drawSubtitle(pptx, slide) {
  text(slide, [
    {
      text: "Combining several self attention mechanisms  give the self attention greater",
      options: { breakLine: true },
    },
    { text: "power of discrimination", options: {} },
  ], {
    x: px(60), y: px(148.5), w: px(820), h: px(50),
    align: "center", valign: "top", bold: true, fontSize: 20, color: RED,
    lineSpacing: 22.5,
  });
}

// Content box: border cols 71-73 / 878-880, rows 195-198 / 481-484
// -> x 72, y 196, w 808, h 287; 2pt #990000 border, fill = panel gray
function drawContentBox(pptx, slide) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(72), y: px(196), w: px(808), h: px(287),
    fill: { color: BOXFILL }, line: { color: BOXBORDER, width: 2 },
  });
}

// Body lines: left edge x=82-83; ink tops L1 234, L2 286, L3 346, L4 398 (+wrap 428);
// 24.5pt regular blue (closed-loop render_1: 24pt ran ~2% narrow — "matrices" ended
// 419 vs original 425; 24.5 scales every line's ink to <=7px of the original);
// y values = ink_top - first-line offset (calibrated on render_1)
function drawBody(pptx, slide) {
  const X = px(82), W = px(760);

  // L1 — quotes blue, r bold red full-size (vision-certified, origcrop_line1.txt)
  text(slide, [
    { text: "Each Head is indexed with \u201C", options: { color: BLUE } },
    { text: "r", options: { bold: true, color: RED } },
    { text: "\u201D", options: { color: BLUE } },
  ], { x: X, y: px(227.5), w: W, h: px(34), align: "left", valign: "top", fontSize: 24.5 });

  // L2 — W^r_q groups: bold blue W, red sup r, green sub q/k/v; verbatim spacing
  // (" ," / " ,W" / " ."); separator 1 widened to two-space "  ,  " per the original's
  // measured ~30px q-end -> next-W gap (render_1 single-space ran 22.5 vs 30)
  text(slide, [
    { text: "Each head has its own matrices ", options: { color: BLUE } },
    ...wGroup("q"),
    { text: "  ,  ", options: { color: BLUE } },
    ...wGroup("k"),
    { text: " ,", options: { color: BLUE } },
    ...wGroup("v"),
    { text: " .", options: { color: BLUE } },
  ], { x: X, y: px(279), w: W, h: px(34), align: "left", valign: "top", fontSize: 24.5 });

  // L3 — bold red X, bold red Y with red superscript r
  text(slide, [
    { text: "For input ", options: { color: BLUE } },
    { text: "X", options: { bold: true, color: RED } },
    { text: " each attention head produces a different output vector ", options: { color: BLUE } },
    { text: "Y", options: { bold: true, color: RED } },
    { text: "r", options: { color: RED, superscript: true, fontSize: 24 } },
    { text: ".", options: { color: BLUE } },
  ], { x: X, y: px(340), w: W, h: px(34), align: "left", valign: "top", fontSize: 24.5 });

  // L4 — wraps after "linear" (measured L4a x82..770 / L4b x82..849); wrap pitch 30px
  // -> explicit lineSpacing 30 (render_1 verified pitch 30.2); "linear transformation"
  // bold blue; "original X dimension." bold (pixel-verified: both words run +8px vs
  // regular in render_1 while the six surrounding words match within 1px — the exact
  // Arial-bold delta; the instructor emphasized the whole phrase); final X bold red;
  // verbatim "concatenated ,"
  text(slide, [
    {
      text: "All Output vectors are concatenated , and pass through a ",
      options: { color: BLUE, breakLine: false },
    },
    { text: "linear", options: { bold: true, color: BLUE, breakLine: true } },
    { text: "transformation", options: { bold: true, color: BLUE } },
    { text: " to reduce the dimension back to ", options: { color: BLUE } },
    { text: "original ", options: { bold: true, color: BLUE } },
    { text: "X", options: { bold: true, color: RED } },
    { text: " dimension.", options: { bold: true, color: BLUE } },
  ], {
    x: X, y: px(391), w: px(800), h: px(64), align: "left", valign: "top",
    fontSize: 24.5, lineSpacing: 30,
  });
}

// ---- composition ----------------------------------------------------------------

const pptx = new (require("pptxgenjs"))();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: 42 });
drawTitle(pptx, slide);
drawSubtitle(pptx, slide);
drawContentBox(pptx, slide);
drawBody(pptx, slide);

pptx.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
});
