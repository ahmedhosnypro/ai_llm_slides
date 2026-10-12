#!/usr/bin/env python3
"""PIL measurement pass 4: container borders, pre border, verr text, annotation
border/text lines, pencil ASCII, blue/green curve traces, arrow ASCII."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")
a = np.asarray(IM).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def modal(pix, label, n=4):
    cnt = Counter(map(tuple, pix.reshape(-1, 3)))
    print(f"  {label}:", [(f"#{c:02X}{m:02X}{y:02X}", k) for (c, m, y), k in cnt.most_common(n)])

# ---- 1. pre border: pixel scan around the box (row y=235 and col x=242) ----
print("pre box row y=235, x196..215:", [f"{x}:{tuple(a[235,x])}" for x in range(198, 212)])
print("pre box row y=235, x272..286:", [f"{x}:{tuple(a[235,x])}" for x in range(272, 286)])
print("pre box col x=242, y202..216:", [f"{y}:{tuple(a[y,242])}" for y in range(203, 215)])
print("pre box col x=242, y255..267:", [f"{y}:{tuple(a[y,242])}" for y in range(255, 267)])

# ---- 2. verr box: outer bbox via red border stroke; red text ink ----
red = (r>120)&(g<100)&(b<100)
sub = np.zeros_like(red); sub[165:310, 745:800] = red[165:310, 745:800]
ys, xs = np.where(sub)
print(f"verr red ink (border+text): x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
# text = interior only
inner = np.zeros_like(red); inner[178:295, 770:792] = red[178:295, 770:792]
ys, xs = np.where(inner)
print(f"verr red TEXT ink: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
modal(a[inner], "verr text/border color", 4)
# border stroke: columns 750..756 at row 235
print("verr row y=235, x746..760:", [f"{x}:{tuple(a[235,x])}" for x in range(746, 760)])
print("verr col x=771, y168..180:", [f"{y}:{tuple(a[y,771])}" for y in range(168, 180)])
print("verr col x=771, y292..304:", [f"{y}:{tuple(a[y,771])}" for y in range(292, 304)])

# ---- 3. annotation box border strokes ----
print("annot row y=350: x256..268:", [f"{x}:{tuple(a[350,x])}" for x in range(256, 268)])
print("annot row y=350: x734..746:", [f"{x}:{tuple(a[350,x])}" for x in range(734, 746)])
print("annot col x=500: y320..332:", [f"{y}:{tuple(a[y,500])}" for y in range(320, 332)])
print("annot col x=500: y372..384:", [f"{y}:{tuple(a[y,500])}" for y in range(372, 384)])
# text line structure: row profile of dark-ish ink in box
sub = a[325:385, 263:740]
dk = (sub[:,:,0] < 170) & (sub[:,:,1] < 190) & (sub[:,:,2] < 170)
rowprof = dk.sum(axis=1)
print("annot text row profile (y325+i:count):", {325+i: int(c) for i, c in enumerate(rowprof) if c > 0})

# ---- 4. pencil ASCII ----
sub = a[200:235, 243:285]
dk = (sub[:,:,0] + sub[:,:,1] + sub[:,:,2]) < 480
print("pencil ASCII (x243..284, y200..234):")
for i, row in enumerate(dk):
    print(f"{200+i:3d} " + "".join("#" if v else "." for v in row))

# ---- 5. input box border + fill scan ----
print("input row y=235: x76..90:", [f"{x}:{tuple(a[235,x])}" for x in range(76, 90)])
print("input col x=118: y206..220:", [f"{y}:{tuple(a[y,118])}" for y in range(206, 220)])

# ---- 6. predicted border scan ----
print("pred row y=235: x654..668:", [f"{x}:{tuple(a[235,x])}" for x in range(654, 668)])
print("pred row y=235: x728..742:", [f"{x}:{tuple(a[235,x])}" for x in range(728, 742)])

# ---- 7. blue solid curve trace (per-x mean y) ----
blue = (b - (r+g)//2 > 22) & (b > 90)
bm = np.zeros_like(blue); bm[120:215, 100:372] = blue[120:215, 100:372]
print("blue SOLID trace (x: ymean[ymin..ymax] n):")
for x in range(100, 372, 12):
    ys = np.where(bm[:, x])[0]
    if len(ys):
        print(f"  x{x}: y{ys.mean():.0f} [{ys.min()}..{ys.max()}] n={len(ys)}")
# head zone detail
ys, xs = np.where(bm[:, 105:135])
print(f"blue head zone x105..135: y{ys.min()}..{ys.max()}")

# ---- 8. dashed blue trace (segment centroids) ----
bm2 = np.zeros_like(blue); bm2[120:215, 460:860] = blue[120:215, 460:860]
from scipy import ndimage
lab, nlab = ndimage.label(bm2, structure=np.ones((3,3)))
segs = []
for i in range(1, nlab+1):
    ys, xs = np.where(lab == i)
    if len(ys) < 6: continue
    segs.append((xs.mean(), ys.mean(), len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
segs.sort()
print("blue DASHED segments (xc, yc, n, bbox):")
for xc, yc, n, x0, x1, y0, y1 in segs:
    print(f"  ({xc:.0f},{yc:.0f}) n={n} x{x0:.0f}..{x1:.0f} y{y0:.0f}..{y1:.0f}")

# ---- 9. green curves: per-column trace in 4 head zones + bundle ----
green = (g - (r+b)//2 > 18) & (g > 80)
gm = np.zeros_like(green); gm[255:330, 150:800] = green[255:330, 150:800]
print("green trace (x: ymin..ymax, n) every 12px:")
for x in range(150, 800, 12):
    ys = np.where(gm[:, x])[0]
    if len(ys):
        print(f"  x{x}: y{ys.min()}..{ys.max()} n={len(ys)}")

# ---- 10. ASCII: arrow a1 + container left border zone ----
sub = a[192:280, 150:215]
redm = (sub[:,:,0]>130)&(sub[:,:,1]<100)&(sub[:,:,2]<100)
print("ASCII red x150..214, y192..279 (a1 + container left):")
for i, row in enumerate(redm):
    line = "".join("#" if v else "." for v in row)
    if "#" in line:
        print(f"{192+i:3d} {line}")

# ---- 11. container top/bottom dash rows (proper windowing) ----
red2 = (r>130)&(g<100)&(b<100)
for row in (195, 196, 197, 271, 272, 273):
    xs = np.where(red2[row, 150:700])[0] + 150
    if len(xs):
        runs = []
        s = p = None
        for x in xs:
            if s is None: s = p = x
            elif x == p+1: p = x
            else: runs.append((s, p)); s = p = x
        runs.append((s, p))
        print(f"container row {row}: {len(runs)} runs, extent x{xs.min()}..{xs.max()}, first8 {runs[:8]}")
# left/right border columns
for col in (189, 190, 191, 192, 193, 653, 655, 657, 659):
    ys = np.where(red2[190:280, col])[0] + 190
    if len(ys) > 5:
        print(f"container col {col}: n={len(ys)} y{ys.min()}..{ys.max()}")
