// slide_032.js — "Sin/Cos Positional Encoder" (Deep Learning DSAI 308, video 002, slide 32)
//
// CONTENT SPEC: analysis/slide_032_final.json (verbatim text; validated PASS_WITH_FIXES).
// Original frame: unique_slides/slide_032.jpg (960x540, 1px = 1pt at slide scale).
// Wrap points / styles / quote glyphs confirmed by gate crop-reads (scratch/slide032/read_*.txt).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): SHARED module
// videos/deep-learning/shared_patterns/house_chrome.js — drawHouseChrome(pptx, slide,
// {numeral: 32}); ml-intro house values SUPERSEDED for this playlist.
//
// FRAME->SLIDE MAPPING (identical to certified slide_002 build; re-verified on THIS
// frame 2026-10-11: border lines x 58..902, top rows 42-44, bottom rows 516-517):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
//   slide_x = (fx - 18.63)/0.96123 ; slide_y = fy/0.95556
// Badge cross-check: measured pale-yellow badge frame x 858..892 y 56..86 (center
// 875.2, 71.2) maps to slide (891.0, 74.5) vs house (893, 71) — within ~3px. OK.
//
// MEASURED SPEC (frame px -> slide pt, PIL: scratch/slide032/measure_content*.py):
//   title  ink x 336..612 y 59..74  -> slide x 330.2..618.3 (w 288.1) y 61.7..78.5
//          Verdana Bold em 18.9 (width-fit 18.92; cap-fit consistent) -> 19pt, C00000
//   sub    ink x 263..690 y 83..98  -> slide x 254.2..699.6 (w 445.4) y 86.9..103.6
//          Arial Bold em 22.08 -> 22pt; core B~108 = same navy as body (000080)
//   vector box: navy border path frame x 86..203.5 y 98..196.5 -> slide 70.1..192.3 /
//          102.6..205.7; white fill; border 000080 (core (36,28,105) JPEG-darkened).
//          NOTE: NO red border on this box (measured; spec's "red border" was the
//          big red brackets misread — frame is ground truth).
//   vector content: thin CM-style red brackets, stroke ~3.1pt + ~9.4pt serifs,
//          spanning slide y 117.2..190.5 (h 73.3); left stroke x 80.5, right stroke
//          right-edge 172.1; rows 'sin(ωt)'/'cos(ωt)' Arial Bold em 18.6 (width fit
//          18.6 = parens-span fit 18.66), ink left 95.1, baselines 142.3 / 177.9
//          (pitch 35.6). Rows are typed text IN THE ORIGINAL (Arial-look) -> built
//          as verbatim text runs; brackets via the certified mathtext->600dpi PNG
//          mechanism (scripts/render_eq.py, em 26.4, C00000) — CM bracket style
//          matches the measured stroke/serif geometry exactly.
//   callout: border path frame x 218.5..853.5 y 118..172 -> slide 207.9..868.2 /
//          123.5..180.0; fill FFFFCC, border CC6600 ~1.25pt (border core (117,89,65)
//          JPEG-darkened thin line). Text 20pt REGULAR black (em-fit 19.96 reg vs
//          18.26 bold), 2 lines (gate read): L1 'Where "t" is the step (position)
//          and ω is the frequency of trigonometric' / L2 'function Sine/Cosine';
//          "t" (with quotes) and ω RED; text left ink 216.8; baselines 148.6 / 170.5
//          (pitch 22.0).
//   main panel: navy border path frame x 74..878 y 208..507.5 -> slide 57.6..893.9 /
//          217.7..531.3; fill measured (233,254,249) = E9FEF9 (spec's E0F7FA measured
//          G too low; measured wins); border 000080 1.5pt.
//   body lines (Arial Bold, navy 000080 — all blue text cores read B~100-110 =
//          000080 JPEG-darkened; spec's 0000CC would read B~170+; frame wins):
//     L1 y 227..244 ink x 85..798  -> capTop 237.6, left 69.3,  w 741.6  (italic)
//     L2 y 292..309 text x 103..518 -> capTop 305.6, textLeft 87.8 (chevron x 84..88)
//     L3 y 324..341 x 102..783 -> capTop 339.1, left 86.9
//     L4 y 356..373 x 102..728 -> capTop 372.6, left 86.9
//     L5 y 388..405 text x 103..728 -> capTop 406.0, textLeft 87.8 (chevron 84..88)
//     L6 y 452..470 text x 102..854 -> capTop 473.0, textLeft 86.9 (chevron 84..88)
//     pitch L2..L5 = 32px = 33.5pt; blank-line gaps L1->L2, L5->L6 = 65px = 68pt.
//     Uniform em fit 19.82..19.91 -> 19.9pt all lines.
//     Highlights (5 measured, spec said 4 — measured wins): 'between -1 and 1' (L2),
//     'Distance' + '"t" and "t+1"' + 'constant' (L3), '"t" may take any positive
//     value' (L5). Greens italic (gate reads): '(bounded values)',
//     '[Distance (Pos1, Pos2) = Distance (Pos90, Pos91)]',
//     '(No limitation of length of Sequence )'. L6 red close: C00000 bold upright.
//     Chevron glyph: '›' (U+203A, gate reads) ~20pt gray 808080 on L2/L5/L6 only.
//     Quotes: curly "" per gate reads on L1/L3/L4/subtitle/callout; L5 straight ".
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (judge GROUND RULES (c), spec imagery note):
//   * white mouse cursor overlapping 'Pos91' on L4 (gate read crop_L3L4).
//   * black letterbox strip below frame row 517 (video player chrome, slide y >= 541).
//
// ATTEMPT-2 FIXES (resumed worker 2026-10-11; attempt-1 flaws caught by closed-loop self-check
// + PIL probes of render_1.png vs the original frame; render_1 kept banked as evidence):
//   1. bracket PNGs were matplotlib-C0 BLUE ('C00000' unhashed parses as cycle color) -> recolored C00000.
//   2. right bracket x was -0.102in (double /72) -> PT(163.72), ink-right 172.6.
//   3. L6 text box w 780 -> 800: the line needs ~789pt; 'Vector) ??' wrapped to a 2nd line.
//   4. callout text shifted up 2.0pt (sat ~2pt low); L2/L5 body boxes x 86.0 -> 87.9.
//   5. chevrons 20pt reg -> 16.5pt bold, ink-centered on the original's ink centers.
//   6. subtitle charSpacing 0.1 (was 3.1pt narrow).

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const NAVY = "000080";     // all blue text + box borders (measured)
const RED = "C00000";      // title, vector content, L6 warning, callout t/omega
const GREEN = "009900";
const YEL = "FFFF00";
const GRAY = "808080";
const FILL_CYAN = "E9FEF9";
const FILL_CALLOUT = "FFFFCC";
const BORDER_CALLOUT = "CC6600";
const ARIAL = "Arial";
const VERDANA = "Verdana";
const PT = (v) => v / 72;

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "32")
const s = pres.addSlide();
drawHouseChrome(pres, s, { numeral: 32 });

// ---- 2. main content panel: cyan fill + navy 1.5pt border
s.addShape(pres.ShapeType.rect, {
  x: PT(57.6), y: PT(217.7), w: PT(893.9 - 57.6), h: PT(531.3 - 217.7),
  fill: { color: FILL_CYAN }, line: { color: NAVY, width: 1.5 },
});

// ---- 3. vector box: white fill + thin navy border
s.addShape(pres.ShapeType.rect, {
  x: PT(70.1), y: PT(102.6), w: PT(192.3 - 70.1), h: PT(205.7 - 102.6),
  fill: { color: "FFFFFF" }, line: { color: NAVY, width: 1 },
});

// ---- 4. vector brackets: certified mathtext PNGs (600dpi, exact size, never rescaled)
// ATTEMPT-2 FIX: PNGs re-colored to C00000 (were rendered with matplotlib 'C00000'
// = C0 cycle blue; alpha/geometry unchanged, blue originals archived in
// scratch/slide032/bug_evidence_blue_brk/). Ink bbox inside each PNG: x 8..74,
// y 8..603 px -> ink offset 0.96pt from image left/top, ink 7.92x71.4pt.
// Placed so INK lands on the measured original: left ink-left 81.5, right
// ink-right 172.6 (prior fit 172.1 / re-measure 173.1), ink top 118.3.
// ATTEMPT-2 FIX (right bracket): x was PT(172.1)/72-0.135 = -0.102in (double /72,
// off-slide, invisible) -> PT(163.72).
s.addImage({ path: A + "eq_032_vec_brkL.png", x: PT(80.5), y: PT(117.2), w: 0.13667, h: 1.01667 });
s.addImage({ path: A + "eq_032_vec_brkR.png", x: PT(163.72), y: PT(117.2), w: 0.135, h: 1.01667 });

// ---- 5. vector rows: verbatim typed text (as in the original), Arial Bold 18.5 red
s.addText("sin(ωt)", {
  x: PT(94.5), y: PT(142.3 - 16.7), w: PT(90), h: PT(28),
  fontSize: 18.5, bold: true, color: RED, fontFace: ARIAL, margin: 0, valign: "top",
});
s.addText("cos(ωt)", {
  x: PT(94.5), y: PT(177.9 - 16.7), w: PT(90), h: PT(28),
  fontSize: 18.5, bold: true, color: RED, fontFace: ARIAL, margin: 0, valign: "top",
});

// ---- 6. definition callout: FFFFCC fill + CC6600 border
s.addShape(pres.ShapeType.rect, {
  x: PT(207.9), y: PT(123.5), w: PT(868.2 - 207.9), h: PT(180.0 - 123.5),
  fill: { color: FILL_CALLOUT }, line: { color: BORDER_CALLOUT, width: 1.25 },
});
// callout text: two single-line boxes at measured baselines (no auto pitch anywhere)
// ATTEMPT-2 FIX: both boxes shifted up 2.0pt (render sat ~2pt low vs original band).
s.addText([
  { text: "Where ", options: { color: "000000" } },
  { text: "“t”", options: { color: RED } },
  { text: " is the step (position) and ", options: { color: "000000" } },
  { text: "ω", options: { color: RED } },
  { text: " is the frequency of trigonometric", options: { color: "000000" } },
], {
  x: PT(216.3), y: PT(146.6 - 18.1), w: PT(645), h: PT(26),
  fontSize: 20, fontFace: ARIAL, margin: 0, valign: "top", align: "left",
});
s.addText("function Sine/Cosine", {
  x: PT(216.3), y: PT(168.5 - 18.1), w: PT(400), h: PT(26),
  fontSize: 20, color: "000000", fontFace: ARIAL, margin: 0, valign: "top",
});

// ---- 7. title (Verdana Bold 19 red) + subtitle (Arial Bold 22 navy), measured centers
// ATTEMPT-2 FIX: subtitle charSpacing 0.1 (render was 3.1pt narrow vs original ink width).
s.addText("Sin/Cos Positional Encoder", {
  x: PT(474.25 - 300), y: PT(56.4), w: PT(600), h: PT(30),
  align: "center", valign: "top", fontSize: 19, bold: true, color: RED, fontFace: VERDANA, margin: 0,
});
s.addText("Vector of Dimension “2” to define Position", {
  x: PT(476.9 - 300), y: PT(82.7), w: PT(600), h: PT(30),
  align: "center", valign: "top", fontSize: 22, bold: true, color: NAVY, fontFace: ARIAL, margin: 0,
  charSpacing: 0.1,
});

// ---- 8. body lines (Arial Bold 19.9 navy). Single-line boxes at measured geometry.
const bodyBox = (extra) => Object.assign({
  fontSize: 19.9, bold: true, color: NAVY, fontFace: ARIAL, margin: 0, valign: "top",
}, extra);

// L1 — italic lead-in (no marker), curly quotes, verbatim ' , ' and '....'
s.addText([
  { text: "This vector can be used to define word position at step “t” , t=0,1,2,3,4,5,6,7,....", options: { italic: true } },
], bodyBox({ x: PT(68.5), y: PT(237.6 - 3.8), w: PT(780), h: PT(30) }));

// L2 — chevron + 'Values are ' + highlighted 'between -1 and 1' + green italic
// ATTEMPT-2 FIX: chevrons 16.5pt bold, ink-centered on the original's ink centers
// (70.6, 311.85/412.35/480.35); original ink w 5.2 h 6.3 — 16.5pt gives h≈7.1 (was 8.6 at 20pt).
s.addText("›", { x: PT(68.2), y: PT(299.9), w: PT(20), h: PT(26), fontSize: 16.5, bold: true, color: GRAY, fontFace: ARIAL, margin: 0, valign: "top" });
s.addText([
  { text: "Values are ", options: {} },
  { text: "between -1 and 1", options: { highlight: YEL } },
  { text: " ", options: {} },
  { text: "(bounded values)", options: { color: GREEN, italic: true } },
], bodyBox({ x: PT(87.9), y: PT(305.6 - 3.8), w: PT(780), h: PT(30) }));

// L3 — continuation (no marker), all bold italic, three highlighted spans
s.addText([
  { text: "Distance", options: { italic: true, highlight: YEL } },
  { text: " between vectors representing positions ", options: { italic: true } },
  { text: "“t” and “t+1”", options: { italic: true, highlight: YEL } },
  { text: "  is ", options: { italic: true } },
  { text: "constant", options: { italic: true, highlight: YEL } },
], bodyBox({ x: PT(86.0), y: PT(339.1 - 3.8), w: PT(780), h: PT(30) }));

// L4 — continuation, bold italic + green bracket segment (cursor artifact omitted)
s.addText([
  { text: "irrespective of “t”  ", options: { italic: true } },
  { text: "[Distance (Pos1, Pos2) = Distance (Pos90, Pos91)]", options: { color: GREEN, italic: true } },
], bodyBox({ x: PT(86.0), y: PT(372.6 - 3.8), w: PT(780), h: PT(30) }));

// L5 — chevron + highlighted '"t" may take any positive value' (straight quotes) + green italic
s.addText("›", { x: PT(68.2), y: PT(400.4), w: PT(20), h: PT(26), fontSize: 16.5, bold: true, color: GRAY, fontFace: ARIAL, margin: 0, valign: "top" });
s.addText([
  { text: "\"t\" may take any positive value", options: { italic: true, highlight: YEL } },
  { text: " ", options: {} },
  { text: "(No limitation of length of Sequence )", options: { color: GREEN, italic: true } },
], bodyBox({ x: PT(87.9), y: PT(406.0 - 3.8), w: PT(780), h: PT(30) }));

// L6 — chevron + 'Position Vector Length = 2' + red warning close
s.addText("›", { x: PT(68.2), y: PT(468.4), w: PT(20), h: PT(26), fontSize: 16.5, bold: true, color: GRAY, fontFace: ARIAL, margin: 0, valign: "top" });
s.addText([
  { text: "Position Vector Length = 2", options: {} },
  { text: "  ", options: {} },
  { text: "(Cannot be combined with Word Embedding Vector) ??", options: { color: RED } },
// ATTEMPT-2 FIX (critical): L6 box was w=780 while the line needs ~789pt at Arial Bold 19.9 —
// 'Vector) ??' WRAPPED to a second line in the LO render. Widened to 800 (ink ends ~868 < 893.9
// panel edge; original line ink 86.7..871.1).
], bodyBox({ x: PT(86.0), y: PT(473.0 - 3.8), w: PT(800), h: PT(30) }));

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_032_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
