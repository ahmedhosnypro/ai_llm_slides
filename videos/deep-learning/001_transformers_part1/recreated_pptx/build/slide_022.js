// build/slide_022.js — slide 022 "Continuous bag-of-words (CBOW)   vs Skip-Gram Models"
//
// ROOT build (no dependency parents). Geometry PIL-measured from the original frame
// videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg (960x540,
// 1px = 1pt = 1/72 in) — scratch/slide022/measure*.py — plus one gate vision read of
// the CBOW PROJECTION zoom (vision_lproj.txt) that pinned the projection squares.
// Content per analysis/slide_022_final.json (gate-passed PASS_WITH_FIXES, score 9),
// provenance per slide_022_source/SOURCES.md (Mikolov 2013 Fig 1, course recoloring).
//
// Measured facts honored (frame px):
//   blue panels L x117..487 / R x486..840 (shared middle edge), y122..524, #0000CC
//   containers y142..462: L IN 157..259 | L PROJ 264..366 | L OUT 372..473
//                         R IN 498..572 | R PROJ 577..659 | R OUT 665..767
//   squares (white fill, #D9D9D9 outline, w22-23 x h42-46): L-IN x218..240 at
//     y193/248/355/409 (pair-gap-pair rhythm); L-OUT x391..413 y303; R-IN x547..569
//     y303; R-OUT x676..698 y193/248/355/409; PROJ squares x305..328 / x607..630,
//     y302..348 (vision-pinned)
//   headers (Arial 11 regular #404040): INPUT x215..246 / PROJECTION x276..347 /
//     OUTPUT x377..421 / INPUT x523..554 / PROJECTION x584..654 / OUTPUT x676..720,
//     band y164..173 — widths match regular Arial advances exactly (bold rejected)
//   word labels (Arial 11): w(t-2)/(t-1)/(t+1)/(t+2) #404040 left edge x184 (left
//     panel) / x713 (right panel), band centers y213.5/271/378.5/432 and
//     216.5/271/376/429.5; w(t) #000000 at x420 (L-OUT) / x506 (R-IN)
//   SUM (Arial 11 #404040) centered over L-PROJ square, band y284..291, x304..329
//   arrows (black 1pt, triangle heads): CBOW 4 converge from input squares' right
//     edges to 4 spread points on the PROJ square's left edge + 1 horizontal exit
//     (329,323)->(388,323); Skip-gram 1 horizontal (570,324)->(604,324) + 4 fan from
//     spread points on the PROJ square's right edge to the R-OUT squares' left edges
//   tags: L x254..378 y474..502, R x551..675, fill #FFFF99, border #C00000,
//     text bold 16 — tag TEXT is dark olive #4A4A00 in the frame (core pixels
//     110,117,37 = #4A4A00-on-yellow JPEG blend; red #C00000 would measure R>>G —
//     measured R==G, so red is REJECTED; #4A4A00 is already this deck's on-yellow
//     ink, cf. badge outline in the slide's own spec colors)
//   title: spec string verbatim (3 spaces before "vs"), Arial bold #C00000 26pt —
//     26pt (not spec's ~28pt estimate) because measured ink width 726px and cap
//     height ~18.5px both solve to 26pt Arial Bold; ink center x494 (not 480) —
//     title box centered on the MEASURED center.
//   mouse cursor near w(t-1) in the right panel = recording artifact, NOT drawn.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const px = (v) => v / 72; // frame px -> inches

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pres.addSlide();

// ---- playlist house chrome (badge numeral = printed number on the frame) ----
drawHouseChrome(pres, slide, { numeral: 22 });

const SANS = "Arial";

// ---- palette (spec accents; JPEG-validated in scratch measurements) ----------
const BLUE = "0000CC";   // panel borders
const DKRED = "8B0000";  // INPUT container borders
const ORANGE = "E8940A"; // PROJECTION container borders
const PEACH = "F5C99B";  // PROJECTION fill
const GREEN = "008000";  // OUTPUT container borders
const SQRLINE = "D9D9D9";// small-square outlines
const HEADER = "404040"; // INPUT/PROJECTION/OUTPUT + w(t-k) labels + SUM
const BLACK = "000000";  // arrows + w(t) labels
const TAGFILL = "FFFF99";
const TAGEDGE = "C00000";
const TAGTEXT = "4A4A00";
const TITLE_RED = "C00000";

// ---- helper: text box centered on a measured point --------------------------
function label(text, cx, cy, opts = {}) {
  const w = opts.w || 1.6;
  slide.addText(text, {
    x: px(cx) - w / 2, y: px(cy) - 0.14, w, h: 0.28,
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: opts.fontSize || 11,
    color: opts.color || HEADER, bold: !!opts.bold,
    lineSpacing: opts.fontSize ? opts.fontSize * 1.2 : 13.2,
  });
}
function leftLabel(text, leftX, cy, color) {
  slide.addText(text, {
    x: px(leftX), y: px(cy) - 0.14, w: 1.1, h: 0.28,
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 11, color, lineSpacing: 13.2,
  });
}

// ---- title (spec string verbatim; 26pt per frame-measured metrics) ----------
slide.addText("Continuous bag-of-words (CBOW)   vs Skip-Gram Models", {
  x: px(494) - 12.13 / 2, y: 0.954, w: 12.13, h: 0.5,
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 26, bold: true, color: TITLE_RED,
  lineSpacing: 31.2,
});

// ---- two blue panels (shared middle edge at x486) ---------------------------
slide.addShape(pres.ShapeType.rect, {
  x: px(117), y: px(122), w: px(487 - 117), h: px(524 - 122),
  fill: { type: "none" }, line: { color: BLUE, width: 2.5 },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(486), y: px(122), w: px(840 - 486), h: px(524 - 122),
  fill: { type: "none" }, line: { color: BLUE, width: 2.5 },
});

// ---- six containers (y142..462) ---------------------------------------------
const CTY = 142, CTH = 462 - 142;
function container(x0, x1, edge, fill) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x0), y: px(CTY), w: px(x1 - x0), h: px(CTH),
    fill: fill ? { color: fill } : { type: "none" },
    line: { color: edge, width: 2 },
  });
}
container(157, 259, DKRED, "FFFFFF");   // L INPUT
container(264, 366, ORANGE, PEACH);     // L PROJECTION
container(372, 473, GREEN, "FFFFFF");   // L OUTPUT
container(498, 572, DKRED, "FFFFFF");   // R INPUT
container(577, 659, ORANGE, PEACH);     // R PROJECTION
container(665, 767, GREEN, "FFFFFF");   // R OUTPUT

// ---- headers (measured centers, band y164..173) ------------------------------
label("INPUT", 230.5, 168.5);
label("PROJECTION", 311.5, 168.5);
label("OUTPUT", 399, 168.5);
label("INPUT", 538.5, 168.5);
label("PROJECTION", 619, 168.5);
label("OUTPUT", 698, 168.5);

// ---- small squares -----------------------------------------------------------
const SQW = 22, SQH = 42;
function square(x0, y0, w, h) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x0), y: px(y0), w: px(w || SQW), h: px(h || SQH),
    fill: { color: "FFFFFF" }, line: { color: SQRLINE, width: 1.25 },
  });
}
// L-INPUT: pair-gap-pair rhythm (edges y193/235, 248/290, 355/397, 409/451)
square(218, 193); square(218, 248); square(218, 355); square(218, 409);
// L-OUTPUT w(t) square (x391..413, y303..345)
square(391, 303);
// R-INPUT w(t) square (x547..569, y303..345)
square(547, 303);
// R-OUTPUT squares (x676..698, same rhythm as L-INPUT)
square(676, 193); square(676, 248); square(676, 355); square(676, 409);
// PROJECTION squares (vision-pinned: x305..328 / x607..630, y302..348, h46)
square(305, 302, 23, 46);
square(607, 302, 23, 46);

// ---- arrows (black 1pt, triangle head at end) --------------------------------
function arrow(x1, y1, x2, y2) {
  const o = {
    x: px(Math.min(x1, x2)), y: px(Math.min(y1, y2)),
    w: px(Math.abs(x2 - x1)), h: px(Math.abs(y2 - y1)),
    line: { color: BLACK, width: 1, endArrowType: "triangle" },
  };
  if ((x2 - x1) * (y2 - y1) < 0) o.flipV = true; // up-right / down-left
  slide.addShape(pres.ShapeType.line, o);
}
// CBOW: 4 converging (input squares' right edges -> spread points on PROJ sq left edge)
arrow(241, 214, 302, 307);
arrow(241, 269, 302, 317);
arrow(241, 376, 302, 331);
arrow(241, 430.5, 302, 342);
// CBOW: horizontal exit PROJ -> OUTPUT square
arrow(329, 323, 388, 323);
// Skip-gram: horizontal input w(t) -> PROJ square
arrow(570, 324, 604, 324);
// Skip-gram: 4 fanning (spread start points on PROJ sq right edge -> R-OUT squares)
arrow(630, 307, 676, 214.5);
arrow(630, 318, 676, 269.5);
arrow(630, 329, 676, 376);
arrow(630, 340, 676, 430.5);

// ---- word labels --------------------------------------------------------------
// left panel INPUT labels (left edge x184; measured band centers)
leftLabel("w(t-2)", 184, 213.5, HEADER);
leftLabel("w(t-1)", 184, 271, HEADER);
leftLabel("w(t+1)", 184, 378.5, HEADER);
leftLabel("w(t+2)", 184, 432, HEADER);
// left OUTPUT w(t) (right of the square, x420)
leftLabel("w(t)", 420, 323, BLACK);
// right INPUT w(t) (left of the square, x506)
leftLabel("w(t)", 506, 324, BLACK);
// right OUTPUT labels (right of the squares, x713)
leftLabel("w(t-2)", 713, 216.5, HEADER);
leftLabel("w(t-1)", 713, 271, HEADER);
leftLabel("w(t+1)", 713, 376, HEADER);
leftLabel("w(t+2)", 713, 429.5, HEADER);
// SUM over the L-PROJECTION square (measured x304..329, band y284..291)
label("SUM", 316.5, 287.5);

// ---- yellow tag boxes ---------------------------------------------------------
function tag(text, x0, x1) {
  slide.addText(text, {
    shape: pres.ShapeType.roundRect, rectRadius: 0.05,
    x: px(x0), y: px(474), w: px(x1 - x0), h: px(502 - 474),
    fill: { color: TAGFILL }, line: { color: TAGEDGE, width: 1.5 },
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 16, bold: true, color: TAGTEXT,
    lineSpacing: 19.2,
  });
}
tag("CBOW", 254, 378);
tag("Skip-gram", 551, 675);

// ---- deliverable ---------------------------------------------------------------
const OUT = path.join(__dirname, "..", "slide_022_recreated.pptx");
pres.writeFile({ fileName: OUT }).then(() => console.log("WROTE", OUT));
