#!/usr/bin/env python3
"""Measure pass 2: sample raw colors, find exact container border + highlight boxes."""
from PIL import Image
import numpy as np
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_012.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def med(x, y, k=2):
    p = a[max(0,y-k):y+k+1, max(0,x-k):x+k+1].reshape(-1,3)
    m = np.median(p, axis=0).astype(int)
    return f"({m[0]},{m[1]},{m[2]}) #{m[0]:02X}{m[1]:02X}{m[2]:02X}"

print("== samples ==")
print("panel gray (x=60,y=300):", med(60, 300))
print("page white (x=500,y=300):", med(500, 300))
print("tan box interior (x=345,y=60):", med(345, 60))
print("tan box interior (x=590,y=80):", med(590, 80))
print("pink box interior (x=404,y=174):", med(404, 174))
print("pink box interior (x=650,y=182):", med(650, 182))
print("container border top (x=400,y=53):", med(400, 53))
print("container border bot (x=400,y=525):", med(400, 525))
print("panel top stroke (x=400,y=43):", med(400, 43))
print("panel bot stroke (x=400,y=538):", med(400, 538))
print("watermark text (x=115,y=250):", med(115, 250))
print("tan date region (x=115,y=290):", med(115, 290))

# darkest pixel inside tan title box -> glyph core color
tb = a[54:84, 334:600]
lum = tb.sum(axis=2)
iy, ix = np.unravel_index(np.argmin(lum), lum.shape)
print("darkest in title box:", med(334+ix, 54+iy), "at", (334+ix, 54+iy))
# glyph core: median of pixels below 40th percentile luminance inside box
tl = tb.sum(axis=2)
mask = tl < np.percentile(tl, 3)
print("title glyph core median:", np.median(tb[mask], axis=0).astype(int))

pb = a[171:185, 398:459]
pl = pb.sum(axis=2)
mask = pl < np.percentile(pl, 5)
print("affiliation glyph core median (in pink):", np.median(pb[mask], axis=0).astype(int))

# == container border: scan for red-ish rows/cols with looser mask ==
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
redish = (r - np.maximum(g, b) > 60) & (r > 110)
row_counts = redish.sum(axis=1)
col_counts = redish.sum(axis=0)
print("== redish rows (count>150) ==", [(y, int(row_counts[y])) for y in range(H) if row_counts[y] > 150])
print("== redish cols (count>150) ==", [(x, int(col_counts[x])) for x in range(W) if col_counts[x] > 150])

# container border: restrict to x in [90, 810] for rows, y in [45, 535] for cols
sub = redish[45:535, 90:810]
rc = sub.sum(axis=1); cc = sub.sum(axis=0)
print("container rows:", [(45+y, int(rc[y])) for y in range(sub.shape[0]) if rc[y] > 250])
print("container cols:", [(90+x, int(cc[x])) for x in range(sub.shape[1]) if cc[x] > 250])

# == tan clusters with adaptive mask around sampled core ==
def clusters(mask, min_n=40, name=""):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) >= min_n:
            out.append((xs.min(), xs.max(), ys.min(), ys.max(), len(ys)))
    out.sort(key=lambda t: (t[2], t[0]))
    print(f"== {name} clusters ({len(out)}) ==")
    for x0, x1, y0, y1, n in out:
        print(f"  x[{x0},{x1}] y[{y0},{y1}] n={n}")
    return out

tanc = np.array([247, 213, 168])
dtan = np.abs(a - tanc).sum(axis=2)
clusters(dtan < 120, 40, "tan")

pinkc = np.array([255, 155, 232])
dpink = np.abs(a - pinkc).sum(axis=2)
clusters(dpink < 150, 40, "pink")

# == dark ink bands inside container only (exclude border rows/cols) ==
lum = (r*299 + g*587 + b*114)//1000
dark = lum < 120
dark[:54,:] = False; dark[524:,:] = False; dark[:,:96] = False; dark[:,797:] = False
prof = [(y, int(dark[y].sum())) for y in range(H) if dark[y].sum() > 40]
bands = []
for y, c in prof:
    if bands and y <= bands[-1][1] + 4:
        bands[-1][1] = y; bands[-1][2] = max(bands[-1][2], c)
    else:
        bands.append([y, y, c])
print("== ink bands in container ==")
for y0, y1, c in bands:
    seg = dark[y0:y1+1]
    xs = np.where(seg.any(axis=0))[0]
    print(f"  y[{y0},{y1}] maxn={c} x[{xs.min()},{xs.max()}]")

# == gray watermark: low-sat mid-gray in x 96..150 ==
sat = np.max(a, axis=2) - np.min(a, axis=2)
wm = (sat < 40) & (lum > 100) & (lum < 200)
wm[:, :96] = False; wm[:, 150:] = False; wm[:60, :] = False; wm[524:, :] = False
ys, xs = np.where(wm)
print(f"== gray watermark bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] n={len(ys)}")
# row profile of watermark ink
wrow = wm.sum(axis=1)
runs = [(y, int(wrow[y])) for y in range(H) if wrow[y] > 2]
if runs:
    print("  wm rows first/last:", runs[0], runs[-1], "count rows:", len(runs))
