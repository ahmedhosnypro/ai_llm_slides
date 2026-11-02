import os
from PIL import Image
import numpy as np
NS = os.environ.get("NS", "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure")
im = np.array(Image.open(f"{NS}/unique_slides/slide_002.jpg").convert("RGB")).astype(int)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > 140) & (R - G > 60) & (R - B > 60)
green = (G > 100) & (G - R > 40) & (G - B > 40)
blue = (B > 120) & (B - R > 40) & (B - G > 30)

def stats(mask, name, x0=0, x1=960, y0=0, y1=540):
    m = np.zeros_like(mask); m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(xs) == 0:
        print(name, "none"); return m
    print(name, "bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
    return m

mred = stats(red, "red left", 0, 620, 100, 520)
mgreen = stats(green, "green mid", 300, 620, 100, 520)
mblue = stats(blue, "blue act", 560, 960, 0, 220)
for name, m in (("red", mred), ("green", mgreen)):
    col = m[150:470, :].sum(axis=0)
    peaks = [(x, int(c)) for x, c in enumerate(col) if c > 120]
    print(name, "tall cols:", peaks)
    row = m.sum(axis=1)
    rpeaks = [(y, int(c)) for y, c in enumerate(row) if c > 100]
    print(name, "wide rows:", rpeaks[:40])
# dark ink (any non-white) in left area to find pane borders
dark = (R < 120) & (G < 120) & (B < 120)
mdark = stats(dark, "dark left", 60, 620, 130, 510)
col = mdark.sum(axis=0)
print("dark tall cols:", [(x, int(c)) for x, c in enumerate(col) if c > 200])
row = mdark.sum(axis=1)
print("dark wide rows:", [(y, int(c)) for y, c in enumerate(row) if c > 300])
EOF_MARKER_NOT_USED = None
