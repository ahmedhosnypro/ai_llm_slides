#!/usr/bin/env python3
# Pre-judge self-check for slide 044 attempt 1 (150dpi render 2001x1125; frame px *2000/960).
# v2: density-based panel detection; original-referenced margins; chrome strokes excluded.
from PIL import Image
import numpy as np
REN = "recreated_pptx/qa/slide044/render_1.png"
ORG = "unique_slides/slide_044.jpg"
S = 2000/960.0
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
L = np.asarray(Image.open(REN).convert("L")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
orgL = np.asarray(Image.open(ORG).convert("L")).astype(int)
fails, notes = [], []
def fr(v): return v*S

# 1. inset panel: green border via DENSITY (border columns carry hundreds of green px)
r,g,b = im[...,0], im[...,1], im[...,2]
green = (g>90)&(g-r>40)&(g-b>40)
sub = green[int(fr(70)):int(fr(310)), int(fr(715)):int(fr(925))]
cols = sub.sum(axis=0); rows = sub.sum(axis=1)
cd = np.where(cols>80)[0]; rd = np.where(rows>80)[0]
if not len(cd) or not len(rd): fails.append("panel: green border strokes not found (density)")
else:
    x0,x1 = 715+cd.min()/S, 715+cd.max()/S
    y0,y1 = 70+rd.min()/S, 70+rd.max()/S
    notes.append(f"panel border bands: x {x0:.1f}..{x1:.1f} y {y0:.1f}..{y1:.1f} (orig strokes 738-741/904-908, 80-83/294-298)")
    if abs(x0-739.5)>4 or abs(x1-906.5)>4 or abs(y0-81.5)>4 or abs(y1-296.5)>4:
        fails.append(f"panel border centerline off: x{x0:.1f}..{x1:.1f} y{y0:.1f}..{y1:.1f}")
white = (r>235)&(g>235)&(b>235)
if not white[int(fr(110)), int(fr(750))] or not white[int(fr(250)), int(fr(860))]:
    fails.append("panel interior not white at reference points")

# 2. stack front box: lavender fill + dark top border (rows 168..173)
lav = (abs(r-190)<28)&(abs(g-180)<28)&(abs(b-212)<30)
cnt = lav[int(fr(172)):int(fr(198)), int(fr(750)):int(fr(870))].sum()
notes.append(f"lavender stack px: {int(cnt)}")
if cnt < 2000: fails.append(f"stack lavender fill sparse: {cnt}")
band = L[int(fr(168)):int(fr(173)), int(fr(750)):int(fr(870))]
if (band<110).sum() < 200: fails.append(f"stack front top border weak: {(band<110).sum()}")

# 3. concat pale-yellow fill
yel2 = (r>225)&(g>235)&(b<225)&(g-b>18)
c2 = yel2[int(fr(131)):int(fr(147)), int(fr(788)):int(fr(830))].sum()
notes.append(f"concat yellow px: {int(c2)}")
if c2 < 400: fails.append(f"concat yellow fill sparse: {c2}")

# 4. bottom three Linear boxes: white interior + dark left borders (band min)
for bx in (745,791,837):
    interior = white[int(fr(228)), int(fr(bx+6)):int(fr(bx+33))].sum()
    if interior < 20: fails.append(f"bottom box @{bx} interior not white")
    band = L[int(fr(226)):int(fr(234)), int(fr(bx-1)):int(fr(bx+2.5))]
    if band.min() > 150: fails.append(f"bottom box @{bx} left border not dark")

# 5. V/K/Q ink present at y280..290
for cx,label in ((763.5,"V"),(809.5,"K"),(855.5,"Q")):
    zone = L[int(fr(280)):int(fr(290)), int(fr(cx-7)):int(fr(cx+7))]
    if (zone<120).sum() < 4: fails.append(f"{label} label ink missing")

# 6. arrow shafts present
for cx,y0f,y1f,label in ((810.5,88,96,"top out"),(810.5,118,128,"lin->concat"),
                          (810.5,150,167,"concat->stack"),(763.5,245,275,"arr V"),
                          (809.5,245,275,"arr K"),(855.5,245,275,"arr Q")):
    col = L[int(fr(y0f)):int(fr(y1f)), int(fr(cx))]
    if (col<140).sum() < (y1f-y0f)*0.4: fails.append(f"arrow shaft {label} weak: {(col<140).sum()}")

# 7. title alignment vs original (frame px)
def ink_extent(imgL, scale, y0,y1,x0,x1,thr=120):
    m = (imgL[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)] < thr)
    ys,xs = np.where(m)
    if not len(xs): return None
    return (x0+xs.min()/scale, x0+xs.max()/scale, int(m.sum()))
r1 = ink_extent(L, S, 52,78, 500,870); o1 = ink_extent(orgL, 1.0, 52,78, 500,870)
notes.append(f"title line1 ink: render {r1} vs orig {o1}")
if r1 and o1 and abs((r1[0]+r1[1])/2 - (o1[0]+o1[1])/2) > 6: fails.append("title line1 center off vs original")
r2 = ink_extent(L, S, 80,99, 560,736); o2 = ink_extent(orgL, 1.0, 80,99, 560,736)
notes.append(f"title line2 visible ink: render {r2} vs orig {o2}")
if r2 and o2 and abs(r2[1]-o2[1])>6: fails.append("title line2 visible tail end off")

# 8. containment: inset ink bbox vs the ORIGINAL's own ink bbox in the panel
def panel_ink(imgL, scale):
    m = (imgL[int(84*scale):int(294*scale), int(742*scale):int(904*scale)] < 130)
    ys,xs = np.where(m)
    return (742+xs.min()/scale, 742+xs.max()/scale, 84+ys.min()/scale, 84+ys.max()/scale)
pi_r = panel_ink(L, S); pi_o = panel_ink(orgL, 1.0)
notes.append(f"panel ink bbox: render {tuple(round(v,1) for v in pi_r)} vs orig {tuple(round(v,1) for v in pi_o)}")
if any(abs(a-bb)>5 for a,bb in zip(pi_r, pi_o)): fails.append("panel inner ink extent differs from original by >5 frame px")
# house frame: THIS slide's content ink inside 42..918 / 45..538 (chrome strokes excluded)
d2 = L < 130
win = d2[int(fr(48)):int(fr(534)), int(fr(47)):int(fr(914))]
ys3,xs3 = np.where(win)
lx, rx = 47+xs3.min()/S, 47+xs3.max()/S
notes.append(f"content ink x {lx:.1f}..{rx:.1f} (house frame inner 45..915)")
if lx < 43 or rx > 916: fails.append(f"content ink outside house frame: x {lx:.1f}..{rx:.1f}")

# 9. h=5 tag zone: render must LOOK like the original there (lavender box bottom/border, no black tag)
zr = im[int(fr(199)):int(fr(212)), int(fr(748)):int(fr(778))].astype(float)
zo = np.asarray(Image.fromarray(org[199:212, 748:778].astype(np.uint8)).resize((zr.shape[1], zr.shape[0]), Image.LANCZOS)).astype(float)
mad = np.abs(zr-zo).mean()
notes.append(f"h5-tag zone mean|diff| vs original: {mad:.1f}")
if mad > 60: fails.append(f"h5-tag zone differs from original (mad {mad:.0f})")

# 10. title sliver above the panel top stroke (orig text rows 78-79)
sliver = (L[int(fr(78)):int(fr(79.8)), int(fr(600)):int(fr(736))] < 120).sum()
osliver = (orgL[78:80, 600:736] < 120).sum()
notes.append(f"title sliver above panel: render {int(sliver)} px vs orig {int(osliver)} px")
if abs(int(sliver)-int(osliver)) > 3: fails.append("title sliver band differs from original")

# 11. badge yellow cut matches the original (occlusion)
def yel_ext(img, scale):
    rr,gg,bb = img[...,0], img[...,1], img[...,2]
    yel = (rr>200)&(gg>200)&(bb<190)
    y0=int(71*scale-36*scale)
    win = yel[y0:int(71*scale+36*scale), int(893*scale-36*scale):int(893*scale+36*scale)]
    ys,xs = np.where(win)
    return (y0+ys.min())/scale, (y0+ys.max())/scale
ye_r, ye_o = yel_ext(im, S), yel_ext(org, 1.0)
notes.append(f"badge yellow y-extent: render {ye_r} vs orig {ye_o}")
if abs(ye_r[1]-ye_o[1])>4: fails.append("badge occlusion cut differs from original")

print("== selfcheck attempt 1 (v2) ==")
for n in notes: print("  note:", n)
if fails:
    print("FAIL")
    for f in fails: print("  -", f)
    raise SystemExit(1)
print("PASS")
