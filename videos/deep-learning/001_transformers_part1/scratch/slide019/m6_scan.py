#!/usr/bin/env python3
"""m6_scan.py - vivid-green components, callout box edges, dec-mid A&N mode, L1 start."""
from PIL import Image
import collections

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
px = IM.load()

def vivid(c):
    r, g, b = c
    return g > 150 and g > r + 25 and g > b + 60 and r > 60

def components(pred, x0, y0, x1, y1, minn=20):
    seen = set(); out = []
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            if (xx, yy) in seen or not pred(px[xx, yy]): continue
            stack = [(xx, yy)]; comp = []; seen.add((xx, yy))
            while stack:
                cx, cy = stack.pop(); comp.append((cx, cy))
                for dx in (-2, -1, 0, 1, 2):
                    for dy in (-2, -1, 0, 1, 2):
                        nx, ny = cx + dx, cy + dy
                        if (nx, ny) in seen or not (x0 <= nx < x1 and y0 <= ny < y1): continue
                        if pred(px[nx, ny]):
                            seen.add((nx, ny)); stack.append((nx, ny))
            if len(comp) >= minn:
                xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
                cnt = collections.Counter(px[p] for p in comp)
                out.append((len(comp), (min(xs), min(ys), max(xs), max(ys)), cnt.most_common(2)))
    return out

print("== vivid-green components x585-875 y95-435 (n>=20) ==")
for n, bb, modes in sorted(components(vivid, 585, 95, 875, 435), key=lambda t: (t[1][1], t[1][0])):
    print(f"n={n:5d} bbox={bb} modes={modes}")

print("\n== callout box edges (1px) ==")
def edges(fillpred, x0, x1, y0, y1, label, minrow=40, mincol=15):
    rows = []
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if fillpred(px[x, y]))
        if n >= minrow: rows.append(y)
    cols = []
    if rows:
        for x in range(x0, x1):
            n = sum(1 for y in range(rows[0], rows[-1] + 1) if fillpred(px[x, y]))
            if n >= mincol: cols.append(x)
    print(f"{label}: rows {rows[0]}..{rows[-1]}  cols {cols[0]}..{cols[-1]}")

edges(lambda c: abs(c[0]-206)<14 and c[1]>243 and c[2]>240, 120, 400, 95, 140, "blue callout")
edges(lambda c: abs(c[0]-159)<14 and abs(c[1]-164)<14 and abs(c[2]-160)<14, 280, 560, 138, 182, "gray callout")
edges(lambda c: abs(c[0]-222)<12 and c[1]>245 and abs(c[2]-196)<14, 240, 500, 172, 220, "green callout")

print("\n== dec-mid A&N compartment exact ==")
cnt = collections.Counter()
for y in range(251, 263):
    for x in range(750, 838):
        cnt[px[x, y]] += 1
print(cnt.most_common(6))

print("\n== L1 start (thr sum<665) x340-470 y108-128 ==")
for y in range(108, 129):
    xs = [x for x in range(340, 470) if sum(px[x, y]) < 665]
    if xs: print(f"y={y}: {min(xs)}..{max(xs)} n={len(xs)} {px[xs[0],y]}")

print("\n== enc green channel vertical extent x634-646 ==")
for y in range(270, 412):
    xs = [x for x in range(632, 648) if vivid(px[x, y])]
    if xs: print(f"y={y}: x {min(xs)}..{max(xs)}", end="; ")
print()
print("\n== dec green channel vertical extent x826-842 ==")
for y in range(200, 412):
    xs = [x for x in range(824, 844) if vivid(px[x, y])]
    if xs: print(f"y={y}: x {min(xs)}..{max(xs)}", end="; ")
print()
