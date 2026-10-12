#!/usr/bin/env python3
"""Closed-loop check attempt 1: render_1.png (2000x1125 @150dpi) ink vs mapped targets.
1 render px = 150/72 slide pt (0.72pt/px... rather 1 slide pt = 2.0833 px). Tolerance ~4px.
"""
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide060/render_1.png"
img = Image.open(R).convert("RGB")
W, H = img.size
px = img.load()
K = 150 / 72.0  # slide pt -> render px

def reddish(p):
    r, g, b = p
    return r > 140 and r - g > 60 and r - b > 60

def blueish(p):
    r, g, b = p
    return b > 90 and b - r > 40 and b - g > 30

# targets: (name, x0_pt, x1_pt, captop_pt, baseline_pt, kind)
# from frame measurements: frame->slide x=(fx-18.63)/0.96123, y=fy/0.95556
T = [
    ("title", 263.6, 636.0, 67.0, 90.5, "red"),
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
# cap tops in slide pt: frame rows E1 145.5, E2 209.5, E3 274.5, E4 333.5, E5 395.5,
# E6 438.5, C1 168.8, C2 233.2, C3 295.8, C4 354.8 -> /0.95556

# box border targets: x 64.6..894.5, y 122.4..504.4 (stroke centers)
print(f"render {W}x{H}")
box = {
    "left": None, "right": None, "top": None, "bottom": None,
}
for x in range(100, 1950):
    n = sum(1 for y in range(300, 1000) if blueish(px[x, y]))
    if n > 600:
        if box["left"] is None: box["left"] = x
        box["right"] = x
for y in range(200, 1090):
    n = sum(1 for x in range(200, 1800) if blueish(px[x, y]))
    if n > 1200:
        if box["top"] is None: box["top"] = y
        box["bottom"] = y
print(f"BOX render: left {box['left']} (target {64.6*K:.0f}), right {box['right']} (target {894.5*K:.0f}), "
      f"top {box['top']} (target {122.4*K:.0f}), bottom {box['bottom']} (target {504.4*K:.0f})")
print(f"BOX slide pt: left {box['left']/K:.1f}, right {box['right']/K:.1f}, top {box['top']/K:.1f}, bottom {box['bottom']/K:.1f}")

# fill color sample (box interior empty spot)
from collections import Counter
c = Counter()
for y in range(960, 1040):
    for x in range(1300, 1700):
        c[px[x, y]] += 1
print("fill top:", c.most_common(3), "(target FFFFFF)")

# per-line ink measurement: search band around each target, excluding box border cols
BORDL, BORDR = box["left"] + 6, box["right"] - 6
print(f"{'line':6s} {'x0 (t/dx)':>16s} {'x1 (t/dx)':>16s} {'cap (t/dy)':>16s} {'base (t/dy)':>16s}")
results = []
for name, x0t, x1t, capt, bt, kind in T:
    ylo = int((capt - 14) * K); yhi = int((bt + 14) * K)
    xs, ys = [], []
    for y in range(max(ylo, int(box["top"]) + 6), min(yhi, int(box["bottom"]) - 6)):
        for x in range(BORDL, BORDR):
            p = px[x, y]
            ok = reddish(p) if kind == "red" else (blueish(p) or reddish(p))
            if ok:
                xs.append(x); ys.append(y)
    if not xs:
        print(f"{name:6s} NO INK FOUND  <-- BLOCKER")
        results.append((name, None))
        continue
    # baseline: last row with >30% of max row count; cap: first row with >15%
    from collections import Counter as C2
    rc = C2(ys)
    mx = max(rc.values())
    base = max(y for y, n in rc.items() if n > 0.30 * mx)
    cap = min(y for y, n in rc.items() if n > 0.15 * mx)
    x0, x1 = min(xs), max(xs)
    dx0, dx1 = x0 - x0t * K, x1 - x1t * K
    dcap, dbase = cap - capt * K, base - bt * K
    flag = "" if max(abs(dx0), abs(dx1), abs(dcap), abs(dbase)) <= 4 else "  <-- FIX"
    print(f"{name:6s} {x0:5.0f}({x0t*K:5.0f}/{dx0:+5.1f}) {x1:5.0f}({x1t*K:5.0f}/{dx1:+5.1f}) "
          f"{cap:5.0f}({capt*K:5.0f}/{dcap:+5.1f}) {base:5.0f}({bt*K:5.0f}/{dbase:+5.1f}){flag}")
    results.append((name, (dx0, dx1, dcap, dbase)))

# title measured separately (outside box)
xs, ys = [], []
for y in range(int(40 * K), int(120 * K)):
    for x in range(int(150 * K), int(1900 * K)):
        if reddish(px[x, y]):
            xs.append(x); ys.append(y)
rc = C2(ys); mx = max(rc.values())
base = max(y for y, n in rc.items() if n > 0.30 * mx)
cap = min(y for y, n in rc.items() if n > 0.15 * mx)
print(f"title  {min(xs):5.0f}({263.6*K:5.0f}/{min(xs)-263.6*K:+5.1f}) {max(xs):5.0f}({636.0*K:5.0f}/{max(xs)-636.0*K:+5.1f}) "
      f"{cap:5.0f}({67.0*K:5.0f}/{cap-67.0*K:+5.1f}) {base:5.0f}({90.5*K:5.0f}/{base-90.5*K:+5.1f})")
