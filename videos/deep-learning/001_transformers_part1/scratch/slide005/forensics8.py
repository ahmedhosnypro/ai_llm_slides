#!/usr/bin/env python3
"""Forensics 8: final resolution — luma+hue cell classification, faint-stroke deviation maps."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0].astype(float), im[:, :, 1].astype(float), im[:, :, 2].astype(float)

TOP, PITCH, NCELL = 178.5, (462.5 - 178.5) / 18, 18
STACKS = [("WV", 163, 244), ("FM1", 308, 390), ("FM2", 456, 537), ("FM3", 598, 679), ("FM4", 737, 818)]

def lum(px):
    return 0.299 * px[0] + 0.587 * px[1] + 0.114 * px[2]

def hueclass(a):  # avg rgb tuple
    R, G, B = a
    L = lum((R, G, B))
    if L > 246: return "WHITE"
    if 226 <= L <= 244 and abs(R - G) < 8 and abs(G - B) < 12: return "PANEL"
    if L < 210 and abs(R - G) < 14 and abs(G - B) < 14: return "GRAY/OUTLINE"
    if L >= 205 and R - G > 18 and G - B > -8 and R - B > 25: return "YELLOW-ish"
    if 200 <= L <= 232 and R - G > 18 and G - B > -20 and B < 215: return "PEACH-ish"
    if G - R > 15 and B - R > 15 and L > 175: return "CYAN-ish"
    if R - G > 18 and B - G > 18 and L > 200: return "PINK-ish"
    if G - R > 10 and G - B > 5 and L > 215: return "PGREEN-ish"
    return f"OTHER(luma{L:.0f})"

print("=== per-cell classification (tight 12px interior strip, hue+luma) ===")
for nm, x0, x1 in STACKS:
    line = []
    for ci in range(NCELL):
        y0 = int(TOP + PITCH * ci) + 4
        y1 = int(TOP + PITCH * (ci + 1)) - 4
        cx0, cx1 = (x0 + x1) // 2 - 6, (x0 + x1) // 2 + 6
        a = tuple(round(v, 1) for v in im[y0:y1, cx0:cx1].reshape(-1, 3).mean(axis=0))
        line.append(f"{ci+1}:{hueclass(a)}")
    print(f"{nm}: " + " | ".join(line))

print("\n=== deviation maps (non-panel, non-outline pixels) ===")
def devmap(xa, xb, ya, yb, label, thr=26):
    print(f"--- {label} ({xa}-{xb}, {ya}-{yb}) ---")
    for y in range(ya, yb):
        row = []
        for x in range(xa, xb):
            px = im[y, x]
            d_panel = abs(px[0]-233)+abs(px[1]-233)+abs(px[2]-231)
            d_line = abs(px[0]-167)+abs(px[1]-175)+abs(px[2]-184)
            if min(d_panel, d_line) > thr:
                row.append("X")
            else:
                row.append(".")
        print(f"{y:3d} " + "".join(row))

# gap1 upper: triangle 1 (x246-308, y176-232)
devmap(246, 308, 178, 230, "gap1 upper")
