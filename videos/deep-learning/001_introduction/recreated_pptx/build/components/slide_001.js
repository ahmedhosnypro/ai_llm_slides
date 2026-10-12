// components/slide_001.js — slide 001 "Deep  Learning DSAI 308" course-cover composition
// (001_introduction).
//
// DEPENDENCY CONTRACT (founder directive 2026-10-11; banked 2026-10-12 under the
// PLAYLIST-SCOPED BANKING OBLIGATION, retro style): this is the playlist's course-cover
// slide — every future lecture video under videos/deep-learning/ opens on the same cover,
// so a later lecture's slide 1 (or any recap referencing `deep-learning/001_introduction:1`)
// MUST require() this module by ABSOLUTE path and call renderBase(pptx, slide, opts) —
// or cherry-pick blocks via opts.skip / opts.only — NEVER re-derive or copy-paste the
// geometry. Derived additively from the CERTIFIED build script build/slide_001.js
// (attempt 3, visual-judge PASS 2026-10-12, transcript recreated_pptx/qa/slide001/
// judge_attempt_3.txt) and verified 0-pixel-diff against the certified 150dpi render.
//
// BADGE NUMERAL: default 1 — this lecture's original frames carry NO badge and NO printed
// slide numbers (PIL-probed 2026-10-12); the playlist chrome law mandates the badge and the
// deck AGENTS.md pins the numeral = file number, assumption PENDING FOUNDER VETO. If the
// founder vetoes badges, the fix lands HERE + in shared_patterns (never per-slide).
//
// Block granularity (one function per visual block, in z-order):
//   title, prepared_by, instructors, logo
// (No separate top-rule block: the spec's "top rule" is the chrome panel's TOP BORDER —
// the dark row-43 line sits exactly on this frame's panel gray extent; drawing a content
// rule on the mandated chrome border would double a single original line. The letterbox
// strip and '+' cursor artifact in the original are recording artifacts, excluded per the
// spec recreation_brief step 8 and judge ground rule (c).)
//
// GEOMETRY PROVENANCE: PIL forensics on unique_slides/slide_001.jpg (960x540, 1px = 1pt,
// in = px/72) — scratch/slide001/forensics.py + probe2-4.py; typography ground truth from
// the 2x-crop vision read scratch/slide001/typography_read.txt (names/headings bold ITALIC;
// prepared email bold upright; instructor emails REGULAR, email2 italic), corroborated by
// stem-slope + ink-density measurements; closed-loop verified element-by-element
// (qa/slide001/selfcheck_attempt_3_out.txt: all 10 elements within tolerance).
const { drawHouseChrome } = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/shared_patterns/house_chrome.js");

const RED = "C00000";    // title + red headings (spec title_text)
const NAVY = "1414B8";   // names (spec body_text; frame core (27,15,158))
const EBLUE = "1F1F8F";  // emails (spec accent; frame core muted (71,64,143))
const FONT = "Arial";

function drawTitle(pptx, slide) {
  // one centered box, two lines, 63pt bold (LibreOffice/Arial-substitute cap 0.688em on
  // 42-43px measured caps), lineSpacing 70 (measured cap-to-cap pitch 70px), attempt 1's
  // empirically closed-loop-PASSed geometry, unchanged through certification.
  slide.addText(
    [
      { text: "Deep  Learning", options: { breakLine: true } },
      { text: "DSAI 308", options: {} },
    ],
    {
      x: 0.417, y: 1.612, w: 12.13, h: 2.1,
      align: "center", valign: "top",
      fontSize: 63, bold: true, color: RED, fontFace: FONT, margin: 0,
      lineSpacing: 70,
    }
  );
}

function drawPreparedBy(pptx, slide) {
  // credit block, centered at measured ink center 7.14in (box x 4.64, w 5.0)
  slide.addText("Prepared By", {
    x: 4.64, y: 3.9806, w: 5.0, h: 0.42,
    align: "center", valign: "top",
    fontSize: 20, bold: true, italic: true, color: RED, fontFace: FONT, margin: 0,
  });
  slide.addText("Dr. Khaled Mostafa ElSayed", {
    x: 4.64, y: 4.3147, w: 5.0, h: 0.5,
    align: "center", valign: "top",
    fontSize: 23, bold: true, italic: true, color: NAVY, fontFace: FONT, margin: 0,
  });
  slide.addText("kmelsayed@zewailcity.edu.eg", {
    x: 4.64, y: 4.7178, w: 5.0, h: 0.34,
    align: "center", valign: "top",
    fontSize: 16.5, bold: true, color: EBLUE, fontFace: FONT, margin: 0,
  });
}

function drawInstructors(pptx, slide) {
  // bottom-left block at measured ink-lefts / cap tops; heading tracked (+charSpacing 1.1:
  // the original heading is +16% wider per cap than Liberation metrics), names bold ITALIC,
  // emails REGULAR (email2 italic) per the crop vision read + ink density.
  slide.addText("Instructors:", {
    x: 1.03, y: 5.435, w: 4.5, h: 0.44,
    align: "left", valign: "top",
    fontSize: 21, bold: true, italic: true, charSpacing: 1.1, color: RED, fontFace: FONT, margin: 0,
  });
  slide.addText("Dr. Khaled Mostafa ElSayed", {
    x: 1.628, y: 5.834, w: 4.5, h: 0.44,
    align: "left", valign: "top",
    fontSize: 21, bold: true, italic: true, color: NAVY, fontFace: FONT, margin: 0,
  });
  slide.addText("kmelsayed@zewailcity.edu.eg", {
    x: 1.628, y: 6.2178, w: 4.5, h: 0.34,
    align: "left", valign: "top",
    fontSize: 16.5, color: EBLUE, fontFace: FONT, margin: 0,
  });
  slide.addText("Dr. Mohamed Maher Ata", {
    x: 1.628, y: 6.487, w: 4.5, h: 0.44,
    align: "left", valign: "top",
    fontSize: 21, bold: true, italic: true, color: NAVY, fontFace: FONT, margin: 0,
  });
  slide.addText("momaher@zewailcity.edu.eg", {
    x: 1.628, y: 6.843, w: 4.5, h: 0.34,
    align: "left", valign: "top",
    fontSize: 16.5, italic: true, color: EBLUE, fontFace: FONT, margin: 0,
  });
}

function drawLogo(pptx, slide) {
  // Zewail City logo lockup (teal emblem + bilingual white box), cropped from THIS slide's
  // original frame (resolves all [?] micro-text pixel-exactly), embedded at EXACT size
  // (337x86px @72ppi = 4.6806x1.1944in) at its measured position.
  slide.addImage({
    path: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/build/assets/zewail_logo_001introduction.png",
    x: 7.8611, y: 5.9444, w: 4.6806, h: 1.1944,
  });
}

const BLOCKS = {
  title: drawTitle,
  prepared_by: drawPreparedBy,
  instructors: drawInstructors,
  logo: drawLogo,
};

/**
 * Draw the full slide-001 composition (chrome + all blocks), selectively.
 * @param {object} pptx  pptxgenjs instance (for ShapeType)
 * @param {object} slide slide returned by pptx.addSlide()
 * @param {object} opts  { skip:[names], only:[names], chrome:bool, numeral:string|number }
 *   — skip/only name blocks from the table above; unknown names THROW (a typo in a
 *     child's selector must never silently drop a block).
 */
function renderBase(pptx, slide, opts = {}) {
  const skip = new Set(opts.skip || []);
  const only = opts.only ? new Set(opts.only) : null;
  const known = new Set(Object.keys(BLOCKS));
  for (const name of skip) {
    if (!known.has(name)) throw new Error(`slide_001: unknown block name in opts.skip: '${name}'`);
  }
  if (only) {
    for (const name of only) {
      if (!known.has(name)) throw new Error(`slide_001: unknown block name in opts.only: '${name}'`);
    }
  }
  if (opts.chrome !== false) {
    drawHouseChrome(pptx, slide, { numeral: opts.numeral === undefined ? 1 : opts.numeral });
  }
  for (const [name, fn] of Object.entries(BLOCKS)) {
    if (skip.has(name)) continue;
    if (only && !only.has(name)) continue;
    fn(pptx, slide);
  }
}

module.exports = { renderBase, BLOCKS, COLORS: { RED, NAVY, EBLUE, FONT } };
