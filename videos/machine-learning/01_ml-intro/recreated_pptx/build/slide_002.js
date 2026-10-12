// Build: slide 002 recreation — "Artificial Intelligence" hierarchy diagram
// Spec: analysis/slide_002_final.json (validated PASS_WITH_FIXES)
// Output: recreated_pptx/slide_002_recreated.pptx
const pptxgenpkg = require("pptxgenjs");

const pptx = new pptxgenpkg();
pptx.layout = "LAYOUT_WIDE"; // 13.33 x 7.5 in
const W = 13.33, H = 7.5;

// Palette (from spec colors) — NO '#' prefixes (corrupts file)
const BG = "E8E8E8";      // slide background light gray
const MAROON = "8B2A3A";  // border frame (superseded by house RED below)
const RED = "C00000";     // house frame / title red (founder directive 2026-10-09)
const PARENT = "8B0000";  // dark red parent box
const BLUE = "00008B";   // left child box (spec value; judges 2b/3b contradicted — keep spec)
const GREEN = "2E8B2E";  // right child box (judge 2b: slightly lighter than 1E7B1E)
const ARROW = "CC0000";   // red arrows
const YELLOW = "F5E97B";  // slide-number badge (superseded by house badge)
const WHITE = "FFFFFF";
const BLACK = "000000";

const FONT = "Arial";

let s = pptx.addSlide();
s.background = { color: BG };

// 1. House outer red frame: 0.15in inset from every edge (founder directive)
s.addShape(pptx.shapes.RECTANGLE, {
  x: 0.15, y: 0.15, w: W - 0.3, h: H - 0.3,
  fill: { color: BG }, line: { color: RED, width: 1.5 },
});

// 1b. House slide title at y=0.28 (slide had no separate title element)
s.addText("Artificial Intelligence", {
  x: 0.6, y: 0.28, w: 12.13, h: 0.6, align: "center", valign: "top",
  fontSize: 30, bold: true, color: RED, fontFace: FONT, margin: 0,
});

// 2. Slide-number badge: house geometry/colors, numeral '2' = slide id
s.addShape(pptx.shapes.OVAL, {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  fill: { color: "FFF9C4" }, line: { color: "FFF9C4", width: 0.5 },
});
s.addText("2", {
  x: 12.48, y: 0.30, w: 0.5, h: 0.5,
  align: "center", valign: "middle", fontSize: 18, bold: true,
  color: "333333", fontFace: FONT, margin: 0,
});

// 3. Parent node: dark red box ~35% W x ~12% H, centered, spanning ~28-40% y
const parent = { x: 0.325 * W, y: 0.28 * H, w: 0.35 * W, h: 0.12 * H };
s.addShape(pptx.shapes.RECTANGLE, {
  x: parent.x, y: parent.y, w: parent.w, h: parent.h,
  fill: { color: PARENT },
});
s.addText("Artificial Intelligence", {
  x: parent.x, y: parent.y, w: parent.w, h: parent.h,
  align: "center", valign: "middle", fontSize: 24, bold: true,
  color: WHITE, fontFace: FONT, margin: 0,
});

// 4. Child nodes: compacted per judge consensus (3b/5: over-spread, children
//    should sit closer to the parent) — 24% W each, symmetric about center
const childW = 0.24 * W, childH = 0.12 * H, childY = 0.52 * H;
const leftChild = { x: 3.30, y: childY, w: childW, h: childH };    // center 4.90
const rightChild = { x: 6.83, y: childY, w: childW, h: childH };   // center 8.43

s.addShape(pptx.shapes.RECTANGLE, {
  x: leftChild.x, y: leftChild.y, w: leftChild.w, h: leftChild.h,
  fill: { color: BLUE },
});
s.addText([
  { text: "Rule Based", options: { breakLine: true } },
  { text: "(Expert Systems)", options: {} },
], {
  x: leftChild.x, y: leftChild.y, w: leftChild.w, h: leftChild.h,
  align: "center", valign: "middle", fontSize: 18, bold: true,
  color: WHITE, fontFace: FONT, margin: 0,
});

s.addShape(pptx.shapes.RECTANGLE, {
  x: rightChild.x, y: rightChild.y, w: rightChild.w, h: rightChild.h,
  fill: { color: GREEN },
});
s.addText([
  { text: "Data Based", options: { breakLine: true } },
  { text: "(Machine Learning)", options: {} },
], {
  x: rightChild.x, y: rightChild.y, w: rightChild.w, h: rightChild.h,
  align: "center", valign: "middle", fontSize: 18, bold: true,
  color: WHITE, fontFace: FONT, margin: 0,
});

// 5. Connectors: central trunk + symmetric curved branches (judge 5: the
//    original has a short central drop from the parent bottom-center that
//    then splits into two curved branches; thin ~1 pt red #CC0000,
//    arrowheads pointing into the child boxes).
const startX = parent.x + parent.w / 2;      // 6.665
const startY = parent.y + parent.h;          // 3.00
const leftEndX = leftChild.x + childW / 2;    // 4.90
const rightEndX = rightChild.x + childW / 2; // 8.43
const endY = childY;                         // 3.90
const trunkEndY = startY + 0.45;             // 3.45

// Central trunk: short vertical drop from the parent bottom-center
s.addShape(pptx.shapes.LINE, {
  x: startX, y: startY, w: 0, h: trunkEndY - startY,
  fill: { type: "none" },
  line: { color: ARROW, width: 1 },
});
// Left branch: smooth curve from the trunk end down-left into the left
// child top-center, arrowhead at the child end
s.addShape("curvedConnector2", {
  x: leftEndX, y: trunkEndY, w: startX - leftEndX, h: endY - trunkEndY,
  flipH: true,
  fill: { type: "none" },
  line: { color: ARROW, width: 1, endArrowType: "triangle" },
});
// Right branch: smooth curve from the trunk end down-right into the
// right child top-center, arrowhead at the child end
s.addShape("curvedConnector2", {
  x: startX, y: trunkEndY, w: rightEndX - startX, h: endY - trunkEndY,
  fill: { type: "none" },
  line: { color: ARROW, width: 1, endArrowType: "triangle" },
});

pptx.writeFile({ fileName: "videos/ml-intro/recreated_pptx/slide_002_recreated.pptx" })
  .then(() => console.log("done"));
