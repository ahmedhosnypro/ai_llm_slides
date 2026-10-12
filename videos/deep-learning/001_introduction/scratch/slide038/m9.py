#!/usr/bin/env python3
"""Slide 038 forensics pass 9: dark-ink cluster scan of diagram box + arrow trace + circle ring + '=' color."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

# dark ink relative to surroundings: lum<170, and not part of big colored slab interiors
dark = lum < 170

print("=== dark-ink clusters: 10x10 cells with >4 dark px (box interior x186..807 y254..508) ===")
cells = {}
for cy in range(254, 508, 10):
    for cx in range(186, 807, 10):
        n = dark[cy:cy+10, cx:cx+10].sum()
        if n > 4:
            cells[(cx, cy)] = n
# group into clusters
import collections
seen = set()
clusters = []
for (cx, cy) in sorted(cells):
    if (cx, cy) in seen: continue
    stack = [(cx, cy)]; comp = []
    while stack:
        c = stack.pop()
        if c in seen or c not in cells: continue
        seen.add(c); comp.append(c)
        for dx in (-10, 0, 10):
            for dy in (-10, 0, 10):
                stack.append((c[0] + dx, c[1] + dy))
    xs = [c[0] for c in comp]; ys = [c[1] for c in comp]
    clusters.append((min(xs), max(xs) + 10, min(ys), max(ys) + 10, sum(cells[c] for c in comp)))
clusters.sort(key=lambda t: (t[2], t[0]))
for (x0, x1, y0, y1, n) in clusters:
    print(f"cluster x {x0}..{x1} y {y0}..{y1} darkpx={n}")

print()
print("=== '=' region color (x572..593 y362..375) ===")
reg = a[362:376, 572:594].reshape(-1, 3)
rl = lum[362:376, 572:594].reshape(-1)
sel = reg[rl < 210]
print("modal:", np.median(sel, axis=0), "n=", len(sel))

print()
print("=== circle 3 (red) zoom 1px x685..720 y352..386 ===")
def cls(p):
    rr, gg, bb = p
    if rr > 235 and gg > 235 and bb > 235: return '.'
    if rr < 110 and gg < 110 and bb < 110: return '#'
    if rr > 170 and gg < 100 and bb < 100: return 'R'
    if rr > 150 and gg > 95 and gg < 185 and bb < 115 and (rr - bb) > 40: return 'o'
    if rr > 190 and gg > 170 and bb < 150: return 'y'
    if gg > 120 and (gg - rr) > 30 and (gg - bb) > 15: return 'G'
    if bb > 130 and gg > 120 and rr < 140: return 'c'
    if rr > 80 and bb > 110 and gg < 100: return 'P'
    return '+'
for y in range(352, 386):
    print(f"{y:3d} " + ''.join(cls(a[y, x]) for x in range(685, 721)))

print()
print("=== circle ring color sample (x611..640 ring pixels, lum 100..190) ===")
reg = a[352:386, 606:646].reshape(-1, 3)
rl = lum[352:386, 606:646].reshape(-1)
sel = reg[(rl > 90) & (rl < 200)]
print("ring modal:", np.median(sel, axis=0), "n=", len(sel))

print()
print("=== arrows trace map x385..575 y390..478 (2px) ===")
for y in range(390, 478, 2):
    row = ''
    for x in range(385, 575, 2):
        row += cls(a[y, x])
    print(f"{y:3d} {row}")
