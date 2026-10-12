#!/usr/bin/env python3
"""Slide 038 — m15: green container geometry, ellipsis dots, navy text extent, bar ends."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
invx = lambda fx: round((fx - 18.63) / 0.96123, 1)
invy = lambda fy: round(fy / 0.95556, 1)
IN = lambda pt: round(pt / 72, 3)
green = (G > 120) & (G - R > 40) & (G - B > 40)

print("== green container border: leftmost/rightmost green px per row (y 280..366) ==")
for y in range(280, 367, 4):
    cols = np.where(green[y, 60:900])[0]
    if len(cols):
        print(f"  y={y} (slide {invy(y)}): left {cols.min()+60} right {cols.max()+60} n={len(cols)}")
print("== green col profile: topmost/bottommost green px per col (x 70..890) ==")
for x in range(70, 891, 40):
    rows = np.where(green[275:370, x])[0]
    if len(rows):
        print(f"  x={x} (slide {invx(x)}): top {rows.min()+275} bot {rows.max()+275}")

print("== ellipsis dots (green, X row y 471..482) ==")
gd = (G > 150) & (G - R > 60) & (G - B > 60)
seg = gd[471:483, 600:730]
ys, xs = np.where(seg)
if len(xs):
    print(f"  bbox x {xs.min()+600}..{xs.max()+600} y {ys.min()+471}..{ys.max()+471}")
    colprof = seg.sum(axis=0)
    runs, inr = [], False
    for i, v in enumerate(colprof):
        if v > 0 and not inr: s = i; inr = True
        elif v == 0 and inr: runs.append((s+600, i+600)); inr = False
    print("  dot blobs:", [(a, b, b-a) for a, b in runs])
print("== ellipsis dots (blue, top row y 264..274) ==")
bd = (B > 130) & (R < 90) & (G < 90)
seg = bd[264:274, 600:730]
ys, xs = np.where(seg)
if len(xs):
    print(f"  bbox x {xs.min()+600}..{xs.max()+600} y {ys.min()+264}..{ys.max()+264}")
    colprof = seg.sum(axis=0)
    runs, inr = [], False
    for i, v in enumerate(colprof):
        if v > 0 and not inr: s = i; inr = True
        elif v == 0 and inr: runs.append((s+600, i+600)); inr = False
    print("  dot blobs:", [(a, b, b-a) for a, b in runs])
print("== ellipsis dots (blue, mid row y 370..379) ==")
seg = bd[370:379, 600:730]
ys, xs = np.where(seg)
if len(xs):
    print(f"  bbox x {xs.min()+600}..{xs.max()+600} y {ys.min()+370}..{ys.max()+370}")

print("== navy text: white px col extent rows 415..435 ==")
white = (R > 210) & (G > 210) & (B > 210)
seg = white[415:436, 170:880]
colprof = seg.sum(axis=0)
cols = np.where(colprof > 0)[0]
print(f"  white text x {cols.min()+170}..{cols.max()+170} -> slide {invx(cols.min()+170)}..{invx(cols.max()+170)} (w {invx(cols.max()+170)-invx(cols.min()+170)})")
rows = np.where(seg.sum(axis=1) > 3)[0]
print(f"  white text y {rows.min()+415}..{rows.max()+415} -> slide {invy(rows.min()+415)}..{invy(rows.max()+415)}")

print("== gray bar ends: gray cols at rows 300..316 left/right ==")
gray = (abs(R - G) < 14) & (abs(G - B) < 14) & (R > 185) & (R < 240)
for band in ((300, 303), (310, 313), (317, 320)):
    seg2 = gray[band[0]:band[1], 60:900]
    cols = np.where(seg2.sum(axis=0) > 1)[0]
    if len(cols):
        print(f"  rows {band}: gray x {cols.min()+60}..{cols.max()+60} -> slide {invx(cols.min()+60)}..{invx(cols.max()+60)}")

print("== container fill check: sample (170,330) (500,290) (850,355) raw ==")
for (x, y) in ((100, 330), (170, 300), (500, 290), (500, 355), (850, 300), (85, 345)):
    print(f"  ({x},{y}): {tuple(img[y, x])}")

print("== red arrows precise: dark-red row extent at col2 x 276..283 ==")
darkred = (R > 100) & (R < 230) & (G < 90) & (B < 90)
seg3 = darkred[255:300, 274:284]
rows = np.where(seg3.sum(axis=1) > 0)[0]
print("  red rows:", rows.min()+255, rows.max()+255, "-> slide", invy(rows.min()+255), invy(rows.max()+255))
colprof = seg3.sum(axis=0)
cols = np.where(colprof > 0)[0]
print("  red cols:", cols.min()+274, cols.max()+274)

print("== green arrows precise: col2 x 273..287, y 312..338 ==")
seg4 = green[312:338, 273:288]
rows = np.where(seg4.sum(axis=1) > 0)[0]
print("  green rows:", rows.min()+312, rows.max()+312, "-> slide", invy(rows.min()+312), invy(rows.max()+312))
colprof = seg4.sum(axis=0)
cols = np.where(colprof > 0)[0]
print("  green cols:", cols.min()+273, cols.max()+273)
