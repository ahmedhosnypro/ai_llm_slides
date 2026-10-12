#!/usr/bin/env python3
"""Slide 045 — refined probes (038-consistent mapping: SX=0.962329 OX=17.582 SY=0.955556 OY=0)."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
F38 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
img38 = np.asarray(Image.open(F38).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
SX, OX, SY, OY = 0.962329, 17.582, 0.955556, 0.0
def sx_(fx): return (fx - OX) / SX
def sy_(fy): return (fy - OY) / SY
def P(name, fx0, fx1, fy0, fy1):
    print(f"{name}: frame x {fx0}..{fx1} y {fy0}..{fy1} -> slide x {sx_(fx0):.1f}..{sx_(fx1):.1f} y {sy_(fy0):.1f}..{sy_(fy1):.1f}")

def to_bands(ys, gap=2):
    if len(ys) == 0: return []
    b = []; s = ys[0]; p = ys[0]
    for v in ys[1:]:
        if v > p + gap: b.append((s, p)); s = v
        p = v
    b.append((s, p)); return b

print("== 1. annot box bottom border probe (rows 144..162, frac of blue in x 95..870) ==")
blue = (B > 110) & (R < 110) & (G < 110)
for y in range(144, 163):
    print(f"  y={y} frac={blue[y, 95:870].mean():.2f}", tuple(img[y, 300]), tuple(img[y, 700]))

print("== 2. annot per-line blue x-extents + loose-red ==")
for (a, b, label) in [(88, 103, "line1"), (109, 124, "line2"), (130, 145, "line3")]:
    seg = blue[a:b+1, 95:870]
    cc = np.where(seg.any(axis=0))[0]
    if len(cc): P(f"  {label} blue ink", cc.min()+95, cc.max()+95, a, b)
# loose red-orange on the yellow fill: R>150, R-G>40, R-B>40
loosered = (R > 150) & (R - G > 40) & (R - B > 40)
for (a, b, label) in [(88, 103, "line1"), (109, 124, "line2"), (130, 145, "line3")]:
    seg = loosered[a:b+1, 95:870]
    cc = np.where(seg.any(axis=0))[0]
    rr = np.where(seg.any(axis=1))[0]
    if len(cc): P(f"  {label} red-ish ink", cc.min()+95, cc.max()+95, rr.min()+a, rr.max()+a)
    else: print(f"  {label} red-ish: none")

print("== 3. panel bottom rows (blue frac x 70..890, y 505..518) ==")
for y in range(505, 519):
    print(f"  y={y} frac={blue[y, 70:890].mean():.2f}")

print("== 4. strip anatomy: median column colors, rows top/mid/cont/X vs 038's strips ==")
def strip_anatomy(im, name, fx0, fx1, fy0, fy1):
    sub = im[fy0:fy1+1, fx0:fx1+1]
    med = np.median(sub, axis=0).astype(int)
    # find cell boundaries: columns where color changes a lot
    print(f"  {name} strip frame x {fx0}..{fx1} y {fy0}..{fy1} (w={fx1-fx0+1})")
    print("   med RGB every 3px:", [f"{x+fx0}:({med[x][0]},{med[x][1]},{med[x][2]})" for x in range(0, len(med), 3)])
# 045 rows (frame y): top 168..182, mid 274..288, cont 378..394, X 481..496; first strip left 199
strip_anatomy(img, "045 top/s1", 197, 248, 168, 183)
strip_anatomy(img, "045 mid/s1", 197, 248, 273, 289)
strip_anatomy(img, "045 cont/s1", 197, 248, 377, 395)
strip_anatomy(img, "045 X/s1", 197, 248, 480, 497)
# 038 strips: cols slide [194.9...] barW50 -> frame bar1 x 181..229, rows: top 272.1 h17.8 -> frame 260..277
# (038 mapping: frame = 18.63 + 0.96123*sx ; sy 0.95556)
strip_anatomy(img38, "038 top/s1", 180, 230, 260, 278)
strip_anatomy(img38, "038 mid/s1", 180, 230, 366, 383)
strip_anatomy(img38, "038 X/s1", 180, 230, 469, 486)

print("== 5. plus circle 1: bbox + colors ==")
dredloose = (R < 210) & (R - G > 70) & (R - B > 70)
seg = dredloose[340:370, 195:235]
rr = np.where(seg.any(axis=1))[0]; cc = np.where(seg.any(axis=0))[0]
y0, y1, x0, x1 = rr.min()+340, rr.max()+340, cc.min()+195, cc.max()+195
P("plus1 dredloose bbox", x0, x1, y0, y1)
print(f"  d_frame = {x1-x0+1}x{y1-y0+1} -> slide d = {(x1-x0+1)/SX:.1f} x {(y1-y0+1)/SY:.1f}; center slide ({sx_((x0+x1)/2):.1f},{sy_((y0+y1)/2):.1f})")
cy = (y0+y1)//2; cx = (x0+x1)//2
print("  center px:", tuple(img[cy, cx]), " cross y (x=cx):", [(y, tuple(img[y, cx])) for y in range(y0, y1+1, 2)])
# white plus glyph bbox inside
white = (R > 230) & (G > 230) & (B > 230)
seg2 = white[y0:y1+1, x0:x1+1]
rr2 = np.where(seg2.any(axis=1))[0]; cc2 = np.where(seg2.any(axis=0))[0]
if len(rr2): print(f"  white + glyph: y {rr2.min()+y0}..{rr2.max()+y0} x {cc2.min()+x0}..{cc2.max()+x0}")

print("== 6. container borders ==")
grn = (G > 120) & (R < 130) & (B < 150) & (G - R > 35)
for y in range(293, 302):
    print(f"  top y={y} grnfrac x80..900={grn[y, 80:900].mean():.2f}")
for y in range(368, 380):
    print(f"  bot y={y} grnfrac={grn[y, 80:900].mean():.2f}")
for x in range(70, 150):
    f_ = grn[300:370, x].mean()
    if f_ > 0.1: print(f"  left col x={x} frac={f_:.2f}")
for x in range(895, 870, -1):
    f_ = grn[300:370, x].mean()
    if f_ > 0.1: print(f"  right col x={x} frac={f_:.2f}"); break
print("  fill median inside (x 150..170, y 340..370):", np.median(img[340:370, 150:170].reshape(-1,3), axis=0))
print("  fill right (x 868..884, y 340..370):", np.median(img[340:370, 868:884].reshape(-1,3), axis=0))

print("== 7. arrows, correct zones ==")
def vext(mask, x0, x1, y0, y1, minsum, label):
    seg = mask[y0:y1, x0:x1]
    rr = np.where(seg.sum(axis=1) > minsum)[0]
    if len(rr):
        cc = np.where(seg.any(axis=0))[0]
        print(f"  {label}: y {rr.min()+y0}..{rr.max()+y0} (slide {sy_(rr.min()+y0):.1f}..{sy_(rr.max()+y0):.1f}) x {cc.min()+x0}..{cc.max()+x0}")
    else: print(f"  {label}: none")
navy = (R < 70) & (G < 70) & (B > 100)
red = (R > 140) & (G < 80) & (B < 80)
vext(red, 190, 850, 289, 307, 2, "red thin (midrow->graybar)")
vext(blue & (R < 100), 190, 850, 259, 272, 2, "blue thin (FFNbox->midrow)")
vext(blue & (R < 100), 190, 850, 183, 199, 2, "blue thin (toprow->FFNbox)?")
vext(red, 190, 850, 183, 199, 2, "red thin (toprow->FFNbox)?")
vext(grn, 190, 850, 336, 346, 2, "green thin (plus->graybar)")
vext(grn, 190, 850, 361, 377, 2, "green thin (contY->plus)?")
vext(navy, 190, 850, 361, 377, 2, "navy thin (contY->plus)?")
vext(navy, 190, 850, 396, 412, 3, "block arrows (contY->navy)")
vext(navy, 190, 850, 463, 480, 3, "block arrows (navy->Xrow)")
# sample arrow pixel colors mid-gap at col1 center x=206
for (label, yy) in [("gapA plus->graybar", 341), ("gapB contY->plus", 369), ("gap midrow->graybar", 298), ("gap FFN->midrow", 265), ("gap top->FFN", 191), ("blk1", 403), ("blk2", 471)]:
    print(f"  {label} y={yy} col x=200..212:", [tuple(img[yy, x]) for x in range(200, 213, 3)])

print("== 8. caption text (red ink y 498..515, x 250..580) vs 038 ==")
seg = red[498:516, 250:580]
rr = np.where(seg.any(axis=1))[0]; cc = np.where(seg.any(axis=0))[0]
if len(rr): P("045 caption ink", cc.min()+250, cc.max()+250, rr.min()+498, rr.max()+498)
R38, G38, B38 = img38[:, :, 0], img38[:, :, 1], img38[:, :, 2]
red38 = (R38 > 140) & (G38 < 80) & (B38 < 80)
# 038 caption: slide capTop 519.1 -> frame ~496..510, x hl 263.6..558 -> frame 272..555
seg = red38[494:514, 250:580]
rr = np.where(seg.any(axis=1))[0]; cc = np.where(seg.any(axis=0))[0]
if len(rr): print(f"  038 caption ink: frame x {cc.min()+250}..{cc.max()+250} y {rr.min()+494}..{rr.max()+494}")

print("== 9. FFN icons: tile boundaries ==")
# blue-ish tile borders inside FFN box y 218..256
seg = blue[218:257, 168:880]
cc = np.where(seg.sum(axis=0) > 1)[0]
cl = to_bands(cc, gap=3)
print("  blue col clusters x:", [(a+168, b+168) for a, b in cl])
# green dots rows
grn2 = (G > 120) & (R < 130) & (B < 150) & (G - R > 35)
seg = grn2[205:258, 168:880]
rr = np.where(seg.any(axis=1))[0]
print("  green ink rows y:", [(a+205, b+205) for a, b in to_bands(rr, gap=2)])
# pink fan rows (F4B8C4-ish loose)
pinkl = (R > 200) & (np.abs(G - 165) < 55) & (np.abs(B - 175) < 55) & (R - G > 30)
seg = pinkl[205:258, 168:880]
rr = np.where(seg.any(axis=1))[0]
print("  pink ink rows y:", [(a+205, b+205) for a, b in to_bands(rr, gap=2)])
# loose red (RELU) rows
seg = loosered[205:258, 168:880]
rr = np.where(seg.any(axis=1))[0]
print("  loosered ink rows y:", [(a+205, b+205) for a, b in to_bands(rr, gap=2)])
if len(rr):
    for (a, b) in to_bands(rr, gap=2)[:4]:
        cc2 = np.where(loosered[a+205:b+206, 168:880].any(axis=0))[0]
        print(f"    loosered band y{a+205}..{b+205}: x clusters", [(u+168, v+168) for u, v in to_bands(cc2, gap=6)])

print("== 10. left labels fine bands ==")
for (name, mask, y0, y1) in [("blue", blue, 375, 410), ("orange", (R > 195) & (G > 115) & (G < 205) & (B < 115), 420, 455), ("red", red, 460, 495)]:
    seg = mask[y0:y1, 60:152]
    rr = np.where(seg.sum(axis=1) > 0)[0]
    for (a, b) in to_bands(rr, gap=1):
        cs = np.where(seg[a:b+1].any(axis=0))[0]
        print(f"  {name} line y {a+y0}..{b+y0} (slide {sy_(a+y0):.1f}..{sy_(b+y0):.1f}) x {cs.min()+60}..{cs.max()+60} (cx {sx_((cs.min()+cs.max())/2+60):.1f})")

print("== 11. orange curves: x clusters at rows 356,380,420,450,476 ==")
orange = (R > 195) & (G > 115) & (G < 205) & (B < 115)
for yy in [356, 380, 420, 450, 476]:
    cc = np.where(orange[yy, 150:880])[0]
    cl = to_bands(cc, gap=8)
    print(f"  y={yy}:", [round((a+b)/2+150, 1) for a, b in cl])

print("== 12. strip label widths cols 1,7,8 (mid row) ==")
dred = (R > 110) & (R < 200) & (G < 60) & (B < 60)
# mid row strip centers (frame): ~223, 294, 366, 438, 511, 583, 760(?), 833 -> from 038 cols
for i, cx in enumerate([206, 278, 351, 425, 499, 571, 761, 834], 1):
    seg = dred[270:302, cx-20:cx+20]
    rr = np.where(seg.any(axis=1))[0]
    cc = np.where(seg.any(axis=0))[0]
    if len(cc):
        print(f"  col{i} (frame cx {cx}): label ink x {cc.min()+cx-20}..{cc.max()+cx-20} (w={cc.max()-cc.min()+1}) y {rr.min()+270}..{rr.max()+270}")
