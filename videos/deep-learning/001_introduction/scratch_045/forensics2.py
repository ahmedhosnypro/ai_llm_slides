#!/usr/bin/env python3
"""Forensics pass 2: relaxed border detection for definition/Remember/legend boxes;
sample border colors; starburst bbox; bottom bar."""
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# relaxed blue: anything clearly bluer than red/green
blue = (B - R > 25) & (B - G > 12) & (B > 110)
# relaxed red
red = (R - G > 35) & (R - B > 35) & (R > 110)

def runs(mask, axis, minlen):
    out = []
    if axis == 0:
        for y in range(H):
            xs = np.where(mask[y])[0]
            if len(xs) > minlen:
                d = np.split(xs, np.where(np.diff(xs) > 3)[0] + 1)
                seg = max(d, key=len)
                if len(seg) > minlen:
                    out.append((y, seg[0], seg[-1], len(seg)))
    else:
        for x in range(W):
            ys = np.where(mask[:, x])[0]
            if len(ys) > minlen:
                d = np.split(ys, np.where(np.diff(ys) > 3)[0] + 1)
                seg = max(d, key=len)
                if len(seg) > minlen:
                    out.append((x, seg[0], seg[-1], len(seg)))
    return out

print("== BLUE rows relaxed (>=150) ==")
prev = None
for y, x0, x1, n in runs(blue, 0, 150):
    if prev is None or y - prev > 2:
        print(f"y={y} x{x0}..{x1} n={n}")
    prev = y

print("\n== BLUE rows relaxed (>=60, y>250 excluded top boxes) ==")
prev = None
for y, x0, x1, n in runs(blue, 0, 60):
    if prev is None or y - prev > 2:
        print(f"y={y} x{x0}..{x1} n={n}")
    prev = y

print("\n== RED rows relaxed (>=150) ==")
prev = None
for y, x0, x1, n in runs(red, 0, 150):
    if prev is None or y - prev > 2:
        print(f"y={y} x{x0}..{x1} n={n}")
    prev = y

print("\n== RED vertical relaxed (>=40) ==")
prev = None
for x, y0, y1, n in runs(red, 1, 40):
    if prev is None or x - prev > 2:
        print(f"x={x} y{y0}..{y1} n={n}")
    prev = x

print("\n== BLUE vertical relaxed (>=20) ==")
prev = None
for x, y0, y1, n in runs(blue, 1, 20):
    if prev is None or x - prev > 2:
        print(f"x={x} y{y0}..{y1} n={n}")
    prev = x

# sample border colors at known lines
def sample(y0, y1, x0, x1):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    # modal color of non-white pixels
    nw = reg[(reg[:, 0] < 240) | (reg[:, 1] < 240) | (reg[:, 2] < 240)]
    if len(nw) == 0:
        return None
    modal = {}
    for px in nw[::1]:
        key = (px[0] // 16 * 16, px[1] // 16 * 16, px[2] // 16 * 16)
        modal[key] = modal.get(key, 0) + 1
    top = sorted(modal.items(), key=lambda kv: -kv[1])[:4]
    return top

print("\nborder color def-box top row region y~120 x100..500:", sample(118, 124, 150, 800))
print("border color remember-box row y~245 x100..800:", sample(243, 249, 150, 800))
print("equation panel border y291 x300..690:", sample(290, 293, 320, 680))
print("callout border y364 x740..890:", sample(363, 366, 750, 880))
print("legend box region sample y390..430 x70..260:", sample(388, 436, 72, 255))
