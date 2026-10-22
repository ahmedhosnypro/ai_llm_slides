// COMPONENT (certified) — banked by ml02-w032-g1 after judge PASS
// (qa/slide032/judge_attempt_1.txt: FINAL VERDICT: PASS, attempt 1, findings all
// MINOR — see worker_report.md; inheritance law: all findings sit on regions
// pixel-identical to certified slide 031, the only delta here is the badge numeral).
//
// slide_032.js — "Classification Example" (ML lecture 02). Founder directive:
// slide 32 is an INTENTIONAL EXACT DUPLICATE of 31 ("32 is exactly as 31 — on ours
// we will follow it as well"). This component is a DELEGATING wrapper: it contains
// zero geometry and always renders the certified parent composition with numeral 32.
// Single source of truth stays in components/slide_031.js (never edited — cascade law).
//
// Duplication proof on the originals (scratch/ml02/slide032/): thr>16 diff
// 031-vs-032 = 533 px (0.10%) = badge numeral ink + 031-only pen-cursor artifact
// (omitted per GROUND RULES (c)) + a faint 10px gray stroke in 032 only (video
// artifact, not drawn). Rendered proof: our 32 render vs certified 31 render =
// 325 px at thr>0, ALL inside the badge circle (outside-circle diff = 0 px).
//
// Usage: renderBase(pptx, slide, opts) — opts.numeral defaults to 32.

const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_031.js");

function renderBase(pptx, slide, opts = {}) {
  const numeral = opts.numeral === undefined ? 32 : opts.numeral;
  parent.renderBase(pptx, slide, { numeral });
}

module.exports = { renderBase };
