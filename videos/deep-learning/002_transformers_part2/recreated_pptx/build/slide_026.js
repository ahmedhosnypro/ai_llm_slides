// slide_026.js — "Sin/Cos Encoders" (Deep Learning DSAI 308, Transformers Part II — video 002, slide 26)
//
// The composition lives in the BANKED COMPONENT components/slide_026.js (renderBase + BLOCKS),
// banked after the judge PASS (attempt 2, 2026-10-12) for the dependency family
// 28 ← [27, 26] and 49 ← 26. This wrapper renders the certified composition verbatim:
// children must import the COMPONENT, not this file.
//
// CONTENT SPEC: analysis/slide_026_final.json (verbatim; PASS_WITH_FIXES applied). Original frame:
// unique_slides/slide_026.jpg (960x540). Provenance: slide_026_source/SOURCES.md — the diagram is the
// course's redraw of TI design guide TIDUA05B (TIDA-00176) Figure 1-1; PDF text extraction confirmed
// every label (incl. corridor label "A, B, R" and callout "A+, A-, B+, B- and Marker R+/R-" — the
// spec's "A, B," / ", and Marker R+, R-" were analysis misreads; frame+guide+SOURCES agree).
//
// CHROME LAW (playlist): shared_patterns/house_chrome.js drawHouseChrome(...{numeral:26}).
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide026/measure_chrome*.py): video 002 capture is
// zoomed OUT ~0.958 with a black letterbox strip below. Fitted from THIS frame's chrome landmarks
// (border left 58.5, right 901.5, top 43.0, bottom-border ~516 (black strip starts 518), badge center
// (875.5, 70.5) <-> slide chrome 42, 919, 45, 540, (893,71)) — identical to build/slide_002.js's fitted
// transform:
//   frame_x = 18.628 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// All content ink is mapped to TRUE slide coordinates before drawing (see the component).
//
// OMITTED AS VIDEO-CAPTURE ARTIFACTS (ground rule (c)): black letterbox strip (frame rows 518..539,
// below the 540pt slide bottom under the fitted mapping); the course's own thin dark-red outer border
// and yellow badge are REPLACED by the playlist house chrome (founder directive, judge ground rule (a)).

const pptxgen = require("pptxgenjs");
const path = require("path");
const { renderBase } = require(path.join(__dirname, "components", "slide_026.js"));

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in

const s = pres.addSlide();
renderBase(pres, s, { numeral: 26 });

pres.writeFile({ fileName: path.join(__dirname, "..", "slide_026_recreated.pptx") })
  .then(() => console.log("WROTE slide_026_recreated.pptx"));
