// slide_033.js — machine-learning/02_linear-regression-classification-MSSE
// "Classification  Example" — algorithm walkthrough (ROOT slide, no parents).
//
// Geometry PIL-measured 2026-10-13 from unique_slides/slide_033.jpg (960x540, 1px=1pt).
// Measurement record: scratch/ml02/slide033/{m6,m7,m8}_out.txt + measure*.py.
// Tables/equations: matplotlib mathtext compositions -> 600dpi transparent PNGs
// (build/assets/slide033_eq/) embedded at EXACT size (w=px/600in) per the
// equations-mathtext-png pattern; delimiter bars + minus dashes as plot segments.
// Measured color law: first vector element RED in ALL four panels (incl. positive 1s),
// cols 2-3 BLACK (negatives too); P3 values all RED ">0"; P1/P2 values RED/BLUE per
// class; headers NAVY 000080 with red words '-ve'/'-1' (H3) and '> 0'/'1'/'small' (H4);
// bottom boxes FBFFDA fill, C00000 2pt border; green rule 009900 y368 x84-411.
// Arrows: white-filled block arrows, pink F4C7C3 edge + CC0000 diagonal hatch,
// rendered as PNGs by the same generator (spec: hatched pink arrows).

const path = require("path");
const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require(path.join(__dirname, "..", "..", "shared_patterns", "house_chrome.js"));

const NUMERAL = "33";
const FONT = "Arial";
const sidecars = require(path.join(__dirname, "assets", "slide033_eq", "sidecars.json"));
const SIDE = {};
for (const s of sidecars) SIDE[s.name] = s;

const RED = "FF0000", BLUE = "0000CC", BLACK = "000000", NAVY = "000080";
const AQUA = "ECFDFA", PALEYEL = "FBFFDA", DKRED = "C00000", GREEN = "009900";

function px(v) { return v / 72; }

function drawPanels(pptx, slide) {
  // borderless pale-aqua panel rects (PIL probe 8 solid-fill rects)
  const panels = [
    { x: 107, y: 107, w: 271, h: 124 },  // P1 raw vectors
    { x: 500, y: 97, w: 397, h: 137 },   // P2 grouped classes
    { x: 500, y: 283, w: 397, h: 149 },  // P3 multiply -ve class
    { x: 75, y: 283, w: 364, h: 172 },   // P4 substitute >0 with 1
  ];
  for (const p of panels) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(p.x), y: px(p.y), w: px(p.w), h: px(p.h),
      fill: { color: AQUA }, line: { type: "none" },
    });
  }
}

function drawBoxes(pptx, slide) {
  // bottom result boxes (red border ~2pt, pale yellow fill)
  const boxes = [
    { x: 171, y: 466, w: 227, h: 57 },  // BL "The equation is in the form: Z W = Y"
    { x: 543, y: 477, w: 220, h: 37 },  // BR "W = (Z^T Z)^-1 Z^T Y"
  ];
  for (const b of boxes) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(b.x), y: px(b.y), w: px(b.w), h: px(b.h),
      fill: { color: PALEYEL }, line: { color: DKRED, width: 2 },
    });
  }
  // green rule separating P4 rows 2/3 (measured y367-369, x84-411)
  slide.addShape(pptx.ShapeType.line, {
    x: px(84), y: px(368), w: px(327), h: 0,
    line: { color: GREEN, width: 2.5 },
  });
}

function drawImages(slide) {
  for (const s of sidecars) {
    slide.addImage({
      path: path.join(__dirname, "assets", "slide033_eq", s.name + ".png"),
      x: px(s.x0), y: px(s.y0), w: px(s.w), h: px(s.h),
    });
  }
}

function drawTexts(pptx, slide) {
  // Title (ink measured x363..626 y58..84; same recipe as certified slide 034)
  slide.addText("Classification  Example", {
    x: px(362), y: px(52.5), w: px(300), h: px(36),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 25, bold: true, color: "CC0000",
  });
  // H2 — all navy (no red words measured)
  slide.addText("Rearrange vecotrs (group vectors in same class)", {
    x: px(507), y: px(98), w: px(340), h: px(22),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 14.5, color: NAVY,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(509), y: px(118.5), w: px(324), h: 0,
    line: { color: NAVY, width: 1 },
  });
  // H3 — '-ve' and '-1' red (measured red clusters x696-725, x811-823).
  // fs 16.5 calibrated closed-loop: fs13 rendered '-ve' at x658/end 748; the original
  // ink is x510..823 (313px) -> scale 1.27 lands '-ve' at ~699, '-1' end ~812.
  slide.addText([
    { text: "Multiply vectors belong to ", options: { color: NAVY } },
    { text: "-ve", options: { color: RED } },
    { text: " class with ", options: { color: NAVY } },
    { text: "-1", options: { color: RED } },
  ], {
    x: px(508), y: px(284), w: px(320), h: px(24),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 16.5,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(510), y: px(302.5), w: px(288), h: 0,
    line: { color: NAVY, width: 1 },
  });
  // H4 — '> 0', '1', 'small'(italic) red (measured red clusters x143-160, x200-204,
  // x308-340). fs 14.8 calibrated closed-loop: fs13 rendered 'small' at x279-309; the
  // original is x308-340 -> scale 1.14 lands 'small' at ~307-341, '1' at ~203.
  slide.addText([
    { text: "Substitute ", options: { color: NAVY } },
    { text: "> 0", options: { color: RED } },
    { text: " with ", options: { color: NAVY } },
    { text: "1", options: { color: RED } },
    { text: " (may use any ", options: { color: NAVY } },
    { text: "small", options: { color: RED, italic: true } },
    { text: " positive value)", options: { color: NAVY } },
  ], {
    x: px(76), y: px(284), w: px(380), h: px(24),
    align: "left", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 14.8,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(78), y: px(300.5), w: px(351), h: 0,
    line: { color: NAVY, width: 1 },
  });
  // BL box line 1
  slide.addText("The equation is in the form:", {
    x: px(173), y: px(468), w: px(223), h: px(22),
    align: "center", valign: "middle", margin: 0,
    fontFace: FONT, fontSize: 15, color: BLACK,
  });
}

function renderBase(pptx, slide) {
  drawHouseChrome(pptx, slide, { numeral: NUMERAL });
  drawPanels(pptx, slide);
  drawBoxes(pptx, slide);
  drawImages(slide);
  drawTexts(pptx, slide);
}

if (require.main === module) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const slide = pres.addSlide();
  renderBase(pres, slide);
  const out = path.join(__dirname, "..", "slide_033_recreated.pptx");
  pres.writeFile({ fileName: out })
    .then(() => console.log("WROTE", out))
    .catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, NUMERAL };
