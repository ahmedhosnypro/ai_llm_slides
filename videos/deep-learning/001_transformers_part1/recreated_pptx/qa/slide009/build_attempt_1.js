// build/slide_009.js — slide 009 "Traditional RNN  Seq2Seq model / (Challenges) —
// [3] Very Long Sequence / Vanishing Gradient"
//
// DEPENDENCY-GATED CHILD BUILD (founder directive 2026-10-11; edge 9 <- 6, REMOVE/REPLACE delta):
// slide 9 = slide 6's judge-certified composition + delta. The base comes from the certified
// component components/slide_006.js — NEVER re-derived or copy-pasted. Measured delta
// (scratch/slide009/measure*.py, 11 PIL passes on unique_slides/slide_009.jpg):
//   (1) The ENTIRE decoder+encoder diagram (all dec_*/enc_* blocks + ctx_arc) is RIGID-SHIFTED
//       by (+9,+2) frame px — template-matched per block (27/27 matched (9,2), low SSD).
//       Implemented by rendering the parent's block functions through a coordinate-shifting
//       slide PROXY — the certified drawing code itself does the drawing (single source of
//       truth), my frame's measured shift applied as a transform. NO geometry re-derived.
//   (2) dec_caption ("Decoder (RNN)") and enc_caption ("Encoder (RNN)") are UNSHIFTED
//       (template match (0,0), ssd 2.0-4.8 — pixel-identical). Title L1 unchanged (<=7px
//       video jitter of the identical string — slide-007 precedent).
//   (3) REMOVED: parent blocks "callout" (pink Context Vector label) and "leader" — verified
//       absent (region now backprop-panel fill; no pink F6DCDD, no red diagonal line).
//   (4) NO blue connector curve exists (spec's connector (1) is a vision hallucination):
//       whole-slide bluish scan finds only subtitle + callout + summary-box inks. Not drawn.
//   (5) ADDED: subtitle "(Challenges)" (BLUE #00007B per frame — spec's "red" is wrong);
//       blue callout box "[3] Very Long Sequence / Vanishing Gradient" (both underlined);
//       gray summary box (3 color-coded lines); full Back-Propagation panel.
//
// BACKPROP PANEL — frame-verified structure (resolves the spec's [?] flags):
//   * 11 nabla squares (NOT ~12): cream #F9E8D6, thin dusty-red border, y373..394, w~24.5,
//     aligned 1:1 with the 11 green boxes; nabla glyph size GROWS left->right (w4->w14).
//   * 10 pink chain rects (NOT 11): centered BETWEEN the 11 arrows (chain links), joined by
//     a thin dark-red line y415.
//   * 11 green x0..x10 boxes y463..483 (fill #ECFFF0, border #7AA87A), 11 green up-arrows
//     y419..462 at the green-box centers, dark-green bold labels with true subscripts.
//   * Panel rect x502..918 y314..498, fill #EAE6DD (warm gray — spec's "white" is wrong),
//     thin blue-gray border; red over-brace PNG (assets/brace009.png, matplotlib 600dpi);
//     "Back Propagation" 15.5pt bold italic #CC0000; long LEFT-pointing red arrow
//     (shaft y357.5, wedge head tip x520, filled dot d15 at x888..903), all #CC0000
//     (dot solid-read (194,0,0..205,0,15) anchors the red).
//
// LAWS honored: playlist chrome via components/house_chrome.js (numeral 9 = printed number);
// verbatim text incl. double spaces; margin:0 + explicit fontFace everywhere; explicit
// lineSpacing on every multi-line box; no '#' in hex; single-version deliverable.

const path = require("path");
const pptxgen = require("pptxgenjs");
const parent = require(path.join(__dirname, "components", "slide_006.js"));
const { drawHouseChrome } = require(path.join(__dirname, "components", "house_chrome.js"));

const px = parent.px; // frame px -> inches (v/72); 1 frame px = 1 pt
const ASSETS = path.join(__dirname, "assets");

// ---- delta palette (frame-measured) ------------------------------------------
const D = {
  blue: "00007B",      // subtitle ink (0,0,117..129)
  navy: "000062",      // callout + summary lead-in ink (0,0,92..113)
  calloutFill: "CCE4F7",
  calloutEdge: "9DB2CF",
  grayFill: "D9D9D9",  // summary box (217,217,217)
  green: "1E8212",     // summary keywords (20,135,18)
  failRed: "CC0000",
  panelFill: "EAE6DD", // backprop panel (234,230,221)
  panelEdge: "A6ABC0", // panel border (top core (151,155,180), sides (192,193,195))
  red: "CC0000",       // brace/arrow/dot/text (dot solid-read (194..205,0,0..15))
  sqFill: "F9E8D6",    // nabla squares (249,232,214)
  sqEdge: "BE9D96",    // square borders (190,157,150)
  nabla: "000000",
  pinkFill: "F7CCE0",  // pink chain rects
  chainLine: "721A1D", // joining line (114,25,29)
  gArrow: "7AA87A",    // up-arrows
  gFill: "ECFFF0",     // green boxes (236,255,240)
  gEdge: "7AA87A",
  gLabel: "106C3B",    // x-label ink (16,108,59)
};
const SANS = "Arial";

// ---- coordinate-shifting proxy: render parent blocks at MY measured shift -----
// The certified component draws via slide.addShape/addText/addImage; the proxy adds
// (+9,+2) frame px to every x/y it passes through. Drawing code stays the parent's.
function shiftedSlide(real, dxIn, dyIn) {
  const shift = (o) => {
    const c = Object.assign({}, o);
    if (c.x !== undefined) c.x += dxIn;
    if (c.y !== undefined) c.y += dyIn;
    return c;
  };
  return {
    addShape: (t, o) => real.addShape(t, shift(o)),
    addText: (t, o) => real.addText(t, shift(o)),
    addImage: (o) => real.addImage(shift(o)),
  };
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist chrome (badge numeral 9 = printed frame number) --------------
drawHouseChrome(pres, slide, { numeral: 9 });

// ---- 2) certified parent composition ------------------------------------------
// pass A: unshifted blocks (title + both captions — measured (0,0))
parent.renderBase(pres, slide, {
  only: ["title", "dec_caption", "enc_caption"], chrome: false,
});
// pass B: rigid-shifted diagram blocks (+9,+2 frame px); callout+leader REMOVED
const proxy = shiftedSlide(slide, 9 / 72, 2 / 72);
parent.renderBase(pres, proxy, {
  skip: ["title", "dec_caption", "enc_caption", "callout", "leader"], chrome: false,
});

// ---- 3) DELTA (a): subtitle "(Challenges)" — BLUE (frame modes (0,0,117..129)) --
// ink x380..534 y87..112 — same string/geometry as certified slide 7 (27pt).
slide.addText("(Challenges)", {
  x: px(252.5), y: px(81), w: px(400), h: px(30),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 27, bold: true, color: D.blue,
});

// ---- 3) DELTA (b): blue callout box --------------------------------------------
// box x108..391 y130..188 (fill CCE4F7, 1px blue-gray border); L1 ink x145..352
// (y142..161 incl underline), L2 ink x179..320 (y162..178 incl underline); baseline
// pitch 17px. L1 ~18pt / L2 ~15pt (per-char ink width vs slide-7 calibration).
slide.addShape(pres.ShapeType.rect, {
  x: px(108), y: px(130), w: px(283), h: px(58),
  fill: { color: D.calloutFill }, line: { color: D.calloutEdge, width: 1 },
});
slide.addText(
  [
    { text: "[3] Very Long Sequence", options: { fontSize: 18, underline: { style: "sng" }, breakLine: true } },
    { text: "Vanishing Gradient", options: { fontSize: 15, underline: { style: "sng" } } },
  ],
  {
    x: px(108), y: px(130), w: px(283), h: px(58),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, bold: true, color: D.navy,
    lineSpacing: 17,
  }
);

// ---- 3) DELTA (c): gray summary box ---------------------------------------------
// box x61..440 y201..292 (fill D9D9D9, no border); 3 left-aligned bold lines, ink
// rows y212..230 / 238..255 / 264..281 (pitch 26px); text left edge x74; L1 carries
// the frame's wider gap (colon->RNN 20px vs 9-10px on L2/L3 => two extra spaces).
slide.addShape(pres.ShapeType.rect, {
  x: px(61), y: px(201), w: px(379), h: px(91),
  fill: { color: D.grayFill }, line: { type: "none" },
});
slide.addText(
  [
    { text: "Short Sequence:   ", options: { color: D.navy } },
    { text: "RNN", options: { color: D.green, breakLine: true } },
    { text: "Long Sequence: ", options: { color: D.navy } },
    { text: "LSTM, GRU", options: { color: D.green, breakLine: true } },
    { text: "Very Long Sequence: ", options: { color: D.navy } },
    { text: "FAIL", options: { color: D.failRed } },
  ],
  {
    x: px(74), y: px(201), w: px(366), h: px(91),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 17.5, bold: true,
    lineSpacing: 26,
  }
);

// ---- 3) DELTA (d): BACK-PROPAGATION PANEL ---------------------------------------
// panel rect x502..918 y314..498, fill EAE6DD, thin blue-gray border
slide.addShape(pres.ShapeType.rect, {
  x: px(502), y: px(314), w: px(416), h: px(184),
  fill: { color: D.panelFill }, line: { color: D.panelEdge, width: 1.25 },
});

// (d1) red over-brace (600dpi PNG, measured curve)
slide.addImage({
  path: path.join(ASSETS, "brace009.png"),
  x: px(519), y: px(321), w: px(389), h: px(21),
});

// (d2) "Back Propagation" — ink x640..771 y338..352, bold italic red
slide.addText("Back Propagation", {
  x: px(630), y: px(335), w: px(152), h: px(20),
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 15.5, bold: true, italic: true, color: D.red,
});

// (d3) long LEFT-pointing red arrow: shaft y357.5 x537..888 (lw 3), wedge head
// (tip x520, base x537, h11), filled dot d15 c(895.5,357.5)
slide.addShape(pres.ShapeType.line, {
  x: px(537), y: px(357.5), w: px(351), h: 0,
  line: { color: D.red, width: 3 },
});
slide.addShape(pres.ShapeType.triangle, {
  x: px(523), y: px(349), w: px(11), h: px(17), rotate: 270,
  fill: { color: D.red }, line: { type: "none" },
});
slide.addShape(pres.ShapeType.ellipse, {
  x: px(888), y: px(350), w: px(15), h: px(15),
  fill: { color: D.red }, line: { type: "none" },
});

// (d4) 11 nabla squares (y373..394) aligned with the 11 green boxes; nabla glyph
// grows left->right (measured w: 6,8,9,9,10,11,12,13(+2) for squares 4..11)
const SQ_X = [518, 555, 594, 632, 670, 704, 739, 773, 811, 846, 881];
const SQ_W = [24, 26, 24, 24, 24, 25, 24, 25, 25, 25, 24];
const NB_W = [4, 5, 6, 8, 9, 9, 10, 11, 12, 13, 14];
const NB_H = [5, 6, 8, 10, 11, 11, 12, 12, 14, 15, 16];
for (let k = 0; k < 11; k++) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(SQ_X[k]), y: px(373), w: px(SQ_W[k]), h: px(21),
    fill: { color: D.sqFill }, line: { color: D.sqEdge, width: 0.75 },
  });
  const cx = SQ_X[k] + SQ_W[k] / 2;
  slide.addShape(pres.ShapeType.triangle, {
    x: px(cx - NB_W[k] / 2), y: px(384 - NB_H[k] / 2), w: px(NB_W[k]), h: px(NB_H[k]),
    flipV: true, fill: { type: "none" },
    line: { color: D.nabla, width: Math.max(0.75, NB_W[k] / 9) },
  });
}

// (d5) pink chain: thin dark-red joining line y415 + 10 rects BETWEEN the 11 arrows
slide.addShape(pres.ShapeType.line, {
  x: px(531), y: px(415), w: px(363), h: 0,
  line: { color: D.chainLine, width: 1 },
});
const GB_CX = [531, 566, 600, 638, 673, 707.5, 742, 780, 818, 856, 894]; // green-box centers = arrow x
for (let k = 0; k < 10; k++) {
  const cx = (GB_CX[k] + GB_CX[k + 1]) / 2;
  slide.addShape(pres.ShapeType.rect, {
    x: px(cx - 10), y: px(410), w: px(20), h: px(11),
    fill: { color: D.pinkFill }, line: { type: "none" },
  });
}

// (d6) 11 green up-arrows y419..462 (head at top), then 11 green x-boxes y463..483
for (let k = 0; k < 11; k++) {
  slide.addShape(pres.ShapeType.line, {
    x: px(GB_CX[k]), y: px(419), w: 0, h: px(43),
    line: { color: D.gArrow, width: 1, beginArrowType: "triangle" },
  });
}
const GB_X = [520, 555, 589, 627, 662, 696, 731, 769, 807, 845, 883];
const GB_W = [22, 22, 22, 22, 22, 23, 22, 22, 22, 22, 22];
const XLABELS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
for (let k = 0; k < 11; k++) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(GB_X[k]), y: px(463), w: px(GB_W[k]), h: px(20),
    fill: { color: D.gFill }, line: { color: D.gEdge, width: 0.75 },
  });
  // label: bold dark-green 'x' + true subscript numeral (measured x-glyph h8 => ~14pt)
  slide.addText(
    [
      { text: "x", options: { fontSize: 14 } },
      { text: XLABELS[k], options: { fontSize: 9.5, subscript: true } },
    ],
    {
      x: px(GB_X[k] - 4), y: px(464), w: px(GB_W[k] + 8), h: px(18),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, bold: true, color: D.gLabel,
    }
  );
}

// ---- output (SINGLE-VERSION law: one plain-named deliverable) -------------------
const OUT = path.join(__dirname, "..", "slide_009_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
