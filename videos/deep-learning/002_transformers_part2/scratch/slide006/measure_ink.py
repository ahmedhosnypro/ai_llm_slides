#!/usr/bin/env python3
"""Precise ink measurement: title + 6 agenda lines, slide-pt mapping, color census."""
from PIL import Image
import numpy as np
from collections import Counter

p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(p).convert("RGB")).astype(int)
H, W = a.shape[:2]
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

A, SX = 18.128, 0.961232   # frame_x = A + SX*slide_x
By, SY = -0.591, 0.957576  # frame_y = By + SY*slide_y
def mx(fx): return (fx - A) / SX
def my(fy): return (fy - By) / SY

red  = (R - G > 40) & (R - B > 40) & (R > 100)
blue = (B - R > 40) & (B - G > 40) & (B > 120)

# title: red ink, y 46..110, x 80..880
tys, txs = np.where(red[46:110, 80:880]); txs += 80; tys += 46
print("TITLE frame bbox x %d..%d y %d..%d" % (txs.min(), txs.max(), tys.min(), tys.max()))
print("TITLE slide  x %.1f..%.1f (w %.1f, cx %.1f)  y %.1f..%.1f (h %.1f)" %
      (mx(txs.min()), mx(txs.max()), mx(txs.max())-mx(txs.min()), (mx(txs.min())+mx(txs.max()))/2,
       my(tys.min()), my(tys.max()), my(tys.max())-my(tys.min())))
core = a[tys, txs]
cc = Counter(map(tuple, core))
print("TITLE core colors:", cc.most_common(6))

# per-line blue bands, full frame x 80..880, y 120..420
band = blue[120:420, 80:880]
brow = band.sum(axis=1)
lines, inl = [], False
for i, v in enumerate(brow):
    if v >= 3 and not inl: inl, st = True, i
    elif v < 3 and inl:
        inl = False
        if i - st > 4: lines.append((st+120, i-1+120))
if inl: lines.append((st+120, 419))
merged = []
for ln in lines:
    if merged and ln[0] - merged[-1][1] <= 5: merged[-1] = (merged[-1][0], ln[1])
    else: merged.append(list(ln))

print("\nAGENDA LINES:")
tops = []
for k, (y0, y1) in enumerate(merged, 1):
    sub = blue[y0:y1+1, 80:880]
    ys, xs = np.where(sub); xs += 80; ys += y0
    print("L%d frame x %d..%d y %d..%d (h %d) | slide x %.1f..%.1f (w %.1f, cx %.1f, left %.1f) y %.1f..%.1f (h %.1f)" %
          (k, xs.min(), xs.max(), ys.min(), ys.max(), ys.max()-ys.min()+1,
           mx(xs.min()), mx(xs.max()), mx(xs.max())-mx(xs.min()), (mx(xs.min())+mx(xs.max()))/2, mx(xs.min()),
           my(ys.min()), my(ys.max()), my(ys.max())-my(ys.min())))
    tops.append(my(ys.min()))
    ccore = a[ys, xs]; cc2 = Counter(map(tuple, ccore))
    print("   core:", cc2.most_common(4))
print("\npitches (top-to-top, slide pt):", [round(tops[i+1]-tops[i],1) for i in range(len(tops)-1)])

# badge numeral ink (dark px inside badge circle)
bx0,bx1,by0,by1 = 859,892,57,85
sub = a[by0:by1+1, bx0:bx1+1]
dark = (sub[:,:,0]<120)&(sub[:,:,1]<120)&(sub[:,:,2]<120)
dys,dxs = np.where(dark)
if len(dxs): print("\nbadge numeral dark ink n=%d (frame y %d..%d)" % (len(dxs), dys.min()+by0, dys.max()+by0))

# badge fill core + ring core samples
print("badge fill sample (875,71):", tuple(a[71,875]), " ring sample near x=858/893:", tuple(a[71,858]), tuple(a[71,893]))

# anything else? non-bg ink in lower half (y 380..515, x 45..915) excluding border
sub = a[380:515, 45:915]
nonbg = (np.abs(sub[:,:,0].astype(int)-233)>40) | (np.abs(sub[:,:,1]-233)>40) | (np.abs(sub[:,:,2]-231)>40)
print("\nlower-half non-bg px count:", int(nonbg.sum()))
if nonbg.sum():
    nys, nxs = np.where(nonbg)
    print("  bbox x %d..%d y %d..%d sample colors %s" % (nxs.min()+45, nxs.max()+45, nys.min()+380, nys.max()+380, Counter(map(tuple, sub[nys,nxs])).most_common(3)))
# mid area right of agenda lines x 480..900, y 110..380
sub2 = a[110:380, 480:900]
nonbg2 = (np.abs(sub2[:,:,0]-233)>40) | (np.abs(sub2[:,:,1]-233)>40) | (np.abs(sub2[:,:,2]-231)>40)
print("right-of-agenda non-bg px count:", int(nonbg2.sum()))
