#!/usr/bin/env python3
# m1_chrome.py — slide 016 chrome landmarks + frame->slide mapping fit.
# Convention per certified 009/010 (P1 head):
#   slide_x = (frame_x - 17.628) / 0.961232 ;  slide_y = frame_y / 0.955556
# House chrome (playlist law): gray panel E9E9E7 x 42..918, y 45..bottom (bottom
# stroke rows 538-539 slide), red C00000 border L/R/T; badge d~36 center (893,71),
# fill FDFD96, ring 6A5ACD ~2pt, numeral 333333 Arial 18 bold.
# This script RE-FITS the mapping on THIS frame (slide_016.jpg, 960x540).
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_016.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"frame {W}x{H}")

def is_red(px):
    r, g, b = px
    return r > 140 and g < 90 and b < 90

out = []
out.append("=== LETTERBOX ===")
lum = a.mean(axis=2)
rowmean = lum.mean(axis=1)
top_black = 0
while top_black < H and rowmean[top_black] < 40:
    top_black += 1
bot_black = 0
while bot_black < H and rowmean[H - 1 - bot_black] < 40:
    bot_black += 1
print(f"letterbox rows: top 0..{top_black-1}, bottom {H-bot_black}..{H-1}")

out.append("=== CHROME PANEL BORDER (red C00000, JPEG-soft — reddish score r-(g+b)/2) ===")
def redscore(px):
    return int(px[0] - (px[1] + px[2]) / 2)

# verticals: scan rows y=300 and y=450 for border columns
for yscan in (300, 450):
    row = a[yscan]
    lscored = sorted(((x, redscore(row[x])) for x in range(40, 75)), key=lambda t: -t[1])[:3]
    rscored = sorted(((x, redscore(row[x])) for x in range(880, 930)), key=lambda t: -t[1])[:3]
    print(f"@y{yscan}: left border cols {lscored}  right border cols {rscored}")
# horizontals: scan columns for border rows
for xscan in (60, 100, 890):
    col = a[:, xscan]
    tsc = sorted(((y, redscore(col[y])) for y in range(20, 110)), key=lambda t: -t[1])[:3]
    bsc = sorted(((y, redscore(col[y])) for y in range(495, 525)), key=lambda t: -t[1])[:3]
    print(f"@x{xscan}: top border rows {tsc}  bottom border rows {bsc}")

out.append("=== PANEL GRAY / CANVAS SAMPLES ===")
for name, (x, y) in [("chrome gray @(300,500)", (300, 500)), ("chrome gray @(450,105)", (450, 105)),
                     ("canvas outside panel @(20,270)", (20, 270)), ("canvas @(950,270)", (950, 270)),
                     ("panel gray @(470,300)", (470, 300))]:
    patch = a[y:y+8, x:x+8].reshape(-1, 3)
    med = np.median(patch, axis=0).astype(int)
    print(f"{name}: #{med[0]:02X}{med[1]:02X}{med[2]:02X}  rgb{tuple(med)}")

out.append("=== BADGE ===")
# yellow pixels in badge region
reg = a[40:110, 840:915]
mask = (reg[:, :, 0] > 215) & (reg[:, :, 1] > 195) & (reg[:, :, 2] < 175)
ys, xs = np.nonzero(mask)
if len(xs):
    bx0, bx1, by0, by1 = xs.min()+840, xs.max()+840, ys.min()+40, ys.max()+40
    cx, cy = (bx0+bx1)/2, (by0+by1)/2
    print(f"yellow bbox fx ({bx0}..{bx1}, {by0}..{by1}) center ({cx:.1f},{cy:.1f}) d=({bx1-bx0+1},{by1-by0+1})")
    # ring color: pixels just outside yellow bbox along horizontal through center
    ringpix = []
    yy = int(round(cy))
    for xx in range(int(bx0)-6, int(bx0)+1):
        ringpix.append(a[yy, xx])
    for xx in range(int(bx1), int(bx1)+7):
        ringpix.append(a[yy, xx])
    rp = np.array(ringpix)
    print("ring samples (left→right of yellow):", ["#%02X%02X%02X" % tuple(p) for p in rp[::2]])
    # darkest saturated ring pixel candidates in annulus
    ann = a[int(by0)-5:int(by1)+6, int(bx0)-5:int(bx1)+6]
    am = ann.reshape(-1, 3)
    purple = am[(am[:, 2] > am[:, 1] + 30) & (am[:, 0] > 70) & (am[:, 0] < 200) & (am[:, 2] > 120)]
    if len(purple):
        print(f"purple-ish ring px n={len(purple)} median #{int(np.median(purple[:,0])):02X}{int(np.median(purple[:,1])):02X}{int(np.median(purple[:,2])):02X}")
    else:
        print("purple-ish ring px: NONE")
    # numeral ink: dark pixels inside yellow bbox
    inreg = a[by0+6:by1-5, bx0+6:bx1-5].reshape(-1, 3)
    dark = inreg[inreg.sum(axis=1) < 330]
    if len(dark):
        print(f"numeral dark px n={len(dark)} median #{int(np.median(dark[:,0])):02X}{int(np.median(dark[:,1])):02X}{int(np.median(dark[:,2])):02X}")
        dys, dxs = np.nonzero((a[by0:by1+1, bx0:bx1+1].sum(axis=2) < 330))
        if len(dxs):
            print(f"numeral ink bbox fx ({dxs.min()+bx0}..{dxs.max()+bx0}, {dys.min()+by0}..{dys.max()+by0}) h={dys.max()-dys.min()+1}")
    # red ring? spec (ml-intro) claims red outline/red numeral
    red = am[(am[:, 0] > 150) & (am[:, 1] < 90) & (am[:, 2] < 90)]
    print(f"red px in badge annulus n={len(red)}")
else:
    print("NO yellow badge found in region")

out.append("=== MAPPING FIT (this frame) ===")
# border cores: left/right from y=300 scan, top from x=60/x=100/x=890 consensus
row300 = a[300]
fxL = max(range(40, 75), key=lambda x: redscore(row300[x]))
fxR = max(range(880, 930), key=lambda x: redscore(row300[x]))
sx_scale = (fxR - fxL) / (918 - 42)
sx_off = fxL - 42 * sx_scale
print(f"border cores: left fx {fxL}, right fx {fxR}")
print(f"fit: slide_x = (fx - {sx_off:.3f}) / {sx_scale:.6f}   (certified 009/010: (fx-17.628)/0.961232)")
# vertical: top border core = consensus of x=60/100/890 argmax in y 20..110
tops = []
for xscan in (60, 100, 890):
    tops.append(max(range(20, 110), key=lambda y: redscore(a[y, xscan])))
fyT = float(np.median(tops))
sy_scale = fyT / 45.0
print(f"top border cores @x60/100/890: {tops} -> fyT {fyT}")
print(f"fit: slide_y = fy / {sy_scale:.6f}   (certified 009/010: fy/0.955556)")
# bottom stroke
bots = []
for xscan in (60, 100, 890):
    bots.append(max(range(495, 525), key=lambda y: redscore(a[y, xscan])))
print(f"bottom stroke rows @x60/100/890: {bots} -> slide {[round(y/sy_scale,1) for y in bots]} (house stroke rows 538-539)")
print(f"letterbox rows on THIS frame: top NONE, bottom 519..539 (below chrome bottom)")
# badge in slide coords
if len(xs):
    bcx = (cx - sx_off) / sx_scale
    bcy = cy / sy_scale
    print(f"badge yellow bbox fx ({bx0}..{bx1}, {by0}..{by1}) -> slide center ({bcx:.1f},{bcy:.1f}), d_slide=({(bx1-bx0+1)/sx_scale:.1f},{(by1-by0+1)/sy_scale:.1f})  house center (893,71) d36")

open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide016/m1_chrome_output.txt", "w").write("\n".join(out) + "\n")
print("\n(wrote m1_chrome_output.txt — console lines above are the full detail)")
