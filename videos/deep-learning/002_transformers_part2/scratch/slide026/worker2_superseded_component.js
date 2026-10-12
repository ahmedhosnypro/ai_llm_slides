// components/slide_026.js — BANKED COMPONENT for slide 026
// "Sin/Cos Encoders (an industrial application of Motor Control System)"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 26)
//
// Dependency law (founder directive 2026-10-11): slides 28 (via 27+26) and 49 depend on
// this composition, so it is banked as a reusable component drawn at BLOCK granularity:
//   renderBase(pptx, slide, opts)
//     opts.numeral  badge numeral (default 26 = the number printed on the original frame)
//     opts.skip     array of block names to omit (child removes parent blocks)
//     opts.only     array of block names to draw exclusively (child selects blocks)
// Children must `require` THIS module by absolute path and call renderBase — never
// copy-paste or re-derive the geometry. House chrome is drawn ONCE here (block
// "chrome") via the playlist shared primitive; children must not re-draw it.
//
// Block names: chrome, title, subtitle, tidaContainer, tidaTag, subboxes, whiteBoxes,
//   adc, triangles, comparator, psu, busAndOutputs, signalLines, hostBox, connector,
//   blueBox, whiteStrip, rightPanel, diffBox, fan, encoderMotor, positionArrow, caption.
//
// MEASUREMENTS (PIL on unique_slides/slide_026.jpg, 960x540, 1px = 1pt at frame scale;
// scratch/slide026/*.py + gate crop reads cropread_R1..R12 .txt):
//   frame->slide mapping (identical to certified 002 builds): frame_x = 18.63 +
//   0.96123*slide_x ; frame_y = 0.95556*slide_y  (chrome borders measured x 58/901,
//   top 43, bottom 516-517; badge bbox (859,56)-(892,85) -> house (893,71) d36).
//   All geometry below is stored in FRAME px and converted with FX()/FY()/FW()/FH().
//   Black bars rows 518-539 = video letterbox BELOW the slide bottom edge (slide bottom
//   maps to fy 516) — intentionally NOT recreated (video-capture artifact, ground rule c).
//   The "chip/IC icon" near SPI = presenter cursor overlay artifact (cropread_R1/R6) — omitted.
//   Fonts fitted with Liberation Sans (Arial-metric) against measured ink widths.

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const FONT = "Arial";
const IN = (pt) => pt / 72;
// frame -> slide pt
const FX = (fx) => (fx - 18.63) / 0.96123;
const FY = (fy) => fy / 0.95556;
const FW = (w) => w / 0.96123;
const FH = (h) => h / 0.95556;

// palette (frame-measured cores; JPEG-true since white/panel-gray sample true)
const C = {
  blueFill: "10BDEC", blueLine: "0C4E62",
  sb1: "F5D6BB", sb2: "D6E7BD", sb3: "FFFFFF",
  grayBox: "D6D8D5", grayBoxLine: "222222",
  tidaFill: "C4DCA0", tidaDash: "92D050",
  subDash: "3C4A1E",
  white: "FFFFFF",
  adcFill: "EB9B68", blkLine: "333333",
  triFill: "6BCF92",
  compFill: "79C698",
  psuFill: "D0B971",
  v24Fill: "D7D7D9",
  panelLine: "1E7240",
  diffFill: "EED1AF",
  ellipseFill: "E9CBA8",
  redArrow: "CC0000",
  darkRedText: "800818",
  navy: "000068",
  ink: "1A1A1A",
  motorFill: "C6C8C5", motorFin: "9E9E9E", encBox: "A4A6A3", encConn: "7C7C7C",
  cable: "A6A6A6", shaft: "B0B0B0",
};

function rect(pptx, slide, x0, y0, x1, y1, o) {
  slide.addShape(pptx.ShapeType.rect, {
    x: IN(FX(x0)), y: IN(FY(y0)), w: IN(FW(x1 - x0)), h: IN(FH(y1 - y0)), ...o,
  });
}
function txt(slide, str, x0, y0, x1, y1, o) {
  slide.addText(str, {
    x: IN(FX(x0)), y: IN(FY(y0)), w: IN(FW(x1 - x0)), h: IN(FH(y1 - y0)), ...o,
  });
}
function hline(slide, x1, x2, y, o) {
  slide.addShape(pptx.ShapeType.line, {
    x: IN(FX(Math.min(x1, x2))), y: IN(FY(y)), w: IN(FW(Math.abs(x2 - x1))), h: 0, ...o,
  });
}
function vline(slide, x, y1, y2, o) {
  slide.addShape(pptx.ShapeType.line, {
    x: IN(FX(x)), y: IN(FY(Math.min(y1, y2))), w: 0, h: IN(FH(Math.abs(y2 - y1))), ...o,
  });
}

// ---- block painters (each takes pptx; slide closed over via argument) ----
const BLOCKS = {
  chrome(pptx, slide, opts) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 26 : opts.numeral });
  },

  title(pptx, slide) {
    // ink x 372..551 (cx slide 460.9pt), cap band y 60..74 -> 22pt bold
    slide.addText("Sin/Cos Encoders", {
      x: IN(FX(461.5) - 436.7), y: IN(FY(60) - 0.267 * 22), w: IN(12.13), h: IN(30),
      align: "center", valign: "top", margin: 0,
      fontSize: 22, bold: true, color: C.darkRedText, fontFace: FONT,
    });
  },

  subtitle(pptx, slide) {
    // ink x 207..722, band y 84..97 -> 22pt bold navy, cx slide 463.3pt
    slide.addText("(an industrial application of Motor Control System)", {
      x: IN(FX(464.5) - 436.7), y: IN(FY(84) - 0.267 * 22), w: IN(12.13), h: IN(30),
      align: "center", valign: "top", margin: 0,
      fontSize: 22, bold: true, color: C.navy, fontFace: FONT,
    });
  },

  tidaContainer(pptx, slide) {
    rect(pptx, slide, 402, 187, 659.5, 467.5, {
      fill: { color: C.tidaFill },
      line: { color: C.tidaDash, width: 1, dashType: "dash" },
    });
  },

  tidaTag(pptx, slide) {
    rect(pptx, slide, 576, 192, 650, 211, { fill: { color: C.white } });
    txt(slide, "TIDA-00176", 576, 194, 650, 210, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 10.5, bold: true, color: "000000", fontFace: FONT,
    });
  },

  subboxes(pptx, slide) {
    // three dashed path sub-boxes, measured fills (peach / light green / lavender)
    rect(pptx, slide, 458, 222, 589, 285, {
      fill: { color: C.sb1 }, line: { color: C.subDash, width: 1, dashType: "dash" },
    });
    rect(pptx, slide, 458, 292.5, 589, 342, {
      fill: { color: C.sb2 }, line: { color: C.subDash, width: 1, dashType: "dash" },
    });
    rect(pptx, slide, 458, 350.5, 589, 401, {
      fill: { color: "EAE9EF" }, line: { color: C.subDash, width: 1, dashType: "dash" },
    });
  },

  whiteBoxes(pptx, slide) {
    // floating white label boxes (borderless, measured)
    rect(pptx, slide, 465, 225, 580, 239, { fill: { color: C.white } });
    txt(slide, "16-bit high-res path", 465, 226.5, 580, 238, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 9, color: "000000", fontFace: FONT,
    });
    rect(pptx, slide, 465, 299, 528, 313, { fill: { color: C.white } });
    txt(slide, "Analog path", 465, 300, 528, 312, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 9, color: "000000", fontFace: FONT,
    });
    rect(pptx, slide, 512, 381, 584, 397, { fill: { color: C.white } });
    txt(slide, "Comparators", 512, 382, 584, 396, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 9, color: "000000", fontFace: FONT,
    });
  },

  adc(pptx, slide) {
    // Dual ADC: right-pointing pentagon (homePlate), 2-line label
    slide.addShape(pptx.ShapeType.homePlate, {
      x: IN(FX(471)), y: IN(FY(247)), w: IN(FW(56)), h: IN(FH(31)),
      fill: { color: C.adcFill }, line: { color: C.blkLine, width: 1 },
    });
    slide.addText([
      { text: "Dual", options: { breakLine: true } },
      { text: "ADC", options: {} },
    ], {
      x: IN(FX(471)), y: IN(FY(247)), w: IN(FW(50)), h: IN(FH(31)),
      align: "center", valign: "middle", margin: 0, lineSpacing: 10,
      fontSize: 9.5, color: "000000", fontFace: FONT,
    });
  },

  triangles(pptx, slide) {
    // two green amplifier triangles, apex LEFT (rotate 270 from up-apex)
    for (const [x0, y0, x1, y1] of [[545, 245, 578, 279], [544, 300, 581, 336]]) {
      slide.addShape(pptx.ShapeType.triangle, {
        x: IN(FX(x0)), y: IN(FY(y0)), w: IN(FW(x1 - x0)), h: IN(FH(y1 - y0)),
        rotate: 270, fill: { color: C.triFill }, line: { color: "000000", width: 1 },
      });
    }
  },

  comparator(pptx, slide) {
    // comparator triangle (apex left) + I-beam hysteresis glyph inside
    slide.addShape(pptx.ShapeType.triangle, {
      x: IN(FX(472)), y: IN(FY(358)), w: IN(FW(34)), h: IN(FH(27)),
      rotate: 270, fill: { color: C.compFill }, line: { color: "000000", width: 1 },
    });
    rect(pptx, slide, 497.5, 372, 500.5, 392, { fill: { color: "000000" } });
    rect(pptx, slide, 492, 372, 505, 375, { fill: { color: "000000" } });
    rect(pptx, slide, 492, 389, 505, 392, { fill: { color: "000000" } });
  },

  psu(pptx, slide) {
    // Power Supplies block (khaki) + 24 V gray box + arrows + 5 V / 3.3 V + supply line + note
    rect(pptx, slide, 458, 413, 528.5, 459.5, {
      fill: { color: C.psuFill }, line: { color: C.blkLine, width: 1 },
    });
    slide.addText([
      { text: "Power", options: { breakLine: true } },
      { text: "Supplies", options: {} },
    ], {
      x: IN(FX(458)), y: IN(FY(413)), w: IN(FW(70.5)), h: IN(FH(46.5)),
      align: "center", valign: "middle", margin: 0, lineSpacing: 11,
      fontSize: 9, color: "000000", fontFace: FONT,
    });
    // 24 V box + feed arrow
    rect(pptx, slide, 389, 426, 414, 447, {
      fill: { color: C.v24Fill }, line: { color: C.blkLine, width: 1 },
    });
    txt(slide, "24 V", 389, 428, 414, 445, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7, color: "333333", fontFace: FONT,
    });
    hline(slide, 414, 457, 436, {
      line: { color: "000000", width: 1, endArrowType: "triangle" },
    });
    // 5 V / 3.3 V output arrows + labels
    hline(slide, 528.5, 555, 421.5, {
      line: { color: "000000", width: 1, endArrowType: "triangle" },
    });
    txt(slide, "5 V", 557, 415.5, 578, 428, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 8.5, bold: true, color: "000000", fontFace: FONT,
    });
    hline(slide, 528.5, 555, 431.5, {
      line: { color: "000000", width: 1, endArrowType: "triangle" },
    });
    txt(slide, "3.3 V", 558, 425, 584, 438, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 8.5, bold: true, color: "000000", fontFace: FONT,
    });
    // Encoder supply line: PSU right edge -> bus, label below
    hline(slide, 528.5, 625.5, 445, { line: { color: "000000", width: 1 } });
    txt(slide, "Encoder Supply: 5.25 V", 535, 448.5, 630, 459, {
      align: "left", valign: "middle", margin: 0,
      fontSize: 8.5, color: "000000", fontFace: FONT,
    });
  },

  busAndOutputs(pptx, slide) {
    // vertical bus at x 625.5 (y 263.5..445) + output arrows with LEFT heads
    vline(slide, 625.5, 263.5, 445, { line: { color: "000000", width: 1 } });
    // upper output: bus -> triangle-1 base (left head)
    hline(slide, 581, 625.5, 263.5, {
      line: { color: "000000", width: 1, beginArrowType: "triangle" },
    });
    // middle output: triangle-2 base -> encoder connector (left head at triangle)
    hline(slide, 581, 647, 319, {
      line: { color: "000000", width: 1, beginArrowType: "triangle" },
    });
  },

  signalLines(pptx, slide) {
    // three signal lines blue panel <-> TIDA targets (pass behind host box);
    // left arrowheads at the blue panel end (cropread_R1), right head into Dual ADC (R2)
    hline(slide, 381, 470.5, 263.5, {
      line: { color: "000000", width: 1, beginArrowType: "triangle", endArrowType: "triangle" },
    });
    hline(slide, 381, 544.5, 319, {
      line: { color: "000000", width: 1, beginArrowType: "triangle" },
    });
    hline(slide, 381, 470.5, 375.5, {
      line: { color: "000000", width: 1, beginArrowType: "triangle" },
    });
    // analog branch down to comparator (left head at comparator right edge)
    vline(slide, 530.5, 319, 374.5, { line: { color: "000000", width: 1 } });
    hline(slide, 508, 530.5, 374.5, {
      line: { color: "000000", width: 1, endArrowType: "triangle" },
    });
    // connection labels inside the container (above/below each line)
    txt(slide, "A, B", 420, 249.5, 440, 260, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7, color: "000000", fontFace: FONT,
    });
    txt(slide, "SPI", 421, 266, 437, 276, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7, bold: true, color: "000000", fontFace: FONT,
    });
    txt(slide, "A, B", 421, 305.5, 440, 316, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7, color: "000000", fontFace: FONT,
    });
    txt(slide, "Analog", 421, 322.5, 450, 332.5, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7, color: "000000", fontFace: FONT,
    });
    txt(slide, "A, B, R", 420, 362, 450, 372.5, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7, color: "000000", fontFace: FONT,
    });
    txt(slide, "TTL", 421, 378.5, 438, 388.5, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7, color: "000000", fontFace: FONT,
    });
  },

  hostBox(pptx, slide) {
    // vertical gray box over the signal lines; label reads bottom-to-top
    rect(pptx, slide, 394, 252, 413.5, 387, {
      fill: { color: C.grayBox }, line: { color: C.grayBoxLine, width: 1 },
    });
    slide.addText("Host MCU Interface", {
      x: IN(FX(403.75) - IN(FH(126)) / 2), y: IN(FY(319.5) - IN(FW(17)) / 2),
      w: IN(FH(126)), h: IN(FW(17)), rotate: 270,
      align: "center", valign: "middle", margin: 0,
      fontSize: 12.5, bold: true, color: "333333", fontFace: FONT,
    });
  },

  connector(pptx, slide) {
    // Encoder connector vertical box; label reads bottom-to-top
    rect(pptx, slide, 647, 279, 667.5, 375, {
      fill: { color: "D9DBD8" }, line: { color: C.grayBoxLine, width: 1 },
    });
    slide.addText("Encoder connector", {
      x: IN(FX(657.25) - IN(FH(88)) / 2), y: IN(FY(327) - IN(FW(16)) / 2),
      w: IN(FH(88)), h: IN(FW(16)), rotate: 270,
      align: "center", valign: "middle", margin: 0,
      fontSize: 9.5, bold: true, color: "333333", fontFace: FONT,
    });
  },

  blueBox(pptx, slide) {
    rect(pptx, slide, 230, 237, 380.5, 388.5, {
      fill: { color: C.blueFill }, line: { color: C.blueLine, width: 1.5 },
    });
    // three stacked sub-blocks (peach / light green / white)
    rect(pptx, slide, 234, 254.5, 341, 283.5, { fill: { color: C.sb1 } });
    rect(pptx, slide, 234, 306.5, 341, 334.5, { fill: { color: C.sb2 } });
    rect(pptx, slide, 234, 357.5, 341, 384.5, { fill: { color: C.sb3 } });
    const fineRuns = [
      { text: "Fine Angle", options: { bold: true } },
      { text: ": atan(A/B)", options: {} },
    ];
    slide.addText([
      ...fineRuns.map((r, i) => ({ ...r, options: { ...r.options, breakLine: i === 0 } })),
      { text: "\u2192 Option 1: 16 bit", options: {} },
    ], {
      x: IN(FX(234)), y: IN(FY(254.5)), w: IN(FW(107)), h: IN(FH(29)),
      align: "center", valign: "middle", margin: 0, lineSpacing: 10.5,
      fontSize: 8, color: C.ink, fontFace: FONT,
    });
    slide.addText([
      { text: "Fine Angle", options: { bold: true, underline: true, breakLine: true } },
      { text: ": atan(A/B)", options: { breakLine: true } },
      { text: "\u2192 Option 2: 12-bit", options: {} },
    ], {
      x: IN(FX(234)), y: IN(FY(306.5)), w: IN(FW(107)), h: IN(FH(28)),
      align: "center", valign: "middle", margin: 0, lineSpacing: 10.5,
      fontSize: 8, color: C.ink, fontFace: FONT,
    });
    slide.addText([
      { text: "Coarse Angle", options: { bold: true, underline: true, breakLine: true } },
      { text: "Incremental count", options: {} },
    ], {
      x: IN(FX(234)), y: IN(FY(357.5)), w: IN(FW(107)), h: IN(FH(27)),
      align: "center", valign: "middle", margin: 0, lineSpacing: 10.5,
      fontSize: 8, color: C.ink, fontFace: FONT,
    });
    // right-edge peripheral labels (right-aligned to x 377)
    txt(slide, "SPI", 352, 256, 377, 269, {
      align: "right", valign: "middle", margin: 0,
      fontSize: 7.5, bold: true, color: "333333", fontFace: FONT,
    });
    slide.addText([
      { text: "12-bit", options: { breakLine: true } },
      { text: "ADC", options: {} },
    ], {
      x: IN(FX(344)), y: IN(FY(310)), w: IN(FW(33)), h: IN(FH(24)),
      align: "right", valign: "middle", margin: 0, lineSpacing: 9,
      fontSize: 7, bold: true, color: C.navy, fontFace: FONT,
    });
    txt(slide, "eQEP", 348, 369, 377, 382, {
      align: "right", valign: "middle", margin: 0,
      fontSize: 6.5, bold: true, color: "333333", fontFace: FONT,
    });
  },

  whiteStrip(pptx, slide) {
    // white strip between encoder connector and right panel border (measured 668-683)
    rect(pptx, slide, 667.5, 246, 684, 400, { fill: { color: C.white } });
  },

  rightPanel(pptx, slide) {
    // white rounded rectangle, thick dark-green border
    slide.addShape(pptx.ShapeType.roundRect, {
      x: IN(FX(686)), y: IN(FY(188)), w: IN(FW(168)), h: IN(FH(276)),
      rectRadius: 0.1, fill: { color: C.white },
      line: { color: C.panelLine, width: 2.75 },
    });
  },

  diffBox(pptx, slide) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: IN(FX(695)), y: IN(FY(246)), w: IN(FW(135)), h: IN(FH(33)),
      rectRadius: 0.05, fill: { color: C.diffFill },
    });
    slide.addText([
      { text: "Differential Sine and Cosine", options: { breakLine: true } },
      { text: "A+, A-, B+, B-, and Marker R+, R-", options: {} },
    ], {
      x: IN(FX(695)), y: IN(FY(246)), w: IN(FW(135)), h: IN(FH(33)),
      align: "center", valign: "middle", margin: 0, lineSpacing: 10.5,
      fontSize: 8, color: "000000", fontFace: FONT,
    });
    // leader line from bubble bottom-left down to the wire-label stack (down head)
    slide.addShape(pptx.ShapeType.line, {
      x: IN(FX(699)), y: IN(FY(279)), w: IN(FW(2)), h: IN(FH(8)),
      flipH: true, line: { color: "000000", width: 1, endArrowType: "triangle" },
    });
  },

  fan(pptx, slide) {
    // 8-wire fan: connector -> junction J1 -> labels -> junction J2 -> thick cable
    const yc = [287.5, 300.5, 309.5, 318, 327.5, 335.5, 344.5, 355.5];
    const labels = ["A+", "A-", "B+", "B-", "R+", "R-", "Up", "Un"];
    const J1 = [691, 324];
    const J2 = [737, 335];
    const wire = { line: { color: "000000", width: 0.75 } };
    const exits = [292, 302, 311, 319, 327, 336, 346, 362];
    for (let i = 0; i < 8; i++) {
      // connector right edge -> J1
      slide.addShape(pptx.ShapeType.line, {
        x: IN(FX(667.5)), y: IN(FY(Math.min(exits[i], J1[1]))),
        w: IN(FW(J1[0] - 667.5)), h: IN(FH(Math.abs(J1[1] - exits[i]))),
        flipV: J1[1] < exits[i], ...wire,
      });
      // J1 -> label tick
      slide.addShape(pptx.ShapeType.line, {
        x: IN(FX(J1[0])), y: IN(FY(Math.min(yc[i], J1[1]))),
        w: IN(FW(708 - J1[0])), h: IN(FH(Math.abs(yc[i] - J1[1]))),
        flipV: yc[i] < J1[1], ...wire,
      });
      // label
      txt(slide, labels[i], 707, yc[i] - 4.5, 723, yc[i] + 4.5, {
        align: "center", valign: "middle", margin: 0,
        fontSize: 6.5, color: "000000", fontFace: FONT,
      });
      // label -> J2
      slide.addShape(pptx.ShapeType.line, {
        x: IN(FX(723)), y: IN(FY(Math.min(yc[i], J2[1]))),
        w: IN(FW(J2[0] - 723)), h: IN(FH(Math.abs(J2[1] - yc[i]))),
        flipV: J2[1] < yc[i], ...wire,
      });
    }
    // thick cable S-curve J2 -> encoder connector top
    slide.addShape(pptx.ShapeType.line, {
      x: IN(FX(J2[0])), y: IN(FY(J2[1])), w: IN(FW(16)), h: IN(FH(6)),
      flipV: true, line: { color: C.cable, width: 3 },
    });
    slide.addShape(pptx.ShapeType.line, {
      x: IN(FX(753)), y: IN(FY(341)), w: IN(FW(11)), h: IN(FH(10)),
      line: { color: C.cable, width: 3 },
    });
  },

  encoderMotor(pptx, slide) {
    // encoder body + top connector + tabs
    rect(pptx, slide, 753, 358, 783, 398, {
      fill: { color: C.encBox }, line: { color: "555555", width: 1 },
    });
    rect(pptx, slide, 761, 350, 773, 358, { fill: { color: C.encConn } });
    rect(pptx, slide, 783, 366, 788, 373, { fill: { color: "666666" } });
    rect(pptx, slide, 783, 380, 788, 387, { fill: { color: "666666" } });
    // AC motor: body + fins + nameplate + shaft
    rect(pptx, slide, 786, 357, 831, 398, {
      fill: { color: C.motorFill }, line: { color: "8C8C8C", width: 1 },
    });
    for (const fy of [365, 373, 381, 389]) {
      hline(slide, 788, 829, fy, { line: { color: C.motorFin, width: 0.75 } });
    }
    slide.addShape(pptx.ShapeType.roundRect, {
      x: IN(FX(791)), y: IN(FY(368)), w: IN(FW(20)), h: IN(FH(15)),
      rectRadius: 0.03, fill: { color: "E8E8E8" }, line: { color: "999999", width: 0.75 },
    });
    rect(pptx, slide, 831, 373, 848, 381, { fill: { color: C.shaft } });
    txt(slide, "AC Motor", 795, 347, 835, 358, {
      align: "center", valign: "middle", margin: 0,
      fontSize: 7.5, bold: true, color: "000000", fontFace: FONT,
    });
    // 3-line cable annotation
    slide.addText([
      { text: "Shielded twisted", options: { breakLine: true } },
      { text: "pairs cable, up to", options: { breakLine: true } },
      { text: "50...150m", options: {} },
    ], {
      x: IN(FX(766)), y: IN(FY(297.5)), w: IN(FW(90)), h: IN(FH(32)),
      align: "left", valign: "top", margin: 0, lineSpacing: 10,
      fontSize: 8.5, color: "000000", fontFace: FONT,
    });
    // Sin/Cos Encoder ellipse
    slide.addShape(pptx.ShapeType.ellipse, {
      x: IN(FX(741)), y: IN(FY(399)), w: IN(FW(58)), h: IN(FH(26)),
      fill: { color: C.ellipseFill },
    });
    slide.addText([
      { text: "Sin/Cos", options: { breakLine: true } },
      { text: "Encoder", options: {} },
    ], {
      x: IN(FX(741)), y: IN(FY(399)), w: IN(FW(58)), h: IN(FH(26)),
      align: "center", valign: "middle", margin: 0, lineSpacing: 9,
      fontSize: 7.5, bold: true, color: "000000", fontFace: FONT,
    });
  },

  positionArrow(pptx, slide) {
    // thick red left-pointing block arrow: head triangle + shaft rect (measured)
    slide.addShape(pptx.ShapeType.triangle, {
      x: IN(FX(160)), y: IN(FY(298)), w: IN(FW(11)), h: IN(FH(18.5)),
      rotate: 270, fill: { color: C.redArrow },
    });
    rect(pptx, slide, 171, 302.5, 210.5, 312, { fill: { color: C.redArrow } });
    // label beneath: "Position" / "(Angle)", 2 lines red bold
    slide.addText([
      { text: "Position", options: { breakLine: true } },
      { text: "(Angle)", options: {} },
    ], {
      x: IN(FX(140)), y: IN(FY(321.5)), w: IN(FW(59)), h: IN(FH(36)),
      align: "center", valign: "top", margin: 0, lineSpacing: 16,
      fontSize: 13.5, bold: true, color: C.darkRedText, fontFace: FONT,
    });
  },

  caption(pptx, slide) {
    slide.addText([
      { text: "EMC-compliant interface to Sin/Cos incremental position encoder switch", options: { breakLine: true } },
      { text: "1-VPP  Differential analog output signals", options: {} },
    ], {
      x: IN(FX(554) - 250), y: IN(FY(481) - 0.267 * 13), w: IN(500), h: IN(32),
      align: "center", valign: "top", margin: 0, lineSpacing: 14,
      fontSize: 13, bold: true, color: C.darkRedText, fontFace: FONT,
    });
  },
};

const ORDER = [
  "chrome", "title", "subtitle", "whiteStrip", "rightPanel", "fan",
  "encoderMotor", "diffBox", "tidaContainer", "tidaTag", "subboxes", "whiteBoxes",
  "adc", "triangles", "comparator", "psu", "busAndOutputs", "signalLines",
  "hostBox", "connector", "blueBox", "positionArrow", "caption",
];

/**
 * Draw the full slide-026 composition.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide the slide returned by pptx.addSlide()
 * @param {object} opts  { numeral, skip: [block], only: [block] }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  for (const name of ORDER) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    BLOCKS[name](pptx, slide, opts);
  }
}

module.exports = { renderBase, BLOCKS, ORDER, C };
