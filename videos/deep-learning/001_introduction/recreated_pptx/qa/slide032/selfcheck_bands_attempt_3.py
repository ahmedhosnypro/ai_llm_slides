#!/usr/bin/env python3
"""slide_032 band-based closed-loop check: each body line measured over ITS OWN rows
(band detection in the body column), so no neighbor bleed. Plus chrome-excluded title,
arrow-aware plane, words, boxes, bar. All values in frame px (render*72/150)."""
import sys
import numpy as np
from PIL import Image
K = sys.argv[1] if len(sys.argv) > 1 else "3"
BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide032"
A = np.asarray(Image.open(f"{BASE}/render_{K}.png").convert("RGB")).astype(int)
S = A.shape[0] / 540.0
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
blue = (b > 100) & (b > r + 40) & (b > g + 30)
red = (r > 120) & (g < 80) & (b < 80) & (r > g + 60)
blk = (r < 80) & (g < 80) & (b < 80)
brown = (r > 130) & (r < 220) & (g > 60) & (g < 150) & (b < 90) & (r > g + 40)

def bbox(mask, y0, y1, x0, x1):
    sub = mask[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    ys, xs = np.where(sub)
    if len(ys) == 0: return None
    return (round(x0+xs.min()/S,1), round(x0+xs.max()/S,1), round(y0+ys.min()/S,1), round(y0+ys.max()/S,1))

fails = 0
def chk(name, got, want, tol=4.0):
    global fails
    d = [round(gv-wv,1) for gv, wv in zip(got[:4], want[:4])]
    ok = all(abs(x) <= tol for x in d)
    if not ok: fails += 1
    print(f"{name:32s} got {str(got[:4]):28s} want {str(tuple(want[:4])):20s} d={d} {'PASS' if ok else 'FAIL'}")

col = blue[int(135*S):int(392*S), int(60*S):int(660*S)]
rc = col.sum(axis=1)
bands=[]; s=None
for i,c in enumerate(rc):
    if c>3 and s is None: s=i
    elif c<=3 and s is not None: bands.append((s,i-1)); s=None
targets = [("L1",95,286,149,170),("L2",88,573,175,196),("L3",88,452,238,259),
           ("L4",88,493,263,285),("L5",88,516,326,348),("L6",88,274,352,374)]
assert len(bands) == 6, f"expected 6 body bands, got {len(bands)}"
for k,(s,e) in enumerate(bands):
    y0, y1 = 135+s/S, 135+e/S
    xs = np.where(col[s:e+1].any(axis=0))[0]
    chk(f"body {targets[k][0]}", (60+xs.min()/S, 60+xs.max()/S, y0, y1), targets[k][1:])
sub = red[int(65*S):int(135*S), int(100*S):int(860*S)]
ys, xs = np.where(sub)
chk("title", (100+xs.min()/S, 100+xs.max()/S, 65+ys.min()/S, 65+ys.max()/S), (176,773,80,112))
chk("label '2-D Image'", bbox(red, 215, 268, 620, 900), (692,807,229,250))
bg = (b > 140) & (b > r + 15) & (r > 100) & (r < 200) & (g > 100) & (g < 190)
chk("left box border", bbox(bg, 120, 440, 60, 600), (77,591,139,422))
chk("right box border", bbox(red, 255, 515, 595, 905), (612,890,271,501))
pm = brown.copy(); pm[int(398*S):, int(770*S):] = False   # exclude arrow tail fully
chk("plane (arrow excl.)", bbox(pm, 300, 510, 620, 800), (645,774,315,495))
chk("filter", bbox(blue, 335, 390, 700, 780), (728,754,345,378))
chk("arrow in plane", bbox(red, 360, 410, 650, 770), (744,774,368,401), tol=5)
chk("'Grayscale'", bbox(blk, 265, 320, 620, 900), (684,863,276,308))
chk("'Filters' (y438+)", bbox(red, 438, 465, 760, 860), (777,842,441,456))
br = [y for y in range(int(505*S), A.shape[0]) if blk[y, int(100*S):int(880*S)].sum() > int(600*S)]
top = br[0]/S if br else 999
ok = abs(top-519) <= 4
if not ok: fails += 1
print(f"{'black bar top':32s} {top:.1f} want 519 {'PASS' if ok else 'FAIL'}")
print(f"\n{fails} hard failures")
