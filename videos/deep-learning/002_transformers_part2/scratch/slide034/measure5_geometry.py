#!/usr/bin/env python3
"""measure5_geometry.py — precise geometry: containers, boxes, purple bar, arrows,
brace, summary box. Masks + per-row/col profiles."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]

def bbox(mask, name, ymin=40, ymax=514, xmin=45, xmax=935):
    ys, xs = np.where(mask[ymin:ymax, xmin:xmax])
    if len(xs) == 0:
        print(f"{name}: EMPTY"); return None
    print(f"{name}: x {xs.min()+xmin}..{xs.max()+xmin}  y {ys.min()+ymin}..{ys.max()+ymin}  n={len(xs)}")
    return (xs.min()+xmin, xs.max()+xmin, ys.min()+ymin, ys.max()+ymin)

print("== 1. TOKEN-ROW CONTAINER ==")
# lavender-blue fill (192,192,240)bin
tokfill = (r > 175) & (r < 215) & (g > 175) & (g < 215) & (b > 225)
bbox(tokfill, "token fill (C0C0F0-class)", 125, 185)
# dash: dark blue-violet (96,96,168)bin
dash = (r > 80) & (r < 135) & (g > 80) & (g < 135) & (b > 150) & (b < 205)
bbox(dash, "token dash+border (6060A8-class)", 125, 185)
for y in range(130, 182):
    n = dash[y, 170:890].sum()
    if n > 5:
        xs = np.where(dash[y, 170:890])[0] + 170
        print(f"  dashrow y{y}: n={n} x {xs.min()}..{xs.max()}")

print("== 2. VECTOR-ROW CONTAINER ==")
vecfill = (r > 228) & (b > 228) & (g > 205) & (g < 242) & (r - g > 8)
bbox(vecfill, "vector fill (F0D8F0-class)", 285, 345)
for y in range(285, 345):
    n = vecfill[y, 170:890].sum()
    if n > 100:
        xs = np.where(vecfill[y, 170:890])[0] + 170
        print(f"  fillrow y{y}: n={n} x {xs.min()}..{xs.max()}")

print("== 3. VECTOR BOXES (pink fills + red borders) ==")
pink = (r > 225) & (r < 255) & (g > 150) & (g < 205) & (b > 170) & (b < 215)
bbox(pink, "pink box fill", 285, 345)
redb = (r > 140) & (g < 100) & (b < 110)
bbox(redb, "red in vector band", 295, 340)

print("== 4. PURPLE BAR ==")
purp = (r > 100) & (r < 190) & (g < 60) & (b > 100) & (b < 190)
bbox(purp, "purple bar", 200, 270)
for y in [216, 230, 250]:
    xs = np.where(purp[y, 100:900])[0] + 100
    print(f"  row y{y}: x {xs.min()}..{xs.max()} n={len(xs)}")

print("== 5. ARROWS ==")
red2 = (r > 150) & (g < 90) & (b < 90)
for y0, y1, nm in [(170, 220, "arrow1"), (248, 295, "arrow2")]:
    ys, xs = np.where(red2[y0:y1, 480:580])
    if len(xs):
        print(f"{nm}: y {ys.min()+y0}..{ys.max()+y0}  x {xs.min()+480}..{xs.max()+480}")

print("== 6. BRACE ==")
ys, xs = np.where(red2[330, :] if False else red2[332:362, 150:900])
if len(xs):
    print(f"brace red: y {ys.min()+332}..{ys.max()+332}  x {xs.min()+150}..{xs.max()+150}")
for y in range(334, 360):
    xs2 = np.where(red2[y, 150:900])[0] + 150
    if len(xs2) > 2:
        print(f"  brace y{y}: n={len(xs2)} x {xs2.min()}..{xs2.max()}")

print("== 7. SUMMARY BOX (green border) ==")
grn = (g > 100) & (g - r > 30) & (g - b > 30)
ys, xs = np.where(grn[355:512, 200:850])
if len(xs):
    print(f"green border: x {xs.min()+200}..{xs.max()+200}  y {ys.min()+355}..{ys.max()+355}")
# left/right border columns
for x in range(215, 840):
    n = grn[360:505, x].sum()
    if n > 60:
        print(f"  green col x{x}: n={n}")
