// slide_017.js — slide 017 "The Complete ML Classification Process" (001_introduction,
// Deep Learning DSAI 308) — GRANDCHILD: 17 ← 16 ← 9 (transitive chain).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11/12; 001_introduction/slide_dependencies.json
// edges 17←16, 16←9; BOTH parents CERTIFIED — 16: gen_status=passed + visual_check=PASS
// (judge_attempt_1.txt, banked component), 9: certified with banked component):
// this build IMPORTS the certified components — it NEVER re-derives or copy-pastes
// their geometry:
//   require('.../recreated_pptx/build/components/slide_016.js')  (which itself requires
//   '.../recreated_pptx/build/components/slide_009.js' by absolute path)
// Composition = parent-9 renderBase at block granularity (chrome with THIS slide's
// numeral + panel/blackbar/chain boxes 2-4/arrows 2-4) + slide-016's chain delta blocks
// (training_ellipse_016, box_pre_016, arrow1_016, curve1_016, box_classifier_output_016
// — pixel-diff vs slide_016.jpg outside the 17-delta regions is <6 stray px) + THIS
// slide's measured delta only.
//
// DELTA vs parent 16 (all PIL-measured on unique_slides/slide_017.jpg, 960x540, 1px=1pt,
// in = px/72; measurement scripts in scratch/slide017/, prior worker forensics preserved
// in qa/slide017/): the pixel diff 017 vs 016 touches ONLY rows 68-87 (title 'ML' band),
// 245-250 (6px codec noise), 278-457 (annotation band). Chain boxes/arrows/ellipse are
// PIXEL-IDENTICAL to 16 (inherited via 016's delta blocks):
//   1. title — same certified geometry as 9's drawTitle (box 117,58.5 w700 h40, Arial
//      bold 26, lineSpacing 30; ink x219..715 cap 68 baseline 87 in BOTH frames) but
//      'ML' recolored NAVY 000080 (ink core modal (0,0,113..117), darkest-20% (0,0,115)
//      — the deck's certified navy; spec #0000CC loses to ink per deck law). Ink bboxes
//      left/right of ML identical in both frames (diff = video-codec macroblock noise).
//   2. callout_inspection — 16's A (85,291,194,41) shifted DOWN +64: strokes y355/393,
//      same x85 w194; text bands 361..373 / 377..387 (same 14pt pitch-16 metrics).
//   3. callout_handcrafted — 16's B (280,336,154,60) moved down+in: strokes x281..432 /
//      y400..457 → (281,400,152,58); text bands 415..426 / 432..445.
//   4. callout_decision — 16's C (435,282,140,60) shifted DOWN +64: strokes y346/403 →
//      (435,346,140,58); text bands 354..363 / 370..382 / 388..397; x-geometry identical
//      to 16 (certified x435 w140 — right-border cols match in both frames).
//   5. callout_apply — 16's D (612,282,89,41) 2-line "Apply"/"Model" REPLACED by a
//      single-line box: strokes x613..698 / y283..321 → (613,283,86,39), ONE text band
//      297..309 ("Apply Model", 14pt bold — 'Apply Model' @14pt = 83px vs measured 80).
//   6. NEW yellow starburst "Based on / Trained Model!": star16 (deck mechanism, cf.
//      slide_018/020 builds) at outline bbox (709,265,166,74); fill FAFEDB (core modal
//      (250,254,219)), gray edge C2C4C2 w1 (stroke modal (206,208,207) — thin-stroke
//      JPEG; family edge). Text 11pt bold red C00000 pitch 13 ("Trained Model!" @11pt =
//      77.6px vs measured 79), bands 291..298 / 304..311, center x788.
//   7. NEW red dashed divider: hand-drawn dashed line, ink band y332..336 (rows
//      332/334/335, ~2pt thick), dashes x77..858 (dash 3-4px, gap 3-4px), drawn OVER the
//      starburst's bottom spike tips (red dash px measured inside the star x-range).
//      Mechanism: native LINE, dashType sysDash, width 2, C00000.
//   8. NEW white starburst "Based on / Human Experience": star16 at outline bbox
//      (624,358,200,57); fill FFFFFF (core (254,255,253)), gray edge C2C4C2 w1 (stroke
//      modal (181,191,182)). Text 12pt bold NAVY 000080 pitch 13.5 ("Human Experience"
//      @12pt = 108.0px vs measured 108), bands 375..382 / 389..395, center x713.5.
//
// VERBATIM text per analysis/slide_017_final.json (PASS_WITH_FIXES, score 9); all 23
// recreation_brief steps honored (steps 1-3/16-22 map to the blocks above; step 23:
// mouse-cursor artifact and black letterbox bar NOT drawn — blackbar is the certified
// slide-005 progress-bar precedent from parent 9). LAWS: no '#' hex, margin:0 + explicit
// fontFace + explicit lineSpacing everywhere, chrome drawn once (numeral "17" = file
// number per the deck's PENDING-FOUNDER-VETO badge law), single-version deliverable.

const pptxgen = require("pptxgenjs");
const P16 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_016.js");
const P9 = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_009.js");

const C = Object.assign({}, P9.C, {
  starYFill: "FAFEDB",   // Trained Model starburst fill (core modal 250,254,219)
  starWFill: "FFFFFF",   // Human Experience starburst fill (core 254,255,253)
});
const SANS = "Arial";
const px = P9.px;

// parent-9 blocks this slide OMITS: title (recolored delta below) + every block 16
// already skips (removed/replaced on the 16 frame — same removals hold here, the diff
// proves it) + box_post (replaced by 16's Classifier Output block).
const P9_SKIP = [
  "title",
  "training_ellipse", "box_pre", "box_post", "arrow1", "curve1", "curve2",
  "final_ellipse", "label_cleaned", "label_vectors", "label_features", "label_predicted",
];

// slide-016 chain delta blocks inherited UNCHANGED (pixel-identical regions)
const P16_INHERIT = [
  "training_ellipse_016", "box_pre_016", "arrow1_016", "curve1_016",
  "box_classifier_output_016",
];

// ---- slide-017 delta blocks -----------------------------------------------------

function drawTitle17(pptx, slide) {
  // parent title geometry, 'ML' recolored navy (runs: spaces ride INSIDE the red runs)
  slide.addText(
    [
      { text: "The Complete ", options: { color: C.red } },
      { text: "ML", options: { color: C.navy } },
      { text: " Classification Process", options: { color: C.red } },
    ],
    {
      x: px(117), y: px(58.5), w: px(700), h: px(40),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 26, bold: true, color: C.red,
      lineSpacing: 30,
    }
  );
}

// gray hand-annotation callout: the certified parent style (roundRect rectRadius 0.07,
// fill E6E8E6 edge C2C4C2 1pt, 14pt bold, lineSpacing 16) at THIS frame's measured
// geometry. textDy/textH follow the parent's certified centering patterns.
function callout(pptx, slide, x, y, w, h, lines, textDy, textH) {
  slide.addShape(pptx.ShapeType.roundRect, {
    x: px(x), y: px(y), w: px(w), h: px(h), rectRadius: 0.07,
    fill: { color: C.labelFill }, line: { color: C.labelEdge, width: 1 },
  });
  const items = lines.map((t, i) => ({
    text: t, options: { breakLine: i < lines.length - 1 },
  }));
  slide.addText(items, {
    x: px(x + 1), y: px(y + textDy), w: px(w - 2), h: px(textH),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize: 14, bold: true, color: C.black,
    lineSpacing: 16,
  });
}

function drawCalloutInspection(pptx, slide) {
  callout(pptx, slide, 85, 355, 194, 39,
    ["Based on your inspection", "You select the techniques"], 3.8, 32);
}
function drawCalloutHandcrafted(pptx, slide) {
  callout(pptx, slide, 281, 400, 152, 58,
    ["Handcrafted features", "(by You)"], 13, 32);
}
function drawCalloutDecision(pptx, slide) {
  callout(pptx, slide, 435, 346, 140, 58,
    ["Your decision", "And using which", "approach"], 6, 48);
}
function drawCalloutApply(pptx, slide) {
  callout(pptx, slide, 613, 283, 86, 39, ["Apply Model"], 4, 32);
}

// starburst callout: star16 (deck mechanism) + centered bold text lines
function starburst(pptx, slide, x, y, w, h, fill, lines, fontSize, textColor, lineSpacing, tx, ty, tw, th) {
  slide.addShape(pptx.ShapeType.star16, {
    x: px(x), y: px(y), w: px(w), h: px(h),
    fill: { color: fill }, line: { color: C.labelEdge, width: 1 },
  });
  const items = lines.map((t, i) => ({
    text: t, options: { breakLine: i < lines.length - 1 },
  }));
  slide.addText(items, {
    x: px(tx), y: px(ty), w: px(tw), h: px(th),
    align: "center", valign: "middle", margin: 0,
    fontFace: SANS, fontSize, bold: true, color: textColor,
    lineSpacing,
  });
}

function drawStarTrainedModel(pptx, slide) {
  starburst(pptx, slide, 709, 265, 166, 74, C.starYFill,
    ["Based on", "Trained Model!"], 11, C.red, 13, 743, 287, 90, 28);
}
function drawStarHumanExperience(pptx, slide) {
  starburst(pptx, slide, 624, 358, 200, 57, C.starWFill,
    ["Based on", "Human Experience"], 12, C.navy, 13.5, 652, 372, 124, 27);
}

function drawDivider(pptx, slide) {
  // hand-drawn dashed red divider, drawn LAST (crosses the starburst's spike tips).
  // dashType 'dash' ([4,3]xw) @1pt: closed-loop measured dash 8.3px/gap 6.25px duty 0.57
  // @150dpi vs original dash 8.3/gap 4.2 duty 0.57 (sysDash @2pt measured 13/4 duty 0.74 —
  // rejected; ink band y332..336, dash x77..858).
  slide.addShape(pptx.ShapeType.line, {
    x: px(77), y: px(334), w: px(858 - 77), h: 0,
    line: { color: C.red, width: 1, dashType: "dash" },
  });
}

// ---- composition ----------------------------------------------------------------

const DELTA_BLOCKS = {
  title_017: drawTitle17,
  callout_inspection_017: drawCalloutInspection,
  callout_handcrafted_017: drawCalloutHandcrafted,
  callout_decision_017: drawCalloutDecision,
  callout_apply_017: drawCalloutApply,
  star_trained_model_017: drawStarTrainedModel,
  star_human_experience_017: drawStarHumanExperience,
  divider_017: drawDivider,
};

/**
 * Draw the full slide-017 composition: certified 16->9 chain (chrome with numeral 17 +
* inherited chain blocks) plus this slide's measured delta.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[delta-names], only:[delta-names], numeral }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  // certified grandparent composition at block granularity (chrome numeral = 17)
  P9.renderBase(pptx, slide, { skip: P9_SKIP, numeral: opts.numeral === undefined ? "17" : opts.numeral });
  // certified parent chain delta (pixel-identical regions on this frame)
  for (const name of P16_INHERIT) P16.DELTA_BLOCKS[name](pptx, slide);
  // this slide's measured delta (divider last — it crosses the starburst spikes)
  for (const [name, fn] of Object.entries(DELTA_BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

// ---- build ----------------------------------------------------------------------

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_017_recreated.pptx";
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();
renderBase(pres, slide);
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
