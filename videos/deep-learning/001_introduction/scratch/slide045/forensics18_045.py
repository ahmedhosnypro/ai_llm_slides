#!/usr/bin/env python3
"""forensics18_045.py — closed-loop D1/D2/D4 forensics on the ORIGINAL frame vs render_5.

D1: starburst vs defbox line-1 text — star-ink (red spikes + pale-yellow fill) per-column
    bottom profile in the defbox text band; direct star-vs-text ink overlap counts.
D2: arrow wedge vs eq(a) x_{r-i,c-j} subscript — red-vs-darkink contact in the sub_a zone.
D4: complete red-annotation inventory of the original in the equation area (x460..900,
    y300..475) vs render_5 — every red component enumerated; ASCII maps of the Gradient-
    line zone (D4) and the eq(c)/Input-callout zone.
Banked as qa/slide045/forensics18_out.txt.
"""
import numpy as np
from PIL import Image
from collections import deque

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
ren = np.asarray(Image.open(f"{QA}/render_5.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
S = ren.shape[0] / 540.0
out = []
def P(*a):
    line = " ".join(str(x) for x in a)
    out.append(line); print(line)

def masks(im, k):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    red = (r - g > 25) & (r - b > 15) & (r > 90)
    yellow = (r > 195) & (g > 195) & (b < 225) & ((r - b) > 18) & ((g - b) > 18)
    dark = (lum < 205) & ~red
    return red, yellow, dark

def win(mask, k, x0, x1, y0, y1):
    return mask[int(y0*k):int(y1*k)+1, int(x0*k):int(x1*k)+1]

def dilate(m):
    p = np.pad(m, 1)
    return (p[0:-2,0:-2]|p[0:-2,1:-1]|p[0:-2,2:]|p[1:-1,0:-2]|p[1:-1,1:-1]|p[1:-1,2:]|
            p[2:,0:-2]|p[2:,1:-1]|p[2:,2:])

def comps(mask, k, X0, X1, Y0, Y1, min_n=8):
    w = win(mask, k, X0, X1, Y0, Y1)
    lab = np.zeros(w.shape, bool); res = []
    for y in range(w.shape[0]):
        for x in range(w.shape[1]):
            if w[y, x] and not lab[y, x]:
                q = deque([(y, x)]); lab[y, x] = True; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy+dy, cx+dx
                            if 0 <= ny < w.shape[0] and 0 <= nx < w.shape[1] and w[ny, nx] and not lab[ny, nx]:
                                lab[ny, nx] = True; q.append((ny, nx))
                if len(pts) >= min_n:
                    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                    res.append((X0+min(xs)/k, X0+max(xs)/k, Y0+min(ys)/k, Y0+max(ys)/k, len(pts)/(k*k)))
    return sorted(res, key=lambda t: -t[4])

ro, yo, do = masks(org, 1.0)
rr, yr, dr = masks(ren, S)

P("== D1: STARBURST vs DEFBOX LINE-1 ==")
P("-- star-ink (red|yellow) per-column max-y in band y>=105, x756..924 (step 4; frame px) --")
for nm, sm, k in (("org", None, 1.0), ("ren5", None, S)):
    redm, yelm, darkm = (ro, yo, do) if nm == "org" else (rr, yr, dr)
    star = redm | yelm
    prof = []
    for x in range(756, 925, 4):
        col = win(star, k, x, min(x+3, 924), 105, 165)
        ys, xs = np.where(col)
        prof.append(f"{x}:{(105+ys.max()/k) if len(ys) else '-'}")
    P(f"  {nm}: " + " ".join(prof))
P("-- overlap star-ink vs line-1 TEXT darkink (window y117..150 x756..895) --")
for nm, (redm, yelm, darkm), k in (("org", (ro, yo, do), 1.0), ("ren5", (rr, yr, dr), S)):
    star = (redm | yelm)
    st = win(star, k, 756, 895, 117, 150)
    tx = win(darkm, k, 756, 895, 117, 150)
    exact = int((st & tx).sum() / (k*k))
    touch = int((dilate(st) & tx).sum() / (k*k))
    ys, xs = np.where(tx)
    txr = (756+xs.min()/k, 756+xs.max()/k, 117+ys.min()/k, 117+ys.max()/k) if len(ys) else None
    P(f"  {nm}: text-bbox={txr}  star^text exact={exact}  within1px={touch}")
P("-- star ink columns descending below defbox top border (y>=116), x-range --")
for nm, (redm, yelm), k in (("org", (ro, yo), 1.0), ("ren5", (rr, yr), S)):
    star = redm | yelm
    band = win(star, k, 700, 930, 116, 165)
    ys, xs = np.where(band)
    if len(ys):
        P(f"  {nm}: star-ink below y116: x {700+xs.min()/k:.0f}..{700+xs.max()/k:.0f}  ymax={116+ys.max()/k:.1f}  n={int(len(ys)/(k*k))}")
    else:
        P(f"  {nm}: none")

P("")
P("== D2: ARROW WEDGE vs sub_a (x_{r-i,c-j}) INK ==")
for nm, (redm, darkm), k in (("org", (ro, do), 1.0), ("ren5", (rr, dr), S)):
    sub = win(darkm, k, 604, 654, 336, 352)
    red = win(redm, k, 604, 654, 336, 352)
    nsub = int(sub.sum()/(k*k))
    exact = int((red & sub).sum()/(k*k))
    touch = int((dilate(red) & sub).sum()/(k*k))
    P(f"  {nm}: sub_ink={nsub}  red^sub exact={exact} ({100.0*exact/max(nsub,1):.1f}%)  red-within1px={touch} ({100.0*touch/max(nsub,1):.1f}%)")
P("-- wedge red component bboxes (window x592..660 y330..362) --")
for nm, redm, k in (("org", ro, 1.0), ("ren5", rr, S)):
    cs = comps(redm, k, 592, 660, 330, 362)
    P(f"  {nm}: " + "; ".join(f"x{a:.0f}..{b:.0f} y{c:.0f}..{d:.0f} n={n:.0f}" for a, b, c, d, n in cs[:5]))

P("")
P("== D4: RED-ANNOTATION INVENTORY x460..900 y300..475 (org vs ren5) ==")
for nm, redm, k in (("org", ro, 1.0), ("ren5", rr, S)):
    cs = comps(redm, k, 460, 900, 300, 475, min_n=6)
    P(f"  {nm}: {len(cs)} components")
    for a, b, c, d, n in cs[:12]:
        P(f"    x{a:6.1f}..{b:6.1f} y{c:6.1f}..{d:6.1f} n={n:6.0f}")

def ascii_map(mask, k, X0, X1, Y0, Y1, tag):
    P(f"-- {tag} (x{X0}..{X1} y{Y0}..{Y1}; r=red, #=dark ink) --")
    w = win(mask, k, X0, X1, Y0, Y1)
    ysw = int((Y1-Y0)*k)+1
    for yy in range(0, ysw, max(1, int(round(k)))):
        row = ""
        for xx in range(0, w.shape[1], 1):
            blk = w[yy:yy+max(1,int(round(k))), xx:xx+1]
            row += "r" if blk.any() and False else ""
        # simpler: per cell of 1 frame-px
    # frame-px cells
    for fy in range(Y0, Y1+1):
        line = f" y{fy:4.0f} "
        for fx in range(X0, X1+1):
            cell_r = win(redm, k, fx, fx, fy, fy).any()
            cell_d = win(darkm, k, fx, fx, fy, fy).any() if darkm is not None else False
            line += "r" if cell_r else ("#" if cell_d else ".")
        out.append(line); print(line)

P("")
P("== D4 ZONE MAPS (org only) ==")
ascii_map(ro, 1.0, 470, 600, 424, 462, "org Gradient/N-2a zone (red+dark)")
ascii_map(ro, 1.0, 640, 740, 430, 476, "org eq(c)->Input-callout zone (red+dark)")
P("")
P("== D4 ZONE MAP (ren5, Gradient/N-2a zone) ==")
ascii_map(rr, S, 470, 600, 424, 462, "ren5 Gradient/N-2a zone")

open(f"{QA}/forensics18_out.txt", "w").write("\n".join(out) + "\n")
print("\nwrote forensics18_out.txt")
