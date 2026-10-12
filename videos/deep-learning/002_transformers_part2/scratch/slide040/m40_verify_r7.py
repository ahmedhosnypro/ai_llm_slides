#!/usr/bin/env python3
"""m30: verify attempt-4 NEW elements in render_4 against frame-measured targets.
render mapping: rx=(fx-18.63)*2.16766, ry=fy*2.18013."""
import numpy as np
from PIL import Image

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide040/render_7.png'
im = np.asarray(Image.open(REN).convert('RGB')).astype(int)
lum = (im[:,:,0]+im[:,:,1]+im[:,:,2])/3.0
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

def R(fx, fy): return int(round((fx-18.63)*2.16766)), int(round(fy*2.18013))

ok = True
def check(label, cond, detail):
    global ok
    print(f"  [{'PASS' if cond else 'FAIL'}] {label}: {detail}")
    ok = ok and cond

print("== 1. eq3 lavender rect: top edge y~870 (frame 399), left x~315, right x~582 ==")
x0, y0 = R(164, 399); x1, y1 = R(287, 446)
row = lum[y0-2:y0+3, x0:x1+1] < 225
check("eq3 rect top edge", row.any(axis=1).all() and row.shape[0] > 0, f"rows y{y0-2}..{y0+2} x{x0}..{x1} dark={int(row.sum())}")
col = lum[y0:y1+1, x0-2:x0+3] < 225
check("eq3 rect left edge", (col.sum(axis=0) >= col.shape[0]*0.9).sum() >= 2, f"cols x{x0-2}..{x0+2} y{y0}..{y1} dark={int(col.sum())}")
col2 = lum[y0:y1+1, x1-2:x1+3] < 225
check("eq3 rect right edge", (col2.sum(axis=0) >= col2.shape[0]*0.9).sum() >= 2, f"cols x{x1-2}..{x1+2} dark={int(col2.sum())}")
# stroke color sample at top edge
xs = np.where(lum[y0, x0:x1] < 225)[0]
if len(xs):
    c = im[y0, x0:x1][xs].mean(axis=0)
    print(f"     top-edge stroke mean RGB: {c.round(0)} (target lavender-lightened ~190,190,215)")

print("== 2. eq4 pink rect: top y~983 (frame 451), bottom y~1036 (frame 475), right x~764 (frame 371) ==")
x0, y0 = R(164, 451); x1, y1 = R(371, 475)
rowt = lum[y0-2:y0+3, x0:x1+1] < 230
check("eq4 rect top edge", (rowt.sum(axis=1) >= rowt.shape[1]*0.9).sum() >= 2, f"y{y0-2}..{y0+2} x{x0}..{x1} dark={int(rowt.sum())}")
rowb = lum[y1-2:y1+3, x0:x1+1] < 230
check("eq4 rect bottom edge", (rowb.sum(axis=1) >= rowb.shape[1]*0.9).sum() >= 2, f"dark={int(rowb.sum())}")
xs = np.where(lum[y0, x0:x1] < 230)[0]
if len(xs):
    print(f"     top-edge stroke mean RGB: {im[y0, x0:x1][xs].mean(axis=0).round(0)} (target pink-lightened ~225,205,205)")

print("== 3. y_i ellipse tan fill ==")
x0, y0 = R(177, 462)
patch = im[y0-3:y0+4, x0-3:x0+4].reshape(-1, 3)
Lp = (patch[:,0]+patch[:,1]+patch[:,2])/3
sel = patch[(Lp > 150) & (Lp < 235)]
if len(sel):
    m = sel.mean(axis=0)
    tanlike = m[0] > m[2] + 30 and m[0] > 190
    check("ellipse interior tan", bool(tanlike), f"mean RGB {m.round(0)} (target ~(240,190,130) lightened)")
else:
    check("ellipse interior tan", False, "no mid-tone pixels found")

print("== 4. underlines in render ==")
def underline_probe(fy, fx0, fx1, label):
    y = int(round(fy*2.18013))
    x0 = int(round((fx0-18.63)*2.16766)); x1 = int(round((fx1-18.63)*2.16766))
    band = (lum[y-2:y+3, x0:x1+1] < 200)
    n = int(band.sum())
    # coverage: fraction of x-columns having dark ink in the band
    cov = float((band.any(axis=0)).mean())
    check(label, cov > 0.85, f"y~{y} x{x0}..{x1} coverage {cov:.2f} n={n}")
underline_probe(157, 664, 826, "L2 red underline (frame y157 x664..826)")
underline_probe(157, 391, 540, "learn-params underline (frame y157 x391..540)")
underline_probe(181, 106, 434, "L3 red underline (frame y181 x106..434)")
# L1 must have NO underline
y = int(round(133*2.18013))
x0 = int(round((540-18.63)*2.16766)); x1 = int(round((822-18.63)*2.16766))
n_l1 = int((lum[y-2:y+3, x0:x1+1] < 200).sum())
check("L1 has NO underline", n_l1 < 40, f"dark px in band y~{y}: {n_l1}")

print("== 5. gamma/beta still RED in render (judge-override preserved) ==")
def colorclass(fx0, fx1, fy0, fy1, label):
    x0, y0 = R(fx0, fy0); x1, y1 = R(fx1, fy1)
    box = im[y0:y1, x0:x1].reshape(-1, 3)
    L = (box[:,0]+box[:,1]+box[:,2])/3
    d = box[L < 190]
    if len(d) == 0:
        check(label, False, "no dark px"); return
    redish = int(((d[:,0] > d[:,1]+40) & (d[:,0] > d[:,2]+40)).sum())
    greenish = int(((d[:,1] > d[:,0]+25) & (d[:,1] > d[:,2]+25)).sum())
    check(label, redish > greenish * 3, f"red={redish} green={greenish} of n={len(d)}")
colorclass(534, 549, 144, 160, "intro gamma red")
colorclass(580, 597, 141, 160, "intro beta red")

print("== 6. highlight green fills ==")
def fillmode(fx0, fx1, fy0, fy1, label, target):
    x0, y0 = R(fx0, fy0); x1, y1 = R(fx1, fy1)
    box = im[y0:y1, x0:x1].reshape(-1, 3)
    L = (box[:,0]+box[:,1]+box[:,2])/3
    sel = box[(L > 150) & (L < 250)]
    if len(sel) == 0:
        check(label, False, "no fill px"); return
    m = sel.mean(axis=0)
    got = tuple(int(v) for v in m)
    check(label, abs(m[0]-target[0]) < 25 and abs(m[1]-target[1]) < 25 and abs(m[2]-target[2]) < 25,
          f"mean RGB {got} vs target {target}")
fillmode(391, 529, 146, 157, "intro hl ~D8F8D8(+text mix)", (200, 240, 200))
fillmode(206, 423, 228, 247, "panel hl ~B0E8B0(+text mix)", (170, 225, 170))

print()
print("ATTEMPT-4 NEW-ELEMENT CHECK:", "PASS" if ok else "FAIL")
