#!/usr/bin/env python3
"""Precise measurement: stroke centroids, title lines (borders excluded), colors, cursor."""
from PIL import Image
import numpy as np

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_058.jpg"
im = np.asarray(Image.open(IM).convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[..., 0], im[..., 1], im[..., 2]
red = (R > 110) & (R - G > 50) & (R - B > 40)

def wcentroid(cnt, idxs):
    v = cnt.astype(float)
    return (idxs * v).sum() / v.sum()

# ---- stroke centroids (exclude title rows for cols; exclude border cols for rows)
# left stroke: cols 55..62, rows 60..500 (avoid badge & top/bottom strokes)
seg = red[60:500, 55:63]
cnt = seg.sum(axis=0)
cols = np.arange(55, 63)
print("left stroke cols:", {int(c): int(n) for c, n in zip(cols, cnt) if n > 0})
left_c = wcentroid(cnt, cols)
# right stroke: cols 898..906
seg = red[60:500, 898:907]
cnt = seg.sum(axis=0)
cols = np.arange(898, 907)
print("right stroke cols:", {int(c): int(n) for c, n in zip(cols, cnt) if n > 0})
right_c = wcentroid(cnt, cols)
# top stroke: rows 38..48, cols 100..850
seg = red[38:49, 100:850]
cnt = seg.sum(axis=1)
rows = np.arange(38, 49)
print("top stroke rows:", {int(r): int(n) for r, n in zip(rows, cnt) if n > 0})
top_c = wcentroid(cnt, rows)
# bottom stroke: rows 512..520
seg = red[512:521, 100:850]
cnt = seg.sum(axis=1)
rows = np.arange(512, 521)
print("bottom stroke rows:", {int(r): int(n) for r, n in zip(rows, cnt) if n > 0})
bot_c = wcentroid(cnt, rows)
print(f"stroke centroids: left {left_c:.2f} right {right_c:.2f} top {top_c:.2f} bottom {bot_c:.2f}")

# ---- fit mapping to slide chrome landmarks (42, 919, 45, 540)
import numpy.linalg as la
fx = np.array([left_c, right_c]); sy = np.array([42, 919])
A = np.vstack([sy, np.ones(2)]).T
s_x, a = la.lstsq(A, fx, rcond=None)[0]
fy = np.array([top_c, bot_c]); sl = np.array([45, 540])
A = np.vstack([sl, np.ones(2)]).T
s_y, b = la.lstsq(A, fy, rcond=None)[0]
print(f"fit: frame_x = {a:.3f} + {s_x:.5f}*slide_x ; frame_y = {b:.3f} + {s_y:.5f}*slide_y")
inv = lambda ptx, pty: ((ptx - a) / s_x, (pty - b) / s_y)
# badge cross-check
bx, by = inv(875.5, 70.5)
print(f"badge frame(875.5,70.5) -> slide ({bx:.1f},{by:.1f}) vs house (893,71): d=({bx-893:.1f},{by-71:.1f})")

# ---- title lines (exclude border strokes: x 70..890)
tit = red.copy()
tit[:, :70] = False; tit[:, 891:] = False
band = tit[150:400, :]
rr = band.sum(axis=1)
runs = []; inrun = False
for i, v in enumerate(rr):
    if v > 3 and not inrun: start = i; inrun = True
    elif v <= 3 and inrun: runs.append((start + 150, i - 1 + 150)); inrun = False
if inrun: runs.append((start + 150, 399))
print("title line runs:", runs)
for (ya, yb) in runs:
    sub = tit[ya:yb + 1]
    yy, xx = np.nonzero(sub)
    print(f"  L y{ya}..{yb} (h{yb-ya+1}) x{xx.min()}..{xx.max()} (w{xx.max()-xx.min()+1}) cx {(xx.min()+xx.max())/2:.1f} n {len(xx)}")
    # core color census: most saturated red pixels
    px = im[ya:yb + 1][sub]
    # darkest/quartile by luminance
    lum = px.sum(axis=1)
    core = px[lum <= np.percentile(lum, 25)]
    print(f"    core RGB mean {core.mean(axis=0).round(1)} median {np.median(core, axis=0)}")

# ---- cursor artifact: black ink inside panel (exclude strip rows >=516)
blk = (R < 90) & (G < 90) & (B < 90)
blk[516:, :] = False
blk[:, :70] = False; blk[:, 891:] = False; blk[:50, :] = False
ys, xs = np.nonzero(blk)
if len(xs):
    print("black ink in panel bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
    # cluster rows
    import collections
    print("  sample rows:", sorted(collections.Counter(ys // 10 * 10).items())[:20])

# ---- badge ring: purple pixels near badge
pur = (B > 120) & (B - G > 30) & (R > 80) & (R < 180)
pur[:40, :] = False; pur[110:, :] = False; pur[:, :840] = False
ys, xs = np.nonzero(pur)
if len(xs):
    print("badge ring bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs),
          "core", np.median(im[ys, xs], axis=0))

# ---- panel gray + border color census
panel = im[350:400, 200:800].reshape(-1, 3)
print("panel gray median", np.median(panel, axis=0))
border_px = im[42, 100:850][red[42, 100:850]]
print("top border core median", np.median(border_px, axis=0))
badge_fill = im[65:78, 865:885].reshape(-1, 3)
print("badge fill median", np.median(badge_fill, axis=0))
