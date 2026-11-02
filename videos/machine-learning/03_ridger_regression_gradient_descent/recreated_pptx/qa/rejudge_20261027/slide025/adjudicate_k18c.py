#!/usr/bin/env python3
"""Round 3: locate BL dark-text clusters and TL colored mass directly in render_18."""
import numpy as np
from PIL import Image
from scipy import ndimage

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
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

def dark_mask(a, t=140):
    return a.max(2) < t

print("== render BL region dark-text clusters (slide coords) ==")
c = rgn(ren, 60, 290, 475, 535, S)
dm = dark_mask(c)
lab, n = ndimage.label(dm)
sizes = ndimage.sum(dm, lab, range(1, n+1))
objs = ndimage.find_objects(lab)
clusters = []
for i, s in enumerate(sizes):
    if s > 30:
        sl = objs[i]
        x0 = 60 + sl[1].start / S; x1 = 60 + sl[1].stop / S
        y0 = 290 + sl[0].start / S; y1 = 290 + sl[0].stop / S
        clusters.append((int(s), x0, y0, x1, y1))
clusters.sort(key=lambda t: -t[0])
for s, x0, y0, x1, y1 in clusters[:25]:
    print(f"  {s:5d} render-px  slide x{x0:.0f}..{x1:.0f} y{y0:.0f}..{y1:.0f}  ({(x1-x0):.0f}x{(y1-y0):.0f} slide-px = {s/S/S:.0f})")

print()
print("== orig BL region dark-text clusters (slide coords) ==")
co = rgn(orig, 60, 290, 475, 535, 1.0)
dm = dark_mask(co)
lab, n = ndimage.label(dm)
sizes = ndimage.sum(dm, lab, range(1, n+1))
objs = ndimage.find_objects(lab)
clusters = []
for i, s in enumerate(sizes):
    if s > 30:
        sl = objs[i]
        clusters.append((int(s), 60+sl[1].start, 290+sl[0].start, 60+sl[1].stop, 290+sl[0].stop))
clusters.sort(key=lambda t: -t[0])
for s, x0, y0, x1, y1 in clusters[:25]:
    print(f"  {s:5d} px  slide x{x0}..{x1} y{y0}..{y1}")

print()
print("== TL render colored map (ASCII, 20-slide-px cells, x60..470 y110..295) ==")
c = rgn(ren, 60, 110, 470, 295, S)
cm = colored_mask(c)
h, w = cm.shape
cell = int(20 * S)
for yy in range(0, h, cell):
    row = ""
    for xx in range(0, w, cell):
        f = cm[yy:yy+cell, xx:xx+cell].mean()
        row += "#" if f > 0.66 else ("+" if f > 0.33 else ("." if f > 0.05 else " "))
    print(f"  y{110+yy/S:5.0f} {row}")
print("== TL orig colored map ==")
co = rgn(orig, 60, 110, 470, 295, 1.0)
cm = colored_mask(co)
h, w = cm.shape
for yy in range(0, h, 20):
    row = ""
    for xx in range(0, w, 20):
        f = cm[yy:yy+20, xx:xx+20].mean()
        row += "#" if f > 0.66 else ("+" if f > 0.33 else ("." if f > 0.05 else " "))
    print(f"  y{110+yy:5d} {row}")
print(f"render colored px={int(colored_mask(rgn(ren,60,110,470,295,S)).sum())} "
      f"({colored_mask(rgn(ren,60,110,470,295,S)).mean()*100:.1f}% of region); "
      f"orig colored px={int(colored_mask(co).sum())} ({colored_mask(co).mean()*100:.1f}%)")

print()
print("== BR render extra-ink map (slide cells 16px, x470..901 y342..535; 'X'=render-only ink) ==")
x0, y0, x1, y1 = 470, 342, 901, 535
co = rgn(orig, x0, y0, x1, y1, 1.0)
cr = rgn(ren, x0, y0, x1, y1, S)
crs = np.asarray(Image.fromarray(cr.astype(np.uint8)).resize((co.shape[1], co.shape[0]), Image.LANCZOS)).astype(int)
ink_o = colored_mask(co) | red_mask(co) | dark_mask(co)
ink_r = colored_mask(crs) | red_mask(crs) | dark_mask(crs)
dil = ink_o.copy()
for _ in range(3):
    dil = dil | np.roll(dil, 1, 0) | np.roll(dil, -1, 0) | np.roll(dil, 1, 1) | np.roll(dil, -1, 1)
extra = ink_r & ~dil
for yy in range(0, co.shape[0], 16):
    row = ""
    for xx in range(0, co.shape[1], 16):
        f = extra[yy:yy+16, xx:xx+16].mean()
        row += "X" if f > 0.3 else ("x" if f > 0.1 else ("." if f > 0.02 else " "))
    print(f"  y{y0+yy:5d} {row}")
