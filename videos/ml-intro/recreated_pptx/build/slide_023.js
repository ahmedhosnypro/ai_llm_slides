// Build: slide 023 recreation — "Data Sets" section-divider slide.
// Spec: analysis/slide_023_final.json (validated PASS_WITH_FIXES; renumbered from
// old-deck slide 030 — same pixels, new2old_mapping "23" -> old 30, diff 0.0)
// Output: recreated_pptx/slide_023_recreated.pptx
//
// HOUSE FRAME RULE (founder, 2026-10-09; recorded in AGENTS.md and
// scripts/17_worker_instructions.md): every slide uses slide 3's shared outer template,
// OVERRIDING the spec JSON and any judge finding for these elements — background E8E8E8,
// outer red frame (rect x:0.15 y:0.15 w:13.03 h:7.2, line C00000 width 1.5, no visible
// fill over BG), slide-number badge (oval x:12.48 y:0.30 w:0.5 h:0.5, fill/line FFF9C4,
// the SLIDE ID "23" — no zero-padding — bold 18pt 333333), slide-title text box
// (y:0.28, x:0.6, w:12.13, align center; slide-3 style: red bold 30pt Arial).
// Judge discrepancies about frame/badge/title-y are OVERRIDDEN — not fix triggers.
//
// Slide content per spec: the spec's central visual element is the white-filled rectangle
// with thin dark-red (#A02C3A) outline (17%-80% width, 32%-66% height) containing the large
// bold red (#B01E28) verbatim title 'Data Sets' — kept in place as the content layer
// under the house chrome (same pattern as the slide-032 house rebuild). The faint gray
// stray squiggle (spec 'artifact', uncertain [?]) is a video/cursor artifact and is
// deliberately NOT recreated (per the judge standard).

const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette — NO '#' prefixes (corrupts the file)
const BG = "E8E8E8";        // slide background light gray (house + spec)
const HOUSE_RED = "C00000";  // house frame line / house title
const BADGE_YELLOW = "FFF9C4"; // house badge fill/line
const INK = "333333";        // house badge numeral
const BOX_RED = "A02C3A";    // spec: dark-red outline of the title box
const TITLE_RED = "B01E28";  // spec: large in-box title red
const WHITE = "FFFFFF";      // spec: title box fill
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// HOUSE FRAME 1: outer thin red frame inset 0.15in from every edge
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: HOUSE_RED, width: 1.5 },
});

// HOUSE FRAME 2: slide-title text box (slide-3 template style)
s.addText("Data Sets", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.9, align: "center", valign: "top",
  fontSize: 30, bold: true, color: HOUSE_RED, fontFace: FONT, margin: 0,
});

// HOUSE FRAME 3: slide-number badge, top-right corner inside the frame.
// Badge numeral = SLIDE ID ("23"), per founder clarification 2026-10-09
// (matches the number printed on the original slide_023.jpg — OCR-verified).
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5,
  fill: { color: BADGE_YELLOW }, line: { color: BADGE_YELLOW, width: 0.5 },
});
s.addText("23", {
  x: 12.48, y: 0.3, w: 0.5, h: 0.5, align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// CONTENT (per spec): white title box with thin dark-red outline, centered.
// Spec: ~17%-80% width, ~32%-66% height.
const boxX = 0.17 * W, boxY = 0.32 * H;
const boxW = (0.80 - 0.17) * W, boxH = (0.66 - 0.32) * H;
s.addShape(pptx.shapes.RECTANGLE, {
  x: boxX, y: boxY, w: boxW, h: boxH,
  fill: { color: WHITE }, line: { color: BOX_RED, width: 1.5 },
});

// CONTENT (per spec): large bold red verbatim title centered in the white box
s.addText("Data Sets", {
  x: boxX, y: boxY, w: boxW, h: boxH,
  align: "center", valign: "middle",
  fontSize: 60, bold: true, color: TITLE_RED, fontFace: FONT, margin: 0,
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_023_recreated.pptx" })
  .then(() => console.log("done"));
