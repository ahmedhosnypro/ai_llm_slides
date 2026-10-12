#!/usr/bin/env python3
"""forensics20: starburst vs badge-window + line-1, org vs render_5 (attempt-2 fix basis).
Badge checker window (frame px): x[857..929] y[35..107]  (canonical center (893,71) d36).
Windows measured at frame scale for the 960x540 original; render scaled by /2.08333.
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
org = np.asarray(Image.open(VID + "/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(VID + "/recreated_pptx/qa/slide045/render_5.png").convert("RGB")).astype(int)
s = ren.shape[0] / 540.0

def mask(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    yel = (r > 200) & (g > 200) & (b < 190)          # checker yellow (badge fill + star AA dust)
    yel2 = (r > 200) & (g > 200) & (b < 220)         # looser yellow (star fill F0F6CE b=206)
    red = (r > 120) & (g < 110) & (b < 110)
    dark = (r < 110) & (g < 110) & (b < 110)
    return yel, yel2, red, dark

oyel, oyel2, ored, odark = mask(org)
ryel, ryel2, rred, rdark = mask(ren)

WIN = (857, 929, 35, 107)  # x0,x1,y0,y1 frame px
print("== A. checker-yellow inside BADGE WINDOW (x857..929 y35..107) ==")
for name, ym in (("org", oyel), ("ren5", ryel)):
    w = ym[WIN[2]:WIN[3], WIN[0]:WIN[1]]
    n = int(w.sum())
    if n:
        ys, xs = np.where(w)
        print(f"  {name}: n={n} bbox frame x{WIN[0]+xs.min()}..{WIN[0]+xs.max()} y{WIN[2]+ys.min()}..{WIN[2]+ys.max()}")
    else:
        print(f"  {name}: n=0")

print("== B. star components (loose yellow + red), region x740..935 y25..175 ==")
def comps(ym, region, min_n=25):
    x0, x1, y0, y1 = region
    m = ym[y0:y1, x0:x1]
    # simple 4-connected labeling
    lbl = np.zeros(m.shape, int); cur = 0
    from collections import deque
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            if m[i, j] and not lbl[i, j]:
                cur += 1; q = deque([(i, j)]); lbl[i, j] = cur
                while q:
                    a, b_ = q.popleft()
                    for da, db in ((1,0),(-1,0),(0,1),(0,-1)):
                        na, nb = a+da, b_+db
                        if 0 <= na < m.shape[0] and 0 <= nb < m.shape[1] and m[na, nb] and not lbl[na, nb]:
                            lbl[na, nb] = cur; q.append((na, nb))
    out = []
    for c in range(1, cur+1):
        ys, xs = np.where(lbl == c)
        if len(ys) >= min_n:
            out.append((x0+xs.min(), x0+xs.max(), y0+ys.min(), y0+ys.max(), len(ys)))
    return sorted(out, key=lambda t: -t[4])

for name, ym2, rm in (("org", oyel2, ored), ("ren5", ryel2, rred)):
    ycomps = comps(ym2, (740, 935, 25, 175))
    rcomps = comps(rm, (740, 935, 25, 175))
    print(f"  {name} loose-yellow comps: " + "; ".join(f"x{c[0]}..{c[1]} y{c[2]}..{c[3]} n={c[4]}" for c in ycomps[:6]))
    print(f"  {name} red comps:        " + "; ".join(f"x{c[0]}..{c[1]} y{c[2]}..{c[3]} n={c[4]}" for c in rcomps[:6]))

print("== C. star ink (any of loose-yellow|red) per-column presence ABOVE defbox border (y25..113) ==")
for name, ym2, rm in (("org", oyel2, ored), ("ren5", ryel2, rred)):
    m = (ym2 | rm)
    sub = m[25:114, 740:935]
    cols = np.where(sub.any(axis=0))[0] + 740
    if len(cols):
        # contiguous runs
        runs = []
        st = p = cols[0]
        for c in cols[1:]:
            if c == p + 1: p = c
            else: runs.append((st, p)); st = p = c
        runs.append((st, p))
        print(f"  {name}: col runs {runs}")
        rows = np.where(m[25:114, 740:935].any(axis=1))[0] + 25
        print(f"  {name}: rows {rows.min()}..{rows.max()}")
    else:
        print(f"  {name}: none")

print("== D. defbox top border rows (y110..120) red|blue-dark presence x756..900 ==")
for name, rm, dm in (("org", ored, odark), ("ren5", rred, rdark)):
    for y in range(112, 119):
        row_r = rm[y, 756:900]; row_d = dm[y, 756:900]
        # find interrupted spans of border (non-ink) assuming border spans most
        borderish = row_r | row_d
        gapc = np.where(~borderish)[0] + 756
        if len(gapc) > 60:
            print(f"  {name} y{y}: border mostly ABSENT (non-ink cols {len(gapc)}, {gapc.min()}..{gapc.max()})")
        else:
            print(f"  {name} y{y}: border present, gaps at {gapc[:12]}{'...' if len(gapc)>12 else ''}")

print("== E. line-1 text row dark ink (y117..150) bbox x756..900 ==")
for name, dm in (("org", odark), ("ren5", rdark)):
    sub = dm[117:150, 756:900]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  {name}: text bbox x{756+xs.min()}..{756+xs.max()} y{117+ys.min()}..{117+ys.max()} n={len(ys)}")
    else:
        print(f"  {name}: no dark ink")

print("== F. star ink vs line-1 band y117..150: star columns (loose-yellow|red) ==")
for name, ym2, rm in (("org", oyel2, ored), ("ren5", ryel2, rred)):
    m = (ym2 | rm)[117:150, 740:935]
    cols = np.where(m.any(axis=0))[0] + 740
    print(f"  {name}: star-ink cols in text band: {cols.min()}..{cols.max()} n_cols={len(cols)}" if len(cols) else f"  {name}: none")

print("== G. org star: lowest ink per column (bottom envelope), x756..900, y in 100..170 ==")
m = (oyel2 | ored)
for x in range(756, 900, 6):
    col = np.where(m[100:170, x])[0]
    print(f"  org x{x}: bottom y={100+col.max() if len(col) else '-'}", end="")
    if (x - 756) % 36 == 30: print()
print()
