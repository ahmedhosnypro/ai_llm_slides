// slide_030.js — "Untitled" rotation-matrix derivation slide (Deep Learning DSAI 308,
// Transformers Part II — video 002, slide 30; badge numeral 30).
//
// CONTENT SPEC: analysis/slide_030_final.json (PASS_WITH_FIXES). Original frame:
// unique_slides/slide_030.jpg (960x540). SOURCES: slide_030_source/SOURCES.md
// (Kazemnejad M_{phi,k} + Vaswani §3.5 — equation-by-equation confirmed).
//
// CHROME LAW (playlist, founder 2026-10-11): shared module
// videos/deep-learning/shared_patterns/house_chrome.js — drawHouseChrome({numeral:30});
// ml-intro house values superseded. No title on this slide (spec + frame agree).
//
// FRAME->SLIDE MAPPING (derived from THIS frame's four chrome border landmarks,
// scratch/slide030/build/probe_border2.py — left core 58, right core 901, top core 43,
// bottom stroke 517 half-cut by the letterbox; b=843/877=0.96123, c=43/45=0.95556):
//   slide_x = (fx - 17.63) / 0.96123   ;  slide_y = fy / 0.95556
// Badge cross-check: frame badge yellow bbox center (875.5, 71.0) -> slide (891.5, 74.3)
// vs house (893, 71) — same ~3px JPEG-bbox bias as certified siblings 002/032. OK.
// OMITTED as video artifacts (judge GROUND RULES (c)): pen/highlighter cursor frozen
// over the 2x2 matrix top-right, black letterbox strip below the slide bottom.
//
// MEASURED SPEC (all frame px; probes measure_final/probe2-7/precheck/fixup in
// scratch/slide030/build/): FRAME WINS over the analysis JSON where they disagree —
//   * v1 vector cells are RED (like their brackets), not black (spec error).
//   * (t+delta) is yellow-highlighted in vecbox v2 cells, deriv L1 final sin(wdelta),
//     deriv L2 cos(wdelta), matrix r1c2+r2c2 (spec missed these), and the matrix
//     r2c1 highlight is GREEN (spec said yellow) — marker coding measured.
//   * deriv half 2 color-codes terms: vector entries sin(wt)/cos(wt) RED (match the
//     red vector bracket captions), matrix entries cos(wdelta)/sin(wdelta) NAVY
//     (match "Independent of Position"), first halves + = + - BLACK.
//   * blue text/borders measure navy (cores B~93-142, same signature 032 certified
//     as 000080); reds are C00000-family per the deck law.
//   * matrix box top border y333 (not 352); note box y352..473; note text = header +
//     3 blue lines (spec line 2 wraps); caption2 sits lower (y454..464) than caption1.
//   * note header "From Computer Graphics:" IS red bold italic (crop-verified;
//     first probe band missed it).
//
// EQUATIONS: professional 2D via matplotlib mathtext -> 600dpi transparent PNG ->
// addImage at EXACT size (w = px/600), colors HASHED ('#C00000','#000080','#000000')
// per the 2026-10-12 color law. Placement: ink-left + math-baseline anchoring
// (y_img = baseline_slide - baseline_frac*h_img); "=" / brace ink-top anchored.
// Tall vector/matrix brackets: rect-built stems+ticks at the measured strokes
// (certified slide-031 mechanism). Minus bars: 2px rects (measured rows 303-304 /
// 411-412; a width-fitted 4pt mathtext minus renders sub-pixel thin).
// Underbrace: PIL-drawn raster brace_030.png at exact size (certified slide-020
// mechanism; LO mis-renders rotated leftBrace presets).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const EQ = require(
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_030_manifest.json");

const ASSETS =
  "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets";

// frame(px) -> slide(pt) mapping; pt -> inch
const MX = (fx) => (fx - 17.63) / 0.96123;
const MY = (fy) => fy / 0.95556;
const IN = (pt) => pt / 72;
const PAD = 8 / 600; // render_eq transparent pad per side (in)

// palette (PIL cores; hashed hexes only for mathtext, bare for pptxgenjs)
const NAVY = "000080", RED = "C00000", BLACK = "000000";
const FILL_REMEMBER = "F9FCCF", FILL_NOTE = "F0FCE4", GREEN_BORDER = "468654";
const HL_Y = "F8FE7A", HL_G = "8DCE9B"; // measured marker bodies (avg over stroke)
const FONT = "Arial";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();

// ---- 1) house chrome (panel + badge "30") ---------------------------------------
drawHouseChrome(pres, s, { numeral: 30 });

function box(x0, y0, x1, y1, fill, line, lw) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: IN(MX(x0)), y: IN(MY(y0)), w: IN(MX(x1 + 1) - MX(x0)), h: IN(MY(y1 + 1) - MY(y0)),
    fill: { color: fill }, line: { color: line, width: lw },
  });
}
function hl(x0, y0, x1, y1, color) {
  s.addShape(pres.shapes.RECTANGLE, {
    x: IN(MX(x0)), y: IN(MY(y0)), w: IN(MX(x1 + 1) - MX(x0)), h: IN(MY(y1 + 1) - MY(y0)),
    fill: { color }, line: { color, width: 0 },
  });
}
// tall bracket: stem + inward top/bottom ticks (certified 031 mechanism, frame px)
function bracketL(x, y0, y1, color) {
  const t = 2.2, tick = 8;
  s.addShape(pres.shapes.RECTANGLE, { x: IN(MX(x)), y: IN(MY(y0)), w: IN(MX(x + t) - MX(x)), h: IN(MY(y1) - MY(y0)), fill: { color }, line: { color, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: IN(MX(x)), y: IN(MY(y0)), w: IN(MX(x + tick) - MX(x)), h: IN(MY(y0 + t) - MY(y0)), fill: { color }, line: { color, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: IN(MX(x)), y: IN(MY(y1 - t)), w: IN(MX(x + tick) - MX(x)), h: IN(MY(y1) - MY(y1 - t)), fill: { color }, line: { color, width: 0 } });
}
function bracketR(x, y0, y1, color) {
  const t = 2.2, tick = 8;
  s.addShape(pres.shapes.RECTANGLE, { x: IN(MX(x)), y: IN(MY(y0)), w: IN(MX(x + t) - MX(x)), h: IN(MY(y1) - MY(y0)), fill: { color }, line: { color, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: IN(MX(x - tick + t)), y: IN(MY(y0)), w: IN(MX(x + t) - MX(x - tick + t)), h: IN(MY(y0 + t) - MY(y0)), fill: { color }, line: { color, width: 0 } });
  s.addShape(pres.shapes.RECTANGLE, { x: IN(MX(x - tick + t)), y: IN(MY(y1 - t)), w: IN(MX(x + t) - MX(x - tick + t)), h: IN(MY(y1) - MY(y1 - t)), fill: { color }, line: { color, width: 0 } });
}
// text placed by cap-top (032 lead rule: box top = capTop - 0.22em)
function txt(str, inkLeftFrame, capTopFrame, emPx, color, opts = {}) {
  const emPt = emPx / 0.95556;
  const adv = opts.emAdv; // advance in em (measured, Arial/Liberation)
  const wPt = adv ? adv * emPt * 1.35 : 300;
  s.addText(str, {
    x: IN(MX(inkLeftFrame)), y: IN(MY(capTopFrame) - 0.22 * emPt), w: IN(wPt),
    h: IN(1.6 * emPt), align: "left", valign: "top", fontSize: Math.round(emPt * 10) / 10,
    bold: !!opts.bold, italic: !!opts.italic, color, fontFace: FONT, margin: 0,
  });
}
// equation image from manifest (baseline or ink-top anchor)
function eq(name) {
  const e = EQ[name];
  const x = IN(MX(e.ink_left_frame)) - PAD;
  const y = e.anchor === "inktop"
    ? IN(MY(e.ink_top_frame)) - PAD
    : IN(MY(e.baseline_frame)) - e.baseline_frac * (e.h_px / 600);
  s.addImage({ path: `${ASSETS}/${e.file || name}.png`, x, y, w: e.w_px / 600, h: e.h_px / 600 });
}

// ---- 2) content boxes ------------------------------------------------------------
box(90, 54, 374, 234, "FFFFFF", NAVY, 1.75);     // vector definitions
box(501, 102, 848, 185, FILL_REMEMBER, NAVY, 1.75); // Remember callout
box(87, 241, 661, 325, "FFFFFF", NAVY, 1.75);    // derivation
box(87, 333, 617, 498, "FFFFFF", NAVY, 1.75);    // matrix equation
box(623, 352, 871, 473, FILL_NOTE, GREEN_BORDER, 1.75); // computer-graphics note

// ---- 3) highlight marker rects (behind equation ink; measured bboxes) ------------
hl(304, 153, 344, 175, HL_Y);  // vecbox v2 r1 (t+delta)
hl(301, 193, 341, 215, HL_Y);  // vecbox v2 r2
hl(147, 245, 188, 267, HL_Y);  // deriv L1 (t+delta)
hl(432, 248, 492, 267, HL_G);  // deriv L1 cos(wdelta)
hl(590, 244, 651, 269, HL_Y);  // deriv L1 final sin(wdelta)
hl(154, 291, 194, 314, HL_Y);  // deriv L2 (t+delta)
hl(438, 297, 509, 314, HL_Y);  // deriv L2 cos(wdelta)
hl(584, 292, 650, 312, HL_G);  // deriv L2 final sin(wdelta)
hl(180, 355, 221, 377, HL_Y);  // matrix left vec r1 (t+delta)
hl(178, 394, 218, 416, HL_Y);  // matrix left vec r2
hl(302, 354, 374, 375, HL_G);  // matrix r1c1 cos(wdelta)
hl(390, 355, 453, 375, HL_Y);  // matrix r1c2 sin(wdelta)
hl(304, 400, 365, 420, HL_G);  // matrix r2c1 sin(wdelta)  [GREEN - measured]
hl(378, 397, 460, 419, HL_Y);  // matrix r2c2 cos(wdelta)

// ---- 4) minus bars (measured 4x2 frame-px bars; LO snaps shape rects UP ~2px,
// so the rect is drawn 1 frame-px tall -> renders ~3 rows = the original's soft
// 2-row ink at 150dpi; 2-3px-tall rects read as square dots in crop comparison) --
hl(508, 303, 511, 303, BLACK);  // deriv L2 "-" between cos(wt) and sin(wt) (ink rows 303-304)
hl(288, 411, 291, 411, BLACK);  // matrix r2c1 "-" inside the bracket (ink rows 411-412)

// ---- 5) tall brackets --------------------------------------------------------------
bracketL(242, 58, 137, RED);   bracketR(329, 58, 137, RED);    // vecbox v1 (red)
bracketL(243, 152, 229, BLACK); bracketR(359, 152, 229, BLACK); // vecbox v2 (black)
bracketL(120, 353, 430, BLACK); bracketR(236, 353, 430, BLACK); // matrix left vec
bracketL(279, 352, 431, NAVY);  bracketR(471, 352, 431, NAVY);  // 2x2 matrix (blue)
bracketL(484, 352, 431, RED);   bracketR(570, 352, 431, RED);   // matrix right vec

// ---- 6) text elements ---------------------------------------------------------------
// labels (regular, red): em from Liberation advances (7.17 / 8.31 em)
txt("Vector of Pos \u201Ct\u201D", 102, 89.2, 15.04, RED, { emAdv: 7.17 });
txt("Vector of Pos \u201Ct+\u03B4\u201D", 104, 183.2, 15.04, RED, { emAdv: 8.31 });
// remember header (bold italic navy, underlined)
txt("Remember:", 512, 112, 14.0, NAVY, { bold: true, italic: true, emAdv: 5.5 });
s.addShape(pres.shapes.RECTANGLE, { // underline (measured frame y123..124.5)
  x: IN(MX(512)), y: IN(MY(123)), w: IN(MX(590) - MX(512)), h: IN(MY(124.5) - MY(123)),
  fill: { color: NAVY }, line: { color: NAVY, width: 0 },
});
// captions (red)
txt("Vector of Pos \u201Ct+\u03B4\u201D", 98, 444.2, 15.04, RED, { emAdv: 8.31 });
txt("Vector of Pos \u201Ct\u201D", 490, 453.2, 14.78, RED, { emAdv: 7.17 });
// independent label (navy bold italic) — em 19.40: render_1 measured the ink 1.15%
// narrower than the original (dR=-4.6 @150dpi, closed-loop FAIL); +2% size closes it
txt("Independent of Position \u201Ct\u201D", 230, 481, 19.40, NAVY, { bold: true, italic: true, emAdv: 13.0 });
// note box (L1 red bold italic; L2-L4 navy bold italic)
txt("From Computer Graphics:", 634, 360.2, 16.47, RED, { bold: true, italic: true, emAdv: 12.45 });
txt("Rotation Matrix of Vector at", 633, 391.8, 17.05, NAVY, { bold: true, italic: true, emAdv: 13.02 });
txt("Pos \u201Ct\u201D with angle \u201C\u03C9\u03B4\u201D", 633, 410.6, 17.30, NAVY, { bold: true, italic: true, emAdv: 11.33 });
txt("e.g \u201C\u03C9\u201D , \u201C2\u03C9\u201D , \u201C3\u03C9\u201D , ...", 633, 436.0, 16.19, NAVY, { bold: true, italic: true, emAdv: 11.67 });

// ---- 7) equations (mathtext PNGs, exact size, baseline-anchored) --------------------
// vecbox
eq("vb1_r1"); eq("vb1_r2");
eq("vb2_r1a"); eq("vb2_r1b"); eq("vb2_r2a"); eq("vb2_r2b");
// derivation line 1
eq("d1_s1"); eq("d1_s2"); eq("d1_s3"); eq("d1_s4"); eq("d1_s5");
eq("d1_s6"); eq("d1_s7"); eq("d1_s8"); eq("d1_s9"); eq("d1_s10");
// derivation line 2 (s8 minus drawn as rect above)
eq("d2_s1"); eq("d2_s2"); eq("d2_s3"); eq("d2_s4"); eq("d2_s5");
eq("d2_s6"); eq("d2_s7"); eq("d2_s9"); eq("d2_s10");
// matrix box
eq("m_la"); eq("m_lb"); eq("m_l2a"); eq("m_l2b");
eq("m_eq"); // ink-top anchored "="
eq("m_r1c1"); eq("m_r1c2"); eq("m_r2c1"); eq("m_r2c2");
eq("m_ra"); eq("m_rb");
// remember identities
eq("rm_id1"); eq("rm_id2");

// ---- 8) underbrace (raster at exact size) + nothing else below it --------------------
eq("brace");

pres.writeFile({
  fileName:
    "videos/deep-learning/002_transformers_part2/recreated_pptx/slide_030_recreated.pptx",
}).then(() => console.log("OK slide_030_recreated.pptx"));
