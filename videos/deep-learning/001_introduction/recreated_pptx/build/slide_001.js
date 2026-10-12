// build/slide_001.js — "Deep  Learning DSAI 308" course cover (001_introduction).
// ATTEMPT 3 (CERTIFIED: visual-judge PASS 2026-10-12, transcript
// recreated_pptx/qa/slide001/judge_attempt_3.txt; closed-loop
// qa/slide001/selfcheck_attempt_3_out.txt all-PASS; house_chrome_check PASS).
//
// This build script is a THIN ENTRY over the banked component
// components/slide_001.js (renderBase) — the single source of truth for the
// composition, banked under the PLAYLIST-SCOPED BANKING OBLIGATION so future
// lectures' cover slides can require() it by absolute path. Geometry/typography
// provenance and the chrome/no-top-rule/artifact-omission rationale live in the
// component header. Badge numeral = 1 (originals carry no printed numbers;
// PENDING FOUNDER VETO per 001_introduction/AGENTS.md).
const { renderBase } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/components/slide_001.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();
renderBase(pres, s, { numeral: 1 });

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_001_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
