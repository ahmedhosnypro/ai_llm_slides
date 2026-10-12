// slide_033.js — "Sin/Cos Positional Encoder" (Deep Learning DSAI 308, video 002, slide 33)
//
// CONTENT SPEC: analysis/slide_033_final.json (verbatim; validated PASS_WITH_FIXES, score 9).
// Original frame: unique_slides/slide_033.jpg (960x540, old extraction 68).
// Wrap points / color runs / bracket styles confirmed by gate crop-reads
// (scratch/slide033/read_eq|defs|example|pairbox|index|omega.txt, 2026-10-12).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): SHARED module
// videos/deep-learning/shared_patterns/house_chrome.js — drawHouseChrome(pptx, slide,
// {numeral: 33}); ml-intro house values SUPERSEDED for this playlist. The deck's own
// inset dark-red template frame (measured f x58..901 y43..517) is superseded by the
// shared chrome per the playlist law (precedent: certified slide_031 build).
//
// FRAME->SLIDE MAPPING (identical to certified slide_032 build; re-verified on THIS
// frame: border cols 58/901, rows 43/517; badge f(859..891, 57..84) -> slide center
// (891.0, 73.8) vs house (893, 71) — within ~3px. OK):
//   slide_x = (fx - 18.63) / 0.96123 ;  slide_y = fy / 0.95556
//
// MEASURED SPEC (slide pt; PIL scratch/slide033/measure*.py + closed-loop checks
// selfcheck_1/2 + debug1..3 on render_1/render_2):
//   title  Verdana Bold 18.8 C00000 — width-perfect (ren 325.9..610.6 vs orig 326.0..611.1)
//   sub    Arial Bold 22.2 NAVY 000080, ink center y81.45 (ren d=1.2 vs orig)
//   defs box  x426.9..771.3 y105.7..301.4 fill FCFFD6 border C00000 1.25; 6 lines left
//          ink 435.2, baselines 129.5/157.7/199.9/238.5/265.8/294.1; body 14pt (width-fit:
//          L2 31ch->240pt), bracketed lists 9pt navy; runs per read_defs + hue probes:
//          L1 red (Word/d bold, wide gap before “d” per read) + [Even Num] bold italic
//          green; L2 all red (Position/d bold); L3 purple label + bold “K”=d/2 + navy 9pt
//          list; L4 blue label + bold “i” + navy 9pt list; L5/L6 navy bold Even/Odd + blue
//          Index “i” is + green bold (Sine|Cosine) Term + red bold i=2*k(+1).
//   example box x789.0..903.4 y105.7..300.3 fill FCFFD6 border C00000; rows (ink tops)
//          121.4/149.7/188.4/226.0/254.3/282.6 = Example:, d=100, K=[0 ..49], i=[0 .. 99],
//          Sin [0,2,4,...], Cos [1,3,5,...] (2 blank gaps, read_example); ALL BOLD 15pt
//          (read: "bold-weight sans-serif"; width-fit E5 89.4pt) left ink 796.2;
//          Example: red bold italic underline; d red bold + "=100" ED7D31 (hue #b17f68);
//          K/i purple bold + blue [..] runs; Sin/Cos lines navy.
//   omega box x473.5..893 y311..534 fill E9FEF9 border NAVY 2pt; lines (row-profile
//          word segments, orig): A1 11.5pt base 328.1 left 482.1; A2 13pt base 347.0
//          left 482.1; B1 main 13.5pt base 433.0 left 488.3 + "(Used in First Pair)"
//          12pt left 736.9 (separate segment, 85pt gap in orig); B2 main 13.5 base 452.0
//          + "(Used in Last Pair)" 12pt left 727.6; Note: 12.5 bold italic underline base
//          480.0 left 487.3; C2 14pt base 501.5 left 491.4 (line starts at opening “);
//          C3 14pt base 520.3 left 491.4. Body NAVY 000080; red tokens ω/Pairs/Pair/k/d;
//          bold Largest/Smallest/NOT; ONLY bold per spec typography.
//   eq sub-box x718.2..880.5 y362.1..413.4 fill FDFDFC border C00000 rounded; internals
//          (measure11 + closed loop): omega red 25pt x731 base 390.7; K sub blue 8pt
//          x750 base 397.7; "=" two navy bars x767.1 w8.3 y383.0/388.3; BLUE fraction
//          bar x785.8 w77 y385.1 h1.4; "1" black 16 x817 base 377.6; "10,000" black 17.5
//          x786 base 406.5; "2k/d" red 12.5 x840.5 base 400.6. Colors per read_eq.
//   general pair card x76.3..172.1 y130.8..220.9 fill E1E0D6 border 7F6B59 2pt rounded
//          + shadow 655241 (+2.5 offset); red square brackets x87.2/x159.8 y140.2..211.4;
//          sin(ωt)/cos(ωt) C00000 bold 18.5 centered x123.7 baselines 158.8/199.7.
//   info box x48.2..202.2 y237.6..337.0 fill E0F8E8 border 00B050 1pt; 4 lines 14.5pt
//          (width-fit ~1.1x of 13pt render) centered x125, baselines 255.5/272.3/287.8/322.8.
//   vector pairs col x212.7 w29.4 (box4 x207.4 w47.9); fills A6D8AC/EDDDA4 alternating
//          (green,tan,green,tan,green), borders 00B050/ED7D31 1pt; values black bold
//          11.5 centered x227.4 (231.4), baselines 167.4/236.5/307.7/406/511.7.
//   pair col x315.9 w86.1; same alternation; pair formula lines = certified mathtext
//          mechanism (scripts/render_eq.py -> 600dpi transparent PNG -> addImage EXACT
//          size, never rescaled): 10 PNGs p33_* at 16.4pt width-fit to orig ink (all
//          within ~1.5pt), placed by baseline rule y_img = base - basefrac*h, centered
//          x354; green 00B050 on G boxes, orange ED7D31 on T boxes; box3 capital Sin
//          (\mathrm{Sin}); replaces pptxgenjs subscript runs (measured ~6pt too deep).
//   index strip x258.1..299.8 y127.7..535.8 fill FCFEE9 + red "]" bracket stem 305.5;
//          values red 12 centered x275, baselines 143.4/183.1/213.5/252.2/284.6/321.3/
//          357/384.1/419.6/484.5/520.1 (i,0,1,2,3,4,5,2k,2k+1,d-1-1,d-1; "5" confirmed
//          by read_index).
//   dx1 bracket "]" stem x411.1..413.4 y125.6..534.8; label dx1 red bold 13 x415.2
//          base 534.8.
//   dots: faint gray vertical triples in vec gaps (340..364, 438..462) and pair gaps
//          (276..300, 385..409).
//
// OMITTED AS VIDEO ARTIFACTS (judge GROUND RULES (c), spec imagery): mouse cursor near
//   sin(ω_k t) box (~f375,415); bottom letterbox bar f y518+.
//
// pptxgenjs laws: no '#' in hex, fontFace everywhere, margin 0, PNG equations never
// rescaled, LAYOUT_WIDE, single plain-named deliverable (SINGLE-VERSION law).

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const RED = "C00000";
const NAVY = "000080";
const BLUE = "0000CC";
const PURPLE = "7030A0";
const GREEN = "00B050";
const ORANGE = "ED7D31";
const BLACK = "000000";
const FILL_DEFS = "FCFFD6";
const FILL_OMEGA = "E9FEF9";
const FILL_EQBOX = "FDFDFC";
const FILL_INFO = "E0F8E8";
const FILL_CARD = "E1E0D6";
const BORDER_CARD = "7F6B59";
const SHADOW_CARD = "655241";
const FILL_GRN = "A6D8AC";
const FILL_TAN = "EDDDA4";
const FILL_INDEX = "FCFEE9";
const DOTS = "8C8C8C";
const ARIAL = "Arial";
const VERDANA = "Verdana";
const PT = (v) => v / 72;
const LQ = "\u201C", RQ = "\u201D", OM = "\u03C9", APX = "\u2248";

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets";
// mathtext pair-line PNGs (render_eq.py @16.4pt, 600dpi): w/h pt + baseline fraction
const EQ = {
  s0: { f: "p33_s0.png", w: 63.84, h: 17.04, bf: 0.78873 },
  c0: { f: "p33_c0.png", w: 67.80, h: 17.04, bf: 0.78873 },
  s1: { f: "p33_s1.png", w: 63.84, h: 16.92, bf: 0.79433 },
  c1: { f: "p33_c1.png", w: 67.80, h: 16.92, bf: 0.79433 },
  s2: { f: "p33_s2.png", w: 65.52, h: 16.92, bf: 0.79433 },
  c2: { f: "p33_c2.png", w: 67.80, h: 16.92, bf: 0.79433 },
  sk: { f: "p33_sk.png", w: 63.12, h: 16.92, bf: 0.79433 },
  ck: { f: "p33_ck.png", w: 67.20, h: 16.92, bf: 0.79433 },
  sdh: { f: "p33_sdh.png", w: 75.00, h: 18.00, bf: 0.74667 },
  cdh: { f: "p33_cdh.png", w: 79.08, h: 18.00, bf: 0.74667 },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const s = pres.addSlide();
drawHouseChrome(pres, s, { numeral: 33 });

// single-line text; LO first-baseline at y+0.903*fs (Arial, calibrated on render_2)
function txt(runs, x, baseline, opts) {
  const o = Object.assign({ fontSize: 12, fontFace: ARIAL, margin: 0, valign: "top" }, opts);
  const fs = o.fontSize;
  const bl = o._bl || 0.903;   // LO first-baseline factor (Arial measured 0.903; Verdana ~1.0)
  const at = Object.assign({ x: PT(x), y: PT(baseline - bl * fs), w: PT(opts._w || 300), h: PT(fs * 1.7) }, o);
  delete at._w; delete at._bl;
  s.addText(runs, at);
}
function ctxt(runs, cx, baseline, opts) {
  const w = (opts && opts._w) || 200;
  txt(runs, cx - w / 2, baseline, Object.assign({}, opts, { align: "center", _w: w }));
}

// ---- panels ------------------------------------------------------------------
s.addShape(pres.ShapeType.rect, { x: PT(426.9), y: PT(105.7), w: PT(344.4), h: PT(195.7), fill: { color: FILL_DEFS }, line: { color: RED, width: 1.25 } });
s.addShape(pres.ShapeType.rect, { x: PT(789.0), y: PT(105.7), w: PT(114.4), h: PT(194.6), fill: { color: FILL_DEFS }, line: { color: RED, width: 1.25 } });
s.addShape(pres.ShapeType.rect, { x: PT(473.5), y: PT(311.0), w: PT(419.5), h: PT(223.0), fill: { color: FILL_OMEGA }, line: { color: NAVY, width: 2 } });
s.addShape(pres.ShapeType.roundRect, { x: PT(718.2), y: PT(362.1), w: PT(162.3), h: PT(51.3), rectRadius: 0.05, fill: { color: FILL_EQBOX }, line: { color: RED, width: 1.25 } });
s.addShape(pres.ShapeType.rect, { x: PT(48.2), y: PT(237.6), w: PT(154.0), h: PT(99.4), fill: { color: FILL_INFO }, line: { color: GREEN, width: 1 } });
s.addShape(pres.ShapeType.rect, { x: PT(258.1), y: PT(127.7), w: PT(41.8), h: PT(408.1), fill: { color: FILL_INDEX }, line: { color: FILL_INDEX, width: 0 } });

// ---- general pair card (shadow behind, then card) -----------------------------
s.addShape(pres.ShapeType.roundRect, { x: PT(78.8), y: PT(133.3), w: PT(95.8), h: PT(90.1), rectRadius: 0.06, fill: { color: SHADOW_CARD }, line: { color: SHADOW_CARD, width: 0 } });
s.addShape(pres.ShapeType.roundRect, { x: PT(76.3), y: PT(130.8), w: PT(95.8), h: PT(90.1), rectRadius: 0.06, fill: { color: FILL_CARD }, line: { color: BORDER_CARD, width: 2 } });

// ---- column boxes -------------------------------------------------------------
function colBox(x, y, h, green, w) {
  s.addShape(pres.ShapeType.roundRect, {
    x: PT(x), y: PT(y), w: PT(w), h: PT(h), rectRadius: 0.05,
    fill: { color: green ? FILL_GRN : FILL_TAN },
    line: { color: green ? GREEN : ORANGE, width: 1 },
  });
}
colBox(212.7, 130.8, 59.7, true, 29.4);   // vec "0"
colBox(212.7, 203.0, 59.8, false, 29.4);  // vec "1"
colBox(212.7, 270.0, 62.8, true, 29.4);   // vec "2"
colBox(212.7, 370.5, 62.9, false, 29.4);  // vec "K"
colBox(207.4, 470.9, 62.8, true, 47.9);   // vec "[d/2]-1"
colBox(315.9, 130.8, 61.8, true, 86.1);   // pair 1
colBox(315.9, 203.0, 58.6, false, 86.1);  // pair 2
colBox(315.9, 270.0, 62.8, true, 86.1);   // pair 3
colBox(315.9, 370.5, 60.7, false, 86.1);  // pair 4
colBox(315.9, 470.9, 62.8, true, 86.1);   // pair 5

// ---- rect-built square brackets (certified slide_031 pattern: stem + ticks) ----
function bracketL(xStem, y0, y1, tick) {   // "[" — ticks point right
  const t = 2.2;
  s.addShape(pres.ShapeType.rect, { x: PT(xStem), y: PT(y0), w: PT(t), h: PT(y1 - y0), fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addShape(pres.ShapeType.rect, { x: PT(xStem), y: PT(y0), w: PT(tick), h: PT(t), fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addShape(pres.ShapeType.rect, { x: PT(xStem), y: PT(y1 - t), w: PT(tick), h: PT(t), fill: { color: RED }, line: { color: RED, width: 0 } });
}
function bracketR(xStemRight, y0, y1, tick) { // "]" — ticks point left
  const t = 2.2;
  s.addShape(pres.ShapeType.rect, { x: PT(xStemRight - t), y: PT(y0), w: PT(t), h: PT(y1 - y0), fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addShape(pres.ShapeType.rect, { x: PT(xStemRight - tick), y: PT(y0), w: PT(tick), h: PT(t), fill: { color: RED }, line: { color: RED, width: 0 } });
  s.addShape(pres.ShapeType.rect, { x: PT(xStemRight - tick), y: PT(y1 - t), w: PT(tick), h: PT(t), fill: { color: RED }, line: { color: RED, width: 0 } });
}
bracketL(87.2, 140.2, 211.4, 5);    // general pair [
bracketR(161.9, 140.2, 211.4, 5);   // general pair ]
bracketR(305.5, 127.7, 535.8, 5);   // index strip ]
bracketR(413.4, 125.6, 534.8, 5);   // dx1 ]

// ---- faint ellipsis dots (3-dot vertical clusters) -----------------------------
function dots(cx, y0, y1) {
  const n = 3, d = 2.4;
  for (let i = 0; i < n; i++) {
    const y = y0 + ((y1 - y0) * i) / (n - 1) - d / 2;
    s.addShape(pres.ShapeType.ellipse, { x: PT(cx - d / 2), y: PT(y), w: PT(d), h: PT(d), fill: { color: DOTS }, line: { color: DOTS, width: 0 } });
  }
}
dots(220.5, 340, 364);   // vec gap 2 -> K
dots(220.5, 438, 462);   // vec gap K -> [d/2]-1
dots(354, 276, 300);     // pair gap 3 -> 4
dots(354, 385, 409);     // pair gap 4 -> 5

// ---- title + subtitle ----------------------------------------------------------
s.addText("Sin/Cos Positional Encoder", {
  x: PT(468.6 - 300), y: PT(57.55 - 15), w: PT(600), h: PT(30),
  align: "center", valign: "middle", fontSize: 18.8, bold: true, color: RED, fontFace: VERDANA, margin: 0,
});
s.addText("Positional Vector with Same dimension as Embedding dimension", {
  x: PT(471.2 - 350), y: PT(81.45 - 15), w: PT(700), h: PT(30),
  align: "center", valign: "middle", fontSize: 22.2, bold: true, color: NAVY, fontFace: ARIAL, margin: 0,
});

// ---- column labels --------------------------------------------------------------
ctxt([{ text: "Vector", options: {} }], 220, 106.7, { fontSize: 10.5, color: NAVY, _w: 120 });
ctxt([{ text: "Pairs " + LQ + "K" + RQ, options: {} }], 220, 122.5, { fontSize: 10.5, color: NAVY, _w: 120 });
ctxt([{ text: "Index " + LQ + "i" + RQ, options: {} }], 281.5, 125.6, { fontSize: 11, color: RED, _w: 120 });

// ---- vector values (black bold, centered) ---------------------------------------
const VV = [["0", 167.4], ["1", 236.5], ["2", 307.7], ["K", 406.0]];
for (const [v, b] of VV) ctxt([{ text: v, options: {} }], 227.4, b, { fontSize: 11.5, bold: true, color: BLACK, _w: 60 });
ctxt([{ text: "[d/2]-1", options: {} }], 231.4, 511.7, { fontSize: 11.5, bold: true, color: BLACK, _w: 90 });

// ---- index values (red, centered) ------------------------------------------------
const IV = [["i", 143.4], ["0", 183.1], ["1", 213.5], ["2", 252.2], ["3", 284.6], ["4", 321.3],
            ["5", 357.0], ["2k", 384.1], ["2k+1", 419.6], ["d-1-1", 484.5], ["d-1", 520.1]];
for (const [v, b] of IV) ctxt([{ text: v, options: {} }], 275, b, { fontSize: 12, color: RED, _w: 90 });

// ---- general pair card text -------------------------------------------------------
ctxt([{ text: "sin(" + OM + "t)", options: {} }], 123.7, 158.8, { fontSize: 18.5, bold: true, color: RED, _w: 90 });
ctxt([{ text: "cos(" + OM + "t)", options: {} }], 123.7, 199.7, { fontSize: 18.5, bold: true, color: RED, _w: 90 });

// ---- pair column formula lines: certified mathtext PNGs (exact size, never rescaled)
function eqImg(key, baseline) {
  const e = EQ[key];
  s.addImage({
    path: ASSETS + "/" + e.f,
    x: PT(354 - e.w / 2), y: PT(baseline - e.bf * e.h),
    w: PT(e.w), h: PT(e.h),
  });
}
eqImg("s0", 153.2); eqImg("c0", 187.2);
eqImg("s1", 219.7); eqImg("c1", 256.8);
eqImg("s2", 290.3); eqImg("c2", 325.9);
eqImg("sk", 390.3); eqImg("ck", 424.8);
eqImg("sdh", 489.7); eqImg("cdh", 526.3);

// ---- info box lines (centered x125) ------------------------------------------------
ctxt([{ text: "Sin/Cos pairs", options: { bold: true } }], 125, 255.5, { fontSize: 14.5, color: BLACK, _w: 170 });
ctxt([{ text: "Vector Represents", options: {} }], 125, 272.3, { fontSize: 14.5, color: BLACK, _w: 170 });
ctxt([{ text: "Position ", options: { bold: true } }, { text: LQ + "t" + RQ, options: { bold: true, color: RED } }], 125, 287.8, { fontSize: 14.5, color: BLACK, _w: 170 });
ctxt([{ text: "Any " + LQ, options: {} }, { text: OM, options: { color: RED } }, { text: RQ + " is accepted", options: {} }], 125, 322.8, { fontSize: 14.5, color: BLACK, _w: 190 });

// ---- definitions panel (14pt body, 9pt bracketed lists) ------------------------------
txt([
  { text: "Word ", options: { bold: true, color: RED } },
  { text: "Embedding Dimension ", options: { color: RED } },
  { text: " " + LQ + "d" + RQ, options: { bold: true, color: RED } },
  { text: " ", options: {} },
  { text: "[Even Num]", options: { bold: true, italic: true, color: GREEN } },
], 435.2, 131.5, { fontSize: 13, color: BLACK, _w: 350, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Position ", options: { bold: true, color: RED } },
  { text: "Encoding Dimension  ", options: { color: RED } },
  { text: LQ + "d" + RQ, options: { bold: true, color: RED } },
], 435.2, 159.7, { fontSize: 13, color: BLACK, _w: 350, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Number of Vector Pairs " + LQ, options: { color: PURPLE } },
  { text: "K" + RQ + "=d/2", options: { bold: true, color: PURPLE } },
  { text: "  [0, 1, 2,... d/2-1]", options: { color: NAVY, fontSize: 8 } },
], 435.2, 199.9, { fontSize: 13, color: BLACK, _w: 350, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Elements Index ", options: { color: BLUE } },
  { text: LQ + "i" + RQ, options: { bold: true, color: BLUE } },
  { text: "  [0, 1, 2, ..., d-1]", options: { color: NAVY, fontSize: 8 } },
], 435.2, 238.5, { fontSize: 13, color: BLACK, _w: 350, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Even ", options: { bold: true, color: NAVY } },
  { text: "Index ", options: { color: BLUE } },
  { text: LQ + "i" + RQ, options: { bold: true, color: BLUE } },
  { text: "  is ", options: { color: BLUE } },
  { text: "Sine Term", options: { bold: true, color: GREEN } },
  { text: " ,   ", options: { color: RED } },
  { text: "i=2*k", options: { bold: true, color: RED } },
], 435.2, 265.8, { fontSize: 13, color: BLACK, _w: 350, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Odd ", options: { bold: true, color: NAVY } },
  { text: " Index ", options: { color: BLUE } },
  { text: LQ + "i" + RQ, options: { bold: true, color: BLUE } },
  { text: " is ", options: { color: BLUE } },
  { text: "Cosine Term,", options: { bold: true, color: GREEN } },
  { text: "  ", options: {} },
  { text: "i=2*k+1", options: { bold: true, color: RED } },
], 435.2, 294.1, { fontSize: 13, color: BLACK, _w: 350, fontFace: VERDANA, _bl: 1.0 });

// ---- example panel (all bold 15pt per read_example) -----------------------------------
txt([{ text: "Example:", options: { bold: true, italic: true, underline: true, color: RED } }], 796.2, 132.5, { fontSize: 15, color: BLACK, _w: 130 });
txt([{ text: "d", options: { bold: true, color: RED } }, { text: "=100", options: { color: ORANGE } }], 796.2, 161.2, { fontSize: 15, color: BLACK, _w: 130 });
txt([{ text: "K", options: { bold: true, color: PURPLE } }, { text: "=[0 ..49]", options: { color: BLUE } }], 796.2, 201.0, { fontSize: 15, color: BLACK, _w: 130 });
txt([{ text: "i", options: { bold: true, color: PURPLE } }, { text: "=[0 .. 99]", options: { color: BLUE } }], 796.2, 238.5, { fontSize: 15, color: BLACK, _w: 130 });
txt([{ text: "Sin [0,2,4,...]", options: { color: NAVY } }], 796.2, 265.8, { fontSize: 15, color: BLACK, _w: 130, charSpacing: 0.5 });
txt([{ text: "Cos [1,3,5,...]", options: { color: NAVY } }], 796.2, 294.1, { fontSize: 15, color: BLACK, _w: 130, charSpacing: 0.5 });

// ---- omega box lines (segment-accurate; body navy, red tokens) --------------------------
txt([
  { text: "Use different " + LQ, options: {} },
  { text: OM, options: { color: RED } },
  { text: RQ + " values for different " + LQ, options: {} },
  { text: "Pairs", options: { color: RED } },
  { text: RQ, options: {} },
], 482.1, 328.1, { fontSize: 11, color: NAVY, _w: 310, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Select " + LQ, options: {} },
  { text: OM, options: { color: RED } },
  { text: RQ + " Value Based on " + LQ, options: {} },
  { text: "Pair", options: { color: RED } },
  { text: RQ + " index ", options: {} },
  { text: "k", options: { color: RED } },
], 482.1, 347.0, { fontSize: 12.5, color: NAVY, _w: 310, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Largest", options: { bold: true } },
  { text: "  " + LQ, options: {} },
  { text: OM, options: { color: RED } },
  { text: RQ + " value = 1", options: {} },
], 488.3, 435.0, { fontSize: 13, color: NAVY, _w: 220, fontFace: VERDANA, _bl: 1.0 });
txt([{ text: "(Used in First Pair)", options: {} }], 736.9, 435.0, { fontSize: 11, color: NAVY, _w: 140, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: "Smallest", options: { bold: true } },
  { text: "  " + LQ, options: {} },
  { text: OM, options: { color: RED } },
  { text: RQ + " value " + APX + "  1/10000", options: {} },
], 488.3, 454.0, { fontSize: 13, color: NAVY, _w: 220, fontFace: VERDANA, _bl: 1.0 });
txt([{ text: "(Used in Last Pair)", options: {} }], 727.6, 454.0, { fontSize: 11, color: NAVY, _w: 140, fontFace: VERDANA, _bl: 1.0 });
txt([{ text: "Note:", options: { bold: true, italic: true, underline: true } }], 487.3, 482.5, { fontSize: 12, color: NAVY, _w: 100, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: LQ, options: {} },
  { text: OM, options: { color: RED } },
  { text: RQ + " Value depends on Embedding Dimension ", options: {} },
  { text: LQ, options: {} },
  { text: "d", options: { color: RED } },
  { text: RQ + " ONLY", options: { bold: true } },
], 491.4, 503.0, { fontSize: 13, color: NAVY, _w: 400, fontFace: VERDANA, _bl: 1.0 });
txt([
  { text: LQ, options: {} },
  { text: OM, options: { color: RED } },
  { text: RQ + " Value does ", options: {} },
  { text: "NOT", options: { bold: true } },
  { text: " depend on Sequence Length", options: {} },
], 491.4, 521.9, { fontSize: 13, color: NAVY, _w: 400, fontFace: VERDANA, _bl: 1.0 });

// ---- boxed equation (measured internals; stacked fraction = real bar) -------------------
txt([{ text: OM, options: {} }], 731.0, 390.7, { fontSize: 25, color: RED, _w: 40 });
txt([{ text: "K", options: {} }], 750.0, 397.7, { fontSize: 8, color: NAVY, _w: 20 });
s.addShape(pres.ShapeType.rect, { x: PT(767.1), y: PT(382.4), w: PT(8.3), h: PT(1.2), fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
s.addShape(pres.ShapeType.rect, { x: PT(767.1), y: PT(387.9), w: PT(8.3), h: PT(1.2), fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
s.addShape(pres.ShapeType.rect, { x: PT(785.8), y: PT(384.9), w: PT(77.0), h: PT(1.4), fill: { color: NAVY }, line: { color: NAVY, width: 0 } });
txt([{ text: "1", options: {} }], 817.0, 377.6, { fontSize: 16, color: BLACK, _w: 20 });
txt([{ text: "10,000", options: {} }], 786.0, 406.5, { fontSize: 17.5, color: BLACK, _w: 80 });
txt([{ text: "2k/d", options: {} }], 840.5, 400.6, { fontSize: 12.5, color: RED, _w: 40 });

// ---- dx1 label ---------------------------------------------------------------------------
txt([{ text: "dx1", options: {} }], 415.2, 534.8, { fontSize: 13, bold: true, color: RED, _w: 60 });

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_033_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
