// slide_019.js — 002_transformers_part2 slide 019 "Encoder – Decoder Transformer"
// (Deep Learning DSAI 308, video 002, slide 19 — recap of lecture 001 slide 19).
//
// CONTENT SPEC: analysis/slide_019_final.json (PASS_WITH_FIXES; verbatim labels,
// [?] items preserved). Original frame: unique_slides/slide_019.jpg (960x540).
//
// CROSS-VIDEO CHILD LAW (founder directive 2026-10-11): this slide's composition is
// lecture 001 slide 19's CERTIFIED component, imported — NEVER re-drawn. The parent
// component is required FRESH at build time by ABSOLUTE PATH:
//   /home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/
//     recreated_pptx/build/components/slide_019.js
// (re-banked v2 2026-10-12 01:52, md5 eeda3307335a7f398fe106d3864929cb, 0-pixel-diff
// verified vs 001's certified qa/slide019/render_4.png). Badge numeral 19 = the number
// printed on THIS frame (== parent default, passed explicitly anyway).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide019/m1..m8): video 002's
// capture is zoomed OUT ~0.958 with a letterbox strip below the slide. Fitted from
// this frame's four chrome border landmarks (left 58.3, right 901.4, top 43.3,
// bottom 516.9 frame px) and composed with 001's own frame->build transform
// (001:19 landmarks L38.95 R920.09 T43.10 B538.09 vs certified render 41.76/918.96/
// 44.88/539.52; scratch m7/m8):
//   frame_x = 18.0787 + 0.961084 * build_x ;  frame_y = 0.4700 + 0.957187 * build_y
// Cross-checks: frame badge ring (875.5, 71.0) -> build (892.1, 73.7) vs house badge
// (893, 71) — same ~+2.8pt y residual the certified slide-002 build measured and
// accepted as capture noise; content-masked affine SSD fit (m6) agrees within ~0.5px.
// All delta geometry below is measured in FRAME px and converted to build pt through
// this mapping (scratch m9..m15).
//
// PIL DELTA vs the imported composition (my frame is ground truth; scratch/m9_delta.py,
// m10..m15): panel-diff masked SSD 11 after alignment. Measured delta:
//   REMOVED (present in 001:19, absent here — 100% panel-gray in my frame):
//     legend1/2/3     the three color-callout boxes 'Normalization Layer' /
//                     'Feed Forward Layer' / 'Residual Connections'
//     leader1..5      their hairlines + the two black arrowheads into the encoder /
//                     decoder Feed Forward boxes
//     navy chevrons   drawDecGreen's zone-1 pair (783.5,197/202) and zone-2 pair
//                     (783.5,255.5/259.5) — my frame shows only the inherited thin
//                     dark up-arrow shafts there; the zone-3 pair (772,313/318) IS
//                     present (measured navy) and is redrawn by drawDecGreenChild
//   ADDED:
//     bottom band     translucent yellow rounded band x558.5 y411.5 w352 h84 build pt,
//                     fill FFFF00 ~50% transparency (blend-fit alpha 0.45-0.5 over
//                     mint/peach/dark-tan backgrounds, m13), rounded corners
//                     (~0.1-0.28in; left-edge inset fit), drawn OVER the outer green
//                     frame border (measured: border shows through as yellow-green)
//     pin             red map-pin 'WE ARE HERE': head circle d~71.5 centered
//                     (567.5, 369.5) build pt (chord-fit residuals <2pt, m13), tail
//                     tapering to tip (595.1, 435.2) with its right edge ~vertical at
//                     x595.5 (drawn as two red triangles), white bold 2-line text
//                     'WE ARE' / 'HERE' (block b547..594 x 345..396). Pin sits ON TOP
//                     of the band (tail red visible over band yellow, m13 rows).
//   INHERITED-VARIANCE (documented, no action): 1px dash-phase fragments of 018's
//     dashed zoom lines at build (623..628, 303..309)/(374..380) and the decoder
//     container right-border capture-phase darkness (frame x825: (32,74,38) here vs
//     (79,120,91) in 001's frame — sub-pixel phase blend of the same dark-green line).
//
// Laws honored: composition imported (require by absolute path, numeral passed);
// verbatim text; margin:0 + explicit fontFace on new text; explicit lineSpacing on
// the pin text; no '#' in hex; PIL-measured geometry; single-version deliverable
// ../slide_019_recreated.pptx; house chrome drawn ONCE by the parent chain.

const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/components/slide_019.js");
const pptxgen = require("pptxgenjs");

const px = PARENT.px; // build pt -> inches (1px = 1pt = 1/72 in)

// ---- measured delta palette (JPEG-core, scratch m10/m13) ------------------------
const C = {
  pinRed: "C00000",        // pin core (192,0,0)
  bandYellow: "FFFF00",    // translucent highlighter band
  greenBright: "8CC62E",   // dec trunk/connector core (parent value, kept verbatim)
  navy: "05008F",          // zone-3 chevrons (parent value, kept verbatim)
  white: "FFFFFF",
};

// ---- delta block 1: decoder green routing WITHOUT the zone-1/2 chevron pairs -----
// Geometry copied VERBATIM from the certified parent's drawDecGreen (trunk, six
// horizontal connectors, zone-3 chevron pair at (772,313)/(772,318)) minus the four
// chevrons my frame does not show. The certified component file itself is untouched.
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

// ---- delta block 2: translucent yellow bottom band -------------------------------
function drawBottomBand(pptx, slide) {
  slide.addShape("rect", {
    x: px(561.5), y: px(412.5), w: px(351), h: px(84),
    rectRadius: 0.12,
    fill: { color: C.bandYellow, transparency: 50 },
    line: { color: C.bandYellow, width: 0.25, transparency: 50 },
  });
}

// ---- delta block 3: WE ARE HERE map-pin -----------------------------------------
// Head: circle d71.5 at (531.6..603.1, 333.8..405.3) build pt (chord fit m13).
// Tail: ONE smooth wedge (cropcmp_pin_2 fix: the two-triangle version showed a
// zig-zag kink; single triangle fitted to the measured taper — right edge ~vertical
// at x595.5, apex = measured tip (595.1, 435.2), base corners inside the head circle,
// whole wedge rotated -20 deg with the balloon tilt). Text: THREE tilted lines
// 'WE' / 'ARE' / 'HERE' (cropcmp_pin_2 finding; measured block b547..594 x b345..396).
function drawPin(pptx, slide) {
  const red = { color: C.pinRed };
  slide.addShape("ellipse", {
    x: px(531.8), y: px(333.8), w: px(71.4), h: px(71.4),
    fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  // single tail wedge: apex lands on the measured tip; base hidden in the head
  slide.addShape("triangle", {
    x: px(572.8), y: px(391.65), w: px(29.25), h: px(44.9),
    flipV: true, rotate: 340, fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  // bulb->tail transition bulge (selfcheck_attempt_3: the original's teardrop taper
  // bulges lower-left to ~x552-573 at y405..417; the straight wedge edge ran ~7-10pt
  // thin there. Small rotated ellipse overlaps circle and wedge -> smooth union).
  slide.addShape("ellipse", {
    x: px(557), y: px(402), w: px(22), h: px(12),
    rotate: 342, fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  slide.addShape("ellipse", {
    x: px(564), y: px(405.5), w: px(16), h: px(11),
    rotate: 342, fill: red, line: { color: C.pinRed, width: 0.5 },
  });
  // label: three lines tilted with the balloon (cropcmp_pin_2: 'WE'/'ARE'/'HERE')
  slide.addText([
    { text: "WE", options: { breakLine: true } },
    { text: "ARE", options: { breakLine: true } },
    { text: "HERE", options: {} },
  ], {
    x: px(537.5), y: px(343), w: px(60), h: px(55),
    align: "center", valign: "middle", margin: 0, rotate: 342,
    fontFace: "Arial", fontSize: 12.5, bold: true, color: C.white,
    lineSpacing: 17,
  });
}

// ---- delta block 4: decoder inter-box arrow shafts -------------------------------
// 017's decoder spine stops at y201 and resumes at y306 (in lecture 001 the gaps
// were filled by slide-019's navy chevrons, which THIS frame does not have). This
// frame shows the continuous thin dark shafts through both gaps (measured m14:
// gap1 build y194..206, gap2 build y250..263, center x~784.5-785, core ~2-3pt wide).
function drawGapShafts(pptx, slide) {
  const seg = (y0, y1) => slide.addShape("line", {
    x: px(784.7), y: px(y0), w: 0, h: px(y1 - y0),
    line: { color: "2F2F2F", width: 1.75 },
  });
  seg(193.6, 206.4);
  seg(250.5, 263.5);
}

// ---- composition ----------------------------------------------------------------

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();

// base: lecture-001 slide-19 certified composition with THIS slide's measured
// removals (legend callouts, leader lines, zone-1/2 navy chevrons)
const SKIP = [
  "legend1", "legend2", "legend3",
  "leader1", "leader2", "leader3", "leader4", "leader5",
  "dec_green",
];
PARENT.renderBase(pres, s, { numeral: 19, skip: SKIP });

// this slide's additions, in measured z-order: band under the pin
drawDecGreenChild(pres, s);
drawGapShafts(pres, s);
drawBottomBand(pres, s);
drawPin(pres, s);

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_019_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
