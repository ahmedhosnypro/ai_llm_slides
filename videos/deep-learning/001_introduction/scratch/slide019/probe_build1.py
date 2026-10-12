#!/usr/bin/env python3
"""Targeted probes for slide 019 build. 960x540 frame, 1px = 1pt."""
import numpy as np
from PIL import Image
from collections import Counter

IM = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
H, W, _ = IM.shape
r, g, b = IM[..., 0], IM[..., 1], IM[..., 2]
lum = (r * 299 + g * 587 + b * 114) // 1000

def bbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), len(xs))

def modal(px_list, n=4):
    c = Counter((int(p[0]) // 8 * 8, int(p[1]) // 8 * 8, int(p[2]) // 8 * 8) for p in px_list)
    return [(f"#{v[0]:02X}{v[1]:02X}{v[2]:02X}", k) for v, k in c.most_common(n)]

print("== A. TITLE red ink y60..105 x100..900 ==")
m = (r > 110) & (g < 70) & (b < 70)
tb = bbox(m, 100, 60, 900, 105)
print(" title ink bbox:", tb, "center:", (tb[0] + tb[2]) / 2 if tb else None)
sub = IM[60:105, 100:900][m[60:105, 100:900]]
print(" title color modal:", modal(sub))
# column profile to check centering
cols = np.nonzero(m[60:105, 100:900].any(axis=0))[0] + 100
print(" title cols min/max:", cols.min(), cols.max())

print("== B. box border rects ==")
# input & samples: dark brown stroke
brown = (r > 80) & (r < 170) & (g > 50) & (g < 120) & (b < 100) & (r > g + 15) & (g >= b)
for nm, (x0, y0, x1, y1) in [("input", (60, 190, 175, 285)), ("samples", (805, 190, 915, 285))]:
    bb = bbox(brown, x0, y0, x1, y1)
    print(f" {nm} brown-border bbox:", bb)
# pre & extr: navy stroke
navy = (b > 70) & (b > r + 35) & (b > g + 35)
for nm, (x0, y0, x1, y1) in [("pre", (185, 185, 300, 285)), ("extr", (305, 185, 420, 285))]:
    bb = bbox(navy, x0, y0, x1, y1)
    print(f" {nm} navy-border bbox:", bb)
# sel: green stroke
grn = (g > 70) & (g > r + 25) & (g > b + 25) & (lum < 190)
for nm, (x0, y0, x1, y1) in [("sel", (420, 185, 535, 285))]:
    bb = bbox(grn, x0, y0, x1, y1)
    print(f" {nm} green-border bbox:", bb)
# pred: purple stroke
pur = (r > 110) & (b > 110) & (g < 90)
for nm, (x0, y0, x1, y1) in [("pred", (645, 195, 745, 275))]:
    bb = bbox(pur, x0, y0, x1, y1)
    print(f" {nm} purple-border bbox:", bb)
# verr: red stroke excluding text col
red = (r > 140) & (g < 60) & (b < 60)
vb = bbox(red, 730, 160, 815, 320)
print(" verr red bbox (border+text):", vb)
vb2 = bbox(red, 730, 160, 772, 320)
print(" verr red left-of-text bbox:", vb2)
# per-row red extents at verr left border
for y in (175, 200, 235, 270, 295):
    xs = np.nonzero(red[y, 730:815])[0] + 730
    print(f"  verr row {y} red cols:", (xs.min(), xs.max(), len(xs)) if len(xs) else None)
for x in (745, 760, 790, 800):
    ys = np.nonzero(red[160:320, x])[0] + 160
    print(f"  verr col {x} red rows:", (ys.min(), ys.max(), len(ys)) if len(ys) else None)

print("== C. ellipse ring ==")
dark = lum < 175
eb = bbox(dark, 340, 95, 505, 172)
print(" ellipse dark bbox:", eb)

print("== D. classif border: pixels at fill edge ==")
# classif fill 533..628 207..263; check cols 528..536 and rows 202..210 for dark stroke colors
for x in (529, 531, 533, 630, 632):
    ys = np.nonzero(lum[200:270, x] < 120)[0] + 200
    if len(ys):
        px = IM[ys, x]
        print(f"  classif col {x} dark rows {ys.min()}..{ys.max()} n={len(ys)} modal:", modal(px, 3))
for y in (203, 205, 265, 267):
    xs = np.nonzero(lum[y, 525:640] < 120)[0] + 525
    if len(xs):
        px = IM[y, xs]
        print(f"  classif row {y} dark cols {xs.min()}..{xs.max()} n={len(xs)} modal:", modal(px, 3))

print("== F. annotation border ==")
agrn = (g > r + 12) & (g > b + 12) & (lum < 215)
ab = bbox(agrn, 190, 330, 815, 412)
print(" annot green-ish bbox:", ab)
for y in (336, 338, 340, 400, 402, 404):
    xs = np.nonzero(agrn[y, 190:815])[0] + 190
    if len(xs):
        print(f"  annot row {y}: cols {xs.min()}..{xs.max()} n={len(xs)} modal:", modal(IM[y, xs], 3))
for x in (197, 200, 203, 797, 800):
    ys = np.nonzero(agrn[330:412, x])[0] + 330
    if len(ys):
        print(f"  annot col {x}: rows {ys.min()}..{ys.max()} n={len(ys)} modal:", modal(IM[ys, x], 3))

print("== G. chain arrows (red y228..242 per gap) ==")
for nm, (x0, x1) in [("input->pre", (166, 196)), ("pre->extr", (291, 316)), ("extr->sel", (411, 431)),
                     ("sel->classif", (526, 534)), ("classif->pred", (630, 656)), ("pred->verr", (736, 746)),
                     ("verr<-samples", (792, 816))]:
    mm = red[226:244, x0:x1]
    ys, xs = np.nonzero(mm)
    if len(xs):
        print(f" {nm}: x {x0+xs.min()}..{x0+xs.max()} y {226+ys.min()}..{226+ys.max()} n={len(xs)}")
    else:
        print(f" {nm}: none")

print("== H. text ink colors ==")
def darkest(x0, y0, x1, y1, label):
    sub = IM[y0:y1, x0:x1].reshape(-1, 3)
    l = (sub[:, 0] * 299 + sub[:, 1] * 587 + sub[:, 2] * 114) // 1000
    dk = sub[l < np.percentile(l, 2)]
    print(f" {label} darkest modal:", modal(dk, 4))
darkest(84, 220, 155, 255, "input text")
darkest(813, 220, 882, 255, "samples text")
darkest(210, 232, 278, 252, "pre line2")
darkest(327, 220, 403, 250, "extr text")
darkest(443, 220, 500, 250, "sel text")
darkest(540, 228, 622, 242, "classif white-text zone (brightest)")
bright = IM[228:242, 540:622].reshape(-1, 3)
bl = (bright[:, 0] * 299 + bright[:, 1] * 587 + bright[:, 2] * 114) // 1000
print(" classif text brightest modal:", modal(bright[bl > np.percentile(bl, 90)], 3))
darkest(664, 218, 735, 252, "pred text")
darkest(388, 118, 448, 150, "ellipse text")
darkest(305, 340, 700, 378, "annot text")
sub = IM[183:287, 772:790].reshape(-1, 3)
sl = (sub[:, 0] * 299 + sub[:, 1] * 587 + sub[:, 2] * 114) // 1000
print(" verr text darkest modal:", modal(sub[sl < np.percentile(sl, 4)], 4))

print("== I. blue arc core ==")
darkest(120, 140, 340, 208, "blue solid arc")

print("== J. annotation text rows/cols per line ==")
at = (g < 180) & (g > r - 10) & (lum < 190)
l1 = bbox(at, 290, 338, 710, 357)
l2 = bbox(at, 290, 358, 710, 380)
print(" annot line1 bbox:", l1)
print(" annot line2 bbox:", l2)
