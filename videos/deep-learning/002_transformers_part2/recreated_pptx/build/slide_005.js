// slide_005.js — 002_transformers_part2 slide 005 "Encoder – Decoder Transformer"
// (Deep Learning DSAI 308, video 002, slide 5 — Part II recap of the Part-I figure).
//
// CONTENT SPEC: analysis/slide_005_final.json (PASS_WITH_FIXES, score 9; verbatim
// labels, [?] items preserved). Original frame: unique_slides/slide_005.jpg (960x540).
// SOURCES: slide_005_source/SOURCES.md (arXiv 1706.03762v7 Fig 1 + Fig 2 left/right,
// banked in 001/slide_18_source — verified 2026-10-11).
//
// COMPOSITION LAW (empirically established, scratch/slide005/m6..m11): this frame is
// the SAME figure state as lecture 001 slide 18 — the m8 diff of MY frame vs 001:18's
// frame (affine fitted from this frame's chrome landmarks L58.5/R902/T42/B516.5 vs
// 001:18's L38.5/R920.5/T42/B538) shows panel diff 25.07 with every >=40px component
// being (a) my two orange highlight bands, (b) the badge numeral (18 vs 5), or (c)
// 1px border/dash PHASE artifacts of identical content (inset frames, trunk, bypass).
// The two "callout boxes", the dashed connector curves, the h annotation, the yellow
// L-band, the title, the insets and the whole Figure-1 architecture of THIS frame are
// 001:18's certified composition. I therefore import 001:18's CERTIFIED component
// (001 DB: gen_status=passed, visual_check=PASS; md5 c6c99d501a426f9858110e2e98154f54)
// by ABSOLUTE PATH and draw ONLY the measured delta. (002:19 — the same figure at the
// LATER 019 state with legends/steel repaints/pin/bottom-band — is NOT my state; its
// render diffed against my frame exactly at those 019-only blocks, m6.)
//
// FRAME->SLIDE MAPPING: video 002 capture zoomed OUT ~0.958 with letterbox below.
// This frame's four chrome landmarks match 002:19's certified fit (L58.32 R901.37
// T43.26 B516.85) within ~1px, so the certified composite mapping applies:
//   frame_x = 18.0787 + 0.961084 * build_x ;  frame_y = 0.4700 + 0.957187 * build_y
// (build pt = slide pt; render px = build pt * 150/72, zero offset — the certified
// selfcheck lesson). All delta geometry below is measured in FRAME px and converted
// through this mapping. Letterbox strip (frame rows 517..539) = video artifact,
// BELOW the mapped slide bottom — omitted per the deck GEOMETRY FACT + judge
// GROUND RULES (c); same for any pen cursor (none present in this frame).
//
// PIL DELTA vs the imported composition (my frame is ground truth; scratch/slide005/
// m9_bands.py + m10_edges.py + m11_zones.py, alpha-fit of ED7D31 over the warped
// 001:18 reference):
//   ADDED band (b)  translucent orange rectangle over the encoder Multi-Head
//                   Attention box extending LEFT past the encoder panel edge:
//                   build x583 y357.5 w151 h46; tint map: solid rows build
//                   y358..403, cols x586..733 with 1-2pt anti-alias fringe; blend
//                   alpha median 0.63 (p25 0.60 / p75 0.72) over peach panel,
//                   tan container, salmon box, blue/red circles -> ED7D31 at
//                   transparency 37 (B-channel fit, LO effective-alpha offset ~0.05 measured).
//   ADDED band (c)  translucent orange rectangle over the decoder attention stack
//                   (cross-attention box + masked-attention box top + V/K/Q row +
//                   N x circle), extending RIGHT past the decoder panel edge:
//                   build x748.5 y276.5 w139.5 h48; tint map: solid rows build
//                   y278..322 (fringe 276/324), cols x749..884 (fringe to 888);
//                   alpha median 0.61 (p25 0.58 / p75 0.66) over mint panel,
//                   tan-brown box, purple box, mint N x -> transparency 37 (B-channel fit, LO effective-alpha offset ~0.05 measured).
//   BADGE           numeral 5 = the number printed on THIS frame (verified in-frame;
//                   the component default is 18 — passed explicitly).
//   INHERITED (no action, GT18-diff clean): banner1/banner2 callouts (the spec's
//                   callout boxes — text runs colored exactly as 018 renders them,
//                   which pixel-matches this frame), connect_h/connect_tan curves +
//                   arrowheads (the spec's "dashed annotation arrows" — thin red/pink
//                   curves; my frame matches 001:18's curves; dash-phase variance is
//                   documented inherited variance), dash_d1/d2/d3 zoom connectors,
//                   h_annot, enc/dec MHA boxes, 017's solid-yellow L-band (rects
//                   678,251,67,16 / 730,267,15,41 / 740,307,47,16 — the spec's
//                   "yellow highlight zone"; frame-measured yellow mask rows build
//                   252..267 x 677..742 match rect1/rect2), 'Output' + 'Outputs'
//                   yellow highlights (frame yellow rows build 112..129 / 495..510),
//                   corner handles (12-corner green-pixel counts match 001:18 within
//                   JPEG noise), decoder spine/gaps, chevron-free state (019's navy
//                   chevrons are 019-state content absent from BOTH frames).
//
// FOUNDER ARROW FIX (2026-10-12, defect: "arrows between components not attaching"):
// the six connector blocks (connect_h/connect_tan/h_annot/dash_d1/d2/d3) are drawn
// by build/components/slide_018_arrows_fix.js — a COPY-THEN-MODIFY wrapper that
// calls the certified 001:18 component with those blocks SKIPPED and redraws them
// at geometry PIL-measured on THIS frame (scratch/slide005_fix/ m13..m27): the
// spurious banner1 stroke deleted, connect_tan extended onto the inset top border,
// the h circle/head/curve re-anchored to the measured circle (center build
// (493.4,378.6) d22, head tip touching its top), d1/d2 as single STRAIGHT dashed
// lines attached at both ends (d1 -> enc MHA box left border (650,372), d2 -> red
// rect left border (304.8,375.5)), d3 re-sloped (-0.957) onto the SDPA inset edge.
// Arrows draw BEFORE the orange bands (in the original the band tints d1's tail).
//
// [?] items preserved per validation.uncertain_items: decoder cross-attention box
// text/fill (rendered by the certified dec_mha_box block — measured match), left
// flowchart bypass endpoint (inherited inset_sdpa_flow), gray copy counts (inherited).
//
// Laws honored: composition imported (require by absolute path, numeral passed);
// verbatim text; no '#' in hex; transparency property (no alpha hex); PIL-measured
// geometry; explicit fontFace via the certified chain; single-version deliverable
// ../slide_005_recreated.pptx; house chrome drawn ONCE inside the component.

const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_018_arrows_fix.js");
const pptxgen = require("pptxgenjs");

const px = PARENT.px; // build pt -> inches (1px = 1pt = 1/72 in)

// ---- measured delta palette (JPEG-core, scratch m9) ------------------------------
const C = {
  highlightOrange: "ED7D31", // instructor highlight overlays (spec #ED7D31)
};

// ---- delta block 1: orange highlight over the encoder MHA (extends left) ---------
function drawBandB(pptx, slide) {
  slide.addShape("rect", {
    x: px(583), y: px(357.5), w: px(151), h: px(46),
    fill: { color: C.highlightOrange, transparency: 37 },
    line: { color: C.highlightOrange, width: 0.25, transparency: 37 },
  });
}

// ---- delta block 2: orange highlight over the decoder attention stack ------------
function drawBandC(pptx, slide) {
  slide.addShape("rect", {
    x: px(748.5), y: px(276.5), w: px(139.5), h: px(48),
    fill: { color: C.highlightOrange, transparency: 37 },
    line: { color: C.highlightOrange, width: 0.25, transparency: 37 },
  });
}

// ---- composition ----------------------------------------------------------------

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();

// base: lecture-001 slide-18 certified composition (house chrome incl. badge,
// title, callout banners, insets + zoom dashes, Figure-1 architecture) with the
// six connector blocks replaced by the measured arrow fix (see header above)
PARENT.renderBase(pres, s, { numeral: 5 });

// this slide's additions, measured z-order: bands OVER the boxes they tint AND
// over d1's tail (the original tints the dashes under the band)
drawBandB(pres, s);
drawBandC(pres, s);

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_005_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
