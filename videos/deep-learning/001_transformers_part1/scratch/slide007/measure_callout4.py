#!/usr/bin/env python3
"""Callout pass 4: connector endpoints+color, underline rows, border core, line1 underline."""
from PIL import Image
import numpy as np
from collections import Counter

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides"
b = np.asarray(Image.open(f"{BASE}/slide_007.jpg").convert("RGB")).astype(int)

# --- connector: dark-ish px (sum<560) right of box x456..525, y150..300 ---
print("connector: dark px per row (x456..525, sum<560):")
pts = []
for yy in range(150, 300):
    seg = b[yy, 456:526]
    dk = np.nonzero(seg.sum(axis=1) < 560)[0]
    if len(dk):
        pts.append((yy, 456 + dk.min(), 456 + dk.max()))
        cols = [seg[i].tolist() for i in dk[:3]]
        if yy % 4 == 0 or yy < 160 or yy > 270:
            print(f"  y={yy}: x {456+dk.min()}..{456+dk.max()} n={len(dk)} cols{cols[:2]}")
if pts:
    print("connector extent: y", pts[0][0], "..", pts[-1][0])
    for (y, x0, x1) in pts[::12]:
        print(f"   y={y} x={x0}..{x1}")

# --- underlines: rows near each line bottom, blue-dark, x-extent ---
def rowext(y0, y1, x0, x1, thr=560):
    out = []
    for yy in range(y0, y1 + 1):
        seg = b[yy, x0:x1]
        dk = np.nonzero(seg.sum(axis=1) < thr)[0]
        if len(dk) > 2:
            out.append((yy, x0 + dk.min(), x0 + dk.max(), len(dk)))
    return out

print("\nline1 zone rows y194..206 x180..320:", rowext(194, 206, 180, 320))
print("\nline2 zone rows y213..223 x75..420:", rowext(213, 223, 75, 420))
print("\nline3 zone rows y231..243 x50..445:", rowext(231, 243, 50, 445))
print("\nline4 zone rows y248..260 x50..445:", rowext(248, 260, 50, 445))

# --- per-line main x extents at mid-line rows (thr 400) ---
def lineext(yc, x0=50, x1=445, thr=420):
    seg = b[yc, x0:x1]
    dk = np.nonzero(seg.sum(axis=1) < thr)[0]
    return (x0 + dk.min(), x0 + dk.max(), len(dk)) if len(dk) else None

print("\nmid-line extents:")
for name, y in [("L1", 191), ("L2", 210), ("L3a", 227), ("L3b", 229), ("L4", 246)]:
    print(f"  {name} y={y}:", lineext(y))

# --- border core color: darkest px along each edge ---
edges = {
    "top": [b[170, x] for x in range(60, 440, 10)],
    "bottom": [b[266, x] for x in range(60, 440, 10)],
    "left": [b[y, 44] for y in range(175, 265, 10)],
    "right": [b[y, 455] for y in range(175, 265, 10)],
}
for k, v in edges.items():
    v = np.array(v)
    lum = v.sum(axis=1)
    i = np.argmin(lum)
    print(f"border {k}: darkest {v[i].tolist()} mean {v.mean(axis=0).round(0).tolist()}")

# --- fill again: exact mode over whole box interior minus text ---
inter = b[173:264, 48:452].reshape(-1, 3)
inter = inter[inter.sum(axis=1) > 600]
print("\nfill mode (interior, bright):", Counter(map(tuple, inter)).most_common(4))
