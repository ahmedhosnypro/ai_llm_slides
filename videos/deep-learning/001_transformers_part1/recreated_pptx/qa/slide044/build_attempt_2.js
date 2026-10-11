// build/slide_044.js — slide 044 "Multi Head Self Attention of Word X2 'Wide'
// Architecture" (deep-learning/001_transformers_part1). CHILD of 44←43 (founder
// dependency graph): requires the certified parent component
// components/slide_043.js (renderBase, frozen) and draws ONLY this slide's delta.
//
// DELTA (PIL-measured on unique_slides/slide_044.jpg, 960x540, 1px=1pt, in=px/72;
// measurement scripts scratch/slide044/m1..m19):
//   1. TITLE REPLACED at child-measured position: the frame carries slide 43's
//      title runs drawn 9px LEFT of the parent's box (word-cluster scan m13:
//      every line-1 word shifted -9px, identical widths; IoU 0.753 @ dx=-9 vs
//      0.194 @ dx=0, m14; line2 IoU 0.755 @ dx=-9). Per 17 §3 the child's frame
//      is ground truth for inherited elements, so the parent title block is
//      skipped and re-drawn with the parent's exact runs at x-9px. (This is a
//      measured frame fact, NOT a manual shift of the diagram blocks — those
//      are untouched, per the dispatch.)
//   2. INSET (the pure addition): green-framed white panel x738..908, y80..298
//      (border ~4px #1F8A1C measured core (28,139,21)) reproducing the paper's
//      Figure 2 RIGHT topology in course style, drawn BOTTOM-UP with up arrows:
//      V,K,Q labels (y281..288) -> 3 thin up-arrows (shafts x763/x809/x855,
//      y278..240) -> three 'Linear' boxes (x745/x791/x837, y220..239, EACH with
//      TWO grey outlined duplicate boxes fanned behind it, tops y209/y214, right
//      slivers poking right) -> 3 hollow grey connectors w/ dark tips (y201..219)
//      -> lavender stack: front box x746..875, y170..200, #BEB4D4, black border,
//      2-line dark label 'Scaled Dot-Product'/'Attention' + TWO grey fanned
//      behind layers (tops y157/y163, right edges poking x~881/x~889) -> THREE
//      thin arrows rising into Concat (x805/x810/x815, middle strong) + a thin
//      diagonal arrow entering the stack from upper-left ((790,155)->(800,168))
//      -> pale-yellow 'Concat' box (x786..832, y128..149, fill F5FEC7) ->
//      'Linear' box (x790..831, y96..116) -> up output arrow (x810, y96..85).
//      'h' annotation right of the stack: bracket-like diagonal + tick + h.
//   3. OCCLUSIONS (reproduced by z-order — inset drawn AFTER renderBase, blocks
//      NOT shifted): the panel covers the title line-2 right tail (ink x738..797,
//      visible '"Wide" Architec'), the bottom-left arc of the '44' badge
//      (badge x875..911 y53..89 vs panel top y80), the h=5 tag (747..777,
//      198..212), the h=5 card's top-right corner and the h=5 dashed X-box top
//      (x748..790, y244..298; below y298 it shows again — measured identical).
//
// Frame-vs-spec notes (frame wins, recorded for the report):
//   - spec's 'Y1' output-vector label: frame shows NO delta vs 43 in the vecbox
//     region (m9) -> the certified Y2 rendering is inherited verbatim.
//   - spec's '4 groups of 3 cells' concat bar: frame identical to 43's certified
//     5-segment bar in that zone (diff y150..300 x<738 = 2px noise) -> inherited.
//   - spec's '4 overlapping purple boxes': frame shows front box + ONE behind
//     layer (top sliver y158..170, right sliver x875..881) -> 2 layers drawn.
//
// LAWS honored: playlist chrome via components/house_chrome.js (numeral = 44);
// verbatim text; margin:0 + fontFace everywhere; no '#' in hex; explicit
// lineSpacing on the multi-line stack label; single-version deliverable.

const path = require("path");
const pptxgen = require("pptxgenjs");
const { renderBase } = require(path.join(__dirname, "components", "slide_043.js"));

const OUT = path.join(__dirname, "..", "slide_044_recreated.pptx");

const px = (v) => v / 72;
const SANS = "Arial";

// inset palette (pixel-measured cores)
const IC = {
  panelBorder: "1F8A1C",   // (28,139,21) median of 7 border samples
  boxBorder: "1A1A1A",     // near-black box borders
  ink: "1A1A1A",
  arrow: "222222",
  concatFill: "F5FEC7",    // (245,254,199)
  stackFront: "BEB4D4",    // (186,177,204)/(196,186,221)
  stackBehind: "E0E0EA",   // (224,224,234)
  stackBehindLine: "A0A0B0",
  shadow: "B4B6B3",        // (178,180,177) gray shadow strips/connectors
  shadowLine: "555555",
};

function text(slide, str, o) {
  slide.addText(str, Object.assign({ fontFace: SANS, margin: 0 }, o));
}

// ---- delta 1: title at the child-measured position (parent runs, x -9px) ----

function drawTitle44(pptx, slide) {
  // line 1 — parent runs; box x 491 (center 691) so ink lands at the measured
  // 44-frame center 688 (43's ink center 697 under the parent's x500 box)
  text(slide, [
    { text: "Multi Head Self Attention of Word ", options: { color: "333333" } },
    { text: "X", options: { color: "C00000" } },
    { text: "2", options: { color: "C00000", subscript: true, fontSize: 14 } },
  ], {
    x: px(491), y: px(48), w: px(400), h: px(30), align: "center", valign: "middle",
    bold: true, fontSize: 20,
  });
  // line 2 — same runs; right tail occluded by the inset (z-order)
  text(slide, [
    { text: "\u201C", options: { color: "333333" } },
    { text: "Wide", options: { color: "1F1F8C", highlight: "FFFF00" } },
    { text: "\u201D Architecture", options: { color: "333333" } },
  ], {
    x: px(491), y: px(77), w: px(400), h: px(24), align: "center", valign: "middle",
    bold: true, fontSize: 20,
  });
}

// ---- delta 2: the Figure-2-right inset (drawn ON TOP of the inherited base) --

function drawInset(pptx, slide) {
  // panel: green border, white fill — covers title tail, badge arc, h=5 tag/card.
  // Centerline x740..906 / y82..296 so the 3.5pt stroke lands on the measured
  // border bands (738-741 / 904-908 / 80-83 / 294-298) — keeps the original's
  // 2px title sliver visible above the top stroke.
  slide.addShape(pptx.ShapeType.rect, {
    x: px(740), y: px(82), w: px(166), h: px(214),
    fill: { color: "FFFFFF" }, line: { color: IC.panelBorder, width: 3.5 },
  });

  // top output arrow: up, from the top Linear box toward the panel border
  slide.addShape(pptx.ShapeType.line, {
    x: px(810.5), y: px(85.5), w: 0, h: px(10.5),
    line: { color: IC.arrow, width: 1.5, beginArrowType: "triangle" },
  });

  // top Linear box (x790..831, y96..116)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(790), y: px(96), w: px(41), h: px(20),
    fill: { color: "FFFFFF" }, line: { color: IC.boxBorder, width: 1.75 },
  });
  text(slide, "Linear", {
    x: px(790), y: px(96), w: px(41), h: px(20), align: "center", valign: "middle",
    fontSize: 8, color: IC.ink,
  });

  // arrow Linear -> Concat (down)
  slide.addShape(pptx.ShapeType.line, {
    x: px(810.5), y: px(116), w: 0, h: px(12),
    line: { color: IC.arrow, width: 1.5, endArrowType: "triangle" },
  });

  // Concat box (x786..832, y128..149), pale yellow fill, dark border
  slide.addShape(pptx.ShapeType.rect, {
    x: px(786), y: px(128), w: px(46), h: px(21),
    fill: { color: IC.concatFill }, line: { color: IC.boxBorder, width: 1.75 },
  });
  text(slide, "Concat", {
    x: px(786), y: px(128), w: px(46), h: px(21), align: "center", valign: "middle",
    fontSize: 8.5, color: IC.ink,
  });

  // attention stack: THREE layers — two grey outlined boxes fanned behind the
  // lavender front box, offset up-right (measured top edges y157/y163/y169;
  // right edges poke out at x~881 and x~889; left edges hidden behind the front)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(760), y: px(157), w: px(129), h: px(31), rectRadius: 0.06,
    fill: { color: "ECECF2" }, line: { color: "A8A8B2", width: 0.75 },
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(753), y: px(163), w: px(129), h: px(31), rectRadius: 0.06,
    fill: { color: "E4E4EE" }, line: { color: "999AA4", width: 1 },
  });

  // three thin arrows rising from the stack into Concat (heads at top; the
  // middle one strong/dark per the frame's highlighted centre shaft)
  slide.addShape(pptx.ShapeType.line, {
    x: px(805.5), y: px(149.5), w: 0, h: px(15.5),
    line: { color: "444444", width: 1, beginArrowType: "triangle" },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(810.5), y: px(149.5), w: 0, h: px(15.5),
    line: { color: "1A1A1A", width: 1.75, beginArrowType: "triangle" },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(815.5), y: px(149.5), w: 0, h: px(15.5),
    line: { color: "444444", width: 1, beginArrowType: "triangle" },
  });

  // thin diagonal arrow entering the stack from upper-left (measured
  // (790,155)->(800,168), head at the lower-right end)
  slide.addShape(pptx.ShapeType.line, {
    x: px(790), y: px(155), w: px(9.5), h: px(12.5),
    line: { color: "333333", width: 1, endArrowType: "triangle" },
  });

  // front stack box (x746..875, y170..200) + 2-line label (explicit pitch)
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(746), y: px(169.5), w: px(129), h: px(30.5), rectRadius: 0.08,
    fill: { color: IC.stackFront }, line: { color: "141414", width: 1.75 },
  });
  text(slide, [
    { text: "Scaled Dot-Product", options: { breakLine: true } },
    { text: "Attention", options: {} },
  ], {
    x: px(746), y: px(169.5), w: px(129), h: px(30.5), align: "center", valign: "middle",
    fontSize: 8, color: IC.ink, lineSpacing: 10,
  });

  // h annotation right of the stack, per the frame: bracket-like diagonal stroke
  // down the stack's right edge + short horizontal tick + upright 'h'
  slide.addShape(pptx.ShapeType.line, {
    x: px(884), y: px(172), w: px(6), h: px(11), flipH: true,
    line: { color: "333333", width: 1.25 },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: px(878), y: px(184.5), w: px(11), h: 0,
    line: { color: "333333", width: 1 },
  });
  text(slide, "h", {
    x: px(881), y: px(185), w: px(12), h: px(11), align: "center", valign: "middle",
    fontSize: 8, color: IC.ink,
  });

  // per bottom Linear box: TWO grey outlined duplicate boxes fanned behind it
  // (measured: faint top edge y209-210 w/ rounded corners + strong band y214-216;
  // right slivers at x785-787 and x791-795 for box A) — then the white box.
  for (const bx of [745, 791, 837]) {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(bx + 8), y: px(209), w: px(41), h: px(20), rectRadius: 0.06,
      fill: { color: "D6D8D5" }, line: { color: "9A9C98", width: 0.75 },
    });
    slide.addShape(pptx.ShapeType.roundRect, {
      x: px(bx + 4), y: px(214), w: px(43), h: px(20), rectRadius: 0.06,
      fill: { color: "C6C8C5" }, line: { color: "8A8C88", width: 1 },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: px(bx), y: px(220), w: px(39), h: px(20),
      fill: { color: "E9EDE9" }, line: { color: IC.boxBorder, width: 1.75 },
    });
    text(slide, "Linear", {
      x: px(bx), y: px(220), w: px(39), h: px(20), align: "center", valign: "middle",
      fontSize: 7.5, color: IC.ink,
    });
  }

  // three hollow grey connectors (boxes -> stack): dark tip at top, dark side
  // edges, no fill so the fanned layers show through (measured white interior
  // above y209, grey below)
  for (const cx of [762, 808, 854]) {
    slide.addShape(pptx.ShapeType.rect, {
      x: px(cx), y: px(201), w: px(8), h: px(19),
      fill: { type: "none" }, line: { color: "3A3A3A", width: 1 },
    });
    slide.addShape(pptx.ShapeType.triangle, {
      x: px(cx - 0.5), y: px(201), w: px(9), h: px(4.5),
      fill: { color: "333333" }, line: { type: "none" },
    });
  }

  // three thin up-arrows V/K,Q -> boxes (heads at top, y240..278)
  for (const ax of [763.5, 809.5, 855.5]) {
    slide.addShape(pptx.ShapeType.line, {
      x: px(ax), y: px(240), w: 0, h: px(38),
      line: { color: IC.arrow, width: 1.25, beginArrowType: "triangle" },
    });
  }

  // V, K, Q labels (y279..291), centered under the arrows
  const vkq = [["V", 763.5], ["K", 809.5], ["Q", 855.5]];
  for (const [t, cx] of vkq) {
    text(slide, t, {
      x: px(cx - 8), y: px(279), w: px(16), h: px(12), align: "center", valign: "middle",
      fontSize: 8, color: IC.ink,
    });
  }
}

// ---- composition ---------------------------------------------------------------

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// certified parent base (chrome with numeral 44 + all 18 blocks except title)
renderBase(pres, slide, { numeral: 44, skip: ["title"] });

// child delta — title first (same layer as the parent's would be), then the
// inset LAST so it sits on top and reproduces the original's occlusions
drawTitle44(pres, slide);
drawInset(pres, slide);

pres.writeFile({ fileName: OUT }).then(() => {
  console.log("WROTE", OUT);
});
