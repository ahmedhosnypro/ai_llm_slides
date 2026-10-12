// slide_041.js — "Normalization" taxonomy tree (Deep Learning DSAI 308, Transformers Part II — video 002, slide 41)
//
// CONTENT SPEC: analysis/slide_041_final.json (verbatim; PASS_WITH_FIXES applied; [?] items kept:
//   the root box prints exactly "Normalization" / "of" in the curated frame — recreation follows the frame).
// Provenance: slide_041_source/SOURCES.md (Wu & He 1803.08494 §2 taxonomy + Salimans & Kingma 1602.07868 —
//   course-made drawing, no published figure reproduced).
//
// CHROME LAW (founder directive 2026-10-11, playlist-wide): shared module
// videos/deep-learning/shared_patterns/house_chrome.js, numeral 41 (the number printed on THIS frame).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide041/m1_chrome.py + m2_borders.py):
// video 002 capture zoomed OUT to ~0.958 scale with a black letterbox strip BELOW the slide
// (frame rows 519..539 full-dark -> slide y >= 542: outside the 540pt slide, omitted — ground rule (c)).
// Fitted from THIS frame's four chrome border landmarks (left cols 58-59 c=58.5, right core 901,
// top core row 43, bottom rows 516-518 c=517 <-> slide chrome 42, 919, 45, 540):
//   slide_x = 42 + (fx - 58.5) * 877/842.5 ;  slide_y = 45 + (fy - 43) * 495/474
// Badge cross-check: yellow-bbox center (875.5, 71.0) -> slide (892.4, 74.2) vs house (893, 71):
// ~3px, same JPEG-bbox noise as certified slides 002/039 — same playlist template confirmed.
//
// MEASURED FACTS honored here (frame = ground truth; scratch/slide041/m3..m7):
//   * title "Normalization" red bold: ink slide [340.2,71.1 -> 568.2,96.2], center x 454.2
//     (NOT slide-centered; identical offset to certified slide 39's 453.4), advance fit -> 35.3pt bold.
//   * root box  fill mode (250,230,214) #FAE6D6 + 1px gray #A6A6A6 border; text bold red, two lines.
//   * blue box  fill mode (2,2,166)   #0000A6, borderless (border rows are pure AA transitions);
//     spec's #00008B guess measured 25-35 too dark on a 3600px solid — frame wins.
//   * green box fill mode (10,134,58) #0A863A, borderless (spec 007A3D family confirmed).
//   * cyan boxes fill mode (222,254,254) #E0FFFF-family, thin gray #A6A6A6 border; 4 boxes
//     x 254.9..493.3, h 40.7, pitch 54.3/54.3/57.4 (measured, not even — box 4 sits 3px lower).
//   * green leaf fill mode (214,254,230) #D6FEE6, thin gray border.
//   * leaf text: bold "Weight" cores p25 (26,120,66) ~= #007A3D — SAME green as the Weights box
//     (spec fix's #1A7A1A standardized without hex evidence; frame census wins for both words).
//   * cyan/leaf text ~21.5pt (advance fit 21.7-21.8, cap fit 21.8; spec's ~18pt estimate was low).
//   * connectors: SHAFTS are thin (~1-2 frame px) LIGHT hairlines — frame cores: drop
//     (216,215,213), hbar (214,213,211), spine (195,158,165), cyan shafts ~(215,186,191),
//     right shaft (211,192,194) — with SOLID red triangle heads ((184,0,0) cores = CC0000)
//     measured separately: elbow root->parents: drop line x453.7 y176.6->213.7, hbar y213.7
//     x224.7->684.3, two DOWN heads above the blue/green boxes; spine x225.9 y286.2->500.3 +
//     four right-pointing heads into the cyan boxes; right shaft x684.3 y284.1->326.5 + DOWN
//     head into the leaf box. (First read as "washed JPEG red" — the crop-pair vision check
//     crop_top_elbow_cmp.txt + shaft luma 170-215 proved the shafts are genuinely LIGHT;
//     corrected in attempt 3.)
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): black letterbox strip
//     (frame rows 519..539) and the black mouse cursor over "Batch" (spec imagery note).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "41")
drawHouseChrome(pres, s, { numeral: 41 });

const RED = "CC0000", NAVY = "000080", GRAY = "A6A6A6", LGRAY = "C0C0C0";
const BLUE_FILL = "0000A6", GREEN_FILL = "0A863A", LEAF_GREEN = "007A3D";
const CYAN_FILL = "E0FFFF", LEAF_FILL = "D6FEE6", ROOT_FILL = "FAE6D6";
const FONT = "Arial";

const pt = v => v / 72;
const K_AR = 0.9831; // baseline->boxTop lead (em) — inherited closed-loop constant from certified slide_039

function textLine(id, runs, opts) {
  // runs: [{text, size, bold, color}]; single line, positioned by BASELINE (slide pts)
  const maxAscent = Math.max(...runs.map(r => K_AR * r.size));
  const maxSize = Math.max(...runs.map(r => r.size));
  s.addText(runs.map(r => ({
    text: r.text,
    options: { fontSize: r.size, bold: !!r.bold, color: r.color, fontFace: FONT },
  })), {
    x: pt(opts.cx - opts.boxW / 2), y: pt(opts.baseline - maxAscent),
    w: pt(opts.boxW), h: pt(1.6 * maxSize),
    align: "center", valign: "top", margin: 0,
  });
}
function rect(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pres.ShapeType.rect, {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h),
    fill: { color: fill },
    line: lineColor ? { color: lineColor, width: lineW } : { type: "none" },
  });
}
function vline(x, y1, y2, wpt) {
  s.addShape(pres.ShapeType.line, {
    x: pt(x), y: pt(y1), w: 0, h: pt(y2 - y1),
    line: { color: RED, width: wpt },
  });
}
function hline(x1, x2, y, wpt) {
  s.addShape(pres.ShapeType.line, {
    x: pt(x1), y: pt(y), w: pt(x2 - x1), h: 0,
    line: { color: RED, width: wpt },
  });
}
// down-pointing solid triangle: base (top) width bw centered cx, from yBase down to yApex
function headDown(cx, yBase, yApex, bw) {
  s.addShape(pres.ShapeType.triangle, {
    x: pt(cx - bw / 2), y: pt(yBase), w: pt(bw), h: pt(yApex - yBase),
    fill: { color: RED }, line: { type: "none" }, flipV: true,
  });
}
// right-pointing solid triangle: apex at xApex, base (left) at xBase, vertical extent cy±hh
function headRight(xBase, xApex, cy, hh) {
  const wv = xApex - xBase, hv = 2 * hh;
  // up-triangle (w=hv, h=wv) rotated 90deg CW about its center -> points right
  s.addShape(pres.ShapeType.triangle, {
    x: pt((xBase + xApex) / 2 - hv / 2), y: pt(cy - wv / 2), w: pt(hv), h: pt(wv),
    fill: { color: RED }, line: { type: "none" }, rotate: 90,
  });
}

// ---- 2. connectors FIRST (z-order under boxes) — measured elbow + spine + right drop
// CLOSED-LOOP CROP FIX (attempt 2 -> 3, crop_top_elbow_cmp.txt FAIL + frame luma evidence):
// the original's connector SHAFTS are thin LIGHT hairlines (frame cores: drop (216,215,213),
// hbar (214,213,211), spine (195,158,165), cyan shafts ~(215,186,191), right shaft (211,192,194);
// luma 170-215 — a saturated red line would sit at luma ~61), with only the arrowheads solid red.
// Attempt 2's 2pt CC0000 shafts read ~3x heavier than the original (judge MAJOR). Fixed: 1pt
// shafts at the measured per-connector colors; heads kept solid CC0000, shrunk ~12% (the frame
// ink bboxes carry ~1px JPEG halo each side).
const SHAFT_DROP = "D7D6D4", SHAFT_HBAR = "D6D5D3", SHAFT_SPINE = "C39EA5",
      SHAFT_CYAN = "D7BABF", SHAFT_RIGHT = "D3C0C2";
function vlineC(x, y1, y2, wpt, color) {
  s.addShape(pres.ShapeType.line, {
    x: pt(x), y: pt(y1), w: 0, h: pt(y2 - y1),
    line: { color: color, width: wpt },
  });
}
function hlineC(x1, x2, y, wpt, color) {
  s.addShape(pres.ShapeType.line, {
    x: pt(x1), y: pt(y), w: pt(x2 - x1), h: 0,
    line: { color: color, width: wpt },
  });
}
function headDownC(cx, yBase, yApex, bw, color) {
  s.addShape(pres.ShapeType.triangle, {
    x: pt(cx - bw / 2), y: pt(yBase), w: pt(bw), h: pt(yApex - yBase),
    fill: { color: color }, line: { type: "none" }, flipV: true,
  });
}
function headRightC(xBase, xApex, cy, hh, color) {
  const wv = xApex - xBase, hv = 2 * hh;
  s.addShape(pres.ShapeType.triangle, {
    x: pt((xBase + xApex) / 2 - hv / 2), y: pt(cy - wv / 2), w: pt(hv), h: pt(wv),
    fill: { color: color }, line: { type: "none" }, rotate: 90,
  });
}
vlineC(453.7, 176.6, 213.7, 1, SHAFT_DROP);      // drop from root bottom
hlineC(224.7, 684.3, 213.7, 1, SHAFT_HBAR);      // horizontal split bar
headDownC(224.7, 218.2, 228.0, 8.2, RED);        // head into Activations Outputs
headDownC(684.3, 218.2, 228.0, 9.0, RED);        // head into Weights
vlineC(225.9, 286.2, 500.3, 1, SHAFT_SPINE);     // left spine
const CY = [328.6, 382.9, 437.2, 494.6];
for (const cy of CY) {
  hlineC(225.9, 241.9, cy, 1, SHAFT_CYAN);       // shaft
  headRightC(241.9, 253.3, cy, 3.8, RED);        // head into cyan box
}
vlineC(684.3, 284.1, 326.5, 1, SHAFT_RIGHT);     // right drop from Weights
headDownC(684.3, 327.6, 338.8, 8.2, RED);        // head into Weight Normalization

// ---- 3. boxes (cyan/leaf borders lightened to C0C0C0 per crop judge MINOR + frame luma ~190;
//      root border stays A6A6A6 — measured (167,167,169))
rect(347.5, 124.4, 217.6, 52.2, ROOT_FILL, GRAY, 1);    // root
rect(113.3, 231.9, 221.7, 54.3, BLUE_FILL);             // Activations Outputs
rect(572.4, 229.8, 222.7, 54.3, GREEN_FILL);            // Weights
rect(254.9, 308.2, 238.4, 40.7, CYAN_FILL, LGRAY, 1);   // Batch
rect(254.9, 362.5, 238.4, 40.7, CYAN_FILL, LGRAY, 1);   // Instance
rect(254.9, 416.8, 238.4, 40.7, CYAN_FILL, LGRAY, 1);   // Group
rect(254.9, 474.2, 238.4, 40.7, CYAN_FILL, LGRAY, 1);   // Layer
rect(565.1, 342.6, 236.3, 38.7, LEAF_FILL, LGRAY, 1);   // Weight Normalization

// ---- 4. text (single-line boxes positioned by measured baselines; centers = measured box centers)
// sizes CLOSED-LOOP corrected from attempt 1 (c2_closedloop2.py): render ink was 2-5% narrow at
// the advance-fit sizes -> root 21->22, parents 21->21.7, cyan 21.5->22.1, leaf 21.5->22.
// title (ink center x 454.2, baseline 96.2; boxW mirrors certified slide 39's title box)
textLine("title", [{ text: "Normalization", size: 35.3, bold: true, color: RED }],
  { baseline: 96.2, cx: 454.2, boxW: 320.9 });
// root box: two lines (verbatim two-line break "Normalization" / "of")
textLine("rootL1", [{ text: "Normalization", size: 22, bold: true, color: RED }],
  { baseline: 144.2, cx: 456.3, boxW: 280 });
textLine("rootL2", [{ text: "of", size: 22, bold: true, color: RED }],
  { baseline: 168.8, cx: 456.3, boxW: 120 });
// blue parent: two lines white bold
textLine("blueL1", [{ text: "Activations", size: 21.7, bold: true, color: "FFFFFF" }],
  { baseline: 253.4, cx: 224.15, boxW: 260 });
textLine("blueL2", [{ text: "Outputs", size: 21.7, bold: true, color: "FFFFFF" }],
  { baseline: 278.2, cx: 224.15, boxW: 220 });
// green parent
textLine("greenL1", [{ text: "Weights", size: 21.7, bold: true, color: "FFFFFF" }],
  { baseline: 264.6, cx: 683.75, boxW: 220 });
// cyan leaves: bold category word + regular "Normalization", navy
textLine("cyan1", [{ text: "Batch", size: 22.1, bold: true, color: NAVY },
                   { text: " Normalization", size: 22.1, bold: false, color: NAVY }],
  { baseline: 335.8, cx: 374.1, boxW: 320 });
textLine("cyan2", [{ text: "Instance", size: 22.1, bold: true, color: NAVY },
                   { text: " Normalization", size: 22.1, bold: false, color: NAVY }],
  { baseline: 390.1, cx: 374.1, boxW: 340 });
textLine("cyan3", [{ text: "Group", size: 22.1, bold: true, color: NAVY },
                   { text: " Normalization", size: 22.1, bold: false, color: NAVY }],
  { baseline: 444.5, cx: 374.1, boxW: 330 });
textLine("cyan4", [{ text: "Layer", size: 22.1, bold: true, color: NAVY },
                   { text: " Normalization", size: 22.1, bold: false, color: NAVY }],
  { baseline: 501.9, cx: 374.1, boxW: 330 });
// green leaf: bold "Weight" + regular "Normalization", both measured leaf green
textLine("leaf", [{ text: "Weight", size: 22, bold: true, color: LEAF_GREEN },
                  { text: " Normalization", size: 22, bold: false, color: LEAF_GREEN }],
  { baseline: 369.4, cx: 683.25, boxW: 340 });

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_041_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
