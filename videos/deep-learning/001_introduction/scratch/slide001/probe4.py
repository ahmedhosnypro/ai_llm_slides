#!/usr/bin/env python3
"""Probe 4: italic detection via isolated vertical stems (leftmost ink in a narrow
x-window that contains only the first glyph's stem)."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
core_red = (r > 140) & (g < 60) & (b < 60)
core_blue = (b > 110) & (r < 90) & (g < 90)

def stem(y0, y1, x0, x1, mask, label):
    pts = []
    for y in range(y0, y1):
        xs = np.where(mask[y, x0:x1])[0]
        if len(xs):
            pts.append((y, x0 + xs.min(), x0 + xs.max()))
    if len(pts) < 6:
        print(f"{label}: too few rows ({len(pts)})")
        return
    ys = np.array([p[0] for p in pts]); lx = np.array([p[1] for p in pts], dtype=float)
    slope = np.polyfit(ys, lx, 1)[0]
    lean = lx[-1] - lx[0]
    print(f"{label}: rows {ys.min()}-{ys.max()} stem-left {lx.min():.0f}->{lx.max():.0f} "
          f"(lean {lean:+.0f}px over {ys.max()-ys.min()} rows, slope {slope:+.3f}) "
          f"{'ITALIC' if slope > 0.12 else 'UPRIGHT' if slope < 0.05 else 'ambiguous'}")

print("=== stems ===")
stem(292, 307, 452, 470, core_red,  "'P' of Prepared By      (red)")
stem(317, 334, 360, 380, core_blue, "'D' of prepared name   (blue)")
stem(344, 358, 394, 412, core_blue, "'k' of prepared email  (blue)")
stem(398, 412, 70, 95, core_red,    "'I' of Instructors:    (red)")
stem(426, 441, 114, 134, core_blue, "'D' of instr name1     (blue)")
stem(452, 464, 114, 132, core_blue, "'k' of instr email1    (blue)")
stem(472, 488, 113, 133, core_blue, "'D' of instr name2     (blue)")
stem(497, 511, 113, 131, core_blue, "'k' of instr email2    (blue)")
stem(129, 171, 240, 285, core_red,  "'D' of title Deep      (red)")
stem(199, 242, 330, 360, core_red,  "'D' of title DSAI      (red)")
