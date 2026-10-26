// components/slide_018.js — slide 018 composition. CHILD of slide 017 (certified,
// frozen): requires ./slide_017.js and calls its renderBase at block granularity,
// skipping 17's left annotation column (callout1..4 + leader1..4). NEVER re-derives
// or copies parent geometry — the entire right-side Figure-1 architecture, title,
// yellow band, feeds and feedback come from the parent component untouched.
//
// SLIDE 018 DELTA (PIL-measured on unique_slides/slide_018.jpg, 960x540, 1px=1pt,
// in = px/72; scans in scratch/slide018/m0..m20 + vision probes probe_banner /
// probe_sdpa / probe_mhainset / probe_encmha / probe_gap through the gate):
//   banner1        peach callout x71-488 y104-145, fill F2C699, 2 lines (L1 black,
//                  L2 mixed: "Multi-Head" blue / "Self Attention" red / quotes+block black)
//   banner2        tan callout x109-415 y157-199, fill DECDBB, 2 lines dark red
//   connect_h      (F6 re-measured 2026-10-13: attempt 1 ran banner1-bottom pink +
//                  gray lanes, but the frame is verifiably clean below banner1 — no
//                  printed ink; the founder's drawn arrow runs from BANNER2's right
//                  end to the "h" circle). Now draws ONLY the small tan/red
//                  down-arrowhead on the "h" circle top (present in the frame);
//                  the connector path lives in connect_tan (extends banner2's
//                  printed pink curve (417,182)->(443,232 fade) down to the "h"
//                  circle per the founder's F6 arrow)
//   inset_sdpa_*   Figure-2-left inset: green frame x59-189 y269-491 + corner
//                  handles + red italic 2-line title + q/k/v circles, MatMul x2,
//                  Scale, Mask (opt.), SoftMax, black arrows, V bypass up the right
//   inset_mha_*    Figure-2-right inset: green frame x300-508 y246-515 + handles +
//                  red italic title + Linear/Concat/SDPA-stack/3xLinear/v-k-q +
//                  offset gray shadow copies + red rectangle (x303-475 y354-396)
//                  drawn around the mauve SDPA box
//   h_annot        "h" in a small tan-ringed circle at (494,367), black curved line
//                  from the red rectangle to it, red down-arrowhead on top
//   dash_d1/d2/d3/d4  thin red DASHED connectors (RE-MEASURED 2026-10-13 from the
//                  founder's F6 evidence, qa/slide018/arrow/ — the two ">" chevrons
//                  he traced mark the TRUE pairs): d1 inset-B top-right corner
//                  (508,250) -> enc MHA box top-left corner (644,349); d4 NEW:
//                  inset-B bottom-right (509,506) -> enc MHA box bottom-left edge
//                  (638,387) [was MISSING in attempt 1]; d2 inset-A top-right
//                  (191,275) -> red rect left edge (299,368); d3 inset-A bottom-right
//                  (191,484) -> red rect left-bottom edge (297,394) [attempt 1 drew
//                  only a fading stub to (238,433) — the frame shows the full stroke]
//   dec_wrapper    green outer wrapper around the WHOLE decoder stack (olive +
//                  purple containers), frame-measured x744-843 y199-411, stroke
//                  #3E7150 — founder F6 "box" hint (olive highlight + handwritten
//                  "box" + blue arrow on the evidence). Missing from parent 17's
//                  component; drawn here as 18's own delta (see
//                  scratch/slide018/CHILD_DELTA.md for the cascade)
//   enc_mha_box    SOLID red outline x650-722 y355-387, salmon fill C87E57, drawn
//                  over the parent's encoder MHA compartment
//   dec_mha_box    DASHED red outline x748-821 y277-310, fill B28659; first covers
//                  the parent's protruding glyph tops with an olive patch (redrawing
//                  the two faint interior verticals), drawn over the compartment
//   fig_handles    small green squares at the corners of the right architecture
//                  frame (present in the frame; parent 17 omitted them — delta here)
//
// BANK CONTRACT (founder directive 2026-10-11): child 19 composes on THIS module and
// replaces the banner blocks (banner1, banner2, connect_h) with its normalization /
// feed-forward / residual callouts and adds green residual arrows. It should skip
// { banner1, banner2, connect_h, connect_tan } and keep the inset_*, dash_*, *_mha_box, and
// fig_handles blocks. opts.skip / opts.only select delta blocks; opts.chrome=false
// suppresses the house chrome (drawn once here via components/house_chrome.js).

const parent = require("./slide_017.js");
const { drawHouseChrome } = require("./house_chrome.js");

const px = parent.px;

// ---- slide-018 palette (JPEG-core measured, scratch/slide018/m20_scan.py) -------
const C = {
  red: "C00000",
  banner1Fill: "F2C699",     // (242,198,153)
  banner1Border: "C00000",   // red border per cmp_banner_1 (original shows red box borders)
  banner2Fill: "DECDBB",     // (222,205,187)
  banner2Border: "C00000",   // red border per cmp_banner_1
  darkRed: "943634",         // banner2 base text (orange-brown family)
  pinkConn: "C47070",        // thin pink/red curved banner connectors (cmp_banner_1)
  tanArrow: "653716",        // faint tan arrowhead into the "h" circle (measured (101,55,22))
  blue: "00008B",            // "Multi-Head" run (parent calloutBlue)
  ink: "000000",
  grayLine: "A6A6A6",        // faint connector
  frameGreen: "1B723F",      // inset frame border core (29,113,63)
  lavender: "C0B9DA",        // MatMul boxes (192,185,218)
  paleYellow: "FCFBC5",      // Scale (252,251,197)
  rose: "EEC3D7",            // Mask (opt.) (238,195,215)
  paleGreen: "C8E9CE",       // SoftMax (200,233,206)
  concatYellow: "F8FBC6",    // Concat (248,251,198)
  linearFill: "E9EDEA",      // Linear boxes (231,237,233)
  shadowFill: "E4E4E4",      // offset gray copies
  shadowBorder: "ABABAB",
  mauve: "BB93AE",           // SDPA box (187,147,174)
  circleBlue: "0000A1",      // inset v/k circles (0,0,161)
  circleRed: "990000",       // inset q circles (153,0,0)
  boxBorder: "404040",
  linearBorder: "808080",
  hRing: "B89070",           // "h" circle ring (212,188,160)/(184,156,132)
  mhaText: "8C4423",         // MHA box text (140,68,35)
  salmon: "C87E57",          // encoder MHA box fill (200,126,87)
  tanBrown: "B28659",        // decoder MHA box fill (178,134,89)
  olive: "B0B070",           // parent decoder-stack fill (for the cover patch)
  wrapGreen: "3E7150",       // decoder outer wrapper stroke (F6 modal (62,113,80))
  spine: "2F2F2F",
  black: "333333",
};
const SANS = "Arial";

// ---- helpers --------------------------------------------------------------------

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

function letterCircle(slide, cx, cy, d, fill, letter, fontSize) {
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

function flowBox(slide, x, y, w, h, fill, border, borderColor, lines, fontSize, lineSpacing) {
  slide.addShape("rect", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: borderColor, width: border },
  });
  const items = lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } }));
  slide.addText(items, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize, bold: true, color: C.black,
    lineSpacing,
  });
}

function cornerHandle(slide, cx, cy) {
  slide.addShape("rect", {
    x: px(cx - 3), y: px(cy - 3), w: px(6), h: px(6),
    fill: { color: C.frameGreen }, line: { color: C.frameGreen, width: 0.25 },
  });
}

// ---- delta blocks (z-order = call order in renderBase) --------------------------

function drawBanner1(pptx, slide) {
  slide.addShape("rect", {
    x: px(71), y: px(104), w: px(417), h: px(42),
    fill: { color: C.banner1Fill }, line: { color: C.banner1Border, width: 1.25 },
  });
  slide.addText(
    [
      { text: "Both Encoder and Decoder Blocks Contain", options: { color: C.ink, breakLine: true } },
      { text: "\u201C", options: { color: C.ink } },
      { text: "Multi-Head", options: { color: C.blue } },
      { text: " ", options: { color: C.ink } },
      { text: "Self Attention", options: { color: C.red } },
      { text: "\u201D block", options: { color: C.ink } },
    ],
    {
      x: px(71), y: px(104), w: px(417), h: px(42),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 16, bold: true, lineSpacing: 20,
    }
  );
}

function drawBanner2(pptx, slide) {
  slide.addShape("rect", {
    x: px(109), y: px(157), w: px(306), h: px(42),
    fill: { color: C.banner2Fill }, line: { color: C.banner2Border, width: 1 },
  });
  slide.addText(
    [
      { text: "\u201Ch\u201D", options: { color: C.red } },
      { text: " Heads", options: { color: C.darkRed, breakLine: true } },
      { text: "Outputs of Heads are ", options: { color: C.darkRed } },
      { text: "concatenated", options: { color: C.red } },
    ],
    {
      x: px(109), y: px(157), w: px(306), h: px(42),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 15, bold: true, lineSpacing: 21,
    }
  );
}

function drawConnectH(pptx, slide) {
  // F6: the banner1-bottom pink lane + gray middle lane measured as FABRICATED
  // (frame clean below banner1 — see scratch/slide018/RESUME.md). Only the small
  // tan down-arrowhead on the "h" circle survives (measured (101,55,22)).
  slide.addShape("triangle", {
    x: px(489.5), y: px(347), w: px(7), h: px(8), flipV: true,
    fill: { color: C.tanArrow }, line: { color: C.tanArrow, width: 0.5 },
  });
}

function drawConnectTan(pptx, slide) {
  // thin pink/red curved connector from the tan ("h Heads") banner's right end,
  // CONTINUED down to the "h" circle per the founder's F6 drawn arrow (the frame
  // prints the start of this curve (417,182)->(~443,232) before video-compression
  // fades; the founder's annotation completes it onto the "h" circle top, where
  // the frame carries the tan arrowhead). Same pink family as measured (255,191,194
  // JPEG-core at (439,223)).
  addLines(slide, C.pinkConn, 0.75, [
    [417, 182], [445, 212], [470, 238], [481, 296], [491, 348.5],
  ]);
}

function drawInsetSdpaTitle(pptx, slide) {
  slide.addText(
    [
      { text: "Scaled Dot-Product", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(54), y: px(227), w: px(148), h: px(40),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 15, bold: true, italic: true, color: C.red,
      lineSpacing: 18,
    }
  );
}

function drawInsetSdpaFrame(pptx, slide) {
  slide.addShape("rect", {
    x: px(59), y: px(269), w: px(130), h: px(222),
    fill: { type: "none" }, line: { color: C.frameGreen, width: 2.25 },
  });
  cornerHandle(slide, 59, 269);
  cornerHandle(slide, 189, 269);
  cornerHandle(slide, 59, 491);
  cornerHandle(slide, 189, 491);
}

function drawInsetSdpaFlow(pptx, slide) {
  // circles (bottom, straddling the frame's lower border) — lowercase per the raw
  letterCircle(slide, 91.5, 473.5, 15, C.circleRed, "Q", 7.5);
  letterCircle(slide, 128, 473, 17, C.circleBlue, "K", 7.5);
  letterCircle(slide, 166.5, 473, 18, C.circleBlue, "V", 7.5);
  // chain boxes bottom-up
  flowBox(slide, 76, 429, 88, 16, C.lavender, 0.75, C.boxBorder, ["MatMul"], 8, 10);
  flowBox(slide, 93, 397, 38, 12, C.paleYellow, 0.75, C.boxBorder, ["Scale"], 7, 9);
  flowBox(slide, 77, 363, 69, 14, C.rose, 0.75, C.boxBorder, ["Mask (opt.)"], 7, 9);
  flowBox(slide, 80, 330, 62, 15, C.paleGreen, 0.75, C.boxBorder, ["SoftMax"], 7, 9);
  flowBox(slide, 105, 294, 68, 18, C.lavender, 0.75, C.boxBorder, ["MatMul"], 8, 10);
  // arrows (flow runs bottom-up)
  addLines(slide, C.black, 0.75, [[91.5, 466], [91.5, 446]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[128, 464], [128, 446]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[112, 429], [112, 410]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[112, 397], [112, 378]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[112, 363], [112, 346]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[112, 330], [112, 313]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[139, 294], [139, 271]], { endArrow: true });
  // v bypass: long line up the right side into the top MatMul
  addLines(slide, C.black, 0.75, [[166.5, 464], [166.5, 313]], { endArrow: true });
}

function drawInsetMhaTitle(pptx, slide) {
  slide.addText("Multi-Head Attention", {
    x: px(294), y: px(210), w: px(200), h: px(24),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 15, bold: true, italic: true, color: C.red,
  });
}

function drawInsetMhaFrame(pptx, slide) {
  slide.addShape("rect", {
    x: px(300), y: px(246), w: px(208), h: px(269),
    fill: { type: "none" }, line: { color: C.frameGreen, width: 2.25 },
  });
  cornerHandle(slide, 300, 246);
  cornerHandle(slide, 508, 246);
  cornerHandle(slide, 300, 515);
  cornerHandle(slide, 508, 515);
}

function drawInsetMhaFlow(pptx, slide) {
  // shadow copies (gray, offset up-right) behind the top Linear
  slide.addShape("rect", {
    x: px(372), y: px(259), w: px(47), h: px(23),
    fill: { color: C.shadowFill }, line: { color: C.shadowBorder, width: 0.75 },
  });
  flowBox(slide, 364, 266, 47, 23, C.linearFill, 0.75, C.linearBorder, ["Linear"], 8, 10);
  addLines(slide, C.black, 0.75, [[387, 266], [387, 250]], { endArrow: true });
  // Concat
  flowBox(slide, 364, 312, 46, 14, C.concatYellow, 0.5, C.boxBorder, ["Concat"], 7.5, 9);
  addLines(slide, C.black, 0.75, [[387, 312], [387, 290]], { endArrow: true });
  addLines(slide, "8A8A8A", 0.75, [[379, 312], [379, 292]], { endArrow: true });
  addLines(slide, "8A8A8A", 0.75, [[395, 312], [395, 292]], { endArrow: true });
  // SDPA stack: gray copy behind, then red rectangle, then the mauve box
  slide.addShape("rect", {
    x: px(317), y: px(343), w: px(161), h: px(32),
    fill: { color: C.shadowFill }, line: { color: C.shadowBorder, width: 0.75 },
  });
  slide.addShape("rect", {
    x: px(303), y: px(354), w: px(172), h: px(42),
    fill: { type: "none" }, line: { color: C.red, width: 1.5 },
  });
  flowBox(slide, 309, 360, 161, 32, C.mauve, 0, C.mauve,
    ["Scaled Dot-Product", "Attention"], 8, 11);
  // three parallel Linear boxes with their own shadow copies
  const LX = [[309, 42], [359, 48], [416, 48]];
  for (const [bx, bw] of LX) {
    slide.addShape("rect", {
      x: px(bx + 7), y: px(397), w: px(bw), h: px(18),
      fill: { color: C.shadowFill }, line: { color: C.shadowBorder, width: 0.75 },
    });
    flowBox(slide, bx, 403, bw, 18, C.linearFill, 0.75, C.linearBorder, ["Linear"], 7.5, 9);
    addLines(slide, C.black, 0.75, [[bx + bw / 2, 403], [bx + bw / 2, 397]], { endArrow: true });
    addLines(slide, "8A8A8A", 0.75, [[bx + bw / 2 - 6, 403], [bx + bw / 2 - 6, 398]], { endArrow: true });
    addLines(slide, "8A8A8A", 0.75, [[bx + bw / 2 + 6, 403], [bx + bw / 2 + 6, 398]], { endArrow: true });
  }
  // circles (bottom, straddling the frame's lower border) — lowercase per the raw
  letterCircle(slide, 330, 498, 18, C.circleBlue, "V", 7.5);
  letterCircle(slide, 387.5, 498, 18, C.circleBlue, "K", 7.5);
  letterCircle(slide, 445, 498.5, 16, C.circleRed, "Q", 7.5);
  // arrows circles -> Linear boxes
  addLines(slide, C.black, 0.75, [[330, 489], [330, 422]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[387.5, 489], [387.5, 422]], { endArrow: true });
  addLines(slide, C.black, 0.75, [[445, 490], [445, 422]], { endArrow: true });
}

function drawHAnnot(pptx, slide) {
  // black curved line from the red rectangle to the "h" circle
  addLines(slide, C.black, 0.75, [[477, 389], [480, 381], [483, 374], [486, 368]]);
  // gray ghost circle offset behind the "h" circle
  slide.addShape("ellipse", {
    x: px(488.5), y: px(353.5), w: px(19), h: px(19),
    fill: { type: "none" }, line: { color: C.grayLine, width: 0.75 },
  });
  // "h" in a small tan-filled circle (cmp_mhainset_1: tan/beige with ghost behind)
  slide.addShape("ellipse", {
    x: px(484.5), y: px(357.5), w: px(19), h: px(19),
    fill: { color: "D4BCA0" }, line: { color: "8A6A48", width: 1 },
  });
  slide.addText("h", {
    x: px(484.5), y: px(357.5), w: px(19), h: px(19),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 10, bold: true, italic: true, color: C.black,
  });
}

function drawDashD1(pptx, slide) {
  // red dashed connector: MHA inset top-right corner -> encoder MHA box TOP-LEFT
  // corner (F6 re-measure: the frame's dashes form ONE straight diagonal
  // (508,250)->(644,349), not a bent polyline ending mid-edge)
  // tip lands ON the drawn enc_mha_box outline's top-left corner (build box is
  // x650-722; the frame's box reads x634-723 with fill from ~x650 — contact must
  // be against the DRAWN outline)
  addLines(slide, C.red, 1, [[508, 250], [651, 356.5]], { dash: "sysDash" });
}

function drawDashD4(pptx, slide) {
  // red dashed connector (MISSING in attempt 1 — founder F6 right ">" chevron has
  // TWO arms): MHA inset bottom-right corner -> enc MHA box bottom-left edge
  addLines(slide, C.red, 1, [[509, 506], [651, 386.5]], { dash: "sysDash" });
}

function drawDashD2(pptx, slide) {
  // red dashed connector: SDPA inset top-right -> red rectangle's LEFT EDGE in the
  // MHA inset (F6 re-measure: straight diagonal (191,275)->(299,368) hitting the
  // rect edge at y368 within rect y354-396)
  addLines(slide, C.red, 1, [[191, 275], [301, 369]], { dash: "sysDash" });
}

function drawDashD3(pptx, slide) {
  // red dashed connector: SDPA inset bottom-right -> red rectangle's left-bottom
  // edge (F6 re-measure: the frame shows the FULL diagonal (191,484)->(297,394);
  // attempt 1's fading stub to (238,433) was the defect the founder circled)
  addLines(slide, C.red, 1, [[191, 484], [300, 394.5]], { dash: "sysDash" });
}

function drawDecWrapper(pptx, slide) {
  // F6 "box": the course figure draws ONE green outer wrapper around the ENTIRE
  // decoder layer stack (olive A&N/FF/A&N/MHA container + purple masked-MHA
  // container). Frame-measured edges: left x744-746, right x840-842, top y199-202,
  // bottom y408-411; stroke modal #3E7150. Missing from parent slide_017.js —
  // drawn here as 18's own delta (cascade: scratch/slide018/CHILD_DELTA.md).
  slide.addShape("roundRect", {
    x: px(744), y: px(199), w: px(99), h: px(212), rectRadius: 0.04,
    fill: { type: "none" }, line: { color: C.wrapGreen, width: 1.25 },
  });
}

function drawEncMhaBox(pptx, slide) {
  // SOLID red outline + salmon fill over the parent's encoder MHA compartment
  slide.addShape("roundRect", {
    x: px(650), y: px(355), w: px(72), h: px(32), rectRadius: 0.04,
    fill: { color: C.salmon }, line: { color: C.red, width: 1.5 },
  });
  slide.addText(
    [
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(650), y: px(355), w: px(72), h: px(32),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 9, bold: true, color: C.mhaText, lineSpacing: 10.5,
    }
  );
}

function drawDecMhaBox(pptx, slide) {
  // cover the parent's protruding glyph tops with the stack's own olive fill,
  // then redraw the two faint interior verticals the patch crosses
  slide.addShape("rect", {
    x: px(747), y: px(265), w: px(92), h: px(13),
    fill: { color: C.olive }, line: { color: C.olive, width: 0.25 },
  });
  addLines(slide, "4A4A4A", 0.5, [[753.5, 265], [753.5, 278]]);
  addLines(slide, "4A4A4A", 0.5, [[818.5, 265], [818.5, 278]]);
  // DASHED red outline + tan-brown fill over the compartment
  slide.addShape("roundRect", {
    x: px(748), y: px(277), w: px(73), h: px(33), rectRadius: 0.04,
    fill: { color: C.tanBrown }, line: { color: C.red, width: 1.25, dashType: "dash" },
  });
  slide.addText(
    [
      { text: "Multi-Head", options: { breakLine: true } },
      { text: "Attention", options: {} },
    ],
    {
      x: px(748), y: px(277), w: px(73), h: px(33),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 8.5, bold: true, color: C.mhaText, lineSpacing: 10,
    }
  );
}

function drawFigHandles(pptx, slide) {
  cornerHandle(slide, 572, 103);
  cornerHandle(slide, 896, 103);
  cornerHandle(slide, 572, 526);
  cornerHandle(slide, 896, 526);
}

// ---- composition ----------------------------------------------------------------

const PARENT_SKIP = [
  "callout1", "callout2", "callout3", "callout4",
  "leader1", "leader2", "leader3", "leader4",
];

const DELTA_BLOCKS = {
  banner1: drawBanner1,
  banner2: drawBanner2,
  inset_sdpa_title: drawInsetSdpaTitle,
  inset_sdpa_frame: drawInsetSdpaFrame,
  inset_sdpa_flow: drawInsetSdpaFlow,
  inset_mha_title: drawInsetMhaTitle,
  inset_mha_frame: drawInsetMhaFrame,
  inset_mha_flow: drawInsetMhaFlow,
  h_annot: drawHAnnot,
  dash_d1: drawDashD1,
  dash_d2: drawDashD2,
  dash_d3: drawDashD3,
  dash_d4: drawDashD4,
  dec_wrapper: drawDecWrapper,
  enc_mha_box: drawEncMhaBox,
  dec_mha_box: drawDecMhaBox,
  connect_h: drawConnectH,
  connect_tan: drawConnectTan,
  fig_handles: drawFigHandles,
};

/**
 * Draw the full slide-018 composition: house chrome + slide 17's certified base
 * (minus its callout column) + slide 18's delta, selectively.
 * @param {object} pptx  pptxgenjs instance
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[delta names], only:[delta names], chrome:bool, numeral }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 18 : opts.numeral });
  }
  parent.renderBase(pptx, slide, { chrome: false, skip: PARENT_SKIP });
  for (const [name, fn] of Object.entries(DELTA_BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, DELTA_BLOCKS, PARENT_SKIP, C, px };
