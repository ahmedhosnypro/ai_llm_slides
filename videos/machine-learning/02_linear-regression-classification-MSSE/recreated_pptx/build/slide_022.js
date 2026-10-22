// slide_022.js — "Monotonic Functions" (ML lecture 02, root slide, no dependents)
//
// Ground truth (PIL-measured from unique_slides/slide_022.jpg, 960x540, 1px=1pt):
//   title ink "Monotonic Functions" x326..621 y74..95 (center 473.5, 84.5)
//   3 white panels w/ dark-navy border: p1 (103,123,200,209) p2 (386,123,201,209)
//     p3 (666,123,201,209); border core #3B318C (nominal 33297E)
//   red L-axes per panel (nominal C00000): vaxis p1 x119 y133..307, p2 x404 y135..309,
//     p3 x682 y136..311; haxis p1 y307.5 ->x289, p2 y309.5 ->x570, p3 y311.5 ->x849.5
//   O/P labels right of vaxis top; I/P labels under haxis right end (12pt bold red)
//   blue curves (nominal 4E44A8): matplotlib 600dpi PNGs over full panel rects
//     (assets/slide022_p{1,2,3}_curve.png, sidecar slide022_curves_sidecar.json)
//   green dashed arrows (light shaft 9DBE85 sysDot 1pt + solid head 45771D):
//     p1 UP head(152..159,196..203); p1 RIGHT head(210..218,288..295)
//     p2 DOWN head(424..431,254..262); p2 RIGHT head(480..487,290..298)
//     p3 DOWN(694..701,241..249) UP(782..789,207..217) DOWN(824..831,241..249)
//     p3 RIGHT heads x740/787/854 at y~299
//   tan guide lines p3: x747 + x795, y135..318 (nominal E2CBA8, 1pt)
//   captions 22pt bold red, 2 lines, pitch 27: c1 center 193.5, c2 486, c3 776
//     L1 cap top y359, L2 cap top y386
//   defbox rect x118..863 y427..503, fill FAFCE7, thin rose border C0504D 1pt;
//     serif 18pt text, 2 lines, pitch 33, left x128, L1 cap top y447
//   mouse cursor at ~(345,350): screen-recording artifact — NEVER drawn (judge
//     GROUND RULES (c))
//   badge = house chrome canon (876,73) d35, numeral 22
//
// House chrome: shared_patterns/house_chrome.js (THIS deck: white FFFFFF canvas,
// gray E9E9E7 panel x61..899 y46->bottom, C00000 1pt border, bottom stroke rows
// 538-539, badge FDFD96 + 6A5ACD ring, numeral 333333 Arial 18pt bold).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { drawHouseChrome } = require(path.resolve(__dirname, "../../shared_patterns/house_chrome.js"));

// ---- nominal colors (measured cores; JPEG-soft originals -> family nominals)
const C_TITLE = "C00000";     // title + captions red (measured luma ~CC0000)
const C_AXIS = "C00000";      // axes red
const C_PANEL_BORDER = "33297E"; // panel border dark navy
const C_CURVE = "4E44A8";     // baked into PNGs
const C_ARROW_HEAD = "45771D";
const C_ARROW_SHAFT = "9DBE85";
const C_TAN = "E2CBA8";
const C_DEF_FILL = "FAFCE7";
const C_DEF_BORDER = "C0504D";
const C_DEF_TEXT = "26261E";
const C_LABEL = "C00000";     // O/P, I/P labels

const PX = 1 / 72; // 1px = 1pt = 1/72 in

// ---- per-panel measured geometry -------------------------------------------
const PANELS = {
  p1: { rect: [103, 123, 200, 209],
        vaxis: [119, 142, 119, 307], vhead: [119, 133],
        haxis: [119, 307.5, 280, 307.5], hhead: [284.5, 307.5],
        op: [124, 138], ip: [262, 311] },
  p2: { rect: [386, 123, 201, 209],
        vaxis: [404, 144, 404, 309], vhead: [404, 135],
        haxis: [404, 309.5, 561, 309.5], hhead: [565.5, 309.5],
        op: [410, 138], ip: [540, 311] },
  p3: { rect: [666, 123, 201, 209],
        vaxis: [682, 145, 682, 311], vhead: [682, 136],
        haxis: [682, 311.5, 840, 311.5], hhead: [845, 311.5],
        op: [688, 141], ip: [822, 310] },
};

// green arrows: [shaftX1, shaftY, shaftX2] vertical or [x, y, x2] horizontal
const ARROWS = [
  // p1
  { panel: "p1", kind: "v", x: 155.5, y1: 206, y2: 297, head: "up",    hc: [155.5, 200] },
  { panel: "p1", kind: "h", y: 291.5, x1: 170, x2: 207, head: "right", hc: [213.5, 291.5] },
  // p2
  { panel: "p2", kind: "v", x: 427.5, y1: 152, y2: 252, head: "down",  hc: [427.5, 258] },
  { panel: "p2", kind: "h", y: 294, x1: 433, x2: 478, head: "right",   hc: [483.5, 294] },
  // p3
  { panel: "p3", kind: "v", x: 697.5, y1: 200, y2: 239, head: "down",  hc: [697.5, 245] },
  { panel: "p3", kind: "v", x: 785.5, y1: 219, y2: 295, head: "up",    hc: [785.5, 212] },
  { panel: "p3", kind: "v", x: 827.5, y1: 195, y2: 239, head: "down",  hc: [827.5, 245] },
  { panel: "p3", kind: "h", y: 299.5, x1: 686, x2: 731, head: "right", hc: [736, 299.5] },
  { panel: "p3", kind: "h", y: 299.5, x1: 745, x2: 782, head: "right", hc: [787, 299.5] },
  { panel: "p3", kind: "h", y: 299.5, x1: 800, x2: 849, head: "right", hc: [854, 299.5] },
];

const TAN_LINES = [747, 795]; // p3, y135..318
const ASSETS = path.resolve(__dirname, "assets");

// ---- per-block draws (component exports) ------------------------------------
function drawPanel(pptx, slide, p) {
  const [x, y, w, h] = p.rect;
  slide.addShape(pptx.ShapeType.rect, {
    x: x * PX, y: y * PX, w: w * PX, h: h * PX,
    fill: { color: "FFFFFF" },
    line: { color: C_PANEL_BORDER, width: 2 },
  });
}

function drawTanLines(pptx, slide) {
  for (const tx of TAN_LINES) {
    slide.addShape(pptx.ShapeType.line, {
      x: tx * PX, y: 135 * PX, w: 0, h: (318 - 135) * PX,
      line: { color: C_TAN, width: 1 },
    });
  }
}

function drawArrowHead(pptx, slide, dir, cx, cy) {
  // solid triangle, 9x9 box centered (cx, cy); apex points `dir`
  const opts = {
    x: (cx - 4.5) * PX, y: (cy - 4.5) * PX, w: 9 * PX, h: 9 * PX,
    fill: { color: C_ARROW_HEAD }, line: { type: "none" },
  };
  if (dir === "down") opts.flipV = true;
  if (dir === "right") opts.rotate = 90;
  if (dir === "left") opts.rotate = 270;
  slide.addShape(pptx.ShapeType.triangle, opts);
}

function drawArrows(pptx, slide) {
  for (const a of ARROWS) {
    if (a.kind === "v") {
      slide.addShape(pptx.ShapeType.line, {
        x: a.x * PX, y: a.y1 * PX, w: 0, h: (a.y2 - a.y1) * PX,
        line: { color: C_ARROW_SHAFT, width: 1, dashType: "sysDot" },
      });
    } else {
      slide.addShape(pptx.ShapeType.line, {
        x: a.x1 * PX, y: a.y * PX, w: (a.x2 - a.x1) * PX, h: 0,
        line: { color: C_ARROW_SHAFT, width: 1, dashType: "sysDot" },
      });
    }
    drawArrowHead(pptx, slide, a.head, a.hc[0], a.hc[1]);
  }
}

function drawCurve(pptx, slide, key) {
  // 600dpi transparent PNG covering the full panel rect; embed at exact size
  slide.addImage({
    path: path.join(ASSETS, `slide022_${key}_curve.png`),
    x: PANELS[key].rect[0] * PX, y: PANELS[key].rect[1] * PX,
    w: PANELS[key].rect[2] * PX, h: PANELS[key].rect[3] * PX,
  });
}

function drawAxes(pptx, slide, p) {
  const [vx1, vy1, vx2, vy2] = p.vaxis;
  const [hx1, hy1, hx2, hy2] = p.haxis;
  slide.addShape(pptx.ShapeType.line, {
    x: vx1 * PX, y: vy1 * PX, w: 0, h: (vy2 - vy1) * PX,
    line: { color: C_AXIS, width: 2 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: hx1 * PX, y: hy1 * PX, w: (hx2 - hx1) * PX, h: 0,
    line: { color: C_AXIS, width: 2 },
  });
  // UP head at vaxis top; RIGHT head at haxis end
  slide.addShape(pptx.ShapeType.triangle, {
    x: (p.vhead[0] - 4.5) * PX, y: p.vhead[1] * PX, w: 9 * PX, h: 9 * PX,
    fill: { color: C_AXIS }, line: { type: "none" },
  });
  slide.addShape(pptx.ShapeType.triangle, {
    x: (p.hhead[0] - 4.5) * PX, y: (p.hhead[1] - 4.5) * PX, w: 9 * PX, h: 9 * PX,
    fill: { color: C_AXIS }, line: { type: "none" }, rotate: 90,
  });
}

function drawAxisLabels(pptx, slide, p) {
  slide.addText("O/P", {
    x: p.op[0] * PX, y: p.op[1] * PX, w: 26 * PX, h: 13 * PX,
    fontSize: 12, bold: true, color: C_LABEL, fontFace: "Arial",
    align: "left", valign: "middle", margin: 0,
  });
  slide.addText("I/P", {
    x: p.ip[0] * PX, y: p.ip[1] * PX, w: 27 * PX, h: 13 * PX,
    fontSize: 12, bold: true, color: C_LABEL, fontFace: "Arial",
    align: "right", valign: "top", margin: 0,
  });
}

function drawTitle(pptx, slide, opts = {}) {
  slide.addText(opts.text || "Monotonic Functions", {
    x: (opts.cx !== undefined ? opts.cx - 300 : 173.5) * PX,
    y: (opts.cy !== undefined ? opts.cy - 36 : 48) * PX,
    w: 600 * PX, h: 72 * PX,
    align: "center", valign: "middle",
    fontSize: opts.size || 30, bold: true, color: C_TITLE,
    fontFace: "Arial", margin: 0,
  });
}

function drawCaption(pptx, slide, lines, centerX, capTopY) {
  slide.addText(lines.map((t) => ({ text: t, options: { breakLine: true } })), {
    x: (centerX - 85) * PX, y: capTopY * PX, w: 170 * PX, h: 56 * PX,
    align: "center", valign: "top",
    fontSize: 22, bold: true, color: C_TITLE, fontFace: "Arial",
    lineSpacing: 27, margin: 0,
  });
}

function drawDefBox(pptx, slide, opts = {}) {
  const top = opts.top !== undefined ? opts.top : 427;
  const left = opts.left !== undefined ? opts.left : 118;
  slide.addShape(pptx.ShapeType.rect, {
    x: left * PX, y: top * PX, w: 745 * PX, h: 76 * PX,
    fill: { color: C_DEF_FILL },
    line: { color: C_DEF_BORDER, width: 1 },
  });
  const reg = { fontSize: 19, color: C_DEF_TEXT, fontFace: "Times New Roman" };
  const bold = Object.assign({}, reg, { bold: true });
  const line1 = [
    { text: "For Monotonically ", options: reg },
    { text: "increase", options: bold },
    { text: " function:  When Input ", options: reg },
    { text: "increases", options: bold },
    { text: " \u2192 Output ", options: reg },
    { text: "increases", options: bold },
  ];
  const line2 = [
    { text: "For Monotonically ", options: reg },
    { text: "decrease", options: bold },
    { text: " function:  When Input ", options: reg },
    { text: "increases", options: bold },
    { text: " \u2192 Output ", options: reg },
    { text: "decreases", options: bold },
  ];
  slide.addText(
    line1.concat([{ text: "", options: { breakLine: true } }]).concat(line2),
    {
      x: (opts.textLeft !== undefined ? opts.textLeft : 127) * PX,
      y: (opts.textTop !== undefined ? opts.textTop : 430) * PX,
      w: 710 * PX, h: 70 * PX,
      align: "left", valign: "top",
      fontSize: 19, color: C_DEF_TEXT, fontFace: "Times New Roman",
      lineSpacing: 33, margin: 0,
    }
  );
}

// renderBase: full slide composition
function renderBase(pptx, slide, opts = {}) {
  drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 22 : opts.numeral });
  for (const key of ["p1", "p2", "p3"]) drawPanel(pptx, slide, PANELS[key]);
  drawTanLines(pptx, slide);
  drawArrows(pptx, slide);
  for (const key of ["p1", "p2", "p3"]) drawCurve(pptx, slide, key);
  for (const key of ["p1", "p2", "p3"]) {
    drawAxes(pptx, slide, PANELS[key]);
    drawAxisLabels(pptx, slide, PANELS[key]);
  }
  drawTitle(pptx, slide, opts.title || {});
  drawCaption(pptx, slide, ["Monotonically", "Increase"], 193.5, 353);
  drawCaption(pptx, slide, ["Monotonically", "Decrease"], 486, 353);
  drawCaption(pptx, slide, ["Not", "Monotonic"], 776, 353);
  drawDefBox(pptx, slide, opts.defbox || {});
}

// ---- build ------------------------------------------------------------------
function build(outPath) {
  const pptx = new pptxgen();
  pptx.layout = "LAYOUT_WIDE";
  const slide = pptx.addSlide();
  renderBase(pptx, slide);
  return pptx.writeFile({ fileName: outPath }).then(() => console.log("written:", outPath));
}

if (require.main === module) {
  const out =
    process.argv[2] ||
    path.resolve(__dirname, "../slide_022_recreated.pptx");
  build(out).catch((e) => { console.error(e); process.exit(1); });
}

module.exports = { renderBase, drawTitle, drawDefBox, PANELS, ARROWS };
