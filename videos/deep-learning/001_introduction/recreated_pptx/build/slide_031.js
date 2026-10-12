// slide_031.js — 001_introduction slide 31 "Where to Get Filters for Recognition"
// (Deep Learning DSAI 308). RESUMED build: predecessor died after forensics + a
// matrix test render; this build completes the chain from the banked measurements.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_031.jpg (960x540, 1px = 1pt)
//   (scratch/forensics_031.py .. forensics12_031.py). Direct 1px=1pt mapping — the
//   certified precedent of this video (slides 001/002/005; slide_005's frame carries
//   the SAME chrome landmarks 58/43/899 and was certified with direct mapping).
// Chrome: playlist house chrome (founder directive 2026-10-11) via
//   shared_patterns/house_chrome.js — imported, NEVER re-drawn. Badge numeral 31
//   (file number; this lecture's frames carry no printed numbers — assumption
//   PENDING FOUNDER VETO, 001_introduction/AGENTS.md 2026-10-12).
//
// MEASURED SPEC (frame px):
//   title ink   x 180..778 (w 599, center 479), cap top 88, baseline 113.5
//               -> ARIAL BOLD 34.9pt. ATTEMPT-4 TYPEFACE FIX: the judge (attempt 1, MINOR)
//                  read the original title as SANS and the ink maps confirm it — 'W' and
//                  'G' at 38pt show uniform 6-7px strokes, zero serifs, flat terminals
//                  (scratch/forensics14_031.py); a Times 'W' would show flared foot
//                  serifs. forensics8 also fit sans better (relSSE 0.0141 vs 0.0209,
//                  uniform +2.7px errs = metric drift, not glyph-shape error). The spec's
//                  "serif throughout" note was wrong for the title (body/bullets ARE
//                  serif — judge confirmed, advances fit). Sans solve: 34.9pt (w 599,
//                  cap 0.716em = 25.0 vs meas 25.5).
//   content box x 98..887, y 133..367; border 2px LIGHT PERIWINKLE — modal (161,158,185),
//               chroma-doubling reconstruction (156,156,208) ~= 9999CC (NOT the spec's
//               1F1FB4 guess: text ink modal (0,0,108-119) is the navy; the border is a
//               different, pale periwinkle — PIL modal beats the spec per deck pixel law)
//   body lines  navy 000080 (modal (0,0,108..119); certified slide_005 blue), Times New
//               Roman Bold 23.5pt (forensics7 width solve 22.9-23.5 + attempt-2 closed
//               loop: at 23 all lines rendered -2.6% narrow; 23.5 pins all ink widths
//               within ~4px). Ink lefts 109/109/108/109; baselines 159.5 / 211.5 /
//               237.5 / 263.5 (x-height bottoms; L2-L3b pitch 26 = wrap/paragraph pitch,
//               L1->L2 52 = blank line, verbatim per spec)
//   bullets     red C00000 Bold TNR 23.5pt, TEXT LEFT 134 (ink-decoded: the x 135..151
//               red shape is the 'A' GLYPH of "Are" — apex 141..143 at top, legs to the
//               baseline, verified by ink map forensics13; "Are"=135..170 word-fit) —
//               attempt-3 FIX: an earlier reading mistook the 'A' for a red d16 dot and
//               indented text to 152 (caught by the stand-down peer's cross-validation +
//               forensics13 ink map). Round BLACK dots d~6.5 at (111.5, 309.5) and
//               (111.5, 348.5) (cols 109..114, rows 307..312 / 346..351, core (0,0,2)) —
//               the certified slide_005 bullet-dot pattern (black d~7 at x~110-113.5).
//               Baselines 318 / 357.
//   label box   x 377..608, y 435..477, border 9999CC ~2pt; text "Filter Parameters"
//               navy Bold ARIAL 25.5pt (forensics7 sans word-fit errs +0.4/-1.2 px vs
//               serif +2.5/-6.5; title proven sans -> same source textbox), ink left 388,
//               baseline 464.5
//   matrix box  x 623..843, y 386..504, border C00000 2pt, white fill
//   matrix ink  brackets x 634..643 / 824..833, span y 397..494, BLACK rect-style
//               (stem ~4px + ticks); theta grid: theta-ink lefts 647/718/789 (col pitch
//               71), theta glyph h 18, baselines 418/451/484 (row pitch 33); subscripts
//               hang below baseline
//   black bar   x 38..921, y 518..539 in the ORIGINAL; drawn y 518..537.5 (h 19.5) so the
//               chrome's half-visible bottom stroke stays visible and house_chrome_check.py
//               passes (2-frame-px deviation, documented — same as certified slide_005/002)
// EXCLUDED as recording artifacts (judge GROUND RULES (c) + spec brief step 11):
//   mouse cursor at the matrix box lower-right edge; PowerPoint "...ument has just been
//   saved..." tooltip at bottom-left.
//
// EQUATIONS (professional 2D law): 3x3 theta matrix. mathtext has NO matrix environment
// (genfrac test: rows compress to ~15pt pitch vs the original's 33pt — unusable), so the
// CERTIFIED mechanism from 002 slide_031/030 applies: 9 per-entry mathtext renders
// (STIX serif fs=26 black 600dpi — STIX matches the original's serif theta: glyph h 18.0
// exact at fs 26; DejaVu is wider-proportioned sans) + rect-built brackets.
// Placement: theta-ink-left + math-baseline anchoring from the sidecars
// (build/assets/eq_031_manifest.json; per-entry PNGs eq_031_theta{1..9}.png + sidecars,
// banked). The predecessor's banked eq_031_matrix_test.png (88x56pt ink vs the needed
// 200x98pt, no sidecar, unverifiable) is KEPT banked but NOT used — re-rendered instead
// per the equation law (re-render, never rescale).
//
// pptxgenjs laws: bare hex (no '#'), fontFace everywhere, margin: 0, explicit
// lineSpacing, images at EXACT sidecar size (never rescaled).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const EQ = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/eq_031_manifest.json");

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_031_recreated.pptx";

const px = (v) => v / 72; // frame px (=pt) -> inches

// palette (PIL-measured; bare hex for pptxgenjs)
const RED = "C00000";       // title, bullets, matrix box border, dots (JPEG-dark modals)
const NAVY = "000080";      // body + label text (modal (0,0,108..119))
const PERIWINKLE = "9999CC"; // content/label box borders (chroma-reconstructed modal)
const BLACK = "000000";     // matrix glyphs + brackets + bottom bar
const WHITE = "FFFFFF";

const SERIF = "Times New Roman"; // body + bullets (ink + judge confirmed)
const SANS = "Arial";            // title + label (ink maps forensics14 + forensics7)

// LO single-line baseline calibration (empirical, closed-loop): for box height H px and
// lineSpacing L pt, rendered baseline ~= top + (H - L)/2 + K*fs. K pinned per family from
// renders: Times New Roman ~0.924 (attempt-2/3 closed loop), Arial ~0.905
// (certified slide_005 empirical).
function lineTop(baselinePx, fs, Hpx, Lpt, K) {
  const k = K === undefined ? 0.924 : K; // TNR empirical (attempt-2/3 closed loop); pass 0.905 for Arial
  return baselinePx - (Hpx - Lpt) / 2 - k * fs;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "31") ----
drawHouseChrome(pres, slide, { numeral: "31" });

// ---- 2) content box (white, periwinkle border) x98..887 y133..367 ----
slide.addShape(pres.ShapeType.rect, {
  x: px(98), y: px(133), w: px(790), h: px(235),
  fill: { color: WHITE }, line: { color: PERIWINKLE, width: 1.5 },
});

// ---- 3) title — TNR Bold 38.3 C00000, ink center 479, baseline 113.5 ----
// box h 0.8in (57.6px), lineSpacing 46. ATTEMPT-4/5: Arial Bold (typeface fix per judge
// MINOR + ink maps forensics14; sans solve 34.9 -> 35.1 to pin the measured 599px
// advance). LO's Arial baseline offset differs from TNR's (attempt-4 closed loop:
// rendered +6.5 low at the k=0.905 model) -> empirical baseline target 107.0.
slide.addText("Where to Get Filters for Recognition", {
  x: px(479) - 6, y: px(lineTop(107.0, 35.1, 57.6, 46, 0.905)), w: 12, h: 0.8,
  align: "center", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 35.1, bold: true, color: RED,
  lineSpacing: 46,
});

// ---- 4) body lines — navy TNR Bold 23; single-line boxes at measured baselines ----
// box h 0.5in (36px), lineSpacing 28: top = baseline - (36-28)/2 - 0.955*23
const BODY = [
  { text: "There are Several, handcrafted filters in computer vision", left: 108, base: 159.5, w: 640 },
  { text: "For example:", left: 108, base: 211.5, w: 300 },
  { text: "Canny, Sobel, Gaussian blur, smoothing, low- level segmentation,", left: 107, base: 237.5, w: 690 },
  { text: "morphological filters, Gabor filters,...", left: 108, base: 263.5, w: 500 },
];
for (const L of BODY) {
  slide.addText(L.text, {
    x: px(L.left), y: px(lineTop(L.base, 23.5, 36, 28)), w: px(L.w), h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: SERIF, fontSize: 23.5, bold: true, color: NAVY,
    lineSpacing: 28,
  });
}

// ---- 5) bullets — red TNR Bold 23.5, text left 134, baselines 318/357; BLACK dots ----
// (attempt-3 dot fix: black d6.5 at (111.5,309.5)/(111.5,348.5) per the forensics13 ink
//  map + the certified slide_005 pattern; the red x135..151 ink is the 'A' glyph itself,
//  so the text box starts at 134 — an earlier red-d16 dot at 142.5 + text-152 reading
//  was wrong and is removed)
const BULLETS = [
  { text: "Are they optimal for recognition?", base: 318, dotCy: 309.5 },
  { text: "Can we learn them from our data?", base: 357, dotCy: 348.5 },
];
for (const b of BULLETS) {
  slide.addShape(pres.ShapeType.ellipse, {
    x: px(111.5 - 3.25), y: px(b.dotCy - 3.25), w: px(6.5), h: px(6.5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
  });
  slide.addText(b.text, {
    x: px(133.5), y: px(lineTop(b.base, 23.5, 36, 28)), w: px(420), h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: SERIF, fontSize: 23.5, bold: true, color: RED,
    lineSpacing: 28,
  });
}

// ---- 6) label box + text ----
slide.addShape(pres.ShapeType.rect, {
  x: px(377), y: px(435), w: px(232), h: px(43),
  fill: { color: WHITE }, line: { color: PERIWINKLE, width: 2 },
});
// "Filter Parameters" — navy Arial Bold 25.5, ink left 388, baseline 464.5.
// ATTEMPT-4/5: typeface fix (forensics7 sans word-fit; title proven sans -> same source
// textbox). fs 26 (25.5 rendered 2% narrow); LO Arial offset -> empirical baseline
// target 461.3 (attempt-4 rendered +3.2 low at 464.5).
slide.addText("Filter Parameters", {
  x: px(387), y: px(lineTop(461.3, 26, 36, 32, 0.905)), w: px(220), h: 0.5,
  align: "left", valign: "middle", margin: 0,
  fontFace: SANS, fontSize: 26, bold: true, color: NAVY,
  lineSpacing: 32,
});

// ---- 7) matrix box (white, red border) x623..843 y386..504 ----
slide.addShape(pres.ShapeType.rect, {
  x: px(623), y: px(386), w: px(221), h: px(119),
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// ---- 8) matrix brackets — rect-built stems+ticks (certified 002 slide-031 mechanism) ----
function bracketL(x, y0, y1, stemW, tickW, tickH) {
  const h = y1 - y0;
  slide.addShape(pres.ShapeType.rect, { x: px(x), y: px(y0), w: px(stemW), h: px(h), fill: { color: BLACK }, line: { color: BLACK, width: 0 } });
  slide.addShape(pres.ShapeType.rect, { x: px(x), y: px(y0), w: px(tickW), h: px(tickH), fill: { color: BLACK }, line: { color: BLACK, width: 0 } });
  slide.addShape(pres.ShapeType.rect, { x: px(x), y: px(y1 - tickH), w: px(tickW), h: px(tickH), fill: { color: BLACK }, line: { color: BLACK, width: 0 } });
}
function bracketR(x, y0, y1, stemW, tickW, tickH) {
  const h = y1 - y0;
  slide.addShape(pres.ShapeType.rect, { x: px(x), y: px(y0), w: px(stemW), h: px(h), fill: { color: BLACK }, line: { color: BLACK, width: 0 } });
  slide.addShape(pres.ShapeType.rect, { x: px(x + stemW - tickW), y: px(y0), w: px(tickW), h: px(tickH), fill: { color: BLACK }, line: { color: BLACK, width: 0 } });
  slide.addShape(pres.ShapeType.rect, { x: px(x + stemW - tickW), y: px(y1 - tickH), w: px(tickW), h: px(tickH), fill: { color: BLACK }, line: { color: BLACK, width: 0 } });
}
// measured: L stem x634..637 (w 3.5) ticks to 643; R stem x830..833 (w 4) ticks to 824;
// span y 397..494.5
bracketL(634, 397, 494.5, 3.5, 9.5, 2.5);
bracketR(830, 397, 494.5, 4, 10, 2.5);

// ---- 9) theta entries — 9 mathtext PNGs at EXACT sidecar size, baseline-anchored ----
for (const e of EQ.equations) {
  slide.addImage({
    path: `${ASSETS}/${e.image}`,
    x: e.x_in, y: e.y_in, w: e.w_in, h: e.h_in,
  });
}

// ---- 10) black bottom bar (over the panel; chrome bottom stroke kept visible) ----
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(518), w: px(884), h: px(19.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
