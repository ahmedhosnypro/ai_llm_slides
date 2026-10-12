#!/usr/bin/env python3
"""forensics23: org geometry for attempt-3 fixes.
A) callout connector lines (Weights->theta_ij, Input->x_rc in eq(c))
B) region subscript ink shape (x552..618 y400..415)
C) Remember: underline stroke (x75..145 y246..252)
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
org = np.asarray(Image.open(VID + "/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = org[:, :, 0], org[:, :, 1], org[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)
dark = (r < 110) & (g < 110) & (b < 110)

print("== A1. ORG red corridor x620..745 y348..435 (excluding panel border x696..703) ==")
m = red[348:435, 620:745].copy()
m[:, 696-620:704-620] = False
ys, xs = np.where(m)
if len(ys):
    print(f"  red px n={len(ys)} bbox x{620+xs.min()}..{620+xs.max()} y{348+ys.min()}..{348+ys.max()}")
    for y in range(348, 435):
        cols = np.where(red[y, 620:745])[0] + 620
        cols = [c for c in cols if not (696 <= c <= 703)]
        if cols:
            print(f"  y{y}: {cols}")
else:
    print("  none")
print("== A2. ORG red corridor x640..745 y400..470 (excl x696..703) ==")
for y in range(400, 470):
    cols = np.where(red[y, 640:745])[0] + 640
    cols = [c for c in cols if not (696 <= c <= 703)]
    if cols:
        print(f"  y{y}: {cols}")

print("== B. ORG region-subscript zone map x552..618 y400..416 (left x552; r=red #=dark) ==")
for y in range(400, 416):
    row = ""
    for x in range(552, 618):
        row += "r" if red[y, x] else ("#" if dark[y, x] else ".")
    print(f"  y{y} {row}")

print("== C. ORG Remember underline zone x75..145 y244..254 (dark|red per row) ==")
for y in range(244, 254):
    cols_d = np.where(dark[y, 75:145])[0] + 75
    cols_r = np.where(red[y, 75:145])[0] + 75
    print(f"  y{y}: dark={list(cols_d[:20])}{'...' if len(cols_d)>20 else ''} red={list(cols_r[:20])}{'...' if len(cols_r)>20 else ''}")

print("== D. ORG red in y364..400 x640..745 full (Weights connector upper part, incl border cols flagged) ==")
for y in range(360, 400):
    cols = np.where(red[y, 620:745])[0] + 620
    if cols:
        print(f"  y{y}: {list(cols)}")
