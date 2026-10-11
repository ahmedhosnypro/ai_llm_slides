#!/usr/bin/env python3
"""PIL color census + component map for slide_016.jpg (960x540, 1px = 1pt)."""
import sys
import numpy as np
from PIL import Image

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_016.jpg").convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

print(f"frame {W}x{H}")

# ---- 1. coarse color census (quantize /8) ----
q = (IM // 8) * 8
flat = q.reshape(-1, 3)
colors, counts = np.unique(flat, axis=0, return_counts=True)
order = np.argsort(-counts)
print("\n-- top 45 quantized colors (q8) --")
for i in order[:45]:
    c = colors[i]
    print(f"  ({c[0]:3d},{c[1]:3d},{c[2]:3d})  n={counts[i]:6d}")

# ---- 2. component finder for a target color ----
def components(mask, min_area=30):
    # simple 4-connectivity labeling via BFS (frame is small)
    lbl = np.zeros(mask.shape, dtype=int)
    cur = 0
    comps = []
    ys, xs = np.where(mask)
    coords = set(zip(ys.tolist(), xs.tolist()))
    seen = set()
    from collections import deque
    for start in coords:
        if start in seen:
            continue
        cur += 1
        qq = deque([start])
        seen.add(start)
        pix = []
        while qq:
            y, x = qq.popleft()
            pix.append((y, x))
            for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                n = (y+dy, x+dx)
                if n in coords and n not in seen:
                    seen.add(n)
                    qq.append(n)
        if len(pix) >= min_area:
            py = np.array([p[0] for p in pix]); px_ = np.array([p[1] for p in pix])
            comps.append((px_.min(), py.min(), px_.max(), py.max(), len(pix)))
    return comps

def near(c, tol):
    return (abs(r-c[0])<tol) & (abs(g-c[1])<tol) & (abs(b-c[2])<tol)

# callout fills per spec: light green C8E6C9, light pink F2C6C6, tan D2A679,
# yellow FFFF99, light blue D6E8F8. Panel fills FBE5D6 / D9F2D9. Highlight FFFF00.
targets = {
    "callout_lightgreen(C8E6C9)": (200, 230, 201),
    "callout_lightpink(F2C6C6)":  (242, 198, 198),
    "callout_tan(D2A679)":        (210, 166, 121),
    "callout_yellow(FFFF99)":     (255, 255, 153),
    "callout_lightblue(D6E8F8)":  (214, 232, 248),
    "panel_peach(FBE5D6)":        (251, 229, 214),
    "panel_lightgreen(D9F2D9)":   (217, 242, 217),
    "highlight_yellow(FFFF00)":   (255, 255, 0),
    "tanbox(D9A05B)":             (217, 160, 91),
    "orange(E8A33D)":             (232, 163, 61),
    "brown(C69C6D)":              (198, 156, 109),
    "green(A9D18E)":              (169, 209, 142),
    "vkblue(4472C4)":             (68, 114, 196),
    "gray(BFBFBF)":               (191, 191, 191),
}
print("\n-- components (min_area 120) x0,y0 -> x1,y1 (area) --")
for name, c in targets.items():
    m = near(c, 22)
    # exclude chrome panel/badge region artifacts by noting all; print all comps
    comps = components(m, 120)
    comps.sort(key=lambda t: (t[1], t[0]))
    if comps:
        print(f"{name}:")
        for x0, y0, x1, y1, a in comps[:14]:
            print(f"   x{x0}-{x1} y{y0}-{y1}  (w{x1-x0+1} h{y1-y0+1}) n={a}")
    else:
        print(f"{name}: NONE (mask n={int(m.sum())})")
