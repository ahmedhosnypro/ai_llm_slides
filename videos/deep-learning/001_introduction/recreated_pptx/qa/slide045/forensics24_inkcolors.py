#!/usr/bin/env python3
"""forensics24: what ink (red/dark/blue) actually forms the org connectors?"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
org = np.asarray(Image.open(VID + "/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = org[:, :, 0], org[:, :, 1], org[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)
dark = (r < 110) & (g < 110) & (b < 110)
blue = (b > 120) & (r < 110) & (g < 110)


def scan(name, m, x0, x1, y0, y1, excl=None):
    sub = m[y0:y1, x0:x1].copy()
    if excl:
        sub[:, excl[0] - x0: excl[1] - x0] = False
    ys, xs = np.where(sub)
    if not len(ys):
        print(f"{name}: none")
        return
    print(f"{name}: n={len(ys)} bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()}")
    for y in range(y0, y1):
        cols = list(np.where(m[y, x0:x1])[0] + x0)
        if excl:
            cols = [c for c in cols if not (excl[0] <= c <= excl[1])]
        if cols:
            print(f"  y{y}: {cols}")


print("== corridor A (Weights->theta) x698..738 y344..375, ALL inks (red R dark D blue B) ==")
for y in range(344, 375):
    row = ""
    for x in range(698, 738):
        row += "R" if red[y, x] else ("D" if dark[y, x] else ("B" if blue[y, x] else "."))
    if "#" in row or "R" in row or "D" in row or "B" in row:
        print(f"  y{y} {row}")

print("== blob zoom x686..712 y340..360 (R/D/B) ==")
for y in range(340, 360):
    row = ""
    for x in range(686, 712):
        row += "R" if red[y, x] else ("D" if dark[y, x] else ("B" if blue[y, x] else "."))
    print(f"  y{y} {row}")

scan("A-dark x640..745 y348..435", dark, 640, 745, 348, 435, excl=(696, 704))
scan("A-blue x640..745 y348..435", blue, 640, 745, 348, 435, excl=(696, 704))
scan("B-dark x640..745 y400..470", dark, 640, 745, 400, 470, excl=(696, 704))
scan("B-blue x640..745 y400..470", blue, 640, 745, 400, 470, excl=(696, 704))
scan("B-red wide x600..760 y395..475", red, 600, 760, 395, 475, excl=(696, 704))
