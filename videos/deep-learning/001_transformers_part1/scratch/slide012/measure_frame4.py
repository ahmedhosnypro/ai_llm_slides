#!/usr/bin/env python3
"""Measure pass 4: precise highlight boxes, border cores, mapping least-squares."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_012.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(float)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = (r * 299 + g * 587 + b * 114) / 1000

print("== raw 1px border cores ==")
for y in [52, 53]:
    row = a[y, 300:500]
    i = np.argmin(row.sum(axis=1))
    print(f"  top y={y}: darkest px {row[i].astype(int)} at x={300+i}")
for x in [93, 94, 796, 797]:
    col = a[100:500, x]
    i = np.argmin(col.sum(axis=1))
    print(f"  col x={x}: darkest px {col[i].astype(int)} at y={100+i}")
for y in [524, 525]:
    row = a[y, 300:500]
    i = np.argmin(row.sum(axis=1))
    print(f"  bottom y={y}: darkest px {row[i].astype(int)} at x={300+i}")

def box_stats(x0, x1, y0, y1, name):
    reg = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    rl = (reg[:, 0] * 299 + reg[:, 1] * 587 + reg[:, 2] * 114) / 1000
    # interior: pixels within 60 lum of the 80th percentile (background of box)
    bg = np.percentile(rl, 80)
    interior = reg[np.abs(rl - bg) < 25]
    ink = reg[rl < np.percentile(rl, 2)]
    print(f"  {name}: interior median {np.median(interior, axis=0).astype(int)}"
          f" n={len(interior)}/{len(reg)}; darkest 2% median {np.median(ink, axis=0).astype(int)}")
    return np.median(interior, axis=0), np.median(ink, axis=0)

print("== highlight boxes: interior + ink-under ==")
box_stats(280, 330, 168, 176, "pink1 Vaswani (upper band, no text)")
box_stats(270, 345, 175, 184, "pink1 Vaswani full")
box_stats(395, 450, 175, 184, "pink1 Shazeer full")
box_stats(500, 575, 175, 184, "pink1 Parmar full")
box_stats(600, 690, 175, 184, "pink1 Uszkoreit full")
box_stats(255, 335, 235, 244, "pink2 Jones full")
box_stats(575, 640, 235, 244, "pink2 Kaiser full")
box_stats(340, 590, 56, 62, "tan title (top pad band)")
box_stats(340, 590, 75, 82, "tan title (bottom pad band)")
box_stats(100, 135, 190, 300, "tan date band (x100-135)")

print("== watermark glyphs under tan date band: darkest 3% in x108-140 y200-310 ==")
reg = a[200:311, 108:141].reshape(-1, 3)
rl = (reg[:, 0] * 299 + reg[:, 1] * 587 + reg[:, 2] * 114) / 1000
ink = reg[rl < np.percentile(rl, 3)]
print("  darkest 3% median:", np.median(ink, axis=0).astype(int), "n=", len(ink))
print("  (plain watermark glyph below tan, y330-523 x110-140) darkest 3%:")
reg2 = a[330:524, 110:141].reshape(-1, 3)
rl2 = (reg2[:, 0] * 299 + reg2[:, 1] * 587 + reg2[:, 2] * 114) / 1000
ink2 = reg2[rl2 < np.percentile(rl2, 3)]
print("   ", np.median(ink2, axis=0).astype(int), "n=", len(ink2))

print("== pink box precise bounds (core mask) ==")
def bounds(x0, x1, y0, y1, core, tol, name):
    reg = a[y0:y1, x0:x1]
    d = np.abs(reg - np.array(core)).sum(axis=2)
    m = d < tol
    ys, xs = np.where(m)
    if len(ys) < 10:
        print(f"  {name}: no core px"); return
    print(f"  {name}: x[{x0+int(np.percentile(xs,2))},{x0+int(np.percentile(xs,98))}]"
          f" y[{y0+int(np.percentile(ys,2))},{y0+int(np.percentile(ys,98))}] n={len(ys)}")

bounds(255, 350, 160, 200, [243, 165, 247], 90, "pink1 Vaswani")
bounds(375, 470, 160, 200, [243, 165, 247], 90, "pink1 Shazeer")
bounds(485, 590, 160, 200, [243, 165, 247], 90, "pink1 Parmar")
bounds(590, 700, 160, 200, [243, 165, 247], 90, "pink1 Uszkoreit")
bounds(250, 350, 222, 252, [243, 165, 247], 90, "pink2 Jones")
bounds(565, 655, 222, 252, [243, 165, 247], 90, "pink2 Kaiser")
bounds(330, 605, 50, 88, [248, 215, 177], 60, "tan title")
bounds(88, 142, 180, 315, [249, 215, 178], 60, "tan date band")

print("== least-squares mapping (frame = s*page + o) ==")
# (frame_y_ink_center, page_y_ink_center)
pts_y = [
    (68.5, 447.0),    # title text center (tan box center vs page title center)
    (91.5, 537.5),    # rule center
    (165.5, 793.0),   # row1 names
    (192.0, 888.5),   # row1 emails
    (225.0, 1001.0),  # row2 names
    (251.0, 1093.0),  # row2 emails
    (282.5, 1208.5),  # row3 name
    (296.5, 1256.0),  # row3 email
    (345.0, 1427.5),  # Abstract heading
    (375.5, 1526.0),  # abstract line 1
    (518.0, 2029.5),  # abstract line 12
]
ys = np.array([p[0] for p in pts_y]); ps = np.array([p[1] for p in pts_y])
A = np.vstack([ps, np.ones_like(ps)]).T
(sy, oy), res, *_ = np.linalg.lstsq(A, ys, rcond=None)
pred = A @ np.array([sy, oy])
print(f"  s_y={sy:.5f} oy={oy:.2f} max|res|={np.abs(pred-ys).max():.2f}")
for (fy, py), pv in zip(pts_y, pred):
    print(f"    page {py:7.1f} -> frame {pv:6.1f} (measured {fy})")

pts_x = [
    (352.0, 882.0), (578.0, 1663.0),   # title
    (226.0, 450.0), (705.0, 2099.0),   # rule
    (259.0, 553.0), (692.0, 2067.0),   # row1 names
    (239.0, 488.0), (694.0, 2063.0),   # row1 emails
    (269.0, 600.0), (662.0, 1950.0),   # abstract block
]
xs_f = np.array([p[0] for p in pts_x]); xs_p = np.array([p[1] for p in pts_x])
A = np.vstack([xs_p, np.ones_like(xs_p)]).T
(sx, ox), *_ = np.linalg.lstsq(A, xs_f, rcond=None)
pred = A @ np.array([sx, ox])
print(f"  s_x={sx:.5f} ox={ox:.2f} max|res|={np.abs(pred-xs_f).max():.2f}")

print("== crop window (frame container border edges -> page coords) ==")
for name, fv in [("left x93.5", 93.5), ("right x796.5", 796.5), ("top y52.5", 52.5), ("bottom y524.5", 524.5)]:
    if "x" in name:
        print(f"  {name} -> page x {(fv-ox)/sx:.1f}")
    else:
        print(f"  {name} -> page y {(fv-oy)/sy:.1f}")
print("== page edges -> frame ==")
for name, pv in [("page x0", 0), ("page x2550", 2550), ("page y0", 0), ("page y3300", 3300)]:
    if "x" in name:
        print(f"  {name} -> frame x {pv*sx+ox:.1f}")
    else:
        print(f"  {name} -> frame y {pv*sy+oy:.1f}")
