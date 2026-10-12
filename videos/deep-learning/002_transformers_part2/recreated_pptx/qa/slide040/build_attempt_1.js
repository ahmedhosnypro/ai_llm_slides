// slide_040.js — "Normalization Parameters" (Deep Learning DSAI 308, Transformers Part II — video 002, slide 40)
//
// CONTENT SPEC: analysis/slide_040_final.json (verbatim; PASS_WITH_FIXES applied).
// Original frame: unique_slides/slide_040.jpg (960x540). All ink positions PIL-measured
// (scratch/slide040/m1..m25) and mapped to TRUE slide coordinates through the frame->slide
// transform fitted from this frame's four chrome landmarks (left 58, right 901, top 43,
// bottom 517 <-> slide 42, 919, 45, 540 — identical to certified slide_002/039):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Badge cross-check: yellow-bbox center (875.5, 71.0) -> slide (891.4, 74.3) vs house
// (893, 71) — within JPEG-bbox noise (same as certified slide_002/039), same template.
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js, numeral 40.
//
// MEASURED FACTS honored here (frame = ground truth; overrides spec guesses):
//   * intro paragraph: 3 lines, Times serif ~19.7pt (width-fit; spec's 16-17pt was a
//     vision guess — x-height/cap/advance measurements say ~19.5-20), baselines slide
//     y 137.1 / 162.3 / 187.3 (pitch 25.11pt, set explicitly).
//   * intro "learn parameters" = green #008000 bold on light-green highlight (measured
//     fill #D3FFD1-interior, spec #90EE90 family); BUT the intro "γ" and "β" glyph cores
//     measured DARK RED ((103,0,15)/(119,10,31) raw) — spec said green; frame wins
//     (same law as certified slide_039). "and" between them measured green.
//   * red underlined phrase: underline present ONLY under line 3 (rows 178..185, x
//     104..436); L2's red run "convert the mean and" has NO underline (rows 158..167
//     probed empty) — spec's whole-phrase underline corrected by frame.
//   * algorithm panel: white rect frame[145,204,552,497] -> slide[131.5,213.5,423.4,306.6],
//     black 1.5pt border. Content = Ioffe & Szegedy Algorithm 1 re-typeset (CM style):
//     header lines + 4 display equations rendered as matplotlib-mathtext PNGs (certified
//     mechanism, cm fontset, 600dpi, hashed colors) placed at measured left edges and
//     row baselines: h1 138.7/235.0, h2 196.0/257.4, h3 137.7/278.9, eq1 150.1/335.9,
//     eq2 150.1/395.6, eq3 158.5/447.9, eq4 159.6/491.7 (slide pt).
//   * display sums have limits above/below (m upper 292..297, i=1 lower 331..339);
//     arrows are LONG (x 194..232 = 40pt) -> \longleftarrow in eq1/eq2/eq3, short in eq4.
//   * highlights (frame-measured rects): lavender #9999CC behind mu_B (eq1), sigma^2_B
//     (eq2), mu_B numerator + sigma^2_B denominator (eq3); pink #FF9C9C behind xhat_i
//     (eq3+eq4) and '// normalize'; orange #FFA64D behind '// scale and shift'; green
//     #90EE90 behind params line, gamma (eq4), beta (eq4). PIL census shows NO highlight
//     behind "x_i -" or the radical tail (white fills) and NO separate light-blue class —
//     spec's #A6D0F2 numerator/denominator claim corrected to lavender by frame.
//   * thin lavender underline under the WHOLE eq3 math (frame row 446, x 164..287,
//     core (143,142,172) = #9999CC-family) — reproduced as a 1.5pt line.
//   * orange ellipse outline #FF8C00 around y_i (eq4): frame[170,454,191,475].
//   * comments '// ...' Arial ~14pt, right-aligned to ink x 548.6, baselines 333.8 /
//     394.6 / 447.9 / 490.8.
//   * title "Normalization Parameters" Arial Bold red CC0000 ~35.5 (cap/width fit), ink
//     center x 467.5 (NOT slide-centered — measured as-is), baseline 93.1.
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): black letterbox strip
//     (frame rows 519..539 — maps BELOW slide bottom 540, off-slide), no pen cursor here.

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets";
const eq = n => JSON.parse(fs.readFileSync(`${ASSETS}/slide040_${n}_eq.json`, "utf8"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 0. playlist house chrome (white canvas, gray panel + red border, badge "40")
drawHouseChrome(pres, s, { numeral: 40 });

const RED = "C00000", BLUE = "2222CC", GREEN = "008000", BLACK = "000000";
const LAV = "9999CC", PINK = "FF9C9C", ORNG = "FFA64D", ORNGE = "FF8C00", GRNHL = "90EE90";
const pt = v => v / 72;
const K_AR = 0.9831, K_TS = 0.97; // baseline->boxTop lead (em) — closed-loop corrected

function textLine(id, runs, opts) {
  const maxAscent = Math.max(...runs.map(r => (r.options.fontFace === "Times New Roman" ? K_TS : K_AR) * r.options.fontSize));
  const maxSize = Math.max(...runs.map(r => r.options.fontSize));
  s.addText(runs.map(r => ({
    text: r.text,
    options: {
      fontSize: r.options.fontSize, bold: !!r.options.bold, italic: !!r.options.italic,
      color: r.options.color, fontFace: r.options.fontFace || "Arial",
      underline: r.options.underline, breakLine: !!r.options.breakLine,
    },
  })), {
    x: pt(opts.boxX), y: pt(opts.baseline - maxAscent),
    w: pt(opts.boxW), h: pt(1.6 * maxSize),
    align: opts.align || "left", valign: "top", margin: 0,
    lineSpacing: opts.lineSpacing || undefined,
  });
}
function rect(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pres.ShapeType.rect, {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h),
    fill: { color: fill }, line: { color: lineColor, width: lineW },
  });
}

// ---- 1. boxes FIRST (z-order under highlights/text)
// intro paragraph box  frame[88,104,892,185] -> slide [72.2,108.8,836.4,84.8]
rect(72.2, 108.8, 836.4, 84.8, "FFFFFF", RED, 2);
// algorithm panel  frame[145,204,552,497] -> slide [131.5,213.5,423.4,306.6]
rect(131.5, 213.5, 423.4, 306.6, "FFFFFF", BLACK, 1.5);

// ---- 2. highlight rects (frame-measured, slide pt)
rect(385.4, 151.7, 148.1, 13.6, GRNHL, GRNHL, 0);   // intro "learn parameters"  frame[389,145,531,158]
rect(191.5, 236.4, 231.8, 24.1, GRNHL, GRNHL, 0);   // panel params line       frame[203,226,425,249]
rect(151.1, 315.9, 25.0, 26.2, LAV, LAV, 0);        // mu_B eq1                frame[164,302,188,327]
rect(153.2, 376.6, 26.1, 25.1, LAV, LAV, 0);        // sigma^2_B eq2           frame[166,360,191,384]
rect(244.6, 416.4, 27.0, 26.2, LAV, LAV, 0);        // mu_B eq3 numerator      frame[254,398,280,423]
rect(220.9, 443.6, 24.7, 24.1, LAV, LAV, 0);        // sigma^2_B eq3 denom     frame[231,424,255,447]
rect(156.3, 429.0, 25.0, 26.2, PINK, PINK, 0);      // xhat_i eq3              frame[169,410,193,434]
rect(457.6, 430.1, 92.0, 22.0, PINK, PINK, 0);      // '// normalize'          frame[458,411,547,432]
rect(200.1, 472.8, 14.6, 22.0, GRNHL, GRNHL, 0);    // gamma eq4               frame[211,452,225,473]
rect(214.6, 472.8, 18.8, 24.1, PINK, PINK, 0);      // xhat_i eq4              frame[225,452,243,475]
rect(251.2, 472.8, 14.6, 22.0, GRNHL, GRNHL, 0);    // beta eq4                frame[260,452,274,473]
rect(424.3, 472.8, 125.4, 22.0, ORNG, ORNG, 0);     // '// scale and shift'    frame[426,452,547,473]

// ---- 3. title (Arial Bold red; ink center 467.5, baseline 93.1)
textLine("title", [{ text: "Normalization Parameters", options: { fontSize: 35.5, bold: true, color: RED, fontFace: "Arial" } }],
  { baseline: 93.13, boxX: 217.5, boxW: 500, align: "center" });

// ---- 4. intro paragraph — 3 lines, Times 20.0 (closed-loop width-fit), explicit pitch
// 26.2pt (baselines 135.9/162.1/188.3 — attempt-2: ascender-top pitch is 25 frame px = 26.17pt).
// L2 is SPLIT into two boxes so the green/red runs start exactly at the measured highlight
// position (frame x 390 -> slide 386.4) — the prefix box renders independently.
const TS = 20.0;
textLine("introL1", [
  { text: "Instead of restricting the Activations of each layer to be ", options: { fontSize: TS, color: BLACK, fontFace: "Times New Roman" } },
  { text: "strictly ", options: { fontSize: TS, color: BLUE, fontFace: "Times New Roman", italic: true } },
  { text: "Zero ", options: { fontSize: TS, color: BLUE, fontFace: "Times New Roman", bold: true } },
  { text: "mean ", options: { fontSize: TS, color: BLUE, fontFace: "Times New Roman" } },
  { text: "and ", options: { fontSize: TS, color: BLUE, fontFace: "Times New Roman" } },
  { text: "unit ", options: { fontSize: TS, color: BLUE, fontFace: "Times New Roman", bold: true } },
  { text: "variance,", options: { fontSize: TS, color: BLUE, fontFace: "Times New Roman" } },
], { baseline: 135.9, boxX: 88, boxW: 800 });
textLine("introL2a", [
  { text: "Normalization allows the network to ", options: { fontSize: TS, color: BLACK, fontFace: "Times New Roman" } },
], { baseline: 162.1, boxX: 88, boxW: 320 });
textLine("introL2b", [
  { text: "learn parameters ", options: { fontSize: TS, color: GREEN, fontFace: "Times New Roman", bold: true } },
  { text: "\u03B3 ", options: { fontSize: TS, color: RED, fontFace: "Times New Roman", italic: true } },
  { text: "and ", options: { fontSize: TS, color: GREEN, fontFace: "Times New Roman" } },
  { text: "\u03B2 ", options: { fontSize: TS, color: RED, fontFace: "Times New Roman", bold: true } },
  { text: "that can ", options: { fontSize: TS, color: BLACK, fontFace: "Times New Roman" } },
  { text: "convert the mean and", options: { fontSize: TS, color: RED, fontFace: "Times New Roman" } },
], { baseline: 162.1, boxX: 386.4, boxW: 520 });
textLine("introL3", [
  { text: "variance to any value that ", options: { fontSize: TS, color: RED, fontFace: "Times New Roman", underline: { style: "sng" } } },
  { text: "Minimizes Loss.", options: { fontSize: TS, color: RED, fontFace: "Times New Roman", bold: true, underline: { style: "sng" } } },
], { baseline: 188.3, boxX: 88, boxW: 500 });

// ---- 5. panel header/equation PNGs (certified mathtext mechanism; exact size, baseline-anchored)
function eqImage(name, leftInk, baseline) {
  const d = eq(name);
  const w = d.w_in, h = d.h_in;
  s.addImage({
    path: `${ASSETS}/slide040_${name}.png`,
    x: pt(leftInk), y: baseline / 72 - d.baseline_frac * h,
    w, h,
  });
  return d;
}
eqImage("h1", 138.7, 235.0);
eqImage("h2", 196.0, 254.3);
eqImage("h3", 137.7, 278.9);
eqImage("eq1", 150.1, 335.9);
eqImage("eq2", 150.1, 395.6);
eqImage("eq3", 158.5, 447.9);
eqImage("eq4", 159.6, 491.7);

// ---- 6. thin lavender underline under the whole eq3 math (frame row 446, x 164..287)
s.addShape(pres.ShapeType.line, {
  x: pt(151.1), y: pt(467.2), w: pt(127.8), h: 0,
  line: { color: LAV, width: 1.5 },
});

// ---- 7. comments (Arial 16.3 — closed-loop width-fit: 14pt rendered 15% narrow)
const CM = 16.3;
textLine("c1", [{ text: "// mini-batch mean", options: { fontSize: CM, color: BLACK, fontFace: "Arial" } }],
  { baseline: 333.8, boxX: 380, boxW: 170, align: "right" });
textLine("c2", [{ text: "// mini-batch variance", options: { fontSize: CM, color: BLACK, fontFace: "Arial" } }],
  { baseline: 394.6, boxX: 380, boxW: 170, align: "right" });
textLine("c3", [{ text: "// normalize", options: { fontSize: CM, color: BLACK, fontFace: "Arial" } }],
  { baseline: 447.9, boxX: 380, boxW: 170, align: "right" });
textLine("c4", [{ text: "// scale and shift", options: { fontSize: CM, color: BLACK, fontFace: "Arial" } }],
  { baseline: 490.8, boxX: 380, boxW: 170, align: "right" });

// ---- 8. orange ellipse outline around y_i (eq4) — frame[170,454,191,475], no fill
s.addShape(pres.ShapeType.ellipse, {
  x: pt(157.5), y: pt(475.1), w: pt(21.8), h: pt(22.0),
  fill: { color: "FFFFFF", transparency: 100 },
  line: { color: ORNGE, width: 1.5 },
});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_040_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
