// build/slide_015.js — slide 015 "Encoder – Decoder Transformer" (child of 14).
//
// DEPENDENCY CONTRACT: requires the CERTIFIED parent component
// components/slide_014.js and draws ONLY this slide's delta at the frame's own
// measured geometry (scratch/slide015/measure1-4.py + recolor2.py + verify_asset.py):
//   inherited  : title, left_panel, left_figure (pixel-identical to slide 14's frame,
//                left-region mean|diff| vs slide_014.jpg = 0.97), house chrome (numeral 15)
//   removed    : arc, right_panel, right_figure, red_caption, blue_takeaway
//   delta      : right panel = white card with 2pt green border (stroke cols 572-574 /
//                893-895, rows 104-106 / 523-525 -> centerline rect 573,105,321,419,
//                border #00B050); inside it the RECOLORED paper Figure 1
//                (founder mandate: downloaded arXiv image, recolored per the frame —
//                encoder column shaded peach FDEDDD, decoder column shaded mint
//                CEFFE1, per-box tint remaps measured from the frame, background
//                fields traced from the frame at class agreement 0.999, asset
//                PIL-verified dark-ink IoU 0.579); red gutter block arrow
//                (shaft x[458,512] y[300,313] + head base x512 y[295,318] tip (525,306.5),
//                600dpi PNG, exact size); two small red data-flow up-arrows
//                (x[654,666] y[487,513] and x[740,750] y[116,140]); headers
//                "Encoder" (#C00000) / "Decoder" (#00A651) Arial bold italic 16pt
//                (frame ink widths 66/67 px at cap band y116..128).
//
// LAWS honored: parent component imported, never re-derived (dependencies.md);
// founder figure-image mandate (001_transformers_part1/AGENTS.md); verbatim labels
// come from the paper figure itself; margin:0 + explicit fontFace on text; no '#'
// in hex; single-version deliverable (no equations -> no OMML pass).

const path = require("path");
const pptxgen = require("pptxgenjs");
const parent = require(path.join(__dirname, "components", "slide_014.js"));

const ASSETS = path.join(__dirname, "assets");
const px = (v) => v / 72;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
const slide = pres.addSlide();

// ---- base: parent certified composition, minus the replaced right half ---------
parent.renderBase(pres, slide, {
  numeral: 15,
  skip: ["arc", "right_panel", "right_figure", "red_caption", "blue_takeaway"],
});

// ---- delta: right half ----------------------------------------------------------
// right panel card: white fill, 2pt green border
slide.addShape(pres.ShapeType.rect, {
  x: px(573), y: px(105), w: px(321), h: px(419),
  fill: { color: "FFFFFF" },
  line: { color: "00B050", width: 2 },
});

// recolored Figure 1 (600dpi canvas: shading fields baked in, paper figure on top)
slide.addImage({
  path: path.join(ASSETS, "slide015_fig1_color.png"),
  x: px(575), y: px(107), w: px(318), h: px(416),
});

// red transition block arrow in the gutter (600dpi PNG at exact size)
slide.addImage({
  path: path.join(ASSETS, "slide015_blockarrow.png"),
  x: px(458), y: px(295), w: px(68), h: px(24),
});

// small red data-flow up-arrows (600dpi PNGs at exact size)
slide.addImage({
  path: path.join(ASSETS, "slide015_up1.png"),
  x: px(654), y: px(487), w: px(13), h: px(27),
});
slide.addImage({
  path: path.join(ASSETS, "slide015_up2.png"),
  x: px(740), y: px(116), w: px(11), h: px(25),
});

// Encoder / Decoder headers (the only italics on the slide)
slide.addText("Encoder", {
  x: px(583), y: px(112), w: px(110), h: px(20),
  align: "left", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 16, bold: true, italic: true, color: "C00000",
});
slide.addText("Decoder", {
  x: px(769), y: px(111), w: px(117), h: px(20),
  align: "right", valign: "middle", margin: 0,
  fontFace: "Arial", fontSize: 16, bold: true, italic: true, color: "00A651",
});

pres.writeFile({ fileName: path.join(__dirname, "..", "slide_015_recreated.pptx") })
  .then(() => console.log("WROTE slide_015_recreated.pptx"))
  .catch((e) => { console.error(e); process.exit(1); });
