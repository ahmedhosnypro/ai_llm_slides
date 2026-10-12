#!/usr/bin/env python3
"""Forensics pass 1 — slide_028.jpg (960x540, 1px = 1pt). PIL-only measurements.

Measures: red title bands (row profile, per-band x-extent / cap / dense-baseline / tail,
modal color), dark ink bands (attribution bottom-left), black bar, constant video chrome
(inset strokes), cursor region, panel bounds.
"""
import numpy as np
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_028.jpg"
im = Image.open(ORIG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

print(f"size {W}x{H}")

def red_mask(r, g, b):
    return (r > 110) & (r > g + 40) & (r > b + 40)

def dark_mask(r, g, b):
    return (r < 120) & (g < 120) & (b < 120)

rm = red_mask(R, G, B)
dm = dark_mask(R, G, B)

# ---- red row profile (whole frame) ----
rows = rm.sum(axis=1)
bands = []
in_b = False
for y in range(H):
    if rows[y] > 3 and not in_b:
        y0, in_b = y, True
    elif rows[y] <= 3 and in_b:
        bands.append((y0, y - 1))
        in_b = False
if in_b:
    bands.append((y0, H - 1))
print("\n-- red bands (y0,y1,height,peak_count) --")
for (y0, y1) in bands:
    seg = rows[y0:y1 + 1]
    print(f"  y {y0:3d}..{y1:3d} h={y1-y0+1:3d} peak={int(seg.max())}")

# ---- per-band x extent + vertical marks + modal color ----
print("\n-- red band detail --")
for (y0, y1) in bands:
    sub = rm[y0:y1 + 1, :]
    cols = sub.sum(axis=0)
    xs = np.where(cols > 0)[0]
    ys_rel = np.where(sub.sum(axis=1) > 2)[0]
    if len(xs) == 0:
        continue
    # modal color among strongly red pixels
    rr = a[y0:y1 + 1, :, :][sub]
    if len(rr):
        # quantize to reduce JPEG noise
        q = (rr // 8 * 8)
        vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
        top = vals[np.argsort(-counts)][:3]
        cnts = np.sort(counts)[::-1][:3]
        print(f"  band y{y0}..{y1}: x {xs.min()}..{xs.max()} (w {xs.max()-xs.min()+1}, center {(xs.min()+xs.max())/2:.1f})"
              f" rows{ys_rel.min()}..{ys_rel.max()} modal_rgb {list(map(list, top))} counts {list(map(int,cnts))}")

# dark-dense rows inside each red band (baseline estimate) + full column profile marks
print("\n-- red band vertical marks (col-count thresholds) --")
for (y0, y1) in bands:
    sub = rm[max(0, y0 - 6):y1 + 7, :]
    rp = sub.sum(axis=1)
    ys = [i + max(0, y0 - 6) for i, n in enumerate(rp) if n > 3]
    dense = [y for y, n in zip(range(max(0, y0 - 6), y1 + 7), rp) if n > 40]
    print(f"  band y{y0}..{y1}: first_ink {min(ys) if ys else None} last_ink {max(ys) if ys else None} dense_rows {dense[:3]}..{dense[-3:] if dense else None}")

# ---- dark ink bands in lower-left (attribution + bar + cursor) ----
print("\n-- dark bands, x 60..500, y 400..539 --")
dl = dm[:, 60:500].sum(axis=1)
in_b = False
for y in range(400, H):
    if dl[y] > 2 and not in_b:
        y0, in_b = y, True
    elif dl[y] <= 2 and in_b:
        print(f"  dark band y {y0}..{y-1} h={y-y0}")
        sub = dm[y0:y, 60:500]
        cols = sub.sum(axis=0)
        xs = np.where(cols > 0)[0]
        rr = a[y0:y, 60:500, :][sub]
        if len(rr):
            q = (rr // 8 * 8)
            vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
            top = vals[np.argsort(-counts)][:2]
            print(f"    x {xs.min()+60}..{xs.max()+60} modal_rgb {list(map(list, top))} count {int(np.sort(counts)[::-1][0])}")
        in_b = False
if in_b:
    print(f"  dark band y {y0}..{H-1} (to bottom)")

# ---- full-width dark bands (bar) ----
print("\n-- full-width dark bands y 460..539 (x 100..900) --")
dw = dm[:, 100:900].sum(axis=1)
for y in range(460, H):
    if dw[y] > 400:
        print(f"  y={y} darkcount={int(dw[y])}")

# ---- constant chrome: top inset stroke, left inset stroke ----
print("\n-- constant video chrome --")
top_red = [(y, int(rm[y, 42:918].sum())) for y in range(38, 50) if rm[y, 42:918].sum() > 50]
print(f"  top inset stroke rows: {top_red}")
left_red = [(x, int(rm[50:535, x].sum())) for x in range(50, 66) if rm[50:535, x].sum() > 100]
print(f"  left inset stroke cols: {left_red}")
right_red = [(x, int(rm[50:535, x].sum())) for x in range(895, 915) if rm[50:535, x].sum() > 100]
print(f"  right inset stroke cols: {right_red}")

# ---- panel bounds (gray vs white) ----
print(f"  pixel(20,20)={tuple(a[20,20])} pixel(300,300)={tuple(a[300,300])} pixel(480,500)={tuple(a[480,500])}")
# scan row 300 for gray panel edges
row = a[300]
grayish = np.where((np.abs(row[:, 0] - 233) < 12) & (np.abs(row[:, 1] - 233) < 12) & (np.abs(row[:, 2] - 231) < 12))[0]
print(f"  gray-panel x-range at row 300: {grayish.min()}..{grayish.max()}" if len(grayish) else "  no gray at row 300")

# ---- cursor hunt: spec x~29% y~85% -> (278,459) ----
print("\n-- cursor region scan (x 240..320, y 430..480) --")
sub = a[430:480, 240:320]
blackish = (sub[..., 0] < 80) & (sub[..., 1] < 80) & (sub[..., 2] < 80)
whiteish = (sub[..., 0] > 240) & (sub[..., 1] > 240) & (sub[..., 2] > 240)
ys, xs = np.where(blackish)
if len(ys):
    print(f"  black ink: x {xs.min()+240}..{xs.max()+240} y {ys.min()+430}..{ys.max()+430} count={len(ys)}")
ys, xs = np.where(whiteish)
if len(ys):
    print(f"  white ink: x {xs.min()+240}..{xs.max()+240} y {ys.min()+430}..{ys.max()+430} count={len(ys)}")
