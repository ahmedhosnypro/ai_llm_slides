#!/usr/bin/env python3
"""Pass 10: nabla square borders; blue curve wide search; square size gradient."""
from PIL import Image
import numpy as np
from scipy import ndimage

B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0].astype(int), bi[:,:,1].astype(int), bi[:,:,2].astype(int)

print("== BLUISH wide search (curve) x395..720 y150..345 ==")
bluish = (Bl - R > 25) & (Bl - G > 12) & (Bl > 120) & (R < 220)
sub = np.zeros_like(bluish); sub[150:345, 395:720] = bluish[150:345, 395:720]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 10:
        ys, xs = sl
        res.append((area, xs.start, ys.start, xs.stop, ys.stop))
res.sort(reverse=True)
for area, x0, y0, x1, y1 in res[:15]:
    print(f"  area={area:5d} x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0})")

print("== VERTICAL profile x=859 (big square) y360..405 ==")
for y in range(360, 406):
    r, g, b = bi[y, 859]
    print(f"  y{y}: ({r},{g},{b})", end="  ")
    if (y-359) % 3 == 0: print()
print()
print("== VERTICAL profile x=537 (small square) y360..405 ==")
for y in range(360, 406):
    r, g, b = bi[y, 537]
    print(f"  y{y}: ({r},{g},{b})", end="  ")
    if (y-359) % 3 == 0: print()
print()
print("== HORIZONTAL profile y=371 (above nablas) x495..915 — find square top borders ==")
row = bi[371, 495:915]
dark = [(495+i, tuple(int(v) for v in row[i])) for i in range(len(row)) if row[i].sum() < 630]
print("  px with sum<630:", dark[:60])
print("== HORIZONTAL profile y=396 (below nablas) x495..915 — find square bottom borders ==")
row = bi[396, 495:915]
dark = [(495+i, tuple(int(v) for v in row[i])) for i in range(len(row)) if row[i].sum() < 630]
print("  px with sum<630:", dark[:60])
