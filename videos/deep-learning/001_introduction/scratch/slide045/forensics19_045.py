#!/usr/bin/env python3
"""forensics19_045.py — corrected D4 zone maps (org dark+red, bug-fixed) + D1 line-1
per-column ink continuity (detect star-covered characters) + contact locations.
Banked as qa/slide045/forensics19_out.txt."""
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

def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    red = (r - g > 25) & (r - b > 15) & (r > 90)
    dark = (lum < 205) & ~red
    return red, dark

ro, do = masks(org)
rr, dr = masks(ren)

def px(mask, k, fx, fy):
    return mask[int(round(fy*k)), int(round(fx*k))]

def amap(redm, darkm, k, X0, X1, Y0, Y1, tag):
    P(f"-- {tag} (x{X0}..{X1} y{Y0}..{Y1}; r=red, #=dark) --")
    for fy in range(Y0, Y1+1):
        line = f" y{fy:4d} "
        for fx in range(X0, X1+1):
            r_ = px(redm, k, fx, fy)
            d_ = px(darkm, k, fx, fy)
            line += "r" if r_ else ("#" if d_ else ".")
        out.append(line); print(line)

P("== D4 ZONE MAPS (bug-fixed: each image uses its OWN dark mask) ==")
amap(ro, do, 1.0, 460, 630, 418, 462, "ORG Gradient-line zone (b3 label + limits)")
amap(rr, dr, S, 460, 630, 418, 462, "REN5 Gradient-line zone")
amap(ro, do, 1.0, 620, 745, 415, 478, "ORG eq(c) -> Input-callout zone")
amap(ro, do, 1.0, 756, 900, 105, 160, "ORG starburst bottom / defbox line-1 tail")

P("")
P("== D1: line-1 band per-column dark-ink count (y119..145), x756..888 ==")
P("   (a column with ink in org but none in ren5 under the star = covered character)")
missing = []
extra = []
for fx in range(756, 889):
    o = sum(px(do, 1.0, fx, fy) for fy in range(119, 146))
    r_ = sum(px(dr, S, fx, fy) for fy in range(119, 146))
    if o > 0 and r_ == 0:
        missing.append((fx, o))
    if r_ > 0 and o == 0:
        extra.append((fx, r_))
P(f"  org-ink-but-ren5-empty columns: {missing if missing else 'NONE'}")
P(f"  ren5-ink-but-org-empty columns: {extra[:20]}{'...' if len(extra)>20 else ''} (n={len(extra)})")

P("")
P("== D1: where are the star^text contacts? (window y117..150 x756..895) ==")
def dilate(m):
    p = np.pad(m, 1)
    return (p[0:-2,0:-2]|p[0:-2,1:-1]|p[0:-2,2:]|p[1:-1,0:-2]|p[1:-1,1:-1]|p[1:-1,2:]|
            p[2:,0:-2]|p[2:,1:-1]|p[2:,2:])
r_, g_, b_ = org[:,:,0], org[:,:,1], org[:,:,2]
yo = (r_ > 195) & (g_ > 195) & (b_ < 225) & ((r_ - b_) > 18) & ((g_ - b_) > 18)
r_, g_, b_ = ren[:,:,0], ren[:,:,1], ren[:,:,2]
yr = (r_ > 195) & (g_ > 195) & (b_ < 225) & ((r_ - b_) > 18) & ((g_ - b_) > 18)
for nm, redm, yelm, darkm, k in (("org", ro, yo, do, 1.0), ("ren5", rr, yr, dr, S)):
    star = (redm | yelm)[int(117*k):int(150*k)+1, int(756*k):int(895*k)+1]
    tx = darkm[int(117*k):int(150*k)+1, int(756*k):int(895*k)+1]
    touch = dilate(star) & tx
    ys, xs = np.where(touch)
    if len(ys):
        # cluster the contact x positions
        xs_f = sorted(set(int(756 + x/k) for x in xs))
        groups = []
        for v in xs_f:
            if groups and v - groups[-1][-1] <= 3:
                groups[-1].append(v)
            else:
                groups.append([v])
        P(f"  {nm}: contact x-clusters: {[f'{gp[0]}..{gp[-1]}' for gp in groups]}")
    else:
        P(f"  {nm}: no contacts")

P("")
P("== RAW RGB samples (sanity) ==")
for tag, im, k, fx, fy in (("org x916 y140", org, 1.0, 916, 140),
                            ("org x918 y140", org, 1.0, 918, 140),
                            ("ren5 x917 y140", ren, S, 917, 140),
                            ("org x500 y436", org, 1.0, 500, 436),
                            ("org x700 y436", org, 1.0, 700, 436),
                            ("org x660 y436", org, 1.0, 660, 436)):
    v = im[int(round(fy*k)), int(round(fx*k))]
    P(f"  {tag}: RGB={tuple(int(c) for c in v)}")

open(f"{QA}/forensics19_out.txt", "w").write("\n".join(out) + "\n")
print("\nwrote forensics19_out.txt")
