#!/usr/bin/env python3
# debug4.py — remaining measurements: box borders, softmax text hist, outline color,
# green circle profile, cursor region, brace ends.
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_056.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

# 1) softmax white text: per-column count, then cluster
bar = a[230:262, 170:826]
wm = (bar[..., 0] > 190) & (bar[..., 1] > 190) & (bar[..., 2] > 190)
colhit = wm.sum(axis=0)
hits = [(i + 170, int(c)) for i, c in enumerate(colhit) if c > 0]
print("softmax white col hits (first 12):", hits[:12])
print("softmax white col hits (last 12):", hits[-12:])
# row extent of white pixels with x in 400..600
wm2 = wm[:, 230:430]
rows = np.nonzero(wm2.sum(axis=1))[0]
print("softmax white rows (x 400..600):", [(int(rr) + 230) for rr in rows])
ys, xs = np.nonzero(wm)
print("white bbox:", xs.min() + 170, xs.max() + 170, ys.min() + 230, ys.max() + 230, "n=", len(xs))

# 2) box borders with relaxed green
greenish = (a[..., 1] - a[..., 0] > 22) & (a[..., 1] - a[..., 2] > 15) & (a[..., 1] > 110)
print("top border rows:", [(y, int(greenish[y, 170:830].sum()), tuple(a[y, 400])) for y in range(292, 304) if greenish[y, 170:830].sum() > 50])
print("bottom border rows:", [(y, int(greenish[y, 170:830].sum()), tuple(a[y, 400])) for y in range(428, 440) if greenish[y, 170:830].sum() > 50])
print("left border cols:", [(x, int(greenish[305:425, x].sum()), tuple(a[370, x])) for x in range(158, 172) if greenish[305:425, x].sum() > 30])
print("right border cols:", [(x, int(greenish[305:425, x].sum()), tuple(a[370, x])) for x in range(826, 840) if greenish[305:425, x].sum() > 30])

# 3) pale circle outline color: darkest pixels around first circle (center ~197,159 r~17)
reg = a[140:180, 178:218].reshape(-1, 3)
lum = reg.sum(axis=1)
idx = np.argsort(lum)[:15]
print("darkest ring px:", [tuple(reg[i]) for i in idx])

# 4) green circle col profile at x=398 (print all)
col = a[386:438, 398]
print("col x=398:", [(386 + i, tuple(col[i])) for i in range(52)])

# 5) cursor region right of text end (x 605..665, y 460..500)
def nonbg(band, tol=25):
    return (np.abs(band[..., 0] - 233) > tol) | (np.abs(band[..., 1] - 233) > tol) | (np.abs(band[..., 2] - 231) > tol)
reg = a[455:505, 605:670]
m = nonbg(reg)
ys, xs = np.nonzero(m)
print("cursor-region nonbg n:", len(xs))
if len(xs):
    print("  x", xs.min() + 605, xs.max() + 605, "y", ys.min() + 455, ys.max() + 455, "mean", reg[ys, xs].mean(axis=0).round(0))
# also inside bar after text: bar is dark blue; find light pixels x 610..830
reg2 = a[462:500, 610:830]
m2 = (reg2[..., 0] > 120) & (reg2[..., 1] > 120)
ys2, xs2 = np.nonzero(m2)
print("in-bar light px after text:", len(xs2), ("x", xs2.min() + 610, xs2.max() + 610, "y", ys2.min() + 462, ys2.max() + 462) if len(xs2) else "")

# 6) brace: per-row x extent (apex/ends shape)
reddish = (a[..., 0] - a[..., 1] > 50) & (a[..., 0] - a[..., 2] > 40) & (a[..., 0] > 90)
for y in range(119, 137):
    xs = np.nonzero(reddish[y, 150:850])[0]
    if len(xs):
        print(f"brace y={y}: x {xs.min() + 150}..{xs.max() + 150} n={len(xs)}")

# 7) brace color sample
print("brace px @ (499,121):", tuple(a[121, 499]), " @(200,133):", tuple(a[133, 200]))

# 8) pale circle fill color histogram (mode) in first circle
reg = a[145:175, 182:212].reshape(-1, 3)
from collections import Counter
c = Counter(map(tuple, reg))
print("pale fill top colors:", c.most_common(5))

# 9) magenta circle diameter check: col profile first magenta center (frame ~201?)
# magenta centers slide x: 191.3 -> frame mx^-1: fx = 17.63 + 191.3*0.96123 = 201.5
col = a[316:356, 201]
print("magenta col x=201:", [(316 + i, tuple(col[i])) for i in range(0, 40, 2)])
