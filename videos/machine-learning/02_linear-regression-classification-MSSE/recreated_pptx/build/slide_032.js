// slide_032.js — "Classification Example" (ML lecture 02) — INTENTIONAL EXACT DUPLICATE of certified slide 031.
// Worker ml02-w032-g1, 2026-10-13. Founder directive (verbatim): "32 is exactly as 31
// (duplication but it's intentional on the original slides, but on ours we will follow it as well)".
//
// Duplication verified on the ORIGINALS by PIL (scratch/ml02/slide032/dup_check_output.txt,
// cluster_output.txt, probe_clusters_output.txt, probe_gray_stroke_output.txt):
//   slide_031.jpg vs slide_032.jpg, thr>16 diff = 533 px (0.10% of frame):
//   - badge numeral ink (digit "1" vs "2") inside circle d~35 @ (876,73)  -> THE intentional diff;
//   - x[228..246] y[447..463] (135 px): presenter's pen/marker cursor ink present in 031 only
//     (032 is clean) — correctly OMITTED from the certified recreation per GROUND RULES (c);
//   - x=455 y[387..396] (56 px): faint 1px-wide gray stroke (RGB 133-160) in 032 only, 10px tall,
//     in empty margin left of the green box border — video artifact, not content, not drawn;
//   - remainder: <=4px JPEG-noise components (max diff 147 isolated single pixels).
// => NO content delta. Build = certified parent component + badge numeral 32, nothing else.
// Parent NEVER edited (cascade law): components/slide_031.js is required read-only.

const pptxgen = require("pptxgenjs");
const base = require("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/build/components/slide_031.js");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
const slide = pptx.addSlide();
base.renderBase(pptx, slide, { numeral: 32 });

const out =
  process.argv[2] ||
  "videos/machine-learning/02_linear-regression-classification-MSSE/recreated_pptx/slide_032_recreated.pptx";
pptx.writeFile({ fileName: out }).then(() => console.log("written:", out));
