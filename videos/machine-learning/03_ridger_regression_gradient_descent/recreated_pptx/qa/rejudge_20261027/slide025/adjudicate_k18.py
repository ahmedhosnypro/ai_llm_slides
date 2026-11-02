#!/usr/bin/env python3
"""PIL adjudication of k17z3 judge findings D1..D6 on render_18 vs original slide_025.jpg.

render_18.png is 2001x1125 (S = 2001/960). Original is 960x540 slide-px.
All coordinates below are in SLIDE px; render coords = slide*S.
"""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = NS + "/recreated_pptx/qa/rejudge_20261027/slide025"
ORIG = NS + "/unique_slides/slide_025.jpg"
RENDER = Q + "/render_18.png"

S = 2001 / 960.0
orig = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
ren = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
assert ren.shape[:2] == (1125, 2001), ren.shape

def rgn(a, x0, y0, x1, y1, scale):
    """crop slide-px box (x0..x1, y0..y1 inclusive-ish) from array a at given scale"""
    return a[int(y0*scale):int(np.ceil(y1*scale))+1, int(x0*scale):int(np.ceil(x1*scale))+1]

def red_mask(a):
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (R > 110) & (G < 120) & (B < 120) & (R - G > 50) & (R - B > 50)

def dark_mask(a):
    return a.max(2) < 140

def colored_mask(a):
    mx, mn = a.max(2), a.min(2)
    return ((mx - mn) > 60) & (mx > 90) & ~red_mask(a)

print("== D4/D5: lowest colored/red/dark ink row in BL and BR plot regions ==")
for name, (x0, y0, x1, y1) in {
    "BL": (60, 296, 470, 535), "BR": (470, 342, 901, 535),
}.items():
    for tag, a, sc in (("orig", orig, 1.0), ("render", ren, S)):
        c = rgn(a, x0, y0, x1, y1, sc)
        m = colored_mask(c) | red_mask(c)
        ys, xs = np.nonzero(m)
        # slide-space coords
        sy = (ys / sc) + y0
        print(f"  {name} {tag}: colored/red ink max slide-y = {sy.max():.1f} "
              f"(house bottom stroke y=538.5; image bottoms BL=527 BR=531)")

print()
print("== D1: BL label anchor boxes, ink stats + cross-corr vs original ==")
LABELS = {
    "Global Maxima": (242, 304, 268, 319),
    "Local Maxima":  (286, 337, 315, 352),
    "Local Minima":  (286, 390, 311, 399),
    "Global Minima": (145, 439, 201, 465),
}
for name, (x0, y0, x1, y1) in LABELS.items():
    pad = 6
    co = rgn(orig, x0-pad, y0-pad, x1+pad, y1+pad, 1.0)
    cr = rgn(ren, x0-pad, y0-pad, x1+pad, y1+pad, S)
    cr_small = np.asarray(Image.fromarray(cr.astype(np.uint8)).resize((co.shape[1], co.shape[0]), Image.LANCZOS)).astype(int)
    do, dr = dark_mask(co), dark_mask(cr_small)
    # normalized cross correlation of binarized ink
    a = do.astype(float) - do.mean(); b = dr.astype(float) - dr.mean()
    ncc = float((a*b).sum() / (np.sqrt((a*a).sum()*(b*b).sum()) + 1e-9))
    yo, xo = np.nonzero(do); yr, xr = np.nonzero(dr)
    print(f"  '{name}' box x{x0}..{x1} y{y0}..{y1}: orig ink={do.sum()} bbox x{x0-pad+xo.min()}..{x0-pad+xo.max()} y{y0-pad+yo.min()}..{y0-pad+yo.max()} | "
          f"render ink={dr.sum()} bbox x{x0-pad+xr.min()}..{x0-pad+xr.max()} y{y0-pad+yr.min()}..{y0-pad+yr.max()} | NCC={ncc:.3f}")

print()
print("== D2: BR photo inset — photo-like (non-jet colored, textured) block scan in BR ==")
c_o = rgn(orig, 470, 342, 901, 535, 1.0)
c_r = rgn(ren, 470, 342, 901, 535, S)
c_rs = np.asarray(Image.fromarray(c_r.astype(np.uint8)).resize((c_o.shape[1], c_o.shape[0]), Image.LANCZOS)).astype(int)
for tag, c in (("orig", c_o), ("render", c_rs)):
    cm = colored_mask(c)
    # photo detection: colored pixels that are NOT jet-family. jet colors have B high when R low etc.
    R, G, B = c[:, :, 0], c[:, :, 1], c[:, :, 2]
    # jet runs blue->cyan->green->yellow->red; a photo has arbitrary colors incl. strong blue with low R AND white-ish mix
    nonjet = cm & ~(((B > R) & (B > 120)) | ((G > 100) & (R > 100)) | (R > 150))
    ys, xs = np.nonzero(nonjet)
    if len(xs):
        print(f"  {tag}: non-jet colored px={len(xs)} bbox slide x{470+xs.min()}..{470+xs.max()} y{342+ys.min()}..{342+ys.max()}")
    else:
        print(f"  {tag}: no non-jet colored px")
    # also: bright blue photo block = strong blue with low red in a solid rectangle
    photo = (B > 140) & (R < 100) & (G > 60) & (G < 200)
    ys, xs = np.nonzero(photo & ~cm | photo)
    frac = photo.mean()
    print(f"  {tag}: blue-photo mask frac={frac:.4f} px={int(photo.sum())}")

print()
print("== D3: TL surface silhouette — colored ink height profile ==")
for tag, a, sc in (("orig", orig, 1.0), ("render", ren, S)):
    c = rgn(a, 60, 110, 470, 295, sc)
    cm = colored_mask(c)
    ys, xs = np.nonzero(cm)
    h = ys / sc
    print(f"  TL {tag}: colored px={len(xs)} slide-y range {h.min()+110:.1f}..{h.max()+110:.1f} "
          f"(height {h.max()-h.min():.1f}px) x range {(xs/sc).min()+60:.1f}..{(xs/sc).max()+60:.1f}")
    # vertical profile: max width of colored ink per y-band of 10 slide-px
    prof = []
    for yb in range(110, 295, 10):
        band = cm[int(yb*sc)-int(110*sc):int((yb+10)*sc)-int(110*sc)]
        prof.append(int(band.sum()/sc) if band.size else 0)
    print(f"    width profile (per 10px y-band, slide px): {prof}")

print()
print("== D6: label boxes vs plot vertical centers ==")
plots = {"TL": (60, 116, 470, 289), "TR": (470, 116, 901, 316), "BR": (470, 346, 901, 530), "BL": (60, 296, 470, 527)}
for n, (x0, y0, x1, y1) in plots.items():
    print(f"  plot {n}: y {y0}..{y1} center {(y0+y1)/2:.0f}")
for i, (x, y, w, h) in enumerate([(270,137,137,42),(475,184,137,42),(474,354,138,38),(382,452,137,38)], 1):
    print(f"  label{i}: y {y}..{y+h} center {(y+y+h)/2:.0f}")
