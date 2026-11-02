#!/usr/bin/env python3
"""Round 2 adjudication: BR extra ink (D2), BL asset label placement (D1), TL asset vs orig (D3)."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
B = NS + "/recreated_pptx/build"
ORIG = NS + "/unique_slides/slide_025.jpg"
S = 2001 / 960.0

orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
ren = np.asarray(Image.open(Q + "/render_18.png").convert("RGB")).astype(int)

def rgn(a, x0, y0, x1, y1, scale):
    return a[int(y0*scale):int(np.ceil(y1*scale))+1, int(x0*scale):int(np.ceil(x1*scale))+1]

def red_mask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R > 110) & (G < 120) & (B < 120) & (R - G > 50) & (R - B > 50)

def colored_mask(a):
    mx, mn = a.max(2), a.min(2)
    return ((mx - mn) > 60) & (mx > 90) & ~red_mask(a)

def dark_mask(a):
    return a.max(2) < 140

print("== D2: BR region ink-only-in-render (render has ink where orig is blank) ==")
x0, y0, x1, y1 = 470, 342, 901, 535
co = rgn(orig, x0, y0, x1, y1, 1.0)
cr = rgn(ren, x0, y0, x1, y1, S)
crs = np.asarray(Image.fromarray(cr.astype(np.uint8)).resize((co.shape[1], co.shape[0]), Image.LANCZOS)).astype(int)
ink_o = colored_mask(co) | red_mask(co) | dark_mask(co)
ink_r = colored_mask(crs) | red_mask(crs) | dark_mask(crs)
extra = ink_r & ~ink_o
dil = ink_o.copy()
for _ in range(3):
    dil = dil | np.roll(dil, 1, 0) | np.roll(dil, -1, 0) | np.roll(dil, 1, 1) | np.roll(dil, -1, 1)
extra_strict = ink_r & ~dil
ys, xs = np.nonzero(extra_strict)
if len(xs):
    print(f"  extra render ink (strict): {len(xs)} px, bbox slide x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()}")
    # cell census 24px cells
    cells = {}
    for yy, xx in zip(ys, xs):
        cells.setdefault((xx//24, yy//24), 0)
        cells[(xx//24, yy//24)] += 1
    top = sorted(cells.items(), key=lambda kv: -kv[1])[:12]
    for (cx, cy), n in top:
        print(f"    cell slide x{x0+cx*24}..{x0+cx*24+24} y{y0+cy*24}..{y0+cy*24+24}: {n} extra px")
else:
    print("  no strict extra ink")
print(f"  total extra (loose): {int(extra.sum())} px; missing (orig-only): {int((ink_o & ~ink_r).sum())} px")

print()
print("== D1: BL asset label anchors (asset 1220x987 at slide x83 y290 293x237; scale 1220/293) ==")
bl = np.asarray(Image.open(B + "/assets/plot_025_bl.png").convert("RGB")).astype(int)
sc = 293 / 1220.0  # slide px per asset px
def asset_box(sx0, sy0, sx1, sy1):
    ax0 = int((sx0 - 83) / sc); ay0 = int((sy0 - 290) / sc)
    ax1 = int((sx1 - 83) / sc); ay1 = int((sy1 - 290) / sc)
    return bl[ay0:ay1+1, ax0:ax1+1]
LABELS = {
    "Global Maxima": (242, 304, 268, 319),
    "Local Maxima":  (286, 337, 315, 352),
    "Local Minima":  (286, 390, 311, 399),
    "Global Minima": (145, 439, 201, 465),
}
for name, (bx0, by0, bx1, by1) in LABELS.items():
    pad = 8
    sub = asset_box(bx0-pad, by0-pad, bx1+pad, by1+pad)
    dm = dark_mask(sub)
    ys, xs = np.nonzero(dm)
    if len(xs):
        # convert back to slide px
        print(f"  '{name}' anchor: asset ink={len(xs)} slide bbox x{bx0-pad+xs.min()*sc:.0f}..{bx0-pad+xs.max()*sc:.0f} y{by0-pad+ys.min()*sc:.0f}..{by0-pad+ys.max()*sc:.0f}")
    else:
        print(f"  '{name}' anchor: NO dark ink")
# scan whole BL asset for dark text clusters outside the anchor boxes (misplaced labels)
dm = dark_mask(bl)
from scipy import ndimage
lab, n = ndimage.label(dm)
print(f"  BL asset dark clusters: {n}")
sizes = ndimage.sum(dm, lab, range(1, n+1))
big = [(i+1, int(s)) for i, s in enumerate(sizes) if s > 200]
for i, s in big:
    ys, xs = np.nonzero(lab == i)
    print(f"    cluster {i}: {s}px slide bbox x{83+xs.min()*sc:.0f}..{83+xs.max()*sc:.0f} y{290+ys.min()*sc:.0f}..{290+ys.max()*sc:.0f}")

print()
print("== D3: TL asset vs orig TL crop — colored census + silhouette diff ==")
tl = np.asarray(Image.open(B + "/assets/plot_025_tl.png").convert("RGB")).astype(int)
# TL asset 750x720 placed at x85 y115 180x173; scale = 180/750 slide px per asset px
sct = 180 / 750.0
co = rgn(orig, 60, 110, 470, 295, 1.0)
# build slide-space canvas of the render region from the asset
canvas = np.full((co.shape[0], co.shape[1], 3), 255, dtype=int)
ah, aw = tl.shape[:2]
gh, gw = int(173 / sct * sct), 0  # asset covers 180x173 slide px at (85,115)
sh, sw = int(round(173 / sct)), 0
# place asset into canvas coords: slide x85..265 -> canvas x 85-60=25..; y115..288 -> canvas y 5..
ax0 = int(85 - 60); ay0 = int(115 - 110)
g = np.asarray(Image.fromarray(tl.astype(np.uint8)).resize((180, 173), Image.LANCZOS)).astype(int)
canvas[ay0:ay0+173, ax0:ax0+180] = g
cm_o = colored_mask(co); cm_g = colored_mask(canvas)
print(f"  orig colored px={int(cm_o.sum())}  asset-as-placed colored px={int(cm_g.sum())}")
ys, xs = np.nonzero(cm_g & ~cm_o)
if len(xs):
    print(f"  asset-only colored ink: {len(xs)} px bbox slide x{60+xs.min()}..{60+xs.max()} y{110+ys.min()}..{110+ys.max()}")
ys, xs = np.nonzero(cm_o & ~cm_g)
if len(xs):
    print(f"  orig-only colored ink: {len(xs)} px bbox slide x{60+xs.min()}..{60+xs.max()} y{110+ys.min()}..{110+ys.max()}")
