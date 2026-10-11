// slide_039.js — "Normalization" (Deep Learning DSAI 308, Transformers Part II — video 002, slide 39)
//
// CONTENT SPEC: analysis/slide_039_final.json (verbatim text; PASS_WITH_FIXES applied).
// Original frame: unique_slides/slide_039.jpg (960x540). All ink positions PIL-measured
// (scratch/slide039/m1..m8) and mapped to TRUE slide coordinates through the frame->slide
// transform fitted from this frame's four chrome border landmarks (left 59, right 902,
// top 43, bottom 516  <->  slide 42, 919, 45, 540 — identical to certified slide_002):
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Badge cross-check: yellow-bbox center (875.5, 71.0) -> slide (891.4, 74.3) vs house
// (893, 71) — within JPEG-bbox noise (same as certified slide_002), same playlist template.
//
// CHROME LAW: shared playlist module shared_patterns/house_chrome.js, numeral 39.
//
// MEASURED FACTS honored here (frame = ground truth, overrides spec guesses):
//   * title "Normalization" Arial Bold 35 (ink w 229.9pt / cap-h fit), ink center x 453.4
//     (NOT slide-centered — measured as-is).
//   * blues measured navy ~#000080 (text cores (0,0,96)-(24,24,120)); spec's #0000CC was
//     a vision-model guess — frame wins.
//   * "Transforming the inputs to be" is BLACK REGULAR Arial 19 (measured stems 3px vs 5px
//     bold; w/h fit exact) — the spec validation had unified it to blue bold; frame wins.
//   * red text/borders CC0000 (spec; core bins consistent with C00000-family + JPEG).
//   * summary fill pale cyan ~E0FFFF (measured (237-239,255,254) deep interior; spec's
//     E8F2FF has G=242, measured G=255 saturated — frame wins).
//   * underlines measured: stmt2 'covariate shift' (frame x 213..335), b1 'stable
//     distribution of inputs,' (223..428), b2 'Accelerate the training' (99..269).
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): black letterbox strip
//     (frame rows 518..539, below slide bottom 516->540) and pen-cursor blob near
//     'inputs,' (~frame 393..410, 455..475).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "39")
drawHouseChrome(pres, s, { numeral: 39 });

const RED = "CC0000", NAVY = "000080", BLACK = "000000";
const pt = v => v / 72;
const K_AR = 0.9831, K_TS = 0.97; // baseline->boxTop lead (em) — closed-loop corrected

function textLine(id, runs, opts) {
  // runs: [{text, size, bold, color, font, italic, underline, charSpacing}]
  const maxAscent = Math.max(...runs.map(r => (r.options.fontFace === "Times New Roman" ? K_TS : K_AR) * r.options.fontSize));
  const maxSize = Math.max(...runs.map(r => r.options.fontSize));
  const o = {
    x: pt(opts.boxX), y: pt(opts.baseline - maxAscent),
    w: pt(opts.boxW), h: pt(1.6 * maxSize),
    align: opts.align || "left", valign: "top", margin: 0,
  };
  s.addText(runs.map(r => ({
    text: r.text,
    options: {
      fontSize: r.options.fontSize, bold: !!r.options.bold, italic: !!r.options.italic,
      color: r.options.color, fontFace: r.options.fontFace || "Arial",
      underline: r.options.underline, charSpacing: r.options.charSpacing,
    },
  })), o);
}

// ---- shapes FIRST (z-order under text): quote box, container, summary box, flow boxes, arrows, dots
function box(x, y, w, h, fill, lineColor, lineW) {
  s.addShape(pres.ShapeType.rect, {
    x: pt(x), y: pt(y), w: pt(w), h: pt(h),
    fill: { color: fill }, line: { color: lineColor, width: lineW },
  });
}
// quote box  frame[74,96,880,153] -> slide [57.6,100.5,896.1,160.1]
box(57.6, 100.5, 838.5, 59.7, "FFFFFF", RED, 2);
// big container  frame[72,162,878,397] -> slide [55.5,169.5,894.0,415.5]
box(55.5, 169.5, 838.5, 246.0, "FFFFFF", RED, 2);
// summary box  frame[72,410,878,503] -> slide [55.5,429.1,894.0,526.4]
box(55.5, 429.1, 838.5, 97.3, "E0FFFF", NAVY, 2);
// flow boxes (yellow fill, thin red border)  slide y 179.0..256.4
box(101.3, 179.0, 183.6, 77.4, "FFFFCC", RED, 1.5);   // box1 frame x 116..292
box(335.4, 179.0, 239.2, 77.4, "FFFFCC", RED, 1.5);   // box2 frame x 342..570
box(622.5, 179.0, 233.0, 77.4, "FFFFCC", RED, 1.5);   // box3 frame x 618..840

// arrows: thin red shafts with triangle heads (measured: shaft ~3px, head ~7px tall)
s.addShape(pres.ShapeType.line, {
  x: pt(285.4), y: pt(218.2), w: pt(50.0), h: 0,
  line: { color: RED, width: 2.5, endArrowType: "triangle" },
});
s.addShape(pres.ShapeType.line, {
  x: pt(574.6), y: pt(217.7), w: pt(48.9), h: 0,
  line: { color: RED, width: 2.5, endArrowType: "triangle" },
});

// bullet dots (measured 6px dia at frame (81..86, 447..452) and (81..86, 469..474))
s.addShape(pres.ShapeType.ellipse, {
  x: pt(67.5 - 3.15), y: pt(470.4 - 3.15), w: pt(6.3), h: pt(6.3),
  fill: { color: NAVY }, line: { color: NAVY, width: 0.5 },
});
s.addShape(pres.ShapeType.ellipse, {
  x: pt(67.5 - 3.15), y: pt(493.4 - 3.15), w: pt(6.3), h: pt(6.3),
  fill: { color: NAVY }, line: { color: NAVY, width: 0.5 },
});

// title: ArialB35.6 ink w=229.9 (closed-loop v3b: size 35->35.6, up 1.16pt, center +0.79)
textLine("title", [{text:"Normalization",options:{fontSize:35.6,bold:true,color:"CC0000",fontFace:"Arial"}}], {baseline: 86.74, boxX: 293.77, boxW: 320.9, align: "center"});
// quoteL1: TimesI22.2 (v3b: 22->22.2 width, boxX +1.73) ink w=811.5
textLine("quoteL1", [{text:"The behavior of machine learning algorithms  changes when the input distribution changes.",options:{fontSize:22.2,bold:false,italic:true,color:"000080",fontFace:"Times New Roman"}}], {baseline: 130.8, boxX: 65.63, boxW: 1072.7});
// covshift: TimesB20.5 + charSpacing 0.77 (v3b: LO serif 8% narrow; right edge +2.3, up 1.32)
textLine("covshift", [{text:"{Covariate shift }",options:{fontSize:20.5,bold:true,color:"CC0000",fontFace:"Times New Roman",charSpacing:0.77}}], {baseline: 154.08, boxX: 644.23, boxW: 217.3, align: "right"});
// f1l1: ArialB14.75 (v3b: 14.5->14.75 width) ink w=156.1
textLine("f1l1", [{text:"layer weights changes",options:{fontSize:14.75,bold:true,color:"CC0000",fontFace:"Arial"}}], {baseline: 202.0, boxX: 82.31, boxW: 221.2, align: "center"});
// f1l2: ArialB14.75 (v3b: 14.5->14.75 width) ink w=145.6
textLine("f1l2", [{text:"during training steps",options:{fontSize:14.75,bold:true,color:"000000",fontFace:"Arial"}}], {baseline: 235.5, boxX: 91.24, boxW: 207.5, align: "center"});
// f2l1: ArialB14 ink w=209.1
textLine("f2l1", [{text:"Outputs of Activation functions",options:{fontSize:14,bold:true,color:"CC0000",fontFace:"Arial"}}], {baseline: 204.2, boxX: 306.81, boxW: 291.4, align: "center"});
// f2l2: PIXEL-MEASURED split (v3b column profile): "of each layer " BLACK cores (1,2,0)
// (frame cols 389..471) + "change" RED cores (107,16,13) (frame cols 477..522) — the
// vision transcript's "all red" was a small-text misread; frame wins (fidelity law).
textLine("f2l2", [{text:"of each layer ",options:{fontSize:14,bold:true,color:"000000",fontFace:"Arial"}},{text:"change",options:{fontSize:14,bold:true,color:"CC0000",fontFace:"Arial"}}], {baseline: 231.3, boxX: 354.48, boxW: 200.1, align: "center"});
// f3l1: ArialB14 ink w=156.2
textLine("f3l1", [{text:"Inputs to the next layer,",options:{fontSize:14,bold:true,color:"000000",fontFace:"Arial"}}], {baseline: 204.2, boxX: 627.94, boxW: 223.1, align: "center"});
// f3l2: ArialB14 ink w=218.5
textLine("f3l2", [{text:"(With different Input distribution)",options:{fontSize:14,bold:true,color:"CC0000",fontFace:"Arial"}}], {baseline: 231.3, boxX: 587.58, boxW: 304.1, align: "center"});
// conclusion: ArialB16.5 + charSpacing 0.55 (v3b: width -5.7pt at matched height), up 0.79
textLine("conclusion", [{text:"Conclusion:",options:{fontSize:16.5,bold:true,color:"CC0000",fontFace:"Arial",charSpacing:0.55}}], {baseline: 276.51, boxX: 72.20, boxW: 143.8});
// stmt1: ArialB18.4 (v3b: 18.5->18.4 width) ink w=484.8
textLine("stmt1", [{text:"Input distribution of each layer changes with each step .",options:{fontSize:18.4,bold:true,color:"000080",fontFace:"Arial"}}], {baseline: 301.4, boxX: 151.30, boxW: 661.6});
// idea: ArialB18.5 ink w=366.2 (v3b: within tol, unchanged)
textLine("idea", [{text:"The basic idea behind Normalization is to:",options:{fontSize:18.5,bold:true,color:"CC0000",fontFace:"Arial"}}], {baseline: 341.2, boxX: 72.20, boxW: 501.0});
// stmt2: ArialB18.7 (v3b: 18.5->18.7 width) ink w=567.0
textLine("stmt2", [{text:"Limit ",options:{fontSize:18.7,bold:true,color:NAVY,fontFace:"Arial"}},{text:"covariate shift",options:{fontSize:18.7,bold:true,color:NAVY,fontFace:"Arial",underline:{style:"sng"}}},{text:" by normalizing the activations of each layer",options:{fontSize:18.7,bold:true,color:NAVY,fontFace:"Arial"}}], {baseline: 365.3, boxX: 152.30, boxW: 752.9});
// lineC SPLIT into its three verbatim runs as separately-positioned boxes (v3b: runs 2-3
// rendered ~3.5pt left of the original's run boundaries as one box — inter-run gap metrics;
// split keeps every character verbatim, fixes run x to measured ink 73.2 / 213.7 / 466.5).
// Shared-baseline preserved: trans box baseline raised by its ascent delta (18.68-18.19=0.49).
textLine("lc_norm", [{text:"Normalization:  ",options:{fontSize:18.5,bold:true,color:RED,fontFace:"Arial"}}], {baseline: 406.0, boxX: 72.20, boxW: 200});
textLine("lc_trans", [{text:"Transforming the inputs to be ",options:{fontSize:19,bold:false,color:BLACK,fontFace:"Arial",charSpacing:0.08}}], {baseline: 406.49, boxX: 212.8, boxW: 300});
textLine("lc_zero", [{text:"Zero mean and unit variance.",options:{fontSize:18.5,bold:true,color:NAVY,fontFace:"Arial"}}], {baseline: 406.0, boxX: 465.6, boxW: 300});
// sumhead: ArialB18.7 (v3b: 18.5->18.7 width) ink w=307.9
textLine("sumhead", [{text:"Normalization allows each layer to:",options:{fontSize:18.7,bold:true,color:"CC0000",fontFace:"Arial"}}], {baseline: 453.2, boxX: 66.00, boxW: 421.1});
// b1: ArialB16.25 (v3b rounds: 16.5->16.3->16.25 width), up 1.0pt
textLine("b1", [{text:"learn on a more ",options:{fontSize:16.25,bold:true,color:NAVY,fontFace:"Arial"}},{text:"stable distribution of inputs,",options:{fontSize:16.25,bold:true,color:NAVY,fontFace:"Arial",underline:{style:"sng"}}}], {baseline: 477.4, boxX: 83.70, boxW: 474.0});
// b2: ArialB16.34 (v3b rounds: 16.5->16.4->16.25->16.34 interpolated width), up 0.6pt
textLine("b2", [{text:"Accelerate the training",options:{fontSize:16.34,bold:true,color:NAVY,fontFace:"Arial",underline:{style:"sng"}}},{text:" of the network (don't stick with very small learning rates).",options:{fontSize:16.34,bold:true,color:NAVY,fontFace:"Arial"}}], {baseline: 499.3, boxX: 82.60, boxW: 842.9});

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_039_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
