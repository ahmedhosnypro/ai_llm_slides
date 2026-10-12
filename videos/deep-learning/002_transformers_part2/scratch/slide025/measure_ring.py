#!/usr/bin/env python3
"""Ring radial analysis + remaining elements for slide_025.jpg."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)
darkm = (r < 120) & (g < 120) & (b < 120)

# ---- ring center search: use red trace pixels in panel, excluding label regions
# panel interior approx x 455..830, y 145..385. cos label ~x>700,y<240; exclude.
Y0, Y1, X0, X1 = 145, 390, 455, 835
sub_red = np.zeros_like(redm)
sub_red[Y0:Y1, X0:X1] = redm[Y0:Y1, X0:X1]
# exclude cos/sin label region (top right) and panel border
sub_red[:250, 700:] = False
sub_red[:150, :] = False
sub_red[385:, :] = False
sub_red[:, :458] = False
sub_red[:, 832:] = False
ys, xs = np.nonzero(sub_red)
print("ring red trace px count:", len(xs), "bbox:", (xs.min(), ys.min(), xs.max(), ys.max()))

def radius_stats(cx, cy, mask, rmin=40, rmax=160):
    yy, xx = np.nonzero(mask)
    d = np.hypot(xx - cx, yy - cy)
    th = np.degrees(np.arctan2(yy - cy, xx - cx)) % 360
    sel = (d > rmin) & (d < rmax)
    d, th = d[sel], th[sel]
    bins = ((th + 1.125) // 2.25).astype(int)  # 2.25-degree bins
    means = []
    for k in np.unique(bins):
        means.append(d[bins == k].mean())
    return np.mean(means), np.std(means)

best = None
for cy in range(255, 280):
    for cx in range(600, 630):
        m, s = radius_stats(cx, cy, sub_red, 50, 150)
        if best is None or s < best[0]:
            best = (s, cx, cy, m)
print(f"best center: std={best[0]:.2f} center=({best[1]},{best[2]}) meanR={best[3]:.1f}")

cx, cy = best[1], best[2]
# per-angle min/max radius for red and green (finer bins)
for name, mask in (("red", sub_red), ("green", None)):
    if mask is None:
        m2 = np.zeros_like(greenm)
        m2[Y0:Y1, X0:X1] = greenm[Y0:Y1, X0:X1]
        m2[:250, 700:] = False  # exclude sin label? sin label ~ (730..752, 222..238)
        m2[:150, :] = False; m2[385:, :] = False; m2[:, :458] = False; m2[:, 832:] = False
        mask = m2
    yy, xx = np.nonzero(mask)
    d = np.hypot(xx - cx, yy - cy)
    th = np.degrees(np.arctan2(yy - cy, xx - cx)) % 360
    sel = (d > 40) & (d < 160)
    d, th = d[sel], th[sel]
    bins = ((th) // 5).astype(int)
    rows = []
    for k in range(72):
        selk = bins == k
        if selk.sum() > 3:
            rows.append((k * 5, round(d[selk].min(), 1), round(d[selk].max(), 1), round(d[selk].mean(), 1)))
    print(f"-- {name}: angle,(rmin,rmax,rmean) every 5deg --")
    print(rows)

# white center circle: find gray outline circle near center
grayline = (np.abs(r - g) < 20) & (np.abs(g - b) < 20) & (r > 100) & (r < 200)
sub = grayline[cy - 40:cy + 40, cx - 40:cx + 40]
yy, xx = np.nonzero(sub)
if len(xx):
    print("center circle gray bbox (rel to center):", (xx.min() - 40, yy.min() - 40, xx.max() - 40, yy.max() - 40))

# dashed radial lines: dark pixels along rays to the right, radius 40..150, angle near 0 (+-25deg)
sub_dark = np.zeros_like(darkm)
sub_dark[Y0:Y1, X0:X1] = darkm[Y0:Y1, X0:X1]
yy, xx = np.nonzero(sub_dark)
d = np.hypot(xx - cx, yy - cy)
th = np.degrees(np.arctan2(yy - cy, xx - cx))
sel = (d > 30) & (d < 160) & (np.abs(th) < 30)
print("dashed-line dark px in right sector:", sel.sum(), "theta range:", th[sel].min() if sel.sum() else None, th[sel].max() if sel.sum() else None)
if sel.sum():
    ths = th[sel]; ds = d[sel]
    # cluster by theta
    import collections
    hist = collections.Counter((ths // 2).astype(int) * 2)
    print("theta histogram (2deg bins):", dict(sorted(hist.items())))
