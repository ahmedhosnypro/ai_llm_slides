// Slide 039 — machine-learning/02_linear-regression-classification-MSSE
// "One vs All   (for Multi Class Classification)"
// Root slide (no parents, no children per the dispatch brief).
//
// Structure (all geometry PIL-measured from unique_slides/slide_039.jpg, 960x540, 1px=1pt):
//   1. house chrome via shared module — numeral 39 (badge = printed number)
//   2. scatter chart as ONE generated graph image (gen-3 point extraction +
//      gen-4 re-render with measured plot box x93.5..234 y76..186, per-spine colors,
//      x labels -3..4 CONFIRMED present via vision read of the frame crop)
//   3. title: single line, ink x319..785 y69..90 (center x552 — NOT slide-centered;
//      frame wins) — bold ~25pt 8B0000
//   4. Training Sample box (tan), three dark model boxes (white bold 2-line text,
//      curly quotes), three pastel output boxes (dark 2-line text, left-aligned at
//      x548; ALL THREE read +ve if Class "1" — verified verbatim on the original by
//      crop vision 2026-10-13), Decision box (light fill + brown border)
//   5. fan arrows: light-gray hairline shafts (custGeom cubic beziers, fitted by
//      gen-3 LSQ, curves.json) + dark-brown triangular heads; model->output arrows
//      straight with red/blue/green heads matching their model
//   6. Decision Rules panel: underlined bold black header; three rules with the
//      -> arrows ALIGNED in a column at x~466 in the original — replicated with
//      per-rule segment boxes (left part / arrow / right part), rule colors
//      green/red/purple (measured mid-tones)
const pptxgen = require("pptxgenjs");

const HOUSE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/shared_patterns/house_chrome.js";
const CHART = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/assets/slide039_chart.png";
const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/slide_039_recreated.pptx";

const { drawHouseChrome } = require(HOUSE);

const px = (v) => v / 72; // frame px -> inches (1px = 1pt = 1/72 in)
const FONT = "Arial";

// measured colors (frame modals / darkest cores, 2026-10-13)
const C = {
  title: "8B0000",
  m1: "9F0000", m2: "0200A9", m3: "055927",
  obFill1: "FBCCCE", obFill2: "E3FFFB", obFill3: "D6FFEA",
  obLine1: "9C0014", obLine2: "0F00A8", obLine3: "148E15",
  tsFill: "DDD0C0", tsLine: "B5AC9D", tsText: "5A3A1C",
  decFill: "F8FCEE", decLine: "674B36", decText: "2B2E22",
  rulesFill: "F8FCEE", rulesLine: "5F2126",
  rule1: "2E7A24", rule2: "B01020", rule3: "8A1E8A",
  shaft: "A6A5A1", headBrown: "623E17",
  headRed: "C3000B", headBlue: "0400C0", headGreen: "0D9608",
};

// gen-3 LSQ-fitted fan-arrow beziers (curves.json); dec endpoints extended x751->756.5
// to meet the measured head base at x757 (heads x757..764 tip on the Dec border x765)
const CURVES = {
  ts_m1: { p0: [237, 249.5], c1: [287.19, 255.56], c2: [277.46, 152.29], p3: [311, 157] },
  ts_m2: { line: [[237, 249.5], [310, 249.5]] },
  ts_m3: { p0: [237, 249.5], c1: [286.57, 241.86], c2: [279.17, 344.03], p3: [311, 339.5] },
  dec_ob1: { p0: [692, 157], c1: [740.36, 159.24], c2: [722.36, 228.17], p3: [756.5, 249.5] },
  dec_ob2: { line: [[692, 249.5], [756.5, 249.5]] },
  dec_ob3: { p0: [692, 339.5], c1: [740.46, 337.58], c2: [722.26, 270.25], p3: [756.5, 249.5] },
};

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
pptx.author = "ai_llm_slides";
pptx.title = "Slide 39";

const slide = pptx.addSlide();
drawHouseChrome(pptx, slide, { numeral: "39" });

// --- 2. generated scatter chart (baked red rect + plot box + ticks + labels) ---
slide.addImage({ path: CHART, x: px(78), y: px(67), w: px(165), h: px(132) });

// --- 3. title (ink center x552, band y69..90; 23pt from closed-loop render match) ---
slide.addText("One vs All   (for Multi Class Classification)", {
  x: px(96), y: px(56), w: px(912), h: px(40),
  fontSize: 23, bold: true, color: C.title, fontFace: FONT,
  align: "center", valign: "middle", margin: 0,
});

// --- 4a. Training Sample box (x99..234.5 y219..279.5) ---
slide.addShape(pptx.ShapeType.rect, {
  x: px(99), y: px(219), w: px(135.5), h: px(60.5),
  fill: { color: C.tsFill }, line: { color: C.tsLine, width: 1 },
});
  slide.addText(
    [
      { text: "Training", options: { breakLine: true } },
      { text: "Sample", options: {} },
    ],
    {
      x: px(99), y: px(219), w: px(135.5), h: px(60.5),
      fontSize: 16, bold: true, color: C.tsText, fontFace: FONT,
      align: "center", valign: "middle", lineSpacing: 19, margin: 0,
    }
  );

// --- 4b. model boxes (x317..515) ---
const models = [
  { y: 119.5, h: 75, fill: C.m1, cls: "1" },
  { y: 213, h: 73.5, fill: C.m2, cls: "2" },
  { y: 302, h: 74.5, fill: C.m3, cls: "3" },
];
for (const m of models) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(317), y: px(m.y), w: px(198), h: px(m.h),
    fill: { color: m.fill },
  });
  slide.addText(
    [
      { text: "Classification Model", options: { bold: true, fontSize: 17, breakLine: true } },
      { text: `(of Class \u201C${m.cls}\u201D)`, options: { fontSize: 15 } },
    ],
    {
      x: px(317), y: px(m.y), w: px(198), h: px(m.h),
      fontSize: 15.5, bold: true, color: "FFFFFF", fontFace: FONT,
      align: "center", valign: "middle", lineSpacing: 20, margin: 0,
    }
  );
}

// --- 4c. output boxes (x547.5..690.5; left border measured x548-549 — the x539 red
// ink is the arrowhead, not the border; text CENTERED in the box, center x~619) —
// ALL THREE verbatim "+ve if Class "1"" ---
const obs = [
  { y: 131, h: 52.5, fill: C.obFill1, line: C.obLine1 },
  { y: 223, h: 53.5, fill: C.obFill2, line: C.obLine2 },
  { y: 313, h: 52.5, fill: C.obFill3, line: C.obLine3 },
];
for (const ob of obs) {
  slide.addShape(pptx.ShapeType.rect, {
    x: px(547.5), y: px(ob.y), w: px(143), h: px(ob.h),
    fill: { color: ob.fill }, line: { color: ob.line, width: 1 },
  });
  slide.addText(
    [
      { text: "+ve if Class \u201C1\u201D", options: { bold: true, fontSize: 13, breakLine: true } },
      { text: "-ve for other classes", options: { fontSize: 14 } },
    ],
    {
      x: px(547.5), y: px(ob.y), w: px(143), h: px(ob.h),
      fontSize: 14, color: "000000", fontFace: FONT,
      align: "center", valign: "middle", lineSpacing: 15, margin: 0,
    }
  );
}

// --- 4d. Decision box (x765..850.5 y219..280) ---
slide.addShape(pptx.ShapeType.rect, {
  x: px(765), y: px(219), w: px(85.5), h: px(61),
  fill: { color: C.decFill }, line: { color: C.decLine, width: 1 },
});
slide.addText("Decision", {
  x: px(765), y: px(219), w: px(85.5), h: px(61),
  fontSize: 12.5, bold: true, color: C.decText, fontFace: FONT,
  align: "center", valign: "middle", margin: 0,
});

// --- 5. arrows: hairline shafts + explicit triangular heads ---
function custCurve(cv) {
  const start = cv.p0 || cv.line[0];
  const points = [{ x: px(start[0]), y: px(start[1]), moveTo: true }];
  if (cv.line) {
    points.push({ x: px(cv.line[1][0]), y: px(cv.line[1][1]) });
  } else {
    points.push({
      x: px(cv.p3[0]), y: px(cv.p3[1]),
      curve: { type: "cubic", x1: px(cv.c1[0]), y1: px(cv.c1[1]), x2: px(cv.c2[0]), y2: px(cv.c2[1]) },
    });
  }
  slide.addShape(pptx.ShapeType.custGeom, {
    x: 0, y: 0, w: 13.333, h: 7.5, // full-slide bbox; absolute inch points
    line: { color: C.shaft, width: 0.75 }, // no fill option -> <a:noFill/>
    points,
  });
}
for (const key of ["ts_m1", "ts_m2", "ts_m3", "dec_ob1", "dec_ob2", "dec_ob3"]) custCurve(CURVES[key]);
// model -> output straight shafts (x516..542 at the three lane centers; head base at 539.5)
for (const y of [157.5, 249.5, 339.5]) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(516), y: px(y), w: px(26), h: 0,
    line: { color: C.shaft, width: 0.75 },
  });
}
// heads: right-pointing triangles (default triangle points up; rotate 90), 8x8px
function head(x, y, color) {
  slide.addShape(pptx.ShapeType.triangle, {
    x: px(x), y: px(y), w: px(8), h: px(8), rotate: 90,
    fill: { color }, line: { color, width: 0 },
  });
}
head(309.5, 153.5, C.headBrown);  // TS -> m1 (tip x317.5, y157.5)
head(309.5, 245.5, C.headBrown);  // TS -> m2 (tip x317.5, y249.5)
head(309.5, 335.5, C.headBrown);  // TS -> m3 (tip x317.5, y339.5)
head(539.5, 153.5, C.headRed);    // m1 -> ob1 (tip x547.5 on the left border x548-549)
head(539.5, 245.5, C.headBlue);   // m2 -> ob2
head(539.5, 335.5, C.headGreen);  // m3 -> ob3
head(757, 245.5, C.headBrown);    // ob* -> Decision (tip x765 on the border; heads overlap in the original)

// --- 6. Decision Rules panel (x86..861.5 y413..526.5) ---
slide.addShape(pptx.ShapeType.rect, {
  x: px(86), y: px(413), w: px(775.5), h: px(113.5),
  fill: { color: C.rulesFill }, line: { color: C.rulesLine, width: 1 },
});
// underlined header (ink x96..213 y426..441)
slide.addText("Decision Rules", {
  x: px(96), y: px(420), w: px(250), h: px(24),
  fontSize: 16, bold: true, color: "000000", fontFace: FONT,
  underline: true, align: "left", valign: "middle", margin: 0,
});
// three rules — -> arrows aligned in a column at x~466 (measured), as segment boxes;
// 18pt (closed-loop match; 18.5 wrapped r2 seg1 in LO), arrow glyph 12pt (original ~8px)
function rule(bandCenter, color, seg1, seg2) {
  const y = bandCenter - 12;
  slide.addText(seg1, {
    x: px(96), y: px(y), w: px(358), h: px(24),
    fontSize: 18, color, fontFace: FONT,
    align: "left", valign: "middle", margin: 0,
  });
  slide.addText("\u2192", {
    x: px(456), y: px(y), w: px(22), h: px(24),
    fontSize: 12, color, fontFace: FONT,
    align: "center", valign: "middle", margin: 0,
  });
  slide.addText(seg2, {
    x: px(481), y: px(y), w: px(370), h: px(24),
    fontSize: 18, color, fontFace: FONT,
    align: "left", valign: "middle", margin: 0,
  });
}
rule(457, C.rule1, "Number of Positive output  (Only One)", "Input is properly Classified");
rule(483, C.rule2, "Number of Positive output  (More than One)", "can NOT define the class");
rule(508.5, C.rule3, "NO Positive output", "Not one of the classes  (new class)");

pptx.writeFile({ fileName: OUT }).then(() => console.log("wrote", OUT));
