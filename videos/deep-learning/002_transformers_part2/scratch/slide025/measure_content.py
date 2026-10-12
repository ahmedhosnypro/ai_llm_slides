#!/usr/bin/env python3
"""Content geometry measurement for slide_025.jpg.
Reports ink bboxes + color censuses per region of interest (frame px).
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def census(x0, y0, x1, y1, n=6):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    q = (sub // 24 * 24)
    keys, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    tot = len(sub)
    return [(tuple(int(v) for v in keys[i]), round(counts[i] / tot * 100, 1)) for i in order]

def ink_bbox(x0, y0, x1, y1, bg, tol=28):
    """bbox of pixels differing from bg color by > tol (max channel)."""
    sub = a[y0:y1, x0:x1]
    d = np.abs(sub - np.array(bg)).max(axis=2)
    ys, xs = np.nonzero(d > tol)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())

GRAY = (234, 234, 234)
WHITE = (255, 255, 255)

regions = {
    "title":        (200, 60, 760, 92, GRAY),
    "subtitle":     (150, 92, 810, 118, GRAY),
    "left_panel":   (85, 155, 320, 385, GRAY),
    "motor_area":   (100, 165, 315, 380, WHITE),
    "arrow":        (330, 205, 460, 320, GRAY),
    "right_panel":  (440, 130, 850, 400, GRAY),
    "summary":      (120, 395, 840, 460, GRAY),
    "footer":       (60, 462, 650, 512, GRAY),
}
for name, (x0, y0, x1, y1, bg) in regions.items():
    bb = ink_bbox(x0, y0, x1, y1, bg)
    print(f"{name}: ink bbox = {bb}")

print("\ncolor censuses:")
print("title:", census(340, 66, 580, 90))
print("subtitle:", census(200, 92, 720, 116))
print("left panel border sample row 172:", census(95, 168, 315, 178))
print("callout:", census(120, 305, 235, 360))
print("arrow:", census(345, 215, 410, 250))
print("arrow label:", census(310, 258, 450, 315))
print("right panel border:", census(450, 140, 840, 152))
print("ring red @right:", census(770, 255, 800, 280))
print("ring green @right:", census(760, 285, 795, 310))
print("summary:", census(160, 400, 800, 455))
print("footer:", census(70, 465, 600, 510))
