// components/slide_017.js — slide 017 "Encoder – Decoder Transformer" certified composition.
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slides 18 and 19 build on this
// composition. They MUST require() this module and call renderBase(pptx, slide, opts)
// (or cherry-pick blocks via opts.skip / opts.only) — NEVER re-derive or copy-paste
// this geometry. Child 18 replaces the left annotation column (callouts+leaders) with
// banners + Figure-2 insets; child 19 replaces the banners with normalization/FFN/
// residual callouts. The Figure-1 body blocks (enc_*, dec_*, feeds, feedback, ...) are
// drawn identically for all three slides.
//
// Block granularity (one function per visual block, in z-order):
//   title, callout1..4, leader1..4, fig_frame, panels, panel_labels, yellow_band,
//   enc_stack, enc_vkq, enc_pe, enc_embed, enc_base, enc_nx,
//   dec_stack, dec_purple, dec_vkq_masked, dec_top, dec_spine, dec_pe, dec_embed,
//   dec_base, dec_nx, green_trunk, feeds, feedback.
//
// GEOMETRY PROVENANCE: PIL-measured from unique_slides/slide_017.jpg (960x540, 1px=1pt,
// in = px/72) — scanline runs, per-color component maps, mode fill sampling
// (scratch/slide017/m0..m22), plus vision probes of 6 crops through the gate
// (probe_enc/dec/gap/decbot/encbot/penc/decgap/opband.txt). Structure cross-checked
// against the paper's Figure 1 (arXiv 1706.03762v7, banked in slide_18_source/).
//
// LAWS honored: playlist chrome via components/house_chrome.js (drawn ONCE here);
// verbatim text incl. curly quotes (“t-1”, “t”) and the spaced "N x" repeat glyph per
// the gate-passed spec; margin:0 + explicit fontFace everywhere; explicit lineSpacing
// on every multi-line box; no '#' in hex; dashed feedback + thin connectors as native
// lines; the faint gray callout leader lines (measured at y151/245-254/364-379/492).

const { drawHouseChrome } = require("./house_chrome.js");

const px = (v) => v / 72;

// ---- palette (JPEG-core measured) --------------------------------------------
const C = {
  titleRed: "C00000",
  calloutYellow: "FFFF99",   // measured (248,248,152)
  calloutPink: "F0B0F8",     // measured (240,176,248)
  calloutTan: "D8C8B8",      // measured (216,200,184)
  calloutBlue: "00008B",     // measured core (3,0,84)
  calloutPurple: "9900CC",
  calloutDarkRed: "943634",
  pinkLineRed: "C00000",
  frameGreen: "00A000",      // measured cores (14,136,15)/(16,135,17)
  encPanel: "FBECDB",        // measured (251,236,219)
  decPanel: "C8F8E0",        // measured (200,248,224)
  tanFill: "C8A888",         // encoder container / nodes (200,168,136)
  tanBorder: "7B4B2A",
  brownFill: "B08058",       // encoder embedding block (176,128,88)
  brownBorder: "6E4423",
  oliveFill: "B0B070",       // FF inset + decoder stack (176,176,112)
  maroonFill: "B8706C",      // decoder embedding block (184,112,108)
  maroonBorder: "753029",
  purpleFill: "CE8ADC",     // measured (205,138,220)
  purpleBorder: "562366",   // measured (86,35,102)
  softmaxFill: "A8ECBC",     // measured mode (168,236,188)
  linearFill: "B0E4CE",      // measured mode (176,228,206)
  vkBlue: "2A26A0",          // measured cores (36,32,144)/(46,38,170)
  qRed: "C00000",
  yellow: "FFFF00",
  ink: "1A1A1A",
  line: "333333",
  spine: "2F2F2F",
  decBorder: "4A7360",       // decoder stack border (measured (70,115,84))
  feedback: "6B2A28",        // dashed feedback curve (measured (80,40,40))
  leader: "C8C8C8",
  decGreenText: "0E7D10",    // "Decoder" label (measured (13,125,15))
  shiftedGreen: "3C8C3C",    // "(shifted right)" green text
  embText: "331111",
};
const SANS = "Arial";

// ---- helpers -------------------------------------------------------------------

function addLines(slide, color, width, pts, opts = {}) {
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0] = pts[i];
    const [x1, y1] = pts[i + 1];
    const line = { color, width };
    if (opts.dash) line.dashType = opts.dash;
    if (opts.endArrow && i === pts.length - 2) line.endArrowType = "triangle";
    slide.addShape("line", {
      x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
      w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
      flipV: y1 < y0, flipH: x1 < x0,
      line,
    });
  }
}

function plusGlyph(slide, cx, cy, r, color, width) {
  addLines(slide, color, width, [[cx - r, cy], [cx + r, cy]]);
  addLines(slide, color, width, [[cx, cy - r], [cx, cy + r]]);
}

function sineGlyph(slide, cx, cy, w, h, color, width) {
  // 4-segment zigzag approximating the measured squiggle
  const x0 = cx - w / 2;
  addLines(slide, color, width, [
    [x0, cy + h / 2], [x0 + w * 0.25, cy - h / 2],
    [x0 + w * 0.5, cy + h / 2], [x0 + w * 0.75, cy - h / 2], [x0 + w, cy + h / 2],
  ]);
}

function vLetterCircle(slide, cx, cy, d, fill, letter, fontSize) {
  slide.addShape("ellipse", {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: fill }, line: { color: fill, width: 0.5 },
  });
  slide.addText(letter, {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize, bold: true, color: "FFFFFF",
  });
}

// ---- block functions (z-order = call order) ------------------------------------

function drawTitle(pptx, slide) {
  slide.addText("Encoder – Decoder Transformer", {
    x: px(140), y: px(48), w: px(680), h: px(44),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 36, bold: true, color: C.titleRed,
  });
}

function drawCallout1(pptx, slide) {
  slide.addShape("rect", {
    x: px(103), y: px(120), w: px(425), h: px(63), fill: { color: C.calloutYellow },
  });
  slide.addText(
    [
      { text: "Decoder Output (at step “t-1”)", options: { breakLine: true } },
      { text: "Is supplied as Decoder Input (at step “t”)", options: {} },
    ],
    {
      x: px(103), y: px(120), w: px(425), h: px(63),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 17, bold: true, color: C.calloutBlue,
      lineSpacing: 22,
    }
  );
}

function drawCallout2(pptx, slide) {
  slide.addShape("rect", {
    x: px(183), y: px(211), w: px(305), h: px(67), fill: { color: C.calloutPink },
  });
  slide.addText(
    [
      { text: "First Decoder Block", options: { color: C.calloutPurple, fontSize: 18, breakLine: true } },
      { text: "No Input from Encoder Attention", options: { color: C.pinkLineRed, fontSize: 16 } },
    ],
    {
      x: px(183), y: px(211), w: px(305), h: px(67),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, bold: true, lineSpacing: 22,
    }
  );
}

function drawCallout3(pptx, slide) {
  slide.addShape("rect", {
    x: px(103), y: px(340), w: px(419), h: px(50), fill: { color: C.calloutTan },
  });
  slide.addText(
    [
      { text: "Input Positional Encoder", options: { fontSize: 18, breakLine: true } },
      { text: "(Position of Input Word within the Input Sequence)", options: { fontSize: 14 } },
    ],
    {
      x: px(103), y: px(340), w: px(419), h: px(50),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, bold: true, color: C.calloutDarkRed, lineSpacing: 21,
    }
  );
}

function drawCallout4(pptx, slide) {
  slide.addShape("rect", {
    x: px(87), y: px(469), w: px(445), h: px(47), fill: { color: C.calloutTan },
  });
  slide.addText(
    [
      { text: "Output Positional Encoder", options: { fontSize: 18, breakLine: true } },
      { text: "(Position of Output Word within the Output Sequence)", options: { fontSize: 14 } },
    ],
    {
      x: px(87), y: px(469), w: px(445), h: px(47),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, bold: true, color: C.calloutDarkRed, lineSpacing: 21,
    }
  );
}

function drawLeader1(pptx, slide) {
  addLines(slide, C.leader, 0.75, [[530, 151], [572, 151]]);
}
function drawLeader2(pptx, slide) {
  addLines(slide, C.leader, 0.75, [[521, 245], [572, 254]]);
}
function drawLeader3(pptx, slide) {
  addLines(slide, C.leader, 0.75, [[523, 365], [572, 379]]);
}
function drawLeader4(pptx, slide) {
  addLines(slide, C.leader, 0.75, [[533, 492], [572, 492]]);
}

function drawFigFrame(pptx, slide) {
  slide.addShape("rect", {
    x: px(572), y: px(103), w: px(324), h: px(423),
    fill: { type: "none" }, line: { color: C.frameGreen, width: 1.5 },
  });
}

function drawPanels(pptx, slide) {
  slide.addShape("rect", {
    x: px(577), y: px(108), w: px(161), h: px(414), fill: { color: C.encPanel },
  });
  slide.addShape("rect", {
    x: px(740), y: px(108), w: px(154), h: px(414), fill: { color: C.decPanel },
  });
}

function drawPanelLabels(pptx, slide) {
  slide.addText("Encoder", {
    x: px(581), y: px(112), w: px(84), h: px(20),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 13, bold: true, italic: true, color: C.titleRed,
  });
  slide.addText("Decoder", {
    x: px(818), y: px(112), w: px(72), h: px(20),
    align: "right", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 13, bold: true, italic: true, color: C.decGreenText,
  });
}

function drawYellowBand(pptx, slide) {
  // L-shaped highlight of the encoder->decoder V/K paths + flare over the circles
  slide.addShape("rect", { x: px(678), y: px(251), w: px(67), h: px(16), fill: { color: C.yellow } });
  slide.addShape("rect", { x: px(730), y: px(267), w: px(15), h: px(41), fill: { color: C.yellow } });
  slide.addShape("rect", { x: px(740), y: px(307), w: px(47), h: px(16), fill: { color: C.yellow } });
}

function drawEncStack(pptx, slide) {
  // outer container (Add&Norm / FeedForward / Add&Norm / Multi-Head Attention)
  slide.addShape("roundRect", {
    x: px(628), y: px(267), w: px(100), h: px(142), rectRadius: 0.06,
    fill: { color: C.tanFill }, line: { color: C.tanBorder, width: 1.25 },
  });
  // sub-box separators (the original draws the sub-layers as distinct outlined boxes)
  addLines(slide, C.tanBorder, 0.5, [[630, 287.5], [725, 287.5]]);
  addLines(slide, C.tanBorder, 0.5, [[630, 315.5], [725, 315.5]]);
  addLines(slide, C.tanBorder, 0.5, [[630, 357.5], [725, 357.5]]);
  // residual curves hugging the inside-left (measured verticals)
  addLines(slide, C.tanBorder, 0.75, [[632, 292], [632, 404]]);
  addLines(slide, C.tanBorder, 0.75, [[642, 318], [642, 344]]);
  // Feed Forward inset box (olive)
  slide.addShape("rect", {
    x: px(651), y: px(288), w: px(69), h: px(27),
    fill: { color: C.oliveFill }, line: { color: C.tanBorder, width: 0.75 },
  });
  slide.addText(
    [
      { text: "Feed", options: { breakLine: true } },
      { text: "Forward", options: {} },
    ],
    {
      x: px(651), y: px(288), w: px(69), h: px(27),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: C.ink, lineSpacing: 11,
    }
  );
  slide.addText("Add & Norm", {
    x: px(630), y: px(267), w: px(97), h: px(20),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: C.ink,
  });
  slide.addText("Add & Norm", {
    x: px(630), y: px(334), w: px(97), h: px(28),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: C.ink,
  });
  slide.addText(
    [
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(630), y: px(356), w: px(97), h: px(30),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: C.ink, lineSpacing: 11,
    }
  );
  // small up-arrows between the sub-layer compartments (measured stub marks)
  for (const ya of [284, 313, 355]) {
    slide.addShape("triangle", {
      x: px(674.5), y: px(ya), w: px(6), h: px(4.5),
      fill: { color: C.tanBorder }, line: { color: C.tanBorder, width: 0.5 },
    });
  }
}

function drawEncVkq(pptx, slide) {
  vLetterCircle(slide, 663.5, 400.5, 12, C.vkBlue, "V", 7);
  vLetterCircle(slide, 695, 400.5, 11, C.vkBlue, "K", 7);
  vLetterCircle(slide, 717.5, 400.5, 11, C.qRed, "Q", 7);
}

function drawEncPe(pptx, slide) {
  // spine stubs: container bottom -> PE node -> embedding block (up-arrow into block)
  addLines(slide, C.spine, 0.75, [[686.5, 409], [686.5, 415]]);
  addLines(slide, C.spine, 0.75, [[686.5, 445], [686.5, 452]], { endArrow: false });
  // small upward arrowhead on the lower stub
  slide.addShape("triangle", {
    x: px(683), y: px(443.5), w: px(7), h: px(6),
    fill: { color: C.spine }, line: { color: C.spine, width: 0.5 },
  });
  // PE node box (dark brown, measured mode (176,128,88)) with plus-in-circle + sine
  slide.addShape("roundRect", {
    x: px(649), y: px(415), w: px(79), h: px(30), rectRadius: 0.05,
    fill: { color: C.brownFill }, line: { color: C.brownBorder, width: 1 },
  });
  slide.addShape("ellipse", {
    x: px(649), y: px(420), w: px(19), h: px(19),
    fill: { type: "none" }, line: { color: "6E4423", width: 1.25 },
  });
  plusGlyph(slide, 658.5, 429.5, 5.5, "6E4423", 1.25);
  sineGlyph(slide, 686, 430, 24, 8, "6E4423", 1);
  // label at left
  slide.addText(
    [
      { text: "Positional", options: { breakLine: true } },
      { text: "Encoding", options: {} },
    ],
    {
      x: px(594), y: px(416), w: px(56), h: px(28),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: "404040", lineSpacing: 12,
    }
  );
}

function drawEncEmbed(pptx, slide) {
  // horizontal double-headed bus at embedding level (behind the block)
  addLines(slide, C.line, 0.75, [[648, 449], [736, 449]]);
  slide.addShape("rect", {
    x: px(636), y: px(444), w: px(91), h: px(40), rectRadius: 0.05,
    fill: { color: C.brownFill }, line: { color: C.brownBorder, width: 1 },
  });
  // inner tan label box
  slide.addShape("rect", {
    x: px(653), y: px(446), w: px(68), h: px(25),
    fill: { color: C.tanFill }, line: { color: C.brownBorder, width: 0.75 },
  });
  slide.addText(
    [
      { text: "Input", options: { breakLine: true } },
      { text: "Embedding", options: {} },
    ],
    {
      x: px(653), y: px(446), w: px(68), h: px(25),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.embText, lineSpacing: 10.5,
    }
  );
  // bus arrowheads (over the block edges, as measured)
  slide.addShape("triangle", {
    x: px(640), y: px(446), w: px(8), h: px(7), flipH: true,
    fill: { color: C.line }, line: { color: C.line, width: 0.5 },
  });
  slide.addShape("triangle", {
    x: px(737), y: px(446), w: px(8), h: px(7),
    fill: { color: C.line }, line: { color: C.line, width: 0.5 },
  });
}

function drawEncBase(pptx, slide) {
  // thick red up arrow: shaft + head
  slide.addShape("rect", {
    x: px(654.5), y: px(495), w: px(10), h: px(18),
    fill: { color: C.qRed }, line: { color: C.line, width: 0.5 },
  });
  slide.addShape("triangle", {
    x: px(651), y: px(488), w: px(17), h: px(8),
    fill: { color: C.qRed }, line: { color: C.line, width: 0.5 },
  });
  slide.addText("Inputs", {
    x: px(664), y: px(494), w: px(44), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, color: C.ink,
  });
}

function drawEncNx(pptx, slide) {
  slide.addShape("ellipse", {
    x: px(597.5), y: px(329.5), w: px(25), h: px(25),
    fill: { color: C.tanFill }, line: { color: C.tanBorder, width: 0.75 },
  });
  slide.addText("N x", {
    x: px(597.5), y: px(329.5), w: px(25), h: px(25),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 8, bold: true, color: "333333",
  });
}

function drawDecStack(pptx, slide) {
  // olive container: A&N / FF / A&N / Multi-Head Attention
  slide.addShape("roundRect", {
    x: px(744), y: px(201), w: px(97), h: px(105), rectRadius: 0.05,
    fill: { color: C.oliveFill }, line: { color: C.decBorder, width: 1 },
  });
  addLines(slide, C.decBorder, 0.75, [[745, 219.5], [840, 219.5]]);
  addLines(slide, C.decBorder, 0.75, [[745, 249.5], [840, 249.5]]);
  addLines(slide, C.decBorder, 0.75, [[745, 264.5], [840, 264.5]]);
  // faint interior verticals (measured x753 / x818 / x822 residual channel)
  addLines(slide, "4A4A4A", 0.5, [[753.5, 202], [753.5, 305]]);
  addLines(slide, "4A4A4A", 0.5, [[818.5, 202], [818.5, 305]]);
  slide.addText("Add & Norm", {
    x: px(746), y: px(202), w: px(94), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9.5, bold: true, color: C.ink,
  });
  slide.addText(
    [
      { text: "Feed", options: { breakLine: true } },
      { text: "Forward", options: {} },
    ],
    {
      x: px(746), y: px(221), w: px(94), h: px(28),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: C.ink, lineSpacing: 11,
    }
  );
  slide.addText("Add & Norm", {
    x: px(746), y: px(250), w: px(94), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9.5, bold: true, color: C.ink,
  });
  slide.addText(
    [
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(746), y: px(265), w: px(94), h: px(40),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: C.ink, lineSpacing: 11,
    }
  );
}

function drawDecPurple(pptx, slide) {
  // purple container: [Add & Norm] / [Masked Multi-Head Attention] / V-K-Q row,
  // with the residual channel line at x818.5 (measured full-height vertical)
  slide.addShape("roundRect", {
    x: px(746), y: px(327), w: px(88), h: px(81), rectRadius: 0.06,
    fill: { color: C.purpleFill }, line: { color: C.purpleBorder, width: 1 },
  });
  addLines(slide, C.purpleBorder, 0.75, [[748, 330.5], [817, 330.5]]);
  addLines(slide, C.purpleBorder, 0.75, [[748, 347.5], [817, 347.5]]);
  addLines(slide, C.purpleBorder, 0.75, [[748, 383.5], [817, 383.5]]);
  addLines(slide, C.purpleBorder, 0.75, [[818.5, 330], [818.5, 406]]);
  slide.addText("Add & Norm", {
    x: px(748), y: px(331), w: px(69), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 8, bold: true, color: C.ink,
  });
  slide.addText(
    [
      { text: "Masked", options: { breakLine: true } },
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(748), y: px(348), w: px(69), h: px(35),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.ink, lineSpacing: 10.5,
    }
  );
}

function drawDecVkqMasked(pptx, slide) {
  vLetterCircle(slide, 752, 391.5, 13, C.vkBlue, "V", 7);
  vLetterCircle(slide, 795, 391.5, 15, C.vkBlue, "K", 7);
  vLetterCircle(slide, 821.5, 391.5, 11, C.qRed, "Q", 7);
}

function drawDecVkqCross(pptx, slide) {
  vLetterCircle(slide, 748.5, 316, 10, C.vkBlue, "V", 6.5);
  vLetterCircle(slide, 773, 316.5, 9, C.vkBlue, "K", 6.5);
  vLetterCircle(slide, 820, 316.5, 10, C.qRed, "Q", 6.5);
}

function drawDecTop(pptx, slide) {
  // red up-arrow + dark line at the decoder's top-left (as measured)
  slide.addShape("rect", {
    x: px(742), y: px(119), w: px(8), h: px(21),
    fill: { color: C.qRed }, line: { color: C.qRed, width: 0.5 },
  });
  slide.addShape("triangle", {
    x: px(748), y: px(114.5), w: px(13), h: px(9),
    fill: { color: C.qRed }, line: { color: C.qRed, width: 0.5 },
  });
  addLines(slide, C.line, 0.75, [[741, 117], [741, 139]]);
  // Output Probabilities: yellow band + two tiny bold lines
  slide.addShape("roundRect", {
    x: px(761), y: px(112), w: px(51), h: px(16), rectRadius: 0.04,
    fill: { color: C.yellow },
  });
  slide.addText("Output", {
    x: px(761), y: px(112), w: px(51), h: px(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 8, color: C.ink,
  });
  slide.addText("Probabilities", {
    x: px(756), y: px(127), w: px(60), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 8, color: C.ink,
  });
  // Softmax / Linear boxes
  slide.addShape("rect", {
    x: px(752), y: px(152), w: px(67), h: px(14),
    fill: { color: C.softmaxFill }, line: { color: C.line, width: 0.75 },
  });
  slide.addText("Softmax", {
    x: px(752), y: px(152), w: px(67), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9, bold: true, color: C.ink,
  });
  slide.addShape("rect", {
    x: px(752), y: px(177), w: px(67), h: px(14),
    fill: { color: C.linearFill }, line: { color: C.line, width: 0.75 },
  });
  slide.addText("Linear", {
    x: px(752), y: px(177), w: px(67), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9, bold: true, color: C.ink,
  });
}

function drawDecSpine(pptx, slide) {
  // center connector segments (measured x785, gaps only where boxes sit)
  addLines(slide, C.spine, 0.75, [[785.5, 141], [785.5, 152]]);
  addLines(slide, C.spine, 0.75, [[785.5, 165], [785.5, 177]]);
  addLines(slide, C.spine, 0.75, [[785.5, 191], [785.5, 201]]);
  addLines(slide, C.spine, 0.75, [[785.5, 306], [785.5, 491]]);
  // upward arrowheads on the segment tops (into Output Probabilities / Softmax / Linear)
  for (const ya of [141.5, 165.5, 191.5]) {
    slide.addShape("triangle", {
      x: px(782.5), y: px(ya), w: px(6), h: px(5),
      fill: { color: C.spine }, line: { color: C.spine, width: 0.5 },
    });
  }
}

function drawDecPe(pptx, slide) {
  // plus-in-circle on the spine + sine circle to its right (dark outlines)
  slide.addShape("ellipse", {
    x: px(777), y: px(411.5), w: px(16), h: px(16),
    fill: { color: C.decPanel }, line: { color: C.spine, width: 1.25 },
  });
  plusGlyph(slide, 785, 419.5, 4.5, C.spine, 1.25);
  addLines(slide, C.spine, 1.25, [[793, 419.5], [796, 419.5]]);
  slide.addShape("ellipse", {
    x: px(795), y: px(411), w: px(18), h: px(18),
    fill: { color: C.decPanel }, line: { color: C.spine, width: 1.25 },
  });
  sineGlyph(slide, 804, 420, 11, 7, C.spine, 1);
  slide.addText(
    [
      { text: "Positional", options: { breakLine: true } },
      { text: "Encoding", options: {} },
    ],
    {
      x: px(836), y: px(419), w: px(48), h: px(28),
      align: "left", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9.5, bold: true, color: "333333", lineSpacing: 12,
    }
  );
}

function drawDecEmbed(pptx, slide) {
  slide.addShape("roundRect", {
    x: px(749), y: px(417), w: px(76), h: px(65), rectRadius: 0.05,
    fill: { color: C.maroonFill }, line: { color: C.maroonBorder, width: 1 },
  });
  slide.addShape("rect", {
    x: px(756), y: px(446), w: px(63), h: px(25),
    fill: { type: "none" }, line: { color: C.maroonBorder, width: 0.75 },
  });
  slide.addText(
    [
      { text: "Output", options: { breakLine: true } },
      { text: "Embedding", options: {} },
    ],
    {
      x: px(756), y: px(446), w: px(63), h: px(25),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.embText, lineSpacing: 10.5,
    }
  );
}

function drawDecBase(pptx, slide) {
  slide.addShape("rect", {
    x: px(761), y: px(492), w: px(51), h: px(19), fill: { color: C.yellow },
  });
  slide.addText("Outputs", {
    x: px(761), y: px(492), w: px(51), h: px(19),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 11, bold: true, color: C.ink,
  });
  slide.addText("(shifted right)", {
    x: px(748), y: px(508), w: px(76), h: px(14),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9, bold: true, color: C.shiftedGreen,
  });
}

function drawDecNx(pptx, slide) {
  slide.addShape("ellipse", {
    x: px(845.5), y: px(300.5), w: px(21), h: px(21),
    fill: { color: C.oliveFill }, line: { color: C.decBorder, width: 0.75 },
  });
  slide.addText("N x", {
    x: px(845.5), y: px(300.5), w: px(21), h: px(21),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 7.5, bold: true, color: "333333",
  });
}

function drawGreenTrunk(pptx, slide) {
  // dark-green vertical line hugging the decoder stack's right (measured x841, y203..415)
  addLines(slide, C.decBorder, 1, [[841, 203], [841, 415]]);
}

function drawFeeds(pptx, slide) {
  // the two thin V/K feed paths encoder -> decoder MHA circles (inside the yellow band)
  addLines(slide, C.line, 0.75, [[692, 267], [692, 258], [736, 258], [736, 311], [743.5, 311]]);
  addLines(slide, C.line, 0.75, [[700, 267], [700, 262], [741, 262], [741, 316], [768.5, 316]]);
}

function drawFeedback(pptx, slide) {
  // red dashed S-curve: Output Probabilities band -> right side -> Outputs (arrowhead at end)
  addLines(slide, C.feedback, 1.25, [
    [820, 119], [850, 150], [876, 200], [888, 300], [884, 420], [818, 492],
  ], { dash: "dashDot", endArrow: true });
}

// ---- composition ----------------------------------------------------------------

const BLOCKS = {
  title: drawTitle,
  callout1: drawCallout1,
  callout2: drawCallout2,
  callout3: drawCallout3,
  callout4: drawCallout4,
  leader1: drawLeader1,
  leader2: drawLeader2,
  leader3: drawLeader3,
  leader4: drawLeader4,
  fig_frame: drawFigFrame,
  panels: drawPanels,
  panel_labels: drawPanelLabels,
  yellow_band: drawYellowBand,
  enc_stack: drawEncStack,
  enc_vkq: drawEncVkq,
  enc_pe: drawEncPe,
  enc_embed: drawEncEmbed,
  enc_base: drawEncBase,
  enc_nx: drawEncNx,
  dec_stack: drawDecStack,
  dec_purple: drawDecPurple,
  dec_vkq_masked: drawDecVkqMasked,
  dec_vkq_cross: drawDecVkqCross,
  dec_top: drawDecTop,
  dec_spine: drawDecSpine,
  dec_pe: drawDecPe,
  dec_embed: drawDecEmbed,
  dec_base: drawDecBase,
  dec_nx: drawDecNx,
  green_trunk: drawGreenTrunk,
  feeds: drawFeeds,
  feedback: drawFeedback,
};

/**
 * Draw the full slide-017 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 17 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px };
