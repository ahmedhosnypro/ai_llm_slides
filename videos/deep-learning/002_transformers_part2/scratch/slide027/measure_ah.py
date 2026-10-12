#!/usr/bin/env python3
"""Arrowhead orientation at hi-res (decisive) + curated center map + equation advances + badge scale."""
import numpy as np
from PIL import Image

HI = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/hi_res_1545.png").convert("RGB")).astype(int)
S = 1280 / 960.0

# AH positions (960-scale curated): AH1 (766,180) phi30, AH2 (684.5,95.5) phi60, AH3 (581.5,67.5) phi90, AH4 (473.5,96) phi120
for nm, (cx9, cy9) in (("AH1 phi30", (766, 180)), ("AH2 phi60", (684.5, 95.5)), ("AH3 phi90", (581.5, 67.5)), ("AH4 phi120", (473.5, 96))):
    cx, cy = cx9 * S, cy9 * S
    print(f"== {nm} hi-res ASCII (x {int(cx)-14}..{int(cx)+14}, y {int(cy)-14}..{int(cy)+14}) '#'>60 '+'>30 '.'dark ==")
    for y in range(int(cy) - 14, int(cy) + 15):
        line = ""
        for x in range(int(cx) - 14, int(cx) + 15):
            c = HI[y, x]
            om = c[0] - (c[1] + c[2]) / 2.0
            dk = int(np.abs(c - np.array([233, 233, 231])).sum())
            line += "#" if om > 60 else ("+" if om > 30 else ("." if dk > 40 else " "))
        print(f"{y:4d} {line}")
    print()

CUR = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg").convert("RGB")).astype(int)
print("== curated center map x556..604 y252..318 ('@'dark 'o'warm '.'dark-ish) ==")
for y in range(252, 319, 2):
    line = ""
    for x in range(556, 605):
        c = CUR[y, x]
        dk = (233 - c[0]) + (233 - c[1]) + (231 - c[2])
        dark = c[0] < 140 and c[1] < 140
        warm = (int(c[0]) - int(c[2])) > 40 and c[0] > 180
        line += "@" if dark else ("o" if warm else ("." if dk > 25 else " "))
    print(f"{y:3d} {line}")

print("\n== curated equation box per-line ink ==")
for (y0, y1), nm in (((186, 206), "L1"), ((207, 226), "L2"), ((227, 244), "L3")):
    sub = CUR[y0:y1 + 1, 83:217]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    blue = (sb > 130) & (sr < 120) & (sg < 120)
    redt = (sr > 140) & (sg < 100) & (sb < 100) & (sr - sg > 60)
    grnt = (sg > 110) & (sg - sr > 40) & (sg - sb > 40)
    for m, cn in ((blue, "blue"), (redt, "red"), (grnt, "green")):
        ys, xs = np.where(m)
        if len(xs):
            print(f" {nm} {cn}: x {83+xs.min()}..{83+xs.max()} (w {xs.max()-xs.min()+1}) y {y0+ys.min()}..{y0+ys.max()} n={m.sum()}")

print("\n== badge numeral ink (curated) ==")
sub = CUR[57:86, 859:893]
dk = (sub[:, :, 0] < 150) & (sub[:, :, 1] < 150) & (sub[:, :, 2] < 150)
ys, xs = np.where(dk)
if len(ys):
    print(f"numeral ink: x {859+xs.min()}..{859+xs.max()} y {57+ys.min()}..{57+ys.max()} (h {ys.max()-ys.min()+1} w {xs.max()-xs.min()+1}) n={dk.sum()}")

print("\n== title line 3 'as angles' ink cols (advance check) ==")
tit = (CUR[:, :, 0] > 130) & (CUR[:, :, 1] < 80) & (CUR[:, :, 2] < 80)
band = tit[113:133, :]
xs = np.where(band.sum(axis=0) > 0)[0]
print(f"L3 x {xs.min()}..{xs.max()} w {xs.max()-xs.min()+1}")
band1 = tit[61:79, :]
xs1 = np.where(band1.sum(axis=0) > 0)[0]
print(f"L1 x {xs1.min()}..{xs1.max()} w {xs1.max()-xs1.min()+1}")
