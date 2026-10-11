#!/usr/bin/env python3
"""measure3: exact pixel sampling + vertical column profiles + relaxed text components."""
from PIL import Image
import numpy as np
from collections import Counter, deque

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

def px(x, y):
    r, g, b = a[y, x]
    return f"#{r:02x}{g:02x}{b:02x}"

def patch_mode(x0, y0, x1, y1, top=5):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    c = Counter(map(tuple, reg.tolist()))
    return [(f"#{r:02x}{g:02x}{b:02x}", n) for (r, g, b), n in c.most_common(top)]

print("== exact pixel samples ==")
pts = {
    "decoder container fill": (700, 135), "decoder container fill2": (880, 130),
    "green bar1 cell": (525, 208), "green bar1 cell2": (560, 205), "green bar1 cell3": (585, 210),
    "orange bar1 cell": (550, 253), "orange bar1 cell2": (575, 257), "orange bar1 cell3": (530, 250),
    "encoder container fill": (100, 320), "encoder container fill2": (470, 470),
    "pink bar1 cell": (130, 330), "pink bar1 cell2": (170, 335), "pink bar1 cell3": (190, 325),
    "tan bar1 cell": (130, 415), "tan bar1 cell2": (170, 420), "tan bar1 cell3": (190, 410),
    "callout fill": (700, 420), "callout fill2": (600, 430),
    "background near title": (150, 70), "background bottom": (700, 480),
    "s1 label zone": (510, 262), "h1 label zone": (214, 330),
    "decoder red dot": (513, 262), "encoder red dot": (469, 326),
}
for k, (x, y) in pts.items():
    print(f"  {k} ({x},{y}): {px(x,y)}")

print("\n== patch modes ==")
patches = {
    "decoder container": (650, 125, 720, 140),
    "green bar1": (516, 200, 590, 217),
    "orange bar1": (516, 246, 590, 263),
    "encoder container": (300, 470, 400, 490),
    "pink bar1": (122, 318, 201, 343),
    "tan bar1": (121, 404, 201, 429),
    "callout": (565, 408, 830, 438),
}
for k, (x0, y0, x1, y1) in patches.items():
    print(f"  {k} {patch_mode(x0, y0, x1, y1)}")

# vertical profile: decoder column 1 (x=540-560 band median per row)
def vprofile(x0, x1, y0, y1, label):
    print(f"\n== vprofile {label} x{x0}-{x1} ==")
    prev = None
    for y in range(y0, y1):
        band = a[y, x0:x1]
        med = tuple(int(v) for v in np.median(band, axis=0))
        key = f"#{med[0]:02x}{med[1]:02x}{med[2]:02x}"
        # coarse class
        r, g, b = med
        if r > 235 and g > 235 and b > 200: c = "YEL"
        elif g > r + 15: c = "GRN"
        elif r < 120 and g < 120 and b < 120: c = "DRK"
        elif r > 200 and g < 110: c = "RED"
        elif r > 225 and 150 < g < 225 and 110 < b < 190: c = "PEA"
        else: c = "..."
        print(f"  y={y}: {key} {c}")

vprofile(540, 560, 116, 285, "decoder col1 center")

def vprofile2(x0, x1, y0, y1, label):
    print(f"\n== vprofile {label} x{x0}-{x1} ==")
    for y in range(y0, y1):
        band = a[y, x0:x1]
        med = tuple(int(v) for v in np.median(band, axis=0))
        key = f"#{med[0]:02x}{med[1]:02x}{med[2]:02x}"
        r, g, b = med
        if r > 225 and 150 < g < 225 and 110 < b < 190: c = "PEA"
        elif r > 235 and g > 235 and b > 200: c = "YEL"
        elif r < 120 and g < 120 and b < 120: c = "DRK"
        elif r > 200 and g < 110 and b < 110: c = "RED"
        elif abs(r - g) < 30 and r > 180 and b < 170: c = "TAN"
        else: c = "..."
        print(f"  y={y}: {key} {c}")

vprofile2(140, 190, 306, 496, "encoder col1 center")

# relaxed text ink (sum < 620) components inside the two containers
def comps(m, min_px=8):
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

ink = (a.sum(axis=2) < 620)
dec = np.zeros_like(ink); dec[110:290, 470:910] = ink[110:290, 470:910]
print("\n== decoder ink components (sum<620) ==")
for x0, y0, x1, y1, n in comps(dec, 8):
    print(f"  ({x0},{y0})-({x1},{y1}) w={x1-x0+1} h={y1-y0+1} area={n}  in=({x0/72:.2f},{y0/72:.2f})-({(x1+1)/72:.2f},{(y1+1)/72:.2f})")
enc = np.zeros_like(ink); enc[300:500, 40:495] = ink[300:500, 40:495]
print("\n== encoder ink components (sum<620) ==")
for x0, y0, x1, y1, n in comps(enc, 8):
    print(f"  ({x0},{y0})-({x1},{y1}) w={x1-x0+1} h={y1-y0+1} area={n}  in=({x0/72:.2f},{y0/72:.2f})-({(x1+1)/72:.2f},{(y1+1)/72:.2f})")
