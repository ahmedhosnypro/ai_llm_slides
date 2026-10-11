#!/usr/bin/env python3
"""Measurement v4: clean rectangles + per-line color runs + chevrons + badge."""
from PIL import Image
import numpy as np, json

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_032.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
FX0, SX, SY = 18.63, 0.96123, 0.95556
def to_slide(fx, fy): return ((fx - FX0) / SX, fy / SY)
def pr(label, fx0, fy0, fx1, fy1):
    s0 = to_slide(fx0, fy0); s1 = to_slide(fx1 + 1, fy1 + 1)
    print(f"{label:36s} frame x {fx0}..{fx1} y {fy0}..{fy1} -> slide x {s0[0]:.1f}..{s1[0]:.1f} y {s0[1]:.1f}..{s1[1]:.1f} (w {s1[0]-s0[0]:.1f} h {s1[1]-s0[1]:.1f})")
    return (fx0, fy0, fx1, fy1, s0[0], s0[1], s1[0], s1[1])

def near(c, tol):
    r, g, b = c
    return (np.abs(R - r) < tol) & (np.abs(G - g) < tol) & (np.abs(B - b) < tol)

# ---- cyan panel: strict ----
cyan = near((233, 254, 249), 10)
rowc = cyan.sum(axis=1); colc = cyan.sum(axis=0)
rows = np.where(rowc > 300)[0]; cols = np.where(colc > 100)[0]
print("cyan rows>300:", rows.min(), rows.max(), " cols>100:", cols.min(), cols.max())
print("cyan col profile 50..100:", [(c, int(colc[c])) for c in range(50, 101, 5)])
print("cyan col profile 880..910:", [(c, int(colc[c])) for c in range(880, 911, 3)])
print("cyan row profile 200..220:", [(r, int(rowc[r])) for r in range(200, 221, 2)])
print("cyan row profile 500..520:", [(r, int(rowc[r])) for r in range(500, 521, 2)])

# ---- navy border vs blue text: navy B<170 ----
navy = (R < 90) & (G < 90) & (B > 80) & (B < 170)
r2 = navy.sum(axis=1); c2 = navy.sum(axis=0)
rn = np.where(r2 > 150)[0]; cn = np.where(c2 > 25)[0]
if len(rn) and len(cn):
    print(f"\nnavy-border rect: rows {rn.min()}..{rn.max()} cols {cn.min()}..{cn.max()}")
    pr('navy border rect', int(cn.min()), int(rn.min()), int(cn.max()), int(rn.max()))
else:
    print("\nnavy rows>150:", np.where(r2 > 150)[0][:5], "cols>25:", np.where(c2 > 25)[0][:5])

# ---- callout: orange border, strict CC6600 ----
orange = (np.abs(R - 200) < 55) & (np.abs(G - 105) < 50) & (B < 90) & (R - G > 60) & (G - B > 30)
r3 = orange.sum(axis=1); c3 = orange.sum(axis=0)
ro = np.where(r3 > 60)[0]; co = np.where(c3 > 15)[0]
if len(ro) and len(co):
    print(f"\norange-border rect: rows {ro.min()}..{ro.max()} cols {co.min()}..{co.max()}")
    pr('callout orange border', int(co.min()), int(ro.min()), int(co.max()), int(ro.max()))
else:
    print("\norange rows>60:", np.where(r3 > 60)[0][:10])

# callout fill: pale yellow, require B in 150..225 and R-B>25, count per row
call = (R > 200) & (G > 200) & (B > 150) & (B < 228) & (R - B > 25) & (G - B > 25)
r4 = call.sum(axis=1)
rrows = np.where(r4 > 150)[0]
print("callout fill rows>150:", (rrows.min(), rrows.max()) if len(rrows) else None)
if len(rrows):
    sub = call[rrows.min():rrows.max() + 1]
    cc = sub.sum(axis=0); ccols = np.where(cc > 30)[0]
    pr('callout fill rect', int(ccols.min()), int(rrows.min()), int(ccols.max()), int(rrows.max()))

# ---- subtitle: blue ink, rows 78..112, exclude navy-border rows ----
blue = (R < 120) & (G < 120) & (B > 140)
sub = blue[76:114, 100:900]
csub = sub.sum(axis=0)
cc = np.where(csub > 0)[0]
print("\nsubtitle blue col profile 100..300:", [(c, int(csub[c - 100])) for c in range(100, 301, 10)])
if len(cc):
    pr('subtitle blue ink', 100 + int(cc.min()), 76 + int(np.where(sub.any(axis=1))[0].min()), 100 + int(cc.max()), 76 + int(np.where(sub.any(axis=1))[0].max()))

# ---- per-line color runs (correct bands, from v3) ----
bands = [(227, 244), (292, 309), (324, 341), (356, 373), (388, 405), (452, 470)]
yellow = near((255, 255, 0), 70)
green = (G > 110) & (R < 110) & (B < 110) & (G - R > 50) & (G - B > 50)
red = (R > 120) & (G < 90) & (B < 90)
blue2 = (R < 120) & (G < 120) & (B > 140)

def runs_of(mask, b0, b1, x0=82, x1=879, minw=3):
    m = mask[b0:b1 + 1, x0:x1]
    cols = np.where(m.any(axis=0))[0]
    if not len(cols): return []
    rr = []; r0 = cols[0]
    for j in range(1, len(cols)):
        if cols[j] != cols[j - 1] + 1:
            rr.append((int(r0 + x0), int(cols[j - 1] + x0))); r0 = cols[j]
    rr.append((int(r0 + x0), int(cols[-1] + x0)))
    return [(a1, b2) for a1, b2 in rr if b2 - a1 >= minw]

print("\n== per-line runs (frame x) ==")
for i, (b0, b1) in enumerate(bands):
    yl = runs_of(yellow, b0, b1); gr = runs_of(green, b0, b1); rd = runs_of(red, b0, b1)
    xs_all = np.where((yellow | green | red | blue2)[b0:b1 + 1, 82:879].any(axis=0))[0]
    print(f"L{i+1} y {b0}..{b1}: ink x {82+int(xs_all.min())}..{82+int(xs_all.max())} | YELLOW {yl} | GREEN {gr} | RED {rd}")
    for name, rr in (('Y', yl), ('G', gr), ('R', rd)):
        for a1, b2 in rr:
            s0 = to_slide(a1, 0); s1 = to_slide(b2 + 1, 0)
            print(f"    {name} slide x {s0[0]:.1f}..{s1[0]:.1f} (w {s1[0]-s0[0]:.1f})")

# ---- left-edge ink detail for chevrons: column ink profile x 82..135 per line ----
print("\n== left-edge columns per line (ink cols x 82..140) ==")
inkany = (R < 170) | (yellow)  # any dark or yellow
for i, (b0, b1) in enumerate(bands):
    m = inkany[b0:b1 + 1, 82:141]
    cols = np.where(m.any(axis=0))[0]
    prof = [(82 + int(c), int(m[:, c].sum())) for c in cols[:24]]
    print(f"L{i+1}: {prof}")

# ---- badge clean ----
badge = (R > 225) & (G > 225) & (B > 100) & (B < 215) & (np.abs(R - G) < 30)
bm = np.zeros((H, W), bool); bm[40:110, 845:915] = badge[40:110, 845:915]
ys, xs = np.where(bm)
if len(ys):
    pr('badge yellow', int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
    num = (R < 120) & (G < 120) & (B < 120)
    nm = np.zeros((H, W), bool)
    y0b, y1b, x0b, x1b = int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())
    nm[y0b:y1b + 1, x0b:x1b + 1] = num[y0b:y1b + 1, x0b:x1b + 1]
    ys2, xs2 = np.where(nm)
    if len(ys2):
        pr('badge numeral ink', int(xs2.min()), int(ys2.min()), int(xs2.max()), int(ys2.max()))
# purple ring
purple = (B > 140) & (B - R > 40) & (B - G > 40) & (R > 60) & (R < 160)
pm = np.zeros((H, W), bool); pm[40:115, 840:920] = purple[40:115, 840:920]
ys, xs = np.where(pm)
if len(ys):
    pr('badge purple ring', int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))
