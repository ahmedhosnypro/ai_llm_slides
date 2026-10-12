# stage 2: red ink components, gray canvas modal, white panel bbox, colored box components
from PIL import Image
import numpy as np
from collections import Counter
from scipy import ndimage

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_009.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[...,0], a[...,1], a[...,2]

# ---- red ink (title, arrows, panel border?) ----
red = (r.astype(int) - np.maximum(g, b) > 55) & (r > 100)
lab, n = ndimage.label(red)
print("-- red components > 30 px --")
comps = []
for i in range(1, n+1):
    m = lab == i
    s = m.sum()
    if s < 30: continue
    ys, xs = np.nonzero(m)
    comps.append((s, xs.min(), ys.min(), xs.max(), ys.max()))
comps.sort(reverse=True)
for s, x0, y0, x1, y1 in comps[:40]:
    print(f"  n={s:6d}  x {x0}..{x1}  y {y0}..{y1}  (w={x1-x0+1}, h={y1-y0+1})")

# ---- gray canvas modal color (outside white panel) ----
samp = a[20:40, 100:900].reshape(-1,3)
print("\ngray canvas modal (y20..40):", Counter(map(tuple, samp)).most_common(4))
samp2 = a[470:510, 100:200].reshape(-1,3)
print("gray canvas modal (y470..510 left):", Counter(map(tuple, samp2)).most_common(4))

# ---- white panel bbox ----
white = (r>245)&(g>245)&(b>245)
ys, xs = np.nonzero(white)
print("\nwhite(>245) bbox:", xs.min(), ys.min(), xs.max(), ys.max())
rows = white.sum(axis=1)
first = np.nonzero(rows>500)[0]; last = np.nonzero(rows>500)[0]
print("white rows>500:", first.min(), "..", last.max())
cols = white.sum(axis=0)
strongc = np.nonzero(cols>200)[0]
print("white cols>200:", strongc.min(), "..", strongc.max())

# ---- saturation: colorful components (box fills) ----
mx = a.max(axis=2); mn = a.min(axis=2)
sat = mx - mn
colorful = sat > 25
lab2, n2 = ndimage.label(colorful)
print("\n-- colorful (sat>25) components > 200 px --")
comps2 = []
for i in range(1, n2+1):
    m = lab2 == i
    s = m.sum()
    if s < 200: continue
    ys, xs = np.nonzero(m)
    core = a[m]
    modal = Counter(map(tuple, (core//4*4))).most_common(3)
    comps2.append((s, xs.min(), ys.min(), xs.max(), ys.max(), modal))
comps2.sort(reverse=True)
for s, x0, y0, x1, y1, modal in comps2[:40]:
    print(f"  n={s:6d}  x {x0}..{x1}  y {y0}..{y1} (w={x1-x0+1},h={y1-y0+1})  modal {modal}")

# ---- gray D9-ish label boxes: pixels near gray, sat<12, 190<v<245, inside panel ----
grayish = (sat <= 14) & (mx > 185) & (mx < 242)
lab3, n3 = ndimage.label(grayish)
print("\n-- grayish components 300..4000 px --")
for i in range(1, n3+1):
    m = lab3 == i
    s = m.sum()
    if not (300 <= s <= 4000): continue
    ys, xs = np.nonzero(m)
    h_, w_ = ys.max()-ys.min()+1, xs.max()-xs.min()+1
    if h_ < 10 or w_ < 40: continue
    core = a[m]
    modal = Counter(map(tuple, (core//4*4))).most_common(2)
    print(f"  n={s:6d}  x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()} (w={w_},h={h_}) modal {modal}")

# ---- bottom black bar ----
dark = (mx < 90)
bb = dark[515:540, :]
print("\n-- dark rows 515..539 counts:", [(515+i, int(bb[i].sum())) for i in range(0, 25, 2)])
ys, xs = np.nonzero(dark & (np.arange(H)[:,None] >= 515))
print("bottom dark bbox:", xs.min(), ys.min(), xs.max(), ys.max())
