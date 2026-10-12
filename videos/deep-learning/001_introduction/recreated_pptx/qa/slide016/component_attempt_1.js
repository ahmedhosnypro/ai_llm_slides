// components/slide_016.js — slide 016 "The Complete ML Classification Process"
// (001_introduction, Deep Learning DSAI 308) — DEPENDENT slide, parent = 9.
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11/12; 001_introduction/slide_dependencies.json
// edge 16←9; parent CERTIFIED: gen_status=passed, visual_check=PASS, judge_attempt_1.txt):
// this child IMPORTS the parent's certified composition
//   require('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_009.js')
// and calls its renderBase — the parent's geometry is NEVER re-derived or copy-pasted.
// Only the measured DELTA (below) is drawn on top of / instead of named parent blocks.
// Slide 17 (grandchild via 16) must require THIS module and call renderBase(pptx, slide, opts).
//
// renderBase(pptx, slide, opts) with
//   opts.chrome  — draw house chrome (default true; drawn by the PARENT component via
//                  components/house_chrome.js — never re-drawn here)
//   opts.numeral — badge numeral (default "16"; = the slide's file number per the
//                  playlist badge law, 001_introduction/AGENTS.md PENDING-FOUNDER-VETO)
//   opts.skip / opts.only — delta block selectors (same grammar as the parent).
//
// DELTA vs parent 9 (all PIL-measured on unique_slides/slide_016.jpg, 960x540, 1px=1pt,
// in = px/72; scripts in qa/slide016/: delta_diff.py, measure_regions*.py, measure_*.py):
//   INHERITED UNCHANGED via parent renderBase (skip list omits nothing else):
//     chrome (numeral overridden to 16), title, panel, blackbar, box_extraction,
//     box_selection, box_classification, arrow2, arrow3, arrow4
//     (frame diff vs slide_009.jpg outside the delta regions < 5 px/row).
//   REMOVED parent blocks: curve2, final_ellipse, label_cleaned, label_vectors,
//     label_features, label_predicted  (Final Result terminal + gray output labels
//     are absent in slide_016.jpg — measured white where the parent had them).
//   REPLACED / MOVED delta blocks (child frame is ground truth):
//   1. training_ellipse — same size (x78 w131 h58, fill F6DEC2 core modal 246,222,194,
//      edge 999999) but shifted UP 9px: outline y128..186 vs parent y137..195; label
//      text bands y141..157 / y162..174 (parent 150..166 / 171..183). Text keeps the
//      parent's certified 18pt bold pitch-20 metrics at y137.7.
//   2. box_pre — SAME width/border/text metrics as the parent's chainBox (w105, navy
//      000080 2pt, fill FAFED8, 17pt bold pitch 19) but shifted LEFT 15px: navy border
//      columns 129-130 / 235-236 (parent 144-145 / 250-251). Drawn at x=130.5.
//   3. arrow1 — re-spanned for the shifted box: x236..293 at y236.5 (parent 250..293);
//      same 1.75pt red line + triangle head. arrows 2-4 identical (measured equal).
//   4. curve1 — REDRAWN hand-stroke (600dpi PNG, qa/slide016/gen_curves_016.py, same
//      certified mechanism as the parent's gen_curves_009.py): stem x96.5 from the
//      raised ellipse (~y178), bend right, head tip at the shifted box edge (129.5,236),
//      barbs (119,230)/(119,241). Embedded at measured bbox x91..133, y175..245.
//   5. box_post → "Classifier Output" (REPLACED content, same certified geometry as the
//      parent's box_post x748 w115 h57 at y208): fill DCBFA1 (core modal 220,191,161;
//      spec guess #D9A96A loses to ink per deck law), dark-brown border 552818
//      (darkest-20% ring median 85,40,24), two-line 17pt bold black text
//      "Classifier"/"Output" (ink bands y221..233 / y240..255, pitch 19 = parent's
//      chain text metrics).
//   6. Four gray hand-annotation callouts (the parent's small gray output labels do not
//      exist on this frame) — roundRect fill E6E8E6, edge C2C4C2 (ring modal 195,197,194
//      = parent labelEdge), rectRadius 0.07 (corner ~5px, as parent), 14pt bold black,
//      lineSpacing 16, vertically centered per measured ink bands:
//        A (85,291,194,41)  "Based on your inspection" / "You select the techniques"
//        B (280,336,154,60) "Handcrafted features" / "(by You)"   (lowest, ~10% down)
//        C (435,282,140,60) "Your decision" / "And using which" / "approach" (3 lines)
//        D (612,282,89,41)  "Apply" / "Model"
//      Callout A occupies the parent label_cleaned y-band (291..331) with identical ink
//      starts (298/314) — the parent's certified grayLabel text offset (+3.8, h32) is
//      reused verbatim for h41 boxes; h60 boxes use measured centering (+13.5 h32 for
//      2 lines, +6 h48 for 3 lines).
//
// VERBATIM text per analysis/slide_016_final.json (PASSED content gate, score 9);
// validation.fixes applied (two-line/ three-line wraps). Mouse-cursor and player-chrome
// artifacts omitted per imagery note. LAWS honored: no '#' hex, margin:0 + explicit
// fontFace + explicit lineSpacing everywhere, chrome drawn once by the parent component.

const path = require("path");
const PARENT = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_009.js");

const ASSETS = path.join(__dirname, "..", "assets");

// parent palette reused (never re-invented): red C00000, chain fills/borders, gray
// label pair E6E8E6/C2C4C2, peach F6DEC2/999999. Child-only colors measured on f16:
const C = Object.assign({}, PARENT.C, {
  boxPostFill: "DCBFA1",   // Classifier Output fill (core modal 220,191,161)
  boxPostEdge: "552818",   // dark brown border (darkest-20% ring median 85,40,24)
});
const px = PARENT.px;
const SANS = "Arial";
const BOX_Y = 208, BOX_H = 57; // parent chain band (unchanged for boxes 1 and 5)

// parent blocks this child OMITS (removed on the child frame) or replaces with its own
// measured drawing (training_ellipse, box_pre, arrow1, curve1, box_post):
const SKIP = [
  "training_ellipse", "box_pre", "arrow1", "curve1", "box_post", "curve2",
  "final_ellipse", "label_cleaned", "label_vectors", "label_features", "label_predicted",
];

// ---- delta block functions -----------------------------------------------------

function drawTrainingEllipse(pptx, slide) {
  // parent geometry shifted UP 9px (outline y128..186; fill core rows 131..185)
  slide.addShape(pptx.ShapeType.ellipse, {
    x: px(78), y: px(128), w: px(131), h: px(58),
    fill: { color: C.peach }, line: { color: C.peachEdge, width: 0.75 },
  });
  slide.addText(
    [
      { text: "Training", options: { breakLine: true } },
      { text: "Data", options: {} },
    ],
    {
      x: px(88), y: px(137.7), w: px(111), h: px(40),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 18, bold: true, color: C.black,
      lineSpacing: 20,
    }
  );
}

function drawBoxPre(pptx, slide) {
  // parent chainBox metrics (w105, 2pt navy, 17pt bold pitch 19) at x=130.5 (shift -15)
  slide.addShape(pptx.ShapeType.rect, {
    x: px(130.5), y: px(BOX_Y), w: px(105), h: px(BOX_H),
    fill: { color: C.box1Fill }, line: { color: C.navy, width: 2 },
  });
  slide.addText(
    [
      { text: "Pre", options: { breakLine: true } },
      { text: "processing", options: {} },
    ],
    {
      x: px(130.5), y: px(217.6), w: px(105), h: px(38),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 17, bold: true, color: C.black,
      lineSpacing: 19,
    }
  );
}

function drawArrow1(pptx, slide) {
  // re-spanned for the shifted box: box1 outer right 236.5 -> box2 left border 292
  slide.addShape(pptx.ShapeType.line, {
    x: px(236), y: px(236.5), w: px(293 - 236), h: 0,
    line: { color: C.red, width: 1.75, endArrowType: "triangle" },
  });
}

function drawCurve1(pptx, slide) {
  // 600dpi bezier + head wedge traced to THIS frame (gen_curves_016.py);
  // embed at exact measured bbox — never rescaled
  slide.addImage({
    path: path.join(ASSETS, "curve1_016.png"),
    x: px(91), y: px(175), w: px(42), h: px(70),
  });
}

function drawBoxClassifierOutput(pptx, slide) {
  // parent box_post geometry (x748 w115 h57 @ y208) with this frame's content
  slide.addShape(pptx.ShapeType.rect, {
    x: px(748), y: px(BOX_Y), w: px(115), h: px(BOX_H),
    fill: { color: C.boxPostFill }, line: { color: C.boxPostEdge, width: 2 },
  });
  slide.addText(
    [
      { text: "Classifier", options: { breakLine: true } },
      { text: "Output", options: {} },
    ],
    {
      x: px(748), y: px(217.6), w: px(115), h: px(38),
      align: "center", valign: "middle", margin: 0,
      fontFace: SANS, fontSize: 17, bold: true, color: C.black,
      lineSpacing: 19,
    }
  );
}

// gray hand-annotation callout: parent grayLabel style (roundRect rectRadius 0.07,
// fill E6E8E6 edge C2C4C2 1pt, 14pt bold, lineSpacing 16) at child-measured geometry.
// textDy/textH follow the parent's certified h41 pattern (dy +3.8, h32); taller boxes
// center per measured ink bands (h60: dy +13.5 h32 for 2 lines, dy +6 h48 for 3 lines).
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
  callout(pptx, slide, 85, 291, 194, 41,
    ["Based on your inspection", "You select the techniques"], 3.8, 32);
}
function drawCalloutHandcrafted(pptx, slide) {
  callout(pptx, slide, 280, 336, 154, 60,
    ["Handcrafted features", "(by You)"], 13.5, 32);
}
function drawCalloutDecision(pptx, slide) {
  callout(pptx, slide, 435, 282, 140, 60,
    ["Your decision", "And using which", "approach"], 6, 48);
}
function drawCalloutApply(pptx, slide) {
  callout(pptx, slide, 612, 282, 89, 41,
    ["Apply", "Model"], 3.8, 32);
}

// ---- composition ---------------------------------------------------------------

const DELTA_BLOCKS = {
  training_ellipse_016: drawTrainingEllipse,
  box_pre_016: drawBoxPre,
  arrow1_016: drawArrow1,
  curve1_016: drawCurve1,
  box_classifier_output_016: drawBoxClassifierOutput,
  callout_inspection_016: drawCalloutInspection,
  callout_handcrafted_016: drawCalloutHandcrafted,
  callout_decision_016: drawCalloutDecision,
  callout_apply_016: drawCalloutApply,
};

/**
 * Draw the full slide-016 composition: the certified parent composition (chrome with
 * THIS slide's numeral + all non-omitted blocks) plus this slide's measured delta.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[delta-names], only:[delta-names], chrome:bool, numeral }
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  PARENT.renderBase(pptx, slide, {
    skip: SKIP,
    chrome: opts.chrome !== false,
    numeral: opts.numeral === undefined ? "16" : opts.numeral,
  });
  for (const [name, fn] of Object.entries(DELTA_BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, DELTA_BLOCKS, SKIP, C, px };
