// slide_007.js — 001_introduction slide 7 "Major Domains of Machine/Deep  Learning"
// Deep Learning DSAI 308 playlist.
//
// Geometry: PIL-measured from the ground-truth frame
//   videos/deep-learning/001_introduction/unique_slides/slide_007.jpg (960x540, 1px = 1pt = 1/72 in).
// Measurements re-verified 2026-10-12 by the resumed worker (qa/slide007/measure_original.py
// + follow-up letter-level scans) — the predecessor's numbers were never verified before it died.
//   CORRECTIONS vs the predecessor draft: title font 25pt (NOT 30 — 'M' cap height measured
//   18px -> Arial bold cap 0.716em -> ~25pt; the 30pt "cap 21.5px" claim was wrong), domain
//   labels 25pt (NOT 23 — 'T'/'N' caps 17-18px), boxes y330..441 (NOT 328..442), inner frame
//   stroke 1pt (NOT 2 — profiles show a single 1px core row/col), outer L stroke ~2.5pt with
//   top line x57..903 (measured y42..44 loose / x57..903) and left line x57..59 y42..517.
//
// Chrome: playlist house chrome (founder directive 2026-10-11) via shared_patterns/house_chrome.js
//   — imported, NEVER re-drawn, NEVER ml-intro values. Badge numeral = 7 (slide file number;
//   the ORIGINAL frames of this lecture carry no badge — 001_introduction/AGENTS.md 2026-10-12,
//   assumption pending founder veto).
//
// Measured structure (frame px):
//   per-slide red outer frame = an "L": top line y42..44 (x57..903) + left line x57..59
//     (y42..517, ends at the black strip). NO right/bottom outer edge (verified: right zone
//     x890..945 y40..520 contains only the inner frame's right stroke).
//   inner red frame (complete rect): 1px strokes at left x70, top y119, right x894(-895),
//     bottom y483 -> rect boundary x70..894.5, y119..483.5, line C00000 1pt, white fill.
//   black bottom strip: x38..921, y519..539 fully black (y518 AA edge) -> drawn y519..537.5
//     so the chrome bottom stroke (rows 538-539, required by house_chrome_check.py) stays
//     visible — same 2-frame-px deviation documented on the certified slide_002 build.
//   title box (black): x296..677, y136..249; 3 lines bold yellow centered, 25pt:
//     "Major Domains" (cap y155..172, ink x397..577) / "of" (y184..200, x476..498) /
//     "Machine/Deep  Learning" (y212..235 incl 'g' descender, x341..632) — DOUBLE SPACE
//     verbatim (SOURCES.md). Cap-top pitch 29/28 -> lineSpacing 28.5pt.
//   domain boxes (y330..441, PIL modal colors): blue x90..270 (2,0,167); green x299..474
//     (10,135,59); brown x504..679 (111,59,2); dark red x709..883 (159,0,0). White bold 25pt,
//     cap tops: CV 363/391; NLP 348/~377(cursor-contaminated)/405 -> pitch 28.5.
//   arrows: 4 thin red curves (stroke ~2.2px), shared origin (486.5, 251) = title-box bottom,
//     heads tip down at y~327 landing on box-top centers (180 / 386.5 / 590 / 795).
//     Drawn as ONE matplotlib catmull-rom 600dpi transparent PNG through the traced stroke
//     centers (certified slide_011 mechanism; this pptxgenjs has NO curvedConnector shape —
//     measured: ShapeType has no connector presets). Traces + generator banked in qa/slide007/.
//   mouse-cursor artifact over "Language" in the original: screen-recording artifact,
//     NOT recreated (spec recreation_brief step 12).

const pptxgen = require("pptxgenjs");
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/slide_007_recreated.pptx";
const ASSETS = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets";

const px = (v) => v / 72;

// ---- palette (PIL modal measurements) ----
const RED = "C00000";
const BLACK = "000000";
const WHITE = "FFFFFF";
const YELLOW = "FFFF00";
const BLUE = "0200A7";
const GREEN = "0A873B";
const BROWN = "6F3B02";
const DARKRED = "9F0000";

// ---- build ----
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// Playlist house chrome (white canvas, gray panel + red border, badge numeral 7)
drawHouseChrome(pres, slide, { numeral: "7" });

// Per-slide red outer frame — the original shows ONLY top + left lines (an "L")
slide.addShape(pres.ShapeType.line, {
  x: px(57), y: px(43), w: px(846.5), h: 0,
  line: { color: RED, width: 2.5 },
});
slide.addShape(pres.ShapeType.line, {
  x: px(58), y: px(42.5), w: 0, h: px(474.5),
  line: { color: RED, width: 2.5 },
});

// Inner red frame with white fill (the content area) — 1pt stroke per measured profiles
slide.addShape(pres.ShapeType.rect, {
  x: px(70), y: px(119), w: px(824.5), h: px(364.5),
  fill: { color: WHITE }, line: { color: RED, width: 1 },
});

// Black bottom strip (stops at y537.5 so the chrome bottom stroke stays visible)
slide.addShape(pres.ShapeType.rect, {
  x: px(38), y: px(519), w: px(883.5), h: px(18.5),
  fill: { color: BLACK }, line: { color: BLACK, width: 0 },
});

// Title box — black fill, 3 lines bold yellow, double space verbatim in line 3
slide.addText(
  [
    { text: "Major Domains", options: { breakLine: true } },
    { text: "of", options: { breakLine: true } },
    { text: "Machine/Deep  Learning" },
  ],
  {
    shape: pres.ShapeType.rect,
    x: px(296), y: px(136), w: px(381.5), h: px(113.5),
    fill: { color: BLACK }, line: { color: BLACK, width: 0 },
    align: "center", valign: "middle", margin: 0,
    fontFace: "Arial", fontSize: 25, bold: true, color: YELLOW,
    lineSpacing: 28.5,
  }
);

// Domain boxes — white bold text, centered
const boxText = (extra) =>
  Object.assign(
    {
      shape: pres.ShapeType.rect,
      align: "center", valign: "middle", margin: 0,
      fontFace: "Arial", fontSize: 25, bold: true, color: WHITE,
      lineSpacing: 28.5,
    },
    extra
  );

slide.addText("Time Series", boxText({
  x: px(90), y: px(330), w: px(180), h: px(112),
  fill: { color: BLUE }, line: { color: BLUE, width: 0 },
}));
slide.addText(
  [
    { text: "Computer", options: { breakLine: true } },
    { text: "Vision" },
  ],
  boxText({
    x: px(299), y: px(330), w: px(175), h: px(112),
    fill: { color: GREEN }, line: { color: GREEN, width: 0 },
  })
);
slide.addText("Speech", boxText({
  x: px(504), y: px(330), w: px(175), h: px(112),
  fill: { color: BROWN }, line: { color: BROWN, width: 0 },
}));
slide.addText(
  [
    { text: "Natural", options: { breakLine: true } },
    { text: "Language", options: { breakLine: true } },
    { text: "Processing" },
  ],
  boxText({
    x: px(709), y: px(330), w: px(174), h: px(112),
    fill: { color: DARKRED }, line: { color: DARKRED, width: 0 },
  })
);

// Four curved arrows — ONE 600dpi transparent PNG fan (certified slide_011 mechanism:
// catmull-rom through PIL-traced stroke centers + solid triangle heads), embedded at
// EXACT size (canvas pt [175,245,800,330], never rescaled).
const fan = require(ASSETS + "/arrows007.json");
slide.addImage({
  path: fan.asset,
  x: px(fan.canvas_pt[0]), y: px(fan.canvas_pt[1]),
  w: fan.w_in, h: fan.h_in,
});

pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
