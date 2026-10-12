// slide_038.js — "Self Attention Mechanism (Adding Scaling)" + Figure-2-left inset
// (Deep Learning DSAI 308, lecture 001_transformers_part1). Top-level build for slide 38.
//
// DEPENDENCY LAW (founder directive 2026-10-11): slide 38 = slide 37's certified
// composition + delta. CHILD build — requires the certified frozen component
// components/slide_037.js and calls its renderBase; NEVER re-derives parent geometry.
//
// DELTA (PIL-measured on unique_slides/slide_038.jpg, 960x540, 1px=1pt; scans banked in
// scratch/slide038/m1..m10):
//   1. Figure-2-left inset (pure addition), far right ON the peach canvas:
//      green panel x[797..914] y[114..313] (border 1D7136 ~2.25pt, white fill);
//      five rounded boxes centered on x843.5 except the TOP MatMul (x836..901, offset
//      right — as drawn): MatMul(C3B9DB) y[136..156], SoftMax(CEE6D0) y[166..185],
//      Mask (opt.)(D8B6C5) y[196..214], Scale(F5F9C0) y[225..243], MatMul(C3B9DB)
//      y[255..273]; thin black UP arrows between boxes (x843.5), output stub above the
//      top MatMul (x868.5, y136->124), V bypass up the right side (x891.5, y296->157),
//      Q/K arrows below the bottom MatMul (x825.5 / x859.5), faint Q K V labels at
//      y~295. Top-down stack reads MatMul/SoftMax/Mask(opt.)/Scale/MatMul — the paper
//      figure's stacked layout read top-down (SOURCES.md reading-order artifact; arrows
//      flow bottom-up as drawn — do NOT "fix").
//   2. Scaling box y-shift: the yellow Scaling box sits 8px LOWER in slide 38's frame
//      than in slide 37's (m8: yellow run y[186..419] vs y[178..411]; x identical) while
//      the K.q/√d fraction and the rotated text are at the SAME absolute positions in
//      both frames (m8/m9). Frame = ground truth, so the parent's "scaling" block is
//      SKIPPED and redrawn here: box/inner rect +8px in y; fraction + rotated text keep
//      the parent's certified positions verbatim (same assets, same coords).
//   3. Badge numeral 38 via house chrome (chrome drawn ONCE here).
//   4. Mouse cursors visible in the frames (37: subtitle area; 38: near the lowest W_v
//      box) are video artifacts — omitted per judge ground rule (c).
//
// Run: cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//      videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_038.js

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/house_chrome.js");
const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_037.js");

const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_038_recreated.pptx";

const px = (v) => v / 72; // frame px -> inches

// ---- delta palette (measured cores, m10) -----------------------------------------
const D = {
  panelGreen: "1D7136",   // (29,113,54)
  boxBorder: "404040",    // (52,51,57) washed
  boxText: "333333",
  lavender: "C3B9DB",     // MatMul (195,185,219)
  lightGreen: "CEE6D0",   // SoftMax (206,230,208)
  rose: "D8B6C5",         // Mask (opt.) (216,182,197)
  paleYellow: "F5F9C0",   // Scale (245,249,192)
  black: "1A1A1A",        // arrows/labels (dark cores 43-52)
};

// ---- helpers (mirror the parent component's certified patterns) -------------------
function vArrow(slide, pptx, x, yFrom, yTo, width) {
  // vertical arrow, head at (x, yTo)
  slide.addShape(pptx.shapes.LINE, {
    x: px(x), y: px(Math.min(yFrom, yTo)), w: 0, h: px(Math.abs(yTo - yFrom)),
    flipV: yTo < yFrom,
    line: { color: D.black, width: width, endArrowType: "triangle" },
  });
}

function insetBox(slide, pptx, x, y, w, h, fill, label, fontSize) {
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: D.boxBorder, width: 1.25 }, rectRadius: 0.03,
  });
  slide.addText(label, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: fontSize, bold: true, color: D.boxText,
  });
}

function insetLabel(slide, pptx, cx, cy, letter) {
  slide.addText(letter, {
    x: px(cx - 7), y: px(cy - 6.5), w: px(14), h: px(13),
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 10, bold: true, color: D.black,
  });
}

// ---- delta block 1: Scaling box redrawn at the child frame's measured geometry ----
// Parent's certified geometry (components/slide_037.js drawScaling): outer x372 y177
// w48 h228 / inner x377 y183 w38 h217 / rotated text + fraction at fixed coords.
// Child frame (m8): box yellow run y[186..419] = parent +8px; fraction + text unshifted.
function drawScalingDelta(pptx, slide) {
  // outer rect (+8 in y vs parent)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(372), y: px(185), w: px(48), h: px(228),
    fill: { color: parent.C.scalingFill }, line: { color: parent.C.scalingInner, width: 0.75 },
  });
  // inner lighter rect (+8 in y vs parent)
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(377), y: px(191), w: px(38), h: px(217),
    fill: { color: "FFF069" }, line: { color: parent.C.scalingInner, width: 1 },
  });
  // rotated text — child-frame measured rendering (m11): the frame shows ONE unwrapped
  // vertical line reading top-to-bottom, ink y[240..359] x[386..401] (~120px long, ~16px
  // column => ~16pt), whereas the certified parent's render wraps it into two short
  // columns at y[272..309]. The frame is ground truth for this child delta: text box
  // pre-rotation w130 x h16 centered at (393.5, 299.5); rotate 90 (CW) => reads
  // top-to-bottom, 'S' at top, wrap width 130px (no wrap).
  slide.addText("Scaling by √d", {
    x: px(331.25), y: px(291.5), w: px(130), h: px(16),
    rotate: 90, align: "center", valign: "middle",
    fontSize: 16, bold: true, color: parent.C.scalingText, fontFace: "Arial", margin: 0,
    charSpacing: 1.5,
  });
  // fraction K.q / √d — parent's certified placement verbatim (m8: identical bbox in
  // both frames): num PNG (431,198), red bar x[418..449] y206, den PNG (436,217)
  slide.addImage({
    path: `${ASSETS}/eq_Kq_num_037.png`,
    x: px(431) - 0.33833 / 2, y: px(198) - 0.19333 / 2, w: 0.33833, h: 0.19333,
  });
  slide.addShape(pptx.shapes.LINE, {
    x: px(418), y: px(206), w: px(31), h: 0,
    line: { color: parent.C.red, width: 1.5 },
  });
  slide.addImage({
    path: `${ASSETS}/eq_Sqrtd_037.png`,
    x: px(436) - 0.285 / 2, y: px(217) - 0.23333 / 2, w: 0.285, h: 0.23333,
  });
}

// ---- delta block 2: Figure-2-left inset (course style), pure addition --------------
function drawInset(pptx, slide) {
  // panel
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: px(797), y: px(114), w: px(117), h: px(199),
    fill: { color: "FFFFFF" }, line: { color: D.panelGreen, width: 2.25 },
  });
  // boxes top->bottom (as the frame stacks them; arrows flow bottom-up)
  insetBox(slide, pptx, 836, 136, 65, 20, D.lavender, "MatMul", 10);     // A (offset right, as drawn)
  insetBox(slide, pptx, 813, 166, 61, 19, D.lightGreen, "SoftMax", 10);  // B
  insetBox(slide, pptx, 810, 196, 67, 18, D.rose, "Mask (opt.)", 10);    // C
  insetBox(slide, pptx, 822, 225, 43, 18, D.paleYellow, "Scale", 10);    // D
  insetBox(slide, pptx, 813, 255, 61, 18, D.lavender, "MatMul", 10);     // E
  // chain arrows bottom-up (x843.5): E->D->C->B->A, heads at the upper box's bottom
  vArrow(slide, pptx, 843.5, 255, 246, 1);
  vArrow(slide, pptx, 843.5, 225, 216, 1);
  vArrow(slide, pptx, 843.5, 196, 187, 1);
  vArrow(slide, pptx, 843.5, 166, 157, 1);
  // output stub above the top MatMul (head up, x868.5 = box A center)
  vArrow(slide, pptx, 868.5, 136, 124, 1);
  // V bypass: up the right side (x891.5, right of boxes B/C/D/E) into the top MatMul
  vArrow(slide, pptx, 891.5, 296, 157, 1);
  // Q / K arrows below the bottom MatMul (heads up into its bottom edge)
  vArrow(slide, pptx, 825.5, 289, 274, 1);
  vArrow(slide, pptx, 859.5, 295, 276, 1);
  // input labels (faint in the frame; drawn last, over the arrow tails)
  insetLabel(slide, pptx, 825.5, 295.5, "Q");
  insetLabel(slide, pptx, 860, 295.5, "K");
  insetLabel(slide, pptx, 892, 295.5, "V");
}

// ---- compose ------------------------------------------------------------------------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

drawHouseChrome(pres, slide, { numeral: 38 });
// parent's certified composition; "scaling" replaced by the child-frame redraw
parent.renderBase(pres, slide, { skip: ["scaling"] });
drawScalingDelta(pres, slide);
drawInset(pres, slide);

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT)).catch((e) => {
  console.error("BUILD FAILED:", e);
  process.exit(1);
});
