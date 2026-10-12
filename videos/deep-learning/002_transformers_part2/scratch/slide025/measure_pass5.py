#!/usr/bin/env python3
"""Measurement pass 5: hub disk, callout text, period arrow column, dash endpoints."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# ---- hub: white disk
wm = (r > 240) & (g > 240) & (b > 240)
seg = wm[252:285, 578:615]
ys, xs = np.nonzero(seg)
print("hub white bbox:", (578 + xs.min(), 252 + ys.min(), 578 + xs.max(), 252 + ys.max()), "n=", len(xs))
cx = 578 + (xs.min() + xs.max()) / 2; cy = 252 + (ys.min() + ys.max()) / 2
print(f"hub center approx ({cx:.1f},{cy:.1f})")

# gray ring around hub
grayline = (np.abs(r - g) < 30) & (np.abs(g - b) < 30) & (r > 110) & (r < 210)
seg2 = grayline[int(cy) - 18:int(cy) + 18, int(cx) - 18:int(cx) + 18]
ys2, xs2 = np.nonzero(seg2)
if len(xs2):
    print("hub ring bbox:", (int(cx)-18+xs2.min(), int(cy)-18+ys2.min(), int(cx)-18+xs2.max(), int(cy)-18+ys2.max()))

# ---- callout text: dark-on-tan mask
seg3 = a[300:365, 110:240]
darktan = (seg3.max(axis=2) < 190) & (seg3[..., 0] - seg3[..., 2] > 25)
rows = darktan.sum(axis=1)
print("callout text rowprof y300..364:", "".join("#" if c > 1 else "." for c in rows))
bands = []
inb = False
for i, c in enumerate(rows):
    if c > 1 and not inb: s, inb = i, True
    elif c <= 1 and inb: bands.append((300 + s, 300 + i - 1)); inb = False
if inb: bands.append((300 + s, 300 + 64))
for (s, e) in bands:
    cols = darktan[s - 300:e - 300 + 1].sum(axis=0)
    xs3 = np.nonzero(cols > 0)[0]
    print(f"  callout line band y {s}..{e}  x {110+xs3.min()}..{110+xs3.max()}")
# text color census: darkest pixels
pix = seg3[darktan]
if len(pix):
    q = (pix // 16 * 16)
    keys, counts = np.unique(q, axis=0, return_counts=True)
    order = np.argsort(-counts)[:5]
    print("  text color modes:", [tuple(int(v) for v in keys[i]) for i in order])

# ---- period arrow column: dark px in x 714..726, y 230..320
seg4 = (a[230:325, 714:727].max(axis=2) < 130)
ys4, xs4 = np.nonzero(seg4)
colc = seg4.sum(axis=0)
print("period arrow col census x714..726:", {714 + j: int(c) for j, c in enumerate(colc) if c > 0})
if len(ys4):
    print("  y extent:", 230 + ys4.min(), "..", 230 + ys4.max())
    # width of arrow shaft: rows histogram
    rowc = seg4.sum(axis=1)
    print("  rowprof y230..324:", "".join("#" if c > 0 else "." for c in rowc))

# ---- dashed lines: endpoints. dark px, from hub, theta in [-30..-5] and [5..30], r in [hub_r+3 .. 170]
dashes = (a.max(axis=2) < 130)
yy, xx = np.nonzero(dashes[200:340, 600:835])
pts = np.stack([xx + 600, yy + 200], axis=1).astype(float)
d = np.hypot(pts[:, 0] - cx, pts[:, 1] - cy)
th = np.degrees(np.arctan2(-(pts[:, 1] - cy), pts[:, 0] - cx))
for name, lo, hi in (("upper", 4, 30), ("lower", -30, -4)):
    m = (th > lo) & (th < hi) & (d > 12) & (d < 175)
    if m.sum():
        print(f"{name} dash: n={m.sum()} theta {th[m].min():.1f}..{th[m].max():.1f} med {np.median(th[m]):.1f}; r {d[m].min():.1f}..{d[m].max():.1f}")
        far = pts[m][np.argmax(d[m])]
        near = pts[m][np.argmin(d[m])]
        print(f"   nearest {tuple(near)} farthest {tuple(far)}")

# ---- motor crop bounds: non-white ink inside left panel, excluding border/callout/label/pen
nonwhite = (np.abs(a - 255).max(axis=2) > 40)
seg5 = nonwhite[175:355, 104:300]
# mask out: callout (y>=300 rel), label window, pen cursor below callout
seg5[300 - 175:, :] = False
seg5[210 - 175:230 - 175, 214 - 104:290 - 104] = False   # AC Motor label
ys5, xs5 = np.nonzero(seg5)
print("motor art bbox:", (104 + xs5.min(), 175 + ys5.min(), 104 + xs5.max(), 175 + ys5.max()), "n=", len(xs5))

# ---- summary line 2 exact + title color census
print("title core color:", [tuple(a[yy, xx]) for yy, xx in ((80, 400), (80, 450), (78, 500))])
print("arrow core color:", [tuple(a[yy, xx]) for yy, xx in ((228, 370), (228, 390))])
print("subtitle core:", [tuple(a[yy, xx]) for yy, xx in ((104, 300), (104, 500), (105, 600))])
print("wave red core:", [tuple(a[yy, xx]) for yy, xx in ((266, 703), (270, 706))])
print("wave green core:", [tuple(a[yy, xx]) for yy, xx in ((285, 745), (280, 742))])
