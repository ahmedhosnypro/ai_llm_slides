#!/usr/bin/env python3
"""measure4.py — pass 4: exact modal colors, gridline positions, operator bboxes
(cursor-excluded), note box border/fill/text metrics, bullet word segmentation,
title font solving."""
from PIL import Image, ImageFont
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_044.jpg"
im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

def runs(mask_1d, min_len=1):
    idx = np.where(mask_1d)[0]
    if len(idx) == 0:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v == p + 1:
            p = v
        else:
            if p - s + 1 >= min_len:
                out.append((s, p))
            s = p = v
    if p - s + 1 >= min_len:
        out.append((s, p))
    return out

def exact_modal(x0, x1, y0, y1, n=4):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    return [(tuple(int(c) for c in vals[i]), int(counts[i])) for i in order]

# --- exact fill colors: pick uniform interiors ---
print("cyan cell (r1c3 interior):", exact_modal(190, 210, 180, 195))
print("green cell (r3c3 interior):", exact_modal(200, 215, 245, 258))
print("yellow cell (f33 center):", exact_modal(470, 490, 265, 280))
print("out green (o55 r1c1):", exact_modal(632, 650, 212, 228))
print("gridline sample (vertical between r1c1/r1c2 of 7x7, y~180):",
      [tuple(a[182, x]) for x in range(136, 146)])
print("gridline sample (horizontal, x~120, y 196..208):",
      [tuple(a[y, 120]) for y in range(196, 210)])
print("numeral black (r2c2 '1'): ", exact_modal(146, 160, 198, 212, 6))
print("title red:", exact_modal(300, 310, 80, 88))
print("inner frame red (col 77):", [tuple(a[y, 77]) for y in [200, 300]],
      "row 122:", [tuple(a[122, x]) for x in [200, 500]])
print("note border (col 77 y450):", [tuple(a[y, 77]) for y in [440, 450, 460]],
      "(row ~391):", [tuple(a[391, x]) for x in [100, 300, 500]],
      "(row ~512):", [tuple(a[512, x]) for x in [100, 300, 500]])
print("note fill (300,430):", tuple(a[430, 300]), "(500,200):", tuple(a[430, 500]))
print("note text navy:", exact_modal(95, 130, 410, 418, 4))
print("bullet circle region:", exact_modal(108, 128, 138, 152, 8))

# --- gridline positions: brightness dips along mid-cell lines ---
def dips(fixed, lo, hi, axis, thresh=200):
    if axis == "row":  # scan x at fixed y
        vals = a[fixed, lo:hi].mean(axis=1)
    else:              # scan y at fixed x
        vals = a[lo:hi, fixed].mean(axis=1)
    dark = vals < thresh
    return [(s + lo, e + lo) for s, e in runs(dark, min_len=1)]

print("7x7 vertical gridlines at y=178 (row1):", dips(178, 101, 378, "row"))
print("7x7 horizontal gridlines at x=110 (col1):", dips(110, 173, 383, "col"))
print("f33 vertical gridlines at y=252:", dips(252, 440, 527, "row"))
print("f33 horizontal gridlines at x=445:", dips(445, 247, 313, "col"))
print("o55 vertical gridlines at y=208:", dips(208, 622, 820, "row"))
print("o55 horizontal gridlines at x=630:", dips(630, 203, 354, "col"))

# --- operators, cursor-excluded ---
def inkbox(x0, x1, y0, y1, label):
    sub = a[y0:y1, x0:x1]
    ink = (sub[..., 0] < 150) & (sub[..., 1] < 150) & (sub[..., 2] < 150)
    ys, xs = np.where(ink)
    if len(xs):
        print(f"{label}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} (w {xs.max()-xs.min()+1} h {ys.max()-ys.min()+1})")
    else:
        print(f"{label}: no ink")

inkbox(380, 438, 250, 320, "operator *")
inkbox(528, 620, 250, 320, "operator =")
inkbox(560, 615, 360, 410, "cursor artifact bbox")
inkbox(380, 438, 320, 383, "star gap lower (should be empty)")
inkbox(528, 620, 320, 370, "eq gap lower (should be empty)")

# --- bullet band: word segmentation via column gaps ---
band = a[132:158, 100:880]
ink = (band[..., 0] < 210) | (band[..., 1] < 210) | (band[..., 2] < 210)
colc = ink.sum(axis=0)
words = []
s = None
for i, v in enumerate(colc):
    if v > 0 and s is None:
        s = i
    elif v == 0 and s is not None:
        words.append((s + 100, i - 1 + 100)); s = None
if s is not None:
    words.append((s + 100, len(colc) - 1 + 100))
# merge runs separated by <=2 px (intra-word letter gaps are ~1-3px at this size)
merged = []
for w in words:
    if merged and w[0] - merged[-1][1] <= 3:
        merged[-1] = (merged[-1][0], w[1])
    else:
        merged.append(list(w))
print("bullet word-ish segments (gap>3):", merged)
# per-segment vertical extents
for (sx, ex) in merged:
    sub = a[132:158, sx:ex + 1]
    ink2 = (sub[..., 0] < 210) | (sub[..., 1] < 210) | (sub[..., 2] < 210)
    ys, xs = np.where(ink2)
    print(f"  seg x{sx}..{ex}: y {ys.min()+132}..{ys.max()+132}")

# --- note text lines: per-line ink bbox ---
navy = (B - R > 40) & (R < 140)
lines = [(406, 423), (432, 450), (459, 477), (486, 505)]
for i, (y0, y1) in enumerate(lines):
    sub = navy[y0:y1 + 1, 80:700]
    ys, xs = np.where(sub)
    print(f"note L{i+1}: x {xs.min()+80}..{xs.max()+80} y {ys.min()+y0}..{ys.max()+y0}")

# --- title font solving: TNR Bold vs Arial Bold at cap 25px ---
# cap top 68, baseline ~93 (row counts collapse at 93); ink w 541 (x 211..751)
TITLE = "Solution? Zero-padding! , Others !!"
for name, path in [("LiberationSerif-Bold", "/usr/share/fonts/TTF/LiberationSerif-Bold.ttf"),
                   ("LiberationSans-Bold", "/usr/share/fonts/TTF/LiberationSans-Bold.ttf"),
                   ("DejaVuSerif-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"),
                   ("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")]:
    try:
        for size in range(30, 45):
            f = ImageFont.truetype(path, size)
            w = f.getlength(TITLE)
            asc, desc = f.getmetrics()
            if abs(w - 541) <= 12:
                print(f"{name} size {size}: advance {w:.0f} (target 541) ascent {asc} descent {desc}")
    except OSError as e:
        print(name, "FONT MISSING", e)
