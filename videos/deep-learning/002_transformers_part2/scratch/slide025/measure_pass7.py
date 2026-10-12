#!/usr/bin/env python3
"""Pass 7: (a) ring center+phase robust LSQ fit with 1-cycle nuisance; (b) clean dash
extraction (excl. arrow/label); (c) motor silhouette below y300 right of callout;
(d) callout text color core census; (e) subtitle/footer/title color cores."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)

# ---- (a) ring center + phase: LSQ r(theta) = R0 + C*cos(16th)+D*sin(16th) + dx*cos t + dy*sin t
# use BOTH traces' stroke-centerline samples (red only, cleaner mask)
Y0, Y1, X0, X1 = 145, 392, 455, 760
sub = np.zeros_like(redm)
sub[Y0:Y1, X0:X1] = redm[Y0:Y1, X0:X1]
sub[:250, 700:] = False  # cos label zone
ys, xs = np.nonzero(sub)
for cx0, cy0 in ((600, 266), (604, 273)):
    d = np.hypot(xs - cx0, ys - cy0)
    t = np.arctan2(ys - cy0, xs - cx0)  # y-down angle
    sel = (d > 60) & (d < 150)
    tt, dd = t[sel], d[sel]
    # bin by angle (1 deg), take median radius per bin -> centerline samples
    bins = ((np.degrees(tt)) % 360).astype(int)
    T, R = [], []
    for k in range(360):
        m = bins == k
        if m.sum() >= 3:
            T.append(k * np.pi / 180)
            R.append(np.median(dd[m]))
    T = np.array(T); R = np.array(R)
    n = len(T)
    M = np.stack([np.ones(n), np.cos(16 * T), np.sin(16 * T), np.cos(T), np.sin(T)], axis=1)
    sol, res, *_ = np.linalg.lstsq(M, R, rcond=None)
    R0, C16, S16, dx, dy = sol
    pred = M @ sol
    rms = np.sqrt(np.mean((R - pred) ** 2))
    amp = np.hypot(C16, S16)
    ph = np.degrees(np.arctan2(S16, C16))  # phase of cos term in image angle (y-down)
    print(f"center0 ({cx0},{cy0}): R0={R0:.1f} A={amp:.1f} phase16={ph:.1f}deg (image y-down) dx={dx:.1f} dy={dy:.1f} -> center=({cx0+dx:.1f},{cy0-dy:.1f}) rms={rms:.2f} n={n}")
    # residual after removing 16-period + offset (should be ~flat if center right)
    print(f"   note: dy sign: y-down angle t, radius measured from (cx0,cy0); center shift = (+dx, {-dy:.1f})")

# ---- (b) dashes: dark px, x 615..735, y 232..312, excl arrow (x>=708) & label (x>=734)
dark = (r < 130) & (g < 130) & (b < 130)
seg = np.zeros_like(dark)
seg[232:313, 615:736] = dark[232:313, 615:736]
seg[:, 708:] = False
ys2, xs2 = np.nonzero(seg)
# two-cluster split by sign of (y - line through center): use center (604,273)
for cx0, cy0 in ((604, 273),):
    d = np.hypot(xs2 - cx0, ys2 - cy0)
    th = np.degrees(np.arctan2(-(ys2 - cy0), xs2 - cx0))
    up = th > 0
    for nm, m in (("upper", up), ("lower", ~up)):
        if m.sum() > 5:
            # fit line y = y0 + slope*(x-604)
            X = xs2[m] - cx0
            Y = ys2[m] - cy0
            sl = np.polyfit(X, Y, 1)
            ang = np.degrees(np.arctan(-sl[0]))
            print(f"dash {nm}: n={m.sum()} ang={ang:.1f}deg intercept@x604 = {cy0 + sl[1]:.1f}")
            xr = xs2[m]
            o = np.argsort(xr)
            print(f"   x {xr[o].min()}..{xr[o].max()}; y at xmin {ys2[m][o][0]}, at xmax {ys2[m][o][-1]}")
            # dash pattern: runs along x
            xsorted = np.sort(np.unique(xr))
            runs = []
            s = xsorted[0]; p = xsorted[0]
            for v in xsorted[1:]:
                if v - p > 2:
                    runs.append((s, p)); s = v
                p = v
            runs.append((s, p))
            print(f"   x-runs (dash segments): {runs[:14]}")

# ---- (c) motor silhouette below y300, right of callout x>=228
ink_w = (np.abs(a - 255).max(axis=2) > 45)
seg = ink_w[296:370, 228:302]
rows = seg.sum(axis=1)
print("motor-below rowprof y296..369 x228..301:")
print("".join("#" if c > 30 else ("+" if c > 8 else ("." if c > 0 else " ")) for c in rows))
ys3, xs3 = np.nonzero(seg)
if len(xs3):
    print("  bbox:", (228 + xs3.min(), 296 + ys3.min(), 228 + xs3.max(), 296 + ys3.max()))
# left of callout? x104..120
seg = ink_w[296:370, 104:121]
ys4, xs4 = np.nonzero(seg)
if len(xs4):
    print("motor-below-left bbox:", (104 + xs4.min(), 296 + ys4.min(), 104 + xs4.max(), 296 + ys4.max()), "n", len(xs4))
# below callout? y355..368
seg = ink_w[355:370, 104:302]
ys5, xs5 = np.nonzero(seg)
if len(xs5):
    print("below-callout bbox:", (104 + xs5.min(), 355 + ys5.min(), 104 + xs5.max(), 355 + ys5.max()), "n", len(xs5))

# ---- (d) callout text color: darkest 15% in text bands
seg = a[306:346, 140:216].reshape(-1, 3)
dk = seg[seg.max(axis=1) < 150]
if len(dk):
    print("callout text dark-px mean:", dk.mean(axis=0).round(1), "darkest-quartile mean:", dk[dk.sum(axis=1) <= np.percentile(dk.sum(axis=1), 25)].mean(axis=0).round(1), "n=", len(dk))

# ---- (e) color cores
def core(y0, y1, x0, x1, mask, label):
    sub2 = a[y0:y1, x0:x1]
    m = mask[y0:y1, x0:x1]
    px = sub2[m]
    if len(px):
        s = px.sum(axis=1)
        q = px[s <= np.percentile(s, 30)]
        print(f"{label}: core mean {q.mean(axis=0).round(1)} n={len(px)}")

core(96, 114, 208, 721, (b - r > 40) & (b - g > 30), "subtitle blue")
core(411, 450, 172, 814, (np.abs(a - 234).max(axis=2) > 60), "summary black")
core(473, 505, 83, 590, (b - r > 40) & (b - g > 30), "footer blue")
core(72, 88, 351, 573, redm, "title red")
core(219, 242, 349, 405, redm, "arrow red")
core(267, 312, 315, 441, redm, "arrow-label red")
core(203, 209, 724, 741, redm, "cos label")
core(223, 230, 733, 748, greenm, "sin label")
core(295, 302, 549, 628, (np.abs(a - 234).max(axis=2) > 60), "linecount black")
# tan callout fill core
seg = a[310:350, 126:222].reshape(-1, 3)
tan = seg[(seg[:, 0] > 200) & (seg[:, 2] > 120) & (seg[:, 2] < 205) & (seg[:, 0] - seg[:, 2] > 40)]
print("tan fill core:", tan.mean(axis=0).round(1) if len(tan) else None, "n=", len(tan))
# panel border green core
gm = (g - r > 30) & (g - b > 20) & (g > 70)
core(140, 145, 455, 830, gm, "right panel border green")
core(171, 176, 105, 300, gm, "left panel border green")
