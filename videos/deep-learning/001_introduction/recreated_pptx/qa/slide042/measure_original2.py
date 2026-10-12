#!/usr/bin/env python3
"""Pass 2 — precise per-region geometry for slide 042: title metrics, panel edges,
input slab faces + s-arrow, filter slices, output box faces, equation box + per-line
equation ink bands, legend per-line x extents + colors, diagram label ink bands."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_042.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def modal(x0, x1, y0, y1, label, mask=None, n=4):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    if mask is not None:
        reg = IM[y0:y1+1, x0:x1+1][mask[y0:y1+1, x0:x1+1]]
        if len(reg) == 0: print(f"{label}: mask empty"); return
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    print(f"{label}: " + ", ".join('#%02X%02X%02X(%d)' % (*vals[i], counts[i]) for i in order))

def bands2(rows, gap=3):
    if len(rows) == 0: return []
    out = []; s = p = rows[0]
    for c in rows[1:]:
        if c - p <= gap: p = c
        else: out.append((int(s), int(p))); s = p = c
    out.append((int(s), int(p)))
    return out

def xruns(mask_row, minlen=1):
    xs = np.where(mask_row)[0]
    if len(xs) == 0: return []
    runs = []; s = p = xs[0]
    for c in xs[1:]:
        if c <= p + 1: p = c
        else: runs.append((int(s), int(p))); s = p = c
    runs.append((int(s), int(p)))
    return [(a, bb) for (a, bb) in runs if bb - a + 1 >= minlen]

# ============ 1. TITLE (tight window y70..125, x100..860) ============
print("=" * 20, "TITLE")
redt = (r > 120) & (g < 110) & (b < 110)
tm = np.zeros_like(redt); tm[70:126, 100:860] = redt[70:126, 100:860]
ys = np.where(tm.sum(axis=1) > 0)[0]
xs = np.where(tm.sum(axis=0) > 0)[0]
print(f"title ink: x {xs.min()}..{xs.max()} (w {xs.max()-xs.min()+1}, center {(xs.min()+xs.max())/2})  y {ys.min()}..{ys.max()}")
rowsum = [(int(y), int(tm[y].sum())) for y in range(ys.min(), ys.max()+1)]
print("title rowsums:", rowsum)
modal(100, 860, 70, 126, "title ink modal", mask=tm, n=6)

# ============ 2. INNER PANEL (white fill extent + red border) ============
print("=" * 20, "INNER PANEL")
white = (r > 240) & (g > 240) & (b > 240)
# white row extent at a clean y (no content): find rows where white spans wide
for y in [150, 200, 300, 450, 490, 500]:
    rr = xruns(white[y, 40:920], 30)
    print(f"white y={y}: " + (f"{[(a+40,bb+40) for a,bb in rr]}" if rr else "none"))
# white col extent at clean x
for x in [90, 300, 540, 700, 870, 885]:
    cc = np.where(white[130:510, x])[0]
    if len(cc) > 50: print(f"white x={x}: y {cc.min()+130}..{cc.max()+130} n={len(cc)}")
# red border strokes precise (loose red mask)
redl = (r > 100) & (r < 220) & (g < 110) & (b < 120)
print("inner top stroke rows y130..145 (n red px in x80..888):",
      [(y, int(redl[y, 80:888].sum())) for y in range(130, 146) if redl[y, 80:888].sum() > 300])
print("inner bottom rows y500..512:", [(y, int(redl[y, 80:888].sum())) for y in range(500, 513) if redl[y, 80:888].sum() > 300])
print("inner left cols x70..84 (n red px y140..505):",
      [(x, int(redl[140:506, x].sum())) for x in range(70, 85) if redl[140:506, x].sum() > 200])
print("inner right cols x880..896:",
      [(x, int(redl[140:506, x].sum())) for x in range(880, 897) if redl[140:506, x].sum() > 200])
modal(80, 888, 134, 138, "inner top stroke color", mask=redl)

# ============ 3. INPUT SLAB ============
print("=" * 20, "INPUT SLAB")
modal(60, 320, 150, 370, "slab region modal", n=8)
# precise face colors via tight modal probes
modal(140, 240, 250, 330, "slab front probe")
modal(160, 260, 185, 215, "slab top probe")
modal(250, 300, 240, 320, "slab side probe")
# orange masks (broad, split by brightness)
o = (r > 130) & (g > 60) & (b < 120) & (r > b + 60) & (abs(r - 200) < 80)
o_m = np.zeros_like(o); o_m[130:400, 40:340] = o[130:400, 40:340]
ys3, xs3 = np.where(o_m)
print(f"slab ALL-orange ink: x {xs3.min()}..{xs3.max()}  y {ys3.min()}..{ys3.max()}")
# row profile of orange: to find top face vs front face boundary
prof = [(int(y), int(o_m[y].sum())) for y in range(ys3.min(), ys3.max()+1, 3)]
print("slab orange rowsums:", prof)

# ============ 4. FILTER STACK ============
print("=" * 20, "FILTER STACK")
cyan = (b > 190) & (g > 170) & (r < 190)
green = (g > 130) & (r < 120) & (b < 150) & (g > r + 40)
redf = (r > 190) & (g < 120) & (b < 120)
yellow = (r > 215) & (g > 205) & (b < 150)
purple = (b > 180) & (r > 150) & (r < 215) & (g < 185) & (b > r)
for name, m in [("cyan", cyan), ("green", green), ("red", redf), ("yellow", yellow), ("purple", purple)]:
    mm = np.zeros_like(m); mm[150:360, 250:500] = m[150:360, 250:500]
    ys4, xs4 = np.where(mm)
    if len(xs4) == 0: print(f"{name}: EMPTY"); continue
    print(f"{name}: x {xs4.min()}..{xs4.max()}  y {ys4.min()}..{ys4.max()}  n={len(xs4)}")
# each slice's column profile: x positions of colored slices
colsum = {}
for name, m in [("cyan", cyan), ("green", green), ("red", redf), ("yellow", yellow), ("purple", purple)]:
    mm = np.zeros_like(m); mm[150:360, 250:500] = m[150:360, 250:500]
    cs = mm.sum(axis=0)
    xs4 = np.where(cs > 5)[0]
    if len(xs4): colsum[name] = (int(xs4.min()), int(xs4.max()))
print("slice column extents:", colsum)
modal(260, 470, 190, 330, "stack region modal", n=8)

# ============ 5. EQUALS ============
print("=" * 20, "EQUALS")
black = (r < 90) & (g < 90) & (b < 90)
em = np.zeros_like(black); em[220:310, 465:555] = black[220:310, 465:555]
ys5, xs5 = np.where(em)
print(f"= ink: x {xs5.min()}..{xs5.max()}  y {ys5.min()}..{ys5.max()}")
print("= row bands:", bands2(np.where(em.sum(axis=1) > 0)[0] + ys5.min() if len(ys5) else []))

# ============ 6. OUTPUT BOX ============
print("=" * 20, "OUTPUT BOX")
modal(540, 900, 120, 370, "output region modal", n=8)
modal(620, 780, 250, 340, "output front probe")
modal(640, 800, 150, 200, "output top probe")
modal(830, 890, 250, 330, "output side probe")
tan = (r > 190) & (g > 150) & (b > 80) & (b < 200) & (r > b + 40) & (abs(g - 200) < 60)
tm2 = np.zeros_like(tan); tm2[110:390, 530:920] = tan[110:390, 530:920]
ys6, xs6 = np.where(tm2)
print(f"output ALL-tan ink: x {xs6.min()}..{xs6.max()}  y {ys6.min()}..{ys6.max()}")
prof6 = [(int(y), int(tm2[y].sum())) for y in range(ys6.min(), ys6.max()+1, 4)]
print("output tan rowsums:", prof6)

# ============ 7. EQUATION BOX ============
print("=" * 20, "EQUATION BOX")
blk = (r < 130) & (g < 130) & (b < 130)
eb = np.zeros_like(blk); eb[320:480, 300:545] = blk[320:480, 300:545]
ys7, xs7 = np.where(eb)
print(f"eqbox ALL black ink (thr130): x {xs7.min()}..{xs7.max()}  y {ys7.min()}..{ys7.max()}")
# border detection with loose threshold: long runs
print("eqbox horiz runs >=100 (thr 160):")
blk2 = (r < 160) & (g < 160) & (b < 160)
for y in range(320, 485):
    rr = xruns(blk2[y, 300:545], 100)
    if rr: print(f"  y={y}: {[(a+300,bb+300) for a,bb in rr]}")
print("eqbox vert runs >=100 (thr 160):")
for x in range(300, 546):
    cc = np.where(blk2[320:485, x])[0]
    if len(cc) >= 100:
        bb2 = bands2(cc + 320, gap=2)
        for (a, bb) in bb2:
            if bb - a >= 100: print(f"  x={x}: y {a}..{bb}")
# equation text lines inside the box (exclude border): ink bands in x330..510, y340..458
inner = np.zeros_like(blk2); inner[340:458, 330:512] = blk2[340:458, 330:512]
rows7 = np.where(inner.sum(axis=1) > 2)[0] + 340
print("equation ink line bands:", bands2(rows7, gap=2))
for (a, bb) in bands2(rows7, gap=2):
    seg = inner[a:bb+1]
    xsr = np.where(seg.sum(axis=0) > 0)[0] + 330
    print(f"  band y{a}..{bb}: x {xsr.min()}..{xsr.max()}")

# ============ 8. LEGEND (wide window) ============
print("=" * 20, "LEGEND")
blueleg = (b > 110) & (r < 120) & (g < 120) & (b > r + 40)
lb = np.zeros_like(blueleg); lb[360:510, 60:340] = blueleg[360:510, 60:340]
rows8 = np.where(lb.sum(axis=1) > 1)[0] + 360
print("legend blue bands:", bands2(rows8, gap=3))
blk3 = (r < 120) & (g < 120) & (b < 120)
kb = np.zeros_like(blk3); kb[360:510, 60:340] = blk3[360:510, 60:340]
rows8b = np.where(kb.sum(axis=1) > 1)[0] + 360
kbands = bands2(rows8b, gap=3)
print("legend black bands:", kbands)
for (a, bb) in kbands:
    seg = kb[a:bb+1]
    xsr = np.where(seg.sum(axis=0) > 0)[0] + 60
    print(f"  black band y{a}..{bb}: x {xsr.min()}..{xsr.max()}")
for (a, bb) in bands2(rows8, gap=3):
    seg = lb[a:bb+1]
    xsr = np.where(seg.sum(axis=0) > 0)[0] + 60
    print(f"  blue band y{a}..{bb}: x {xsr.min()}..{xsr.max()}")
modal(100, 250, 370, 495, "legend region modal", n=6)
modal(100, 250, 370, 495, "legend BLUE modal", mask=lb, n=6)

# ============ 9. diagram label ink (black) bands across panel ============
print("=" * 20, "DIAGRAM LABELS (black ink, excluding eqbox/legend)")
dl = np.zeros_like(blk3); dl[140:505, 80:888] = blk3[140:505, 80:888]
dl[335:463, 320:521] = False   # eq box
dl[360:510, 60:340] = False    # legend
ys9 = np.where(dl.sum(axis=1) > 0)[0]
lb9 = bands2(ys9, gap=4)
print("black ink bands in panel (y):", lb9)
for (a, bb) in lb9:
    seg = dl[a:bb+1]
    xsr = np.where(seg.sum(axis=0) > 0)[0] + 80
    # x runs to identify separate labels on this band
    colprof = seg.sum(axis=0) > 0
    rr = xruns(colprof, 3)
    print(f"  band y{a}..{bb}: x {xsr.min()}..{xsr.max()} runs={[(aa+80,bbb+80) for aa,bbb in rr][:12]}")
