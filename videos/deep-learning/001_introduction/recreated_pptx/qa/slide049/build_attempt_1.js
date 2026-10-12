// slide_049.js — 001_introduction slide 49 "Convnets in practice" — Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_049.jpg (960x540, 1px = 1pt = 1/72 in).
//   Measurement passes: qa/slide049/measure_original{,2,3,4}_out.txt + font_forensics_out.txt (banked).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 49 (slide file number; 001_introduction
//   originals carry no printed numbers — ASSUMPTION PENDING FOUNDER VETO, see video AGENTS.md).
//   NOTE: this frame's own panel is x 52..907 (left border x58, washed) vs canonical 42..918 —
//   playlist law fixes the chrome to canonical values (slide_040 precedent, judge ground rule (a)).
//
// Measured constants (frame px):
//   title   "Convnets in practice" ink x 252..707 (center 479.5), cap-top 84, baseline ~116.5,
//           cap ~33px. Font: ARIAL BOLD 46.5pt — word-gap metric solve is self-consistent
//           (in@+227px->46.4pt, practice@+282->46.6, end@+455->46.5) and cap ratio fits
//           (0.716*46.5=33.3); Times Bold is inconsistent (51.0..53.4 spread) and cap-mismatched.
//           Color C00000 (deck red; modal B81020 is JPEG wash).
//   box     blue-bordered white box: stroke-center rect x 99.5..860.5, y 153.5..491.5,
//           fill FFFFFF, border 0000AA 2pt (measured darkest #201878 is chroma-washed;
//           0000AA = certified slide_002 sibling value for the same deck-style box).
//   body    8 text lines, TIMES (Liberation Serif) regular 25.8pt (band4 bold 25.9):
//           serif confirmed by ink-crop forensics + underline advance math:
//           band1 bold run "non-linearities" underline measured x463..621 (159px) vs Times
//           Bold 6.167em*25.8=159.1 (Arial Bold 162.7 = off); band4 underline measured 312px vs
//           Times Bold 12.11em*25.9=313.4 (Arial 313.6 close but start-x off by 2.4);
//           band1 underline START x: Times 463.3 (measured 463) vs Arial 460.7. Body color
//           00008B (spec; measured modal #100080 within wash range).
//   lines   baselines 176.5 / 216.5 / 245.5 / 284.5 / 325.3 / 360.5 / 395.5 / 431
//           (descender-bottom - 0.212em; band1/band4 cross-checked against their underline rows
//           219-220 / 328 at the PowerPoint 0.106em underline offset).
//           text-left: top-level 147.5, wrap line 140.7 (frame shows the wrap 7px LEFT of the
//           text margin — hanging-indent quirk of the original; frame is ground truth),
//           sub-bullets 220.5.
//   dots    BLACK round bullets d~6.75px: top-level cx 115 (cy 168/208/276/316),
//           sub-bullets cx 198.5 (cy 351.5/387/422).
//   wraps   bullet 2 wraps after "(The most" -> line 2 "popular one is the ReLU)" ("ReLU" red).
//   reds    "ReLU" (band2 x334..390) and "max pooling" (band3 x679..805) = C00000;
//           band4 whole line bold+underlined 990000 (spec; measured #770410 washed).
//   artifacts black bottom bar y519..539 x38..921 + mouse cursor (~893,427) are video-capture
//           artifacts — OMITTED per spec recreation_brief step 15 + judge ground rule (c).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_049_recreated.pptx";

// ---- palette (measured / spec) ----
const TITLE_RED = "C00000";
const BODY_BLUE = "00008B";
const DARK_RED = "990000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const BOX_BORDER = "0000AA";

const px = (v) => v / 72;

// ---- geometry (frame px) ----
const BOX = { x: px(99.5), y: px(153.5), w: px(761), h: px(338) };

// Body lines: single-line boxes at measured baselines.
// LO baseline model (validated slide_002/040): baseline = box_top + (box_h_px - lineSpacing)/2 + ascent*fontSize
//   box_h 0.6in = 43.2px; lineSpacing 30 -> top = baseline - (43.2-30)/2 - ascent*size
const BODY_SIZE = 25.8;          // Times/Liberation Serif regular
const BODY_SIZE_B = 25.9;        // bold lead-in line
const ASC_SERIF = 0.891;
const LS_BODY = 30;
const BODY_BOX_H_PX = 43.2;

const topFor = (baseline, size) => baseline - (BODY_BOX_H_PX - LS_BODY) / 2 - ASC_SERIF * size;

// [runs, baseline, boxX, size, bold-all]
const LINES = [
  {
    runs: [{ text: "Several convolutional layers ( 5 or more)", opts: {} }],
    baseline: 176.5, x: 147.5, w: 705, size: 26.1, // closed-loop: 25.8 rendered 5.3px short of orig w 427
  },
  {
    runs: [
      { text: "After the convolutional layers ", opts: {} },
      { text: "non-linearities", opts: { bold: true, underline: { style: "sng" } } },
      { text: " are added (The most", opts: {} },
    ],
    baseline: 216.5, x: 147.5, w: 710, size: BODY_SIZE,
  },
  {
    runs: [
      { text: "popular one is the ", opts: {} },
      { text: "ReLU", opts: { color: TITLE_RED } },
      { text: ")", opts: {} },
    ],
    baseline: 245.5, x: 140.7, w: 300, size: BODY_SIZE,
  },
  {
    runs: [
      { text: "After the ReLU usually some pooling ( Most often ", opts: {} },
      { text: "max pooling", opts: { color: TITLE_RED } },
      { text: ")", opts: {} },
    ],
    baseline: 284.5, x: 147.5, w: 700, size: BODY_SIZE,
  },
  {
    runs: [{ text: "After 5 rounds of cascading:", opts: { bold: true, underline: { style: "sng" }, color: DARK_RED } }],
    baseline: 325.3, x: 147.5, w: 340, size: BODY_SIZE_B,
  },
  {
    runs: [{ text: "Vectorize the last convolutional layer (Flatten)", opts: {} }],
    baseline: 360.5, x: 220.5, w: 640, size: BODY_SIZE,
  },
  {
    runs: [{ text: "Use as Input to the first fully connected layer (FC)", opts: {} }],
    baseline: 395.5, x: 220.5, w: 640, size: BODY_SIZE,
  },
  {
    runs: [{ text: "Proceed as in a traditional classification neural network", opts: {} }],
    baseline: 431, x: 220.5, w: 640, size: 26.05, // closed-loop: 25.8 rendered 5.1px short of orig w 575
  },
];

// Black round bullet dots (measured centers, d ~6.75px)
const DOTS = [
  { cx: 115, cy: 168 }, { cx: 115, cy: 208 }, { cx: 115, cy: 276 }, { cx: 115, cy: 316 },
  { cx: 198.5, cy: 351.5 }, { cx: 198.5, cy: 387 }, { cx: 198.5, cy: 422 },
];
const DOT_D = 6.75;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 49)
drawHouseChrome(pres, slide, { numeral: "49" });

// Blue-bordered white content box (stroke-center rect)
slide.addShape(pres.ShapeType.rect, {
  x: BOX.x, y: BOX.y, w: BOX.w, h: BOX.h,
  fill: { color: WHITE }, line: { color: BOX_BORDER, width: 2 },
});

// Bullet dots (black ellipses; original markers are black round dots, not text bullets)
for (const d of DOTS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(d.cx - DOT_D / 2), y: px(d.cy - DOT_D / 2), w: px(DOT_D), h: px(DOT_D),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
}

// Body lines — Times New Roman (Liberation Serif metric), single-line boxes at measured baselines
for (const L of LINES) {
  const runs = L.runs.map((r) => ({
    text: r.text,
    options: {
      fontFace: "Times New Roman",
      fontSize: L.size,
      color: r.opts.color || BODY_BLUE,
      bold: !!r.opts.bold,
      ...(r.opts.underline ? { underline: r.opts.underline } : {}),
    },
  }));
  slide.addText(runs, {
    x: px(L.x), y: px(topFor(L.baseline, L.size)), w: px(L.w), h: 0.6,
    align: "left", valign: "middle", margin: 0,
    lineSpacing: LS_BODY,
  });
}

// Title — Arial Bold 46.5pt C00000, ink center (479.5, baseline ~116.5)
slide.addText("Convnets in practice", {
  x: px(47.5), y: px(71.6), w: 12, h: 0.8,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 46.5, bold: true, color: TITLE_RED,
  lineSpacing: 52,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
