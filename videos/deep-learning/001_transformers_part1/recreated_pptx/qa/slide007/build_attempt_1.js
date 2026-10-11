// build/slide_007.js — slide 007 "Traditional RNN  Seq2Seq model / (Challenges) — [1] Bottleneck"
//
// DEPENDENCY-GATED CHILD BUILD (founder directive 2026-10-11; edge 7 <- 6):
// slide 7 = slide 6's judge-certified composition + delta. The base (chrome + 27 blocks)
// comes ENTIRELY from the certified component components/slide_006.js via renderBase() —
// never re-derived, never copy-pasted. This script draws ONLY slide 7's delta:
//   (a) title line 2 "(Challenges)" (bold blue, centered under line 1)
//   (b) light-blue "[1] Bottleneck" callout box (4 centered lines, underlined phrases)
//   (c) thin leader connector from the callout to the red context-vector arc
// Verified pure superset (scratch/slide007/diff_006_007.py): nothing inherited is
// removed/moved/resized; the only non-delta diffs are badge numeral 6->7 (chrome)
// and <=7px video-capture jitter of the identical title string.
//
// DELTA GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_007.jpg (960x540,
// 1px=1pt, in=px/72) — scratch/slide007/measure_*.py (5 passes: frame diff, box outline
// scanline, text bands, underline runs, connector trace).
//
// LAWS honored: playlist chrome via component (numeral 7 = printed number on the frame);
// verbatim text incl. double spaces ("sequence  is", "captured  by", "fixed
// dimensionality", title's "RNN  Seq2Seq" from the component); mouse-cursor artifact
// (white arrow over box right-center, measured at x365..372 y243..248) OMITTED; margin:0 +
// explicit fontFace everywhere; explicit lineSpacing 18pt (measured pitch 18px) on the
// multi-line callout; no '#' in hex; single-version deliverable (no suffixes).

const path = require("path");
const pptxgen = require("pptxgenjs");
const parent = require(path.join(__dirname, "components", "slide_006.js"));

const px = parent.px; // frame px -> inches (v/72); 1 frame px = 1 pt

// ---- delta palette (JPEG-core measured from slide_007.jpg) -------------------
const D = {
  blue: "000066",     // subtitle + callout text ink (darkest modes (0,0,89..110))
  boxFill: "DFFFFC",  // callout fill mode (223,255,252)
  boxEdge: "ABB8CB",  // callout border mean ~(171,184,203)
  leader: "A8AABC",   // connector stroke samples ~(167..180, 166..180, 182..196)
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) certified parent composition (chrome incl. badge numeral 7) ----------
parent.renderBase(pres, slide, { numeral: 7 });

// ---- 2) DELTA (a): title line 2 "(Challenges)" --------------------------------
// measured ink x376..533 (center 454.5 ~= title-box center), y87..111 (paren span
// 24 frame px). Calibrated against the LO render (clean-window measurement): 20pt
// gives 245 render px wide / 38 tall -> linear scale to the 329px/50px targets
// => 27pt (matches BOTH ink width and paren-span height).
slide.addText("(Challenges)", {
  x: px(252.5), y: px(81), w: px(400), h: px(30),
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 27, bold: true, color: D.blue,
});

// ---- 2) DELTA (b): bottleneck callout box --------------------------------------
// box outer bbox x44..455 y170..267 (fill rows to y267); corners measured ~1-2px
// (near-square roundRect); fill mode (223,255,252); 1px border ~(171,184,203).
slide.addShape(pres.ShapeType.roundRect, {
  x: px(44), y: px(170), w: px(412), h: px(98), rectRadius: 0.03,
  fill: { color: D.boxFill }, line: { color: D.boxEdge, width: 1 },
});

// 4 centered lines, verbatim incl. double spaces; underlines measured:
//   L1 whole line (y199..200 x191..308); L2 none; L3 phrase "by a single context
//   vector" (y235 x270..442); L4 phrase "fixed  dimensionality" (y252..253 x190..344).
// Line pitch measured 18px -> lineSpacing 18pt. Per-line sizes calibrated against the
// LO render ink widths (frame-scale targets L1 116 / L2 326 / L3 379 / L4 190):
// the frame draws L1 ~13% larger than L2-L4 (per-char 8.3 vs 7.1 px) -> L1 17.5pt,
// L2-L4 15.5pt (render-measured ratios 1.26x / 1.11x on the 14pt first pass).
slide.addText(
  [
    { text: "[1] Bottleneck", options: { fontSize: 17.5, underline: { style: "sng" }, breakLine: true } },
    { text: "The meaning of the entire input sequence  is", options: { fontSize: 15.5, breakLine: true } },
    { text: "Expected to be captured  ", options: { fontSize: 15.5 } },
    { text: "by a single context vector", options: { fontSize: 15.5, underline: { style: "sng" }, breakLine: true } },
    { text: "with ", options: { fontSize: 15.5 } },
    { text: "fixed  dimensionality", options: { fontSize: 15.5, underline: { style: "sng" } } },
  ],
  {
    x: px(44), y: px(170), w: px(412), h: px(98),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", bold: true, color: D.blue,
    fontSize: 15.5,
    lineSpacing: 18,
  }
);

// ---- 2) DELTA (c): leader connector callout -> context-vector arc ---------------
// traced (463,188) -> (477,279): 1px stroke, top end floats ~7px right of the box
// border (measured), lower end meets the red ctx arc ink at (477,279).
slide.addShape(pres.ShapeType.line, {
  x: px(463), y: px(188), w: px(14), h: px(91),
  line: { color: D.leader, width: 1 },
});

// ---- output (SINGLE-VERSION law: one plain-named deliverable) -------------------
const OUT = path.join(__dirname, "..", "slide_007_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
