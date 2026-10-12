// slide_046.js — 001_introduction slide 46 "POOLING"
// Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_046.jpg (960x540, 1px = 1pt = 1/72 in).
//   Measurement passes: qa/slide046/measure_original{,2,3,4,5}_out.txt (banked).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral = 46 (slide file number; 001_introduction
//   originals carry no printed numbers — ASSUMPTION PENDING FOUNDER VETO, see video AGENTS.md).
//
// Measured constants (frame px):
//   title   "POOLING" ink x 403..563 (center 483), cap y 80..105 (cap-h ~25), Arial Bold
//           34.9pt solved (LSans-Bold w 161.5 vs 161; serif cap 2px short) — C00000
//   panel   white FFFFFF content panel, red C00000 border: stroke-center x 57.5..877.5,
//           y 133..456.5 (borders y 132..134 / 455..458, x 56..59 / 876..879). The original's
//           own top/left red L-lines (y 42..44 x 57..902; x 56..59 y 42..517) are this
//           frame's CHROME border (gray fill measured x 38..921 y 43..517 ≈ canonical
//           chrome x 42..918 y 45→bottom) — playlist law fixes chrome to canonical values;
//           deviation covered by judge ground rule (a) (slide_040 precedent).
//   bullets main "Aggregate multiple values into a single value" ink x 137..540 (w 404),
//           band y 151..169, baseline ~165, LSans-Reg 20.4pt solved;
//           subs 17.8pt, ink left 140, baselines 187.5 / 210.5 / 234.5 (bands
//           176..188 / 198..214 / 223..238); text color measured core (106,108,105)
//           smear-corrected -> 5E5E5E (spec 3B3B3B washed lighter by JPEG on thin strokes)
//   markers hollow circles: main d~10.5 at (116..126, 156..166); box markers d~10.5 at
//           (116..126, 259.5..270 / 292.5..303); sub markers d~8 at cx 132.5,
//           cy 182.5 / 205.5 / 229.5 — light gray 999999 stroke
//   boxes   blue-outlined option boxes, stroke-center: box1 x 107..293 y 250..276,
//           box2 x 107..293 y 284..309; border measured stroke modal reconciled to
//           333399 (halo midpoint (153,153,204)≈(170,166,227), core undershoot (35,28,106);
//           spec 3333CC washed); text LSans-Reg 20.4pt, ink left 137.5, baselines
//           268 / 302.5 (bands 254..272 / 288..307)
//   matrix  2x2 green grid x 172..242 y 336..399 (cells 35x31.5), fill 0CC850 (modal
//           (12,200,80)), black 1pt borders; letters a/b/c/d/z LSans-Bold ~18pt black,
//           baselines ~358.5 / 390.5, z baseline ~374.5
//   arrow   hollow right-block-arrow ink x 256..321 y 351..383 (w 65 h 32), white fill,
//           black outline; tip overlaps z square left edge (drawn after z, as in original)
//   pool    'Pool' Times New Roman Italic 19.9pt->20pt, ink x 370..407, band y 361..374,
//           baseline 374.5; '(' x 414..420 y 361..377; ')' x 611..617 y 361..377 (same
//           font/size — normal-size parens, NOT tall delimiters); '==' Arial ~21pt,
//           ink x 626..650 y 365..370, baseline ~371, gray 4E4E4E (measured core (98,98,98))
//   photos  large tiger x 424..610 y 325..413 (187x89), small x 670..767 y 342..389 (98x48)
//           — CROPPED from the original into build/assets/ (photos pptxgenjs cannot draw)
//   caption "Size is reduced" blue bold underlined, LSans-Bold 13.4pt, ink x 676..773
//           (center 724.5), baseline ~408, color 333399 (same reconciliation as boxes)
//   strip   black strip y 518..539 x 38..921 = video-player control bar (spec: omit;
//           judge ground rule (c)) — deliberately NOT recreated. No mouse cursor either.

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_046_recreated.pptx";
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

// ---- palette (measured) ----
const TITLE_RED = "C00000";
const PANEL_BORDER = "C00000";
const BODY_GRAY = "5E5E5E";
const MARKER_GRAY = "999999";
const BOX_BLUE = "333399";
const GREEN = "0CC850";
const BLACK = "000000";
const DIAG_DARK = "262626";
const EQ_GRAY = "4E4E4E";

const px = (v) => v / 72;

// LO single-line baseline model (validated slide_002/slide_040):
//   baseline = box_top + (box_h_px - lineSpacing)/2 + ascent * fontSize
//   ascent: Arial/Liberation Sans 0.9053em, Times/Liberation Serif 0.891em
const BOX_H = 43.2; // 0.6in boxes
function topFor(baseline, ls, size, ascent = 0.9053) {
  return baseline - (BOX_H - ls) / 2 - ascent * size;
}
// single-line text box at measured ink-left / baseline
function line(slide, text, opts) {
  const { x, baseline, size, ls = 24, fontFace = "Arial", color = BODY_GRAY,
          bold = false, italic = false, underline = false, w = 300, ascent } = opts;
  slide.addText(text, {
    x: px(x), y: px(topFor(baseline, ls, size, ascent)), w: px(w), h: 0.6,
    align: "left", valign: "middle", margin: 0,
    fontFace, fontSize: size, bold, italic, color,
    lineSpacing: ls, ...(underline ? { underline: true } : {}),
  });
}
function hollowCircle(slide, cx, cy, d, width) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: "FFFFFF" }, line: { color: MARKER_GRAY, width },
  });
}

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 46)
drawHouseChrome(pres, slide, { numeral: "46" });

// White content panel with thin red border (measured stroke-center rect)
slide.addShape(pres.ShapeType.rect, {
  x: px(57.5), y: px(133), w: px(820), h: px(323.5),
  fill: { color: "FFFFFF" }, line: { color: PANEL_BORDER, width: 1.5 },
});

// Title — Arial Bold ~35pt C00000, ink center (483, baseline 105); closed-loop
// attempt-1: rendered baseline sat +2.5 low -> param 102.5
slide.addText("POOLING", {
  x: px(51), y: px(topFor(102.5, 42, 34.9)), w: 12, h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 34.9, bold: true, color: TITLE_RED,
  lineSpacing: 42,
});

// Bullet list (main 20.4pt + three ~17.95pt subs, light-gray text, hollow markers)
// closed-loop attempt-1: subs rendered +3.5 low -> baselines -3.5; attempt-2 width
// split (sub2 +4.1 @18.0 vs sub3 -5.6 @17.8) -> 17.95 compromise
line(slide, "Aggregate multiple values into a single value",
     { x: 136, baseline: 165, size: 20.4, w: 460 });
line(slide, "Invariance to small transformations",
     { x: 139, baseline: 184, size: 17.95, w: 320 });
line(slide, "Reduces the size of the layer output/input to next layer \u2192 Faster computations",
     { x: 139, baseline: 207, size: 17.95, w: 660 });
line(slide, "Keeps most important information for the next layer",
     { x: 139, baseline: 231, size: 17.95, w: 460 });
hollowCircle(slide, 121, 161, 10.5, 1);
hollowCircle(slide, 132.5, 182.5, 8, 0.75);
hollowCircle(slide, 132.5, 205.5, 8, 0.75);
hollowCircle(slide, 132.5, 229.5, 8, 0.75);

// Option boxes (blue outline, white fill) + marker + text
slide.addShape(pres.ShapeType.rect, {
  x: px(107), y: px(250), w: px(186), h: px(26),
  fill: { color: "FFFFFF" }, line: { color: BOX_BLUE, width: 1.25 },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(107), y: px(284), w: px(186), h: px(25),
  fill: { color: "FFFFFF" }, line: { color: BOX_BLUE, width: 1.25 },
});
line(slide, "Max pooling",     { x: 137, baseline: 268,   size: 20.6, w: 200 });
line(slide, "Average pooling", { x: 136.5, baseline: 302.5, size: 20.6, w: 200 });
hollowCircle(slide, 121, 264.5, 10.5, 1);
hollowCircle(slide, 121, 297.5, 10.5, 1);

// Pooling diagram — 2x2 green matrix, block arrow, z square, Pool( photo ) == photo
function cell(x, y, w, h, letter) {
  slide.addShape(pres.ShapeType.rect, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: GREEN }, line: { color: BLACK, width: 1 },
  });
  slide.addText(letter, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 18, bold: true, color: BLACK, lineSpacing: 21,
  });
}
cell(172, 336, 35.5, 31.5, "a");
cell(207.5, 336, 35, 31.5, "b");
cell(172, 367.5, 35.5, 31.5, "c");
cell(207.5, 367.5, 35, 31.5, "d");
slide.addShape(pres.ShapeType.rect, {
  x: px(314), y: px(352), w: px(34), h: px(31),
  fill: { color: GREEN }, line: { color: BLACK, width: 1 },
});
slide.addText("z", {
  x: px(314), y: px(352), w: px(34), h: px(31),
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 18, bold: true, color: BLACK, lineSpacing: 21,
});
// block arrow over the z square's left edge (as in the original)
slide.addShape(pres.ShapeType.rightArrow, {
  x: px(256), y: px(351), w: px(65), h: px(32),
  fill: { color: "FFFFFF" }, line: { color: BLACK, width: 1 },
});
// 'Pool (' — Times New Roman Italic 20pt (attempt-1: rendered +1 low -> param 373.5)
line(slide, "Pool", { x: 369, baseline: 373.5, size: 20, w: 60,
                      fontFace: "Times New Roman", italic: true, color: DIAG_DARK, ascent: 0.891 });
line(slide, "(", { x: 413.5, baseline: 373.5, size: 20, w: 20,
                   fontFace: "Times New Roman", italic: true, color: DIAG_DARK, ascent: 0.891 });
// large tiger photo (cropped from the original frame)
slide.addImage({
  path: `${ASSETS}/tiger_large.png`,
  x: px(424), y: px(325), w: px(187), h: px(89),
});
// ')' '==' (== attempt-2: bars 5px high; LO probe calibration: bars_mid = param-11.8
// at size 24 ls 24 -> param 379.3 puts bars at 364.2..370.9 vs original 365..370)
line(slide, ")", { x: 610.5, baseline: 373.5, size: 20, w: 20,
                   fontFace: "Times New Roman", italic: true, color: DIAG_DARK, ascent: 0.891 });
line(slide, "==", { x: 625, baseline: 379.3, size: 24, color: EQ_GRAY, w: 40 });
// small tiger photo + caption
slide.addImage({
  path: `${ASSETS}/tiger_small.png`,
  x: px(670), y: px(342), w: px(98), h: px(48),
});
slide.addText("Size is reduced", {
  x: px(624.5), y: px(topFor(405, 18, 13.4)), w: 200 / 72, h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 13.4, bold: true, italic: true, color: BOX_BLUE,
  underline: true, lineSpacing: 18,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
