#!/usr/bin/env python3
"""Direct pixel ground truth: text color samples, box border scan (non-white runs),
content-frame exact edges. Frame coords."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

print("=== TEXT PIXEL SAMPLES (core glyph pixels: darkest/most saturated in region) ===")
def darkest(x0, x1, y0, y1, n=6):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    # most saturated/dark = min sum
    idx = np.argsort(reg.sum(axis=1))[:n]
    return [tuple(int(v) for v in reg[i]) for i in idx]

samples = [
    ("L1 'Feature Vector of' red", 96, 210, 202, 212),
    ("L1 'One' green?", 216, 242, 202, 212),
    ("L1 green?2", 250, 280, 202, 212),
    ("L2 green?", 105, 153, 218, 231),
    ("L2 'one filter' blue", 160, 272, 218, 231),
    ("M1 red", 342, 462, 200, 212),
    ("M1 'One' green", 468, 495, 200, 212),
    ("M1 green?2", 502, 587, 200, 212),
    ("M2 blue", 360, 479, 216, 230),
    ("M2 magenta?", 488, 563, 216, 230),
    ("R1 red", 638, 758, 173, 183),
    ("R2 green?", 680, 777, 189, 201),
    ("R2 magenta?", 788, 867, 189, 201),
    ("R3 blue?", 637, 731, 205, 219),
    ("R3 magenta?", 746, 829, 205, 219),
    ("TITLE", 300, 700, 72, 104),
    ("badge numeral", 862, 890, 60, 82),
]
for name, x0, x1, y0, y1 in samples:
    print(f"  {name}: {darkest(x0, x1, y0, y1)}")

print()
print("=== NON-WHITE RUNS: label box border scan ===")
def nonwhite_runs(y, x0, x1, thr=28, minlen=2):
    row = a[y, x0:x1]
    nw = (np.abs(row - 255).max(axis=1) > thr)
    out, inr = [], False
    for i, v in enumerate(nw):
        if v and not inr: st, inr = i, True
        elif not v and inr:
            if i - st >= minlen: out.append((x0 + st, x0 + i - 1, tuple(int(v2) for v2 in row[(st + i - 1) // 2])))
            inr = False
    if inr: out.append((x0 + st, x0 + len(nw) - 1, tuple(int(v2) for v2 in row[(st + len(nw) - 1) // 2])))
    return out

for lo, hi, xa, xb, name in [(185, 250, 80, 320, "LEFT"), (185, 250, 325, 605, "MIDDLE"), (158, 250, 620, 880, "RIGHT")]:
    print(f"-- {name} box: rows with long non-white runs (>40px) or any run at edges")
    for y in range(lo, hi):
        rr = nonwhite_runs(y, xa, xb)
        long = [t for t in rr if t[1] - t[0] > 40]
        if long:
            print(f"   y{y}: {[(s, e, c) for s, e, c in long]}")

print()
print("=== vertical border scan: columns with non-white runs len>25 in box y-bands ===")
def nonwhite_col_runs(x, y0, y1, thr=28, minlen=2):
    col = a[y0:y1, x]
    nw = (np.abs(col - 255).max(axis=1) > thr)
    out, inr = [], False
    for i, v in enumerate(nw):
        if v and not inr: st, inr = i, True
        elif not v and inr:
            if i - st >= minlen: out.append((y0 + st, y0 + i - 1, tuple(int(v2) for v2 in col[(st + i - 1) // 2])))
            inr = False
    if inr: out.append((y0 + st, y0 + len(nw) - 1, tuple(int(v2) for v2 in col[(st + len(nw) - 1) // 2])))
    return out

for xa, xb, ya, yb, name in [(80, 320, 185, 250, "LEFT"), (325, 605, 185, 250, "MIDDLE"), (620, 880, 158, 250, "RIGHT")]:
    print(f"-- {name}: columns x where a >25px non-white run exists in y{ya}..{yb}")
    for x in range(xa, xb):
        rr = nonwhite_col_runs(x, ya, yb)
        long = [t for t in rr if t[1] - t[0] > 25]
        if long:
            print(f"   x{x}: {[(s, e, c) for s, e, c in long]}")
