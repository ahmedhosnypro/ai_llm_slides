// slide_053.js — "Self Attention Look Ahead Mask (Used in  Decoder first Block )"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 53)
//
// CONTENT SPEC: analysis/slide_053_final.json (verbatim; PASS_WITH_FIXES applied).
// Original frame: unique_slides/slide_053.jpg (960x540). Provenance: slide_053_source/SOURCES.md
// (paper mechanism confirmed; course-authored figure; no external figure to embed).
//
// CHROME LAW (playlist, founder directive 2026-10-11): shared module
// videos/deep-learning/shared_patterns/house_chrome.js — badge numeral 53 (the number
// printed on THIS original frame; verified in-frame yellow badge top-right).
//
// FRAME->SLIDE MAPPING (measured 2026-10-11, scratch/slide053/measure_chrome.py + measure2.py):
// video 002 capture ~0.96 scale + black letterbox BELOW. Fitted from this frame's four
// chrome landmarks (left border col 58.67, right 900.51, top row 43.23, bottom 516.45):
//   slide_x = (frame_x - 18.45)/0.95991 ;  slide_y = (frame_y + 0.29)/0.95600
// Badge cross-check: frame badge center (875.0, 71.0) -> slide (891.4, 74.6) vs house
// (893, 71) — within JPEG-bbox noise (~3px), same playlist template confirmed.
//
// MEASURED FACTS baked into this build (scratch/slide053/measure4-7.py):
//  * title 2 lines, 24pt bold: L1 ink x 249.6..617.3 (center 433.5), cap top 62.6;
//    L2 ink x 249.6..595.4 (center 422.5), cap top 90.35. L2 color split MEASURED from
//    pixels: RED "(Used in  Decoder " + BLUE "first Block " + RED ")" (advance-fit puts
//    the red/blue boundary after "Decoder", x 455|463 frame — the spec's "blue Decoder"
//    is a vision-extraction error; frame is ground truth).
//  * softmax label 14pt bold red, ink left 744.4, cap top 115.9; equation box
//    (737.1, 131.1) 163.6x75.3 black 1.75pt; equation = professional 2D mathtext PNG
//    (single image, ink 751.7,141.5, 117.2x45.5pt vs measured 119.8x45.0 — within the
//    ~4pt closed-loop tolerance).
//  * diagram container (326.6, 115.4) 384.5x314.8, blue 2pt, white fill.
//  * 5 column tags: rotated 45deg CLOCKWISE (text descends L->R), ~84x18pt, centers
//    x [451.6, 495.7, 542.2, 592.6, 636.6], y 172.5; fill DCF5DC, red bold 11.5pt text.
//  * 5 row chips x 347.5 w 86.7 h 26.2, centers y [229.9, 270.7, 309.4, 351.8, 392.05].
//  * matrix (445.4, 210.9) 241.2x205.1 red 1.5pt rounded border; corner-to-corner
//    diagonal from (472.5,210.9) to (685.6,416.0) (measured color boundary); green
//    lower-left triangle DCF5DC, mauve upper-right C4ACA0 (PIL median of THIS frame's
//    wide inter-cell gaps); 5x5 grid, col pitch 48.2, row pitch 41.0; 15 lower cells:
//    yellow FFFFCC chip 20.8x13.6 + navy bold "0" (14pt); 10 upper cells: SALMON CHIP
//    E3AA8A with 7E4027 border + dark-red bold "-inf" value (11.5pt) — measured at
//    full pixel resolution 2026-10-12 (initial "solid red block" read was a red-mask
//    threshold artifact; the original DISPLAYS the -inf mask value in each cell).
//  * blue block arrow: tail rect (294.4,305.7) 19.8x12.1 + head triangle centered
//    (321.3,312.2) 14.2 deep x 19.2 tall, rotate 90, fill 0000CC.
//  * statement box (47.5,436.5) 847.9x94.4 blue 2.5pt — MEASURED: ONE box containing
//    all three text lines (left/right borders run continuously y 420..505 frame, bottom
//    border rows 506..507); the spec's "explanatory lines below the box" is a layout
//    extraction error; frame is ground truth.
//    L1 20pt bold blue, "ADDED" underlined, ink left 65.2 cap top 447.0;
//    L2 17pt bold: red 'Addition of "0" ' + navy 'does not change the original values,
//    consequently ' + red 'no effect on Softmax output' (measured run boundary x 204|213
//    and 586|594 frame);
//    L3 17pt bold: red 'Addition of "-inf" ' + navy 'gets "Zero" output of Softmax, ' +
//    red 'leaving zero attention scores for ' + red-underlined 'future' + red ' Words.'
//    (measured navy 213..450 frame, red 464..809 — wider red than the spec assumed).
//  * OMITTED as video artifacts (judge GROUND RULES (c)): black letterbox strip
//    (frame rows 517..539), mouse-cursor overlay on the matrix right edge (frame
//    x 670..700, y 270..300 — the gap it leaves in the right border is drawn continuous).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const RED = "C00000";
const BLUE = "0000CC";
const GREEN = "DCF5DC";
const MAUVE = "C4ACA0";
const CHIP_YELLOW = "FFFFCC";
const NAVY = "1F1F1F";
const FONT = "Arial";

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_053_recreated.pptx";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "53")
drawHouseChrome(pres, s, { numeral: 53 });

// ---- 2. title line 1 — 24.3pt bold red, ink center 433.5pt, cap top 62.6pt
// (24.3pt: closed-loop attempt 1 -> ink width 363.4 vs target 367.7)
s.addText("Self Attention Look Ahead Mask", {
  x: (433.5 - 216) / 72, y: (62.6 - 0.26 * 24.3) / 72, w: 6.0, h: 0.6,
  align: "center", valign: "top", margin: 0,
  fontSize: 24.3, bold: true, color: RED, fontFace: FONT,
});

// ---- 3. title line 2 — 24.3pt bold, measured red/blue split (boundary after "Decoder")
s.addText([
  { text: "(Used in  Decoder ", options: { color: RED } },
  { text: "first Block ", options: { color: BLUE } },
  { text: ")", options: { color: RED } },
], {
  x: (422.5 - 216) / 72, y: (90.35 - 0.26 * 24.3) / 72, w: 6.0, h: 0.6,
  align: "center", valign: "top", margin: 0,
  fontSize: 24.3, bold: true, fontFace: FONT,
});

// ---- 4. softmax label — 14pt bold red, ink left 744.4, cap top 115.9
s.addText("Softmax", {
  x: (744.4 - 1.0) / 72, y: (115.9 - 0.26 * 14) / 72, w: 1.3, h: 0.35,
  align: "left", valign: "top", margin: 0,
  fontSize: 14, bold: true, color: RED, fontFace: FONT,
});

// ---- 5. equation box — black 1.75pt border, white fill
s.addShape(pres.ShapeType.rect, {
  x: 737.1 / 72, y: 131.1 / 72, w: 163.6 / 72, h: 75.3 / 72,
  fill: { color: "FFFFFF" }, line: { color: "000000", width: 1.75 },
});

// ---- 6. softmax equation — professional 2D mathtext PNG (600dpi, tight+8px pad)
// \sigma(x_j)=\frac{e^{x_j}}{\sum_i e^{x_i}}  @20.7pt black; ink target (751.7, 141.5)
// rendered 120.1x46.6pt vs measured 119.8x45.0 — edges within ~2pt (closed-loop).
// 8px pad @600dpi = 0.01333in -> subtract from box origin so INK lands on target.
s.addImage({
  path: ASSETS + "/eq_053_softmax.png",
  x: 751.7 / 72 - 0.01333, y: 141.5 / 72 - 0.01333, w: 1.66833, h: 0.64667,
});

// ---- 7. diagram container — white fill, blue 2pt border
s.addShape(pres.ShapeType.rect, {
  x: 326.6 / 72, y: 115.4 / 72, w: 384.5 / 72, h: 314.8 / 72,
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 2 },
});

// ---- 8. column tags — rotated 45deg cw, 84x18pt, measured centers
const TAG_X = [451.6, 495.7, 542.2, 592.6, 636.6];
const TAG_WORDS = ["SOS", "Je", "me", "sens", "malade"];
TAG_X.forEach((cx, i) => {
  const x = (cx - 42) / 72, y = (172.5 - 9) / 72;
  s.addShape(pres.ShapeType.rect, {
    x, y, w: 84 / 72, h: 18 / 72, rotate: 45,
    fill: { color: GREEN }, line: { type: "none" },
  });
  s.addText(TAG_WORDS[i], {
    x, y, w: 84 / 72, h: 18 / 72, rotate: 45,
    align: "center", valign: "middle", margin: 0,
    fontSize: 11.5, bold: true, color: RED, fontFace: FONT,
  });
});

// ---- 9. row-label chips — rounded rects x 347.5 w 86.7 h 26.2
const CHIP_CY = [229.9, 270.7, 309.4, 351.8, 392.05];
CHIP_CY.forEach((cy, i) => {
  const y = (cy - 13.1) / 72;
  s.addShape(pres.ShapeType.roundRect, {
    x: 347.5 / 72, y, w: 86.7 / 72, h: 26.2 / 72, rectRadius: 0.08,
    fill: { color: GREEN }, line: { type: "none" },
  });
  s.addText(TAG_WORDS[i], {
    x: 347.5 / 72, y, w: 86.7 / 72, h: 26.2 / 72,
    align: "center", valign: "middle", margin: 0,
    fontSize: 11.5, bold: true, color: RED, fontFace: FONT,
  });
});

// ---- 10. matrix — base white roundRect, triangle fills, diagonal, red border on top
const MX = 445.4, MY = 210.9, MW = 241.2, MH = 205.1;         // matrix frame (slide pt)
const DXX = 472.5, DYX = 685.6;                                // diagonal x at top/bottom
s.addShape(pres.ShapeType.roundRect, {
  x: MX / 72, y: MY / 72, w: MW / 72, h: MH / 72, rectRadius: 0.08,
  fill: { color: "FFFFFF" }, line: { type: "none" },
});
// green strip left of the diagonal's top end + green lower-left triangle
s.addShape(pres.ShapeType.rect, {
  x: MX / 72, y: MY / 72, w: (DXX - MX) / 72, h: MH / 72,
  fill: { color: GREEN }, line: { type: "none" },
});
s.addShape(pres.ShapeType.rtTriangle, {
  x: DXX / 72, y: MY / 72, w: (685.6 - DXX) / 72, h: MH / 72,
  fill: { color: GREEN }, line: { type: "none" },
});
// mauve upper-right triangle (right angle at top-right)
s.addShape(pres.ShapeType.rtTriangle, {
  x: DXX / 72, y: MY / 72, w: (MX + MW - DXX) / 72, h: MH / 72,
  flipH: true, flipV: true,
  fill: { color: MAUVE }, line: { type: "none" },
});
// thin dark diagonal line (top end -> bottom-right corner)
s.addShape(pres.ShapeType.line, {
  x: DXX / 72, y: MY / 72, w: (685.6 - DXX) / 72, h: MH / 72,
  line: { color: NAVY, width: 1 },
});
// red rounded border on top (fills stop just inside it)
s.addShape(pres.ShapeType.roundRect, {
  x: MX / 72, y: MY / 72, w: MW / 72, h: MH / 72, rectRadius: 0.08,
  fill: { type: "none" }, line: { color: RED, width: 1.5 },
});

// ---- 11. 5x5 grid: yellow "0" chips (15 lower incl diagonal) + solid red blocks (10 upper)
const CCX = [469.5, 517.7, 565.9, 614.1, 662.3];   // col centers
const CCY = [231.4, 272.4, 313.4, 354.4, 395.4];   // row centers
for (let r = 0; r < 5; r++) {
  for (let c = 0; c < 5; c++) {
    const cx = CCX[c], cy = CCY[r];
    if (r >= c) {
      // lower triangle (incl diagonal): yellow chip + navy bold "0"
      s.addShape(pres.ShapeType.rect, {
        x: (cx - 10.4) / 72, y: (cy - 6.8) / 72, w: 20.8 / 72, h: 13.6 / 72,
        fill: { color: CHIP_YELLOW }, line: { color: "404040", width: 0.75 },
      });
      s.addText("0", {
        x: (cx - 18) / 72, y: (cy - 8.9) / 72, w: 0.5, h: 0.28,
        align: "center", valign: "middle", margin: 0,
        fontSize: 14, bold: true, color: NAVY, fontFace: FONT,
      });
    } else {
      // upper triangle: SALMON CHIP with dark red-brown border and a dark-red "-inf"
      // value inside (measured 2026-10-12 at full pixel resolution: chip fill E3AA8A,
      // border+value 7E4027; chip ~23.0x17.8pt; the original DISPLAYS the -inf mask
      // value — the initial "solid red block" read was a red-mask threshold artifact).
      s.addShape(pres.ShapeType.roundRect, {
        x: (cx - 11.5) / 72, y: (cy - 8.9) / 72, w: 23.0 / 72, h: 17.8 / 72, rectRadius: 0.036,
        fill: { color: "E3AA8A" }, line: { color: "7E4027", width: 1 },
      });
      s.addText("\u2212\u221E", {
        x: (cx - 10) / 72, y: (cy - 7.7) / 72, w: 20 / 72, h: 16 / 72,
        align: "center", valign: "middle", margin: 0,
        fontSize: 11.5, bold: true, color: "7E4027", fontFace: FONT,
      });
    }
  }
}

// ---- 12. blue block arrow (tail + head), tip touching the container's left border
s.addShape(pres.ShapeType.rect, {
  x: 294.4 / 72, y: 305.7 / 72, w: 19.8 / 72, h: 12.1 / 72,
  fill: { color: BLUE }, line: { type: "none" },
});
s.addShape(pres.ShapeType.triangle, {
  x: (321.3 - 9.6) / 72, y: (312.2 - 7.1) / 72, w: 19.2 / 72, h: 14.2 / 72, rotate: 90,
  fill: { color: BLUE }, line: { type: "none" },
});

// ---- 13. statement box — ONE blue-bordered box containing all three lines (measured)
s.addShape(pres.ShapeType.rect, {
  x: 47.5 / 72, y: 436.5 / 72, w: 847.9 / 72, h: 94.4 / 72,
  fill: { color: "FFFFFF" }, line: { color: BLUE, width: 2.5 },
});

// ---- 14. statement line 1 — 20pt bold blue, "ADDED" underlined
s.addText([
  { text: "Mask Values are ", options: {} },
  { text: "ADDED", options: { underline: true } },
  { text: " to Masked (Scaled) Values", options: {} },
], {
  x: (65.2 - 1.0) / 72, y: (447.0 - 0.26 * 20) / 72, w: 11.0, h: 0.4,
  align: "left", valign: "top", margin: 0,
  fontSize: 20, bold: true, color: BLUE, fontFace: FONT,
});

const LSF = 16.7;

// ---- 15. statement line 2 — 16.6pt bold, measured red/navy/red runs
// (16.6pt: closed-loop attempt 1 -> ink width 764.7 vs target 747.9 at 17pt)
s.addText([
  { text: "Addition of \u201C0\u201D ", options: { color: RED } },
  { text: "does not change the original values, consequently ", options: { color: NAVY } },
  { text: "no effect on Softmax output", options: { color: RED } },
], {
  x: (65.2 + 0.4) / 72, y: (490.9 - 0.26 * 16.7) / 72, w: 11.0, h: 0.35,
  align: "left", valign: "top", margin: 0,
  fontSize: LSF, bold: true, fontFace: FONT,
});

const LSF2 = 16.7;

// ---- 16. statement line 3 — 16.6pt bold, measured red/navy/red + underlined "future"
s.addText([
  { text: "Addition of \u201C-inf\u201D ", options: { color: RED } },
  { text: "gets \u201CZero\u201D output of Softmax, ", options: { color: NAVY } },
  { text: "leaving zero attention scores for ", options: { color: RED } },
  { text: "future", options: { color: RED, underline: true } },
  { text: " Words.", options: { color: RED } },
], {
  x: (65.2 + 0.4) / 72, y: (512.9 - 0.26 * 16.7) / 72, w: 11.0, h: 0.35,
  align: "left", valign: "top", margin: 0,
  fontSize: LSF2, bold: true, fontFace: FONT,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
