#!/usr/bin/env python3
"""forensics20_045.py — final probes: D4 pointer mark RGB/extent, org x717 vertical,
org house-border sanity, ren5 D2 min-clearance, ren5 star-zone ASCII (D1 evidence).
Banked as qa/slide045/forensics20_out.txt."""
import numpy as np
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
ren = np.asarray(Image.open(f"{QA}/render_5.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
S = ren.shape[0] / 540.0
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line); print(line)

def darkmask(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    red = (r - g > 25) & (r - b > 15) & (r > 90)
    return (lum < 205) & ~red, red
do_, ro_ = darkmask(org)
dr_, rr_ = darkmask(ren)

def px(m, k, fx, fy):
    return m[int(round(fy*k)), int(round(fx*k))]

P("== D4 pointer mark: RGB along the stroke (org) ==")
for fx, fy in ((524, 436), (525, 437), (526, 439), (528, 441), (530, 443), (532, 446), (533, 448), (524, 435), (523, 436)):
    v = org[fy, fx]
    P(f"  org({fx},{fy}) RGB={tuple(int(c) for c in v)} lum={int(v.mean())}")
P("  extent scan (dark px, x515..545 y430..455):")
ys, xs = np.where(do_[430:456, 515:546])
if len(ys):
    P(f"    bbox x{515+xs.min()}..{515+xs.max()} y{430+ys.min()}..{430+ys.max()} n={len(ys)}")

P("")
P("== org x717..718 vertical: full extent + RGB ==")
ys, xs = np.where(do_[300:539, 714:722])
if len(ys):
    P(f"  dark bbox x{714+xs.min()}..{714+xs.max()} y{300+ys.min()}..{300+ys.max()} n={len(ys)}")
for fy in (360, 380, 400, 420, 440, 460, 470):
    P(f"  org(717,{fy}) RGB={tuple(int(c) for c in org[fy, 717])}  org(718,{fy})={tuple(int(c) for c in org[fy, 718])}")

P("")
P("== org house right border sanity (x892..930 y110..170 dark/red scan) ==")
r, g, b = org[:, :, 0], org[:, :, 1], org[:, :, 2]
redm = (r - g > 25) & (r - b > 15) & (r > 90)
ys, xs = np.where(redm[110:171, 892:931])
P(f"  red px: {'NONE' if len(ys)==0 else f'x{892+xs.min()}..{892+xs.max()} y{110+ys.min()}..{110+ys.max()} n={len(ys)}'}")
ys, xs = np.where(do_[110:171, 892:931])
P(f"  dark px: {'NONE' if len(ys)==0 else f'x{892+xs.min()}..{892+xs.max()} y{110+ys.min()}..{110+ys.max()} n={len(ys)}'}")

P("")
P("== D2: min clearance red-wedge <-> dark ink (x592..626 y332..360) ==")
def dilate(m, it):
    for _ in range(it):
        p = np.pad(m, 1)
        m = (p[0:-2,0:-2]|p[0:-2,1:-1]|p[0:-2,2:]|p[1:-1,0:-2]|p[1:-1,1:-1]|p[1:-1,2:]|
             p[2:,0:-2]|p[2:,1:-1]|p[2:,2:])
    return m
for nm, redm, darkm, k in (("org", ro_, do_, 1.0), ("ren5", rr_, dr_, S)):
    win_r = redm[int(332*k):int(360*k)+1, int(592*k):int(626*k)+1]
    win_d = darkm[int(332*k):int(360*k)+1, int(592*k):int(626*k)+1]
    for it in range(0, 6):
        if (dilate(win_r.copy(), it) & win_d).any():
            P(f"  {nm}: min clearance = {it} px (first contact at dilation {it})")
            break
    else:
        P(f"  {nm}: clearance >= 5 px")

P("")
P("== ren5 star zone ASCII (x756..900 y105..160; r=red, y=yellow-fill, #=dark) ==")
r, g, b = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
yelm = (r > 195) & (g > 195) & (b < 225) & ((r - b) > 18) & ((g - b) > 18)
for fy in range(105, 161):
    line = f" y{fy:4d} "
    for fx in range(756, 901):
        rr_ = px(rr_, S, fx, fy); yy = px(yelm, S, fx, fy); dd = px(dr_, S, fx, fy)
        line += "r" if rr_ else ("y" if yy else ("#" if dd else "."))
    out.append(line); print(line)

open(f"{QA}/forensics20_out.txt", "w").write("\n".join(out) + "\n")
print("\nwrote forensics20_out.txt")
