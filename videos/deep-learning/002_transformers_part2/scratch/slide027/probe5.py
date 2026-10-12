#!/usr/bin/env python3
"""Probe 5: faint arc stroke hunt in wedges; color means; title color; spoke dots inside fill."""
import numpy as np
from PIL import Image
import math, json

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
H, W = r.shape
CX, CY = 577.2, 284.0

# --- faint warm hunt: any pixel with r-b>18 and r>170 and g<r-8, in annulus r 128..280,
# excluding chip bboxes, +w label bboxes, arrowhead bboxes
excl = [(694,171,762,220),(640,99,690,165),(566,75,588,142),(465,101,515,167),(718,273,785,295),
        (509,64,530,77),(626,64,648,77),(768,92,789,104),(816,222,838,231),
        (577,63,586,73),(681,91,688,101),(760,176,770,184),(470,92,477,102)]
def excluded(x, y):
    return any(x0-2 <= x <= x1+2 and y0-2 <= y <= y1+2 for (x0,y0,x1,y1) in excl)

warm = (r - b > 18) & (r > 170) & (g < r - 8)
ys, xs = np.where(warm)
pts = []
for y, x in zip(ys, xs):
    dx, dy = x - CX, CY - y
    d = math.hypot(dx, dy)
    if 128 <= d <= 285 and not excluded(x, y) and y > 45 and y < 470 and 310 < x < 930:
        a = math.degrees(math.atan2(dy, dx)) % 360
        pts.append((x, y, round(d), round(a, 1), tuple(int(v) for v in im[y, x])))
print("faint warm pts:", len(pts))
for p in pts[:80]:
    print(p)

# --- color means
def mean_of(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys): return None
    return [round(float(im[...,0][y0:y1,x0:x1][ys,xs].mean())), round(float(im[...,1][y0:y1,x0:x1][ys,xs].mean())), round(float(im[...,2][y0:y1,x0:x1][ys,xs].mean())), int(len(ys))]

blue = (b > 110) & (b - r > 40) & (b - g > 40)
redm = (r > 130) & (r - g > 55) & (r - b > 55)
green = (g > 100) & (g - r > 40) & (g - b > 40)
print("eq blue mean:", mean_of(blue, 82, 182, 217, 247))
print("eq red mean:", mean_of(redm, 82, 182, 217, 247))
print("eq green mean:", mean_of(green, 82, 182, 217, 247))
print("title red mean:", mean_of(redm, 62, 55, 310, 140))
print("label +w red mean:", mean_of(redm, 509, 64, 530, 77))
print("chip text green:", mean_of(green, 718, 273, 786, 296))
# spoke red dots (strict) in upper half
print("spoke-dot red mean:", mean_of(redm, 440, 60, 720, 285))

# --- dotted spokes INSIDE the fill? scan fill annulus r 20..120 for reddish
inner = []
for y in range(int(CY)-130, int(CY)+130):
    for x in range(int(CX)-130, int(CX)+130):
        d = math.hypot(x-CX, y-CY)
        if d <= 122:
            rr, gg, bb = im[y, x]
            if rr - gg > 25 and rr > 150:
                inner.append((x, y, round(d), (int(rr), int(gg), int(bb))))
print("reddish-in-fill:", len(inner), inner[:20])

# --- title color core
sub = im[59:80, 73:305]
sr, sg, sb = sub[...,0], sub[...,1], sub[...,2]
core = (sr > 140) & (sg < 90) & (sb < 90)
print("title red mean:", float(sr[core].mean()), float(sg[core].mean()), float(sb[core].mean()), int(core.sum()))
