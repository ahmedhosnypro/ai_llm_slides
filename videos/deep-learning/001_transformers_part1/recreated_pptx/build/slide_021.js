// Slide 021 — "Word Embedding" (CBOW vs Skip-Gram definitions)
// Deep Learning DSAI 308, Transformers — Part I.
//
// Geometry: ALL values PIL-measured from unique_slides/slide_021.jpg (960x540 px,
// 1 px = 1 pt = 1/72 in). House chrome = playlist shared module (founder directive
// 2026-10-11, supersedes ml-intro values): white FFFFFF canvas, gray E9E9E7 panel
// x42..918 y45..540 with thin C00000 border, badge d36 at (893,71) FDFD96 fill /
// 6A5ACD ring, bold 333333 Arial numeral "21".
//
// Measured facts driving this build (frame px):
//   title ink   y77..109  x349..637  (center x493)  -> Arial bold 35pt CC0000
//   subtitle ink y115..139 x132..856 (center x494)  -> Arial bold 26.5pt CC0000,
//        three literal spaces between "(CBOW)" and "vs" (verbatim, validation fix)
//   blue box    x69..879 y170..471, white FFFFFF fill, 3333CC thin border
//   body lines (ink tops; pitch fit (425-201)/10 = 22.4pt exactly, pinned):
//     201  HDR1 "Continuous bag-of-words model:"        bold 19.5 CC0000 (ink w305)
//     224  P1L1  ...consists of a                       (ink w774)
//     246  P1L2  ...called a bag-of-                    (ink w783)  <- original wraps
//          the compound "bag-of-words" AT THE HYPHEN (PPT line-break opportunity);
//          hand-break reproduces the original's visible line breaks exactly.
//     269  P1L3  words model ... is not important.      (ink w575)
//     290.6 blank
//     313  HDR2 "Continuous skip-gram model:"            bold 19.5 CC0000 (ink w274)
//     336  P2L1  ...in the same                          (ink w727)
//     358  P2L2  sentence.                               (ink w83)
//     380.2 blank
//     403  P3L1  "a " + BLUE"bag-of-words model" + " ... a " + BLUE"skip-gram model"
//          (blue runs measured x96..270 and x709..854)   (ink w774)
//     425  P3L2  predicts the context ... itself.        (ink w580, NO blue — measured)
//   Body = Arial 20pt #000000 (Arial-metric advance fit: 20pt ink widths match all
//   7 body lines within +2..+5 px; 19pt was 25..55 px short). Headers Arial bold
//   19.5pt (measured ink widths 305/274 -> bold 19.5 predicts 306.5/276.2).
//   Box interior sampled WHITE (255,255,255) vs panel gray E9E9E7 -> solid white fill.
//   Mouse cursor over "not important" (~55%x, 52%y) = recording artifact: OMITTED
//   (spec layout region 6 + GROUND RULES (c)).
//
// pptxgenjs laws: no '#' in hex, fontFace everywhere, margin:0, explicit
// lineSpacing 22.4 on the multi-line body box, single-space spacer runs (never ""),
// writeFile({fileName}).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const IN = (px) => px / 72;              // 960x540 frame px -> inches

// palette (spec colors block; JPEG core samples reconcile)
const RED = "CC0000", BLUE = "3333CC", BLACK = "000000";
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();

// ---- 1) house chrome (panel + badge "21") -------------------------------------
drawHouseChrome(pres, s, { numeral: 21 });

// ---- 2) blue-bordered white body box x69..879 y170..471 ------------------------
s.addShape(pres.shapes.RECTANGLE, {
  x: IN(69), y: IN(170), w: IN(811), h: IN(302),
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 1.5 },
});

// ---- 3) body text block (11 pinned lines, pitch 22.4pt) ------------------------
// ink top of line 1 target y=201; ascent-in-line offset ~3.5px -> box y 197.5.
// Hand line breaks match the original frame's measured wraps (see header comment).
s.addText(
  [
    { text: "Continuous bag-of-words model:",
      options: { fontSize: 19.5, bold: true, color: RED, breakLine: true } },
    { text: "predicts the middle word based on surrounding context words. The context consists of a",
      options: { fontSize: 20, color: BLACK, breakLine: true } },
    { text: "few words before and after the current (middle) word. This architecture is called a bag-of-",
      options: { fontSize: 20, color: BLACK, breakLine: true } },
    { text: "words model as the order of words in the context is not important.",
      options: { fontSize: 20, color: BLACK, breakLine: true } },
    { text: " ", options: { fontSize: 20, color: BLACK, breakLine: true } },
    { text: "Continuous skip-gram model:",
      options: { fontSize: 19.5, bold: true, color: RED, breakLine: true } },
    { text: "predicts words within a certain range before and after the current word in the same",
      options: { fontSize: 20, color: BLACK, breakLine: true } },
    { text: "sentence.",
      options: { fontSize: 20, color: BLACK, breakLine: true } },
    { text: " ", options: { fontSize: 20, color: BLACK, breakLine: true } },
    { text: "a ", options: { fontSize: 20, color: BLACK } },
    { text: "bag-of-words model", options: { fontSize: 20, color: BLUE } },
    { text: " predicts a word given the neighboring context, a ", options: { fontSize: 20, color: BLACK } },
    { text: "skip-gram model", options: { fontSize: 20, color: BLUE, breakLine: true } },
    { text: "predicts the context (or neighbors) of a word, given the word itself.",
      options: { fontSize: 20, color: BLACK } },
  ],
  {
    x: IN(78), y: IN(197.5), w: IN(800), h: IN(260),
    align: "left", valign: "top", fontFace: FONT, fontSize: 20, color: BLACK,
    lineSpacing: 22.4, margin: 0,
  }
);

// ---- 4) title (ink x349..637 y77..109, center x493) -----------------------------
s.addText("Word Embedding", {
  x: IN(193), y: IN(59.8), w: IN(600), h: IN(60),
  align: "center", valign: "middle", fontSize: 35, bold: true,
  color: RED, fontFace: FONT, margin: 0,
});

// ---- 5) subtitle (ink x132..856 y115..139, center x494; THREE spaces before vs) --
s.addText("Continuous bag-of-words (CBOW)   vs Skip-Gram Models", {
  x: IN(114), y: IN(101.5), w: IN(760), h: IN(46),
  align: "center", valign: "middle", fontSize: 26.5, bold: true,
  color: RED, fontFace: FONT, margin: 0,
});

pres.writeFile({
  fileName:
    "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_021_recreated.pptx",
}).then(() => console.log("OK slide_021_recreated.pptx"));
