#!/usr/bin/env python3
"""Pass 9: disambiguate brace/arrow/dot; all nabla squares; pink chain; labels;
green box exact geometry; panel border color sampling."""
from PIL import Image
import numpy as np
from scipy import ndimage

B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)
R, G, Bl = bi[:,:,0].astype(int), bi[:,:,1].astype(int), bi[:,:,2].astype(int)

print("== ROWS y344..370: reddish (R-G>35,R-B>30,R>140) x-extents in x495..920 ==")
reddish = (R - G > 35) & (R - Bl > 30) & (R > 140)
for y in range(344, 371):
    row = np.where(reddish[y, 495:920])[0]
    if len(row) >= 2:
        # find contiguous runs
        runs = []
        s = row[0]; p = row[0]
        for v in row[1:]:
            if v - p > 3:
                runs.append((s + 495, p + 495)); s = v
            p = v
        runs.append((s + 495, p + 495))
        print(f"  y{y}: n={len(row)} runs={runs}")

print("== CURL CHECK: reddish in x523..545 / x880..905, rows y335..353 ==")
for y in range(335, 354):
    l = np.where(reddish[y, 520:548])[0]
    r = np.where(reddish[y, 878:908])[0]
    print(f"  y{y}: left n={len(l)} {list(l+520) if 0<len(l)<8 else (f'{l.min()+520}..{l.max()+520}' if len(l) else '')} | right n={len(r)} {list(r+878) if 0<len(r)<8 else (f'{r.min()+878}..{r.max()+878}' if len(r) else '')}")

print("== NABLA squares: darkish (R<150,G<150,B<150) comps y368..400 x495..920 ==")
darkish = (R < 150) & (G < 150) & (Bl < 150)
sub = np.zeros_like(darkish); sub[368:400, 495:920] = darkish[368:400, 495:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 5:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
for x0, y0, x1, y1, area in res:
    print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== SQUARE shapes: sample colors at square centers vs panel ==")
centers = [510, 545, 578, 613, 647, 680, 714, 748, 782, 816, 853, 888]
for cx in centers:
    reg = bi[372:378, cx-3:cx+4].reshape(-1,3).mean(axis=0)
    reg2 = bi[386:392, cx-3:cx+4].reshape(-1,3).mean(axis=0)
    print(f"  cx{cx}: top({reg[0]:.0f},{reg[1]:.0f},{reg[2]:.0f}) bot({reg2[0]:.0f},{reg2[1]:.0f},{reg2[2]:.0f})")

print("== PINK chain row: pinkish (R-G>25, B-G>-25, R>200, G 160..220) comps y400..435 ==")
pinkish = (R - G > 25) & (R > 200) & (G > 150) & (G < 225) & (Bl > 150)
sub = np.zeros_like(pinkish); sub[400:435, 495:920] = pinkish[400:435, 495:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 15:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
for x0, y0, x1, y1, area in res:
    print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== GREEN boxes precise: light green fill (G-R>8, G>245) comps y450..495 ==")
greenf = (G - R > 8) & (G > 242) & (Bl - R > -5)
sub = np.zeros_like(greenf); sub[450:495, 490:920] = greenf[450:495, 490:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 40:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
for x0, y0, x1, y1, area in res:
    print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== GREEN box labels: dark-ish ink in y458..488 ==")
d2 = (R < 170) & (G < 190) & (Bl < 170)
sub = np.zeros_like(d2); sub[455:490, 490:920] = d2[455:490, 490:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 4:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
for x0, y0, x1, y1, area in res[:30]:
    print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")

print("== PANEL BORDER color samples ==")
print("  top border y313..315 at x=550,650,800,880:")
for x in (550, 650, 800, 880):
    print(f"    x{x}: {[tuple(int(v) for v in bi[y, x]) for y in (313, 314, 315)]}")
print("  bottom border y497..499 at x=550,700,850:")
for x in (550, 700, 850):
    print(f"    x{x}: {[tuple(int(v) for v in bi[y, x]) for y in (497, 498, 499)]}")
print("  left border x501..503 at y=340,430,470:")
for y in (340, 430, 470):
    print(f"    y{y}: {[tuple(int(v) for v in bi[y, x]) for x in (501, 502, 503)]}")
print("  right border x917..919 at y=340,430,470:")
for y in (340, 430, 470):
    print(f"    y{y}: {[tuple(int(v) for v in bi[y, x]) for x in (917, 918, 919)]}")

print("== UP ARROWS between green and pink rows: greenish vertical strokes y430..458 ==")
garr = (G - R > 20) & (G > 180) & (G - Bl > 15)
sub = np.zeros_like(garr); sub[430:460, 495:920] = garr[430:460, 495:920]
lab, n = ndimage.label(sub, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
res = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area >= 8:
        ys, xs = sl
        res.append((xs.start, ys.start, xs.stop, ys.stop, area))
res.sort()
for x0, y0, x1, y1, area in res[:20]:
    print(f"    x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0}) area={area}")
