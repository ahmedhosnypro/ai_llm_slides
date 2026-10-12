// slide_047.js — 001_introduction slide 47 "AVERAGE POOLING Layer (Take Average Value)"
// (Deep Learning DSAI 308). Fresh build 2026-10-12 from PIL forensics of the ground-truth
// frame videos/deep-learning/001_introduction/unique_slides/slide_047.jpg (960x540, 1px=1pt).
//
// Forensics: qa/slide047/measure_original1..5.py (+ _out.txt), vision reads
// qa/slide047/probe_crop.txt (intro lines), read_eq_labels.txt (bullets 3-4),
// read_legend_grids.txt (legend + grids). NOTE: the dispatch's "POOLING" description
// actually matches slide 046; slide_047.jpg + the PASSED spec + SOURCES.md are all
// "AVERAGE POOLING Layer" — the spec/frame/SOURCES triple is authoritative.
//
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/
// house_chrome.js — imported, NEVER re-drawn. Badge numeral 47 (file number; this
// lecture's frames carry no printed numbers — PENDING FOUNDER VETO, 001 AGENTS.md).
//
// MEASURED SPEC (frame px, 1px = 1pt):
//   lecturer L-frame (deck's own marks, drawn as measured):
//     top hairline y=43, x 58..901 (1px dark red [106,46,54] -> C00000 @0.75pt)
//     left line    x=58 (2px), y 45..513 (C00000 @1.5pt)
//   black bottom bar y 519..538, x 38..921 — DRAWN per certified siblings 005/031
//     (both drew it and PASSED; chrome bottom stroke rows 538-539 kept visible)
//   content box  x 82..875, y 219..487; border 2px red -> C00000 1.5pt, white fill,
//     PLAIN rect (square corners measured; matches certified 005/031 boxes)
//   title        red caps 72..92 (cap 21px -> Arial Bold 29.3); blue 'Layer' cap
//     67..92 (26px -> 36.3). Arial Bold (deck-certified typeface: 002/005/031), red
//     C00000 / blue 0000CC (core [8,0,198]). ink x 140..825 (w 686), center 482.5,
//     baseline 92.5
//   intro lines  TNR Bold Italic 20 (L3 advance 643px/77ch fits 20pt), left 81,
//     baselines 145 / 171.5 / 198.5; colors 000080 / C00000 / 000080 (intro3 core
//     [26,16,112]). Line 2 kept as VERBATIM TEXT (original renders it as typed prose;
//     the two true equations + the 1/2 fraction get the 2D mathtext upgrade)
//   bullets      rings d~10 at (96, 233.5) (96, 264) (96, 299) (96, 338.5), pale tan
//     [212,190,166] -> D4BEA6 1.25pt (JPEG-desaturated ring; spec orange E36C0A
//     overruled by pixels per deck pixel law)
//   bullet 1     'Run a sliding window of size [h_f , w_f ]' Arial 17.5 333333
//     (uniform-stroke glyphs, no serifs at 11px cap; 005 precedent), left 116,
//     baseline 238.5, ink target x 116..475
//   bullet 2     'At each location keep the average value' ('average' bold+underlined,
//     underline row 268), left 116, baseline 267.5, ink target x 116..529
//   label boxes  x 109..311, y 287..313 / 323..351; border navy 000080 1.5pt (core
//     [13,4,119]); text DARK GRAY 333333 Arial (pixels: core [69,70,72] — the spec's
//     "blue text" claim overruled by pixels; vision read: dark sans-serif)
//   eq3          a_{r,c} = 1/(r.c) SUM_{i,j in Omega(r,c)} x_{ij} — original already 2D
//     (stacked fraction bar y 297-299 x 376..400, Sigma with SIDE subscript). mathtext
//     18pt #333333 with side-limits sum; ink left 317, bar y 298
//   eq4         d a_{r,c}/d x_{ij} = 1/(r.c) — original fully 2D (bars y 336-337 at
//     x 319..357 and x 392..415). mathtext 16pt #333333; ink left 320, bar y 337
//   legend box   x 455..566, y 348..475; fill pale cyan (modal [233,252,252]) ->
//     E4FAFF; border PERIWINKLE 9999CC 1pt (modal [150,160,185] == certified slide-031
//     box border; the spec's "red border" claim overruled by pixels — all four border
//     samples are blue-dominant). 'Where:' red C00000 bold italic; rows all navy
//     000080 bold italic (red scan finds NO red in the rows); letters col x 465,
//     words col x 494; baselines 388/407.3/426.6/445.9/465.2; 'Column' w 53 -> 16.5pt
//   input grid   x 571..726, y 365..483; col bounds [571,609.5,649,688.5,727], row
//     bounds [365,394.5,424.5,454,484]; cells 16, thin dark separators -> 0.5pt black
//     outlines (olive blend dips between fills). fills (modals): green 0DCA54
//     [13,202,84], yellow FFFF00 [251,255,10], red E80000 [232,0,0], cyan 0EC0EC
//     [14,192,236]. values 1,4,1,6/2,3,0,9/1,2,7,1/4,1,0,2; numerals TNR Bold 20
//     (digit h 13px, serif '1' flag+base measured)
//   arrow        '=>' TEXT glyph (thin double shafts + open head, ink x 738..757,
//     y 422..431) — the earlier "arrow to x 788" bbox was JPEG halo of the red
//     fraction. TNR ~25pt black
//   fraction     red 1/2: numerator '1' x 779..786 y 405..420, bar x 776..790 y
//     426..428, '2' x 775..790 y 433..449 (stack 45px). mathtext \dfrac{1}{2} 19.5pt
//     #C00000; ink left 775, bar y 427
//   output grid  x 796..871, y 396..453; col bounds [796,833,872], row bounds
//     [396,424.5,454]; values 5,8,4,5 (green/yellow/red/cyan); numerals TNR Bold 20
//   NOT drawn: nothing else; the video-player bottom bar IS drawn (see above).
//
// Equations: matplotlib mathtext -> 600dpi transparent PNG -> addImage EXACT size
// (w = px/600), bar-row anchored (sidecars + PIL bar rows in gen_assets2.py log).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

// ---- palette (measured) ----
const RED = "C00000";
const NAVY = "000080";
const TITLE_BLUE = "0000CC";
const GRAY = "333333";
const PERIWINKLE = "9999CC";
const LEGEND_FILL = "E4FAFF";
const TAN = "D4BEA6";
const BLACK = "000000";
const WHITE = "FFFFFF";
const GREEN = "0DCA54";
const YELLOW = "FFFF00";
const REDFILL = "E80000";
const CYAN = "0EC0EC";

const SERIF = "Times New Roman";
const SANS = "Arial";

const px = (v) => v / 72;
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

// LO single-line baseline calibration (certified 031 model):
// top = baseline - (H - L)/2 - K*fs ; K_TNR=0.955, K_ARIAL=0.905
function lineTop(baselinePx, fs, Hpx, Lpt, K) {
  const k = K !== undefined ? K : 0.955;
  return baselinePx - (Hpx - Lpt) / 2 - k * fs;
}

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "47") ----
drawHouseChrome(pres, slide, { numeral: "47" });

// ---- 2) lecturer L-frame marks (measured) ----
// left red line x=58 (2px), y 45..513
slide.addShape(pres.ShapeType.line, {
  x: px(58.5), y: px(44), w: 0, h: px(469),
  line: { color: RED, width: 1.5 },
});
// top hairline y=43, x 58..901 (1px)
slide.addShape(pres.ShapeType.line, {
  x: px(58), y: px(43.5), w: px(843), h: 0,
  line: { color: RED, width: 0.75 },
});

// ---- 3) black bottom bar (certified 005/031 pattern; chrome bottom stroke visible) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// ---- 4) content box (white, red border) x82..875 y219..487, square corners ----
slide.addShape(pres.ShapeType.rect, {
  x: px(82), y: px(219), w: px(794), h: px(268),
  fill: { color: WHITE }, line: { color: RED, width: 1.5 },
});

// ---- 5) title — Arial Bold 29.5 (red) + 36 'Layer' (blue) + 29.5 (red) ----
// ink x 140..825 (center 482.5), baseline 92.5. Box h 0.667in (48px), lineSpacing 42.
slide.addText(
  [
    { text: "AVERAGE POOLING", options: { color: RED, fontSize: 30.5 } },
    { text: " Layer", options: { color: TITLE_BLUE, fontSize: 39 } },
    { text: " (Take Average Value)", options: { color: RED, fontSize: 30.5 } },
  ],
  {
    x: px(482.5) - 6, y: px(lineTop(92.5, 39, 48, 44, 0.955)), w: 12, h: 0.667,
    align: "center", valign: "middle", margin: 0,
    fontFace: SERIF, bold: true, color: RED,
    lineSpacing: 44,
  }
);

// ---- 6) intro lines — TNR Bold Italic 20, left 81, baselines 145/171.5/198.5 ----
const INTRO = [
  { text: "It is a new Module (Average-POOLING module)", base: 145, color: NAVY },
  { text: "Output = 1/r c * Summation (each_input_pixel * 1)", base: 171.5, color: RED },
  { text: "Required to define its input, its output, and Gradient of Output w.r.t input", base: 198.5, color: NAVY },
];
for (const L of INTRO) {
  slide.addText(L.text, {
    x: px(81), y: px(lineTop(L.base, 21, 28.8, 24, 0.955)), w: px(740), h: 0.4,
    align: "left", valign: "middle", margin: 0,
    fontFace: SERIF, fontSize: 21, bold: true, italic: true, color: L.color,
    lineSpacing: 24,
  });
}

// ---- 7) bullet rings — 4 pale-tan open circles d10 ----
for (const cy of [233.5, 264, 299, 338.5]) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(96 - 5), y: px(cy - 5), w: px(10), h: px(10),
    fill: { color: WHITE }, line: { color: TAN, width: 1.25 },
  });
}

// ---- 8) bullet 1 — 'Run a sliding window of size [h_f , w_f ]' ----
slide.addText(
  [
    { text: "Run a sliding window of size [h", options: {} },
    { text: "f", options: { subscript: true } },
    { text: " , w", options: {} },
    { text: "f", options: { subscript: true } },
    { text: " ]", options: {} },
  ],
  {
    x: px(116), y: px(lineTop(238.5, 19, 25.2, 20, 0.905) + 3.2), w: px(420), h: 0.35,
    align: "left", valign: "middle", margin: 0, charSpacing: 1.5,
    fontFace: SANS, fontSize: 19, color: GRAY,
    lineSpacing: 20,
  }
);

// ---- 9) bullet 2 — 'At each location keep the average value' ----
slide.addText(
  [
    { text: "At each location keep the ", options: {} },
    { text: "average", options: { bold: true, underline: { style: "sng" } } },
    { text: " value", options: {} },
  ],
  {
    x: px(116), y: px(lineTop(267.5, 19, 25.2, 20, 0.905) + 3.2), w: px(460), h: 0.35,
    align: "left", valign: "middle", margin: 0, charSpacing: 1.9,
    fontFace: SANS, fontSize: 19, color: GRAY,
    lineSpacing: 20,
  }
);

// ---- 10) label box 1 + text ----
slide.addShape(pres.ShapeType.rect, {
  x: px(109), y: px(287), w: px(203), h: px(27),
  fill: { color: WHITE }, line: { color: NAVY, width: 1.5 },
});
slide.addText("Activation function:", {
  x: px(109), y: px(287 - 3), w: px(203), h: px(27),
  align: "center", valign: "middle", margin: 0, charSpacing: 2.0,
  fontFace: SANS, fontSize: 18.5, color: GRAY,
});

// ---- 11) eq3 — mathtext PNG, ink left 317, fraction bar y 298 ----
// eq_047_act.png 1668x352 @600dpi (200.2x42.2pt), bar row 196; x = 317/72 - 8/600
slide.addImage({
  path: ASSETS + "/eq_047_act.png",
  x: 4.38944, y: 3.81222, w: 1668 / 600, h: 352 / 600,
});

// ---- 12) label box 2 + text ----
slide.addShape(pres.ShapeType.rect, {
  x: px(109), y: px(323), w: px(203), h: px(29),
  fill: { color: WHITE }, line: { color: NAVY, width: 1.5 },
});
slide.addText("Gradient w.r.t. input", {
  x: px(109), y: px(323 - 3), w: px(203), h: px(29),
  align: "center", valign: "middle", margin: 0, charSpacing: 2.0,
  fontFace: SANS, fontSize: 18.5, color: GRAY,
});

// ---- 13) eq4 — mathtext PNG, ink left 320, bar y 337 ----
// eq_047_grad.png 753x352 @600dpi (90.4x42.2pt), bar row 170
slide.addImage({
  path: ASSETS + "/eq_047_grad.png",
  x: 4.43111, y: 4.39722, w: 753 / 600, h: 352 / 600,
});

// ---- 14) legend box + text ----
slide.addShape(pres.ShapeType.rect, {
  x: px(455), y: px(348), w: px(112), h: px(128),
  fill: { color: LEGEND_FILL }, line: { color: PERIWINKLE, width: 1 },
});
slide.addText("Where:", {
  x: px(465), y: px(lineTop(368, 16.5, 24, 19, 0.955)), w: px(70), h: 24 / 72,
  align: "left", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: 16.5, bold: true, italic: true, color: RED,
  lineSpacing: 19,
});
const LEG_ROWS = [
  { letter: "r", word: "Row", base: 388 },
  { letter: "c", word: "Column", base: 407.3 },
  { letter: "f", word: "filter", base: 426.6 },
  { letter: "h", word: "Height", base: 445.9 },
  { letter: "w", word: "width", base: 465.2 },
];
for (const R of LEG_ROWS) {
  slide.addText(R.letter, {
    x: px(465), y: px(lineTop(R.base, 16.5, 24, 19, 0.955)), w: px(20), h: 24 / 72,
    align: "left", valign: "middle", margin: 0,
    fontFace: SERIF, fontSize: 16.5, bold: true, italic: true, color: NAVY,
    lineSpacing: 19,
  });
  slide.addText(R.word, {
    x: px(494), y: px(lineTop(R.base, 16.5, 24, 19, 0.955)), w: px(70), h: 24 / 72,
    align: "left", valign: "middle", margin: 0,
    fontFace: SERIF, fontSize: 16.5, bold: true, italic: true, color: NAVY,
    lineSpacing: 19,
  });
}

// ---- 15) input grid — 16 cells, thin dark outlines, TNR Bold 20 numerals ----
const GCOLS = [571, 609.5, 649, 688.5, 727];
const GROWS = [365, 394, 424.5, 454, 483.5];
const GVALS = [
  [{ v: "1", f: GREEN }, { v: "4", f: GREEN }, { v: "1", f: YELLOW }, { v: "6", f: YELLOW }],
  [{ v: "2", f: GREEN }, { v: "3", f: GREEN }, { v: "0", f: YELLOW }, { v: "9", f: YELLOW }],
  [{ v: "1", f: REDFILL }, { v: "2", f: REDFILL }, { v: "7", f: CYAN }, { v: "1", f: CYAN }],
  [{ v: "4", f: REDFILL }, { v: "1", f: REDFILL }, { v: "0", f: CYAN }, { v: "2", f: CYAN }],
];
for (let r = 0; r < 4; r++) {
  for (let c = 0; c < 4; c++) {
    const cell = GVALS[r][c];
    const cx0 = GCOLS[c], cy0 = GROWS[r];
    const cw = GCOLS[c + 1] - GCOLS[c], ch = GROWS[r + 1] - GROWS[r];
    slide.addShape(pres.ShapeType.rect, {
      x: px(cx0), y: px(cy0), w: px(cw), h: px(ch),
      fill: { color: cell.f }, line: { color: BLACK, width: 0.5 },
    });
    slide.addText(cell.v, {
      x: px(cx0), y: px(cy0), w: px(cw), h: px(ch),
      align: "center", valign: "middle", margin: 0,
      fontFace: SERIF, fontSize: 20, bold: true, color: BLACK,
    });
  }
}

// ---- 16) arrow '⇒' — TNR ~25pt black, ink center (748, 426.5) ----
slide.addText("\u21D2", {
  x: px(748 - 15), y: px(426.5 - 12), w: px(30), h: px(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: SERIF, fontSize: 25, bold: true, color: BLACK,
});

// ---- 17) red fraction 1/2 — mathtext PNG, ink left 775, bar y 427 ----
// eq_047_half.png 119x379 @600dpi (14.3x45.5pt), bar row 203
slide.addImage({
  path: ASSETS + "/eq_047_half.png",
  x: 10.75056, y: 5.59222, w: 119 / 600, h: 379 / 600,
});

// ---- 18) output grid — 4 cells + numerals ----
const OCOLS = [796, 833, 872];
const OROWS = [396, 424.5, 453.5];
const OVALS = [
  [{ v: "5", f: GREEN }, { v: "8", f: YELLOW }],
  [{ v: "4", f: REDFILL }, { v: "5", f: CYAN }],
];
for (let r = 0; r < 2; r++) {
  for (let c = 0; c < 2; c++) {
    const cell = OVALS[r][c];
    const cx0 = OCOLS[c], cy0 = OROWS[r];
    const cw = OCOLS[c + 1] - OCOLS[c], ch = OROWS[r + 1] - OROWS[r];
    slide.addShape(pres.ShapeType.rect, {
      x: px(cx0), y: px(cy0), w: px(cw), h: px(ch),
      fill: { color: cell.f }, line: { color: BLACK, width: 0.5 },
    });
    slide.addText(cell.v, {
      x: px(cx0), y: px(cy0), w: px(cw), h: px(ch),
      align: "center", valign: "middle", margin: 0,
      fontFace: SERIF, fontSize: 20, bold: true, color: BLACK,
    });
  }
}

// ---- write ----
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_047_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE " + OUT));
