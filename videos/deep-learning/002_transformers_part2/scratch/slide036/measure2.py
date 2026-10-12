#!/usr/bin/env python3
"""Stage 2: precise chrome borders, panel structure, diagram element geometry."""
import numpy as np
from PIL import Image

FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_036.jpg"
im = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def prof_h(y, x0, x1):
    return [f"{x}:{tuple(im[y,x])}" for x in range(x0, x1)]

# 1) chrome borders: scan a horizontal line in the title band (y=120) for red strokes
print("=== row 120, x 40..75:", " ".join(f"{x}:{tuple(im[120,x])}" for x in range(40, 76, 1)))
print("=== row 120, x 895..915:", " ".join(f"{x}:{tuple(im[120,x])}" for x in range(895, 916, 1)))
# vertical profile at x=480 (title band + panel top)
print("=== col 480, y 35..55:", " ".join(f"{y}:{tuple(im[y,480])}" for y in range(35, 56, 1)))
print("=== col 480, y 505..540:", " ".join(f"{y}:{tuple(im[y,480])}" for y in range(505, 540, 1)))

# 2) info panel: cream fill + blue border. blue mask
blue = (b > 140) & (r < 90) & (g < 90)
rows = blue.sum(axis=1)
print("=== blue-heavy rows (>150):", [(y, int(rows[y])) for y in range(H) if rows[y] > 150])
cols = blue.sum(axis=0)
print("=== blue-heavy cols (>80):", [(x, int(cols[x])) for x in range(W) if cols[x] > 80])
# cream fill rows: row fraction of cream-ish inside x 100..860
cream = (r > 245) & (g > 245) & (b > 195) & (b < 235)
frac = cream[:, 150:800].mean(axis=1)
print("=== cream rows (frac>0.5):", [y for y in range(H) if frac[y] > 0.5][:3], "...", [y for y in range(H) if frac[y] > 0.5][-3:])
fr = [y for y in range(H) if frac[y] > 0.5]
if fr: print("cream band:", fr[0], "..", fr[-1])
cfrac = cream[150:300].mean(axis=0)
cc = [x for x in range(W) if cfrac[x] > 0.5]
if cc: print("cream cols:", cc[0], "..", cc[-1])

# 3) navy banner precise
navy = (r < 70) & (g < 70) & (b > 80) & (b < 170)
nrows = navy.sum(axis=1)
nb = [y for y in range(H) if nrows[y] > 300]
print("=== navy banner rows (>300px):", nb[0] if nb else None, "..", nb[-1] if nb else None)
if nb:
    band = navy[nb[0]:nb[-1]+1]
    ncols = band.sum(axis=0)
    nbc = [x for x in range(W) if ncols[x] > (nb[-1]-nb[0]+1)*0.6]
    print("    banner cols:", nbc[0], "..", nbc[-1])
    # banner interior color census (center area, avoiding white text)
    inner = im[nb[0]+8:nb[-1]-7, nbc[0]+10:nbc[0]+200]
    print("    banner fill median:", np.median(inner.reshape(-1,3), axis=0))

# 4) token cells: upper yellow FFFF99-ish, lower pink
yelcell = (r > 235) & (g > 235) & (b > 120) & (b < 190)
pink = (r > 220) & (g > 110) & (g < 200) & (b > 120) & (b < 215) & (np.abs(r - b) < 110)
# restrict to diagram area y 330..500
def blobs(mask, y0, y1, minpx=40):
    sub = mask[y0:y1]
    from scipy import ndimage
    lab, n = ndimage.label(sub)
    out = []
    for i in range(1, n+1):
        ys, xs = np.where(lab == i)
        if len(ys) >= minpx:
            out.append((xs.min(), xs.max(), ys.min()+y0, ys.max()+y0, len(ys)))
    return sorted(out)
try:
    yb = blobs(yelcell, 320, 540, 60)
    print("=== yellow token cells (x0,x1,y0,y1,n):")
    for t in yb: print("   ", t)
    pb = blobs(pink, 320, 540, 60)
    print("=== pink token cells:")
    for t in pb: print("   ", t)
except Exception as e:
    print("blob error:", e)
