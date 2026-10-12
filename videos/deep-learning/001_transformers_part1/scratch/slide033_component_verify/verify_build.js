// verify_build.js — drive the retro-banked component components/slide_033.js exactly
// like a child would (new pptxgen + LAYOUT_WIDE + addSlide + renderBase), plus smoke
// builds. Run:
//   cd /home/ahmed/Projects/ai_llm_slides && NODE_PATH=$(npm root -g) node \
//     videos/deep-learning/001_transformers_part1/scratch/slide033_component_verify/verify_build.js
const path = require("path");
const pptxgen = require("pptxgenjs");

const BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1";
const comp = require(path.join(BASE, "recreated_pptx", "build", "components", "slide_033.js"));
const { drawHouseChrome } = require(path.join(BASE, "recreated_pptx", "build", "components", "house_chrome.js"));
const OUT = path.join(BASE, "scratch", "slide033_component_verify", "renders");

// block names as a child would discover them from the component's own BLOCKS export
const ALL = Object.keys(comp.BLOCKS);
console.log("component BLOCKS (z-order):", ALL.join(", "));
console.log("component exports:", Object.keys(comp).join(", "));
console.log("GEO keys:", Object.keys(comp.GEO).join(", "));

function build(name, fn) {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const slide = pres.addSlide();
  fn(pres, slide);
  return pres.writeFile({ fileName: path.join(OUT, name) })
    .then(() => console.log("WROTE renders/" + name));
}

(async () => {
  // 1. FULL composition — the 0-pixel-diff candidate (child-style call, empty opts)
  await build("component_full.pptx", (p, s) => comp.renderBase(p, s, {}));

  // 2. smoke: skip ONE block ("sigma") -> diff must be confined to the sigma bbox
  await build("smoke_skip_sigma.pptx", (p, s) =>
    comp.renderBase(p, s, { skip: ["sigma"] }));

  // 3. smoke: only = all-but-sigma — must be pixel-identical to #2 (skip ≡ only)
  await build("smoke_only_equivalence.pptx", (p, s) =>
    comp.renderBase(p, s, { only: ALL.filter((n) => n !== "sigma") }));

  // 4. smoke: numeral override (badge must read 99)
  await build("smoke_numeral99.pptx", (p, s) => comp.renderBase(p, s, { numeral: 99 }));

  // 5. smoke: chrome off (no gray panel, no red border, no badge)
  await build("smoke_nochrome.pptx", (p, s) => comp.renderBase(p, s, { chrome: false }));

  // 6/7. chrome-ONLY references for a renderer-neutral badge-glyph proof:
  //      badge crop of the full build must equal chrome-only(numeral 33 — the
  //      component's default); badge crop of the numeral99 build must equal
  //      chrome-only(99). (Explicit numeral REQUIRED: drawHouseChrome({}) draws
  //      NO badge — empty numeral means badge suppressed.)
  await build("smoke_chromeonly_33.pptx", (p, s) => drawHouseChrome(p, s, { numeral: 33 }));
  await build("smoke_chromeonly_99.pptx", (p, s) => drawHouseChrome(p, s, { numeral: 99 }));

  // 8. unknown block names MUST throw (typo in a child's selector never silently
  //    drops a block).
  const throwCases = [
    { label: "skip bogus", opts: { skip: ["bogus"] } },
    { label: "skip mixed valid+bogus", opts: { skip: ["pills", "bogus"] } },
    { label: "only bogus", opts: { only: ["bogus"] } },
    { label: "only mixed valid+bogus", opts: { only: ["title", "nope"] } },
  ];
  let throwFails = 0;
  for (const tc of throwCases) {
    const pres = new pptxgen();
    pres.layout = "LAYOUT_WIDE";
    const slide = pres.addSlide();
    let msg = null;
    try { comp.renderBase(pres, slide, tc.opts); } catch (e) { msg = e.message; }
    if (!msg) { console.error("FAIL (no throw): " + tc.label); throwFails++; }
    else console.log("THREW ok [" + tc.label + "]: " + msg);
  }
  // positive control: every real block name is accepted (skip all = chrome only)
  {
    const pres = new pptxgen();
    pres.layout = "LAYOUT_WIDE";
    const slide = pres.addSlide();
    comp.renderBase(pres, slide, { skip: ALL }); // must NOT throw
    console.log("positive control ok: skip=<all " + ALL.length + " blocks> accepted");
  }
  if (throwFails) { console.error(throwFails + " throw-case FAILURES"); process.exit(1); }
  console.log("ALL BUILDS DONE");
})().catch((e) => { console.error(e); process.exit(1); });
