#!/usr/bin/env python3
"""Forensics pass 2c — slide_025.jpg. Pink boxes via sampled fill, dotted line, arrowheads.
Also: title brightest-core color; small-text column-profile helper demo."""
import numpy as np
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
im = Image.open(ORIG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

print("== raw samples inside candidate pink boxes ==")
for (x, y) in [(70, 100), (90, 100), (110, 110), (65, 118), (100, 96), (100, 124),
               (625, 100), (645, 110), (660, 118), (620, 96), (640, 124), (680, 110)]:
    print(f"  ({x:3d},{y:3d}) {tuple(int(v) for v in a[y, x])}")

# build fill mask from sampled family: R>225, G 120..200, B 170..230
pinkc = (R > 225) & (G > 115) & (G < 205) & (B > 165) & (B < 235)
print(f"\n== pink fill mask total {int(pinkc.sum())} ==")
sub = pinkc[85:135, :]
rows = sub.sum(axis=1)
for i, n in enumerate(rows):
    if n > 2:
        print(f"  y{85+i}: {int(n)}")
cp = pinkc[85:135, :].sum(axis=0)
xs = np.where(cp > 1)[0]
runs = []
s = xs[0]; p = xs[0]
for x in xs[1:]:
    if x - p > 8:
        runs.append((s, p)); s = x
    p = x
runs.append((s, p))
print("  x runs:", [(int(u), int(v)) for u, v in runs])

def box_metrics(x0b, x1b, label):
    print(f"\n  -- {label} --")
    reg = pinkc[85:135, x0b:x1b + 1]
    rr = reg.sum(axis=1); rys = np.where(rr > 2)[0]
    cc = reg.sum(axis=0); cxs = np.where(cc > 1)[0]
    print(f"     fill y {85+rys.min()}..{85+rys.max()} (h {rys.max()-rys.min()+1}), x {x0b+cxs.min()}..{x0b+cxs.max()} (w {cxs.max()-cxs.min()+1})")
    fill = a[85:135, x0b:x1b + 1][reg]
    fq = fill // 8 * 8
    vals, counts = np.unique(fq.reshape(-1, 3), axis=0, return_counts=True)
    t = vals[np.argsort(-counts)][:2]
    print(f"     fill modal: {[list(map(int, v)) for v in t]} counts {list(map(int, np.sort(counts)[::-1][:2]))}")
    # dark border ring: darkest 20% pixels on the fill boundary rows/cols
    dark = (R < 120) & (G < 120) & (B < 120)
    d = dark[85:135, x0b:x1b + 1]
    ys2, xs2 = np.where(d)
    if len(ys2):
        print(f"     dark ink (text+border) x {x0b+xs2.min()}..{x0b+xs2.max()}, y {85+ys2.min()}..{85+ys2.max()}")
        # border columns = dark cols adjacent to fill edges
        print(f"     dark row profile (first/last 4 rows): {[(int(85+ys2[i]),) for i in [0,1,2,3,-4,-3,-2,-1]]}")

box_metrics(50, 140, "Input Samples box")
box_metrics(600, 690, "Sample Label box")

# ---- text ink inside boxes (column profiles -> line structure) ----
print("\n== Input Samples text ink rows (dark<130, x60..135) ==")
dark = (R < 130) & (G < 130) & (B < 130)
seg = dark[88:130, 60:135]
rp = seg.sum(axis=1)
print("  rows:", {85 + i: int(n) for i, n in enumerate(rp) if n > 0})
print("== Sample Label text ink rows (dark<130, x610..680) ==")
seg = dark[88:130, 610:680]
rp = seg.sum(axis=1)
print("  rows:", {85 + i: int(n) for i, n in enumerate(rp) if n > 0})

# ---- dotted magenta line ----
print("\n== dotted line: magenta strict (R>150, G<80, B>150) ==")
mag = (R > 150) & (G < 80) & (B > 150)
seg = mag[95:130, 140:600]
rp = seg.sum(axis=1)
line_rows = {95 + i: int(n) for i, n in enumerate(rp) if n > 0}
print("  rows:", line_rows)
if line_rows:
    rowy = max(line_rows, key=line_rows.get)
    xs = np.where(mag[rowy, 140:600])[0] + 140
    diffs = np.diff(xs)
    uh, uc = np.unique(diffs, return_counts=True)
    print(f"  peak row y{rowy}: {len(xs)} dots x{xs.min()}..{xs.max()}, gaps {dict(zip(map(int,uh),map(int,uc)))}")
# arrowhead zones
for (xa, xb, tag) in [(125, 145, "left of Input Samples right edge"), (590, 615, "right end at Sample Label")]:
    ys2, xs2 = np.where(mag[95:130, xa:xb])
    if len(ys2):
        print(f"  magenta {tag}: {len(ys2)} px x {xa+xs2.min()}..{xa+xs2.max()} y {95+ys2.min()}..{95+ys2.max()}")
        # show the x-histogram to see a wedge shape
        cols = {}
        for xx in xs2:
            cols[int(xa + xx)] = cols.get(int(xa + xx), 0) + 1
        print("    per-x counts:", dict(sorted(cols.items())))
    else:
        print(f"  magenta {tag}: none")

# ---- line left anchor: does the dotted line start at the Input box or pass THROUGH? ----
print("\n== magenta in x130..160 y100..120 (between box and first dots) ==")
ys2, xs2 = np.where(mag[100:121, 130:161])
print(f"  {len(ys2)} px" + (f", x {130+xs2.min()}..{130+xs2.max()}" if len(ys2) else ""))

# ---- title brightest-core color ----
redt = (R > 130) & (G < 110) & (B < 110) & (R > G + 50)
tp = a[68:90, 328:644][redt[68:90, 328:644]]
bright = tp[tp.sum(axis=1).argsort()[-len(tp) // 4:]]
print(f"\n== title core color: top-25% brightest median rgb {tuple(int(v) for v in np.median(bright, axis=0))} ==")
