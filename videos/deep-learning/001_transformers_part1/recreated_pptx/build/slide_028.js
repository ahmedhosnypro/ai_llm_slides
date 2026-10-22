// build/slide_028.js — "Self Attention Mechanism (Not Sensitive to Words Order)"
// (Deep Learning DSAI 308, Transformers — Part I). Child build worker attempt 1,
// 2026-10-11. DEPENDENCY-GATED CHILD (edge 28 <- 26, parent certified attempt 1).
//
// Base = the CERTIFIED component components/slide_026.js via renderBase() — never
// re-derived, never copy-pasted. This script draws ONLY slide 28's delta, PIL-measured
// on unique_slides/slide_028.jpg (960x540, 1px = 1pt = 1/72 in; frame-diff + scanline
// forensics in scratch/slide028/, see qa/slide028/worker_report.md):
//   (a) title line 1 parenthetical "(Not Sensitive to Words Order)" (yellow highlight
//       x481..775 y53..78; ink x233..772 center 502.5 — SAME box/size as parent);
//   (b) subtitle word order shuffles to X4, X2, X1, X3 (verbatim frame content; ink
//       x186..~820 y81..101 — pixel-identical band to the parent's, digits swapped);
//   (c) bottom token row labels shuffle to X4, X2(highlighted), X1, X3 — the strip
//       block is REPLACED (labels only). Strip geometry (container x178..493 y473..518,
//       glyph xs 191/265/339/414, highlight box x261..337 y472..507, X2 label x284..311
//       y480..505) verified pixel-IDENTICAL to the parent frame by diffing the two
//       frames (n>60=0 everywhere except the three digit glyphs + old cursor spot);
//       values reused from the component's certified provenance, labels per the frame.
//   (d) NEW white callout box "Sequential nature of the input is IGNORED" — roundRect
//       x382..719 y426..460 (w337 h34), white fill, dashed green 3B7A40 border
//       (measured dash rhythm ~5on/2off), green 2A842A BOLD ITALIC text (italic per
//       crop-B vision read of the original; matches the deck's certified Y-label green;
//       ink x392..705 y437..451, centered), 15.5pt (render-calibrated).
//   (e) NEW callout box "Mitigated Later with" / "Positional Encoder" —
//       roundRect x725..896 y459..523.5 (w171 h64.5), PALE MINT E6FCE7 fill
//       (crop-B vision read + PIL: lower-interior median (231,253,232) == the deck's
//       container fill; box1's fill is genuinely WHITE (252,255,252)), dashed green
//       border; line 1 red 9E101E bold (matches deck X-label red; ink x734..888
//       y476..491), line 2 blue 0033CC bold italic (matches deck W-label blue; ink
//       x736..886 y494..506); line pitch 18px -> lineSpacing 18; 16.5pt
//       (render-calibrated); block vertically centered.
//   (f) Dot-Product red diamond marks (8) — see block 4b below (judge attempt 2
//       finding, pixel-verified in THIS frame; absent from the certified parent's
//       render, so drawn here as child delta, component untouched).
//   Z-ORDER: strip kept in its certified z-slot (before queryArrows/feedCurves) by
//   splitting renderBase into two opts-gated passes; the new boxes draw AFTER
//   feedCurves so they occlude the right feed curve segment (x~725..742 y~459..468)
//   exactly as the original's layering shows. Title drawn last (parent ORDER).
//   The stacked glyph labels are NOT part of the delta: frame-diff + digit
//   cross-correlation (diagonal sim 0.94-1.0) prove slide 28's stacks are
//   pixel-identical to the parent's (X1..X4 top-to-bottom, both sides) — inherited
//   untouched. (analysis JSON's "X4..X1 top-to-bottom" claim contradicts the frame;
//   the frame is ground truth — documented in worker_report.md.)
//   Mouse cursor (near W23 at x523..539 y327..342 in this frame) = video artifact,
//   not recreated (judge ground rule c).
//
// LAWS honored: playlist chrome via components/house_chrome.js (numeral 28 = printed
// number on the frame); require the certified component (no re-derivation); verbatim
// text incl. the unbalanced parens "( ... ( X4, X2, X1, X3 )"; margin:0 + explicit
// fontFace everywhere; explicit lineSpacing 18 on the only multi-line box; no '#'
// in hex; single-version deliverable.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);
const base = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_026.js"
);

const PX = 1 / 72; // frame px -> inches (same convention as the component)
const C = base.COLORS; // certified deck palette (cell fills, subRed, container greens...)

// delta palette (measured, see header)
const D = {
  boxFill: "FFFFFF",
  boxBorder: "3B7A40",
  greenText: "2A842A",
  redText: "9E101E",
  blueText: "0033CC",
};
const FONT = base.FONT; // Arial

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1) playlist house chrome (badge numeral = printed 28) --------------------
drawHouseChrome(pres, s, { numeral: 28 });

// ---- 2) certified parent composition, minus title/strip/arrows-tail ------------
// (strip replaced by delta (c); queryArrows+feedCurves re-drawn after it so the
// certified z-order strip < queryArrows < feedCurves is preserved; title = delta (a/b))
base.renderBase(pres, s, { skip: ["title", "strip", "queryArrows", "feedCurves"] });

// ---- 3) DELTA (c): bottom token row, labels X4 / X2(highlighted) / X1 / X3 ------
// Geometry = the parent strip's certified values, pixel-verified identical on THIS
// frame (see header). Only the three non-highlighted digit labels differ.
function glyph28(x0, cy, labelSize, label) {
  const cellW = 12, gap = 1, h = 14;
  const fills = [C.cellYellow, C.cellYellow, C.cellOrchid, C.cellLavender, C.cellPink];
  for (let i = 0; i < 5; i++) {
    s.addShape(pres.ShapeType.rect, {
      x: (x0 + i * (cellW + gap)) * PX, y: (cy - h / 2) * PX,
      w: cellW * PX, h: h * PX, fill: { color: fills[i] }, line: { type: "none" },
    });
  }
  const lx = (x0 + 2 * (cellW + gap)) * PX;
  s.addText(
    [
      { text: "X", options: {} },
      { text: label, options: { subscript: true } },
    ],
    {
      x: lx - 0.06, y: (cy - 9) * PX, w: 0.32, h: 0.25,
      align: "center", valign: "middle", bold: true, fontSize: labelSize,
      color: C.subRed, fontFace: FONT, margin: 0,
    }
  );
}
s.addShape(pres.ShapeType.roundRect, {
  x: 178 * PX, y: 473 * PX, w: 315 * PX, h: 45 * PX, rectRadius: 0.07,
  fill: { color: C.containerFill },
  line: { color: C.containerBorder, width: 1.25, dashType: "dash" },
});
const xs = [191, 265, 339, 414];
glyph28(xs[0], 494.5, 9.5, "4");
glyph28(xs[2], 494.5, 9.5, "1");
glyph28(xs[3], 494.5, 9.5, "3");
// highlighted X2: dotted-border box + internal 5-cell magenta glyph + red label
s.addShape(pres.ShapeType.roundRect, {
  x: 261 * PX, y: 472 * PX, w: 76 * PX, h: 35 * PX, rectRadius: 0.05,
  fill: { type: "none" },
  line: { color: C.x2Border, width: 1.5, dashType: "sysDot" },
});
const x2fills = ["E39FBE", "E0A5D3", "C44C88", "D595E2", "DC92E3"];
for (let ci = 0; ci < 5; ci++) {
  s.addShape(pres.ShapeType.rect, {
    x: (265 + ci * 13) * PX, y: 487.5 * PX, w: (ci === 4 ? 12.4 : 12) * PX, h: 14 * PX,
    fill: { color: x2fills[ci] }, line: { type: "none" },
  });
}
s.addText(
  [
    { text: "X", options: {} },
    { text: "2", options: { subscript: true } },
  ],
  {
    x: 279 * PX, y: 478 * PX, w: 0.42, h: 0.24,
    align: "center", valign: "middle", fontSize: 11, bold: true,
    color: C.subRed, fontFace: FONT, margin: 0,
  }
);

// ---- 4) certified z-tail: query arrows + feed curves --------------------------
base.renderBase(pres, s, { only: ["queryArrows", "feedCurves"] });

// ---- 4b) REMOVED 2026-10-13 (F8 cascade): the local 8-diamond delta is deleted.
// The founder-fixed components/slide_026.js now draws the REAL marks (white/ice-blue
// halo + inner blue disc + dark-red arrowheads at the measured bboxes: on-line-left
// right-pointing (311-322,243-251)...(258-268,369-377), below-dot up-pointing
// (326-335,254-264)...(272-280,381-390)); keeping the diamonds would double-draw red
// marks at the same coordinates. Measured evidence: scratch/slide028/CASCADE_DELTA.md,
// scratch/slide028/right_zone/cropdot_vision_1.txt.

// ---- 5) DELTA (d): green annotation box ----------------------------------------
s.addShape(pres.ShapeType.roundRect, {
  x: 382 * PX, y: 426 * PX, w: 337 * PX, h: 34 * PX, rectRadius: 0.15,
  fill: { color: D.boxFill },
  line: { color: D.boxBorder, width: 1.25, dashType: "dash" },
});
s.addText("Sequential nature of the input is IGNORED", {
  x: 382 * PX, y: 426 * PX, w: 337 * PX, h: 34 * PX,
  align: "center", valign: "middle", fontSize: 15.5, bold: true, italic: true,
  color: D.greenText, fontFace: FONT, margin: 0,
});

// ---- 6) DELTA (e): "Mitigated Later with / Positional Encoder" box --------------
// fill = pale mint E6FCE7 (crop-B vision read + PIL: lower-interior median
// (231,253,232) == the deck's container fill; box1's fill is WHITE (252,255,252) —
// the two boxes genuinely differ).
s.addShape(pres.ShapeType.roundRect, {
  x: 725 * PX, y: 459 * PX, w: 171 * PX, h: 64.5 * PX, rectRadius: 0.15,
  fill: { color: "E6FCE7" },
  line: { color: D.boxBorder, width: 1.25, dashType: "dash" },
});
s.addText(
  [
    { text: "Mitigated Later with", options: { color: D.redText, breakLine: true } },
    { text: "Positional Encoder", options: { color: D.blueText, italic: true } },
  ],
  {
    x: 725 * PX, y: 459 * PX, w: 171 * PX, h: 64.5 * PX,
    align: "center", valign: "middle", fontSize: 16.5, bold: true,
    fontFace: FONT, lineSpacing: 18, margin: 0,
  }
);

// ---- 7) DELTA (a/b): MY title block (child frame is ground truth for its text) --
// Same certified boxes/sizes as the parent's drawTitle; strings + highlight extent
// from THIS frame (ink L1 x233..772 center 502.5; highlight x481..775; subtitle ink
// band pixel-identical to parent's).
s.addText(
  [
    { text: "Self Attention Mechanism ", options: {} },
    { text: "(Not Sensitive to Words Order)", options: { highlight: C.highlight } },
  ],
  {
    x: 0.9125, y: 0.725, w: 12.13, h: 0.42, align: "center", valign: "top",
    fontSize: 20, bold: true, color: C.titleBlack, fontFace: FONT, margin: 0,
  }
);
const red = { color: C.subRed };
s.addText(
  [
    { text: "(Self Attention of word ", options: {} },
    { text: "X", options: red }, { text: "2", options: { subscript: true, color: C.subRed } },
    { text: " w.r.t All words in Sentence ( ", options: {} },
    { text: "X", options: red }, { text: "4", options: { subscript: true, color: C.subRed } },
    { text: ", ", options: red },
    { text: "X", options: red }, { text: "2", options: { subscript: true, color: C.subRed } },
    { text: ", ", options: red },
    { text: "X", options: red }, { text: "1", options: { subscript: true, color: C.subRed } },
    { text: ", ", options: red },
    { text: "X", options: red }, { text: "3", options: { subscript: true, color: C.subRed } },
    { text: " )", options: {} },
  ],
  {
    x: 0.843, y: 1.052, w: 12.13, h: 0.36, align: "center", valign: "top",
    fontSize: 19.5, bold: true, color: C.titleBlack, fontFace: FONT, margin: 0,
  }
);

// ---- output (SINGLE-VERSION law: one plain-named deliverable) -------------------
const OUT = "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_028_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
