#!/usr/bin/env python3
"""Measure content ink in slide_042.jpg: title, label boxes, cubes, arrows.
Outputs color-class connected components with bboxes (frame px, 1px=1pt frame space).
Mapping to slide space: slide_x=(fx-18.63)/0.96123, slide_y=fy/0.95556 (from slide_002)."""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def map_slide(x, y):
    return (x - 18.63) / 0.96123, y / 0.95556

def comps(mask, min_px=8):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_px: continue
        out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), len(xs)))
    return out

def show(name, boxes, region=None):
    print(f"--- {name}: {len(boxes)} comps")
    for x0, y0, x1, y1, n in sorted(boxes, key=lambda t: (t[1], t[0])):
        sx0, sy0 = map_slide(x0, y0); sx1, sy1 = map_slide(x1, y1)
        print(f"  f({x0},{y0})..({x1},{y1}) w{x1-x0+1} h{y1-y0+1} n{n}  -> slide ({sx0:.1f},{sy0:.1f})..({sx1:.1f},{sy1:.1f})")

# restrict to content area inside blue frame, above letterbox
Y0, Y1 = 44, 517

# TITLE: red ink in y 44..132 (above blue frame top 133)
m = np.zeros((H, W), bool)
red = (r > 130) & (r - g > 60) & (r - b > 60)
m[Y0:132, 100:880] = red[Y0:132, 100:880]
ys, xs = np.nonzero(m)
print(f"TITLE ink frame bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
sx0, sy0 = map_slide(xs.min(), ys.min()); sx1, sy1 = map_slide(xs.max(), ys.max())
print(f"TITLE slide bbox ({sx0:.1f},{sy0:.1f})..({sx1:.1f},{sy1:.1f}) w {sx1-sx0:.1f} h {sy1-sy0:.1f}")
# per-row profile to see single line vs two lines
rows = m.sum(axis=1)
print("title row ink (y, count):", [(y, int(rows[y])) for y in range(Y0, 132) if rows[y] > 0])

# RED BORDER rectangles of label boxes: red in y 150..270 (between blue top and cubes)
m = np.zeros((H, W), bool)
m[150:275, 60:890] = red[150:275, 60:890]
show("RED in y150..275 (label box borders + text)", comps(m, 4))

# GREEN cubes: g dominant
green = (g > 110) & (g - r > 40) & (g - b > 60)
m = np.zeros((H, W), bool)
m[150:520, 60:890] = green[150:520, 60:890]
show("GREEN comps (cubes)", comps(m, 30))

# OTHER layer colors in right region x>580, y>200
def near(c, tol=45):
    return (abs(r - c[0]) < tol) & (abs(g - c[1]) < tol) & (abs(b - c[2]) < tol)
for name, c in [("magenta", (204, 0, 204)), ("yellow", (255, 215, 0)), ("orange", (255, 127, 0)),
                ("blue", (68, 119, 170))]:
    m = np.zeros((H, W), bool)
    m[200:520, 560:900] = near(c)[200:520, 560:900]
    show(name.upper(), comps(m, 50))
# distinct green of layers vs cube green
m = np.zeros((H, W), bool)
m[200:520, 560:900] = green[200:520, 560:900]
show("GREEN in right region", comps(m, 50))
