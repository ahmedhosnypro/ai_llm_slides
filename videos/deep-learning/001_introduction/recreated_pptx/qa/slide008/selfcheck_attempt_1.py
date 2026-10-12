#!/usr/bin/env python3
"""Closed-loop self-check: 150dpi render vs original slide_008.jpg measured geometry.

Render space: 2001x1125 (13.333x7.5in @150dpi). Original frame: 960x540 (1px=1pt).
Scale render->frame: *960/2000 = 0.48. Tolerance ~4px @150dpi = 1.92px @frame scale.
"""
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide008/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_008.jpg"

im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print(f"render size: {W}x{H}")
S = W / 960.0  # frame px -> render px
oim = Image.open(ORIG).convert("RGB")
oa = np.asarray(oim).astype(int)

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 110) & (G < 90) & (B < 90)
dark = (R < 100) & (G < 100) & (B < 100)

fails = []
def check(name, mine_frame, orig_frame, tol=4.0):
    """mine_frame/orig_frame in frame-px units (960x540 scale)."""
    d = mine_frame - orig_frame
    ok = abs(d) <= tol
    status = "OK " if ok else "FAIL"
    print(f"  [{status}] {name}: mine {mine_frame:.1f} vs orig {orig_frame:.1f} (delta {d:+.1f}, tol {tol})")
    if not ok:
        fails.append((name, mine_frame, orig_frame, d))
    return ok

# ---------- title ----------
# line 1 band: render rows corresponding to frame 60..105
t1 = red[int(55 * S):int(106 * S)].copy()
t1[:, :int(56 * S)] = False
ys, xs = np.nonzero(t1)
cap1 = ys.min() / S + 55
bot1 = ys.max() / S + 55
x1min, x1max = xs.min() / S, xs.max() / S
c1 = (x1min + x1max) / 2
print("-- title line 1 --")
check("L1 cap top", cap1, 63, 4)
check("L1 ink bottom", bot1, 100, 4)
check("L1 x min", x1min, 122, 4)
check("L1 x max", x1max, 854, 4)
check("L1 center", c1, 488, 4)

t2 = red[int(106 * S):int(146 * S)].copy()
t2[:, :int(56 * S)] = False
ys, xs = np.nonzero(t2)
cap2 = ys.min() / S + 106
bot2 = ys.max() / S + 106
x2min, x2max = xs.min() / S, xs.max() / S
c2 = (x2min + x2max) / 2
print("-- title line 2 --")
check("L2 ascender top", cap2, 109, 4)
check("L2 baseline", bot2, 139, 4)
check("L2 x min", x2min, 357, 4)
check("L2 x max", x2max, 618, 4)
check("L2 center", c2, 487.5, 4)

# ---------- vertical red rule ----------
# frame col 58, y 43..516. Find in render: red pixels near x=58*S in col slice
colband = red[:, int(55 * S):int(62 * S)]
ys, xs = np.nonzero(colband)
if len(ys):
    # rule = rows where a near-vertical run exists; exclude badge/box rows (box left border at x71*2)
    ymin, ymax = ys.min() / S, ys.max() / S
    print("-- vertical rule --")
    check("rule y top", ymin, 43, 4)
    check("rule y bottom", ymax, 516, 4)
    cx = (xs.min() / S + 55 + xs.max() / S + 55) / 2
    check("rule x center", cx, 58, 3)
else:
    fails.append(("vertical rule missing", 0, 0, 0))
    print("  [FAIL] vertical rule: NO RED INK found near x58")

# ---------- content box ----------
print("-- content box (border centerlines) --")
# left border: red cols near frame x71 within box rows
boxband = red[int(200 * S):int(500 * S), int(60 * S):int(80 * S)]
ys, xs = np.nonzero(boxband)
if len(xs):
    lcenter = (xs.min() / S + 60 + xs.max() / S + 60) / 2
    check("box left border center", lcenter, 71, 3)
else:
    fails.append(("box left border", 0, 0, 0)); print("  [FAIL] box left border missing")
boxband = red[int(200 * S):int(500 * S), int(450 * S):int(470 * S)]
ys, xs = np.nonzero(boxband)
if len(xs):
    rcenter = (xs.min() / S + 450 + xs.max() / S + 450) / 2
    check("box right border center", rcenter, 460, 3)
else:
    fails.append(("box right border", 0, 0, 0)); print("  [FAIL] box right border missing")
rowband = red[int(145 * S):int(160 * S), int(100 * S):int(440 * S)]
ys, xs = np.nonzero(rowband)
if len(ys):
    tcenter = (ys.min() / S + 145 + ys.max() / S + 145) / 2
    check("box top border center", tcenter, 153, 3)
else:
    fails.append(("box top border", 0, 0, 0)); print("  [FAIL] box top border missing")
rowband = red[int(500 * S):int(520 * S), int(100 * S):int(440 * S)]
ys, xs = np.nonzero(rowband)
if len(ys):
    bcenter = (ys.min() / S + 500 + ys.max() / S + 500) / 2
    check("box bottom border center", bcenter, 510, 3)
else:
    fails.append(("box bottom border", 0, 0, 0)); print("  [FAIL] box bottom border missing")

# ---------- headers ----------
print("-- headers (red, cap tops + left edges) --")
hdr = red.copy()
hdr[:int(150 * S)] = False
hdr[int(515 * S):] = False
hdr[:, :int(80 * S)] = False
hdr[:, int(450 * S):] = False
hdr[:int(158 * S)] = False  # skip top border
hdr[int(505 * S):] = False  # skip bottom border
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
if len(segs) >= 3:
    for i, (s, e) in enumerate(segs[:3]):
        band = hdr[s:e + 1]
        ys2, xs2 = np.nonzero(band)
        cap = s / S
        check(f"hdr{i+1} cap top", cap, [162, 259, 331][i], 4)
        check(f"hdr{i+1} left", xs2.min() / S, 97, 4)
        adv_me = (xs2.max() - xs2.min()) / S
        adv_or = [262, 249, 260][i]
        check(f"hdr{i+1} advance", adv_me, adv_or, 6)
else:
    fails.append(("headers", len(segs), 3, 0)); print("  [FAIL] header bands != 3")

# ---------- bullets ----------
print("-- bullets (dark bands: cap tops, left edges, advances) --")
db = dark.copy()
db[:int(180 * S)] = False
db[int(505 * S):] = False
db[:, :int(150 * S)] = False
db[:, int(470 * S):] = False
rows_d = db.sum(axis=1)
segs = []
start = None
for y in range(db.shape[0]):
    if rows_d[y] > 3 and start is None:
        start = y
    elif rows_d[y] <= 3 and start is not None:
        segs.append((start, y - 1)); start = None
# merge segments with gap < 4 render px (Spacy descender split)
merged = []
for s, e in segs:
    if merged and s - merged[-1][1] <= 4:
        merged[-1] = (merged[-1][0], e)
    else:
        merged.append((s, e))
print(f"  found {len(merged)} bullet bands (expect 11)")
CAPTOPS = [188, 213, 239, 285, 310, 357, 382, 408, 434, 459, 485]
ADV = [55, 11, 54, 98, 60, 97, 46, 44, 50, 61, 69]
if len(merged) == 11:
    for i, (s, e) in enumerate(merged):
        band = db[s:e + 1]
        ys2, xs2 = np.nonzero(band)
        check(f"b{i+1} cap top", s / S, CAPTOPS[i], 4)
        check(f"b{i+1} left", xs2.min() / S, 183, 4)
        check(f"b{i+1} advance", (xs2.max() - xs2.min()) / S, ADV[i], 6)
else:
    fails.append(("bullet bands", len(merged), 11, 0)); print("  [FAIL] bullet band count != 11")

# ---------- dots ----------
print("-- dots --")
d2 = dark.copy()
d2[:, :int(158 * S)] = False
d2[:, int(174 * S):] = False
d2[:int(180 * S)] = False
d2[int(505 * S):] = False
ys, xs = np.nonzero(d2)
if len(ys):
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
            check(f"dot{i+1} cy", cy, CAPTOPS[i] + 5, 4)
            check(f"dot{i+1} cx", cx, 165.5, 4)
    else:
        fails.append(("dot clusters", len(clusters), 11, 0))
else:
    fails.append(("dots missing", 0, 0, 0)); print("  [FAIL] no dots found")

# ---------- colors ----------
print("-- color samples (render px, expect values) --")
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
# title red: sample a thick stroke pixel — find modal in title band
tt = red[int(60 * S):int(100 * S), int(130 * S):int(840 * S)]
ys, xs = np.nonzero(tt)
if len(ys):
    from collections import Counter
    pxv = a[int(60 * S):int(100 * S), int(130 * S):int(840 * S)][ys, xs]
    cnt = Counter(map(tuple, pxv))
    print(f"  title red modal: {cnt.most_common(3)}")

print()
if fails:
    print(f"SELFCHECK RESULT: {len(fails)} FAILURES")
    for f in fails:
        print("  FAIL:", f)
    sys.exit(1)
else:
    print("SELFCHECK RESULT: ALL OK")
