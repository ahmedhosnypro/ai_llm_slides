#!/usr/bin/env python3
"""measure3: precise sub-element geometry for slide_022.jpg"""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def runs_1d(mask, minlen=1):
    out = []
    inr = False
    for i in range(len(mask)):
        if mask[i] and not inr:
            s = i; inr = True
        elif not mask[i] and inr:
            if i - s >= minlen: out.append((s, i - 1))
            inr = False
    if inr and len(mask) - s >= minlen: out.append((s, len(mask) - 1))
    return out

white = (a[:, :, 0] > 235) & (a[:, :, 1] > 235) & (a[:, :, 2] > 235)
dark = a.sum(axis=2) < 260  # near-black ink (text/arrows)

# --- container vertical borders per panel: scan row 300 and row 450
for row in (160, 300, 450):
    print(f"--- row {row} strokes (non-gray, x100..860) ---")
    segs = []
    x = 100
    while x < 860:
        px = a[row, x]
        if abs(px[0]-233)+abs(px[1]-233)+abs(px[2]-231) > 90 and not (px[0]>235 and px[1]>235 and px[2]>235):
            x0 = x
            while x < 860:
                p2 = a[row, x]
                if abs(p2[0]-233)+abs(p2[1]-233)+abs(p2[2]-231) > 90 and not (p2[0]>235 and p2[1]>235 and p2[2]>235):
                    x += 1
                else:
                    break
            mid = tuple(a[row, (x0 + x - 1) // 2])
            segs.append((x0, x - 1, mid))
        else:
            x += 1
    print("   ", segs)

# --- white squares: white runs inside each container band
print("\n=== white-square column runs (row through square centers) ===")
for name, (x0, x1) in [("L-INPUT", (158, 258)), ("L-PROJ", (267, 363)), ("L-OUT", (372, 472)),
                        ("R-INPUT", (500, 577)), ("R-PROJ", (579, 659)), ("R-OUT", (667, 818))]:
    colw = white[:, x0:x1 + 1].sum(axis=1)
    rr = runs_1d(colw > (x1 - x0) * 0.5, 8)
    print(f"{name}: white rows {rr}")

# --- dark text/arrow ink bands per column region
print("\n=== dark ink row-bands per region ===")
for name, (x0, x1) in [("title", (100, 860)), ("L-labels-left-of-input", (60, 156)),
                        ("L-INPUT", (158, 258)), ("L-PROJ", (264, 364)), ("L-OUT", (370, 480)),
                        ("L-OUT-labels-right", (472, 486)), ("R-INPUT-labels-left", (488, 500)),
                        ("R-INPUT", (498, 578)), ("R-PROJ", (576, 662)), ("R-OUT", (663, 820)),
                        ("R-OUT-labels-right", (818, 860)),
                        ("tag-L", (240, 390)), ("tag-R", (540, 690))]:
    band = dark[:, x0:x1 + 1]
    cnt = band.sum(axis=1)
    rr = runs_1d(cnt >= 2, 2)
    print(f"{name}: dark rows {rr}")

print("\n=== dark ink col-bands in label margins ===")
for name, (y0, y1, x0, x1) in [
    ("L input labels", (150, 465, 60, 156)),
    ("L out w(t) label", (150, 465, 473, 486)),
    ("R input w(t) label", (150, 465, 488, 499)),
    ("R out labels", (150, 465, 820, 862)),
    ("headers L panel", (125, 150, 117, 486)),
    ("headers R panel", (125, 150, 488, 840)),
]:
    band = dark[y0:y1 + 1, x0:x1 + 1]
    cnt = band.sum(axis=0)
    rr = runs_1d(cnt >= 1, 1)
    print(f"{name}: dark cols {rr[:30]}")

# --- stroke color samples
print("\n=== stroke color samples ===")
print("green? y300 x372:", tuple(a[300, 372]), " x472:", tuple(a[300, 472]))
print("green? y300 x373:", tuple(a[300, 373]), " x471:", tuple(a[300, 471]))
print("input border y300 x158:", tuple(a[300, 158]), " x257:", tuple(a[300, 257]))
print("proj border y300 x266:", tuple(a[300, 266]), " x363:", tuple(a[300, 363]))
print("proj fill y300 x300:", tuple(a[300, 300]))
print("R input border y300 x500:", tuple(a[300, 500]), " x576:", tuple(a[300, 576]))
print("R out border y300 x667:", tuple(a[300, 667]), " x817:", tuple(a[300, 817]))
print("tag border y488 x255:", tuple(a[488, 255]), " tag fill y488 x300:", tuple(a[488, 300]))
print("title px y85 x140:", tuple(a[85, 140]))
print("header INPUT y135 x170:", tuple(a[135, 170]), tuple(a[133, 175]))
print("badge ring sample y71 x875:", tuple(a[71, 875]), " badge fill y71 x893:", tuple(a[71, 893]))
print("square outline? L-INPUT square edge: sample around y180..200")
