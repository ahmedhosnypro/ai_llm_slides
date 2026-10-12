// build/slide_037.js — 002_transformers_part2 slide 037 "Transformer Blocks (stacked
// over Multi-Head)" (Deep Learning DSAI 308, video 002).
//
// CROSS-VIDEO CHILD LAW (founder directive 2026-10-11): composition = lecture 001
// slide 19's CERTIFIED component, imported by ABSOLUTE PATH — never re-derived:
//   /home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/
//     recreated_pptx/build/components/slide_019.js
// (certified 2026-10-12, judge PASS render_4; 002:19 — the in-video sibling child of
// the same parent — certified PASS with the same import pattern, qa/slide019/).
//
// FRAME->SLIDE MAPPING (previous worker's m0 fit, scratch/slide037/m0_fit_mapping.py):
// video 002's capture zoomed out ~0.96 with a letterbox strip below; fitted from the
// four chrome landmarks: slide_pt = (fx-17.101)/0.962329 , (fy+0.224)/0.96053.
// All delta geometry below is PIL-measured in slide pt (m21_delta_pil.py, fine
// darkness/red maps, scanlines, + m18 funnel bands + vision probe P1 of the pin).
//
// PIL DELTA vs the imported composition (my frame is ground truth):
//   REMOVED (present in 001:19, absent here):
//     legend1/2/3 + leader1..5   the three color-callout boxes + hairlines
//                                (panel-gray in my frame — same finding as 002:19)
//     title                      017's centered title; mine is top-LEFT (measured ink
//                                x94.5-864.5, y59.6-92.9, single line, ~34pt bold red)
//     019 encoder repaints       enc_repaint/enc_addn_top/enc_ff/enc_addn_bot/
//                                enc_green/enc_vcircle — THIS frame re-renders the
//                                encoder sub-stack in the warm Alammar style (measured
//                                columns bx=663..715: gray box y277-291, brown FF box
//                                y292-318, tan gap y319-341, gray box y342-353, salmon
//                                MHA y355-390; contrast 002:19's frame which matches the
//                                parent's steel/gray — measured side-by-side)
//     navy chevrons zone-1/2     absent (as in 002:19); zone-3 present -> redrawn
//     enc_pe / dec_pe icons      the plus-in-circle + sine-circle pairs are replaced by
//                                CLOCK icons (ring + hands; decoder clock measured ring
//                                d~29 at (795-824, 420-442), hands left+down; encoder
//                                clock ring d~24 at (651-676, 418-441))
//   ADDED:
//     title        "Transformer Blocks (stacked over Multi-Head)" top-left, 34pt bold
//     dashed box   red dashed rounded rect x621-741, y250-384 around the encoder stack
//                  (measured edges: left x621 sy271-347, right x736-742 sy264-360, top
//                  y248-252, bottom y370-379; vision P1 + transcript-of-record confirm)
//     pin          red map-pin, head d~71.5 center (631.5,209), right edge of the tail
//                  ~vertical at x660-662, tip (659,267); white bold 3-line text
//                  'WE'/'ARE'/'HERE' tilted (same certified design as 002:19's pin,
//                  translated to THIS frame's measured position)
//     disc         solid red disc d~23 center (683.5,344) over the encoder's lower
//                  'Add & Norm' box (hides its label — vision P1 + transcript)
//     funnel       dash_d3 extended (left inset bottom corner -> (280,385)) + new
//                  dashed line (center inset bottom-right corner (512,492) -> encoder
//                  MHA box (640,372)) — both measured sparse-dash diagonals
//   KEPT (measured present at the inherited geometry):
//     yellow_band  the L-shaped yellow cross-attention highlight IS in this frame
//                  (measured yellow bbox (676,251)-(786,324) == parent's band) — the
//                  dispatch's "remove yellow box" was measured WRONG and is overridden
//     everything else of the 017+018+019 chain (decoder interior diffs are drift-only)
//
// Laws honored: certified component imported (require by absolute path, numeral 37);
// verbatim text; margin:0 + explicit fontFace; explicit lineSpacing on multi-line text;
// no '#' in hex; PIL-measured geometry; single-version deliverable
// ../slide_037_recreated.pptx; house chrome drawn ONCE by the parent chain.

const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_019.js");
const pptxgen = require("pptxgenjs");

const px = PARENT.px; // build pt -> inches (1px = 1pt = 1/72 in)

// ---- measured delta palette (JPEG-core) -----------------------------------------
const C = {
  pinRed: "C00000",
  discRed: "DC1A20",        // disc core (219,23,25)
  boxBorder: "3F3F3F",
  grayBox: "857F73",        // A&N boxes (133,127,115)
  brownBox: "997343",       // FF box (153,115,66)
  ffText: "2E2318",
  anText: "3A3630",
  container: "C8965A",      // this frame's warm container tan (200,150,90)
  busOlive: "C3B744",       // upper residual line (195,183,68)
  busGreen: "81C124",       // lower bus + pickup (129,193,36)
  dashRed: "B01515",        // dashed rounded box (JPEG-darkened C00000)
  clockRing: "2E2E2E",
  white: "FFFFFF",
  greenBright: "8CC62E",    // dec trunk/connector core (parent value, kept verbatim)
  navy: "05008F",           // zone-3 chevrons (parent value, kept verbatim)
};
const SANS = "Arial";

// ---- block: warm repaint of the encoder sub-stack interior -----------------------
// Patch (container color) over 017's interior (its A&N texts, olive FF inset, residual
// curves, sub-arrows), then this frame's own boxes. Stops above the salmon MHA box
// (018's block, y355-387, drawn earlier by renderBase and kept untouched).
function drawEncInterior(pptx, slide) {
  const rect = (x, y, w, h, fill, border, bw) => slide.addShape("rect", {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: border, width: bw },
  });
  const centerText = (x, y, w, h, lines, fontSize, color, lineSpacing) => {
    const items = lines.map((t, i) => ({ text: t, options: { breakLine: i < lines.length - 1 } }));
    slide.addText(items, {
      x: px(x), y: px(y), w: px(w), h: px(h),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize, bold: true, color, lineSpacing,
    });
  };
  // interior patch (inside the container border x628-728 y267-409; stop at the MHA box)
  rect(630.5, 269.5, 95, 84.5, C.container, C.container, 0.25);
  // A&N #1: gray box y277-291 (text measured at sy280-283)
  rect(653, 277, 69, 14.5, C.grayBox, C.boxBorder, 0.75);
  centerText(653, 277, 69, 14.5, ["Add & Norm"], 7.5, C.anText, 9);
  // Feed Forward: brown box y292-318 (2 text lines at sy296-301 / sy308-310)
  rect(654, 292, 59, 26.5, C.brownBox, C.boxBorder, 0.75);
  centerText(654, 292, 59, 26.5, ["Feed", "Forward"], 8, C.ffText, 10);
  // A&N #2: gray box y342-353 (label hidden under the disc in the original)
  rect(653, 342, 69, 11.5, C.grayBox, C.boxBorder, 0.75);
  centerText(653, 342, 69, 11.5, ["Add & Norm"], 7, C.anText, 8.5);
  // residual bus: olive vertical x634 (sy281-355) + green vertical x630 (sy356-405)
  // + green pickup y403.5 x628-688 (measured)
  const line = (color, width, pts) => {
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, y0] = pts[i];
      const [x1, y1] = pts[i + 1];
      slide.addShape("line", {
        x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
        w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
        flipV: y1 < y0, flipH: x1 < x0,
        line: { color, width },
      });
    }
  };
  line(C.busOlive, 2.5, [[634.5, 281], [634.5, 355]]);
  line(C.busGreen, 3.5, [[630, 356], [630, 405]]);
  line(C.busGreen, 4, [[628, 403.5], [688, 403.5]]);
}

// ---- block: red dashed rounded box around the encoder stack ----------------------
function drawDashBox(pptx, slide) {
  slide.addShape("roundRect", {
    x: px(621), y: px(250), w: px(120), h: px(134), rectRadius: 0.08,
    fill: { type: "none" },
    line: { color: C.dashRed, width: 1.25, dashType: "dash" },
  });
}

// ---- block: WE ARE HERE map-pin (002:19's certified design, translated) ----------
// Head circle d71.4 center (631.5,209); tail wedge, right edge ~vertical, tip (659,267);
// transition bulges; 3 tilted white lines. Geometry = 002:19's measured pin shifted by
// (+64.1, -160.6) with the tail shortened 44.9 -> 36 (measured tip).
function drawPin(pptx, slide) {
  const red = { color: C.pinRed };
  slide.addShape("ellipse", {
    x: px(595.8), y: px(173.3), w: px(71.4), h: px(71.4),
    fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  slide.addShape("triangle", {
    x: px(636.9), y: px(231.05), w: px(29.25), h: px(36),
    flipV: true, rotate: 340, fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  slide.addShape("ellipse", {
    x: px(621.1), y: px(241.4), w: px(22), h: px(12),
    rotate: 342, fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  slide.addShape("ellipse", {
    x: px(628.1), y: px(244.9), w: px(16), h: px(11),
    rotate: 342, fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  slide.addText([
    { text: "WE", options: { breakLine: true } },
    { text: "ARE", options: { breakLine: true } },
    { text: "HERE", options: {} },
  ], {
    x: px(601.6), y: px(182.4), w: px(60), h: px(55),
    align: "center", valign: "middle", margin: 0, rotate: 342,
    fontFace: SANS, fontSize: 12.5, bold: true, color: C.white,
    lineSpacing: 17,
  });
}

// ---- block: solid red disc over the encoder's lower Add & Norm -------------------
function drawDisc(pptx, slide) {
  slide.addShape("ellipse", {
    x: px(672), y: px(331.5), w: px(23.5), h: px(23.5),
    fill: { color: C.discRed }, line: { color: C.discRed, width: 0.5 },
  });
}

// ---- block: funnel lines (d3 extension + new inset-bottom diagonal) --------------
function drawFunnel(pptx, slide) {
  const dash = (pts) => {
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, y0] = pts[i];
      const [x1, y1] = pts[i + 1];
      slide.addShape("line", {
        x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
        w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
        flipV: y1 < y0, flipH: x1 < x0,
        line: { color: C.dashRed, width: 1, dashType: "dash" },
      });
    }
  };
  // d3 extended: left inset bottom-right corner -> (280,385) (measured trace)
  dash([[193, 487], [280, 385]]);
  // new: center inset bottom-right corner -> encoder MHA box (measured trace)
  dash([[512, 492], [640, 372]]);
}

// ---- block: PE nodes with CLOCK icons (replace 017's plus/sine icons) ------------
function drawClock(pptx, slide, cx, cy, d) {
  slide.addShape("ellipse", {
    x: px(cx - d / 2), y: px(cy - d / 2), w: px(d), h: px(d),
    fill: { color: C.white }, line: { color: C.clockRing, width: 1.5 },
  });
  // hands: minute to 9 o'clock (left), hour to 6 o'clock (down) — decoder-measured
  slide.addShape("line", {
    x: px(cx - d / 2 + 2), y: px(cy), w: px(d / 2 - 2), h: 0,
    line: { color: C.clockRing, width: 1.75 },
  });
  slide.addShape("line", {
    x: px(cx), y: px(cy), w: 0, h: px(d / 2 - 2),
    line: { color: C.clockRing, width: 1.75 },
  });
}

function drawEncPe(pptx, slide) {
  // node box (017's certified geometry, fill measured equal B08058)
  slide.addShape("roundRect", {
    x: px(649), y: px(415.5), w: px(79), h: px(30), rectRadius: 0.05,
    fill: { color: "B08058" }, line: { color: "6E4423", width: 1 },
  });
  drawClock(pptx, slide, 663.5, 430, 24);
  // bare sine squiggle right of the clock (measured x681-702, y425-441)
  const x0 = 681, w = 21, h = 13, cy = 433;
  for (let i = 0; i < 4; i++) {
    const xa = x0 + (w / 4) * i;
    const xb = x0 + (w / 4) * (i + 1);
    slide.addShape("line", {
      x: px(Math.min(xa, xb)), y: px(i % 2 === 0 ? cy - h / 2 : cy),
      w: px(w / 4), h: px(h / 2), flipV: i % 2 === 0,
      line: { color: "6E4423", width: 1 },
    });
  }
  slide.addText([
    { text: "Positional", options: { breakLine: true } },
    { text: "Encoding", options: {} },
  ], {
    x: px(594), y: px(416), w: px(56), h: px(28),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9.5, bold: true, color: "404040", lineSpacing: 12,
  });
}

function drawDecPe(pptx, slide) {
  drawClock(pptx, slide, 809.9, 431.2, 29);
  slide.addText([
    { text: "Positional", options: { breakLine: true } },
    { text: "Encoding", options: {} },
  ], {
    x: px(836), y: px(419), w: px(48), h: px(28),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 9.5, bold: true, color: "333333", lineSpacing: 12,
  });
}

// ---- block: decoder green routing without the zone-1/2 chevron pairs -------------
// (verbatim from 002:19's certified drawDecGreenChild — this frame shows the same
// trunk + six connectors + zone-3 chevron pair only)
function drawDecGreenChild(pptx, slide) {
  const line = (color, width, pts) => {
    for (let i = 0; i < pts.length - 1; i++) {
      const [x0, y0] = pts[i];
      const [x1, y1] = pts[i + 1];
      slide.addShape("line", {
        x: px(Math.min(x0, x1)), y: px(Math.min(y0, y1)),
        w: px(Math.abs(x1 - x0)), h: px(Math.abs(y1 - y0)),
        flipV: y1 < y0, flipH: x1 < x0,
        line: { color, width },
      });
    }
  };
  const chevronUp = (cx, cy, color, w = 6, h = 4.5) => {
    slide.addShape("triangle", {
      x: px(cx - w / 2), y: px(cy - h / 2), w: px(w), h: px(h),
      fill: { color }, line: { color, width: 0.5 },
    });
  };
  line(C.greenBright, 4, [[834, 210], [834, 404]]);
  line(C.greenBright, 3, [[820, 212], [834, 212]]);
  line(C.greenBright, 3.5, [[789, 258], [835, 258]]);
  line(C.greenBright, 3, [[819, 272], [834, 272]]);
  line(C.greenBright, 3.5, [[788, 320], [835, 320]]);
  line(C.greenBright, 3, [[819, 338], [834, 338]]);
  line(C.greenBright, 3.5, [[791, 402], [835, 402]]);
  chevronUp(772, 313, C.navy);
  chevronUp(772, 318, C.navy);
}

// ---- block: decoder inter-box arrow shafts (verbatim from 002:19) -----------------
function drawGapShafts(pptx, slide) {
  const seg = (y0, y1) => slide.addShape("line", {
    x: px(784.7), y: px(y0), w: 0, h: px(y1 - y0),
    line: { color: "2F2F2F", width: 1.75 },
  });
  seg(193.6, 206.4);
  seg(250.5, 263.5);
}

// ---- block: top-left title --------------------------------------------------------
function drawTitle(pptx, slide) {
  slide.addText("Transformer Blocks (stacked over Multi-Head)", {
    x: px(96), y: px(50), w: px(800), h: px(50),
    align: "left", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 35.5, bold: true, color: "C00000",
  });
}

// ---- composition ----------------------------------------------------------------
//
// SKIP-CHAIN LAW (attempt-1 judge finding, judge_attempt_1.txt CRITICAL: the render
// showed 017's "Encoder – Decoder Transformer" title superimposed on this slide's
// title — a PARENT.renderBase(opts.skip) call does NOT propagate skips down the
// 019->018->017 chain; each level forwards only its own PARENT_SKIP). Fix: compose the
// certified chain from the components' EXPORTED per-block functions in certified
// z-order (chrome -> 017 blocks -> 018 delta blocks -> 019 delta blocks), skipping
// selectively at the level that owns each block. No geometry is re-derived — every
// drawn block is the certified component's own function.
const BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components";
const C017 = require(BASE + "/slide_017.js");
const C018 = require(BASE + "/slide_018.js");
const C019 = require(BASE + "/slide_019.js");
const { drawHouseChrome } = require(BASE + "/house_chrome.js");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();

// 1. house chrome ONCE (playlist primitive), numeral = THIS frame's printed number
drawHouseChrome(pres, s, { numeral: 37 });

// 2. slide-017 certified blocks, minus 018's certified PARENT_SKIP (the left callout
//    column 018 replaces) and this slide's measured removals:
//    title (retitle), enc_pe/dec_pe (clock icons replace the plus/sine pairs).
//    yellow_band KEPT (measured present in this frame).
const SKIP_017 = [...C018.PARENT_SKIP, "title", "enc_pe", "dec_pe"];
for (const [name, fn] of Object.entries(C017.BLOCKS)) {
  if (SKIP_017.includes(name)) continue;
  fn(pres, s);
}

// 3. slide-018 certified delta blocks, minus 019's certified PARENT_SKIP (the banner
//    column 019 replaces) — exactly what 019.renderBase forwards.
for (const [name, fn] of Object.entries(C018.DELTA_BLOCKS)) {
  if (C019.PARENT_SKIP.includes(name)) continue;
  fn(pres, s);
}

// 4. slide-019 certified delta blocks, minus this slide's measured removals:
//    legend callouts + leader hairlines (absent here), 019's encoder repaints (this
//    frame re-renders the encoder sub-stack in its own warm style), dec_green
//    (zone-1/2 chevrons absent; zone-3 redrawn below).
const SKIP_019 = [
  "legend1", "legend2", "legend3",
  "leader1", "leader2", "leader3", "leader4", "leader5",
  "enc_repaint", "enc_addn_top", "enc_ff", "enc_addn_bot", "enc_green", "enc_vcircle",
  "dec_green",
];
for (const [name, fn] of Object.entries(C019.DELTA_BLOCKS)) {
  if (SKIP_019.includes(name)) continue;
  fn(pres, s);
}

// 5. this slide's delta, in measured z-order
drawGapShafts(pres, s);
drawDecGreenChild(pres, s);
drawEncInterior(pres, s);
drawDashBox(pres, s);
drawFunnel(pres, s);
drawPin(pres, s);
drawDisc(pres, s);
drawEncPe(pres, s);
drawDecPe(pres, s);
drawTitle(pres, s);

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_037_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
