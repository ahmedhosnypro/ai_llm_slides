#!/usr/bin/env python3
"""Diagnose right-block fit: side-by-side classified maps + disagreement map."""
from PIL import Image
import numpy as np
import importlib.util, sys, json

spec = importlib.util.spec_from_file_location("gen", "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide042/gen_diagrams.py")
# Instead of importing (it re-runs the fit), replicate the render here.
from PIL import ImageDraw
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
SS = 4
SLABS = [
    dict(name="magenta", front=(158, 0, 164), band=(79, 0, 82), gap=(196, 0, 205)),
    dict(name="green",   front=(133, 255, 13), band=(87, 100, 18), gap=(160, 255, 60)),
    dict(name="orange",  front=(236, 122, 7), band=(112, 58, 10), gap=(248, 150, 40)),
    dict(name="yellow",  front=(250, 255, 13), band=(191, 200, 11), gap=(255, 255, 90)),
    dict(name="blue",    front=(94, 125, 157), band=(41, 55, 64), gap=(130, 165, 195)),
]
RW, FH_R, P_R, BH_R, BW_R, Sh_R = 31, 27, 31.25, 15, 26, 14

def poly(d, pts, color):
    d.polygon([(x * SS, y * SS) for x, y in pts], fill=color)

def render_block(ox, oy, x0, Y0):
    cw = int(4 * ox + 124 + Sh_R + 30); ch = int(4 * -oy + BH_R + 4 * P_R + FH_R + 10)
    img = Image.new("RGB", (cw * SS, ch * SS), (255, 255, 255))
    d = ImageDraw.Draw(img)
    cx0 = x0 - 10; cy0 = Y0 + 4 * oy - BH_R - 6
    for k in range(4, -1, -1):
        s = SLABS[k]
        wx = x0 + k * ox; wy = Y0 + k * oy
        for r in range(4, -1, -1):
            Y = wy + r * P_R
            for c in range(4):
                xc = wx + c * RW
                poly(d, [(xc - cx0, Y - cy0), (xc + BW_R - cx0, Y - cy0),
                         (xc + BW_R + Sh_R - cx0, Y - BH_R - cy0), (xc + Sh_R - cx0, Y - BH_R - cy0)], s["band"])
                poly(d, [(xc + BW_R - cx0, Y - cy0), (xc + RW - cx0, Y - cy0),
                         (xc + RW + Sh_R - cx0, Y - BH_R - cy0), (xc + BW_R + Sh_R - cx0, Y - BH_R - cy0)], s["gap"])
            for c in range(4):
                xc = wx + c * RW
                d.rectangle([(xc - cx0) * SS, (Y - cy0) * SS, (xc + RW - cx0) * SS, (Y + FH_R - cy0) * SS], fill=s["front"])
    return img, cx0, cy0

def classify(a):
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    out = np.full(a.shape[:2], 7, dtype=np.uint8)
    m = (r > 235) & (g > 235) & (b > 230); out[m] = 0
    m = (r > 100) & (b > 100) & (g < 110); out[m] = 1
    m = (g > 140) & (g - r > 30) & (out == 0); out[m] = 2
    m = (g > 60) & (g - r > 10) & (g - b > 20) & (out == 0); out[m] = 2
    m = (r > 150) & (g > 60) & (g < 190) & (b < 100) & (out == 0); out[m] = 3
    m = (r > 170) & (g > 170) & (b < 140) & (out == 0); out[m] = 4
    m = (b > 80) & (b - r > 5) & (out == 0); out[m] = 5
    m = (r < 110) & (g < 110) & (b < 110) & (out == 0); out[m] = 6
    return out

CH = ".MGOYbK?"
orig = Image.open(FR).convert("RGB")
A = np.asarray(orig)

params = (17, -9, 654, 319)
img, cx0, cy0 = render_block(*params)
B = np.asarray(img.resize((img.width // SS, img.height // SS), Image.LANCZOS))
x0f, y0f = int(cx0), int(cy0)
h, w = B.shape[:2]
region = A[y0f:y0f + h, x0f:x0f + w]
ca, cb = classify(region), classify(B)
dis = (ca != cb)
print(f"region x{x0f}..{x0f+w-1} y{y0f}..{y0f+h-1}; disagreement {dis.sum()} ({100.0*dis.sum()/dis.size:.1f}%)")

step = 4
print("ORIG (frame):")
print("     " + "".join(str((x0f + i * step) % 10) for i in range((w + step - 1) // step)))
for yy in range(0, h, step):
    print(f"{y0f+yy:4d} " + "".join(CH[ca[yy, xx]] for xx in range(0, w, step)))
print("RENDER:")
print("     " + "".join(str((x0f + i * step) % 10) for i in range((w + step - 1) // step)))
for yy in range(0, h, step):
    print(f"{y0f+yy:4d} " + "".join(CH[cb[yy, xx]] for xx in range(0, w, step)))
