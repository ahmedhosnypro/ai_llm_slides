// build/slide_030.js — "Self Attention Mechanism (Input Word plays Different Roles)"
// (Deep Learning DSAI 308, Transformers — Part I). Child build worker attempt 1,
// 2026-10-11. DEPENDENCY-GATED CHILD (edge 30 <- 29, parent certified attempt 2).
//
// Base = the CERTIFIED component components/slide_029.js via renderBase() — never
// re-derived, never copy-pasted. That component itself composes the certified
// slide-026 base, so the whole chain 30 <- 29 <- 26 is the import graph. This script
// draws ONLY slide 30's delta, PIL-measured on unique_slides/slide_030.jpg (960x540,
// 1px = 1pt = 1/72 in; frame-diff + connected-component + scanline forensics in
// scratch/slide030/):
//
//   INHERITED UNCHANGED (frame-diff verified, 0 diff px outside the delta zones):
//   the whole parent composition — peach canvas, stacks, Dot Product box+dots, Soft
//   max bar, Sigma box, flow lines (+W21..W24 labels/nodes), green upArrow + Y output,
//   strip incl. the magenta X2 highlight, left red feed curve, K/V/Q badges, tan
//   KEYs/Values boxes, both cyan callouts, chunky red diagonal, dot-feed arrowheads,
//   AND the parent's subtitle (band y79..101: 0 diff px at >45 — retained verbatim).
//   The parent's resultBox ("Values of Matched Keys ...") is REPLACED (skip) by the
//   blue question box below; the parent frame's mouse cursor (gray blob x736..756
//   y352..366) is a video artifact — correctly absent here (ground rule c).
//
//   DELTA (all measured on THIS frame):
//   (a) title L1 REPLACED: "Self Attention Mechanism (Input Word plays Different
//       Roles)" — 20pt bold (S-glyph caps y59..72, same as the parent's certified
//       20pt), ink x181..752 center 466.5 (same box geometry as the parent title),
//       SATURATED yellow FFFF00 highlight x430..754 y54..77 behind the parenthetical.
//       The parent's title block also carries the subtitle, which is UNCHANGED — so
//       the block is skipped and BOTH lines are redrawn: L2 byte-identical to the
//       certified parent subtitle (20.5pt, ink x108..826, red 9E101E tokens).
//   (b) three translucent yellow circles FFFF00 @ ~50% alpha (B-channel: obs 113-119
//       over base 231 => alpha 0.49-0.51), d=70, NO rim (r=36/38 probes read base):
//       left stack  center (100, 326)   [encloses the 3rd chip row cy328.5 — measured
//                                    position, frame is ground truth]
//       right stack center (803, 329)   [3rd chip row cy328.5]
//       query row   center (294, 492.5) [over the strip's magenta X2 highlight box;
//                                    pink-through-yellow sample (223,165,66) at
//                                    (296,490) confirms the translucent overlay]
//   (c) three white annotation boxes, red C00000 1pt border (washed cores
//       d2ada7/c8a59f/ceaba7 — 1pt red family), ~109x45:
//       KEY   x178..286 y263..307 (border-line centers)
//       VALUE x606..714 y270..314
//       QUERY x378..487 y415..459(.5)
//       Text TWO lines, 14pt bold (caps 10px), line pitch 20px, centered, valign
//       middle: line 1 "X2 is used as" (ink 87px wide in ALL three boxes; the "X2"
//       token RED 9E101E — reddish-mask verified x188..200/616..628/388..400 — rest
//       black 000000, cores 63,65,62), line 2 the role word ALL-RED 9E101E:
//       "Key" (x220..244, 25px) / "Value" (x642..678, 37px) / "Query" (x413..452, 40px)
//       — widths match 14pt bold (26/38/41 predicted). Spec's "'Key' in red, rest
//       black" corrected by the frame: the X2 token is red too. NO leader lines:
//       low-threshold diff scans of all three box<->circle corridors show ONLY the
//       circle arcs and the box borders — the spec's "red leader lines" are not in
//       the frame (spec hallucination; frame wins).
//   (d) question box REPLACES the parent resultBox: white rect x573.5..839.5
//       y440.5..506.5 (border cores x574/x838.5/y441/y505.5 — washed blue-gray
//       a896a4/b0a3ac, the parent resultBox's certified 0000CC 1pt treatment),
//       TWO lines 17pt bold ("Should" segment 56px / caps 12px => ~17pt), line pitch
//       21.5px => lineSpacing 22, centered, text block sits 8px above box center
//       (ink y447..484 in box y441..506) => text box y443 h45 valign middle:
//       line 1 "Should we use " (blue 0000CC) + "SAME X2" (RED 9E101E — class-run
//       scan: red x706..773 = SAME 706..752 + X2 758..773; core (135,13,36)~9E101E;
//       spec's "only X2 red" corrected by the frame) + " Vector" (blue);
//       line 2 "for the three Roles ?" (blue, space before ? verbatim).
//       Word segments: Should(584..639) we(645..665) use(672..699) SAME(705..752)
//       X2(758..773) Vector(780..830) | for(626..647) the(653..676) three(683..721)
//       Roles(728..771) ?(780..787).
//
// LAWS honored: playlist chrome via components/house_chrome.js (numeral 30 = printed
// number on the frame); require the certified parent component (no re-derivation);
// delta at THIS frame's measured geometry; verbatim text (space before "?", unclosed
// subtitle paren); margin:0 + fontFace everywhere; explicit lineSpacing on every
// multi-line box; no '#' in hex; single-version deliverable slide_030_recreated.pptx.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js"
);
const parent = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_029.js"
);

const PX = 1 / 72; // frame px -> inches (same convention as the component)
const C = parent.COLORS; // certified deck palette (subRed 9E101E, blue 0000CC, ...)
const FONT = parent.FONT; // Arial

// delta palette (measured, see header). NOTE: the slide-029 component's COLORS does
// NOT export subRed/titleBlack (those live on the slide-026 palette) — attempt-1 bug:
// C.subRed resolved undefined and the red words fell back to black. All colors are
// therefore pinned locally here.
const D = {
  highlight: "FFFF00", // title parenthetical highlight (saturated, parent-certified)
  circleYellow: "FFFF00", // role circles, 50% alpha
  red: "C00000", // annotation box borders (thin red family)
  subRed: "9E101E", // X2 tokens + role words + SAME X2 (cores 135,13,36 / 161,38,58)
  black: "000000", // title + annotation line-1 body (cores 63,65,62)
  blue: "0000CC", // question text + border (parent resultBox treatment; core 2,0,102)
  white: "FFFFFF",
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1) playlist house chrome (badge numeral = printed 30) --------------------
drawHouseChrome(pres, s, { numeral: 30 });

// ---- 2) certified parent composition minus this slide's replaced blocks --------
// skipped: title (L1 replaced by delta (a); its subtitle is redrawn verbatim below),
// resultBox (replaced by the question box, delta (d)).
parent.renderBase(pres, s, { skip: ["title", "resultBox"] });

// ---- 3) DELTA (b): three translucent yellow role circles ------------------------
// centers (100,326) / (803,329) / (294,492.5), d=70, fill FFFF00 @ ~50% alpha, no rim
const CIRCLES = [
  { cx: 100, cy: 326 }, // Keys stack X2-role highlight (3rd chip row, measured)
  { cx: 803, cy: 329 }, // Values stack
  { cx: 294, cy: 492.5 }, // Query row (over the strip's magenta X2 highlight)
];
for (const c of CIRCLES) {
  s.addShape(pres.ShapeType.ellipse, {
    x: (c.cx - 35) * PX, y: (c.cy - 35) * PX, w: 70 * PX, h: 70 * PX,
    fill: { color: D.circleYellow, transparency: 50 }, line: { type: "none" },
  });
}

// ---- 4) DELTA (c): three white role-annotation boxes -----------------------------
// two-line centered 14pt bold, pitch 20px; line 1 "X2 is used as" (X2 red), line 2
// role word all red. Boxes drawn at their border-line-center rects.
function annBox(x, y, w, h, role) {
  s.addShape(pres.ShapeType.rect, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fill: { color: D.white }, line: { color: D.red, width: 1 },
  });
  s.addText(
    [
      { text: "X", options: { color: D.subRed } },
      { text: "2", options: { subscript: true, color: D.subRed } },
      { text: " is used as", options: { color: D.black, breakLine: true } },
      { text: role, options: { color: D.subRed } },
    ],
    {
      x: x * PX, y: y * PX, w: w * PX, h: h * PX,
      align: "center", valign: "middle", bold: true, fontSize: 14,
      fontFace: FONT, lineSpacing: 20, margin: 0,
    }
  );
}
annBox(178, 263, 108, 44, "Key");   // border centers x178/286 y263/307
annBox(606, 270, 108, 44, "Value"); // x606/714 y270/314
annBox(378, 415, 109, 44.5, "Query"); // x378/487 y415/459.5

// ---- 4b) DELTA (c2): three thin red leader lines (judge attempt-1 MINOR, PIXEL-CONFIRMED)
// First-diff forensics missed these (thin 1-2px washed-red anti-aliased strokes under the
// diff threshold); the judge + circles-crop vision reads flagged them, and a 30-only ink
// scan (lum<220 in frame 30, >=220 in frame 29) confirms all three are NEW in THIS frame:
//   KEY:   box left edge (178,270.5) -- (160,270.5) horizontal stub, then diagonal
//          (160,270.5) -> (141,286.5) ending at the left stack container edge/circle.
//   VALUE: box right edge (714,279.5) -- (731,279.5) stub, then diagonal
//          (731,279.5) -> (769,303.5) ending inside the right stack container/circle.
//   QUERY: box bottom-left corner (377.5,459) diagonal down-left -> (306,466.5) ending
//          inside the query circle (measured trail (357,425)->(306,466.5); the fainter
//          upper tail x358..377 washes into the canvas — the line reads corner->circle).
// Thin red C00000 0.75pt lines (frame ink ~1px washed cores 219,177,161).
function leader(x1, y1, x2, y2) {
  const o = {
    x: Math.min(x1, x2) * PX, y: Math.min(y1, y2) * PX,
    w: Math.abs(x2 - x1) * PX, h: Math.abs(y2 - y1) * PX,
    line: { color: D.red, width: 0.75 },
  };
  if (x2 < x1) o.flipH = true;
  if (y2 < y1) o.flipV = true;
  s.addShape(pres.ShapeType.line, o);
}
leader(178, 270.5, 160, 270.5);   // KEY stub
leader(160, 270.5, 141, 286.5);   // KEY diagonal
leader(714, 279.5, 731, 279.5);   // VALUE stub
leader(731, 279.5, 769, 303.5);   // VALUE diagonal
leader(378, 423.5, 362, 423.5);   // QUERY stub (box left edge, y423.5 — th<220 remeasure)
leader(362, 423.5, 306, 466);     // QUERY diagonal -> inside the circle (trail (361,424.5)->(306,466))

// ---- 5) DELTA (d): question box (replaces the parent resultBox) ------------------
s.addShape(pres.ShapeType.rect, {
  x: 573.5 * PX, y: 440.5 * PX, w: 266 * PX, h: 66 * PX,
  fill: { color: D.white }, line: { color: D.blue, width: 1 },
});
s.addText(
  [
    { text: "Should we use ", options: { color: D.blue } },
    { text: "SAME X", options: { color: D.subRed } },
    { text: "2", options: { subscript: true, color: D.subRed } },
    { text: " Vector", options: { color: D.blue, breakLine: true } },
    { text: "for the three Roles ?", options: { color: D.blue } },
  ],
  {
    x: 573.5 * PX, y: 443 * PX, w: 266 * PX, h: 45 * PX,
    align: "center", valign: "middle", bold: true, italic: true, fontSize: 17,
    fontFace: FONT, lineSpacing: 22, margin: 0,
  }
);

// ---- 6) DELTA (a): MY title block (L1 new; L2 = parent's subtitle, unchanged) ----
// L1 ink x181..752 (center 466.5), 20pt bold, highlight x430..754 y54..77.
// Subtitle retained verbatim from the certified parent (0 diff px y79..101):
// 20.5pt bold, ink x108..826, red 9E101E words Query/X2/Keys/Values ("All" black).
s.addText(
  [
    { text: "Self Attention Mechanism ", options: {} },
    { text: "(Input Word plays Different Roles)", options: { highlight: D.highlight } },
  ],
  {
    x: 0.41417, y: 0.725, w: 12.13, h: 0.42, align: "center", valign: "top",
    fontSize: 20, bold: true, color: D.black, fontFace: FONT, margin: 0,
  }
);
{
  const red = { color: D.subRed };
  s.addText(
    [
      { text: "(", options: {} },
      { text: "Query", options: red },
      { text: " using ", options: {} },
      { text: "X", options: red }, { text: "2", options: { subscript: true, color: D.subRed } },
      { text: " All ", options: {} },
      { text: "Keys", options: red },
      { text: " in Dictionary and retrieve Corresponding ", options: {} },
      { text: "Values", options: red },
    ],
    {
      x: 0.42111, y: 1.052, w: 12.13, h: 0.36, align: "center", valign: "top",
      fontSize: 20.5, bold: true, color: D.black, fontFace: FONT, margin: 0,
    }
  );
}

// ---- output (SINGLE-VERSION law: one plain-named deliverable) -------------------
const OUT = "videos/deep-learning/001_transformers_part1/recreated_pptx/slide_030_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
