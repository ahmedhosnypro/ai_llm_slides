// Slide 031 recreation — "Pre processing"
// pptxgenjs 4.0.1; house frame rule (founder directive) + analysis/slide_031_final.json
// Derived from prior old-numbering build (slide_039.js, old id 39) — badge renumbered to 31.
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Colors (NO "#" prefix — corrupts the file)
const BG = "E8E8E8";       // house background
const RED = "C00000";      // frame / content-frame border
const INK = "333333";      // badge numeral
const BADGE = "FFF9C4";    // badge fill (house)
const BLACK = "000000";
const HDRRED = "FF0000";   // 'Preprocessing is' text
const YELBOX = "FFFFCC";   // title box fill (spec)
const PURPLE = "7030A0";   // title box outline (spec)
const WHITE = "FFFFFF";    // content frame fill (spec)
const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// ---- House outer chrome (overrides spec AND judge) ----
// Outer red frame
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: 13.03, h: 7.2,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});
// Slide-number badge: oval, numeral "31" (number printed on the original slide image)
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: BADGE }, line: { color: BADGE, width: 0.5 },
});
s.addText("31", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle",
  fontSize: 18, bold: true, color: INK, fontFace: FONT, margin: 0,
});

// ---- Spec content ----
// Content frame: red/maroon outline, white fill, x 7-93%, y 23-97% of slide
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.93, y: 1.73, w: 11.47, h: 5.55,
  fill: { color: WHITE }, line: { color: RED, width: 2 },
});

// Title box (spec): pale-yellow rect with purple outline, bold black text.
// House rule: title text box y:0.28, x:0.6, w:12.13, centered — box follows the title.
// Judge A1 (old-numbering run): original title is a modest label-sized heading —
// smaller font, snug box.
s.addShape(pptx.shapes.RECTANGLE, {
  x: 5.24, y: 0.30, w: 2.85, h: 0.72,
  fill: { color: YELBOX }, line: { color: PURPLE, width: 1.25 },
});
s.addText("Pre processing", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.72,
  align: "center", valign: "middle",
  fontSize: 23, bold: true, color: BLACK, fontFace: FONT, margin: 0,
});

// Header line (multi-run, no bullet options): 'Preprocessing is' bold red
// + 'Problem dependent and data dependent' bold italic underlined black
s.addText(
  [
    { text: "Preprocessing is", options: { bold: true, color: HDRRED, fontFace: FONT } },
    { text: " Problem dependent and data dependent", options: { bold: true, italic: true, underline: true, color: BLACK, fontFace: FONT } },
  ],
  {
    x: 1.35, y: 1.98, w: 10.2, h: 0.45, align: "left", valign: "middle",
    fontSize: 20, margin: 0,
  }
);

// Body lines: one text box per line (bullet-bug workaround: manual "• " glyphs)
// Judge A1 (old-numbering run): original list is compact, upper-left — smaller type,
// tight spacing.
const LX = 1.35; // list left edge (x ~12% of slide)
function line(y, txt, opts) {
  s.addText(txt, Object.assign({
    x: LX, y, w: 9.8, h: 0.34, align: "left", valign: "middle",
    fontSize: 15, color: BLACK, fontFace: FONT, margin: 0,
  }, opts));
}

line(2.55, "It may include:", { bold: true, fontSize: 17 });
line(2.92, "Gap filling", {}); // plain, unbulleted
const bullets = [
  "Thinning",
  "Contour",
  "Binarization",
  "Noise Removal",
  "Color to Gray",
  "Opening touched points",
  "Resizing",
  "Normalization",
  "......",
];
let by = 3.27;
for (const b of bullets) {
  s.addText("\u2022 " + b, {
    x: LX + 0.15, y: by, w: 9.6, h: 0.30, align: "left", valign: "middle",
    fontSize: 15, color: BLACK, fontFace: FONT, margin: 0,
  });
  by += 0.32;
}

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_031_recreated.pptx" }).then(() => console.log("done"));
