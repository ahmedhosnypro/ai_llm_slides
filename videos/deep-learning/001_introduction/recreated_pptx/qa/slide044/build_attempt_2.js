// slide_044.js — 001_introduction slide 44 "Solution? Zero-padding! , Others !!"
// Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_044.jpg (960x540, 1px = 1pt = 1/72 in).
//   Measurement passes: qa/slide044/measure1..10_out.txt + crops (banked).
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn. Badge numeral 44 (slide file number; 001_introduction
//   originals carry no printed numbers — ASSUMPTION PENDING FOUNDER VETO, video AGENTS.md).
//
// MEASURED SPEC (frame px):
//   title    "Solution? Zero-padding! , Others !!" ink x 211..751 (center 481, w 541),
//            cap top 68, baseline ~92.5, cap 24.5 — SANS bold (crop: no serifs);
//            metric solve: Calibri Bold 37.7 (advance 543 vs 541, cap 24.8 vs 24.5;
//            row-IoU 0.884 + per-word IoU win; coherent with the decisively-solved
//            Calibri bullet). Red C00000 (deck standard).
//   frame    inner content frame stroke-centers x 77..885, y 122..386 (w 808, h 264),
//            white fill, red C00000 ~2pt border.
//   bullet   band y 136..157, baseline 150. Open ring x 111..125 y 141..150 (tan ring,
//            darkest core (198,179,147) -> B39A6E). Words CALIBRI (Carlito) 23.5pt
//            (per-word size solve spread 0.5 vs Arial 3.8 — decisive), black, ink lefts:
//            For 136 / surround 243 / the 340 / image 380 / with 445 / and 607 /
//            layers 766 / of 828 / 0 855. Math tokens (serif-italic in the original,
//            Cambria-Math-like): "s = 1," ink 173..234; "(h_f-1)/2" ink 496..~592;
//            "(w_f-1)/2" ink 651..756; band tops 136, subscript bottoms 156/157.
//            Rendered per the professional-2D law: mathtext -> 600dpi transparent PNG
//            (scripts/render_eq.py), size-solved to the measured ink widths
//            (build/assets/eq_044_*.png + eq_044_manifest.json), placed by
//            ink-left + baseline anchoring (sidecar baseline_frac).
//   grid7    7x7 x 101..378, y 173..383 (cw 39.571, ch 30). CANONICAL fills per
//            corner-sampled classification (measure8): cyan ring r1/r7/c1/c7,
//            green interior — the spec's "R2C5/R2C6 cyan anomaly" was a vision
//            misread; frame is ground truth. Cyan modal (14,191,233)=0EBFE9,
//            green (14,202,82)=0ECA52. Hairline boundaries: sage-mush modals
//            -> 9CC284 @0.5pt. Numerals Arial Bold 17pt (digit cap 12.2 vs
//            measured 12), black, ink-centered per cell.
//            values: 0000000/0111000/0011100/0001110/0001100/0011000/0000000
//   filter   3x3 x 440..527, y 247..313 (cw 29, ch 22), all yellow (247,255,10)~F8FF0A,
//            hairline C0F070 @0.5pt, numerals Arial Bold 13.5pt. values 001/011/111
//   out5     5x5 x 622..820, y 203..354 (cw 39.6, ch 30.2), all green 0ECA52,
//            hairline 84A468 @0.5pt, numerals Arial Bold 17pt.
//            values 11200/01110/00121/10210/01130 (re-derived from the frame crops —
//            match the spec; SOURCES.md discrepancy is about arithmetic, not reading)
//   ops      '*' ink 7x7 at (407..413, 278..284); '=' ink 14x6 at (546..559, 276..281);
//            both rendered as mathtext PNGs (squat math glyphs), ink-center placed.
//   notebox  stroke-centers x 77..672.5, y 393..509 (w 595.5, h 116), white fill,
//            border 9593AB 1pt (measured stroke cores (140,140,168)..(157,156,174) —
//            muted lavender family, NOT the spec's 4472C4; PIL modal beats spec).
//            Text Times New Roman 21pt (serif solve: L1..L4 sizes 21.7/20.9/21.2/20.7
//            — consistent; sans alternative scattered), color 181054 (dark-ink modal
//            (24,16,80..96) + bold-stem (0,0,96)), L1 bold. Ink lefts 88/89/90/88,
//            baselines 418.5/445.5/472.5/499.5 (pitch 27).
//            VERBATIM per frame (spec missed it): L3 = "...of size 3x3 , output..."
//            (space BEFORE the comma; serif width solve: 500px with it vs 495 without,
//            target 500).
//   excluded recording artifacts (judge GROUND RULES (c) + spec brief steps 11/12):
//            mouse cursor x 560..614 y 378..392; full-width black bar y 519..539
//            (video-player progress bar — slide_040 precedent: deliberately omitted).
//            NO gray top line exists in this frame (rows 0..7 white, measured).
//   chrome   canonical playlist chrome drawn (panel x 42..918, y 45..bottom, badge at
//            (893,71) numeral 44); the ORIGINAL frame's own panel border sits at x~58,
//            y~43 with a faint right border — covered by judge ground rule (a),
//            same as certified slides 005/031/040.
//
// pptxgenjs laws: bare hex (no '#'), fontFace everywhere, margin: 0, explicit
// lineSpacing on every multi-line-capable box, images at EXACT sidecar size
// (never rescaled).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_044_recreated.pptx";
const EQ = require(ASSETS + "/eq_044_manifest.json");

const px = (v) => v / 72; // frame px (=pt) -> inches

// ---- palette (PIL-measured, bare hex) ----
const RED = "C00000";      // title + inner frame border (deck standard)
const CYAN = "0EBFE9";     // padding cells (modal (14,191,233))
const GREEN = "0ECA52";    // image/output cells (modal (14,202,82))
const YELLOW = "F8FF0A";   // filter cells (modal (247,255,10))
const BLACK = "000000";    // numerals, bullet words, math tokens
const RING = "B39A6E";     // bullet open-ring (darkest core (198,179,147) + AA)
const LINE_7 = "9CC284";   // 7x7 hairline (sage mush modal)
const LINE_F = "C0F070";   // 3x3 hairline (pale yellow-green modal)
const LINE_O = "84A468";   // 5x5 hairline (olive modal (128,163,97) lightened)
const NOTE_BORDER = "9593AB"; // notebox border (stroke cores 140..157 gray-lavender)
const NOTE_TEXT = "181054";   // note text (dark-ink modal (24,16,84))

// LO single-line baseline model: rendered baseline ~= top + (H - L)/2 + K*fs
// K = font hhea ascent/em: Carlito 0.917, Liberation Serif 0.891, Liberation Sans 0.905.
// (K pinned per-font from the attempt-1 closed-loop render if needed.)
const K_CARL = 0.917, K_TNR = 0.891, K_AR = 0.905;

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- 1) playlist house chrome (white canvas, gray panel + red border, badge "44") ----
drawHouseChrome(pres, slide, { numeral: "44" });

// ---- 2) title — Calibri Bold 37.7 C00000, ink center 481, baseline 92.5 ----
// box h 0.6in (43.2px), lineSpacing 42: top = 92.5 - (43.2-42)/2 - 0.917*37.7 = 57.3
slide.addText("Solution? Zero-padding! , Others !!", {
  x: px(481) - 6, y: px(57.3), w: 12, h: 0.6,
  align: "center", valign: "middle", margin: 0,
  fontFace: "Calibri", fontSize: 37.7, bold: true, color: RED,
  lineSpacing: 42,
});

// ---- 3) inner content frame x 77..885 y 122..386, white, red 2pt ----
slide.addShape(pres.ShapeType.rect, {
  x: px(77), y: px(122), w: px(808), h: px(264),
  fill: { color: "FFFFFF" }, line: { color: RED, width: 2 },
});

// ---- 4) grids (per-cell rects + centered numerals) ----
// NUMERAL BASELINE LAW (closed-loop, render_1 evidence 2026-10-12): with an
// exact lineSpacing == box height (H = L = ch), LibreOffice places the glyph
// baseline at box_top + L − descent·fs — NOT the K-model (H−L)/2 + K·fs used
// in attempt 1 (that model only coincides with LO when K·fs ≈ L − descent·fs,
// as in the bullet box). Empirical offsets measured on render_1's UNCLIPPED
// bottom-row digits (qa/slide044/measure-digit-fix probe):
//   g77 17pt/ch30: baseline − box_top = 26.5   (descent 3.5 = 0.206em)
//   o55 17pt/ch30.2: 26.1                      f33 13.5pt/ch22: 18.5
// Desired baselines = ORIGINAL frame digit ink bottoms: g77 cy+19.5,
// o55 cy+20.3, f33 cy+14.5 (measure6: ink 182..193 / 213..224 / 253..262 etc).
// Attempt-1 bug: digits sat ~11 fpx low and the next row's cell rect CLIPPED
// their lower half (see qa/slide044/crop_render_g77_top.png).
function drawGrid(x0, y0, n, m, cw, ch, fillFn, lineColor, values, numSize, baseDelta, baseOff) {
  for (let r = 0; r < m; r++) {
    for (let c = 0; c < n; c++) {
      const cx = x0 + c * cw, cy = y0 + r * ch;
      slide.addShape(pres.ShapeType.rect, {
        x: px(cx), y: px(cy), w: px(cw), h: px(ch),
        fill: { color: fillFn(r, c) }, line: { color: lineColor, width: 0.5 },
      });
      // numeral: box h = ch, lineSpacing = ch -> LO baseline = top + baseOff
      // top = (cy + baseDelta) − baseOff ; digit ink (baseline−cap..baseline)
      // stays inside the cell, so no later row rect can clip it.
      const top = cy + baseDelta - baseOff;
      slide.addText(values[r][c], {
        x: px(cx), y: px(top), w: px(cw), h: px(ch),
        align: "center", valign: "middle", margin: 0,
        fontFace: "Arial", fontSize: numSize, bold: true, color: BLACK,
        lineSpacing: ch,
      });
    }
  }
}
const isRing = (r, c) => r === 0 || r === 6 || c === 0 || c === 6;
const G77 = ["0000000", "0111000", "0011100", "0001110", "0001100", "0011000", "0000000"];
drawGrid(101, 173, 7, 7, 277 / 7, 30, (r, c) => (isRing(r, c) ? CYAN : GREEN), LINE_7, G77, 17, 19.5, 26.5);
const F33 = ["001", "011", "111"];
drawGrid(440, 247, 3, 3, 29, 22, () => YELLOW, LINE_F, F33, 13.5, 14.5, 18.5);
const O55 = ["11200", "01110", "00121", "10210", "01130"];
drawGrid(622, 203, 5, 5, 198 / 5, 30.2, () => GREEN, LINE_O, O55, 17, 20.3, 26.1);

// ---- 5) operators — mathtext PNGs, ink-center placed ----
// ast ink 7.1x7.6pt centered at (410, 281); eq ink 12.7x5.9pt centered at (552.5, 278.5)
slide.addImage({
  path: `${ASSETS}/eq_044_ast.png`,
  x: px(410 - EQ.eq_044_ast.ink_w / 2), y: px(281 - EQ.eq_044_ast.ink_h / 2),
  w: EQ.eq_044_ast.sidecar.w_in, h: EQ.eq_044_ast.sidecar.h_in,
});
slide.addImage({
  path: `${ASSETS}/eq_044_eq.png`,
  x: px(552.5 - EQ.eq_044_eq.ink_w / 2), y: px(278.5 - EQ.eq_044_eq.ink_h / 2),
  w: EQ.eq_044_eq.sidecar.w_in, h: EQ.eq_044_eq.sidecar.h_in,
});

// ---- 6) bullet line — Calibri 23.5 words + 3 math PNGs, shared baseline 150 ----
// single-line boxes h 0.4in (28.8px), lineSpacing 28:
// top = 150 - (28.8-28)/2 - 0.917*23.5 = 128.05
const BULLET_TOP = 150 - (28.8 - 28) / 2 - K_CARL * 23.5;
const WORDS = [
  ["For", 136], ["surround", 243], ["the", 340], ["image", 380], ["with", 445],
  ["and", 607], ["layers", 766], ["of", 828], ["0", 855],
];
for (const [t, left] of WORDS) {
  slide.addText(t, {
    x: px(left - 1), y: px(BULLET_TOP), w: px(140), h: 0.4,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Calibri", fontSize: 23.5, color: BLACK, lineSpacing: 28,
  });
}
// math tokens: x_img = (ink_left - pad 8px@600dpi)/72; y_img = 150/72 - bf*h_in
for (const [key, inkLeft] of [["eq_044_s1", 173], ["eq_044_htok", 496], ["eq_044_wtok", 651]]) {
  const e = EQ[key];
  slide.addImage({
    path: `${ASSETS}/${key}.png`,
    x: px(inkLeft - 8 / 600 * 72),
    y: 150 / 72 - e.sidecar.baseline_frac * e.sidecar.h_in,
    w: e.sidecar.w_in, h: e.sidecar.h_in,
  });
}
// open ring bullet x 111..125, y 141..150
slide.addShape(pres.ShapeType.ellipse, {
  x: px(111), y: px(141), w: px(14.5), h: px(9.5),
  fill: { color: "FFFFFF", transparency: 100 }, line: { color: RING, width: 1 },
});

// ---- 7) note box x 77..672.5 y 393..509, white, lavender 1pt ----
slide.addShape(pres.ShapeType.rect, {
  x: px(77), y: px(393), w: px(595.5), h: px(116),
  fill: { color: "FFFFFF" }, line: { color: NOTE_BORDER, width: 1 },
});

// ---- 8) note text — TNR 21pt navy, L1 bold, single-line boxes at measured baselines ----
// box h 0.5in (36px), lineSpacing 27. render_1 closed loop: the K-model put the
// ink bands ~2.4 fpx low (LO law: baseline = top + (H−L)/2 + L − descent·fs);
// shift all four boxes up 2.4 fpx -> top = B − 23.21 − 2.4 = B − 25.61
const NOTE_LINES = [
  { text: "Original 5x5", bold: true, left: 88, base: 418.5 },
  { text: "After padding ONE  pixel (surrounding the image) it will be 7x7", bold: false, left: 89, base: 445.5 },
  { text: "After apply one filter  of size 3x3 , output will be 5x5 again", bold: false, left: 90, base: 472.5 },
  { text: "Do the same for next applied filter", bold: false, left: 88, base: 499.5 },
];
for (const L of NOTE_LINES) {
  slide.addText(L.text, {
    x: px(L.left - 1), y: px(L.base - 25.61), w: px(600), h: 0.5,
    align: "left", valign: "middle", margin: 0,
    fontFace: "Times New Roman", fontSize: 21, bold: L.bold, color: NOTE_TEXT,
    lineSpacing: 27,
  });
}

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
