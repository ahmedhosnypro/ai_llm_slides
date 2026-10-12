#!/usr/bin/env python3
"""m2.py — front panel internals + Y outputs, via color masks.
Regions of interest in 960x540 frame px."""
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_039.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)

def runs(m, min_len=2):
    out = []; s = None
    for i, v in enumerate(m):
        if v and s is None: s = i
        elif not v and s is not None:
            if i - s >= min_len: out.append((s, i - 1))
            s = None
    if s is not None and len(m) - s >= min_len: out.append((s, len(m) - 1))
    return out

def bbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(xs): return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())

# color masks
green  = (np.abs(a[:,:,0]-0)<70) & (np.abs(a[:,:,1]-160)<50) & (np.abs(a[:,:,2]-80)<60) & (a[:,:,1]-a[:,:,0]>60)
tan    = (np.abs(a[:,:,0]-205)<28) & (np.abs(a[:,:,1]-160)<28) & (np.abs(a[:,:,2]-105)<35)
pink   = (a[:,:,0]>235) & (np.abs(a[:,:,1]-195)<35) & (np.abs(a[:,:,2]-205)<35) & (a[:,:,0]-a[:,:,1]>25)
blue   = (a[:,:,2]>150) & (a[:,:,2]-a[:,:,0]>60) & (a[:,:,1]<160)   # strong blue (box borders, pill text)
paleblu= (np.abs(a[:,:,0]-200)<25) & (np.abs(a[:,:,1]-222)<20) & (np.abs(a[:,:,2]-244)<20) & (a[:,:,2]-a[:,:,0]>25)
red    = (a[:,:,0]>150) & (a[:,:,1]<90) & (a[:,:,2]<90)
cream  = (a[:,:,0]>248) & (a[:,:,1]>248) & (np.abs(a[:,:,2]-225)<30) & (a[:,:,2]-a[:,:,0]<0)

# ---- Y output boxes (above panels, y<235): green dashed boxes
print("== green in y[100,240] (Y boxes) rows:")
gz = green[100:240, :]
for s, e in runs(gz.sum(axis=1) > 2, 2):
    band = gz[s:e+1, :]
    bb = bbox(green, 0, 100+s, 959, 101+e)
    print(f"  green band y[{100+s},{100+e}] bbox x{bb[0]}..{bb[1]}")
print("== red in y[100,240] (Y arrows + labels):")
rz = red[100:240, :]
for s, e in runs(rz.sum(axis=1) > 2, 2):
    bb = bbox(red, 0, 100+s, 959, 101+e)
    print(f"  red band y[{100+s},{100+e}] bbox x{bb[0]}..{bb[1]}")

# ---- front panel: green dashed boxes (left X, right X, bottom row)
print("== green in panel1 y[225,500] x[110,700]:")
gp = green[225:500, 110:700]
for s, e in runs(gp.sum(axis=1) > 3, 2):
    band = gp[s:e+1, :]
    cols = band.sum(axis=0)
    rr = runs(cols > 0, 2)
    if rr:
        print(f"  y[{225+s},{225+e}] x-runs:", [(110+r0, 110+r1) for r0, r1 in rr][:8])

# ---- Dot Product box (tan)
print("== tan bbox in panel1:", bbox(tan, 110, 225, 700, 500))
tz = tan[225:500, 110:700]
for s, e in runs(tz.sum(axis=1) > 10, 3):
    band = tz[s:e+1, :]
    cols = band.sum(axis=0)
    rr = runs(cols > 0, 2)
    if rr: print(f"  tan y[{225+s},{225+e}] x-runs:", [(110+r0, 110+r1) for r0, r1 in rr][:6])

# ---- pink Scaling/Softmax boxes
print("== pink rows in x[300,560] y[240,480]:")
pk = pink[240:480, 300:560]
for s, e in runs(pk.sum(axis=1) > 8, 3):
    band = pk[s:e+1, :]
    cols = band.sum(axis=0)
    rr = runs(cols > 2, 2)
    if rr: print(f"  pink y[{240+s},{240+e}] x-runs:", [(300+r0, 300+r1) for r0, r1 in rr][:6])

# ---- pale blue Sigma box
print("== paleblue bbox y[140,260] x[400,720]:", bbox(paleblu, 400, 140, 720, 260))

# ---- cream pills along panel tops (y 150..240)
print("== cream pills y[150,245]:")
cr = cream[150:245, :]
for s, e in runs(cr.sum(axis=1) > 15, 3):
    band = cr[s:e+1, :]
    cols = band.sum(axis=0)
    rr = runs(cols > 2, 4)
    if rr: print(f"  cream y[{150+s},{150+e}] x-runs:", [(r0, r1) for r0, r1 in rr][:14])
