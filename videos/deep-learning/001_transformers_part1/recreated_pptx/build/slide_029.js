// build/slide_029.js — "Self Attention Mechanism (as Query and {Key-Value} Dictionary)"
// (Deep Learning DSAI 308, Transformers — Part I). Child build worker attempt 1,
// 2026-10-11. DEPENDENCY-GATED CHILD (edge 29 <- 26, parent certified attempt 1).
//
// Base = the CERTIFIED component components/slide_026.js via renderBase() — never
// re-derived, never copy-pasted. This script draws ONLY slide 29's delta, PIL-measured
// on unique_slides/slide_029.jpg (960x540, 1px = 1pt = 1/72 in; frame-diff + scanline +
// ASCII-map forensics in scratch/slide029/, banked in qa/slide029/worker_report.md):
//
//   INHERITED UNCHANGED (frame-diff verified): peach canvas, both stacks, Dot Product
//   box+dots, Soft max bar, Sigma box, flow lines (+W21..W24 labels, nodes), green
//   upArrow + Y output, strip incl. the magenta 5-cell X2 highlight (probes at
//   x263..330 y476..497 read IDENTICAL to the parent frame). The Sigma->Y dark-red
//   arrow at x583 reads identical in BOTH frames (red tip y151..156 + JPEG-washed
//   luma column below) — inherited via arrowsGreen; the parent ovals that covered it
//   are GONE in this frame (oval-fill probes: child = canvas where parent = F9FCDB).
//
//   DELTA (all measured on THIS frame):
//   (a) title L1 "Self Attention Mechanism (as Query and {Key-Value} Dictionary)" —
//       20pt bold, SATURATED yellow FFFF00 highlight x411..773 y53..78 (NOT the
//       parent's pale FBF29B — measured F5FD1B cores); ink x163..770, center 466.5
//       (box shifted left of parent's).
//   (b) subtitle "(Query using X2 All Keys in Dictionary and retrieve Corresponding
//       Values" (verbatim, unclosed paren) — 20.5pt bold (attempt-1 closed loop: 19.5pt
//       rendered the ink 5.6% narrow vs the frame; 20.5 matches ink x108..826),
//       ink x108..826 y79..101, center 467; red 9E101E words = "Query", "X2", "Keys",
//       "Values" (pixel-verified: "All" ink core 000100 = BLACK; spec's "All Keys red"
//       corrected by the frame).
//   (c) parent's three blue ovals (labels block) REMOVED — replaced by two cyan
//       callouts, pale-cyan EDFBFB fill + dark-green 3B7A40 DASHED border (same
//       border family as the stack containers; dash cores 46785B/5D7B61 measured):
//       c1 x315..490 y140..184: "Matched KEYS with" / "Relevance Percentage",
//       12pt bold italic CC00CC, LEFT-aligned at x326 (L1 ink 325..451, L2 329..469),
//       line pitch 15; the noun "KEYS" is RED C00000 (x384..420).
//       c2 x634..846 y145..188: "Retrieve VALUES" / "Weighted by their Relevance",
//       CENTER-aligned (L1 682..794 and L2 649..828 both center 738.5), pitch 16;
//       noun "VALUES" RED C00000 (x741..794).
//   (d) NEW tan label boxes over the stacks: "KEYs" x64..134 y190..214, "Values"
//       x762..835 y193..218, fill E8C79A (spec), 11pt bold 990000 (spec dark-red
//       family; cores 861708 on tan), centered.
//   (e) NEW red circle badges with WHITE bold letters (letter cores FFF2F3 — the
//       spec's "bold red K" corrected by the frame): K center (163,342) d24 right of
//       the left stack; V center (747.5,342.5) d24 left of the right stack; Q center
//       (258.5,439) d24 right of the query box. Fill C00000 (cores A2051A..B10F1C).
//   (f) NEW orange Query box x111..240 y420..460, fill F2C699, border CFB69B 1pt
//       (darker-than-fill rim measured): "Query" 17pt bold 990000 / "ALL Keys with X2"
//       12pt bold 990000 (subscripted 2), centered, pitch 16.
//   (g) NEW result box x557..827 y433..502: white fill, thin 0000CC border (frame
//       reads a 1px washed blue-gray A097AC — spec's blue kept at 1pt), 3 centered
//       lines 13pt pitch 19: "Values"(red C00000 bi) " of Matched "(blue 0000CC)
//       "Keys"(red bi) / "are returned"(blue) / "when Running "(blue) "Query"(red bi).
//       Red-noun pattern pixel-verified (red x-runs 595..645 / 745..783 / 728..774).
//   (h) feedCurves REPLACED: LEFT curve only, now RED C00000 dashed (path pixel
//       AC5D59 at (102,430) vs parent gray EAD8C2) with a RED head (AB000E at
//       (97,404) vs parent green 477648), same certified path
//       (170,472)-(130,468)-(112,460)-(104,448)-(102,430)-(102,409). RIGHT curve +
//       green head REMOVED (probes at (497,494)/(530,492)/(795,416)/(801,404) and the
//       whole right band: child = canvas where parent = curve/head pixels).
//   (i) queryArrows: the thin red x298 arrow (strip X2 -> Dot Product) REMOVED
//       (0 red px in x272..500 y404..470); the chunky red C5000F diagonal
//       (266,526)->(284,512) KEPT (cores BF000D/C1000C identical to parent).
//   Z-ORDER: inherited blocks keep their certified slots (renderBase ORDER minus
//   skips); left curve drawn before the query box (frame shows canvas at (112,460) —
//   box covers the curve's edge); callouts/boxes/badges/title on top. Title last
//   (parent ORDER).
//   Mouse-cursor artifacts in the parent frame are video artifacts — not recreated.
//
// LAWS honored: playlist chrome via components/house_chrome.js (numeral 29 = printed
// number on the frame); require the certified component (no re-derivation); verbatim
// text incl. the unbalanced paren and the literal "{Key-Value}" braces; margin:0 +
// fontFace everywhere; explicit lineSpacing on every multi-line box; no '#' in hex;
// single-version deliverable slide_029_recreated.pptx.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);
const base = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_026.js"
);

const PX = 1 / 72; // frame px -> inches (same convention as the component)
const C = base.COLORS; // certified deck palette (subRed 9E101E, containerBorder 3B7A40 ...)
const FONT = base.FONT; // Arial

// delta palette (measured, see header)
const D = {
  highlight: "FFFF00",   // title parenthetical highlight (saturated, F5FD1B cores)
  calloutFill: "EDFBFB", // pale cyan (interior samples EFFCFE/EBFEFD/EDFCFC)
  calloutBorder: "3B7A40", // dashed dark green (dash cores 46785B/5D7B61)
  magenta: "CC00CC",     // callout text (cores 7C1186 JPEG-darkened)
  red: "C00000",         // KEYS/VALUES nouns, badges, left curve, result nouns
  darkRed: "990000",     // Query box + tan-label text (spec dark-red family)
  queryFill: "F2C699",
  queryBorder: "CFB69B",
  blue: "0000CC",        // result-box text + border (spec; frame core 0D027B)
  tanBox: "E8C79A",      // KEYs/Values label boxes (spec; measured E7C9A9)
  white: "FFFFFF",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1) playlist house chrome (badge numeral = printed 29) --------------------
drawHouseChrome(pres, s, { numeral: 29 });

// ---- 2) certified parent composition minus this slide's replaced blocks --------
// skipped: title (delta a/b), labels (the 3 ovals -> callouts, delta c),
// queryArrows (thin arrow removed; chunky diagonal re-drawn as delta i),
// feedCurves (right curve+head removed, left curve recolored — delta h).
base.renderBase(pres, s, { skip: ["title", "labels", "queryArrows", "feedCurves"] });

// ---- 3) DELTA (h): LEFT feed curve, RED dashed + RED head ----------------------
const L = [[170, 472], [130, 468], [112, 460], [104, 448], [102, 430], [102, 409]];
for (let i = 0; i < L.length - 1; i++) {
  const o = {
    x: Math.min(L[i][0], L[i + 1][0]) * PX, y: Math.min(L[i][1], L[i + 1][1]) * PX,
    w: Math.abs(L[i + 1][0] - L[i][0]) * PX, h: Math.abs(L[i + 1][1] - L[i][1]) * PX,
    line: { color: D.red, width: 1, dashType: "dash" },
  };
  if (L[i + 1][0] < L[i][0]) o.flipH = true;
  if (L[i + 1][1] < L[i][1]) o.flipV = true;
  s.addShape(pres.ShapeType.line, o);
}
s.addShape(pres.ShapeType.triangle, {
  x: 97 * PX, y: 399 * PX, w: 9 * PX, h: 12 * PX,
  fill: { color: D.red }, line: { type: "none" },
});

// ---- 4) DELTA (f): orange Query box --------------------------------------------
s.addShape(pres.ShapeType.roundRect, {
  x: 111 * PX, y: 420 * PX, w: 129 * PX, h: 40 * PX, rectRadius: 0.06,
  fill: { color: D.queryFill },
  line: { color: D.queryBorder, width: 1 },
});
s.addText(
  [
    { text: "Query", options: { fontSize: 17, breakLine: true } },
    { text: "ALL Keys with X", options: { fontSize: 10.5 } },
    { text: "2", options: { fontSize: 10.5, subscript: true } },
  ],
  {
    x: 111 * PX, y: 421 * PX, w: 129 * PX, h: 38 * PX,
    align: "center", valign: "middle", bold: true, color: D.darkRed,
    fontFace: FONT, lineSpacing: 16, margin: 0,
  }
);

// ---- 5) DELTA (e): K / V / Q badges (red circle, white bold letter) -------------
function badge(cx, cy, letter) {
  s.addShape(pres.ShapeType.ellipse, {
    x: (cx - 12) * PX, y: (cy - 12) * PX, w: 24 * PX, h: 24 * PX,
    fill: { color: D.red }, line: { type: "none" },
  });
  s.addText(letter, {
    x: (cx - 12) * PX, y: (cy - 12) * PX, w: 24 * PX, h: 24 * PX,
    align: "center", valign: "middle", bold: true, fontSize: 13,
    color: D.white, fontFace: FONT, margin: 0,
  });
}
badge(163, 342, "K");
badge(747.5, 342.5, "V");
badge(258.5, 439, "Q");

// ---- 6) DELTA (d): tan KEYs / Values label boxes --------------------------------
s.addShape(pres.ShapeType.roundRect, {
  x: 64 * PX, y: 190 * PX, w: 70 * PX, h: 24 * PX, rectRadius: 0.06,
  fill: { color: D.tanBox }, line: { type: "none" },
});
s.addText("KEYs", {
  x: 64 * PX, y: 190 * PX, w: 70 * PX, h: 24 * PX,
  align: "center", valign: "middle", bold: true, fontSize: 11,
  color: D.darkRed, fontFace: FONT, margin: 0,
});
s.addShape(pres.ShapeType.roundRect, {
  x: 762 * PX, y: 193 * PX, w: 73 * PX, h: 25 * PX, rectRadius: 0.06,
  fill: { color: D.tanBox }, line: { type: "none" },
});
s.addText("Values", {
  x: 762 * PX, y: 193 * PX, w: 73 * PX, h: 25 * PX,
  align: "center", valign: "middle", bold: true, fontSize: 11,
  color: D.darkRed, fontFace: FONT, margin: 0,
});

// ---- 7) DELTA (c): two cyan callouts (replace the parent's three ovals) ---------
// c1: left-aligned text (measured L1 x325..451, L2 x329..469)
s.addShape(pres.ShapeType.roundRect, {
  x: 315 * PX, y: 140 * PX, w: 175 * PX, h: 44 * PX, rectRadius: 0.07,
  fill: { color: D.calloutFill },
  line: { color: D.calloutBorder, width: 1, dashType: "dash" },
});
s.addText(
  [
    { text: "Matched ", options: { color: D.magenta } },
    { text: "KEYS", options: { color: D.red } },
    { text: " with", options: { color: D.magenta, breakLine: true } },
    { text: "Relevance Percentage", options: { color: D.magenta } },
  ],
  {
    x: 326 * PX, y: 145 * PX, w: 160 * PX, h: 34 * PX,
    align: "left", valign: "middle", bold: true, italic: true, fontSize: 12,
    fontFace: FONT, lineSpacing: 15, margin: 0,
  }
);
// c2: center-aligned text (measured L1/L2 both centered on x738.5)
s.addShape(pres.ShapeType.roundRect, {
  x: 634 * PX, y: 145 * PX, w: 212 * PX, h: 43 * PX, rectRadius: 0.07,
  fill: { color: D.calloutFill },
  line: { color: D.calloutBorder, width: 1, dashType: "dash" },
});
s.addText(
  [
    { text: "Retrieve ", options: { color: D.magenta } },
    { text: "VALUES", options: { color: D.red, breakLine: true } },
    { text: "Weighted by their Relevance", options: { color: D.magenta } },
  ],
  {
    x: 634 * PX, y: 150 * PX, w: 212 * PX, h: 33 * PX,
    align: "center", valign: "middle", bold: true, italic: true, fontSize: 12,
    fontFace: FONT, lineSpacing: 16, margin: 0,
  }
);

// ---- 8) DELTA (g): result box ----------------------------------------------------
s.addShape(pres.ShapeType.rect, {
  x: 557 * PX, y: 433 * PX, w: 270 * PX, h: 69 * PX,
  fill: { color: D.white },
  line: { color: D.blue, width: 1 },
});
s.addText(
  [
    { text: "Values", options: { color: D.red, bold: true, italic: true } },
    { text: " of Matched ", options: { color: D.blue } },
    { text: "Keys", options: { color: D.red, bold: true, italic: true, breakLine: true } },
    { text: "are returned", options: { color: D.blue, breakLine: true } },
    { text: "when Running ", options: { color: D.blue } },
    { text: "Query", options: { color: D.red, bold: true, italic: true } },
  ],
  {
    x: 559 * PX, y: 437 * PX, w: 266 * PX, h: 61 * PX,
    align: "center", valign: "middle", fontSize: 13, color: D.blue,
    fontFace: FONT, lineSpacing: 19, margin: 0,
  }
);

// ---- 9) DELTA (i): chunky red diagonal arrow (kept from parent queryArrows) -----
{
  const o = {
    x: 266 * PX, y: 512 * PX, w: 18 * PX, h: 14 * PX,
    line: { color: "C5000F", width: 4, endArrowType: "triangle" },
  };
  o.flipV = true; // from (266,526) up-right to (284,512)
  s.addShape(pres.ShapeType.line, o);
}

// ---- 9b) REMOVED 2026-10-13 (F8 cascade): the local 4 up-triangle delta is deleted.
// The founder-fixed components/slide_026.js now draws the real dot-unit marks at the
// MEASURED bboxes (the local DOTFEEDS sat up to 6.5px left / 4px high of the measured
// below-dot arrowheads, and the 4 on-line-left heads were entirely missing — the fixed
// component supplies all 8 arrowheads); keeping DOTFEEDS would double-draw marks.
// Evidence: scratch/slide029/CASCADE_DELTA.md, scratch/slide029/right_zone/*.txt.

// ---- 10) DELTA (a/b): MY title block --------------------------------------------
// L1 ink x163..770 (center 466.5px); highlight x411..773 y53..78 saturated yellow.
// Subtitle ink x108..826 (center 467px); red words Query / X2 / Keys / Values.
s.addText(
  [
    { text: "Self Attention Mechanism ", options: {} },
    { text: "(as Query and {Key-Value} Dictionary)", options: { highlight: D.highlight } },
  ],
  {
    x: 0.41417, y: 0.725, w: 12.13, h: 0.42, align: "center", valign: "top",
    fontSize: 20, bold: true, color: C.titleBlack, fontFace: FONT, margin: 0,
  }
);
const red = { color: C.subRed };
s.addText(
  [
    { text: "(", options: {} },
    { text: "Query", options: red },
    { text: " using ", options: {} },
    { text: "X", options: red }, { text: "2", options: { subscript: true, color: C.subRed } },
    { text: " All ", options: {} },
    { text: "Keys", options: red },
    { text: " in Dictionary and retrieve Corresponding ", options: {} },
    { text: "Values", options: red },
  ],
  {
    x: 0.42111, y: 1.052, w: 12.13, h: 0.36, align: "center", valign: "top",
    fontSize: 20.5, bold: true, color: C.titleBlack, fontFace: FONT, margin: 0,
  }
);

// ---- output (SINGLE-VERSION law: one plain-named deliverable) -------------------
const OUT = "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_029_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
