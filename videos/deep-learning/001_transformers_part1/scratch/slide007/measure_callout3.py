#!/usr/bin/env python3
"""Callout pass 3: text line bands + underlines, ink color modes, border color, connector trace."""
from PIL import Image
import numpy as np
from collections import Counter

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)

# --- text bands inside box: ink = sum < 400, x60..445 y175..265 ---
sub = b[175:265, 60:445]
ink = sub.sum(axis=2) < 400
rows = ink.sum(axis=1)
print("row profile (y: count) nonzero:")
prev = False
for i, v in enumerate(rows):
    if v > 0:
        print(f"  y={175+i}: {int(v)}", end="")
        if (i % 3) == 0: print()
print("\n")

# band split on gaps >=2
bands = []
cur = None
for i, v in enumerate(rows):
    if v > 0:
        if cur and (175 + i) - cur[1] <= 2:
            cur[1] = 175 + i; cur[2] += int(v)
        else:
            if cur: bands.append(cur)
            cur = [175 + i, 175 + i, int(v)]
if cur: bands.append(cur)
print("bands:", bands)
for (y0, y1, n) in bands:
    m = ink[y0 - 175:y1 - 175 + 1]
    xs = np.nonzero(m.sum(axis=0) > 0)[0]
    print(f"  band y{y0}..{y1} h={y1-y0+1} px={n} x {60+xs.min()}..{60+xs.max()}")

# --- dark ink color histogram (sum<200) ---
dsub = b[175:265, 60:445].reshape(-1, 3)
d = dsub[dsub.sum(axis=1) < 200]
print("\ndark ink px:", len(d), "median:", np.median(d, axis=0), "mode:", Counter(map(tuple, d)).most_common(5))

# --- border color: column x44 and x455 rows 175..265 ---
print("\nleft border col x=44,45 (y180..260, every 20):")
for yy in range(180, 261, 20):
    print(f"  y{yy}:", b[yy, 43].tolist(), b[yy, 44].tolist(), b[yy, 45].tolist())
print("right border col x=455,456:")
for yy in range(180, 261, 20):
    print(f"  y{yy}:", b[yy, 454].tolist(), b[yy, 455].tolist(), b[yy, 456].tolist())
print("top border row y=169,170,171 (x100..300 sample):")
print("  ", b[168, 150].tolist(), b[169, 150].tolist(), b[170, 150].tolist(), b[171, 150].tolist(), b[172, 150].tolist())
print("bottom border row y=266..269 (x150):")
print("  ", b[265, 150].tolist(), b[266, 150].tolist(), b[267, 150].tolist(), b[268, 150].tolist(), b[269, 150].tolist())

# --- connector: blue-ish OR any dark px right of box, y150..300, x456..520 ---
print("\nconnector trace x456..520 y150..305 (non-panel-blue px):")
panel = np.abs(b - np.array([233, 233, 231])).sum(axis=2)
for yy in range(150, 306):
    seg = b[yy, 456:521]
    nonp = panel[yy, 456:521] > 45
    xs = np.nonzero(nonp)[0]
    if len(xs):
        cols = [seg[i].tolist() for i in xs[:6]]
        print(f"  y={yy}: x {(456+xs).tolist()[:8]} cols{cols[:3]}")
