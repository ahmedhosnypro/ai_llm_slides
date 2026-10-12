# Swoosh delta evidence — slide 017 (banked by resume worker 2, 2026-10-12 ~07:15)

FINDING: the return arrow ("swoosh") in THIS frame (002 slide_017.jpg) differs
structurally from the parent's certified swoosh image (001 slide_043 component):

1. COLOR: frame stroke core = #C10002 (bright red, C00000 family; darkest sample
   (186,0,0); arrowhead (195,0,8)). Parent render core = #840E07 (dark red 8B1A10
   family, darkest (126,2,0)). Measured along matched sample points with the same
   probe (see probe outputs in this dir; scripts probe5/probe2 + inline scans).

2. PATH/EXTENT: frame centerline (slide coords, 1px=1pt):
   tail (550,455) -> hook bottom (565,461) -> (600,445) -> (660,416) -> (700,396)
   -> (745,374) -> (772,358); head triangle solid ink at (775..800, 333..356),
   pointing up-right (~27 deg above horizontal; ~63 deg pptxgenjs rotate for a
   default up-triangle). Stroke vertical extent ~6-8 px (n=6-8 red px per column).
   The parent's swoosh image box is (585..760, 325..475) — the frame's head reaches
   x~800, i.e. ~40 px further right; the frame's tail reaches x~550 with a small
   downward hook at x565.

3. LABEL: «"H" Heads» rides the stripe's upper side at the SAME position in BOTH
   lectures (sheet s8: both bands, ~30-35 deg CCW ascending, BOTTOM ~10-15 px lower
   within band). Keep the parent hlabel box geometry (612,392,96x16, rotate 322)
   with the literal quoted text (already implemented in the build script).

PREPARED PATCH (apply to recreated_pptx/build/slide_017.js if the judge flags the
swoosh, or proactively in the next fix cycle):

  1) add "swoosh" to the opts.skip list in the renderBase call;
  2) draw before the label text block:

```js
// ---- delta 6: swoosh arrow redrawn (bright red + longer head, measured) ----------
const sw = "C00000";
const segs = [
  [568, 460, 620, 436],
  [620, 436, 700, 396],
  [700, 396, 770, 361],
];
for (const [x1, y1, x2, y2] of segs) {
  slide.addShape(pptx.ShapeType.line, {
    x: px(x1), y: px(y1), w: px(x2 - x1), h: px(y2 - y1),
    line: { color: sw, width: 7 },
  });
}
// tail hook (down-curl at the arrow's start)
slide.addShape(pptx.ShapeType.line, {
  x: px(552), y: px(452), w: px(16), h: px(9),
  line: { color: sw, width: 7 },
});
// head triangle pointing up-right (~27 deg above horizontal)
slide.addShape(pptx.ShapeType.triangle, {
  x: px(774), y: px(334), w: px(24), h: px(20), rotate: 63,
  fill: { color: sw }, line: { type: "none" },
});
```

Provenance: PIL probes banked in this dir (verify_resume.py, probe2..7.py,
fidelity_diff_render1.py + their stdout captures in swoosh_probe_outputs.txt);
sheet reads s6b_bottomright.txt (legend/wochips inherited-identical),
s8_swooshlabel.txt (label position/text both bands), an_zS5.txt, an_rightswoosh.txt.
