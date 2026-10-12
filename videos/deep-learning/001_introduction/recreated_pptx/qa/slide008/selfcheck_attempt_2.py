#!/usr/bin/env python3
"""Closed-loop self-check, attempt 2: 150dpi render vs original slide_008.jpg geometry.

Fixes vs attempt 1: title band x-restricted to 100..870 (excludes chrome rule x58,
panel borders, badge), vertical-rule check y-limited to 50..525 (excludes chrome bottom
stroke), bullet band merge gap 7 render px. Tolerances in frame px (1 frame px = 2.083
render px @150dpi); the alignment law's ~4px @150dpi = ~1.92 frame px for positions,
wider for JPEG-bleed-padded advances. Adds FRAME CONTAINMENT assertions (self-check #2).
"""
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide008/render_2.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_008.jpg"

im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"render size: {W}x{H}")
S = W / 960.0
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 110) & (G < 90) & (B < 90)
dark = (R < 100) & (G < 100) & (B < 100)

fails = []
def check(name, mine, orig, tol):
    d = mine - orig
    ok = abs(d) <= tol
    print(f"  [{'OK ' if ok else 'FAIL'}] {name}: mine {mine:.1f} vs orig {orig:.1f} (delta {d:+.1f}, tol {tol})")
    if not ok:
        fails.append((name, round(mine, 1), orig, round(d, 1)))

# ---------- title (clean band x 100..870 frame px) ----------
print("-- title line 1 --")
def band(y0, y1, x0=100, x1=870):
    m = red[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.nonzero(m)
    return (ys.min() / S + y0, ys.max() / S + y0, xs.min() / S + x0, xs.max() / S + x0)

b1 = band(50, 107)
check("L1 cap top", b1[0], 63, 2.0)
check("L1 ink bottom", b1[1], 100, 2.0)
check("L1 x min", b1[2], 122, 2.5)
check("L1 x max", b1[3], 854, 2.5)
check("L1 center", (b1[2] + b1[3]) / 2, 488, 2.0)
print("-- title line 2 --")
b2 = band(107, 150)
check("L2 ascender top", b2[0], 109, 2.0)
check("L2 baseline", b2[1], 139, 2.0)
check("L2 x min", b2[2], 357, 2.5)
check("L2 x max", b2[3], 618, 2.5)
check("L2 center", (b2[2] + b2[3]) / 2, 487.5, 2.0)

# ---------- vertical red rule (y 50..525 only) ----------
print("-- vertical rule --")
colband = red[int(50 * S):int(525 * S), int(54 * S):int(63 * S)]
ys, xs = np.nonzero(colband)
if len(ys):
    check("rule y top", ys.min() / S + 50, 44, 2.5)
    check("rule y bottom", ys.max() / S + 50, 515.5, 2.5)
    check("rule x center", (xs.min() / S + 54 + xs.max() / S + 54) / 2, 58, 2.0)
else:
    fails.append(("vertical rule missing", 0, 0, 0)); print("  [FAIL] no rule ink")

# ---------- content box ----------
print("-- content box (border centerlines) --")
def rowband(y0, y1, x0, x1):
    m = red[int(y0 * S):int(y1 * S), int(x0 * S):int(x1 * S)]
    ys, xs = np.nonzero(m)
    return ys, xs
ys, xs = rowband(200, 500, 60, 80)
check("box left border center", (xs.min() / S + 60 + xs.max() / S + 60) / 2, 71, 2.0)
ys, xs = rowband(200, 500, 450, 470)
check("box right border center", (xs.min() / S + 450 + xs.max() / S + 450) / 2, 460, 2.0)
ys, xs = rowband(145, 160, 100, 440)
check("box top border center", (ys.min() / S + 145 + ys.max() / S + 145) / 2, 153, 2.0)
ys, xs = rowband(500, 520, 100, 440)
check("box bottom border center", (ys.min() / S + 500 + ys.max() / S + 500) / 2, 510, 2.0)

# ---------- headers ----------
print("-- headers --")
hdr = red.copy()
hdr[:int(158 * S)] = False
hdr[int(505 * S):] = False
hdr[:, :int(80 * S)] = False
hdr[:, int(450 * S):] = False
rows_h = hdr.sum(axis=1)
segs = []
start = None
for y in range(hdr.shape[0]):
    if rows_h[y] > 4 and start is None:
        start = y
    elif rows_h[y] <= 4 and start is not None:
        segs.append((start, y - 1)); start = None
if start is not None:
    segs.append((start, hdr.shape[0] - 1))
print(f"  found {len(segs)} header bands (expect 3)")
CAPS = [162, 259, 331]
ADVS = [262, 249, 260]
if len(segs) == 3:
    for i, (s, e) in enumerate(segs):
        ys2, xs2 = np.nonzero(hdr[s:e + 1])
        check(f"hdr{i+1} cap top", s / S, CAPS[i], 2.0)
        check(f"hdr{i+1} left", xs2.min() / S, 97, 2.0)
        check(f"hdr{i+1} advance", (xs2.max() - xs2.min()) / S, ADVS[i], 3.5)
else:
    fails.append(("header bands", len(segs), 3, 0)); print("  [FAIL] header band count")

# ---------- bullets ----------
print("-- bullets --")
db = dark.copy()
db[:int(180 * S)] = False
db[int(505 * S):] = False
db[:, :int(175 * S)] = False
db[:, int(470 * S):] = False
rows_d = db.sum(axis=1)
segs = []
start = None
for y in range(db.shape[0]):
    if rows_d[y] > 3 and start is None:
        start = y
    elif rows_d[y] <= 3 and start is not None:
        segs.append((start, y - 1)); start = None
merged = []
for s, e in segs:
    if merged and s - merged[-1][1] <= 7:
        merged[-1] = (merged[-1][0], e)
    else:
        merged.append((s, e))
print(f"  found {len(merged)} bullet bands (expect 11)")
CAPTOPS = [188, 213, 239, 285, 310, 357, 382, 408, 434, 459, 485]
ADV = [55, 11, 54, 98, 60, 97, 46, 44, 50, 61, 69]
if len(merged) == 11:
    for i, (s, e) in enumerate(merged):
        ys2, xs2 = np.nonzero(db[s:e + 1])
        check(f"b{i+1} cap top", s / S, CAPTOPS[i], 2.0)
        check(f"b{i+1} left", xs2.min() / S, 183, 2.0)
        check(f"b{i+1} advance", (xs2.max() - xs2.min()) / S, ADV[i], 3.5)
else:
    fails.append(("bullet bands", len(merged), 11, 0)); print("  [FAIL] bullet band count")

# ---------- dots ----------
print("-- dots --")
d2 = dark.copy()
d2[:, :int(158 * S)] = False
d2[:, int(174 * S):] = False
d2[:int(180 * S)] = False
d2[int(505 * S):] = False
ys, xs = np.nonzero(d2)
order = np.argsort(ys)
ys, xs = ys[order], xs[order]
clusters = []
cur = [0]
for i in range(1, len(ys)):
    if ys[i] - ys[i - 1] > 8:
        clusters.append(cur); cur = []
    cur.append(i)
clusters.append(cur)
print(f"  found {len(clusters)} dot clusters (expect 11)")
if len(clusters) == 11:
    for i, cl in enumerate(clusters):
        cy = (ys[cl].min() / S + ys[cl].max() / S) / 2
        cx = (xs[cl].min() / S + xs[cl].max() / S) / 2
        check(f"dot{i+1} cy", cy, CAPTOPS[i] + 5, 2.0)
        check(f"dot{i+1} cx", cx, 165.5, 2.0)
else:
    fails.append(("dot clusters", len(clusters), 11, 0))

# ---------- FRAME CONTAINMENT (self-check #2) ----------
print("-- frame containment --")
# all bullet/header/dot ink must sit inside box interior (borders at 71..460 x, 153..510 y)
box_ink = np.zeros_like(dark)
box_ink[int(156 * S):int(507 * S), int(74 * S):int(457 * S)] = True
ink_outside_box = dark & box_ink.__xor__(True) & (
    (np.arange(H)[:, None] > 150 * S) & (np.arange(H)[:, None] < 513 * S) &
    (np.arange(W)[None, :] > 60 * S) & (np.arange(W)[None, :] < 470 * S))
n_out = ink_outside_box.sum()
ok = n_out == 0
print(f"  [{'OK ' if ok else 'FAIL'}] dark ink between borders and interior gap: {n_out} px (expect 0)")
if not ok:
    fails.append(("ink outside box interior", n_out, 0, 0))
# red ink above panel top (y<42) other than chrome border rows: rule starts at 43
red_above = red[:int(41 * S), :]
red_above[:, :] &= True
n_above = red_above.sum()
ok = n_above == 0
print(f"  [{'OK ' if ok else 'FAIL'}] red ink above y41 (beyond chrome top border): {n_above} px (expect 0)")
if not ok:
    fails.append(("red ink above panel", n_above, 0, 0))
# right half must be empty: dark ink x>470 between y150..510
right_dark = dark[int(150 * S):int(510 * S), int(470 * S):]
n_right = right_dark.sum()
ok = n_right == 0
print(f"  [{'OK ' if ok else 'FAIL'}] dark ink in empty right region: {n_right} px (expect 0)")
if not ok:
    fails.append(("ink in right region", n_right, 0, 0))

# ---------- colors ----------
print("-- colors --")
def sample(x_frame, y_frame, label, expect, tol=30):
    x, y = int(x_frame * S), int(y_frame * S)
    px = a[y, x]
    d = max(abs(px[0] - expect[0]), abs(px[1] - expect[1]), abs(px[2] - expect[2]))
    ok = d <= tol
    print(f"  [{'OK ' if ok else 'FAIL'}] {label} @({x},{y}): {tuple(px)} expect {expect}")
    if not ok:
        fails.append((label, tuple(px), expect, d))
sample(600, 100, "panel gray", (233, 233, 231))
sample(250, 300, "box fill white", (255, 255, 253), tol=12)
sample(20, 300, "canvas white", (255, 255, 255), tol=12)
sample(58, 300, "rule red", (192, 0, 0), tol=60)
sample(71, 300, "box border red", (192, 0, 0), tol=60)

print()
if fails:
    print(f"SELFCHECK RESULT: {len(fails)} FAILURES")
    for f in fails:
        print("  FAIL:", f)
    sys.exit(1)
print("SELFCHECK RESULT: ALL OK")
