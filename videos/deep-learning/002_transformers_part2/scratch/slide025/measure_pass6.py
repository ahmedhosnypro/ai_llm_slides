#!/usr/bin/env python3
"""Pass 6: close remaining gaps — hub fit (tight), dash endpoints vs ring center,
cos/sin arrow color disambiguation, arrow-label bands recheck, motor sub-structure
(rows/cols profile), title/subtitle/summary/footer em fits, curved-arrow shape."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_025.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

CX, CY = 600, 266  # ring center (from measure_ring best fit)

# ---- 1. hub: tight Kasa fit on gray stroke, window centered on ring center
grayline = (np.abs(r - g) < 30) & (np.abs(g - b) < 30) & (r > 100) & (r < 215)
win = grayline[CY - 30:CY + 30, CX - 30:CX + 30]
ys, xs = np.nonzero(win)
pts = np.stack([xs + CX - 30, ys + CY - 30], axis=1).astype(float)
x, y = pts[:, 0], pts[:, 1]
A = np.stack([x, y, np.ones_like(x)], axis=1)
bb = x**2 + y**2
sol, *_ = np.linalg.lstsq(A, bb, rcond=None)
hcx, hcy = sol[0] / 2, sol[1] / 2
hrad = np.sqrt(sol[2] + hcx**2 + hcy**2)
d = np.hypot(x - hcx, y - hcy)
resid = np.abs(d - hrad)
keep = resid < 3  # drop outliers (dashes etc.)
x2, y2 = x[keep], y[keep]
A2 = np.stack([x2, y2, np.ones_like(x2)], axis=1)
sol2, *_ = np.linalg.lstsq(A2, x2**2 + y2**2, rcond=None)
hcx2, hcy2 = sol2[0] / 2, sol2[1] / 2
hrad2 = np.sqrt(sol2[2] + hcx2**2 + hcy2**2)
print(f"hub tight fit: center ({hcx2:.1f},{hcy2:.1f}) r={hrad2:.1f} n={keep.sum()}/{len(x)}")

# ---- 2. dashes vs ring center: dark px right of hub, angles/radii
dark = (r < 130) & (g < 130) & (b < 130)
Y0, Y1 = CY - 60, CY + 60
X0 = int(CX + 25)
yy, xx = np.nonzero(dark[Y0:Y1, X0:835])
pts2 = np.stack([xx + X0, yy + Y0], axis=1).astype(float)
d2 = np.hypot(pts2[:, 0] - CX, pts2[:, 1] - CY)
th2 = np.degrees(np.arctan2(-(pts2[:, 1] - CY), pts2[:, 0] - CX))  # math y-up
sel = (d2 > 30) & (d2 < 160)
ths, ds = th2[sel], d2[sel]
for name, m in (("above-horiz(th>0)", ths > 0), ("below-horiz(th<0)", ths < 0)):
    if m.sum() > 5:
        print(f"{name}: th {ths[m].min():.1f}..{ths[m].max():.1f} med {np.median(ths[m]):.1f}; r {ds[m].min():.1f}..{ds[m].max():.1f}")
        far = pts2[sel][m][np.argmax(ds[m])]
        print(f"   farthest {tuple(far)}")

# ---- 3. period arrow: exact bbox + head widths
seg = dark[240:310, 710:725]
ys3, xs3 = np.nonzero(seg)
print("period arrow bbox:", (710 + xs3.min(), 240 + ys3.min(), 710 + xs3.max(), 240 + ys3.max()))
rowc = seg.sum(axis=1)
prof = "".join("#" if c >= 5 else ("+" if c >= 2 else ".") for c in rowc)
print("arrow rowprof (5=wide head):", prof)

# ---- 4. cos/sin arrows: color census in clean sub-windows (labels excluded)
def census(y0, y1, x0, x1, label):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    nonbg = sub[(np.abs(sub - 255).max(axis=1) > 60)]
    if len(nonbg):
        q = nonbg // 32 * 32
        keys, counts = np.unique(q, axis=0, return_counts=True)
        order = np.argsort(-counts)[:4]
        print(f"{label}: {[(tuple(int(v) for v in keys[i]), int(counts[i])) for i in order]} n={len(nonbg)}")

census(205, 240, 688, 722, "cos-arrow window (x688..721,y205..239)")
census(225, 260, 688, 732, "sin-arrow window (x688..731,y225..259)")
# where exactly: ink bboxes of red vs green vs dark in each window
redm = (r - g > 60) & (r - b > 50) & (r > 110)
greenm = (g - r > 30) & (g - b > 20) & (g > 70)
for (y0, y1, x0, x1, lbl) in ((205, 242, 688, 723, "cos-arrow"), (226, 262, 688, 733, "sin-arrow")):
    for nm, msk in (("red", redm), ("green", greenm), ("dark", dark)):
        seg = msk[y0:y1, x0:x1]
        ys4, xs4 = np.nonzero(seg)
        if len(xs4) > 3:
            print(f"  {lbl} {nm}: bbox ({x0+xs4.min()},{y0+ys4.min()})-({x0+xs4.max()},{y0+ys4.max()}) n={len(xs4)}")

# ---- 5. arrow-label bands recheck (full center column scan)
seg = redm[210:330, 300:470]
rows = seg.sum(axis=1)
inb = False
for i, c in enumerate(rows):
    if c >= 2 and not inb:
        s, inb = i, True
    elif c < 2 and inb:
        cols = seg[s:i].sum(axis=0)
        xs5 = np.nonzero(cols > 0)[0]
        print(f"center red band y {210+s}..{210+i-1}  x {300+xs5.min()}..{300+xs5.max()}")
        inb = False

# ---- 6. motor sub-structure: row/col ink profiles inside panel (x104..300, y174..300)
ink_w = (np.abs(a - 255).max(axis=2) > 45)
seg = ink_w[174:301, 103:301]
rows = seg.sum(axis=1)
print("motor rowprof y174..300 (x103..300):")
print("".join("#" if c > 60 else ("+" if c > 20 else ("." if c > 2 else " ")) for c in rows))
cols = seg.sum(axis=0)
print("motor colprof:")
print("".join("#" if c > 50 else ("+" if c > 15 else ("." if c > 2 else " ")) for c in cols))

# ---- 7. title/subtitle/summary/footer band precision (minpix=3)
def bands(y0, y1, x0, x1, mask, minpix=3):
    seg = mask[y0:y1, x0:x1]
    rowc = seg.sum(axis=1)
    out, inb, s = [], False, 0
    for i, c in enumerate(rowc):
        if c >= minpix and not inb:
            s, inb = i, True
        elif c < minpix and inb:
            out.append((y0 + s, y0 + i - 1)); inb = False
    if inb:
        out.append((y0 + s, y0 + len(rowc) - 1))
    res = []
    for (bs, be) in out:
        cols = seg[bs - y0:be - y0 + 1].sum(axis=0)
        xs6 = np.nonzero(cols >= 1)[0]
        res.append((bs, be, x0 + int(xs6.min()), x0 + int(xs6.max())))
    return res

bluem = (b - r > 40) & (b - g > 30) & (b > 90)
darkish = (np.abs(a - np.array([234, 234, 234])).max(axis=2) > 60)
print("title bands:", bands(60, 95, 150, 800, redm))
print("subtitle bands:", bands(90, 125, 150, 800, bluem))
print("summary bands:", bands(395, 465, 120, 850, darkish))
print("footer bands:", bands(460, 515, 60, 650, bluem))
print("footer band cores:", [tuple(a[yy, xx]) for yy, xx in ((476, 100), (488, 300), (501, 300))])

# ---- 8. curved arrow shape: dark bbox + row profile in y158..202, x545..655
seg = dark[158:202, 545:655]
rows = seg.sum(axis=1)
print("curved arrow rowprof y158..201:")
print("".join("#" if c > 3 else ("+" if c > 1 else ".") for c in rows))
for i, c in enumerate(rows):
    if c > 0:
        xs7 = np.nonzero(seg[i])[0]
        print(f"  y{158+i}: x {545+xs7.min()}..{545+xs7.max()} n={c}")
