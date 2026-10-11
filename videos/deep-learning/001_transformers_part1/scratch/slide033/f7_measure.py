#!/usr/bin/env python3
"""Comprehensive structured measurements of slide_033.jpg."""
import numpy as np
from PIL import Image
from scipy import ndimage

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[..., 0], a[..., 1], a[..., 2]

def mode_color(mask, label):
    sel = a[mask]
    if len(sel) == 0:
        print(f"{label}: none")
        return
    q = (sel // 4 * 4)
    from collections import Counter
    c = Counter(map(tuple, q)).most_common(3)
    print(f"{label}: n={len(sel)} modes={c}")

def bbox_of(mask, min_area=20):
    lab, n = ndimage.label(mask, np.ones((3, 3)))
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_area:
            continue
        out.append((int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), len(xs)))
    out.sort(key=lambda r: (r[2], r[0]))
    return out

print("=== 1. FILLS (modes) ===")
mode_color((R > 240) & (G > 240) & (B > 240) & (np.abs(R - G) < 8), "white")
mode_color((np.abs(R - 247) < 8) & (np.abs(G - 226) < 8) & (np.abs(B - 205) < 8), "peach")
mode_color((R > 235) & (G > 235) & (B > 235) & (R - B > 90) & (G - B > 90), "yellow")
mode_color((np.abs(R - 219) < 12) & (np.abs(G - 203) < 12) & (np.abs(B - 187) < 12), "taupe")
mode_color((R > 240) & (G > 210) & (G < 240) & (B > 240), "pink/orchid")
mode_color((np.abs(R - 231) < 10) & (np.abs(G - 255) < 10) & (np.abs(B - 233) < 10), "pale green")

print("=== 2. YELLOW regions (W boxes, badge) ===")
ym = (R > 240) & (G > 240) & (R - B > 80) & (G - B > 80)
for x0, x1, y0, y1, ar in bbox_of(ym, 60):
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={x1-x0+1} h={y1-y0+1} a={ar}")

print("=== 3. TAUPE regions (Dot Product) ===")
tm = (np.abs(R - 219) < 14) & (np.abs(G - 203) < 14) & (np.abs(B - 187) < 14)
for x0, x1, y0, y1, ar in bbox_of(tm, 150):
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={x1-x0+1} h={y1-y0+1} a={ar}")

print("=== 4. PINK regions (Softmax) ===")
pm = (R > 240) & (G > 200) & (G < 242) & (B > 240) & (R - G > 6) & (B - G > 6)
for x0, x1, y0, y1, ar in bbox_of(pm, 150):
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={x1-x0+1} h={y1-y0+1} a={ar}")

print("=== 5. PALE-GREEN fill regions (containers) ===")
gm = (G > 235) & (R > 215) & (B > 215) & (G - R > 6) & (G - B > 6)
for x0, x1, y0, y1, ar in bbox_of(gm, 400):
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={x1-x0+1} h={y1-y0+1} a={ar}")

print("=== 6. PALE-YELLOW regions (pills) ===")
pym = (R > 244) & (G > 244) & (B > 185) & (B < 232) & (R - B > 30) & (G - B > 30)
for x0, x1, y0, y1, ar in bbox_of(pym, 100):
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={x1-x0+1} h={y1-y0+1} a={ar}")

print("=== 7. WHITE regions inside panel (boxes/circles; exclude chrome) ===")
wm = (R > 246) & (G > 246) & (B > 246)
wm[:108, :] = False; wm[522:, :] = False; wm[:, :54] = False; wm[:, 866:] = False
for x0, x1, y0, y1, ar in bbox_of(wm, 120):
    print(f"  x[{x0}..{x1}] y[{y0}..{y1}] w={x1-x0+1} h={y1-y0+1} a={ar}")

print("=== 8. VERTICAL red arrow lines (cols 530..632) ===")
redm = (R - G > 50) & (R - B > 50) & (R > 130)
for cx in (534, 565, 596, 627):
    col = redm[:, cx - 4:cx + 5].any(axis=1)
    ys = np.nonzero(col)[0]
    # contiguous runs
    runs = []
    if len(ys):
        start = prev = ys[0]
        for y in ys[1:]:
            if y > prev + 3:
                runs.append((start, prev)); start = y
            prev = y
        runs.append((start, prev))
    print(f"  x~{cx}: red runs y = {[(int(s), int(e)) for s, e in runs if e - s > 2]}")

print("=== 9. Border color samples ===")
print("  Sigma box top border rows 193-195, x 560:", [tuple(a[y, 560]) for y in range(192, 197)])
print("  Sigma box left border cols x 512-516 at y 205:", [tuple(a[205, x]) for x in range(510, 518)])
print("  peach panel top border: rows 106-110 at x 400:", [tuple(a[y, 400]) for y in range(105, 111)])
print("  peach panel left border: cols 50-56 at y 300:", [tuple(a[300, x]) for x in range(49, 57)])
print("  W_k box border: row 228 at x 160-195:", [tuple(a[228, x]) for x in range(155, 200, 5)])
print("  W_k box border rows 226-231 at x 175:", [tuple(a[y, 175]) for y in range(224, 233)])
print("  badge ring sample rows 50-92 col 875-915:")
badge = a[48:94, 870:918]
from collections import Counter
bc = Counter(map(tuple, badge.reshape(-1, 3))).most_common(10)
for c, n in bc:
    print("   ", c, n)
