#!/usr/bin/env python3
"""Slide 045 — comprehensive geometry vs slide-038 certified composition.
Frame->slide mapping refit from THIS frame's chrome landmarks (house: panel
x 42..918 border cols, top row 45, bottom stroke 540; badge center (893,71) d36).
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
H, W, _ = img.shape
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
print(f"frame {W}x{H}")

# ---------- chrome mapping ----------
reddish = (R > 100) & (R - G > 50) & (R - B > 50)
L = next(x for x in range(45, 80) if reddish[100:400, x].mean() > 0.75)
Rc = next(x for x in range(W - 45, W - 80, -1) if reddish[100:400, x].mean() > 0.7)
T = next(y for y in range(30, 60) if reddish[y, 100:850].mean() > 0.75)
Bm = next(y for y in range(505, 539) if reddish[y, 100:850].mean() > 0.4)
SX = (Rc - L) / (918 - 42); OX = L - 42 * SX
SY = (Bm - T) / (540 - 45); OY = T - 45 * SY
print(f"chrome: L={L} R={Rc} T={T} Bm={Bm}  SX={SX:.6f} OX={OX:.3f} SY={SY:.6f} OY={OY:.3f}")
def sx_(fx): return (fx - OX) / SX
def sy_(fy): return (fy - OY) / SY
def band(name, x0, x1, y0, y1):
    print(f"{name}: frame x {x0}..{x1} y {y0}..{y1} -> slide x {sx_(x0):.1f}..{sx_(x1):.1f} y {sy_(y0):.1f}..{sy_(y1):.1f}")

# badge
yel = (R > 220) & (G > 220) & (B < 160)
ys, xs = np.where(yel[40:110, 840:915])
print(f"badge bbox x {xs.min()+840}..{xs.max()+840} y {ys.min()+40}..{ys.max()+40} center "
      f"({sx_((xs.min()+xs.max())/2+840):.1f},{sy_((ys.min()+ys.max())/2+40):.1f}) slide")

# ---------- title ----------
red = (R > 140) & (G < 80) & (B < 80)
seg = red[45:85, 150:800]
rows = np.where(seg.any(axis=1))[0]; cols = np.where(seg.any(axis=0))[0]
band("title ink", cols.min()+150, cols.max()+150, rows.min()+45, rows.max()+45)

# ---------- annot box ----------
# blue border: long blue rows between y 60..160, excluding badge zone x>840
blue = (B > 110) & (R < 110) & (G < 110)
for y in range(60, 160):
    row = blue[y, 70:840]
    if row.mean() > 0.6:
        print("annot top border row:", y, f"frac={row.mean():.2f}", tuple(img[y, 400])); break
for y in range(165, 100, -1):
    row = blue[y, 70:840]
    if row.mean() > 0.6:
        print("annot bottom border row:", y, f"frac={row.mean():.2f}", tuple(img[y, 400])); break
for x in range(70, 120):
    col = blue[80:150, x]
    if col.mean() > 0.7:
        print("annot left border col:", x); break
for x in range(890, 840, -1):
    col = blue[80:150, x]
    if col.mean() > 0.7:
        print("annot right border col:", x); break
# annot text lines: blue ink + red ink inside the box
blueink = blue & True
seg = blue[75:155, 95:865]
rows = np.where(seg.sum(axis=1) > 8)[0]
def to_bands(ys):
    b = []; s = ys[0]; p = ys[0]
    for v in ys[1:]:
        if v > p + 2: b.append((s, p)); s = v
        p = v
    b.append((s, p)); return b
print("annot blue text bands y:", [(a+75, b+75) for a, b in to_bands(rows)])
seg = red[75:155, 95:865]
rows = np.where(seg.sum(axis=1) > 4)[0]
print("annot red text bands y:", [(a+75, b+75) for a, b in to_bands(rows)] if len(rows) else "none")
# line-level x extents for the 3 bands
for (a, b) in to_bands(rows) if len(rows) else []:
    cs = np.where(red[a+75:b+76, 95:865].any(axis=0))[0]
    print(f"  red band y{a+75}..{b+75}: x {cs.min()+95}..{cs.max()+95} -> slide x {sx_(cs.min()+95):.1f}..{sx_(cs.max()+95):.1f} y {sy_(a+75):.1f}..{sy_(b+75):.1f}")

# ---------- panel ----------
for y in range(150, 175):
    row = blue[y, 70:890]
    if row.mean() > 0.7:
        print("panel top row:", y, tuple(img[y, 400])); break
for y in range(518, 440, -1):
    row = blue[y, 70:890]
    if row.mean() > 0.5:
        print("panel bottom row:", y, f"frac={row.mean():.2f}", tuple(img[y, 400])); break
px0 = next(x for x in range(58, 100) if blue[200:450, x].mean() > 0.6)
px1 = next(x for x in range(900, 860, -1) if blue[200:450, x].mean() > 0.6)
print(f"panel cols: {px0}..{px1} -> slide x {sx_(px0):.1f}..{sx_(px1):.1f}")

# ---------- FFN box ----------
for y in range(180, 230):
    row = blue[y, px0+8:px1-8]
    if row.mean() > 0.7:
        print("FFN top row:", y, tuple(img[y, 400])); break
for y in range(280, 230, -1):
    row = blue[y, px0+8:px1-8]
    if row.mean() > 0.7:
        print("FFN bottom row:", y, tuple(img[y, 400])); break
fx0 = next(x for x in range(px0+8, 200) if blue[205:255, x].mean() > 0.6)
fx1 = next(x for x in range(px1-8, 700, -1) if blue[205:255, x].mean() > 0.6)
print(f"FFN cols: {fx0}..{fx1} -> slide x {sx_(fx0):.1f}..{sx_(fx1):.1f}")
# FFN title ink (blue) rows inside box top
seg = blue[202:225, fx0+5:fx1-5]
rows = np.where(seg.sum(axis=1) > 6)[0]
if len(rows):
    cs = np.where(seg.any(axis=0))[0]
    band("FFN title ink", cs.min()+fx0+5, cs.max()+fx0+5, rows.min()+202, rows.max()+202)
# red RELU ink inside FFN box
seg = red[202:258, fx0+5:fx1-5]
rows = np.where(seg.sum(axis=1) > 3)[0]
print("FFN red(RELU) ink bands y:", [(a+202, b+202) for a, b in to_bands(rows)] if len(rows) else "none")
# green dots inside FFN box
grn = (G > 120) & (R < 110) & (B < 130) & (G - R > 40)
seg = grn[202:258, fx0+5:fx1-5]
rows = np.where(seg.sum(axis=1) > 3)[0]
print("FFN green ink bands y:", [(a+202, b+202) for a, b in to_bands(rows)] if len(rows) else "none")
# blue ellipsis dots inside FFN box (blue ink not border rows)
seg = blue[210:255, fx0+10:fx1-10]
cols = np.where(seg.sum(axis=0) > 2)[0]
if len(cols):
    cl = to_bands(cols)
    print("FFN blue col clusters (frame x):", [(a+fx0+10, b+fx0+10) for a, b in cl][:20])

# ---------- vector strips: sample one strip's cross-section ----------
# top row band frame y 168..182; first column strip left edge ~?
# find pink cells in the top band
pinkish = (R > 200) & (np.abs(G - 170) < 45) & (np.abs(B - 180) < 45)
seg = pinkish[165:186, 150:880]
cols = np.where(seg.sum(axis=0) > 2)[0]
cl = to_bands(cols)
print("top-row pink col clusters (frame x):", [(a+150, b+150) for a, b in cl][:20])
c0 = cl[0][0] + 150
print(f"first strip left edge frame x {c0} -> slide {sx_(c0):.1f}")
print("strip cross-section (x=c0..c0+52, y=170..184) sampled every 4px:")
for x in range(c0 - 2, c0 + 54, 4):
    colpx = [tuple(img[y, x]) for y in range(168, 184, 3)]
    print(f"  x={x}: {colpx}")
print("strip vertical scan at x=c0+20, y 160..195:")
for y in range(160, 196, 2):
    print(f"  y={y}: {tuple(img[y, c0+20])}")

# dark-red label ink around strips (990000)
dred = (R > 110) & (R < 200) & (G < 60) & (B < 60)
for (name, y0, y1) in [("top", 160, 195), ("mid", 266, 300), ("cont", 370, 402), ("X", 474, 505)]:
    seg = dred[y0:y1, 150:880]
    rr = np.where(seg.sum(axis=1) > 3)[0]
    print(f"{name} row dred ink bands y:", [(a+y0, b+y0) for a, b in to_bands(rr)] if len(rr) else "none",
          " x-extent:", (np.where(seg.any(axis=0))[0][[0, -1]] + 150) if len(rr) else "-")

# ---------- plus circles ----------
seg = dred[335:375, 150:880]
rr = np.where(seg.sum(axis=1) > 2)[0]
if len(rr):
    print("plus dred bands y:", [(a+335, b+335) for a, b in to_bands(rr)])
    ymid = (rr.min() + rr.max()) // 2 + 335
    cols = np.where(seg[ymid - 335] > 0)[0]
    cl = to_bands(cols)
    print(f"plus row ymid {ymid} centers frame:", [round((a+b)/2 + 150, 1) for a, b in cl])
    print("plus centers slide:", [round(sx_((a+b)/2 + 150), 1) for a, b in cl])
# center pixel + ring color of first circle
cxp = int(round((cl[0][0] + cl[0][1]) / 2)) + 150
print(f"first plus center pixel ({cxp},{ymid}):", tuple(img[ymid, cxp]),
      " ring:", tuple(img[ymid, cxp - 7]), tuple(img[ymid - 6, cxp]))

# ---------- gray bar + its text ----------
gray = (np.abs(R - 217) < 16) & (np.abs(G - 217) < 16) & (np.abs(B - 217) < 16)
seg = gray[300:345, 100:880]
rr = np.where(seg.sum(axis=1) > 300)[0]
gy0, gy1 = rr.min() + 300, rr.max() + 300
cc = np.where(seg[(rr[len(rr)//2])])[0]
band("gray bar", cc.min()+100, cc.max()+100, gy0, gy1)
# text ink inside gray bar: dark pixels
dark = (R < 150) & (G < 150) & (B < 150)
seg = dark[gy0:gy1+1, 160:880]
rr2 = np.where(seg.sum(axis=1) > 2)[0]
cc2 = np.where(seg.any(axis=0))[0]
if len(rr2):
    band("graybar text ink", cc2.min()+160, cc2.max()+160, rr2.min()+gy0, rr2.max()+gy0)
    # red vs black split
    segred = red[gy0:gy1+1, 160:880]
    ccr = np.where(segred.any(axis=0))[0]
    print("graybar red-text x extent:", (ccr.min()+160, ccr.max()+160) if len(ccr) else "none")

# ---------- green container ----------
# dashed border: green line pixels, look for horizontal runs
grnline = (G > 120) & (R < 120) & (B < 140) & (G - R > 40)
seg = grnline[280:420, 60:900]
rr = np.where(seg.sum(axis=1) > 15)[0]
print("green long-run rows y:", [(a+280, int(seg[a].sum())) for a in rr][:20])
# container fill sample (between plus circles, left of first circle)
print("fill sample (x=160, y=345..400):", [tuple(img[y, 160]) for y in range(345, 400, 10)])
print("fill sample right (x=880, y=345..400):", [tuple(img[y, 880]) for y in range(345, 400, 10)])
# vertical green cols (left/right borders)
cc = np.where(seg.sum(axis=0) > 15)[0]
print("green long-run cols x:", [(a+60, int(seg[:, a].sum())) for a in cc][:20])

# ---------- arrows ----------
# thin red arrows (graybar top -> mid row bottom): red ink in gap zone
def vext(mask, x0, x1, y0, y1, minsum=2, label=""):
    seg = mask[y0:y1, x0:x1]
    rr = np.where(seg.sum(axis=1) > minsum)[0]
    if len(rr):
        cc = np.where(seg.any(axis=0))[0]
        print(f"{label}: y {rr.min()+y0}..{rr.max()+y0} (slide {sy_(rr.min()+y0):.1f}..{sy_(rr.max()+y0):.1f}) x {cc.min()+x0}..{cc.max()+x0}")
    else:
        print(f"{label}: none")
vext(red, 180, 860, 292, 322, 2, "red arrows gap (midrow->graybar)")
vext(blue & (R < 100), 180, 860, 258, 275, 2, "blue arrows gap (FFNbox->midrow)")
vext(red, 180, 860, 183, 200, 2, "red/blue gap (toprow->FFNbox) via red")
vext(grnline, 180, 860, 350, 365, 2, "green arrows gap (plus->graybar)")
vext(grnline, 180, 860, 376, 396, 2, "green arrows gap (contY->plus)")
# navy thin arrows plus->contY
navy = (R < 70) & (G < 70) & (B > 100)
vext(navy, 180, 860, 376, 396, 2, "navy thin arrows (plus->contY)?")
# block arrows zones
vext(navy, 180, 860, 412, 432, 3, "block arrows zone1 (contY->navy)")
vext(navy, 180, 860, 483, 503, 3, "block arrows zone2 (navy->Xrow)")
# orange curves vertical extent (exclude left labels x<150 and caption y>494)
orange = (R > 195) & (G > 115) & (G < 205) & (B < 115)
vext(orange, 150, 880, 340, 494, 2, "orange curves (x150-880)")
vext(orange, 60, 150, 400, 510, 2, "orange left labels zone")

# ---------- caption ----------
yel3 = (R > 220) & (G > 200) & (B < 100)
seg = yel3[490:517, 60:900]
rr = np.where(seg.sum(axis=1) > 20)[0]; cc = np.where(seg.sum(axis=0) > 3)[0]
band("caption highlight", cc.min()+60, cc.max()+60, rr.min()+490, rr.max()+490)
seg2 = red[490:517, 60:900]
rr2 = np.where(seg2.any(axis=1))[0]; cc2 = np.where(seg2.any(axis=0))[0]
if len(rr2):
    band("caption text ink", cc2.min()+60, cc2.max()+60, rr2.min()+490, rr2.max()+490)

# ---------- left labels ----------
# blue: 'Output of Self Attention'; orange: 'Residual Connections'; red: 'Input to Self Attention'
vext(blue, 60, 150, 380, 440, 1, "left label blue")
vext(orange, 60, 150, 420, 480, 1, "left label orange")
vext(red, 60, 150, 460, 515, 1, "left label red")
# per-line bands for each color
for (name, mask, y0, y1) in [("blue", blue, 380, 445), ("orange", orange, 420, 485), ("red", red, 460, 515)]:
    seg = mask[y0:y1, 60:150]
    rr = np.where(seg.sum(axis=1) > 0)[0]
    if len(rr):
        for (a, b) in to_bands(rr):
            cs = np.where(seg[a:b+1].any(axis=0))[0]
            print(f"  {name} line y {a+y0}..{b+y0} (slide {sy_(a+y0):.1f}..{sy_(b+y0):.1f}) x {cs.min()+60}..{cs.max()+60} (slide cx {sx_((cs.min()+cs.max())/2+60):.1f})")

# ---------- ellipsis dots ----------
for (name, y0, y1, mask) in [("topY", 168, 186, blue), ("midY", 272, 292, blue), ("contY", 376, 398, blue), ("Xrow", 478, 500, grnline)]:
    seg = mask[y0:y1, 560:760]
    cc = np.where(seg.sum(axis=0) > 1)[0]
    if len(cc):
        cl = to_bands(cc)
        centers = [round((a+b)/2 + 560, 1) for a, b in cl]
        print(f"{name} dots frame-x centers: {centers} -> slide {[round(sx_(c),1) for c in centers]}")
        rr = np.where(seg.sum(axis=1) > 0)[0]
        print(f"   y extent {rr.min()+y0}..{rr.max()+y0} slide {sy_(rr.min()+y0):.1f}..{sy_(rr.max()+y0):.1f}")
