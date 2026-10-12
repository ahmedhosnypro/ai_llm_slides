// components/slide_023.js — BANKED COMPONENT for slide 023
// "Suggested Positional Encoders (Normalize Seq. Length to "1")"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 23)
//
// Dependency law (founder directive 2026-10-11): slide 024 depends on 023, so this
// composition is banked as a reusable component: renderBase(pptx, slide, opts) draws
// the FULL slide (house chrome + content). Children must `require` THIS module by
// absolute path and call renderBase — never copy-paste or re-derive the geometry.
// opts.numeral: badge numeral (default 23 = the number printed on the original).
//
// MEASUREMENTS (identical to ../slide_023.js header — read that for the full record):
// frame->slide mapping slide_x=(fx-17.628)/0.961230, slide_y=(fy+0.045)/0.956566;
// chrome = shared house_chrome.js; content = 3 dashed containers + 8 boxes each,
// ellipsis dots, 6 orange arrow drops + red "+d" labels, light-cyan highlight box
// with lead line / "Problems:" / 3 bullets (bullet 2 wraps, second line magenta).

const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const FONT = "Arial";
const RED = "C00000";
const BOXRED = "CC0000";
const BLUE2 = "3333CC";
const BODYBLUE = "0000CC";
const MAG = "CC00CC";
const ORANGE = "FF9900";
const GRAYDOT = "999999";
const HLfill = "E8FCFA";

const IN = (pt) => pt / 72;

function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 23 : opts.numeral;

  // 1. playlist house chrome
  drawHouseChrome(pptx, slide, { numeral });

  // 2. title + subtitle (measured centers; title genuinely right of slide center)
  slide.addText("Suggested Positional Encoders", {
    x: IN(516.4 - 436.7), y: IN(55.0), w: 12.13, h: IN(40),
    align: "center", valign: "top", margin: 0,
    fontSize: 24.5, bold: true, color: RED, fontFace: FONT,
  });
  slide.addText("(Normalize Seq. Length to \u201C1\u201D)", {
    x: IN(522.6 - 436.7), y: IN(82.8), w: 12.13, h: IN(34),
    align: "center", valign: "top", margin: 0,
    fontSize: 22.5, bold: true, color: BODYBLUE, fontFace: FONT,
  });

  // 3. three dashed rounded containers
  const containers = [
    { x: 147.6, y: 123.4, w: 749.1, h: 40.8, line: "000000", fill: null },
    { x: 145.5, y: 195.5, w: 747.6, h: 40.3, line: BLUE2, fill: "CCCCFF" },
    { x: 144.0, y: 273.4, w: 750.4, h: 42.9, line: BOXRED, fill: "FFE0E0" },
  ];
  for (const c of containers) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: IN(c.x), y: IN(c.y), w: IN(c.w), h: IN(c.h), rectRadius: 0.055,
      fill: c.fill ? { color: c.fill } : { type: "none" },
      line: { color: c.line, width: 1.5, dashType: "dash" },
    });
  }

  // 4. the 24 boxes (8 per row) + texts
  const rows = [
    {
      yTop: 132.3, yBot: 154.2, line: BOXRED, lineW: 0.5, fill: "FFFFFF", txt: BOXRED,
      boxes: [[161.6,223.5],[238.1,300.5],[315.1,376.5],[392.1,453.5],[468.0,529.4],[545.0,606.4],[739.5,806.1],[817.6,885.2]],
      labels: ["Word 0","Word 1","Word 2","Word 3","Word 4","Word 5","Word N-2","Word N-1"],
    },
    {
      yTop: 203.9, yBot: 226.7, line: BLUE2, lineW: 0.5, fill: null, txt: BLUE2,
      boxes: [[157.2,219.4],[233.9,295.8],[310.9,372.3],[387.4,448.8],[463.9,525.8],[540.8,602.2],[734.6,802.0],[812.9,882.1]],
      labels: ["Pos 0","Pos 1","Pos 2","Pos 3","Pos 4","Pos 5","Pos N-2","Pos N-1"],
    },
    {
      yTop: 284.9, yBot: 307.4, line: BOXRED, lineW: 1, fill: "FFFFFF", txt: BOXRED,
      boxes: [[156.4,217.3],[231.9,292.7],[309.9,371.3],[385.3,447.2],[463.9,525.2],[539.3,601.2],[733.8,800.9],[812.4,880.0]],
      labels: ["0","\u03B4","2\u03B4","3\u03B4","4\u03B4","5\u03B4","1-\u03B4","1"],
    },
  ];
  for (const row of rows) {
    for (let i = 0; i < 8; i++) {
      const [bx0, bx1] = row.boxes[i];
      slide.addShape(pptx.ShapeType.rect, {
        x: IN(bx0), y: IN(row.yTop), w: IN(bx1 - bx0), h: IN(row.yBot - row.yTop),
        fill: row.fill ? { color: row.fill } : { type: "none" },
        line: { color: row.line, width: row.lineW },
      });
      slide.addText(row.labels[i], {
        x: IN(bx0), y: IN(row.yTop), w: IN(bx1 - bx0), h: IN(row.yBot - row.yTop),
        align: "center", valign: "middle", margin: 0,
        fontSize: 13, italic: true, color: row.txt, fontFace: FONT,
      });
    }
  }

  // 5. ellipsis dots (5 gray in row 1, 5 blue in row 2, none in row 3)
  const dots = [
    { cx: [635.0, 653.7, 672.4, 691.2, 706.9], cy: 144.3, d: 8.0, color: GRAYDOT },
    { cx: [635.5, 655.3, 673.0, 692.7, 707.8], cy: 217.0, d: 9.8, color: "6B8BB4" },  // measured disc core (107,139,180)
  ];
  for (const dd of dots) {
    for (const cx of dd.cx) {
      slide.addShape(pptx.ShapeType.ellipse, {
        x: IN(cx - dd.d / 2), y: IN(dd.cy - dd.d / 2), w: IN(dd.d), h: IN(dd.d),
        fill: { color: dd.color }, line: { color: dd.color, width: 0.25 },
      });
    }
  }

  // 6. left strip labels (each measured line its own single-line box)
  const labelLines = [
    ["Sequence of", 119.2, 52.0, "7F7F7F", false, true, 14],
    ["words with", 134.9, 52.0, "7F7F7F", false, true, 14],
    ["Length N", 151.6, 52.0, "7F7F7F", false, true, 14],
    ["Position", 200.8, 51.0, BLUE2, true, false, 14],
    ["Embedding", 216.4, 51.0, BLUE2, true, false, 14],
    ["Use Position", 275.0, 48.0, BOXRED, true, false, 14],
    ["Index", 291.7, 48.0, BOXRED, true, false, 14],
  ];
  for (const [txt, cap, x, color, bold, italic, size] of labelLines) {
    slide.addText(txt, {
      x: IN(x), y: IN(cap - 0.267 * size), w: IN(150), h: IN(size * 1.4),
      align: "left", valign: "top", margin: 0, lineSpacing: size * 1.15,
      fontSize: size, bold, italic, color, fontFace: FONT,
    });
  }

  // 7. six arrow drops + heads + "+\u03B4" labels
  const shaftCx = [260.5, 339.5, 416.0, 493.5, 570.0, 844.1];
  // measured: triangle apex at the destination box's bottom edge (y 306.9), wide base
  // below the container's bottom border (y ~318.5, w ~15.6) — arrows point UP into the boxes
  for (const cx of shaftCx) {
    slide.addShape(pptx.ShapeType.triangle, {
      x: IN(cx - 7.8), y: IN(306.9), w: IN(15.6), h: IN(11.6),
      fill: { color: ORANGE }, line: { color: ORANGE, width: 0.25 },
    });
  }
  const labelCx = [217.3, 289.6, 373.9, 452.4, 527.8, 807.2];
  for (const cx of labelCx) {
    slide.addText("+\u03B4", {
      x: IN(cx - 43.2), y: IN(324.1), w: IN(86.4), h: IN(24),
      align: "center", valign: "top", margin: 0,
      fontSize: 17, bold: true, color: BOXRED, fontFace: FONT,
    });
  }

  // 8. highlight box
  slide.addShape(pptx.ShapeType.roundRect, {
    x: IN(54.5), y: IN(363.9), w: IN(853.1), h: IN(162.0), rectRadius: 0.07,
    fill: { color: HLfill },
    line: { color: "0066CC", width: 1.5 },
  });

  // 9. highlight-box text
  slide.addText([
    { text: "Use ", options: { color: BODYBLUE } },
    { text: "\u03B4=1/Seq. Length", options: { color: RED, bold: true } },
    { text: "  First position Encoding=", options: { color: BODYBLUE } },
    { text: "0", options: { color: BODYBLUE, bold: true } },
    { text: ", Last Position Encoding= ", options: { color: BODYBLUE } },
    { text: "1", options: { color: BODYBLUE, bold: true } },
    { text: "  ", options: { color: BODYBLUE } },
    { text: "(Independent of Seq. Length)", options: { color: RED, bold: true, underline: true } },
  ], {
    x: IN(63.5), y: IN(377.0), w: IN(845), h: IN(26),
    align: "left", valign: "top", margin: 0, lineSpacing: 23,
    fontSize: 17, italic: true, fontFace: FONT,
  });

  slide.addText("Problems:", {
    x: IN(62.5), y: IN(401.0), w: IN(200), h: IN(24),
    align: "left", valign: "top", margin: 0, lineSpacing: 23,
    fontSize: 17, bold: true, italic: true, color: RED, fontFace: FONT,
  });

  const dotCy = [437.5, 460.0, 506.0];
  for (const cy of dotCy) {
    slide.addShape(pptx.ShapeType.ellipse, {
      x: IN(87.8 - 4.75), y: IN(cy - 4.75), w: IN(9.5), h: IN(9.5),
      fill: { color: BODYBLUE }, line: { color: BODYBLUE, width: 0.25 },
    });
  }

  slide.addText([
    { text: "\u03B4", options: { color: BODYBLUE, bold: true } },
    { text: " Value depends on ", options: { color: BODYBLUE } },
    { text: "Seq. Length", options: { color: BODYBLUE, bold: true } },
    { text: "  ( ", options: { color: BODYBLUE } },
    { text: "\u03B4", options: { color: BOXRED } },
    { text: " is ", options: { color: BODYBLUE } },
    { text: "small for ", options: { color: BODYBLUE, underline: true } },
    { text: "long", options: { color: BODYBLUE, bold: true, underline: true } },
    { text: " seq", options: { color: BODYBLUE, underline: true } },
    { text: " and ", options: { color: BODYBLUE } },
    { text: "large for ", options: { color: BODYBLUE, underline: true } },
    { text: "short", options: { color: BODYBLUE, bold: true, underline: true } },
    { text: " sequence", options: { color: BODYBLUE, underline: true } },
    { text: " )", options: { color: BODYBLUE } },
  ], {
    x: IN(98.0), y: IN(424.0), w: IN(810), h: IN(24),
    align: "left", valign: "top", margin: 0, lineSpacing: 23,
    fontSize: 17, italic: true, fontFace: FONT,
  });

  slide.addText([
    { text: "In other words, Encoding value of  ", options: { color: BODYBLUE } },
    { text: "position # 4", options: { color: BOXRED, underline: true } },
    { text: "  in  ", options: { color: BODYBLUE, underline: true } },
    { text: "short", options: { color: BODYBLUE, bold: true, underline: true } },
    { text: "  seq", options: { color: BODYBLUE, underline: true } },
    { text: "  will  ", options: { color: BODYBLUE } },
    { text: "differ", options: { color: BODYBLUE, bold: true } },
    { text: "  from  ", options: { color: BODYBLUE } },
    { text: "position #4", options: { color: BOXRED, underline: true } },
    { text: "  in  ", options: { color: BODYBLUE } },
    { text: "long", options: { color: BODYBLUE, bold: true } },
    { text: "  seq", options: { color: BODYBLUE } },
  ], {
    x: IN(98.0), y: IN(446.0), w: IN(810), h: IN(24),
    align: "left", valign: "top", margin: 0, lineSpacing: 23,
    fontSize: 17, italic: true, fontFace: FONT,
  });

  slide.addText("(though they are same position)", {
    x: IN(83.5), y: IN(469.0), w: IN(500), h: IN(24),
    align: "left", valign: "top", margin: 0, lineSpacing: 23,
    fontSize: 17, bold: true, italic: true, color: MAG, fontFace: FONT,
  });

  slide.addText([
    { text: "Position Encoding is  ", options: { color: BODYBLUE } },
    { text: "scalar", options: { color: BODYBLUE, bold: true } },
    { text: "  and Word embedding is  ", options: { color: BODYBLUE } },
    { text: "vector", options: { color: BODYBLUE, bold: true } },
    { text: "   (how to Combine them ?)", options: { color: BODYBLUE } },
  ], {
    x: IN(98.0), y: IN(492.0), w: IN(810), h: IN(24),
    align: "left", valign: "top", margin: 0, lineSpacing: 23,
    fontSize: 17, italic: true, fontFace: FONT,
  });
}

module.exports = { renderBase };
