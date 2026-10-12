// build/slide_025.js — slide 025 "Sine/Cosine Encoders /
// (an industrial application of Motor Control System)"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 25)
//
// CONTENT SPEC: analysis/slide_025_final.json (PASS_WITH_FIXES, score 8; fresh
// re-analysis 2026-10-12 content-gate retry). Original frame:
// unique_slides/slide_025.jpg (960x540, 1px = 1pt). Provenance:
// slide_025_source/SOURCES.md (Wikipedia rotary-encoder + motioncontroltips sine-
// encoder confirm the sin/cos-quadrature + line-count terminology; the citation is a
// frame fact; venue [?] not resolvable from this environment).
//
// CHROME LAW (playlist, founder directive 2026-10-11): shared house chrome via
// videos/deep-learning/shared_patterns/house_chrome.js drawHouseChrome(...{numeral:25}).
// Badge numeral 25 = the number printed on THIS original frame.
//
// FRAME->SLIDE MAPPING (deck standard, fitted from THIS frame's chrome landmarks
// L59/R902/T43/B516 <-> slide 42/919/45/540 — identical to build/slide_002.js and the
// certified components/slide_026.js):
//   slide_x_pt = (frame_x - 18.628) / 0.96123 ;  slide_y_pt = frame_y / 0.95556
// ALL box geometry below is precomputed in SLIDE PT from frame measurements
// (scratch/slide025/measure_*.py passes 1-7 + ASCII mask dumps) — attempt-1 lesson:
// never pass slide-pt values through the frame-px helpers (double-mapping bug).
//
// ENCODER DISK (right panel) = GENERATED IMAGE (advanced-graph rule, founder directive
// 2026-10-09; single-version law): assets/s025_ring.png (matplotlib, 4x) — red cos +
// green sin traces (r0 101.65px, amplitude 6.8px, 16 periods, phases mask-IoU-fitted:
// red 85.8deg / green 176.6deg y-down — 90.8deg offset = the sin/cos quadrature,
// quantitative; trace-vs-frame IoU 0.51/0.51), white hub r11 gray outline (concentric),
// two dashed radial lines (hub edge -> (731,248)/(720,303), one period apart), the
// ONE-PERIOD arc arrow at r=127 between the dashes (measured: the "vertical double
// arrow" is a constant-radius arc), and the rotation arc arrow at r=74. Placement
// verified attempt-1: composite-at-intended-position vs LO render IoU 0.78/0.80.
// All diagram TEXT stays native (fidelity law).
//
// MOTOR ILLUSTRATION (left panel): clipped from the ORIGINAL frame (founder figure
// pattern, certified precedent assets/slide026_motor.png) -> assets/slide025_motor.png
// (frame 103,174-301,301; the 'AC Motor' label region whited out — label is native text).
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (ground rule (c), spec imagery flags both):
//   * mouse cursor below the encoder callout (frame ~(158..167, 348..356))
//   * black letterbox strip below frame row 516 (below the 540pt slide bottom) — the
//     spec's "bottom black bar" region = letterbox, not slide content.
//
// LAWS honored: verbatim text incl. double spaces ("rotary  position", "angular  ",
// "count =16"); explicit fontFace + margin:0 everywhere; explicit lineSpacing on every
// multi-line box; no '#' in hex; single-version deliverable slide_025_recreated.pptx.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS = path.join(__dirname, "assets");
for (const f of ["s025_ring.png", "s025_motor.png"]) {
  if (!fs.existsSync(path.join(ASSETS, f))) throw new Error("missing asset " + f);
}

// ---- palette (frame census cores reconciled with the certified siblings) ----
const TITLE_RED = "C00000";      // title + arrow label + block arrow (arrow census core (159,1,9))
const WAVE_RED = "FF0000";       // cos label
const WAVE_GREEN = "00CC00";     // sin label
const BLUE = "0000CC";           // subtitle + footer (spec; slide-024 precedent; frame cores JPEG-darkened)
const PANEL_GREEN = "00A651";    // panel borders (border core (24,123,62))
const CALLOUT_FILL = "EED0AF";   // census (238.5,207.8,175.4)
const CALLOUT_TEXT = "8B1A1A";   // spec (luma-matched to frame core)
const INK = "000000";
const FONT = "Arial";

// ---- frame-px -> slide-pt helpers (for shapes measured on the frame) ----
const MX = 18.628, SX = 0.96123, SY = 0.95556;
const fx2pt = (fx) => (fx - MX) / SX;
const fy2pt = (fy) => fy / SY;
const IN = (pt) => pt / 72;
// shape boxes from frame px (correct usage: FRAME values only)
const SHP = {
  leftPanel:  { x: fx2pt(101), y: fy2pt(171), w: fx2pt(304) - fx2pt(101), h: fy2pt(366) - fy2pt(171) },
  motor:      { x: fx2pt(103), y: fy2pt(174), w: fx2pt(301) - fx2pt(103), h: fy2pt(301) - fy2pt(174) },
  callout:    { x: fx2pt(121), y: fy2pt(304), w: fx2pt(224) - fx2pt(121), h: fy2pt(353) - fy2pt(304) },
  blockArrow: { x: fx2pt(349), y: fy2pt(219), w: fx2pt(404) - fx2pt(349), h: fy2pt(241) - fy2pt(219) },
  rightPanel: { x: fx2pt(450), y: fy2pt(140), w: fx2pt(834) - fx2pt(450), h: fy2pt(389) - fy2pt(140) },
  ring:       { x: fx2pt(477), y: fy2pt(147), w: fx2pt(733) - fx2pt(477), h: fy2pt(385) - fy2pt(147) },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const slide = pres.addSlide();

// 1. house chrome (canvas + gray panel + red border + badge 25)
drawHouseChrome(pres, slide, { numeral: 25 });

// 2. title + subtitle (ink centers 461.15 / 463.24 pt — NOT the slide center, measured)
slide.addText("Sine/Cosine Encoders", {
  x: IN(461.15 - 420), y: IN(83.20 - 12), w: IN(840), h: IN(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 22, bold: true, color: TITLE_RED,
});
slide.addText("(an industrial application of Motor Control System)", {
  x: IN(463.24 - 420), y: IN(109.88 - 12 - 2.7), w: IN(840), h: IN(24),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 22, bold: true, color: BLUE,
});

// 3. left panel + motor art + label + callout
slide.addShape(pres.ShapeType.roundRect, {
  x: IN(SHP.leftPanel.x), y: IN(SHP.leftPanel.y), w: IN(SHP.leftPanel.w), h: IN(SHP.leftPanel.h),
  fill: { color: "FFFFFF" }, line: { color: PANEL_GREEN, width: 2.25 }, rectRadius: 0.06,
});
slide.addImage({
  path: path.join(ASSETS, "s025_motor.png"),
  x: IN(SHP.motor.x), y: IN(SHP.motor.y), w: IN(SHP.motor.w), h: IN(SHP.motor.h),
});
slide.addText("AC Motor", {
  x: IN(243.85 - 60), y: IN(229.76 - 9), w: IN(120), h: IN(18),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 16, color: INK,
});
slide.addShape(pres.ShapeType.roundRect, {
  x: IN(SHP.callout.x), y: IN(SHP.callout.y), w: IN(SHP.callout.w), h: IN(SHP.callout.h),
  fill: { color: CALLOUT_FILL }, line: { type: "none" }, rectRadius: 0.08,
});
// text box = callout box raised 3.8pt and shifted 3.5pt right (attempt-1/2 empirical:
// LO centers the block 3.8pt low; the frame's text sits 3.5pt right of the tan-box center)
slide.addText([
  { text: "Sin/Cos", options: { breakLine: true } },
  { text: "Encoder", options: {} },
], {
  x: IN(SHP.callout.x + 3.5), y: IN(SHP.callout.y - 3.8), w: IN(SHP.callout.w), h: IN(SHP.callout.h),
  align: "center", valign: "middle", margin: 0, lineSpacing: 23,
  fontFace: FONT, fontSize: 18.5, bold: true, color: CALLOUT_TEXT,
});

// 4. center block arrow + two-line red label
slide.addShape(pres.ShapeType.rightArrow, {
  x: IN(SHP.blockArrow.x), y: IN(SHP.blockArrow.y), w: IN(SHP.blockArrow.w), h: IN(SHP.blockArrow.h),
  fill: { color: TITLE_RED }, line: { type: "none" },
});
// attempt-1 empirical: with lineSpacing 32.5 + valign top, LO puts line-1 ink top at
// box_top + 17.5pt; target ink top 279.43 -> box top 261.9
slide.addText([
  { text: "Sin/Cos Encoder", options: { breakLine: true } },
  { text: "Output Signals", options: {} },
], {
  x: IN(374.44 - 90), y: IN(261.9), w: IN(180), h: IN(70),
  align: "center", valign: "top", margin: 0, lineSpacing: 32.5,
  fontFace: FONT, fontSize: 16, bold: true, color: TITLE_RED,
});

// 5. right panel + generated encoder disk
slide.addShape(pres.ShapeType.roundRect, {
  x: IN(SHP.rightPanel.x), y: IN(SHP.rightPanel.y), w: IN(SHP.rightPanel.w), h: IN(SHP.rightPanel.h),
  fill: { color: "FFFFFF" }, line: { color: PANEL_GREEN, width: 2.25 }, rectRadius: 0.06,
});
slide.addImage({
  path: path.join(ASSETS, "s025_ring.png"),
  x: IN(SHP.ring.x), y: IN(SHP.ring.y), w: IN(SHP.ring.w), h: IN(SHP.ring.h),
});

// 6. right-panel native labels (boxes centered on the frame-measured ink centers)
slide.addText("Rotation direction", {
  x: IN(600.02 - 70), y: IN(218.19 - 5), w: IN(140), h: IN(10),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 9.5, bold: true, color: INK,
});
slide.addText("CCW/CW", {
  x: IN(600.02 - 50), y: IN(235.99 - 5), w: IN(100), h: IN(10),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 10, color: INK,
});
slide.addText("cos", {
  x: IN(742.98 - 25), y: IN(215.06 - 4.5), w: IN(50), h: IN(9),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 11, bold: true, color: WAVE_RED,
});
slide.addText("sin", {
  x: IN(750.06 - 25), y: IN(236.51 - 4.5), w: IN(50), h: IN(9),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 11, bold: true, color: WAVE_GREEN,
});
slide.addText("Line count =16", {
  x: IN(591.77 - 80), y: IN(311.86 - 5), w: IN(160), h: IN(10),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 11.5, bold: true, color: INK,
});
slide.addText([
  { text: "(16 signal periods per", options: { breakLine: true } },
  { text: "revolution)", options: {} },
], {
  x: IN(596.60 - 90), y: IN(318.60 - 2.4), w: IN(180), h: IN(32),
  align: "center", valign: "top", margin: 0, lineSpacing: 14.7,
  fontFace: FONT, fontSize: 10.5, color: INK,
});
slide.addText("Sin/Cos signal period", {
  x: IN(785.17 - 60), y: IN(289.37 - 5.5), w: IN(120), h: IN(11),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 10.5, color: INK,
});

// 7. summary sentence (verbatim double spaces; bands y411..429 / y433..450, pitch 23.02pt;
//    attempt-1: ink landed 1.6pt high -> box top 425.8)
slide.addText([
  { text: "Incremental rotary  position encoders are used in many applications to", options: { breakLine: true } },
  { text: "measure angular  position and speed.", options: {} },
], {
  x: IN(493.00 - 350), y: IN(425.8), w: IN(700), h: IN(48),
  align: "center", valign: "top", margin: 0, lineSpacing: 23,
  fontFace: FONT, fontSize: 20, bold: true, color: INK,
});

// 8. footer reference (3 measured lines; L1 left-aligned at 66.97pt, L2/L3 centered)
slide.addText("For More Info:", {
  x: IN(66.97), y: IN(498.63 - 5), w: IN(140), h: IN(10),
  align: "left", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 11, bold: true, italic: true, color: BLUE,
});
slide.addText("EXTRACTION OF HIGH RESOLUTION POSITION INFORMATION FROM SINUSOIDAL ENCODERS", {
  x: IN(342.14 - 260), y: IN(510.70 - 5), w: IN(520), h: IN(10),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 11, italic: true, color: BLUE,
});
slide.addText("J. Burke, J. F. Moynhan, K. Unterkofler", {
  x: IN(340.58 - 110), y: IN(524.29 - 5), w: IN(220), h: IN(10),
  align: "center", valign: "middle", margin: 0,
  fontFace: FONT, fontSize: 11, italic: true, color: BLUE,
});

pres.writeFile({ fileName: path.join(__dirname, "..", "slide_025_recreated.pptx") })
  .then(() => console.log("WROTE slide_025_recreated.pptx"));
