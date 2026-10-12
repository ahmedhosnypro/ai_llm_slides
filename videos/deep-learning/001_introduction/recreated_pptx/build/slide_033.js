// slide_033.js — 001_introduction slide 33 "Where to Get Filters for Recognition"
// (Deep Learning DSAI 308). FRESH build: two predecessor workers died on API timeouts
// with no build script / pptx; their only banked artifacts were four EXACT pixel crops
// of the original frame (build/assets/s033_{plane_upper,plane_lower,rgb_slab,mc_slab}.png
// — verified 2026-10-12 by pixel-exact correlation, err 0.00) which this build REUSES.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_033.jpg (960x540, 1px = 1pt)
//   (scratch/forensics_033.py runs). Direct 1px=1pt mapping — certified precedent of this
//   video (slides 001/002/005/031/032).
// Chrome: playlist house chrome (founder directive 2026-10-11) via
//   shared_patterns/house_chrome.js — imported, NEVER re-drawn. Badge numeral 33
//   (file number; this lecture's frames carry no printed numbers — assumption
//   PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// MEASURED SPEC (frame px):
//   title        ink x175..773 (w 599, center 474), cap top 80, baseline 105
//                -> Arial Bold 35pt C00000 (PIL width-solve: Arial 35pt = 601 vs 599;
//                TNR 35pt = 548 — sans proven; identical to certified sibling 032 title)
//   text panel   border CENTER-LINE rect x78.5..877.5, y140..266 (border ~2px periwinkle —
//                modal (160,157,188) ->
//                chroma-reconstructed 9999CC (SAME modal+reconstruction as certified
//                slide_031's content box; the spec's "blue 0000CC border" guess loses to
//                ink per deck law))
//   body lines   4 lines, TNR/Liberation Serif Bold 21pt (width solve: 21pt mean err +1.2px
//                over 13 words; cap height 14px exact; 20pt uniformly -1..-5 narrow),
//                blue 000080 (darkest cores (0,0,82..102) match certified slide_031 navy
//                (2,0,99); the spec's 0000CC guess would render cores ~(0,0,113+)).
//                Ink lefts: L1 94, L2/L3/L4 88. Baselines (x-height bottoms):
//                L1 163, L2 210, L3 233, L4 256 (pitch 23; L1->L2 47 = paragraph break).
//   COLOR RUNS   (ink wins over spec's coloring claims):
//     L1 blue "Similarly, if images are " + RED "k-D," + blue "parameters should also be "
//        + RED "k-D"   (spec's "red should also be k-D" is WRONG vs ink: red only on k-D)
//     L2 blue "For " + RED "K=3" + blue " (RGB), use  K-D filter (third dim >> K=3)"
//        (spec's "red use K-D filter" is WRONG vs ink: runs 241..368 all blue;
//        DOUBLE SPACE after "use": original gap 13px vs 7-9px normal — attempt-2
//        closed-loop word-gap solve, drift −7px without it)
//     L3 blue "For " + RED "K=9" + blue " (Satellite  images)  use 9-D filter (3"
//        + blue superscript "rd" (ink x482..492 y218..226 = w10 h8, raised 7px above
//        baseline — rendered as EXACT-BOX PNG s033_rd_sup.png: attempt-1 measured LO
//        auto-scales baseline/superscript runs to ~58% AND under-raises (bottom 229.4
//        vs 226), so the native run cannot hit the measured geometry; the certified
//        equation-law PNG mechanism is deterministic) + blue "dim = 9)" split box
//        (original gaps after "(Satellite"/"images)" are 13-14px = double spaces,
//        closed-loop drift −6px each without them)
//     L4 blue "...etc"
//   underlines   LIGHT PERIWINKLE (not text blue!) strokes y164..166 (core row 165,
//                modal (103,99,180) -> 8888CC), under "images" x205..265 and
//                "parameters" x351..453 — drawn as 1.8px rects (pptxgenjs underline
//                cannot take a different color than its run)
//   diagram panel x87..860, y306..502; red C00000 border ~1.5px, white fill
//                (spec's "x 9-90%" ≈ 86..864 confirmed; the original's OWN left chrome
//                border x58 + its red row-stubs 58..87 are the lecture's lighter chrome,
//                REPLACED by the playlist house chrome per 001_introduction/AGENTS.md —
//                same ruling as certified slides 031/032)
//   imagery      three 3D illustrations REUSED as exact crops from the original frame
//                (dispatch-sanctioned: crop non-drawable imagery at measured boxes):
//                s033_plane_upper x105..213 y345..432; s033_plane_lower x105..192
//                y433..486; s033_rgb_slab x330..494 y318..491; s033_mc_slab
//                x570..764 y343..491. The crops carry their baked-in inner labels
//                ("RGB", "3 dims", "k dims" + arrows — PIL-verified inside the boxes).
//   words        exposed handwritten labels are EXACT CROPS from the original frame
//                (attempt-3 fix after two judge FAILs: Comic-Sans substitution — bold
//                then regular — rendered strokes ~2x the original's thin pen hand, so
//                adjacent letters merged into blobs and the vision model read the
//                labels as truncated "Graysc"/"Multiple"/"Filter"; original pixels are
//                the faithful rendering, same mechanism as the slab crops and 'rd'):
//                "Grayscale" x139..273 y319..343, "Multiple channels" x608..847
//                y318..341, "Filters" x196..268 y442..455 (right tail x269..271 stays
//                with the wedge crop — verified wedge pixels, not the 's').
//   red lines    the callout lines are cropped/authentic inside the crop boxes; drawn
//                only in the gaps: line A (square->word) x213.5,419.5 -> 231.5,440;
//                thick wedge start x269..330 y436..450 as crop s033_line_wedge.png;
//                long line C x494.5,428.5 -> 569.5,421.5 (1pt C00000).
//   black bar    x38..921, y519..539 in the original; drawn y519..537.5 (h 18.5) so the
//                chrome's half-visible bottom stroke stays visible for
//                house_chrome_check.py (documented sibling deviation, slides 002/005/
//                031/032).
// EXCLUDED as spec guess loses-to-ink: the "thin red top rule y~6-8%" (PIL: NO red rows
//   y0..60 — same finding as certified slide_032) and spec background #DEDEDE (the
//   playlist chrome's white canvas + E9E9E7 panel IS the original background (232,232,230)).
//
// pptxgenjs laws: bare hex (no '#'), fontFace everywhere, margin: 0, explicit
// lineSpacing, images at EXACT px size (never rescaled).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_033_recreated.pptx";

const px = (v) => v / 72; // frame px (=pt) -> inches

// palette (PIL-measured; bare hex)
const RED = "C00000";        // title, red runs, diagram panel border, lines, Filters
const BLUE = "000080";       // body text (deck navy, darkest-core match vs slide_031)
const PERIWINKLE = "9999CC"; // text panel border (certified slide_031 reconstruction)
const UNDERLN = "8888CC";    // underline strokes (darker periwinkle, 1px core (103,99,180))
const BLACK = "000000";
const WHITE = "FFFFFF";

const SERIF = "Times New Roman"; // body (TNR metrics = Liberation Serif in LO)
const SANS = "Arial";            // title

// LO single-line baseline calibration (sibling empirical model): for box height H px,
// lineSpacing L pt: rendered baseline ~= top + (H - L)/2 + K*fs; K = 0.924 TNR (slide_031
// closed loop), 0.905 Arial (slide_005). Body: H=36, L=25, fs=21 -> top = base - 24.9.
function lineTop(baselinePx, fs, Hpx, Lpt, K) {
  const k = K === undefined ? 0.924 : K;
  return baselinePx - (Hpx - Lpt) / 2 - k * fs;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "33") ----
drawHouseChrome(pres, slide, { numeral: "33" });

// ---- 2) black bottom bar (over the panel; chrome bottom stroke kept visible) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(884), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// ---- 3) title — Arial Bold 35 C00000, ink center 474, baseline 105 ----
// box h 0.8in (57.6px), lineSpacing 40; top = 105 - (57.6-40)/2 - 0.905*35 = 64.5.
// x: advance-center 476.4 (closed loop attempt 2: ink center rendered 471.6 at box
// center 474 — bearing bias; +2.4 shift, same correction as certified sibling 032)
slide.addText("Where to Get Filters for Recognition", {
  x: px(44.4), y: px(64.5), w: 12, h: 0.8,
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 35, bold: true, color: RED,
  lineSpacing: 40,
});

// ---- 4) text panel (white, periwinkle border) — border center-line x78.5..877.5 y140..266 ----
slide.addShape(pres.ShapeType.rect, {
  x: px(78.5), y: px(140), w: px(799), h: px(126),
  fill: { color: WHITE }, line: { color: PERIWINKLE, width: 1.5 },
});

// ---- 5) body lines — TNR Bold 21, single-line boxes at measured baselines ----
// box h 0.5in (36px), lineSpacing 25 -> top = baseline - (36-25)/2 - 0.924*21
const BODY = [
  { top: lineTop(163, 21, 36, 25), left: 93, runs: [
      { text: "Similarly, if images are ", options: { color: BLUE } },
      { text: "k-D,", options: { color: RED } },
      { text: " parameters should also be ", options: { color: BLUE } },
      { text: "k-D", options: { color: RED } },
  ] },
  { top: lineTop(210, 21, 36, 25), left: 87, runs: [
      { text: "For ", options: { color: BLUE } },
      { text: "K=3", options: { color: RED } },
      { text: " (RGB), use  K-D filter (third dim >> K=3)", options: { color: BLUE } },
  ] },
  // L3 split around the superscript "rd" (rd = exact-box PNG, see header):
  //   L3a ink 88..479 ("...filter (3"), rd PNG x482..492 y218..226, L3b "dim = 9)" 499..572
  { top: lineTop(233, 21, 36, 25), left: 87, runs: [
      { text: "For ", options: { color: BLUE } },
      { text: "K=9", options: { color: RED } },
      { text: " (Satellite  images)  use 9-D filter (3", options: { color: BLUE } },
  ] },
  { top: lineTop(233, 21, 36, 25), left: 498.3, runs: [
      { text: "dim = 9)", options: { color: BLUE } },
  ] },
  { top: lineTop(256, 21, 36, 25), left: 87, runs: [
      { text: "...etc", options: { color: BLUE } },
  ] },
];
for (const L of BODY) {
  slide.addText(L.runs, {
    x: px(L.left), y: px(L.top), w: px(780), h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: SERIF, fontSize: 21, bold: true,
    lineSpacing: 25,
  });
}

// ---- 6) light-periwinkle underlines under "images" and "parameters" (L1) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(205), y: px(164), w: px(61), h: px(1.8),
  fill: { color: UNDERLN }, line: { color: UNDERLN, width: 0 },
});
slide.addShape(pres.ShapeType.rect, {
  x: px(351), y: px(164), w: px(103), h: px(1.8),
  fill: { color: UNDERLN }, line: { color: UNDERLN, width: 0 },
});

// ---- 7) diagram panel (white, red border) — border center-line x87..859.5 y306.5..501.5 ----
// 2pt: original left stroke 3px (cols 86-88), top/bottom/right ~2px (closed loop attempt 2:
// 1.25pt rendered 1.3px — too thin vs the original's 2-3px strokes)
slide.addShape(pres.ShapeType.rect, {
  x: px(87), y: px(306.5), w: px(772.5), h: px(195),
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// ---- 8) illustration crops at EXACT measured boxes (original pixels) ----
const CROPS = [
  { img: "s033_plane_upper.png", x: 105, y: 345, w: 109, h: 88 },
  { img: "s033_plane_lower.png", x: 105, y: 433, w: 88, h: 54 },
  { img: "s033_rgb_slab.png", x: 330, y: 318, w: 165, h: 174 },
  { img: "s033_mc_slab.png", x: 570, y: 343, w: 195, h: 149 },
  { img: "s033_line_wedge.png", x: 269, y: 436, w: 62, h: 15 },
];
for (const c of CROPS) {
  slide.addImage({ path: `${ASSETS}/${c.img}`, x: px(c.x), y: px(c.y), w: px(c.w), h: px(c.h) });
}

// ---- 9) red connector-line stubs in the gaps between crops (C00000 1pt) ----
// line A: from the plane crop's right edge down-right to the "Filters" word top
slide.addShape(pres.ShapeType.line, {
  x: px(213.5), y: px(419.5), w: px(18), h: px(20.5),
  line: { color: RED, width: 1 },
});
// line C: from the rgb crop's right edge up-right to the mc crop's left edge
slide.addShape(pres.ShapeType.line, {
  x: px(494.5), y: px(421.5), w: px(75), h: px(7), flipV: true,
  line: { color: RED, width: 1 },
});

// ---- 10) exposed handwritten words — EXACT crops from the original (see header) ----
slide.addImage({ path: `${ASSETS}/s033_crop_word_grayscale.png`,
  x: px(139), y: px(319), w: px(135), h: px(25) });
slide.addImage({ path: `${ASSETS}/s033_crop_word_multichannels.png`,
  x: px(608), y: px(318), w: px(240), h: px(24) });
slide.addImage({ path: `${ASSETS}/s033_crop_word_filters.png`,
  x: px(196), y: px(442), w: px(73), h: px(14) });

// ---- 11) superscript "rd" of "(3rd dim = 9)" — EXACT CROP from the original frame
// (attempt-3 fix: the probe's single-image read flagged the LANCZOS-resized glyph
// render as garbled — at 11x9px its anti-aliased edges dominate; the original's own
// pixels are the faithful rendering. Crop box x481..493 y217..227, neighbors verified
// clean: '3' ink ends x479, 'dim' starts x499.)
slide.addImage({ path: `${ASSETS}/s033_rd_sup.png`,
  x: px(481), y: px(217), w: px(13), h: px(11) });

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
