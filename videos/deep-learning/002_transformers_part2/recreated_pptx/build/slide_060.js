// slide_060.js — "What is Next  (as of 2020)" — closing reading list
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 60)
//
// CONTENT SPEC: analysis/slide_060_final.json (PASS_WITH_FIXES applied; verbatim text
// preserved incl. the double space before "(as of 2020)", the run-together
// "ModelsBeyond", the double space after "GPT-3", and the no-trailing-period citation
// "…Google Brain"). Original frame: unique_slides/slide_060.jpg (960x540).
// Provenance: slide_060_source/SOURCES.md (BANKED) — all six citations live-verified
// 2026-10-11 (GPT-1/2 Wikipedia, BERT arXiv 1810.04805, RoBERTa 1907.11692,
// Transformer-XL 1901.02860, T5 1910.10683, GPT-3 2005.14165); slide's own
// simplifications ("June 2019" RoBERTa, "Zhang Dai", "May 2019" BERT) are preserved
// verbatim per the fidelity law — slide wins for recreation.
//
// FRAME->SLIDE MAPPING (measured 2026-10-12, scratch/slide060/measure1..6.py):
// four chrome border landmarks in THIS frame — left border col 59, right border col
// 902, top border row 43 (row mean (105,44,52), dark red under JPEG — same value in
// certified slide_002's frame), bottom border row 516 <-> slide chrome 42, 919, 45, 540
// — IDENTICAL to certified slide_002/035/039:
//   frame_x = 18.63 + 0.96123 * slide_x ;  frame_y = 0.95556 * slide_y
// Badge cross-check: yellow-fill bbox (859..892, 56..85) center (875.5, 70.5) maps to
// slide (891.4, 73.8) vs house (893, 71) — within ~3px (same as certified 002/035/039),
// same playlist template. All content ink below is mapped to TRUE slide coordinates.
//
// CHROME LAW (playlist, founder directive 2026-10-11): shared module
// videos/deep-learning/shared_patterns/house_chrome.js, numeral 60. Spec's yellow/
// blue badge and #CC0000 full-perimeter frame are ml-intro-style vision guesses —
// superseded by the playlist chrome law (ground rules (a)).
//
// MEASURED FACTS honored here (frame = ground truth, overrides spec guesses):
//   * TITLE Arial Bold 31.0 (width-fit 30.88 / cap-fit 31.0), ink x 263.6..636.0 —
//     ink center 449.8, genuinely ~30pt LEFT of slide center 480 (measured as-is,
//     slide_035/039 precedent). Baseline row 86.5 -> slide 90.5. Red core census
//     (144-166,13-30,33-46) = C00000-family under this frame's JPEG (identical to
//     certified slide_006's rationale; dispatch deck red = C00000).
//   * ENTRIES Arial Bold 19.85-20.07 (per-line advance fit, real Arial metrics);
//     navy cores (0,0,101)..(15,0,127) R=G=0 -> 000080 (same as certified 032/039
//     calibration); red parenthetical cores (120-152,18-37,29-52) -> C00000 family.
//   * E1 RUN SPLIT (pixel-class map, measure6.py): blue "GPT-1" | RED "and" |
//     blue "GPT-2" | red "(Generative Pre-trained Transformers)" — the spec's
//     "'GPT-1 and GPT-2' all blue" was a vision guess; the frame's columns 150..182
//     ("and") carry 0 blue px and 4-16 red px/col while columns 189..243 ("GPT-2")
//     carry 2-14 blue and 0 red — frame wins. E6: blue "GPT-3" + red "  (175 …)"
//     (two-space gap frame cols 144..160, ink-identical to the spec reading).
//   * E4 is bold ITALIC in both runs (spec + script-12 raw agree) — Arial BoldItalic
//     fit em 19.88; red descriptor starts right after "Transformer-XL:" (col 244).
//   * CITATIONS Arial ITALIC (not bold), underlined, navy, ~17.4-17.8 (per-line
//     advance fit). Typeface: NOT Times New Roman Italic — Times' italic 'f' has a
//     descender; "Radford" shows ZERO ink below the underline (rows 184+ only the
//     'p' of OpenAI and 'y' of February descend, measure6 follow-up). 4x zoom crop
//     vision read (vision_C1.txt): "slanted sans-serif/humanist". Spec agrees
//     (sans-serif throughout). Left ink all four at slide x 113.8 (frame col 128).
//   * CONTENT BOX: stroke centers frame left cols 80-81 -> 64.6, right col 878.5 ->
//     894.5, top rows 116-117 -> 122.4, bottom rows 481-483 -> 504.4. Fill = WHITE
//     (deep-interior census (255,255,253-254); spec's #F5F5F5 was a vision guess —
//     frame wins, slide_039 precedent). Border cores (68-71,62-63,119-123) — the
//     same desaturated-navy JPEG read as certified slide_039's 000080 2pt box border
//     (its frame reads (66-67,60-61,148-149)) -> 000080 @ 2pt.
//   * OMITTED as video-capture artifacts (judge GROUND RULES (c)): black letterbox
//     strip (frame rows 517..539 = slide y >= 541, below the 540pt slide bottom) and
//     the mouse cursor blob at frame (842..845, 425..431) over the lower-right of
//     the content box (spec ~88% h, ~82% v — matches).

const { CHROME, drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const s = pres.addSlide();

// ---- 1. playlist house chrome (white canvas, gray panel + red border, badge "60")
drawHouseChrome(pres, s, { numeral: 60 });

const RED = "C00000", NAVY = "000080";
const pt = v => v / 72;
const K_AR = 0.9831; // baseline->boxTop lead (em), Arial — closed-loop corrected in slide_039

function textLine(id, runs, opts) {
  // runs: [{text, size, bold, italic, color, underline}]
  const maxSize = Math.max(...runs.map(r => r.options.fontSize));
  const o = {
    x: pt(opts.boxX), y: pt(opts.baseline - K_AR * maxSize),
    w: pt(opts.boxW), h: pt(1.6 * maxSize),
    align: opts.align || "left", valign: "top", margin: 0,
  };
  s.addText(runs.map(r => ({
    text: r.text,
    options: {
      fontSize: r.options.fontSize, bold: !!r.options.bold, italic: !!r.options.italic,
      color: r.options.color, fontFace: "Arial",
      underline: r.options.underline ? { style: "sng" } : undefined,
    },
  })), o);
}

// ---- 2. content box FIRST (z-order under text): white fill, navy 2pt border
s.addShape(pres.ShapeType.rect, {
  x: pt(64.6), y: pt(122.4), w: pt(829.9), h: pt(382.0),
  fill: { color: "FFFFFF" }, line: { color: NAVY, width: 2 },
});

// ---- 3. title (measured ink center 449.8, baseline 90.5) — box centered on it
textLine("title",
  [{ text: "What is Next  (as of 2020)", options: { fontSize: 31.1, bold: true, color: RED } }],
  { baseline: 90.5, boxX: 250.6, boxW: 400.0, align: "center" });

// ---- 4. six entry lines (blue name + red parenthetical runs; E1's measured
// 4-run split; E4 bold-italic). Baselines = mapped frame rows (measure4/5):
// E1 159.5->166.94, E2 223.5->233.90, E3 288.5->301.93, E4 347.5->363.62,
// E5 409.5->428.55, E6 452.5->473.51. Left inks: 73.2/74.3/73.2/76.3/73.2/73.2.
const B = { color: NAVY, bold: true }, R = { color: RED, bold: true };
textLine("e1", [
  { text: "GPT-1", options: { fontSize: 19.95, ...B } },
  { text: " and ", options: { fontSize: 19.95, ...R } },
  { text: "GPT-2", options: { fontSize: 19.95, ...B } },
  { text: " (Generative Pre-trained Transformers)", options: { fontSize: 19.95, ...R } },
], { baseline: 166.94, boxX: 72.7, boxW: 700 });
textLine("e2", [
  { text: "BERT", options: { fontSize: 19.93, ...B } },
  { text: " (Bidirectional Encoder Representations from Transformers)", options: { fontSize: 19.93, ...R } },
], { baseline: 233.90, boxX: 73.8, boxW: 700 });
textLine("e3", [
  { text: "RoBERTa", options: { fontSize: 20.04, ...B } },
  { text: " (Robustly Optimized BERT Approach)", options: { fontSize: 20.04, ...R } },
], { baseline: 301.93, boxX: 72.7, boxW: 700 });
textLine("e4", [
  { text: "Transformer-XL:", options: { fontSize: 19.89, ...B, italic: true } },
  { text: " Attentive Language ModelsBeyond a Fixed-Length Context", options: { fontSize: 19.89, ...R, italic: true } },
], { baseline: 363.62, boxX: 75.3, boxW: 780 });
textLine("e5", [
  { text: "T5", options: { fontSize: 19.96, ...B } },
  { text: " (Text-to-Text Transfer Transformer)", options: { fontSize: 19.96, ...R } },
], { baseline: 428.55, boxX: 72.7, boxW: 700 });
textLine("e6", [
  { text: "GPT-3", options: { fontSize: 20.21, ...B } },
  { text: "  (175 Billion Parameter, Beta Release June 2020)", options: { fontSize: 20.21, ...R } },
], { baseline: 473.51, boxX: 72.7, boxW: 700 });

// ---- 5. four citation lines: Arial Italic, underlined, navy, indented to 113.8.
// Baselines: C1 181.5->189.94, C2 245.5->256.92, C3 308.5->322.85, C4 367.6->384.71.
const CIT = { color: NAVY, italic: true, underline: true };
textLine("c1", [{ text: "Radford et al., OpenAI. June 2018 and February 2019.", options: { fontSize: 17.46, ...CIT } }],
  { baseline: 189.94, boxX: 113.3, boxW: 700 });
textLine("c2", [{ text: "Devlin et al., Google AI Language. May 2019.", options: { fontSize: 17.42, ...CIT } }],
  { baseline: 256.92, boxX: 113.3, boxW: 700 });
textLine("c3", [{ text: "Liu et al., Facebook AI. June 2019.", options: { fontSize: 17.43, ...CIT } }],
  { baseline: 322.85, boxX: 113.3, boxW: 700 });
textLine("c4", [{ text: "Zhang Dai et al. Carnegie Mellon University and Google Brain", options: { fontSize: 17.77, ...CIT } }],
  { baseline: 384.71, boxX: 113.3, boxW: 700 });

const OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/slide_060_recreated.pptx";
pres.writeFile({ fileName: OUT }).then(() => console.log("wrote " + OUT));
