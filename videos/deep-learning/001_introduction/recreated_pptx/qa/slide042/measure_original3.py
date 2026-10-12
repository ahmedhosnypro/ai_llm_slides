#!/usr/bin/env python3
"""Pass 3 — polygon geometry per face, equals bars, equation lines, legend extents,
font solving. All bands computed window-relative then offset ONCE."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_042.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def modal(x0, x1, y0, y1, label, mask=None, n=5):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    if mask is not None:
        reg = IM[y0:y1+1, x0:x1+1][mask[y0:y1+1, x0:x1+1]]
        if len(reg) == 0: print(f"{label}: mask empty"); return
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:n]
    print(f"{label}: " + ", ".join('#%02X%02X%02X(%d)' % (*vals[i], counts[i]) for i in order))

def bands(rows, gap=3):
    if len(rows) == 0: return []
    out = []; s = p = rows[0]
    for c in rows[1:]:
        if c - p <= gap: p = c
        else: out.append((int(s), int(p))); s = p = c
    out.append((int(s), int(p)))
    return out

def rowext(mask, y, x0=0):
    xs = np.where(mask[y])[0]
    return (int(xs.min()) + x0, int(xs.max()) + x0) if len(xs) else None

# ============ SLAB: tile color map ============
print("=" * 20, "SLAB tile map (modal per 24x24 tile, x60..344 y180..350)")
for ty in range(180, 350, 24):
    row = []
    for tx in range(60, 344, 24):
        tile = IM[ty:ty+24, tx:tx+24].reshape(-1, 3)
        vals, counts = np.unique(tile, axis=0, return_counts=True)
        v = vals[np.argmax(counts)]
        row.append('#%02X%02X%02X' % (*v,))
    print(f"y{ty:3d}: " + " ".join(row))

# per-face masks near measured modals
front = (abs(r - 175) < 30) & (abs(g - 103) < 30) & (abs(b - 18) < 35)   # AF6712
print("\nslab FRONT (#AF6712) rows:")
fm = np.zeros((H, W), bool); fm[130:400, 40:350] = front[130:400, 40:350]
ys, xs = np.where(fm)
print(f"  front ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
for y in range(ys.min(), ys.max() + 1, 10):
    e = rowext(fm, y)
    if e: print(f"  y={y}: x {e[0]}..{e[1]}")

# top face: lighter orange
topf = (r > 200) & (g > 120) & (g < 190) & (b < 120) & (r > b + 100)
tm_ = np.zeros((H, W), bool); tm_[130:400, 40:350] = topf[130:400, 40:350]
ys, xs = np.where(tm_)
if len(xs): 
    print(f"slab TOP lighter-orange ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
    for y in range(ys.min(), ys.max() + 1, 6):
        e = rowext(tm_, y)
        if e: print(f"  y={y}: x {e[0]}..{e[1]}")
else: print("slab TOP: none")
# side face: darker
sidef = (r > 120) & (r < 165) & (g > 60) & (g < 100) & (b < 60)
sm_ = np.zeros((H, W), bool); sm_[130:400, 40:350] = sidef[130:400, 40:350]
ys, xs = np.where(sm_)
if len(xs):
    print(f"slab SIDE darker ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
    for y in range(ys.min(), ys.max() + 1, 6):
        e = rowext(sm_, y)
        if e: print(f"  y={y}: x {e[0]}..{e[1]}")
else: print("slab SIDE: none")
modal(60, 344, 180, 350, "slab all modal", n=8)

# ============ FILTER STACK: per-slice geometry ============
print("=" * 20, "FILTER SLICES")
slices = {
    "cyan":   (abs(r - 143) < 45, abs(g - 212) < 40, abs(b - 232) < 40),
    "green":  ((g > 120) & (r < 110) & (b < 130), None, None),
    "red":    ((r > 200) & (g < 110) & (b < 110), None, None),
    "yellow": ((r > 215) & (g > 200) & (b < 150), None, None),
    "purple": ((b > 185) & (r > 145) & (r < 215) & (g < 185) & (b > r), None, None),
}
masks = {}
masks["cyan"] = (abs(r - 143) < 45) & (abs(g - 212) < 40) & (abs(b - 232) < 40)
masks["green"] = (g > 120) & (r < 110) & (b < 130) & (g > r + 40)
masks["red"] = (r > 200) & (g < 110) & (b < 110)
masks["yellow"] = (r > 215) & (g > 200) & (b < 150)
masks["purple"] = (b > 185) & (r > 145) & (r < 215) & (g < 185) & (b > r)
for name, m in masks.items():
    mm = np.zeros((H, W), bool); mm[230:320, 280:480] = m[230:320, 280:480]
    ys, xs = np.where(mm)
    if len(xs) < 10: print(f"{name}: sparse n={len(xs)}"); continue
    print(f"{name}: bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
    for y in [ys.min()+2, (ys.min()+ys.max())//2, ys.max()-2]:
        e = rowext(mm, y)
        if e: print(f"   y={y}: x {e[0]}..{e[1]}")
    reg = IM[230:320, 280:480][m[230:320, 280:480]]
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    v = vals[np.argmax(counts)]
    print(f"   modal: #%02X%02X%02X (%d)" % (*v, counts.max()))

# ============ OUTPUT BOX: tile map + face masks ============
print("=" * 20, "OUTPUT BOX tile map (x560..900 y130..360)")
for ty in range(130, 360, 24):
    row = []
    for tx in range(560, 900, 24):
        tile = IM[ty:ty+24, tx:tx+24].reshape(-1, 3)
        vals, counts = np.unique(tile, axis=0, return_counts=True)
        v = vals[np.argmax(counts)]
        row.append('#%02X%02X%02X' % (*v,))
    print(f"y{ty:3d}: " + " ".join(row))
ofront = (abs(r - 239) < 12) & (abs(g - 206) < 14) & (abs(b - 163) < 16)   # EFCEA3
of = np.zeros((H, W), bool); of[120:380, 540:920] = ofront[120:380, 540:920]
ys, xs = np.where(of)
print(f"output FRONT ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
for y in range(ys.min(), ys.max() + 1, 12):
    e = rowext(of, y)
    if e: print(f"  y={y}: x {e[0]}..{e[1]}")
otop = (r > 236) & (g > 205) & (b > 165) & (b < 200)
ot = np.zeros((H, W), bool); ot[120:380, 540:920] = otop[120:380, 540:920]
ys, xs = np.where(ot)
if len(xs):
    print(f"output TOP ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
    for y in range(ys.min(), ys.max() + 1, 6):
        e = rowext(ot, y)
        if e: print(f"  y={y}: x {e[0]}..{e[1]}")
oside = (abs(r - 224) < 14) & (abs(g - 195) < 14) & (abs(b - 161) < 14)   # E0C3A1
osd = np.zeros((H, W), bool); osd[120:380, 540:920] = oside[120:380, 540:920]
ys, xs = np.where(osd)
if len(xs):
    print(f"output SIDE ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
    for y in range(ys.min(), ys.max() + 1, 6):
        e = rowext(osd, y)
        if e: print(f"  y={y}: x {e[0]}..{e[1]}")

# ============ EQUALS bars ============
print("=" * 20, "EQUALS")
blk = (r < 110) & (g < 110) & (b < 110)
em = np.zeros((H, W), bool); em[250:300, 480:570] = blk[250:300, 480:570]
ys, xs = np.where(em)
print(f"= ink: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}")
for y in range(ys.min(), ys.max() + 1):
    e = rowext(em, y)
    if e: print(f"  y={y}: x {e[0]}..{e[1]} n={int(em[y].sum())}")

# ============ EQUATION BOX ============
print("=" * 20, "EQUATION LINES")
blk2 = (r < 140) & (g < 140) & (b < 140)
# inside border x318..520, y335..461; exclude border by 3px inset
inner = np.zeros((H, W), bool)
inner[338:459, 321:518] = blk2[338:459, 321:518]
rows = np.where(inner.sum(axis=1) > 2)[0]
print("eq line bands:", [(a, bb) for (a, bb) in bands(rows, gap=3)])
for (a, bb) in bands(rows, gap=3):
    seg = inner[a:bb+1, :]
    xsr = np.where(seg.sum(axis=0) > 0)[0]
    print(f"  band y{a}..{bb} (h{bb-a+1}): x {xsr.min()}..{xsr.max()}")
    # per-row extents to find fraction bar
    for y in range(a, bb + 1):
        e = rowext(inner, y)
        n = int(inner[y].sum())
        if e: print(f"    y={y}: x {e[0]}..{e[1]} n={n}")

# ============ LEGEND ============
print("=" * 20, "LEGEND")
blueleg = (b > 110) & (r < 130) & (g < 130) & (b > r + 40)
lb = np.zeros((H, W), bool); lb[360:510, 60:340] = blueleg[360:510, 60:340]
rows = np.where(lb.sum(axis=1) > 1)[0]
print("legend blue bands:", bands(rows, gap=3))
blk3 = (r < 130) & (g < 130) & (b < 130)
kb = np.zeros((H, W), bool); kb[360:510, 60:340] = blk3[360:510, 60:340]
rowsb = np.where(kb.sum(axis=1) > 1)[0]
kbands = bands(rowsb, gap=3)
print("legend black bands:", kbands)
for (a, bb) in bands(rows, gap=3):
    seg = lb[a:bb+1, :]
    xsr = np.where(seg.sum(axis=0) > 0)[0]
    if len(xsr): print(f"  blue  y{a}..{bb}: x {xsr.min()+0}..{xsr.max()}")
for (a, bb) in kbands:
    seg = kb[a:bb+1, :]
    xsr = np.where(seg.sum(axis=0) > 0)[0]
    if len(xsr): print(f"  black y{a}..{bb}: x {xsr.min()+0}..{xsr.max()}")
# legend blue color with dilated mask
dil = lb.copy()
for dy in (-1, 0, 1):
    for dx in (-1, 0, 1):
        dil |= np.roll(np.roll(lb, dy, 0), dx, 1)
modal(60, 340, 360, 510, "legend blue dilated modal", mask=dil, n=6)
modal(60, 340, 360, 510, "legend black modal", mask=kb & ~lb, n=4)

# ============ LABELS black ink bands in panel ============
print("=" * 20, "DIAGRAM LABELS")
dl = np.zeros((H, W), bool)
dl[140:505, 80:888] = blk3[140:505, 80:888]
dl[334:463, 315:524] = False  # eqbox
dl[360:510, 60:340] = False   # legend
ys = np.where(dl.sum(axis=1) > 0)[0]
print("label bands:", bands(ys, gap=4))
for (a, bb) in bands(ys, gap=4):
    seg = dl[a:bb+1, :]
    colprof = seg.sum(axis=0) > 0
    xsr = np.where(colprof)[0]
    runs = []
    if len(xsr):
        s = p = xsr[0]
        for c in xsr[1:]:
            if c - p <= 6: p = c
            else: runs.append((int(s), int(p))); s = p = c
        runs.append((int(s), int(p)))
    print(f"  y{a}..{bb}: runs(x)={runs}")
