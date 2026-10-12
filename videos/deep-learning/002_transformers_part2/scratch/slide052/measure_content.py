#!/usr/bin/env python3
"""Measure slide_052 content elements via color masks + connected components.
Frame->slide mapping: slide_x = (fx-18.63)/0.96123, slide_y = fy/0.95556.
Print bboxes in FRAME px and mapped SLIDE pt.
"""
from PIL import Image
import numpy as np
from scipy import ndimage

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_052.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]

def to_slide_bbox(y0, y1, x0, x1):
    sx0 = (x0 - 18.63) / 0.96123; sx1 = (x1 - 18.63) / 0.96123
    sy0 = y0 / 0.95556; sy1 = y1 / 0.95556
    return sx0, sy0, sx1, sy1

def blobs(mask, min_px=30):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px:
            continue
        out.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
    return sorted(out, key=lambda t: (t[1], t[0]))

def show(name, bl, limit=40):
    print(f"== {name} ({len(bl)}) ==")
    for (x0, y0, x1, y1, npx) in bl[:limit]:
        sx0, sy0, sx1, sy1 = to_slide_bbox(y0, y1, x0, x1)
        print(f"  frame x{x0}..{x1} y{y0}..{y1} ({npx}px) -> slide x{sx0:.1f}..{sx1:.1f} y{sy0:.1f}..{sy1:.1f}")

def near(hexc, tol=40):
    hr = int(hexc[1:3], 16); hg = int(hexc[3:5], 16); hb = int(hexc[5:7], 16)
    return (abs(r - hr) < tol) & (abs(g - hg) < tol) & (abs(b - hb) < tol)

# containers
beige = near("#D8C8A8", 35)
ys, xs = np.where(beige)
print("BEIGE upper container frame bbox:", xs.min(), ys.min(), xs.max(), ys.max(),
      "-> slide", [f"{v:.1f}" for v in to_slide_bbox(ys.min(), ys.max(), xs.min(), xs.max())])

pink = near("#FFE1EE", 28)
ys, xs = np.where(pink)
print("PALEPINK lower container frame bbox:", xs.min(), ys.min(), xs.max(), ys.max(),
      "-> slide", [f"{v:.1f}" for v in to_slide_bbox(ys.min(), ys.max(), xs.min(), xs.max())])

# dark red bars 990000
show("DARKRED 990000 blobs", blobs(near("#990000", 38), 300))
# green FFN 00A800
show("GREEN 00A800 blobs", blobs(near("#00A800", 45), 200))
# royal blue 0010C8
show("BLUE 0010C8 blobs", blobs(near("#0010C8", 45), 300))
# purple 800080
show("PURPLE 800080 blobs", blobs(near("#800080", 45), 200))
# pale green word boxes C8E8C8
show("PALEGREEN C8E8C8 blobs", blobs(near("#C8E8C8", 25), 150))
# magenta border E040E0
show("MAGENTA E040E0 blobs", blobs(near("#E040E0", 55), 150))
# token squares yellow FFFF99 / pink FFA6B9
show("TOKYEL FFFF99 blobs", blobs(near("#FFFF99", 30), 8), 60)
show("TOKPINK FFA6B9 blobs", blobs(near("#FFA6B9", 30), 8), 60)
# circles K red FF0000, V green 00CC00, Q blue 0000FF
show("RED FF0000 blobs", blobs(near("#FF0000", 60), 30), 25)
show("GREEN00CC 00CC00 blobs", blobs(near("#00CC00", 45), 30), 25)
show("BLUE0000FF blobs", blobs(near("#0000FF", 55), 30), 25)
# pink output arrow FF9EB5
show("OUTPINK FF9EB5 blobs", blobs(near("#FF9EB5", 35), 30))
