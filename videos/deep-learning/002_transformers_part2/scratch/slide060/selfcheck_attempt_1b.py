#!/usr/bin/env python3
"""Closed-loop check attempt 1b: fixed disjoint bands (base-40..base+2 px), title x-range bug,
citation baseline excludes underline rows (underline reported separately for cap->underline check)."""
from PIL import Image
from collections import Counter

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide060/render_1.png"
img = Image.open(R).convert("RGB")
W, H = img.size
px = img.load()
K = 150 / 72.0

def reddish(p):
    r, g, b = p
    return r > 140 and r - g > 60 and r - b > 60

def blueish(p):
    r, g, b = p
    return b > 90 and b - r > 40 and b - g > 30

# (name, x0t, x1t, capt, baset, kind)  [slide pt]
T = [
    ("e1", 73.2, 598.5, 152.2, 166.94, "mix"),
    ("c1", 113.8, 535.1, 176.6, 189.94, "blue"),
    ("e2", 74.3, 696.0, 219.2, 233.90, "mix"),
    ("c2", 113.8, 464.4, 244.0, 256.92, "blue"),
    ("e3", 73.2, 525.6, 287.2, 301.93, "mix"),
    ("c3", 113.8, 383.2, 309.7, 322.85, "blue"),
    ("e4", 76.3, 793.9, 348.9, 363.62, "mix"),
    ("c4", 113.8, 599.6, 370.9, 384.71, "blue"),
    ("e5", 73.2, 430.0, 413.7, 428.55, "mix"),
    ("e6", 73.2, 596.6, 458.8, 473.51, "mix"),
]
print(f"render {W}x{H}   (tol 4px; bands base-40..base+2 px)")
print(f"{'line':5s} {'x0 t/dx':>14s} {'x1 t/dx':>14s} {'cap t/dy':>14s} {'base t/dy':>14s} {'ultop t/dy':>14s}")
for name, x0t, x1t, capt, bt, kind in T:
    bt_px = bt * K
    ylo, yhi = int(bt_px - 40), int(bt_px + 2)
    xs, ys = [], []
    rowc = {}
    for y in range(ylo, yhi):
        n = 0
        for x in range(140, 1858):
            p = px[x, y]
            ok = reddish(p) if kind == "red" else (blueish(p) or reddish(p))
            if ok:
                xs.append(x); ys.append(y); n += 1
        rowc[y] = n
    if not xs:
        print(f"{name:5s} NO INK  <-- BLOCKER")
        continue
    mx = max(rowc.values())
    ultop = min((y for y, n in rowc.items() if n > 0.6 * mx), default=None)
    base = max((y for y, n in rowc.items() if 0.6 * mx > n > 0.30 * mx), default=None)
    cap = min(y for y, n in rowc.items() if n > 0.15 * mx)
    x0, x1 = min(xs), max(xs)
    # cap->underline distance vs original (28.7px for c1/c2/c3; c4: (367.6-354.8)*2.0833*0.95556... use orig 13.0 frame px -> 13.6pt -> 28.3px)
    ult_t = capt * K + 28.5
    f = lambda v, t: f"{v:5.0f}/{v-t:+5.1f}" if v is not None else "  n/a"
    flag = ""
    for v, t in ((x0, x0t * K), (x1, x1t * K), (cap, capt * K), (base, bt_px)):
        if v is not None and abs(v - t) > 4: flag = "  <-- FIX"
    print(f"{name:5s} {f(x0, x0t*K):>14s} {f(x1, x1t*K):>14s} {f(cap, capt*K):>14s} "
          f"{f(base, bt_px):>14s} {f(ultop, ult_t):>14s}{flag}")

# title (outside box)
xs, ys = [], []
for y in range(int(40 * K), int(120 * K)):
    for x in range(300, 1900):
        if reddish(px[x, y]):
            xs.append(x); ys.append(y)
rc = Counter(ys); mx = max(rc.values())
base = max(y for y, n in rc.items() if n > 0.30 * mx)
cap = min(y for y, n in rc.items() if n > 0.15 * mx)
print(f"title {min(xs):5.0f}/{min(xs)-263.6*K:+5.1f} {max(xs):5.0f}/{max(xs)-636.0*K:+5.1f} "
      f"{cap:5.0f}/{cap-67.0*K:+5.1f} {base:5.0f}/{base-90.5*K:+5.1f}")
