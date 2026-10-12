#!/usr/bin/env python3
"""m19_targets.py — remaining unknowns: dashed containers, green arrows, title metrics,
IO boxes, FFN tiles/dots, borders, red arrows, block-arrow outline, curve color."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_047.jpg"
A = np.asarray(Image.open(F).convert("RGB")).astype(int)
SX, OX, SY = 0.962329, 17.582, 0.955556
sx = lambda x: (x - OX) / SX
sy = lambda y: y / SY
hx = lambda c: "#%02X%02X%02X" % tuple(int(round(v)) for v in c)

print("== A. DASHED CONTAINERS: non-tan, non-red px in unit zones ==")
TAN = np.array([232, 178, 118])
for tag, y0, y1 in [("unit1", 88, 178), ("unit2", 300, 395)]:
    reg = A[y0:y1, 115:915]
    dist_tan = np.abs(reg - TAN).sum(axis=2)
    # exclude red discs/curves and white-ish: keep px that are greenish or olive
    m = (dist_tan > 90) & (reg[:, :, 1] > reg[:, :, 0] - 60) & (reg[:, :, 1] >= reg[:, :, 2]) & (reg[:, :, 0] < 200) & (reg[:, :, 2] < 160)
    ys, xs = np.nonzero(m)
    print(f" {tag}: n={len(ys)}")
    if len(ys):
        rows = np.unique(ys)
        cl, cur = [], [rows[0]]
        for r in rows[1:]:
            if r - cur[-1] <= 2: cur.append(r)
            else: cl.append(cur); cur = [r]
        cl.append(cur)
        for c in cl[:8]:
            sel = (ys >= c[0]) & (ys <= c[-1])
            xs_c = xs[sel]
            samp = reg[ys[sel], xs[sel]]
            print(f"   rows {y0+c[0]}..{y0+c[-1]} (slide {sy(y0+c[0]):.1f}..{sy(y0+c[-1]):.1f}) x {115+xs_c.min()}..{115+xs_c.max()} (slide {sx(115+xs_c.min()):.1f}..{sx(115+xs_c.max()):.1f}) n={sel.sum()} color {hx(np.median(samp,axis=0))}")

print("== B. GREEN ARROWS (loose) ==")
for tag, y0, y1 in [("rowC->p2", 366, 382), ("p2->LN2", 343, 362), ("LN2->rowB", 308, 322),
                    ("rowA->p1", 161, 172), ("p1->LN1", 131, 150), ("FFN->rowA", 190, 204)]:
    reg = A[y0:y1, 180:905]
    m = (reg[:, :, 1] > reg[:, :, 0]) & (reg[:, :, 1] > reg[:, :, 2] + 10)
    n = int(m.sum())
    if n:
        cols = np.nonzero(m.any(axis=0))[0] + 180
        samp = reg[m]
        print(f" {tag}: n={n} cols {cols.min()}..{cols.max()} color {hx(np.median(samp,axis=0))}")
        # cluster cols
        cl, cur = [], [cols[0]]
        for c in cols[1:]:
            if c - cur[-1] <= 4: cur.append(c)
            else: cl.append(cur); cur = [c]
        cl.append(cur)
        print("   col clusters:", [(c[0], c[-1]) for c in cl][:12])
    else:
        print(f" {tag}: none")

print("== C. RED OUTPUT ARROWS extent ==")
reg = A[72:102, 180:905]
m = (reg[:, :, 0] > 120) & (reg[:, :, 1] < 80) & (reg[:, :, 2] < 80)
ys, xs = np.nonzero(m)
print(f" red n={len(ys)} rows {72+ys.min()}..{72+ys.max()} (slide {sy(72+ys.min()):.1f}..{sy(72+ys.max()):.1f}) color {hx(np.median(reg[m],axis=0))}")
rc = m.sum(axis=1)
print(" per-row counts:", [(72 + i, int(n)) for i, n in enumerate(rc)])

print("== D. VERTICAL TITLE per-band ==")
reg = A[115:430, 62:165]
m = (reg[:, :, 0] > 100) & (reg[:, :, 0] < 215) & (reg[:, :, 1] < 90) & (reg[:, :, 2] < 90)
rows = np.nonzero(m.any(axis=1))[0]
cl, cur = [], [rows[0]]
for r in rows[1:]:
    if r - cur[-1] <= 4: cur.append(r)
    else: cl.append(cur); cur = [r]
cl.append(cur)
print(" bands:", [(115 + c[0], 115 + c[-1]) for c in cl])
for c in cl:
    sel = m[c[0]:c[-1] + 1]
    xs = np.nonzero(sel.any(axis=0))[0]
    print(f"   band y {115+c[0]}..{115+c[-1]}: x {62+xs.min()}..{62+xs.max()} (cap {sx(62+xs.max())-sx(62+xs.min()):.1f}pt) n={int(sel.sum())}")
samp = reg[m]
print(" title ink median:", hx(np.median(samp, axis=0)), "darkest-decile:", hx(np.percentile(samp.sum(axis=1), 10) and samp[samp.sum(axis=1) <= np.percentile(samp.sum(axis=1), 10)].mean(axis=0)))

print("== E. IO BOXES ==")
for tag, y0, y1 in [("Out", 38, 95), ("In", 468, 520)]:
    reg = A[y0:y1, 62:215]
    m = (reg[:, :, 0] > 120) & (reg[:, :, 1] < 85) & (reg[:, :, 2] < 85)
    rc = m.sum(axis=1); cc = m.sum(axis=0)
    print(f" {tag}: row counts>15: {[(y0+i,int(n)) for i,n in enumerate(rc) if n>15]}")
    print(f"      col counts>8: {[(62+i,int(n)) for i,n in enumerate(cc) if n>8]}")
    # fill + text
    ink = reg[m]
    print(f"      ink median {hx(np.median(ink,axis=0))}; fill probe:", hx(np.median(A[(y0+y1)//2-4:(y0+y1)//2+4, 75:85].reshape(-1,3),axis=0)))

print("== F. FFN BOX + TILES ==")
# box border: darkest col in x 150..170 at y 240
for x in range(150, 172):
    c = A[240, x]
    if c.sum() < 500: print(f"  left border cand x={x} {hx(c)}")
for x in range(878, 895):
    c = A[240, x]
    if c.sum() < 500: print(f"  right border cand x={x} {hx(c)}")
for y in range(203, 212):
    c = A[y, 500]
    if c.sum() < 520: print(f"  top border cand y={y} {hx(c)}")
for y in range(262, 270):
    c = A[y, 500]
    if c.sum() < 520: print(f"  bottom border cand y={y} {hx(c)}")
# tiles: vertical dark cols across tile band y 228..258
band = A[228:258, 150:900]
darkcols = [(150 + i, int(n)) for i, n in enumerate((band.sum(axis=2) < 480).sum(axis=0)) if n > 12]
print("  tile-border dark cols:", darkcols)
# tile fill vs gap fill
print("  inside-tile fill:", hx(np.median(A[240:244, 200:210].reshape(-1, 3), axis=0)),
      " between-tile fill:", hx(np.median(A[240:244, 260:270].reshape(-1, 3), axis=0)))
# dots: green-dominant and pink-dominant clusters in tile1 (frame x 165..250)
t1 = A[224:262, 160:255]
gm = (t1[:, :, 1] > t1[:, :, 0]) & (t1[:, :, 1] > t1[:, :, 2] + 20)
pm = (t1[:, :, 0] > 200) & (t1[:, :, 2] > 150) & (t1[:, :, 1] < t1[:, :, 0] - 40)
for nm, mm in [("green", gm), ("pink", pm)]:
    ys, xs = np.nonzero(mm)
    if len(ys):
        cols = np.unique(xs)
        cl, cur = [], [cols[0]]
        for c in cols[1:]:
            if c - cur[-1] <= 2: cur.append(c)
            else: cl.append(cur); cur = [c]
        cl.append(cur)
        print(f"  tile1 {nm} dots: {len(cl)} clusters at x", [(160 + c[0], 160 + c[-1]) for c in cl],
              "y", int(ys.min()) + 224, "..", int(ys.max()) + 224, "color", hx(np.median(t1[mm], axis=0)))
    else:
        print(f"  tile1 {nm}: none")
# RELU label: red-ish px in tile1 upper right
rel = A[226:242, 215:252]
rm = (rel[:, :, 0] > 140) & (rel[:, :, 1] < 90) & (rel[:, :, 2] < 90)
print("  tile1 RELU red px:", int(rm.sum()), hx(np.median(rel[rm], axis=0)) if rm.sum() else "")

print("== G. CURVES (orange arcs) color at left of col1 ==")
reg = A[200:290, 150:200]
m = (reg[:, :, 0] > 180) & (reg[:, :, 1] > 70) & (reg[:, :, 1] < 150) & (reg[:, :, 2] < 80)
print(" curve-ish px n=", int(m.sum()), hx(np.median(reg[m], axis=0)) if m.sum() else "")
reg2 = A[430:520, 150:200]
m2 = (reg2[:, :, 0] > 180) & (reg2[:, :, 1] > 70) & (reg2[:, :, 1] < 150) & (reg2[:, :, 2] < 80)
print(" lower-unit curve px n=", int(m2.sum()), hx(np.median(reg2[m2], axis=0)) if m2.sum() else "")

print("== H. LN/MHA/container borders ==")
print(" LN1 top border row y=101:", [(x, hx(A[101, x])) for x in (200, 500, 800)])
print(" LN1 bottom border row y=129:", [(x, hx(A[129, x])) for x in (200, 500, 800)])
print(" MHA top edge y=415..416:", hx(A[415, 500]), hx(A[416, 500]), " bottom y=470..471:", hx(A[470, 500]), hx(A[471, 500]))
print(" container left border y=300:", [(x, hx(A[300, x])) for x in range(123, 130)])
