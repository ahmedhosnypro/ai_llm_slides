#!/usr/bin/env python3
"""Connected-component colour extraction from slide_033.jpg (no scipy)."""
import numpy as np
from PIL import Image
from collections import Counter

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
H, W = o.shape[:2]


def components(mask, min_size=200, x0=0, y0=0):
    """2-pass connected components (4-connected) on a boolean mask."""
    m = mask[y0:, x0:].copy()
    h, w = m.shape
    lab = np.zeros((h, w), dtype=np.int32)
    parent = [0]

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    nxt = 1
    for yy in range(h):
        row = m[yy]
        for xx in range(w):
            if not row[xx]:
                continue
            up = lab[yy - 1, xx] if yy > 0 else 0
            left = lab[yy, xx - 1] if xx > 0 else 0
            if up and left:
                lab[yy, xx] = up
                if up != left:
                    union(up, left)
            elif up:
                lab[yy, xx] = up
            elif left:
                lab[yy, xx] = left
            else:
                lab[yy, xx] = nxt
                parent.append(nxt)
                nxt += 1
    # flatten
    out = {}
    for yy in range(h):
        for xx in range(w):
            l = lab[yy, xx]
            if l:
                out.setdefault(find(l), []).append((yy + y0, xx + x0))
    res = []
    for pts in out.values():
        if len(pts) < min_size:
            continue
        pts = np.array(pts)
        res.append((len(pts), int(pts[:, 1].min()), int(pts[:, 1].max()),
                    int(pts[:, 0].min()), int(pts[:, 0].max())))
    return res


r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

FAMILIES = {
    "CYAN": (b > 80) & (g > 80) & (r < 150) & (b - r > 15) & (g - r > 15),
    "GREEN": (g > 80) & (g - r > 18) & (g - b > 18),
    "VIOLET": (b - r > 25) & (b > 90) & (r > 60) & (g < 200),
    "RED": (r > 140) & (r - g > 50) & (r - b > 50),
    "YELLOW": (r > 190) & (g > 190) & (b < 170),
}

for name, mask in FAMILIES.items():
    print(f"===== {name} components (>=250 px) =====")
    comps = components(mask, min_size=250)
    comps.sort(reverse=True)
    for n, x0, x1, y0, y1 in comps[:24]:
        # dominant colour of the component
        sub = o[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
        mm = mask[y0:y1 + 1, x0:x1 + 1].reshape(-1)
        if mm.sum() == 0:
            continue
        dom = Counter(map(tuple, sub[mm])).most_common(1)[0]
        print(f"  {n:>6}px  x {x0}-{x1}  y {y0}-{y1}  (w={x1-x0+1},h={y1-y0+1})  dom={dom[0]}x{dom[1]}")
    print()
