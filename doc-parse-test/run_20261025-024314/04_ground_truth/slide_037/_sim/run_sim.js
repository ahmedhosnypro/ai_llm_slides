// Run the frozen slide_037.js build under the stubbed pptxgenjs recorder.
// Prints a summary; full record -> draw_record.json (frame-px geometry).
"use strict";
const fs = require("fs");
const path = require("path");

globalThis.__PPTX_RECORD = [];

const GT = path.resolve(__dirname, "..");
require(path.join(GT, "slide_037.js"));

// flush the async writeFile stub then dump
setTimeout(() => {
  const rec = globalThis.__PPTX_RECORD;
  const toPx = (v) => (v === undefined ? null : Math.round(v * 72 * 100) / 100);
  const norm = (e) => {
    if (e.kind === "shape") {
      const o = e.opts || {};
      const fill = o.fill && typeof o.fill === "object" ? o.fill.color : o.fill;
      const lineC = o.line && o.line.color;
      return {
        kind: "shape",
        type: e.type,
        x: toPx(o.x), y: toPx(o.y), w: toPx(o.w), h: toPx(o.h),
        fill: fill || null,
        line: lineC || null,
        dash: (o.line && o.line.dashType) || null,
        rotate: o.rotate || null,
      };
    }
    const o = e.opts || {};
    const text = e.runs.map((r) => r.text).join(
      e.runs.some((r) => r.options && r.options.breakLine) ? "\n" : ""
    );
    return {
      kind: "text",
      text,
      x: toPx(o.x), y: toPx(o.y), w: toPx(o.w), h: toPx(o.h),
      fontSize: o.fontSize || (e.runs[0].options && e.runs[0].options.fontSize) || null,
      bold: o.bold === undefined ? (e.runs[0].options && e.runs[0].options.bold) || false : o.bold,
      color: o.color || (e.runs.map((r) => r.options && r.options.color).find(Boolean)) || null,
      fontFace: o.fontFace || null,
      align: o.align || null,
      rotate: o.rotate || null,
    };
  };
  const out = rec.map(norm);
  fs.writeFileSync(path.join(__dirname, "draw_record.json"), JSON.stringify(out, null, 1));
  const shapes = out.filter((e) => e.kind === "shape");
  const texts = out.filter((e) => e.kind === "text");
  console.log("record events:", rec.length, "shapes:", shapes.length, "textCalls:", texts.length);
  const typeCount = {};
  for (const s of shapes) typeCount[s.type] = (typeCount[s.type] || 0) + 1;
  console.log("shape types:", JSON.stringify(typeCount));
  const palette = new Set();
  for (const s of shapes) { if (s.fill) palette.add(s.fill); if (s.line) palette.add(s.line); }
  for (const t of texts) if (t.color) palette.add(t.color);
  console.log("palette size:", palette.size, JSON.stringify([...palette].sort()));
  console.log("--- text items (text | x,y w,h px | size) ---");
  for (const t of texts)
    console.log(`${JSON.stringify(t.text)} | ${t.x},${t.y} ${t.w}x${t.h} | ${t.fontSize}pt bold=${t.bold} color=${t.color}`);
}, 300);
