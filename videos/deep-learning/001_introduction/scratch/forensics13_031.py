from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R - B > 40) & (R - G > 40) & (R > 90)
black = (R < 90) & (G < 90) & (B < 90)

print("=== bullet1 band y 300..326: red ink map, x 128..185 ===")
for y in range(300, 326):
    row = "".join("#" if red[y, x] else "." for x in range(128, 186))
    print(f"  y={y}: {row}")

print("=== bullet1: red per-row extents x 128..185 ===")
for y in range(300, 326):
    rr = np.where(red[y, 128:186])[0]
    if len(rr): print(f"  y={y}: x {128+rr[0]}..{128+rr[-1]} n={len(rr)}")

print("=== BLACK ink in bullet region x 100..130, y 298..365 ===")
m = black[298:366, 100:130]
rows = np.where(m.any(axis=1))[0]
if len(rows):
    print(f"  black ink bbox: x {100+np.where(m.any(axis=0))[0][0]}..{100+np.where(m.any(axis=0))[0][-1]}  y {298+rows[0]}..{298+rows[-1]}")
    for y in range(298, 366):
        rr = np.where(black[y, 100:130])[0]
        if len(rr): print(f"  y={y}: x {100+rr[0]}..{100+rr[-1]} n={len(rr)}")
else:
    print("  NO black ink in x 100..130, y 298..366")

print("=== bullet1 dot region color core: x 135..151, y 302..319 modal ===")
from collections import Counter
band = a[302:320, 135:152].reshape(-1, 3)
sel = band[band.sum(axis=1) < 450]
print("  modal:", Counter(map(tuple, sel)).most_common(5), "n=", len(sel))

print("=== bullet2 band y 336..362: red per-row extents x 128..185 ===")
for y in range(336, 362):
    rr = np.where(red[y, 128:186])[0]
    if len(rr): print(f"  y={y}: x {128+rr[0]}..{128+rr[-1]} n={len(rr)}")
m2 = black[336:362, 100:130]
rows2 = np.where(m2.any(axis=1))[0]
print("=== bullet2 black ink x100..130:", f"y {336+rows2[0]}..{336+rows2[-1]}" if len(rows2) else "NONE")
