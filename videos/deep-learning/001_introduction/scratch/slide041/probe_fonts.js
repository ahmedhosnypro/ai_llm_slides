const pptxgen = require("pptxgenjs");
const p = new pptxgen();
p.layout = "LAYOUT_WIDE";
const s = p.addSlide();
s.background = { color: "FFFFFF" };
const rows = [
  ["A", "Times New Roman", 16, false, "h (-a:a , -b:b)"],
  ["B", "Times New Roman", 17, false, "h (-a:a , -b:b)"],
  ["C", "Times New Roman", 18, false, "h (-a:a , -b:b)"],
  ["D", "Times New Roman", 17, false, "I (x,y)"],
  ["E", "Times New Roman", 18, false, "I (x,y)"],
  ["F", "Times New Roman", 17, true,  "(odd dimension)"],
  ["G", "Times New Roman", 18, true,  "(odd dimension)"],
  ["H", "Times New Roman", 21.3, false, "Move the filter ONE pixel  (Right, Left, Up, Down) and Re-Calculate"],
  ["I", "Times New Roman", 21.5, false, "Move the filter ONE pixel  (Right, Left, Up, Down) and Re-Calculate"],
];
rows.forEach((r, i) => {
  s.addText(r[4], { x: 0.3, y: 0.3 + i * 0.45, w: 12.5, h: 0.4, align: "left", valign: "middle", margin: 0,
    fontFace: r[1], fontSize: r[2], bold: true, italic: r[3], color: "000000" });
});
p.writeFile({ fileName: "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/scratch/slide041/probe_fonts.pptx" })
  .then(() => console.log("ok"));
