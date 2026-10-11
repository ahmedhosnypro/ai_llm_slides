#!/usr/bin/env python3
"""Fine measurement v2: modal colors per region, RLE scanlines, dark-ink components, red dots."""
from PIL import Image
import numpy as np
from collections import Counter, deque

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)

def modal(x0, y0, x1, y1, top=8):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    q = (reg // 12 * 12)
    c = Counter(map(tuple, q.tolist()))
    return c.most_common(top)

print("== decoder container (478,116)-(902,283) modal ==")
for c, n in modal(478, 116, 902, 283):
    print(f"  #{c[0]:02x}{c[1]:02x}{c[2]:02x}  {n}")
print("== encoder container (46,306)-(487,496) modal ==")
for c, n in modal(46, 306, 487, 496):
    print(f"  #{c[0]:02x}{c[1]:02x}{c[2]:02x}  {n}")
print("== callout region (558,402)-(839,443) modal ==")
for c, n in modal(558, 402, 839, 443):
    print(f"  #{c[0]:02x}{c[1]:02x}{c[2]:02x}  {n}")
print("== title band (200,55)-(700,85) modal ==")
for c, n in modal(200, 55, 700, 85, 6):
    print(f"  #{c[0]:02x}{c[1]:02x}{c[2]:02x}  {n}")

def classify(p):
    r, g, b = p
    if r > 235 and g > 235 and b > 235: return "WHT"
    if r < 90 and g < 90 and b < 90: return "BLK"
    if r > 140 and g < 80 and b < 80: return "RED"
    if g - r > 25 and g > 180 and b < 160: return "GRN"
    if r > 230 and 170 <= g <= 220 and 100 <= b <= 175: return "ORG"  # F7C683-ish
    if r > 235 and g > 235 and 90 <= b <= 190: return "YEL"
    if r > 225 and 140 <= g <= 210 and 120 <= b <= 180: return "PCH"  # peach/pink/tan family
    return "."

def rle(y, x0, x1, minrun=3):
    out = []
    prev, start = None, x0
    for x in range(x0, x1):
        c = classify(a[y, x])
        if prev is None:
            prev, start = c, x
        elif c != prev:
            if x - start >= minrun:
                out.append(f"{start}-{x-1}:{prev}")
            else:
                out.append(f"{start}-{x-1}:{prev.lower()}")
            prev, start = c, x
    out.append(f"{start}-{x1-1}:{prev}")
    return " ".join(out)

print("\n== decoder scanlines ==")
for y in (135, 150, 175, 190, 208, 225, 240, 255, 270):
    print(f"y={y}: " + rle(y, 470, 910))
print("\n== encoder scanlines ==")
for y in (320, 330, 345, 360, 375, 390, 410, 425, 440, 455, 470, 485):
    print(f"y={y}: " + rle(y, 40, 495))

# dark ink components across whole slide (text + arrows)
dark = (a.sum(axis=2) < 330)
def comps(m, min_px=12):
    visited = np.zeros_like(m, dtype=bool)
    ys, xs = np.where(m)
    coords = set(zip(ys.tolist(), xs.tolist()))
    seen = set(); out = []
    for start in coords:
        if start in seen: continue
        q = deque([start]); seen.add(start)
        x0 = x1 = start[1]; y0 = y1 = start[0]; n = 0
        while q:
            y, x = q.popleft(); n += 1
            x0 = min(x0, x); x1 = max(x1, x); y0 = min(y0, y); y1 = max(y1, y)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    p = (y + dy, x + dx)
                    if p in coords and p not in seen:
                        seen.add(p); q.append(p)
        if n >= min_px:
            out.append((x0, y0, x1, y1, n))
    out.sort(key=lambda c: (c[1], c[0]))
    return out

print("\n== dark ink components (x0,y0,x1,y1,area) ==")
for c in comps(dark, 12):
    x0, y0, x1, y1, n = c
    print(f"  ({x0},{y0})-({x1},{y1}) w={x1-x0+1} h={y1-y0+1} area={n}  in=({x0/72:.2f},{y0/72:.2f})-({(x1+1)/72:.2f},{(y1+1)/72:.2f})")

# red components (dots + arrows + frame text)
red = (a[:, :, 0] > 130) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
print("\n== red components ==")
for c in comps(red, 6):
    x0, y0, x1, y1, n = c
    print(f"  ({x0},{y0})-({x1},{y1}) w={x1-x0+1} h={y1-y0+1} area={n}  in=({x0/72:.2f},{y0/72:.2f})-({(x1+1)/72:.2f},{(y1+1)/72:.2f})")
