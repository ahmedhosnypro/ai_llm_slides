#!/usr/bin/env python3
"""Pass 7: fine structure of the backprop panel — dark ink (nabla/text), red strokes,
white patches, box rows; sample clean patches to identify true fill color."""
from PIL import Image
import numpy as np
from scipy import ndimage

B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0], bi[:,:,1], bi[:,:,2]

print("== CLEAN PATCH SAMPLES (panel interior) ==")
for (x0, y0) in [(560, 320), (700, 320), (860, 320), (560, 400), (700, 400), (860, 400),
                 (560, 470), (700, 470), (860, 470), (520, 340), (900, 340), (510, 460)]:
    reg = bi[y0:y0+6, x0:x0+6].reshape(-1, 3).mean(axis=0)
    print(f"  ({x0},{y0}): mean ({reg[0]:.0f},{reg[1]:.0f},{reg[2]:.0f})")

print("== DARK INK (nabla symbols / text) in panel x490..920 y310..500 ==")
dark = (R < 110) & (G < 110) & (Bl < 110)
sub = np.zeros_like(dark); sub[310:500, 490:920] = dark[310:500, 490:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 8:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
print(f"  {len(res)} dark comps (area>=8):")
for x0, y0, x1, y1, area in res:
    print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== REDDISH (loose: R-G>40 & R-Bl>40) row bands in panel ==")
reddish = (R - G > 40) & (R - Bl > 40) & (R > 130)
rows = reddish[300:500, 495:920].sum(axis=1)
s = None
for i, v in enumerate(rows):
    if v >= 8 and s is None: s = i
    elif v < 8 and s is not None:
        print(f"    band y{s+300}..{i+300} peak={int(rows[s:i].max())}")
        s = None
if s is not None: print(f"    band y{s+300}..500 peak={int(rows[s:200].max())}")

print("== WHITE PATCHES inside panel (loose >242) ==")
white = (R > 242) & (G > 242) & (Bl > 242)
sub = np.zeros_like(white); sub[310:500, 490:920] = white[310:500, 490:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 30:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort(key=lambda z: (z[1], z[0]))
print(f"  {len(res)} white comps (area>=30):")
for x0, y0, x1, y1, area in res[:40]:
    print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== TEXT ROWS: 'Back Propagation' red text — cols at y340..370 x520..910 ==")
redstrong = (R > 150) & (G < 90) & (Bl < 90)
cols = redstrong[336:372, 500:920].sum(axis=0)
s = None
for i, v in enumerate(cols):
    if v >= 2 and s is None: s = i
    elif v < 2 and s is not None:
        print(f"    x{s+500}..{i+500}", end=" ")
        s = None
print()
