// build/slide_024.js — slide 024 "Suggested Positional Encoders /
// (Rules Controlling Good Positional Encoder)"
// (Deep Learning DSAI 308, Transformers Part II — video 002, slide 24)
//
// DEPENDENCY-GATED CHILD BUILD (founder directive 2026-10-11; edge 24 <- 23, REPLACE delta):
// slide 24 = slide 23's judge-certified composition (components/slide_023.js, imported —
// NEVER re-derived) + this slide's measured delta. The certified component draws the full
// base through a FILTERING slide PROXY (001 slide_009 precedent: the certified drawing code
// itself stays the single source of truth); the proxy suppresses exactly the two blocks this
// slide REPLACES, so nothing is drawn-then-erased:
//   (1) subtitle text "(Normalize Seq. Length to "1")"  -> replaced by
//       "(Rules Controlling Good Positional Encoder)" on a #FFFF00 highlight strip
//   (2) the cyan problems highlight box + its texts + 3 bullet dots
//       -> replaced by the pale-yellow RULES box ([1][2][3])
// Everything else (title, 3 dashed containers, 24 boxes, ellipsis dots, left strip labels,
// 6 orange arrows + "+δ" labels, house chrome) is inherited 1:1 — PIL diff frame24-vs-frame23
// (scratch/slide024/diff_frames.py) found diff bands ONLY at the subtitle band (fy 82..106)
// and the bottom-box band (fy 366..491); both frames share the SAME chrome landmarks
// (L58/R901/T43/B516 -> mapping fx = 17.628 + 0.961231*slide_x, identical to slide_023's),
// so the parent's certified geometry lands 1:1 on this frame.
//
// MEASURED DELTA (scratch/slide024/*.py, PIL on unique_slides/slide_024.jpg; frame px ->
// slide pt via Sy = fy/0.955556, Sx = (fx-17.628)/0.961231):
//   * subtitle strip: frame x 301..741 y 81..107 -> slide x 294.8..752.5 (w 457.7),
//     y 84.8..112.0 (h 27.2); fill #FFFF00 (census (247,255,59) — chroma-bleed of FFFF00).
//   * subtitle text: ink x 288.6..757.7 (center 523.2), y 90.0..109.9; bold-metrics em fit
//     22.24 (Arialbd) -> 22.5pt bold = the parent's certified subtitle size; ink census
//     (25.9,16.5,110.2) = same family as the parent's certified 0000CC subtitle.
//     Box = the parent's certified subtitle box (x 85.9pt, y 82.8pt, w 12.13in, centered).
//   * rules box: border stroke cores frame cols 73..886 (IDENTICAL to frame23's cyan box
//     cols), rows 349..502 -> slide x 58.7..902.9 (w 844.2), y 365.2..525.3 (h 160.1);
//     fill #FFFFCC (spec; census (252,255,226) = JPEG chroma-lifted), border #0066CC 1.5pt
//     (border-row census (33,24,115)/(37,26,105) matches frame23's certified 0066CC box).
//   * rules text: 6 lines, uniform baseline pitch 22.9 (== parent's certified lineSpacing 23);
//     per-line em from fontTools width+height fits (Arial italic family, duplexed bold):
//     L1 17.25, L2 17.75, L3 17.75, L4 17.5, L5 17.25, L6 17.75 (fit residuals <= 7px@150dpi).
//     Emphasis measured (word-run + ink-coverage analysis: bold ~0.50-0.56 vs regular ~0.39-0.43):
//       L1 RED bold "[1] δ value" + BLUE bold "should be same" + BLUE regular rest
//       L2 BLUE regular; UNDERLINED "(same positions" (underline bins 99..221, continuous
//          through the word gap) and "same values" (bins 391..489, continuous)
//       L3 RED bold "[2] Range of position encoded values" + BLUE bold "should NOT depend on
//          sequence length"
//       L4 BLUE regular (typo "form -1 to 1" verbatim; double space after "range")
//       L5 RED bold "[3] Position Encoding  should be a  VECTOR" + BLUE regular
//          "(not scalar) and of" + BLUE bold UNDERLINED "same dimension as Word Embedding"
//          (underline bins 594..898 continuous — whole tail; resolves the spec's [?])
//       L6 BLUE regular (double space after "easily")
//     Text blue census (45.6,37.6,122.6) = parent's certified 0000CC family; red census
//     (137.2,40.5,39.0) = parent's certified CC0000 red-text family. Line box_y from the
//     EMPIRICAL LO placement gap (closed-loop attempt 1: ink_top = box_y + 0.388×E for
//     lineSpacing 23) applied to the frame's true ink tops (bloomed +1.0pt); L1 carries the
//     frame's measured ~15pt gap after "[1]" (3 spaces; frame word widths pin 17.5pt).
//     Subtitle pinned to 22pt (width fit 22.1-22.24; attempt-1 render at 22.5 was 6pt wide)
//     with box_y 84.5 (frame ink 1pt lower than the parent's frame).
//   * badge numeral 24 = the number printed on THIS original frame.
//   * video-player black bar (frame rows 517+) and any cursor: capture artifacts, omitted.
//
// LAWS honored: playlist chrome via the certified component (drawn ONCE inside renderBase);
// verbatim text incl. double spaces and the "form" typo; margin:0 + explicit fontFace
// everywhere; explicit lineSpacing 23 on every rule line; no '#' in hex; single-version
// deliverable; certified component NOT edited (suppression via proxy, banked in the drop log).

const path = require("path");
const pptxgen = require("pptxgenjs");
const parent = require("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/components/slide_023.js");

const IN = (pt) => pt / 72;
const FONT = "Arial";
const BODYBLUE = "0000CC";
const BOXRED = "CC0000";
const YELLOW = "FFFF00";
const RULES_FILL = "FFFFCC";
const RULES_LINE = "0066CC";

// ---- filtering proxy: render the certified base, suppressing the 2 replaced blocks -----
function filteringSlide(real, pptx, dropped) {
  const proxy = {};
  let bg;
  Object.defineProperty(proxy, "background", {
    get() { return bg; },
    set(v) { bg = v; real.background = v; },
  });
  proxy.addText = function (text, options) {
    const xPt = (options && options.x ? options.x : 0) * 72;
    const yPt = (options && options.y ? options.y : 0) * 72;
    const isSubtitle = text === "(Normalize Seq. Length to \u201c1\u201d)";
    const isBoxText = yPt > 370 && yPt < 535 && xPt < 100;
    if (isSubtitle || isBoxText) {
      dropped.push({ kind: "text", preview: String(Array.isArray(text) ? text.map(t => t.text).join("") : text).slice(0, 50), x: xPt, y: yPt });
      return;
    }
    return real.addText(text, options);
  };
  proxy.addShape = function (type, options) {
    const xPt = (options && options.x ? options.x : 0) * 72;
    const yPt = (options && options.y ? options.y : 0) * 72;
    const isCyanBox = type === pptx.ShapeType.roundRect && yPt > 360 && xPt < 100;
    const isBulletDot = type === pptx.ShapeType.ellipse && xPt > 70 && xPt < 95 && yPt > 425 && yPt < 515;
    if (isCyanBox || isBulletDot) {
      dropped.push({ kind: "shape", shape: String(type), x: xPt, y: yPt });
      return;
    }
    return real.addShape(type, options);
  };
  return proxy;
}

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.333 x 7.5 in
const pptx = pres;
const slide = pres.addSlide();

const dropped = [];
const proxy = filteringSlide(slide, pptx, dropped);

// 1. certified base composition (numeral 24 = this frame's printed number)
parent.renderBase(pptx, proxy, { numeral: 24 });

// 2. DELTA A — subtitle: yellow highlight strip + replaced text
slide.addShape(pptx.ShapeType.rect, {
  x: IN(294.8), y: IN(84.8), w: IN(457.7), h: IN(27.2),
  fill: { color: YELLOW }, line: { type: "none" },
});
slide.addText("(Rules Controlling Good Positional Encoder)", {
  x: IN(85.9), y: IN(84.5), w: 12.13, h: IN(34),
  align: "center", valign: "top", margin: 0,
  fontSize: 22, bold: true, color: BODYBLUE, fontFace: FONT,
});

// 3. DELTA B — rules box (replaces the cyan problems box)
slide.addShape(pptx.ShapeType.roundRect, {
  x: IN(58.7), y: IN(365.2), w: IN(844.2), h: IN(160.1), rectRadius: 0.07,
  fill: { color: RULES_FILL },
  line: { color: RULES_LINE, width: 1.5 },
});

// 4. DELTA C — the three numbered rules (6 measured text lines)
const rules = [
  {
    x: 62.2, y: 377.1, w: 600, size: 17.75, runs: [
      { text: "[1]   \u03b4 value ", options: { color: BOXRED, bold: true } },
      { text: "should be same", options: { color: BODYBLUE, bold: true } },
      { text: " for Long sequence and short sequence", options: { color: BODYBLUE } },
    ],
  },
  {
    x: 97.6, y: 400.1, w: 780, size: 17.75, runs: [
      { text: "(same positions", options: { color: BODYBLUE } },
      { text: " will be encoded with ", options: { color: BODYBLUE } },
      { text: "same values", options: { color: BODYBLUE } },
      { text: " irrespective of the length of the sequence)", options: { color: BODYBLUE } },
    ],
  },
  {
    x: 61.2, y: 422.1, w: 700, size: 17.75, runs: [
      { text: "[2] Range of position encoded values", options: { color: BOXRED, bold: true } },
      { text: " should NOT depend on sequence length", options: { color: BODYBLUE, bold: true } },
    ],
  },
  {
    x: 92.4, y: 446.2, w: 500, size: 17.75, runs: [
      { text: "(predefined fixed range  e.g. from 0 to 1 , form -1 to 1 , ...)", options: { color: BODYBLUE } },
    ],
  },
  {
    x: 62.2, y: 468.4, w: 880, size: 17.5, runs: [
      { text: "[3] Position Encoding  should be a  VECTOR", options: { color: BOXRED, bold: true } },
      { text: " (not scalar) and of ", options: { color: BODYBLUE } },
      { text: "same dimension as Word Embedding", options: { color: BODYBLUE, bold: true } },
    ],
  },
  {
    x: 97.6, y: 491.2, w: 640, size: 17.75, runs: [
      { text: "(in order to easily  combine Position Encoding and Word Encoding vectors)", options: { color: BODYBLUE } },
    ],
  },
];
// 4b. the three underlines as EXPLICIT measured rectangles (frame rows 401-402 / 466-467
// -> slide y 419.7..421.8 / 487.7..489.8, thickness 2.1pt): LO's built-in text underline
// rendered 1.7pt lower than the original's (attempt-1 closed loop), and its offset is not
// controllable — rects reproduce the measured position/thickness exactly.
const underlines = [
  { x: 99.0, y: 419.7, w: 122.5 },   // "(same positions"  (frame bins 99..221)
  { x: 391.5, y: 419.7, w: 98.0 },   // "same values"      (frame bins 391..489)
  { x: 594.0, y: 487.7, w: 303.5 },  // "same dimension as Word Embedding" (bins 594..898)
];
for (const u of underlines) {
  slide.addShape(pptx.ShapeType.rect, {
    x: IN(u.x), y: IN(u.y), w: IN(u.w), h: IN(2.1),
    fill: { color: BODYBLUE }, line: { type: "none" },
  });
}
for (const r of rules) {
  slide.addText(
    r.runs.map((rn) => ({ text: rn.text, options: rn.options })),
    {
      x: IN(r.x), y: IN(r.y), w: IN(r.w), h: IN(26),
      align: "left", valign: "top", margin: 0, lineSpacing: 23,
      fontSize: r.size, italic: true, color: BODYBLUE, fontFace: FONT,
    }
  );
}

// 5. prove what the proxy suppressed (banked evidence)
console.log("proxy dropped calls:", JSON.stringify(dropped, null, 1));
// expected: 1 subtitle text + 6 box texts ("Use δ...", "Problems:", 3 bullets,
// "(though...)") = 7 texts; 1 cyan box shape + 3 bullet-dot ellipses = 4 shapes
const nText = dropped.filter((d) => d.kind === "text").length;
const nShape = dropped.filter((d) => d.kind === "shape").length;
if (nText !== 7 || nShape !== 4) {
  throw new Error(`proxy drops text=${nText} (want 8) shape=${nShape} (want 4) — inspect log`);
}

pres.writeFile({ fileName: path.join(__dirname, "..", "slide_024_recreated.pptx") })
  .then(() => console.log("WROTE slide_024_recreated.pptx"));
