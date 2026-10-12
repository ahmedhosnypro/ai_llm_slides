#!/usr/bin/env python3
"""Slide 030: measure content boxes, highlights, brackets, brace + color census."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def census(x0, y0, x1, y1, label, topn=8):
    """Dominant non-background colors in a region."""
    reg = im[y0:y1, x0:x1].reshape(-1, 3)
    # drop near-gray/near-white/near-black-lightened background (panel gray 231,233,230 and white)
    mask = ~(((np.abs(reg[:, 0] - reg[:, 1]) < 18) & (np.abs(reg[:, 1] - reg[:, 2]) < 18)) |
             ((reg[:, 0] > 225) & (reg[:, 1] > 225) & (reg[:, 2] > 225)))
    sel = reg[mask]
    if len(sel) == 0:
        print(f"{label}: no chroma ink")
        return
    q = (sel // 24) * 24 + 12
    keys, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:topn]
    tops = [f"({keys[i][0]},{keys[i][1]},{keys[i][2]})x{counts[i]}" for i in order]
    print(f"{label}: {' '.join(tops)}")

def bbox(x0, y0, x1, y1, label, mask_fn):
    sub = mask_fn[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(f"{label}: EMPTY")
        return None
    print(f"{label}: frame x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")
    return (int(xs.min()+x0), int(ys.min()+y0), int(xs.max()+x0), int(ys.max()+y0))

# masks
blue = (B > 120) & (B - R > 60) & (B - G > 40)          # blue borders/text
red = (R > 110) & (R - G > 60) & (R - B > 60)           # red ink
yellow = (R > 200) & (G > 180) & (B < 120) & (R - B > 90)  # FFFF00 highlights
green = (G > 130) & (G - R > 30) & (G - B > 30)         # green highlights/border
black = (R < 90) & (G < 90) & (B < 90)

print("=== BOX BORDERS (blue paths) ===")
# Blue vertical strokes: columns with many blue px in the top-left quadrant
print("-- top-left box: blue col counts x 60..420, rows 60..260")
cc = {x: int(blue[60:260, x].sum()) for x in range(60, 421) if blue[60:260, x].sum() > 80}
print("   cols:", cc)
rr = {y: int(blue[y, 60:420].sum()) for y in range(60, 261) if blue[y, 60:420].sum() > 80}
print("   rows:", rr)

print("-- remember box: blue col counts x 480..870, rows 90..200")
cc = {x: int(blue[90:200, x].sum()) for x in range(480, 871) if blue[90:200, x].sum() > 40}
print("   cols:", cc)
rr = {y: int(blue[y, 480:870].sum()) for y in range(90, 201) if blue[y, 480:870].sum() > 100}
print("   rows:", rr)

print("-- derivation box: blue col counts x 60..680, rows 240..330")
cc = {x: int(blue[240:330, x].sum()) for x in range(60, 681) if blue[240:330, x].sum() > 30}
print("   cols:", cc)
rr = {y: int(blue[y, 60:680].sum()) for y in range(240, 331) if blue[y, 60:680].sum() > 150}
print("   rows:", rr)

print("-- matrix box: blue col counts x 60..640, rows 340..520")
cc = {x: int(blue[340:520, x].sum()) for x in range(60, 641) if blue[340:520, x].sum() > 60}
print("   cols:", cc)
rr = {y: int(blue[y, 60:640].sum()) for y in range(340, 521) if blue[y, 60:640].sum() > 150}
print("   rows:", rr)

print("-- note box (green border): green col counts x 620..900, rows 370..500")
cc = {x: int(green[370:500, x].sum()) for x in range(620, 901) if green[370:500, x].sum() > 40}
print("   cols:", cc)
rr = {y: int(green[y, 620:900].sum()) for y in range(370, 501) if green[y, 620:900].sum() > 80}
print("   rows:", rr)

print("=== FILLS ===")
census(560, 110, 830, 185, "remember fill")
census(640, 390, 880, 480, "note fill")
census(120, 60, 360, 240, "vecbox fill")
census(80, 250, 600, 320, "deriv fill")
census(80, 350, 600, 500, "matrix fill")

print("=== HIGHLIGHT RECTS ===")
ys, xs = np.where(yellow)
print(f"yellow total px: {len(xs)}")
# cluster by connected regions via simple labeling
from scipy import ndimage as ndi
lab, n = ndi.label(yellow)
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(xs) > 150:
        print(f"  Y i{i}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} px={len(xs)}")
lab, n = ndi.label(green)
print("green total px:", int(green.sum()))
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(xs) > 150:
        print(f"  G i{i}: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} px={len(xs)}")

print("=== COLOR CENSUS per text region ===")
census(95, 85, 250, 105, "label 'Vector of Pos t'")
census(95, 180, 260, 205, "label 'Vector of Pos t+delta'")
census(520, 105, 700, 190, "remember text")
census(95, 240, 660, 325, "derivation text")
census(100, 360, 620, 520, "matrix box text+brace")
census(630, 380, 890, 490, "note text")
