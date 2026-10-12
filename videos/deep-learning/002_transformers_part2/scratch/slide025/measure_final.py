#!/usr/bin/env python3
"""Final precise measurements: hub, dashes, period arrow, inner text bands."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
dark = (r < 130) & (g < 130) & (b < 130)

# ---- 1. hub circle: gray outline. Search region x 575..625, y 250..295
grayline = (np.abs(r - g) < 30) & (np.abs(g - b) < 30) & (r > 100) & (r < 215)
win = grayline[248:296, 572:628]
ys, xs = np.nonzero(win)
pts = np.stack([xs + 572, ys + 248], axis=1)
# fit circle by algebraic least squares (Kasa)
x, y = pts[:, 0].astype(float), pts[:, 1].astype(float)
A = np.stack([x, y, np.ones_like(x)], axis=1)
bb = x**2 + y**2
sol, *_ = np.linalg.lstsq(A, bb, rcond=None)
cx, cy = sol[0] / 2, sol[1] / 2
rad = np.sqrt(sol[2] + cx**2 + cy**2)
print(f"hub circle fit: center ({cx:.1f},{cy:.1f}) r={rad:.1f}  (n={len(pts)})")

# ---- 2. dashed lines: dark px radiating right from hub, exclude text/arrow regions
hub = (cx, cy)
Y0, Y1 = int(cy - 60), int(cy + 60)
X0 = int(cx + rad + 2)
win2 = dark[Y0:Y1, X0:835]
ys2, xs2 = np.nonzero(win2)
pts2 = np.stack([xs2 + X0, ys2 + Y0], axis=1).astype(float)
d = np.hypot(pts2[:, 0] - hub[0], pts2[:, 1] - hub[1])
th = np.degrees(np.arctan2(-(pts2[:, 1] - hub[1]), pts2[:, 0] - hub[0]))  # y up
sel = (d > rad + 4) & (d < 160)
print("dash px:", sel.sum())
ths, ds = th[sel], d[sel]
# two clusters: theta<0 and theta>0 (split at 0)
for name, m in (("upper(theta<0)", ths < 0), ("lower(theta>0)", ths > 0)):
    if m.sum() > 5:
        print(f"  {name}: theta {ths[m].min():.1f}..{ths[m].max():.1f} median {np.median(ths[m]):.1f}; r {ds[m].min():.1f}..{ds[m].max():.1f}")

# ---- 3. vertical period double-arrow: dark px in x-band right of dashes
# find via column census in region x 700..780, y 240..320, excluding text (text x>735)
seg = dark[235:325, 690:740]
colc = seg.sum(axis=0)
print("arrow region col census (x 690..739):", {690 + j: int(c) for j, c in enumerate(colc) if c > 3})
ys3, xs3 = np.nonzero(seg)
if len(xs3):
    print("  bbox:", (690 + xs3.min(), 235 + ys3.min(), 690 + xs3.max(), 235 + ys3.max()))

# ---- 4. text bands (tight windows, print row profiles)
def prof(y0, y1, x0, x1, thresh=130, label=""):
    seg = (a[y0:y1, x0:x1].max(axis=2) < thresh)
    rows = seg.sum(axis=1)
    print(f"{label} rowprof y{y0}..{y1}:", "".join("#" if c > 1 else "." for c in rows))
    cols = seg.sum(axis=0)
    xs4 = np.nonzero(cols > 0)[0]
    if len(xs4):
        print(f"   x extent: {x0+xs4.min()}..{x0+xs4.max()}")

prof(196, 216, 548, 645, label="RotationDirection")
prof(216, 236, 565, 630, label="CCW/CW")
prof(196, 212, 718, 745, label="cos")
prof(216, 234, 726, 752, label="sin")
prof(286, 308, 545, 650, label="LineCount=16")
prof(306, 322, 535, 660, label="(16 signal periods per")
prof(320, 340, 560, 630, label="revolution)")
prof(262, 290, 735, 830, label="SinCosSignalPeriod")
prof(206, 232, 210, 300, thresh=120, label="AC Motor")
# callout text: dark-red on tan; use r>100, r-g>50
seg = a[305:360, 115:235]
tr = (seg[...,0] - seg[...,1] > 55) & (seg[...,0] - seg[...,2] > 45) & (seg[...,0] > 90)
rows = tr.sum(axis=1)
print("callout text rowprof y305..360:", "".join("#" if c > 1 else "." for c in rows))
cols = tr.sum(axis=0)
xs5 = np.nonzero(cols > 0)[0]
if len(xs5): print("   x extent:", 115 + xs5.min(), "..", 115 + xs5.max())
print("callout text color sample:", [tuple(a[yy, xx]) for yy, xx in ((318, 135), (318, 150), (338, 135), (340, 150))])
# curved rotation arrow bbox
seg = dark[160:196, 500:700]
ys6, xs6 = np.nonzero(seg)
if len(xs6):
    print("curved arrow bbox:", (500 + xs6.min(), 160 + ys6.min(), 500 + xs6.max(), 160 + ys6.max()))
# cos/sin thin arrows (colored)
redarr = (r - g > 60) & (r - b > 50) & (r > 110)
seg = redarr[205:240, 690:730]
ys7, xs7 = np.nonzero(seg)
if len(xs7): print("cos arrow red bbox:", (690 + xs7.min(), 205 + ys7.min(), 690 + xs7.max(), 205 + ys7.max()))
grn = (g - r > 30) & (g - b > 20) & (g > 70)
seg = grn[225:260, 690:740]
ys8, xs8 = np.nonzero(seg)
if len(xs8): print("sin arrow green bbox:", (690 + xs8.min(), 225 + ys8.min(), 690 + xs8.max(), 225 + ys8.max()))
