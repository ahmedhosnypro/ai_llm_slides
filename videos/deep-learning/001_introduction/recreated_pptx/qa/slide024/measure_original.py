#!/usr/bin/env python3
"""Measure slide_024.jpg (960x540, 1px=1pt) — Neural Network Model.
Banks all measured geometry for the build."""
import json
import numpy as np
from PIL import Image
from scipy import ndimage

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_024.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
print(f"size {W}x{H}")

def bbox_of(mask, label):
    ys, xs = np.where(mask)
    if not len(ys):
        return None
    return dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()),
                n=int(len(ys)))

def components(mask, min_px=6):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_px:
            continue
        out.append(dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()),
                        n=int(len(ys)), cx=float((xs.min()+xs.max())/2), cy=float((ys.min()+ys.max())/2)))
    return out

def show(name, items, sort="cy"):
    print(f"\n== {name}: {len(items)} components")
    for c in sorted(items, key=lambda c: (c["cy"], c["cx"]) if sort == "cy" else (c["cx"], c["cy"])):
        print(f"  x{c['x0']}..{c['x1']} y{c['y0']}..{c['y1']} w={c['x1']-c['x0']+1} h={c['y1']-c['y0']+1} n={c['n']} c=({c['cx']:.1f},{c['cy']:.1f})")

def sample(x, y, r=2):
    win = A[max(0,y-r):y+r+1, max(0,x-r):x+r+1].reshape(-1, 3)
    med = np.median(win, axis=0).astype(int)
    return tuple(med)

print("\n== chrome samples")
print("canvas(20,300):", sample(20, 300), " (940,300):", sample(940, 300))
print("panel-gray(200,150):", sample(200, 150), "(500,120):", sample(500, 120))
print("top-border(480,44..47):", [sample(480, yy, 0) for yy in range(42, 50)])
print("left-border(x40..46,300):", [sample(xx, 300, 0) for xx in range(38, 48)])
print("bottom rows y530..539 @x480:", [sample(480, yy, 0) for yy in range(530, 540)])
print("badge region none? yellowish scan top-right:")
yel = (r > 200) & (g > 200) & (b < 190)
print("  yellow px in y<140:", int(yel[:140, :].sum()))

# beige panel
beige = (abs(r - 214) < 22) & (abs(g - 198) < 22) & (abs(b - 182) < 24)
bb = bbox_of(beige[:, :], "beige")
print("\n== beige panel bbox:", bb)
# column profile at row 300 to find left/right edges precisely
row = beige[300]
xs = np.where(row)[0]
print("beige row300 x:", xs.min(), xs.max())
col = beige[:, 700]
ys = np.where(col)[0]
print("beige col700 y:", ys.min(), ys.max())
col = beige[:, 300]
ys = np.where(col)[0]
print("beige col300 y:", ys.min(), ys.max())

# title red text
redt = (r > 150) & (g < 90) & (b < 90)
tit = redt[40:110, 150:820]
comps = [dict(x0=c["x0"]+150, x1=c["x1"]+150, y0=c["y0"]+40, y1=c["y1"]+40, n=c["n"],
              cx=c["cx"]+150, cy=c["cy"]+40) for c in components(tit, 20)]
show("title red text", comps)

# magenta boxes top strip
mag = (r > 190) & (b > 190) & (g < 170) & (abs(r - b) < 60)
top = mag[100:180, :]
show("magenta top strip", components(top, 15))

# dashed line: magenta-ish pixels between the boxes
dash = mag.copy()
dash[:100] = False; dash[180:] = False
mid = dash[:, 140:815]
show("dashed line", components(mid, 2))

# red mesh lines inside panel (exclude text): find thin structures.
redp = (r > 140) & (g < 100) & (b < 100)
panel = np.zeros_like(redp)
panel[168:422, 68:795] = True
mesh = redp & panel
# remove neuron circles (large blobs): label and drop area>800
lab, n = ndimage.label(mesh)
sizes = ndimage.sum(mesh, lab, range(1, n + 1))
big = np.isin(lab, np.where(sizes > 900)[0] + 1)
lines = mesh & ~big
show("red lines (mesh+arrows, thin comps)", components(lines, 25))

# neuron circles by fill colors
def circles(mask, minpx=150):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < minpx:
            continue
        w = xs.max() - xs.min() + 1; h = ys.max() - ys.min() + 1
        out.append(dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()),
                        w=int(w), h=int(h), n=int(len(ys)),
                        cx=float(xs.mean()), cy=float(ys.mean())))
    return out

print("\n== neuron fills (sampled at expected centers)")
# detect all non-beige, non-red-line blobs: use gray/blue/green/orange masks
grayn = (abs(r - 204) < 18) & (abs(g - 204) < 18) & (abs(b - 204) < 18)
bluen = (abs(r - 153) < 30) & (abs(g - 204) < 25) & (b > 230)
greenn = (g > 220) & (r > 120) & (r < 190) & (b < 140)
orangen = (r > 240) & (abs(g - 190) < 35) & (b < 130)
for nm, m in (("gray", grayn), ("blue", bluen), ("green", greenn), ("orange", orangen)):
    mm = m.copy(); mm[:165] = False; mm[425:] = False; mm[:, :65] = False; mm[:, 796:] = True
    mm[:, 796:] = False
    show(f"neuron fill {nm}", circles(mm))

print("\n== sampled colors at approximate neuron centers")
for (cx, cy) in [(165, 213), (165, 285), (165, 363),
                 (255, 213), (255, 285), (255, 363),
                 (425, 213), (425, 285), (425, 363),
                 (585, 213), (585, 285), (585, 363),
                 (670, 213), (670, 285), (670, 363)]:
    print(f"  ({cx},{cy}):", sample(cx, cy))

# black ink inside panel (dividers, glyphs, output boxes, arrows)
blackm = (r < 80) & (g < 80) & (b < 80)
blk = blackm.copy(); blk[:165] = False; blk[430:] = False; blk[:, :60] = False; blk[:, 800:] = False
# output boxes are big rects x>710
show("black in panel right (output boxes+arrows)", components(blk[:, 700:800], 30))
# divider lines + glyphs: thin vertical strokes in neuron region
div = blackm.copy(); div[:165] = False; div[430:] = False; div[:, :60] = False; div[:, 700:] = False
divc = components(div, 8)
show("black thin in neurons zone", [c for c in divc if (c['x1']-c['x0']+1) <= 40])

# magenta dots left
magd = mag.copy(); magd[:165] = False; magd[430:] = False; magd[:, 130:] = False
show("magenta input dots", components(magd, 4))

# gray fan lines
grayl = (abs(r - 170) < 45) & (abs(g - 170) < 45) & (abs(b - 170) < 45) & (abs(r-g) < 14) & (abs(g-b) < 14)
fan = grayl.copy(); fan[:165] = False; fan[430:] = False; fan[:, :60] = False; fan[:, 160:] = False
show("gray fan lines region", components(fan, 15))

# hollow circles (small rings) after col1 and before col5 — rings: light fill with dark edge.
# find them via black-ish ring pixels in the zones
hollow1 = blackm.copy(); hollow1[:165] = False; hollow1[430:] = False; hollow1[:, :175] = False; hollow1[:, 245:] = False
show("hollow after col1 (ring ink)", components(hollow1, 3))
hollow5 = blackm.copy(); hollow5[:165] = False; hollow5[430:] = False; hollow5[:, 610:] = False; hollow5[:, 660:] = False
show("hollow before col5 (ring ink)", components(hollow5, 3))

# red text labels (Net/O) vs lines: red mask minus line mask
redtext = mesh & ~lines & ~big
show("red big comps (lines-blobs)", components(big, 25))

# output boxes
ob = blackm.copy(); ob[:165] = False; ob[430:] = False; ob[:, :700] = False; ob[:, 800:] = False
show("output boxes black", components(ob, 80))

# error bar: dark red 990000 x 795..825
err = (abs(r - 153) < 45) & (g < 60) & (b < 60)
erb = err.copy(); erb[:150] = False; erb[430:] = False; erb[:, :780] = False; erb[:, 830:] = False
show("error bar dark red", components(erb, 50))
print("error bar color sample (808,300):", sample(808, 300))

# bright red Error text inside bar
ert = redp.copy(); ert[:150] = False; ert[430:] = False; ert[:, :780] = False; ert[:, 830:] = False
show("Error bright red text", components(ert, 8))
print("error text sample (808,210):", sample(808, 210), "(808,285):", sample(808, 285), "(808,363):", sample(808, 363))

# class boxes green
clsg = (g > 200) & (abs(r - 153) < 60) & (b < 120)
cls = clsg.copy(); cls[:150] = False; cls[430:] = False; cls[:, :820] = False
show("class boxes", components(cls, 40))
print("class box sample (855,210):", sample(855, 210), "(855,285):", sample(855, 285), "(855,363):", sample(855, 363))

# block arrows bottom (blue/green/orange)
arrb = (r > 200) & (g < 190) & (b < 150)
ab = arrb.copy(); ab[:420] = False; ab[470:] = False; ab[:, :200] = False; ab[:, 700:] = False
show("orange arrow k", components(ab, 40))
bluea = (b > 180) & (r < 120) & (g < 160)
ba = bluea.copy(); ba[:420] = False; ba[470:] = False; ba[:, :200] = False; ba[:, 700:] = False
show("blue arrow i", components(ba, 40))
greena = (g > 150) & (r < 120) & (b < 120)
ga = greena.copy(); ga[:420] = False; ga[470:] = False; ga[:, :200] = False; ga[:, 700:] = False
show("green arrow j", components(ga, 40))
print("arrow colors: i(263,410):", sample(263, 410), " j(428,410):", sample(428, 410), " k(588,410):", sample(588, 410))

# callout boxes y430..465
cb = A[425:470, :, :]
cbr, cbg, cbb = cb[:, :, 0], cb[:, :, 1], cb[:, :, 2]
callb = (cbr > 200) & (cbr < 255) & (cbb > 200) & (cbb < 255) & (cbg > 200)
lab2, n2 = ndimage.label(callb)
print("\n== callout boxes (light fills) y425..470")
for i in range(1, n2 + 1):
    ys, xs = np.where(lab2 == i)
    if len(ys) < 200:
        continue
    print(f"  x{xs.min()}..{xs.max()} y{ys.min()+425}..{ys.max()+425} n={len(ys)} sample=({int(np.median(cbr[lab2==i]))},{int(np.median(cbg[lab2==i]))},{int(np.median(cbb[lab2==i]))})")
print("callout samples: prev(263,445):", sample(263, 445), " cur(428,445):", sample(428, 445), " nxt(590,445):", sample(590, 445))

# Net label arrows (small red arrows above neurons) — part of red thin comps already
# O labels: red text right of neurons — check text bboxes in windows
print("\n== red text windows (O labels, Net labels)")
def redtextbbox(x0, x1, y0, y1, minpx=5):
    m = redp[y0:y1, x0:x1]
    c = components(m, minpx)
    return c
for nm, win in [("Net_i", (195, 245, 168, 190)), ("Net_j", (360, 412, 168, 190)), ("Net_k", (525, 577, 168, 190)),
                ("O_i r1", (266, 300, 192, 212)), ("O_i r2", (266, 300, 264, 284)), ("O_i r3", (266, 300, 342, 362)),
                ("O_j r1", (436, 470, 192, 212)), ("O_j r2", (436, 470, 264, 284)), ("O_j r3", (436, 470, 342, 362)),
                ("O_k r1", (596, 630, 192, 212)), ("O_k r2", (596, 630, 264, 284)), ("O_k r3", (596, 630, 342, 362))]:
    x0, x1, y0, y1 = win
    cs = redtextbbox(x0, x1, y0, y1)
    if cs:
        x0m = min(c['x0'] for c in cs) + x0; x1m = max(c['x1'] for c in cs) + x0
        y0m = min(c['y0'] for c in cs) + y0; y1m = max(c['y1'] for c in cs) + y0
        print(f"  {nm}: x{x0m}..{x1m} y{y0m}..{y1m} (w={x1m-x0m+1} h={y1m-y0m+1}) ncomp={len(cs)}")
    else:
        print(f"  {nm}: NO RED INK in {win}")

# blue italic weight labels
bluew = (b > 140) & (r < 110) & (g < 110)
bw = bluew.copy(); bw[:165] = False; bw[430:] = False; bw[:, :60] = False; bw[:, 700:] = False
show("blue weight labels", components(bw, 5))

# sigma/s glyph ink inside neurons — sample a divider line x offset
print("\n== neuron internals samples")
print("divider col1r1 (165,200..228 x=165..166):", [sample(165, yy, 0) for yy in range(198, 230, 6)])
# glyph ink: count dark px in left half vs right half of each neuron circle
for cx, cy, nm in [(165, 213, "col1r1"), (255, 213, "col2r1"), (425, 213, "col3r1"), (585, 213, "col4r1"), (670, 213, "col5r1")]:
    rr = 20
    win = A[cy-rr:cy+rr, cx-rr:cx+rr]
    dk = (win[:, :, 0] < 90) & (win[:, :, 1] < 90) & (win[:, :, 2] < 90)
    ys, xs = np.where(dk)
    if len(ys):
        print(f"  {nm}: dark n={len(ys)} x{xs.min()+cx-rr}..{xs.max()+cx-rr} y{ys.min()+cy-rr}..{ys.max()+cy-rr}")
    else:
        print(f"  {nm}: no dark ink")
