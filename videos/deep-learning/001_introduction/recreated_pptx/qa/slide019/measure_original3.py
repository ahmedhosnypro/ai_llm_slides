#!/usr/bin/env python3
"""PIL measurement pass 3 for slide_019.jpg: connected-component box geometry,
border strokes, curve traces, annotation box, pencil icon."""
from PIL import Image
import numpy as np
from collections import Counter
from scipy import ndimage

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_019.jpg").convert("RGB")
a = np.asarray(IM).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def modal(pix, label, n=3):
    cnt = Counter(map(tuple, pix.reshape(-1, 3)))
    print(f"  {label}:", [(f"#{c:02X}{m:02X}{y:02X}", k) for (c, m, y), k in cnt.most_common(n)])

def comp_bbox(mask, label, min_px=60):
    lab, nlab = ndimage.label(mask)
    comps = []
    for i in range(1, nlab + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px:
            continue
        comps.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
    comps.sort(reverse=True)
    for k, (npx, x0, x1, y0, y1) in enumerate(comps[:3]):
        print(f"{label} comp{k}: n={npx} x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) center=({(x0+x1)/2:.1f},{(y0+y1)/2:.1f})")
    return comps

# ---- fills (generous region: inside panel, y95..330) ----
fills = {
    "tan (input/samples)": (abs(r-218)<14) & (abs(g-192)<14) & (abs(b-162)<16),
    "paleyellow (pre)":    (abs(r-250)<8) & (abs(g-254)<6) & (abs(b-219)<10),
    "lightcyan (extr)":    (abs(r-228)<10) & (abs(g-254)<6) & (abs(b-251)<8),
    "palegreen (sel)":     (abs(r-244)<10) & (abs(g-254)<6) & (abs(b-236)<10),
    "darkred (classif)":   (r>120)&(r<190)&(g<40)&(b<40),
    "palemagenta (pred)":  (r>245)&(abs(g-215)<20)&(b>245),
    "pink (verr)":         (abs(r-245)<12)&(abs(g-181)<15)&(abs(b-184)<15),
}
for name, m in fills.items():
    mm = np.zeros_like(m); mm[95:335, 60:920] = m[95:335, 60:920]
    comp_bbox(mm, name)

# ---- border strokes: sample 1-2px ring OUTSIDE each fill via dilate-xor ----
def border_of(fillmask, label):
    mm = np.zeros_like(fillmask); mm[95:335, 60:920] = fillmask[95:335, 60:920]
    lab, nlab = ndimage.label(mm)
    if nlab == 0: return
    sizes = ndimage.sum(mm, lab, range(1, nlab+1))
    big = (np.argmax(sizes) + 1)
    comp = lab == big
    dil = ndimage.binary_dilation(comp, iterations=3) & ~ndimage.binary_dilation(comp, iterations=1)
    ys, xs = np.where(dil)
    pix = a[ys, xs]
    # drop white/panel-gray/chrome pixels
    keep = ~((pix[:,0]>235)&(pix[:,1]>235)&(pix[:,2]>235)) & ~((abs(pix[:,0]-233)<14)&(abs(pix[:,1]-233)<14))
    modal(pix[keep], f"{label} border", 4)

for name, m in fills.items():
    border_of(m, name)

# ---- ellipse: exact via fill + ring ----
peach = (abs(r-246)<12) & (abs(g-222)<14) & (abs(b-196)<16)
mm = np.zeros_like(peach); mm[102:175, 350:500] = peach[102:175, 350:500]
comp_bbox(mm, "ellipse fill")
ys, xs = np.where(mm)
ex0, ex1, ey0, ey1 = xs.min(), xs.max(), ys.min(), ys.max()
ring = ndimage.binary_dilation(mm, iterations=2) & ~mm
pix = a[ring]
keep = ~((pix[:,0]>235)&(pix[:,1]>235)&(pix[:,2]>235))
modal(pix[keep], "ellipse border ring", 4)

# ---- dashed red container: bbox + dash metrics on top border ----
red = (r>130)&(g<95)&(b<95)
rm = np.zeros_like(red); rm[190:280, 180:670] = red[190:280, 180:670]
# remove classification box (solid): its bbox from darkred comp; find via largest solid red comp
lab, nlab = ndimage.label(rm)
sizes = ndimage.sum(rm, lab, range(1, nlab+1))
order = np.argsort(sizes)[::-1]
print("red comps in container zone (top 6):")
for oi in order[:6]:
    i = oi + 1
    ys, xs = np.where(lab == i)
    print(f"  n={len(ys)} x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
# container top dash row: row with dashes spanning x190..660 excluding classification x540..640
row_counts = rm[:, 190:540].sum(axis=1)
top_row = int(np.argmax(row_counts[:20])) + 190
dash_row = rm[top_row, 180:670]
xs = np.where(dash_row)[0] + 180
# runs
runs = []
s = p = None
for x in xs:
    if s is None: s = p = x
    elif x == p+1: p = x
    else: runs.append((s,p)); s = p = x
if s is not None: runs.append((s,p))
print(f"container top border row {top_row}: {len(runs)} dashes, sample runs {runs[:8]}")
lens = [e-s+1 for s,e in runs]
gaps = [runs[i+1][0]-runs[i][1]-1 for i in range(len(runs)-1)]
print(f"  dash lens median {sorted(lens)[len(lens)//2] if lens else 0}, gaps median {sorted(gaps)[len(gaps)//2] if gaps else 0}")

# ---- blue curves: full trace ----
blue = (b - (r+g)//2 > 22) & (b > 90)
bm = np.zeros_like(blue); bm[95:230, 60:920] = blue[95:230, 60:920]
lab, nlab = ndimage.label(bm, structure=np.ones((3,3)))
print("blue comps (top 8):")
comps = []
for i in range(1, nlab+1):
    ys, xs = np.where(lab == i)
    if len(ys) < 8: continue
    comps.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
comps.sort(reverse=True)
for npx, x0, x1, y0, y1 in comps[:8]:
    print(f"  n={npx} x{x0}..{x1} y{y0}..{y1}")
modal(a[bm], "blue ink", 4)

# ---- green dashed arrows ----
green = (g - (r+b)//2 > 18) & (g > 80)
gm = np.zeros_like(green); gm[258:340, 150:800] = green[258:340, 150:800]
ys, xs = np.where(gm)
print(f"green ink bbox: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(ys)}")
modal(a[gm], "green ink", 4)
# arrowhead positions: column density peaks near box bottoms
# heads point UP into bottoms of pre(195..290), extr(315..410), sel(430..525), classif(540..640)
for nm, x0, x1 in [("pre", 195, 290), ("extr", 315, 410), ("sel", 430, 525), ("classif", 540, 640)]:
    sub = gm[258:340, x0:x1+1]
    ys2, xs2 = np.where(sub)
    if len(ys2):
        print(f"  green under {nm}: x{xs2.min()+x0}..{xs2.max()+x0} y{ys2.min()+258}..{ys2.max()+258} n={len(ys2)}")

# ---- annotation box ----
sub_y0, sub_y1, sub_x0, sub_x1 = 325, 415, 150, 850
sub = a[sub_y0:sub_y1, sub_x0:sub_x1]
rr, gg, bb = sub[:,:,0], sub[:,:,1], sub[:,:,2]
palegreen = (gg > rr+8) & (gg > bb+8) & (gg > 225) & (rr > 215) & (bb > 200)
ys, xs = np.where(palegreen)
print(f"annotation fill bbox: x{xs.min()+sub_x0}..{xs.max()+sub_x0} y{ys.min()+sub_y0}..{ys.max()+sub_y0}")
modal(sub[palegreen], "annotation fill", 3)
# border: ring around fill bbox
fx0, fx1, fy0, fy1 = xs.min()+sub_x0, xs.max()+sub_x0, ys.min()+sub_y0, ys.max()+sub_y0
ringband = a[fy0-4:fy1+5, fx0-4:fx1+5]
ry, rx = np.where(~((ringband[:,:,0]>235)&(ringband[:,:,1]>235)&(ringband[:,:,2]>235)))
modal(ringband[ry, rx], "annotation border-ish", 5)
# text ink
dk = (rr < 130) & (gg < 150) & (bb < 130)
ys, xs = np.where(dk)
print(f"annotation text ink: x{xs.min()+sub_x0}..{xs.max()+sub_x0} y{ys.min()+sub_y0}..{ys.max()+sub_y0}")
modal(sub[dk], "annotation text", 3)

# ---- pencil icon ----
sub = a[198:232, 245:295]
rr, gg, bb = sub[:,:,0], sub[:,:,1], sub[:,:,2]
dk = (rr < 140) & (gg < 140) & (bb < 140)
ys, xs = np.where(dk)
if len(ys):
    print(f"pencil ink: x{xs.min()+245}..{xs.max()+245} y{ys.min()+198}..{ys.max()+198} n={len(ys)}")
    modal(sub[dk], "pencil ink", 3)

# ---- red chain arrows between boxes (y ~225..250) ----
redm = (r>140)&(g<95)&(b<95)
am = np.zeros_like(redm); am[215:260, 60:920] = redm[215:260, 60:920]
# exclude classification solid box + borders: check gaps
lab, nlab = ndimage.label(am)
print("red arrow comps in chain band (top 10):")
comps = []
for i in range(1, nlab+1):
    ys, xs = np.where(lab == i)
    if len(ys) < 15: continue
    comps.append((len(ys), xs.min(), xs.max(), ys.min(), ys.max()))
comps.sort(reverse=True)
for npx, x0, x1, y0, y1 in comps[:10]:
    print(f"  n={npx} x{x0}..{x1} y{y0}..{y1}")
