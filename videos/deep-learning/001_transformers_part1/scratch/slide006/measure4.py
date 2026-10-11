#!/usr/bin/env python3
"""measure4: non-container ink components per container + exact horizontal runs on bar rows."""
from PIL import Image
import numpy as np
from collections import deque

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)

def comps(m, min_px=6):
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

def show(name, ref, x0, y0, x1, y1, tol=70, min_px=6, maxshow=60):
    reg = a[y0:y1, x0:x1]
    d = np.abs(reg - np.array(ref)).sum(axis=2)
    m = d > tol
    cs = comps(m, min_px)
    print(f"\n== {name} (ref #{ref[0]:02x}{ref[1]:02x}{ref[2]:02x} tol={tol}): {len(cs)} comps ==")
    for x0c, y0c, x1c, y1c, n in cs[:maxshow]:
        X0, Y0, X1, Y1 = x0c + x0, y0c + y0, x1c + x0, y1c + y0
        print(f"  ({X0},{Y0})-({X1},{Y1}) w={X1-X0+1} h={Y1-Y0+1} area={n}  in=({X0/72:.2f},{Y0/72:.2f})-({(X1+1)/72:.2f},{(Y1+1)/72:.2f})")

# decoder: ref = container #fdff85; look for text/arrows/dividers
show("decoder ink vs container", (253, 255, 133), 480, 118, 900, 281, tol=110, min_px=6)
# encoder: ref = container #f8d5ad
show("encoder ink vs container", (248, 213, 173), 48, 308, 485, 494, tol=90, min_px=6)

def hexrun(y, x0, x1, tol=18, minrun=2):
    """RLE by color with per-run median hex."""
    out = []
    start = x0
    def med(xs0, xs1):
        band = a[y, xs0:xs1]
        m = tuple(int(v) for v in np.median(band, axis=0))
        return f"#{m[0]:02x}{m[1]:02x}{m[2]:02x}"
    cur = a[y, x0].copy()
    for x in range(x0 + 1, x1):
        if np.abs(a[y, x] - cur).sum() > tol:
            if x - start >= minrun:
                out.append(f"{start}-{x-1}:{med(start, x)}")
            start = x
            cur = a[y, x].copy()
        else:
            cur = (cur * 0.8 + a[y, x] * 0.2)
    out.append(f"{start}-{x1-1}:{med(start, x1)}")
    return " ".join(out)

print("\n== decoder green bar row y=208 exact runs ==")
print(hexrun(208, 500, 880))
print("\n== decoder barB row y=264 exact runs ==")
print(hexrun(264, 500, 880))
print("\n== decoder barB row y=260 exact runs ==")
print(hexrun(260, 500, 880))
print("\n== encoder pink bar row y=330 exact runs ==")
print(hexrun(330, 110, 470))
print("\n== encoder tan bar row y=414 exact runs ==")
print(hexrun(414, 110, 470))
print("\n== decoder s-label row y=262 x495-600 ==")
print(hexrun(262, 495, 620, tol=25))
