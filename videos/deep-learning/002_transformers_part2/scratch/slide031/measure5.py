#!/usr/bin/env python3
"""Fine scan: derivation line bands, callout, ribbon, left/mid panel internals."""
import numpy as np
from PIL import Image
from scipy.ndimage import label, find_objects

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img).astype(int)

def runs(m, minlen=1):
    out, i, n = [], 0, len(m)
    while i < n:
        if m[i]:
            j = i
            while j < n and m[j]: j += 1
            if j - i >= minlen: out.append((i, j - 1))
            i = j
        else: i += 1
    return out

# ---- derivation lines with lower threshold ----
pan = a[258:512, 66:853]
R, G, B = pan[:, :, 0], pan[:, :, 1], pan[:, :, 2]
ink = (pan.min(axis=2) < 190) | ((pan.max(axis=2) - pan.min(axis=2)) > 45)
rowsum = ink.sum(axis=1)
prof = [int(v) for v in rowsum]
print("row profile (y258+i : count) — valleys marked:")
prev = 0
for i, v in enumerate(prof):
    if (v == 0 and prev > 0) or (v > 0 and prev == 0):
        print(f"  transition at y{258+i} -> {v}")
    prev = v
bands = runs(rowsum > 1, 4)
print("fine bands:", [(258 + y0, 258 + y1) for y0, y1 in bands])

# per fine band: x extent + red/blue split
for y0, y1 in bands:
    seg = pan[y0:y1 + 1]
    r = (seg[:, :, 0] - seg[:, :, 1] > 45) & (seg[:, :, 0] > 120)
    b = (seg[:, :, 2] - seg[:, :, 0] > 45) & (seg[:, :, 2] > 100)
    d = (seg.max(axis=2) < 120)
    cols_any = np.where((r | b | d).any(axis=0))[0]
    rc = np.where(r.any(axis=0))[0]; bc = np.where(b.any(axis=0))[0]; dc = np.where(d.any(axis=0))[0]
    def ext(c):
        return f"x{66+c.min()}..{66+c.max()}" if len(c) else "-"
    print(f"  band y{258+y0}..{258+y1}: all {ext(cols_any)} red {ext(rc)} ({int(r.sum())}px) blue {ext(bc)} ({int(b.sum())}px) dark {ext(dc)} ({int(d.sum())}px)")

# trailing '=' check: rightmost glyph of each of lines 1..5
print("\nrightmost 30px of each line band, column occupancy:")
for (y0, y1), nm in zip(bands[:6], ["L1", "L2", "L3", "L4", "L5", "L6"]):
    if y1 - y0 > 60: continue
    seg = ink[y0:y1 + 1]
    occ = seg.any(axis=0)
    xs = np.where(occ)[0]
    if len(xs) == 0: continue
    # last contiguous run
    rr = runs(occ, 1)
    last = rr[-1]
    print(f"  {nm}: last ink run x{66+last[0]}..{66+last[1]} (w={last[1]-last[0]+1}) full-extent x{66+xs.min()}..{66+xs.max()}")

# ---- callout interior colors ----
print("\ncallout samples:", [(x, tuple(a[y, x])) for x, y in [(585, 478), (720, 485), (600, 495), (700, 475), (640, 474)]])
# ---- ribbon: pale yellow scan ----
reg = a[400:516, 700:925]
py = (reg[:, :, 0] > 225) & (reg[:, :, 1] > 225) & (reg[:, :, 2] > 160) & (reg[:, :, 2] < 225) & ((reg[:, :, 0] - reg[:, :, 2]) > 20)
lab, n = label(py)
print("\npale-yellow comps in ribbon zone (x700..925, y400..516):")
for sl in find_objects(lab):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 100:
        print(f"  y{400+sl[0].start}..{400+sl[0].stop-1} x{700+sl[1].start}..{700+sl[1].stop-1} ({w}x{h})")
print("ribbon samples:", [(x, y, tuple(a[y, x])) for x, y in [(800, 445), (790, 465), (810, 490), (830, 500), (780, 500), (850, 470)]])

# ---- LEFT PANEL internals (x60..205, y44..218) ----
print("\n== LEFT PANEL ==")
lp = a[44:218, 58:206]
Rl, Gl, Bl = lp[:, :, 0], lp[:, :, 1], lp[:, :, 2]
redl = (Rl - Gl > 60) & (Rl > 130)
darkl = (lp.max(axis=2) < 120)
yelhl = (Rl > 220) & (Gl > 220) & (Bl < 150)
inkl = redl | darkl | yelhl
rs = inkl.sum(axis=1)
print("left panel ink bands:", [(44 + y0, 44 + y1) for y0, y1 in runs(rs > 1, 2)])
lab, _ = label(yelhl)
print("yellow highlight comps:")
for sl in find_objects(lab):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 30:
        print(f"  y{44+sl[0].start}..{44+sl[0].stop-1} x{58+sl[1].start}..{58+sl[1].stop-1} ({w}x{h})")
lab, _ = label(redl)
print("red comps >40px:")
for sl in find_objects(lab):
    h = sl[0].stop - sl[0].start; w = sl[1].stop - sl[1].start
    if h * w > 40:
        print(f"  y{44+sl[0].start}..{44+sl[0].stop-1} x{58+sl[1].start}..{58+sl[1].stop-1} ({w}x{h})")

# ---- MIDDLE PANEL internals (x200..690, y44..218) ----
print("\n== MIDDLE PANEL ==")
mp = a[44:218, 200:690]
Rm, Gm, Bm = mp[:, :, 0], mp[:, :, 1], mp[:, :, 2]
redm = (Rm - Gm > 60) & (Rm > 130)
darkm = (mp.max(axis=2) < 120)
bluem = (Bm - Rm > 60) & (Bm > 100)
inkm = redm | darkm | bluem
rs = inkm.sum(axis=1)
print("middle panel ink bands:", [(44 + y0, 44 + y1) for y0, y1 in runs(rs > 1, 2)])
for y0, y1 in runs(rs > 1, 2):
    seg = inkm[y0:y1 + 1]
    cols = np.where(seg.any(axis=0))[0]
    rr_ = np.where(redm[y0:y1 + 1].any(axis=0))[0]
    bb_ = np.where(bluem[y0:y1 + 1].any(axis=0))[0]
    def ext(c): return f"x{200+c.min()}..{200+c.max()}" if len(c) else "-"
    print(f"  band y{44+y0}..{44+y1}: all {ext(cols)} red {ext(rr_)} blue {ext(bb_)}")
