// Build slide 036 — "Problem Formulation"
// Deck: videos/machine-learning/03_ridger_regression_gradient_descent (house chrome = shared_patterns/house_chrome.js)
// Ground truth: unique_slides/slide_036.jpg (960x540, 1px = 1pt = 1/72 in).
// Content: Title + badge + 4 bordered content boxes with left-aligned text, one centered equation, red X mark.
// MEASURED geometry (frame px -> inches via /72):
//   Title "Problem Formulation": ink x=354..628 (center 491), y=64..84
//   Badge: center (876,73) d=35, numeral "36"
//   Panel: x=54..903, y=45..540 (house chrome, E9E9E7 fill, C00000 strokes L/R/bottom, NO top)
//   Box 1: borders y=94, y=212; text lines y=101..116, 127..146, 158..172, 187..202; x=79..435
//   Box 2: borders y=212/226, y=314; text lines y=231..248, 259..278, 288..306; x=81..646
//   Box 3: borders y=328/329, y=421/437; text lines y=338..353, 369..396, 402..410; x=79..780
//   Box 4: borders y=437, y=539; text lines y=442..455, 468..486, 494..512; x=80..846
//   Red X mark in box 3: x=771..778, y=369..382
//   Colors: box border A60000, fill F7F7F7; text black; class I green 008000; Class II blue 0000FF;
//           d(X) red C00000; inequalities blue 0000FF; misclassified/Error/delta_i underlined;
//           summation subscript + trailing phrase red C00000; implication arrows + delta_i red C00000.
// Font sizes fit from ink widths via Arial (Liberation Sans metric):
//   Title: ink w=275px -> ~44pt (from slide_035 calibration)
//   Box body: ink w up to 767px (box 4 line 2) -> ~14-16pt depending on line length
//   Equation: rendered as mathtext PNG (18pt, red C00000)
//   Red X: large standalone, ~36pt bold red FF0000

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("../../shared_patterns/house_chrome.js");
const fs = require("fs");

const OUT = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/slide_036_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

// Equation asset (generated via render_eq.py)
const EQ_ERROR = {
  path: "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/build/assets/eq_036_error.png",
  w_in: 8.10333,
  h_in: 0.55167,
  baseline_frac: 0.93353,
};

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pptx.addSlide();

// House chrome: white canvas, E9E9E7 panel, C00000 L/R/bottom strokes (NO top),
// badge circle with numeral 36 (file number = printed number; no zero-padding).
drawHouseChrome(pptx, slide, { numeral: 36 });

// --- Title: "Problem Formulation" ---
// ink bbox: x=354..628 (w=275, center=491), y=64..84 (h=21, center=74)
// From slide_035: LO ink center ~1.2px left of box center -> box center = 492.2 -> x=71.2 (w=820)
// Baseline at y=74: slide_035 lineSpacing 54, ascent 40.73, halfLead 1.87, LO offset +1.6
// -> baseline = top + 44.2 => top = 74 - 44.2 = 29.8px? But title is above panel (y<45).
// Title is in the TOP margin (y=64..84, panel starts at y=45).
// Wait: the title in this deck is at y=4%-14% of frame (21.6..75.6px). My measurement: y=64..84.
// This is partially in the panel area (panel starts at y=45). The house chrome from slide_003
// has panel at y=45..540. The title must be rendered in the TOP MARGIN above the panel.
// Let me use the frame coordinates directly.
// Frame height 540px = 7.5in. Title y=64..84 -> center ~74px = 1.028in from top.
// slide_035 had title at y=166.8px (2.317in) for a larger 45pt font.
// For ~44pt, baseline at y=74px (1.028in): lineSpacing ~54, top = 74 - 44.2 = 29.8px (0.414in).
slide.addText("Problem Formulation", {
  x: px(71.2), y: px(29.8), w: px(820), h: px(70),
  align: "center", valign: "top", margin: 0,
  fontFace: "Arial", fontSize: 44, bold: true, color: "C00000",
  lineSpacing: 54,
});

// --- Content boxes: draw border rect + fill, then add text ---
// Panel left edge: x=54px (0.75in). Boxes span x=54..903 (850px = 11.806in).
// Measured box borders at x=58 (left stroke of house) and x=901 (right stroke).
// But boxes have their own border A60000 at x=58/59 and x=870/871? Wait - the house strokes
// are at x=58 and x=901. The box borders are at x=58/59 (left) and x=870/871 (right).
// Actually my measurement: vertical reddish at x=58 (house left), x=68 (box 1 left?),
// x=870 (box right), x=901 (house right). The boxes share the house left/right strokes?
// No - the house panel IS the gray background E9E9E7. The boxes are drawn ON the panel
// with their own A60000 borders and F7F7F7 fill.
// The box left border aligns with house left stroke (x=58/59), right border at x=870/871
// (well inside the house right stroke at x=901).
// So box x range: 58..871 (813px = 11.292in). Fill inside: x=59..870 (812px).
// But panel is x=54..903. So boxes are inset 4px from panel left, 32px from panel right.

const BOX_LEFT = 59;   // fill starts at 59 (1px inside left border at 58)
const BOX_RIGHT = 870; // fill ends at 870 (1px inside right border at 871)
const BOX_W = BOX_RIGHT - BOX_LEFT; // 811px = 11.264in
const BOX_X = px(BOX_LEFT);

// Box vertical positions (measured border y's):
// Box 1: y=94 (top border) .. y=212 (bottom border) -> content y=95..211
// Box 2: y=226 (top border) .. y=314 (bottom border) -> content y=227..313
// Box 3: y=329 (top border) .. y=437 (bottom border) -> content y=330..436
// Box 4: y=437 (top border) .. y=539 (bottom border) -> content y=438..538

function drawBox(slide, yTop, yBottom, fillColor, borderColor) {
  const h = yBottom - yTop;
  // border rect (A60000) at yTop..yBottom, x=58..871
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(58), y: px(yTop), w: px(813), h: px(h),
    fill: { color: fillColor }, line: { color: borderColor, width: 1 },
  });
}

// Box fills: F7F7F7 (light gray), borders: A60000 (dark red)
drawBox(slide, 94, 212, "F7F7F7", "A60000");   // Box 1
drawBox(slide, 226, 314, "F7F7F7", "A60000");  // Box 2
drawBox(slide, 329, 437, "F7F7F7", "A60000");  // Box 3
drawBox(slide, 437, 539, "F7F7F7", "A60000");  // Box 4

// --- Box 1 text (y=101..202) ---
// 4 lines, left-aligned. Font size from ink widths: line 1 ink w=337px at 14pt? 
// Line 1: "Define two classes: class I and Class II"
// Line 2: "let d(X) be a discriminant function = W^T X"
// Line 3: "if X ∈ class I then d(X) > 0"
// Line 4: "if X ∈ class II then d(X) < 0"
// Line pitch: ~25px (101->127=26, 127->158=31, 158->187=29). Average ~29px.
// Use lineSpacing = 29pt (inches: 29/72 = 0.403in).
// First line top: y=101px. Baseline offset ~1.6px (slide_035). For 14pt, ascent ~12.7, halfLead ~0.6, baseline = top + 14.9 -> top = 101 - 14.9 = 86.1px.
const B1_TOP = px(86);
const B1_LINE_SPACING = 29;

function addRichText(slide, x, y, w, h, runs, fontSize, lineSpacing) {
  // runs: array of {text, options} where options can have color, bold, italic, underline, breakLine
  const opts = {
    x, y, w, h,
    align: "left", valign: "top", margin: 0,
    fontFace: "Arial", fontSize, color: "000000",
    lineSpacing,
    paraSpaceAfter: 0,
  };
  // Build text array with breakLine on all but last
  const texts = runs.map((r, i) => ({
    text: r.text,
    options: { ...r.options, breakLine: i < runs.length - 1 }
  }));
  slide.addText(texts, opts);
}

// Box 1 lines
// Line 1: "Define two classes: class I and Class II"
// Colors: "class I" green, "Class II" blue
addRichText(slide, BOX_X, B1_TOP, px(BOX_W), px(116), [
  { text: "Define two classes: " },
  { text: "class I", options: { color: "008000" } },
  { text: " and " },
  { text: "Class II", options: { color: "0000FF" } },
], 14, B1_LINE_SPACING);

// Line 2: "let d(X) be a discriminant function = W^T X"
// Color: "d(X)" green (from measurement: green at x=106..113, 132..138, 427..433)
addRichText(slide, BOX_X, px(86 + 29), px(BOX_W), px(116), [
  { text: "let " },
  { text: "d(X)", options: { color: "008000", italic: true } },
  { text: " be a discriminant function = " },
  { text: "W", options: { italic: true } },
  { text: "^T " },
  { text: "X", options: { italic: true } },
], 14, B1_LINE_SPACING);

// Line 3: "if X ∈ class I then d(X) > 0"
// Colors: "class I" green, "d(X)" red, "> 0" blue
addRichText(slide, BOX_X, px(86 + 2*29), px(BOX_W), px(116), [
  { text: "if " },
  { text: "X", options: { italic: true } },
  { text: " \u2208 " },
  { text: "class I", options: { color: "008000" } },
  { text: " then " },
  { text: "d(X)", options: { color: "C00000", italic: true } },
  { text: " > 0", options: { color: "0000FF" } },
], 14, B1_LINE_SPACING);

// Line 4: "if X ∈ class II then d(X) < 0"
// Colors: "class II" blue, "d(X)" red, "< 0" blue
addRichText(slide, BOX_X, px(86 + 3*29), px(BOX_W), px(116), [
  { text: "if " },
  { text: "X", options: { italic: true } },
  { text: " \u2208 " },
  { text: "Class II", options: { color: "0000FF" } },
  { text: " then " },
  { text: "d(X)", options: { color: "C00000", italic: true } },
  { text: " < 0", options: { color: "0000FF" } },
], 14, B1_LINE_SPACING);

// --- Box 2 text (y=231..306) ---
// 3 lines. First line: "For misclassified X :"
// "misclassified" underlined, "X" green (from measurement: green at x=244..257)
const B2_TOP = px(231 - 15); // baseline ~15px down from top for 14pt
const B2_LINE_SPACING = 29;

// Line 1: "For misclassified X :"
addRichText(slide, BOX_X, B2_TOP, px(BOX_W), px(100), [
  { text: "For " },
  { text: "misclassified", options: { underline: true, color: "008000" } },
  { text: " " },
  { text: "X", options: { italic: true, color: "008000" } },
  { text: " :" },
], 14, B2_LINE_SPACING);

// Line 2: "If X ∈ class I and misclassified as Class II then d(X) will be <0"
// Colors: "class I" green, "Class II" blue, "d(X)" red, "<0" blue
// Measurement: red run at x=136..176 (d(X)?), blue at x=385..450 (Class II), green at x=509..516 (class I), red at x=629..648 (will be <0?)
// Actually the verbatim says: "If X ∈ class I and misclassified as Class II then d(X) will be <0"
addRichText(slide, BOX_X, px(231 - 15 + 29), px(BOX_W), px(100), [
  { text: "If " },
  { text: "X", options: { italic: true } },
  { text: " \u2208 " },
  { text: "class I", options: { color: "008000" } },
  { text: " and " },
  { text: "misclassified", options: { underline: true } },
  { text: " as " },
  { text: "Class II", options: { color: "0000FF" } },
  { text: " then " },
  { text: "d(X)", options: { color: "C00000", italic: true } },
  { text: " will be " },
  { text: "<0", options: { color: "0000FF" } },
], 14, B2_LINE_SPACING);

// Line 3: "If X ∈ class II and misclassified as Class I then d(X) will be >0"
// Colors: "Class II" blue, "class I" green, "d(X)" red, ">0" blue
addRichText(slide, BOX_X, px(231 - 15 + 2*29), px(BOX_W), px(100), [
  { text: "If " },
  { text: "X", options: { italic: true } },
  { text: " \u2208 " },
  { text: "Class II", options: { color: "0000FF" } },
  { text: " and " },
  { text: "misclassified", options: { underline: true } },
  { text: " as " },
  { text: "class I", options: { color: "008000" } },
  { text: " then " },
  { text: "d(X)", options: { color: "C00000", italic: true } },
  { text: " will be " },
  { text: ">0", options: { color: "0000FF" } },
], 14, B2_LINE_SPACING);

// --- Box 3 text (y=338..410) ---
// Line 1: "Define Error function as:" with "Error" underlined
// Line 2: centered equation (rendered as PNG)
// Line 3: "take positive and negative values" - wait, this is part of the equation per verbatim
// Actually verbatim: "Error = \u03a3_{all misclassified vectors(i)} (W^T X_i) \u21d2 (W^T X_i) take positive and negative values"
// The recreation_brief says: heading "Define Error function as:" with "Error" underlined,
// followed by the centered equation. The equation includes the trailing phrase in red.
const B3_TOP = px(338 - 15);
const B3_LINE_SPACING = 29;

// Line 1: "Define Error function as:"
addRichText(slide, BOX_X, B3_TOP, px(BOX_W), px(100), [
  { text: "Define " },
  { text: "Error", options: { underline: true, color: "C00000" } },
  { text: " function as:" },
], 14, B3_LINE_SPACING);

// Line 2: Centered equation image
// Equation image: w=8.103in, h=0.552in. Center horizontally in box (BOX_W=11.264in).
// Box center x = 58 + 813/2 = 464.5px (6.451in). Image left = 464.5 - 8.103/2 * 72 = 464.5 - 291.7 = 172.8px.
// Vertical: box 3 content y=330..436 (106px = 1.472in). Equation height 0.552in.
// Center vertically: top = 330 + (106 - 8.103*72*0.552/1.5? No.
// Box top border at 329, bottom at 437. Content area y=330..436.
// Equation image h_in=0.55167in = 39.7px at 72dpi? No, in inches it's 0.55167in.
// Box content height = (436-330)/72 = 1.472in.
// Center: top = 330/72 + (1.472 - 0.55167)/2 = 4.583 + 0.460 = 5.043in = 363px.
// But the equation is at y=369..396 in original (center ~382). That's ~1.2in below box top (330).
// Let me use the measured position: equation center y=382px. Image h=0.552in=39.7pt.
// Top = 382 - 39.7/2 = 362px.
const EQ_X_PX = 464.5 - (EQ_ERROR.w_in * 72) / 2;
const EQ_Y_PX = 362;
slide.addImage({
  path: EQ_ERROR.path,
  x: px(EQ_X_PX), y: px(EQ_Y_PX),
  w: EQ_ERROR.w_in, h: EQ_ERROR.h_in,
});

// Red X mark at far right of box 3
// Original: x=771..778, y=369..382 (center ~774, 375). Box right edge at x=871.
// So X is ~97px from right edge.
// In inches: 774/72 = 10.75in from left. Box right = 871/72 = 12.097in.
// X mark w~7px = 0.097in. Font size ~36pt.
slide.addText("X", {
  x: px(774), y: px(375 - 18), // baseline at 375, ~18pt descent for 36pt
  w: px(30), h: px(40),
  align: "center", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 36, bold: true, color: "FF0000",
  lineSpacing: 36,
});

// --- Box 4 text (y=442..512) ---
// 3 lines.
// Line 1: "Define \u03b4_i as :" with \u03b4_i underlined
// Line 2: "If X \u2208 class I and misclassified as Class II then d(X) will be <0 \u21d2 \u03b4_i = -1 \u21d2 d(X) \u03b4_i >0"
// Line 3: "If X \u2208 class II and misclassified as Class I then d(X) will be >0 \u21d2 \u03b4_i = +1 \u21d2 d(X) \u03b4_i >0"
// Colors per recreation_brief: class I green, Class II blue, implication arrows and delta_i red, final d(X)delta_i >0 blue
const B4_TOP = px(442 - 15);
const B4_LINE_SPACING = 29;

// Line 1: "Define \u03b4_i as :"
addRichText(slide, BOX_X, B4_TOP, px(BOX_W), px(100), [
  { text: "Define " },
  { text: "\u03b4_i", options: { underline: true, italic: true } },
  { text: " as :" },
], 14, B4_LINE_SPACING);

// Line 2
addRichText(slide, BOX_X, px(442 - 15 + 29), px(BOX_W), px(100), [
  { text: "If " },
  { text: "X", options: { italic: true } },
  { text: " \u2208 " },
  { text: "class I", options: { color: "008000" } },
  { text: " and " },
  { text: "misclassified", options: { underline: true } },
  { text: " as " },
  { text: "Class II", options: { color: "0000FF" } },
  { text: " then " },
  { text: "d(X)", options: { color: "C00000", italic: true } },
  { text: " will be " },
  { text: "<0 ", options: { color: "0000FF" } },
  { text: "\u21d2 ", options: { color: "C00000" } },
  { text: "\u03b4_i ", options: { color: "C00000", italic: true } },
  { text: "= -1 ", options: { color: "C00000" } },
  { text: "\u21d2 ", options: { color: "C00000" } },
  { text: "d(X) ", options: { color: "C00000", italic: true } },
  { text: "\u03b4_i ", options: { color: "C00000", italic: true } },
  { text: ">0", options: { color: "0000FF" } },
], 14, B4_LINE_SPACING);

// Line 3
addRichText(slide, BOX_X, px(442 - 15 + 2*29), px(BOX_W), px(100), [
  { text: "If " },
  { text: "X", options: { italic: true } },
  { text: " \u2208 " },
  { text: "Class II", options: { color: "0000FF" } },
  { text: " and " },
  { text: "misclassified", options: { underline: true } },
  { text: " as " },
  { text: "class I", options: { color: "008000" } },
  { text: " then " },
  { text: "d(X)", options: { color: "C00000", italic: true } },
  { text: " will be " },
  { text: ">0 ", options: { color: "0000FF" } },
  { text: "\u21d2 ", options: { color: "C00000" } },
  { text: "\u03b4_i ", options: { color: "C00000", italic: true } },
  { text: "= +1 ", options: { color: "C00000" } },
  { text: "\u21d2 ", options: { color: "C00000" } },
  { text: "d(X) ", options: { color: "C00000", italic: true } },
  { text: "\u03b4_i ", options: { color: "C00000", italic: true } },
  { text: ">0", options: { color: "0000FF" } },
], 14, B4_LINE_SPACING);

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));