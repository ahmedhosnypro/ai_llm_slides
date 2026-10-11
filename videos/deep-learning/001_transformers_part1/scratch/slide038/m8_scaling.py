#!/usr/bin/env python3
"""m8: compare Scaling box + fraction geometry between slide_037 and slide_038
frames; measure exact bboxes in slide_038 (ground truth for this build)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
a38 = np.asarray(Image.open(f"{V}/unique_slides/slide_038.jpg").convert("RGB")).astype(int)
a37 = np.asarray(Image.open(f"{V}/unique_slides/slide_037.jpg").convert("RGB")).astype(int)

def yellow_bbox(a, x0, x1, y0, y1):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    yel = (R > 215) & (G > 200) & (B < 170) & (R - B > 60)
    m = np.zeros(yel.shape, bool); m[y0:y1, x0:x1] = yel[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(xs):
        return None
    return xs.min(), xs.max(), ys.min(), ys.max(), len(xs)

print("scaling-box yellow bbox 37:", yellow_bbox(a37, 355, 470, 150, 460))
print("scaling-box yellow bbox 38:", yellow_bbox(a38, 355, 470, 150, 460))

# red fraction: strong red pixels x[410..460] y[180..240]
def red_bbox(a, x0, x1, y0, y1):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    red = (R > 130) & (R - G > 60) & (R - B > 50)
    m = np.zeros(red.shape, bool); m[y0:y1, x0:x1] = red[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(xs):
        return None
    return xs.min(), xs.max(), ys.min(), ys.max(), len(xs)

print("fraction red bbox 37:", red_bbox(a37, 405, 465, 175, 245))
print("fraction red bbox 38:", red_bbox(a38, 405, 465, 175, 245))

# column profile of yellow in 38 at the box's left/right edges
R, G, B = a38[:, :, 0], a38[:, :, 1], a38[:, :, 2]
yel = (R > 215) & (G > 200) & (B < 170) & (R - B > 60)
cols = yel[150:460, 355:470].sum(axis=0)
print("38 yellow cols>30:", [(x + 355, int(c)) for x, c in enumerate(cols) if c > 30])
rows = yel[150:460, 355:470].sum(axis=1)
print("38 yellow rows>10:", [(y + 150, int(c)) for y, c in enumerate(rows) if c > 10])
# inner lighter rect (FFF069-ish) in 38: brighter yellow
yel2 = (R > 240) & (G > 225) & (B < 140)
m2 = np.zeros(yel2.shape, bool); m2[150:460, 355:470] = yel2[150:460, 355:470]
ys, xs = np.where(m2)
if len(xs):
    print("38 inner-bright bbox:", xs.min(), xs.max(), ys.min(), ys.max(), len(xs))

# rotated text ink inside the box in 38 (orange text)
txt = (R > 180) & (R - B > 80) & (G < 180) & (G - B > 20)
mt = np.zeros(txt.shape, bool); mt[150:460, 360:440] = txt[150:460, 360:440]
ys, xs = np.where(mt)
if len(xs):
    print("38 orange-text bbox in box:", xs.min(), xs.max(), ys.min(), ys.max(), len(xs))
