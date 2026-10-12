// components/slide_026.js — slide 026 "Sin/Cos Encoders" composition (TIDA-00176 block diagram).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11): slide 028 builds on this composition
// (28 ← [27, 26]) and slide 049 re-uses its verified patterns (49 ← 26). Children MUST
// require() this module and call renderBase(pptx, slide, opts) (or cherry-pick blocks via
// opts.skip / opts.only) — NEVER re-derive or copy-paste this geometry.
//
// Block granularity: every visual block is its own function; renderBase accepts
//   opts.skip   — array of block names to OMIT (child removes inherited blocks)
//   opts.only   — array of block names to DRAW exclusively (child replaces composition)
//   opts.chrome — draw house chrome (default true; chrome via the playlist shared
//                 shared_patterns/house_chrome.js primitive)
//   opts.numeral— badge numeral (default 26)
// Block names: white_panel, tida_container, corridor_lines, blue_box, host_bar,
//   corridor_labels, path16, path_analog, comparators, power_row, enc_connector,
//   right_rect, wires, right_contents, pos_arrow, title, subtitle, captions.
// Z-ORDER IS LOAD-BEARING: right_rect MUST be drawn before wires/right_contents (the wire
// fan and signal labels sit on top of it); the analog dashed group before its white label
// box (the box overlaps the group's top edge); corridor_lines before the bars.
//
// GEOMETRY PROVENANCE (certified 2026-10-12, judge PASS attempt 2): PIL-measured from
// unique_slides/slide_026.jpg (960x540) through the frame->slide mapping fitted from THIS
// frame's chrome landmarks (identical to 002 build/slide_002.js):
//   frame_x = 18.628 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Colors are PIL-census modes per region; micro-wires + AC-motor art are exact-size images
// (assets/slide026_wires.png, assets/slide026_motor.png). Verbatim text incl. corridor
// "A, B, R" and callout "A+, A-, B+, B- and Marker R+/R-" (frame+guide TIDUA05B Fig 1-1
// + slide_026_source/SOURCES.md; the spec JSON's "A, B," / ", and Marker R+, R-" were
// analysis misreads, corrected per the frame-wins law).

const path = require("path");
const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const ASSETS = path.join(__dirname, "..", "assets");

// ---- palette (PIL census cores) ----
const C = {
  titleRed: "C00000",
  subtitleBlue: "1A1AC8",
  blueBox: "0EBFEB", blueBoxLine: "0D89B8",
  sub1: "F5D5BC", sub2: "D6E6BF", sub3: "FFFFFF",
  container: "C4DCA0", containerDash: "6D775C",
  groupDash: "6E6A28", groupFill: "F6D7BC",
  white: "FFFFFF", boxLine: "9C9C9C",
  pentagon: "E99968", tri: "6CCE93",
  compBox: "ECE9F0",
  powerSup: "D0BA6F",
  gray: "D7D7D7",
  diffBox: "F1D3B2",
  rrBorder: "1E753E",
  motorBody: "A5A5A5", motorBox: "C9C9C9",
  ink: "1A1A1A", ink2: "333333",
  posRed: "B00011",
};
const F = "Arial";
const px = (v) => v / 72; // slide pt -> inches

// mapping helpers (frame px -> slide inches)
const MX = 18.628, SX = 0.96123, SY = 0.95556;
const x = (fx) => px((fx - MX) / SX);
const y = (fy) => px(fy / SY);
const w = (fw) => px(fw / SX);
const h = (fh) => px(fh / SY);

// ---- block functions ---------------------------------------------------------

function drawWhitePanel(pptx, slide) {
  // frame 218..861 x 158..471
  slide.addShape(pptx.ShapeType.rect, {
    x: x(218), y: y(158), w: w(861 - 218), h: h(471 - 158),
    fill: { color: C.white }, line: { type: "none" },
  });
}

function drawTidaContainer(pptx, slide) {
  // dashed green, frame 402..658 x 187..467
  slide.addShape(pptx.ShapeType.rect, {
    x: x(402), y: y(187), w: w(658 - 402), h: h(467 - 187),
    fill: { color: C.container }, line: { color: C.containerDash, width: 1, dashType: "dash" },
  });
  // white tag box (568..664 x 191..213) + text
  slide.addShape(pptx.ShapeType.rect, {
    x: x(568), y: y(191), w: w(664 - 568), h: h(213 - 191),
    fill: { color: C.white }, line: { type: "none" },
  });
  slide.addText("TIDA-00176", {
    x: x(568), y: y(191), w: w(664 - 568), h: h(213 - 191),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 11.5, bold: true, color: C.ink,
  });
}

function line(slide, pptx, x0, y0, x1, y1, opt = {}) {
  slide.addShape(pptx.ShapeType.line, {
    x: x(x0), y: y(y0), w: w(x1 - x0), h: h(y1 - y0),
    line: { color: opt.color || C.ink, width: opt.width || 1.75,
      beginArrowType: opt.begin || "none", endArrowType: opt.end || "none" },
  });
}

function drawCorridorLines(pptx, slide) {
  // top corridor (frame y263): right arrowhead into the 16-bit path group
  line(slide, pptx, 379, 263, 460, 263, { end: "triangle" });
  // middle corridor (frame y318): left arrowhead into the blue box
  line(slide, pptx, 379, 318, 456, 318, { begin: "triangle" });
  // bottom corridor (frame y376): left arrowhead into the blue box
  line(slide, pptx, 379, 376, 458, 376, { begin: "triangle" });
  // output collector bus (frame x625, y262..445, dark olive)
  line(slide, pptx, 625, 262, 625, 445, { color: "3E5425" });
  // path output arrows (frame-measured)
  line(slide, pptx, 579, 263, 626, 263, { end: "triangle" });   // 16-bit path out -> bus
  line(slide, pptx, 579, 318, 651, 318, { end: "triangle" });   // analog path out -> connector
  line(slide, pptx, 624, 348, 651, 348, { end: "triangle" });   // comparators out -> connector
  // encoder supply line (frame y445 from Power Supplies toward connector)
  line(slide, pptx, 528, 445, 660, 445);
}

function drawBlueBox(pptx, slide) {
  // frame 231..379 x 239..387
  slide.addShape(pptx.ShapeType.rect, {
    x: x(231), y: y(239), w: w(379 - 231), h: h(387 - 239),
    fill: { color: C.blueBox }, line: { color: C.blueBoxLine, width: 1 },
  });
  // sub-block 1 (233..320 x 252..284) peach
  slide.addShape(pptx.ShapeType.rect, { x: x(233), y: y(252), w: w(320 - 233), h: h(284 - 252), fill: { color: C.sub1 }, line: { type: "none" } });
  slide.addText([
    { text: "Fine Angle: ", options: { color: C.titleRed, bold: true, underline: { style: "sng", color: "1A1A1A" } } },
    { text: "atan(A/B)", options: { color: C.ink, bold: true, breakLine: true, underline: { style: "sng", color: "1A1A1A" } } },
    { text: "\u2192 Option 1: 16 bit", options: { color: C.ink } },
  ], {
    x: x(235), y: y(250), w: w(83), h: h(30), align: "left", valign: "middle", margin: 0,
    fontFace: F, fontSize: 8, lineSpacing: 14.5,
  });
  // sub-block 2 (233..320 x 306..336) pale green
  slide.addShape(pptx.ShapeType.rect, { x: x(233), y: y(306), w: w(320 - 233), h: h(336 - 306), fill: { color: C.sub2 }, line: { type: "none" } });
  slide.addText([
    { text: "Fine Angle: ", options: { color: C.titleRed, bold: true, underline: { style: "sng", color: "1A1A1A" } } },
    { text: "atan(A/B)", options: { color: C.ink, bold: true, breakLine: true, underline: { style: "sng", color: "1A1A1A" } } },
    { text: "\u2192 Option 2: 12-bit", options: { color: C.ink } },
  ], {
    x: x(235), y: y(304), w: w(83), h: h(30), align: "left", valign: "middle", margin: 0,
    fontFace: F, fontSize: 8, lineSpacing: 14.5,
  });
  // sub-block 3 (235..318 x 358..388) white
  slide.addShape(pptx.ShapeType.rect, { x: x(235), y: y(358), w: w(318 - 235), h: h(388 - 358), fill: { color: C.sub3 }, line: { type: "none" } });
  slide.addText([
    { text: "Coarse Angle", options: { bold: true, breakLine: true, underline: { style: "sng", color: "1A1A1A" } } },
    { text: "Incremental count", options: {} },
  ], {
    x: x(237), y: y(359), w: w(79), h: h(28), align: "left", valign: "middle", margin: 0,
    fontFace: F, fontSize: 8, color: C.ink, lineSpacing: 14.5,
  });
  // right-edge peripheral labels: chip icon + SPI / 12-bit ADC / eQEP
  slide.addShape(pptx.ShapeType.rect, { x: x(378), y: y(252), w: w(12), h: h(11), fill: { color: C.white }, line: { color: C.ink2, width: 0.75 } });
  line(slide, pptx, 380, 252, 380, 250); line(slide, pptx, 384, 252, 384, 250); line(slide, pptx, 388, 252, 388, 250);
  line(slide, pptx, 380, 263, 380, 265); line(slide, pptx, 384, 263, 384, 265); line(slide, pptx, 388, 263, 388, 265);
  slide.addText("SPI", { x: x(362), y: y(266), w: w(34), h: h(14), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 10.5, color: C.ink });
  slide.addText([
    { text: "12-bit", options: { breakLine: true } },
    { text: "ADC", options: {} },
  ], { x: x(358), y: y(309), w: w(34), h: h(31), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 10.5, color: C.ink, lineSpacing: 11 });
  slide.addText("eQEP", { x: x(358), y: y(370), w: w(36), h: h(17), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 10.5, color: C.ink });
}

function drawHostBar(pptx, slide) {
  // frame 395..412 x 254..385
  slide.addShape(pptx.ShapeType.rect, {
    x: x(395), y: y(254), w: w(412 - 395), h: h(385 - 254),
    fill: { color: C.gray }, line: { color: "4A4A4A", width: 0.75 },
  });
  slide.addText("Host MCU Interface", {
    x: x(390.5), y: y(268), w: w(21), h: h(104),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 10.5, bold: true, color: C.ink,
    vert: "vert270",
  });
}

function drawCorridorLabels(pptx, slide) {
  slide.addText([
    { text: "A, B", options: { breakLine: true } },
    { text: "SPI", options: {} },
  ], { x: x(413), y: y(240), w: w(45), h: h(34), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7.5, color: C.ink, lineSpacing: 9 });
  slide.addText([
    { text: "A, B", options: { breakLine: true } },
    { text: "Analog", options: {} },
  ], { x: x(413), y: y(300), w: w(42), h: h(32), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7.5, color: C.ink, lineSpacing: 9 });
  slide.addText([
    { text: "A, B, R", options: { breakLine: true } },
    { text: "TTL", options: {} },
  ], { x: x(413), y: y(352), w: w(45), h: h(32), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7.5, color: C.ink, lineSpacing: 9 });
}

function drawPath16(pptx, slide) {
  // white label box (456..588 x 220..243)
  slide.addShape(pptx.ShapeType.rect, { x: x(456), y: y(220), w: w(588 - 456), h: h(243 - 220), fill: { color: C.white }, line: { color: C.boxLine, width: 0.75 } });
  slide.addText("16-bit high-res path", { x: x(456), y: y(220), w: w(588 - 456), h: h(243 - 220), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7.5, bold: true, color: C.ink });
  // dashed peach group (462..589 x 241..287)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: x(462), y: y(241), w: w(589 - 462), h: h(287 - 241),
    fill: { color: C.groupFill }, line: { color: C.groupDash, width: 1, dashType: "dash" }, rectRadius: 0.06,
  });
  // Dual ADC pentagon (471..531 x 248..279) — homePlate points right
  slide.addShape(pptx.ShapeType.homePlate, {
    x: x(471), y: y(248), w: w(531 - 471), h: h(279 - 248),
    fill: { color: C.pentagon }, line: { type: "none" },
  });
  slide.addText([
    { text: "Dual", options: { breakLine: true } },
    { text: "ADC", options: {} },
  ], { x: x(473), y: y(250), w: w(40), h: h(27), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7.5, bold: true, color: C.ink, lineSpacing: 9 });
  line(slide, pptx, 531, 262, 543, 262, { end: "triangle", width: 1.5 }); // Dual ADC -> amplifier arrow
  // amplifier triangle (544..579 x 245..279) pointing LEFT (flat edge right, measured)
  slide.addShape(pptx.ShapeType.triangle, { x: x(544), y: y(245), w: w(579 - 544), h: h(279 - 245), fill: { color: C.tri }, line: { type: "none" }, rotate: 270 });
  // top output label "A+,A-,B+,B-" (594..646 x 252..259) + arrow under it (corridor_lines)
  slide.addText("A+,A-,B+,B-", { x: x(590), y: y(247), w: w(60), h: h(16), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 9.5, color: C.ink });
}

function drawPathAnalog(pptx, slide) {
  // dashed transparent group (456..589 x 295..343) FIRST — the white label box overlaps its top
  slide.addShape(pptx.ShapeType.roundRect, {
    x: x(456), y: y(295), w: w(589 - 456), h: h(343 - 295),
    fill: { color: C.container }, line: { color: C.groupDash, width: 1, dashType: "dash" }, rectRadius: 0.06,
  });
  slide.addShape(pptx.ShapeType.rect, { x: x(456), y: y(288), w: w(588 - 456), h: h(317 - 288), fill: { color: C.white }, line: { color: C.boxLine, width: 0.75 } });
  slide.addText("Analog path", { x: x(456), y: y(288), w: w(588 - 456), h: h(317 - 288), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7.5, bold: true, color: C.ink });
  slide.addShape(pptx.ShapeType.triangle, { x: x(544), y: y(301), w: w(579 - 544), h: h(336 - 301), fill: { color: C.tri }, line: { type: "none" }, rotate: 270 });
  // mid output label "A+,A-,B+,B-," (594..646 x 322..330)
  slide.addText("A+,A-,B+,B-,", { x: x(590), y: y(318), w: w(60), h: h(16), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 9.5, color: C.ink });
  // comparators output label "R+,R-" (594..634 x 332..340)
  slide.addText("R+,R-", { x: x(590), y: y(329), w: w(48), h: h(15), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 9.5, color: C.ink });
}

function drawComparators(pptx, slide) {
  line(slide, pptx, 517, 375, 507, 375, { end: "triangle", width: 1.25 }); // into comparator base
  slide.addShape(pptx.ShapeType.rect, { x: x(458), y: y(350), w: w(598 - 458), h: h(400 - 350), fill: { color: C.compBox }, line: { type: "none" } });
  slide.addShape(pptx.ShapeType.triangle, { x: x(473), y: y(358), w: w(506 - 473), h: h(394 - 358), fill: { color: C.tri }, line: { color: "2E8B57", width: 0.75 }, rotate: 270 });
  // hysteresis glyph (Pi shape, black strokes) inside triangle
  slide.addShape(pptx.ShapeType.rect, { x: x(484), y: y(367), w: w(11), h: h(2), fill: { color: "111111" }, line: { type: "none" } });
  slide.addShape(pptx.ShapeType.rect, { x: x(484), y: y(367), w: w(2), h: h(12), fill: { color: "111111" }, line: { type: "none" } });
  slide.addShape(pptx.ShapeType.rect, { x: x(481), y: y(377), w: w(5), h: h(2), fill: { color: "111111" }, line: { type: "none" } });
  slide.addShape(pptx.ShapeType.rect, { x: x(493), y: y(367), w: w(2), h: h(14), fill: { color: "111111" }, line: { type: "none" } });
  slide.addShape(pptx.ShapeType.rect, { x: x(518), y: y(380), w: w(600 - 518), h: h(400 - 380), fill: { color: C.white }, line: { color: C.boxLine, width: 0.75 } });
  slide.addText("Comparators", { x: x(518), y: y(380), w: w(600 - 518), h: h(400 - 380), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7.5, bold: true, color: C.ink });
}

function drawPowerRow(pptx, slide) {
  slide.addText("24 V", { x: x(360), y: y(425), w: w(34), h: h(18), align: "right", valign: "middle", margin: 0, fontFace: F, fontSize: 9, bold: true, color: C.ink });
  slide.addShape(pptx.ShapeType.rect, { x: x(396), y: y(425), w: w(414 - 396), h: h(443 - 425), fill: { color: C.gray }, line: { color: "8C8C8C", width: 0.75 } });
  line(slide, pptx, 414, 434, 460, 434, { end: "triangle" });
  slide.addShape(pptx.ShapeType.rect, { x: x(462), y: y(416), w: w(526 - 462), h: h(456 - 416), fill: { color: C.powerSup }, line: { type: "none" } });
  slide.addText([
    { text: "Power", options: { breakLine: true } },
    { text: "Supplies", options: {} },
  ], { x: x(462), y: y(418), w: w(526 - 462), h: h(36), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 8, bold: true, color: C.ink, lineSpacing: 10 });
  line(slide, pptx, 528, 432, 552, 432, { end: "triangle" });
  slide.addText("5 V", { x: x(554), y: y(424), w: w(32), h: h(16), align: "left", valign: "middle", margin: 0, fontFace: F, fontSize: 9, color: C.ink });
  line(slide, pptx, 528, 450, 552, 450, { end: "triangle" });
  slide.addText("3.3 V", { x: x(554), y: y(442), w: w(38), h: h(16), align: "left", valign: "middle", margin: 0, fontFace: F, fontSize: 9, color: C.ink });
  slide.addText("Encoder Supply: 5.25 V", { x: x(598), y: y(447), w: w(100), h: h(15), align: "left", valign: "middle", margin: 0, fontFace: F, fontSize: 9, color: C.ink });
}

function drawEncConnector(pptx, slide) {
  // frame 649..666 x 280..373
  slide.addShape(pptx.ShapeType.rect, {
    x: x(649), y: y(280), w: w(666 - 649), h: h(373 - 280),
    fill: { color: C.gray }, line: { color: "4A4A4A", width: 0.75 },
  });
  slide.addText("Encoder connector", {
    x: x(647.5), y: y(292), w: w(20), h: h(70),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 10, bold: true, color: C.ink, vert: "vert270",
  });
}

function drawRightRect(pptx, slide) {
  // frame 687..855 x 187..465 — drawn BEFORE wires/right_contents (they sit on top)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: x(687), y: y(187), w: w(855 - 687), h: h(465 - 187),
    fill: { color: C.white }, line: { color: C.rrBorder, width: 2.5 }, rectRadius: 0.12,
  });
}

function drawWires(pptx, slide) {
  // matplotlib PNG at exact size; covers frame (664..860) x (246..430); 1568x1472 px @8x
  slide.addImage({
    path: path.join(ASSETS, "slide026_wires.png"),
    x: x(664), y: y(246), w: w(860 - 664), h: h(430 - 246),
  });
  const wireLabels = ["A+,", "A-,", "B+,", "B-,", "R+,", "R-,", "Up", "Un"];
  wireLabels.forEach((t, i) => {
    slide.addText(t, {
      x: x(681), y: y(301 + i * 12.5), w: w(38), h: h(12),
      align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 6.5, bold: true, color: C.ink,
    });
  });
}

function drawRightContents(pptx, slide) {
  // Differential box (694..831 x 246..280)
  slide.addShape(pptx.ShapeType.rect, { x: x(694), y: y(246), w: w(831 - 694), h: h(280 - 246), fill: { color: C.diffBox }, line: { type: "none" } });
  slide.addText([
    { text: "Differential Sine and Cosine", options: { breakLine: true } },
    { text: "A+, A-, B+, B- and Marker R+/R-", options: {} },
  ], { x: x(696), y: y(244), w: w(133), h: h(32), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 8.5, color: C.ink, lineSpacing: 13 });
  // Shielded twisted pairs note (740..854 x 320..358) — 3 lines
  slide.addText([
    { text: "Shielded twisted", options: { breakLine: true } },
    { text: "pairs cable, up", options: { breakLine: true } },
    { text: "to 50...150m", options: {} },
  ], { x: x(741), y: y(321), w: w(112), h: h(37), align: "left", valign: "middle", margin: 0, fontFace: F, fontSize: 7, color: C.ink, lineSpacing: 11.5 });
  // AC motor: clipped from the ORIGINAL frame (clean clip-art on white, founder figure pattern)
  slide.addImage({ path: path.join(ASSETS, "slide026_motor.png"), x: x(750), y: y(353), w: w(86), h: h(49) });
  slide.addText("AC Motor", { x: x(788), y: y(398), w: w(70), h: h(15), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 7, color: C.ink });
  // Sin/Cos Encoder box (741..799 x 399..425)
  slide.addShape(pptx.ShapeType.rect, { x: x(741), y: y(399), w: w(799 - 741), h: h(425 - 399), fill: { color: C.diffBox }, line: { type: "none" } });
  slide.addText([
    { text: "Sin/Cos", options: { breakLine: true } },
    { text: "Encoder", options: {} },
  ], { x: x(741), y: y(399), w: w(799 - 741), h: h(26), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 10.5, bold: true, color: "7A4A10", lineSpacing: 12 });
}

function drawPosArrow(pptx, slide) {
  slide.addShape(pptx.ShapeType.leftArrow, {
    x: x(155), y: y(294), w: w(226 - 155), h: h(319 - 294),
    fill: { color: C.posRed }, line: { type: "none" },
  });
  slide.addText([
    { text: "Position", options: { breakLine: true } },
    { text: "(Angle)", options: {} },
  ], { x: x(125), y: y(319), w: w(88), h: h(28), align: "center", valign: "middle", margin: 0, fontFace: F, fontSize: 13.5, bold: true, color: C.titleRed, lineSpacing: 13 });
}

function drawTitle(pptx, slide) {
  // measured ink center 461.3pt (NOT the slide center)
  slide.addText("Sin/Cos Encoders", {
    x: px(41.3), y: y(57), w: px(840), h: h(20),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 22, bold: true, color: C.titleRed,
  });
}

function drawSubtitle(pptx, slide) {
  // measured ink center 463.5pt
  slide.addText("(an industrial application of Motor Control System)", {
    x: px(43.5), y: y(81), w: px(840), h: h(22),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 22, bold: true, color: C.subtitleBlue,
  });
}

function drawCaptions(pptx, slide) {
  // measured ink centers ~557pt (captions center on the diagram, not the slide)
  slide.addText("EMC-compliant interface to Sin/Cos incremental position encoder switch", {
    x: px(177), y: y(478), w: px(760), h: h(16),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 13.5, bold: true, color: C.titleRed,
  });
  slide.addText("1-VPP  Differential analog output signals", {
    x: px(177), y: y(493), w: px(760), h: h(15),
    align: "center", valign: "middle", margin: 0,
    fontFace: F, fontSize: 12, bold: true, color: C.titleRed,
  });
}

// ---- composition -------------------------------------------------------------

const BLOCKS = {
  white_panel: drawWhitePanel,
  tida_container: drawTidaContainer,
  corridor_lines: drawCorridorLines,
  blue_box: drawBlueBox,
  host_bar: drawHostBar,
  corridor_labels: drawCorridorLabels,
  path16: drawPath16,
  path_analog: drawPathAnalog,
  comparators: drawComparators,
  power_row: drawPowerRow,
  enc_connector: drawEncConnector,
  right_rect: drawRightRect,
  wires: drawWires,
  right_contents: drawRightContents,
  pos_arrow: drawPosArrow,
  title: drawTitle,
  subtitle: drawSubtitle,
  captions: drawCaptions,
};

/**
 * Draw the full slide-026 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 26 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, C, px, x, y, w, h };
