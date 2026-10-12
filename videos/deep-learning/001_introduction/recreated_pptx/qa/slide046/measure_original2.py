#!/usr/bin/env python3
"""PIL forensics pass 2 — slide_046.jpg. Looser masks, exclude red from dark,
panel edge location, modal colors, font candidate fitting."""
from PIL import Image
import numpy as np
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_046.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)

R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]
redm   = (R > 110) & (R - G > 25) & (R - B > 25)
darkm  = (R+G+B < 400) & ~redm
bluem  = (B - R > 30) & (B - G > 25) & (B > 100)
greenm = (G - R > 40) & (G - B > 40) & (G > 120)
warmm  = (R - B > 45) & (R > 110)          # tiger orange

def modal(seg, mask, label):
    px = seg[mask]
    if len(px) == 0:
        print(f"{label:34s} no px"); return
    c = Counter(map(tuple, px))
    print(f"{label:34s} modal {c.most_common(3)} n={len(px)}")

print("== red structures ==")
# top red line: scan rows 20..60 for red count
for y in range(20, 61):
    n = int(redm[y].sum())
    if n > 5:
        xs = np.nonzero(redm[y])[0]
        print(f"  y={y}: n={n} x {xs.min()}..{xs.max()}")
# left red line: cols 0..80
for x in range(0, 81):
    n = int(redm[:, x].sum())
    if n > 5:
        ys = np.nonzero(redm[:, x])[0]
        print(f"  x={x}: n={n} y {ys.min()}..{ys.max()}")
# panel border: scan a clean row (y=440, below diagram) and col x=780
for y in (120, 125, 130, 131, 132, 133, 134, 135, 440, 455, 456, 457, 458, 460):
    xs = np.nonzero(redm[y])[0]
    if len(xs) > 3:
        print(f"  row y={y}: red x {xs.min()}..{xs.max()} n={len(xs)}")
for x in (60, 62, 63, 64, 66, 895, 898, 900, 902, 905):
    ys = np.nonzero(redm[:, x])[0]
    if len(ys) > 3:
        print(f"  col x={x}: red y {ys.min()}..{ys.max()} n={len(ys)}")
modal(a[133], redm[133], "panel top border color")

print("== panel fill vs canvas ==")
modal(a[430:445, 340:620], np.ones((15, 280), bool), "panel fill (y430-445 x340-620)")
modal(a[470:500, 340:620], np.ones((30, 280), bool), "below panel (y470-500)")
modal(a[20:40, 340:620], np.ones((20, 280), bool), "above panel y20-40")
modal(a[200:220, 930:960], np.ones((20, 30), bool), "right margin x930-960")
modal(a[200:220, 5:30], np.ones((20, 25), bool), "left margin x5-30")
# luminance col profile at y=470 (find panel right edge), y=100
for yy in (100, 470):
    row = a[yy]
    lum = row.sum(axis=1)
    trans = [x for x in range(1, W) if abs(int(lum[x]) - int(lum[x-1])) > 24]
    print(f"  y={yy} luminance transitions x: {trans[:20]}")
col = a[:, 480]
lum = col.sum(axis=1)
trans = [y for y in range(1, H) if abs(int(lum[y]) - int(lum[y-1])) > 24]
print(f"  x=480 luminance transitions y: {trans[:24]}")

print("== title ==")
seg = a[60:130, 300:700]
ys, xs = np.nonzero(redm[60:130, 300:700])
print(f"  title red ink x {300+xs.min()}..{300+xs.max()} y {60+ys.min()}..{60+ys.max()}")
modal(a[60:130, 300:700], redm[60:130, 300:700], "  title color")

print("== bullet lines (dark, red-excluded), x 100..800, y 140..240 ==")
sub = darkm[140:245, 100:800]
rows = sub.sum(axis=1)
run = None
for i, v in enumerate(rows):
    y = 140 + i
    if v > 0 and run is None: run = y
    elif v == 0 and run is not None:
        seg = a[run:y, 100:800]
        mm = darkm[run:y, 100:800]
        ys2, xs2 = np.nonzero(mm)
        print(f"  line y {run}..{y-1} h={y-run}  x {100+xs2.min()}..{100+xs2.max()}  n={int(mm.sum())}")
        run = None
if run is not None:
    seg = a[run:245, 100:800]; mm = darkm[run:245, 100:800]
    ys2, xs2 = np.nonzero(mm)
    print(f"  line y {run}..244 (open)  x {100+xs2.min()}..{100+xs2.max()}")

print("== bullet markers ==")
for (y0, y1, lbl) in [(150, 175, "main"), (178, 195, "sub1"), (198, 216, "sub2"), (220, 240, "sub3")]:
    seg = darkm[y0:y1, 100:150]
    ys2, xs2 = np.nonzero(seg)
    if len(xs2):
        print(f"  {lbl}: x {100+xs2.min()}..{100+xs2.max()} y {y0+ys2.min()}..{y0+ys2.max()} n={len(xs2)}")
    else:
        print(f"  {lbl}: none")
modal(a[150:175, 100:800], darkm[150:175, 100:800], "main bullet text color")
modal(a[178:240, 150:800], darkm[178:240, 150:800], "sub text color")

print("== option boxes ==")
for (y0, y1, lbl) in [(240, 285, "box1"), (278, 320, "box2")]:
    seg = bluem[y0:y1, 95:330]
    ys2, xs2 = np.nonzero(seg)
    if len(xs2):
        print(f"  {lbl} blue ink x {95+xs2.min()}..{95+xs2.max()} y {y0+ys2.min()}..{y0+ys2.max()} n={len(xs2)}")
modal(a[245:285, 100:300], bluem[245:285, 100:300], "box1 border color modal")
# box interior fill
modal(a[258:268, 240:290], np.ones((10,50), bool), "box1 interior fill")
modal(a[292:302, 240:290], np.ones((10,50), bool), "box2 interior fill")
# text inside boxes (dark)
seg = darkm[248:280, 115:300]; ys2, xs2 = np.nonzero(seg)
print(f"  box1 text ink x {115+xs2.min()}..{115+xs2.max()} y {248+ys2.min()}..{248+ys2.max()}")
seg = darkm[283:315, 115:300]; ys2, xs2 = np.nonzero(seg)
print(f"  box2 text ink x {115+xs2.min()}..{115+xs2.max()} y {283+ys2.min()}..{283+ys2.max()}")

print("== diagram ==")
seg = greenm[320:430, 150:280]; ys2, xs2 = np.nonzero(seg)
print(f"  matrix green x {150+xs2.min()}..{150+xs2.max()} y {320+ys2.min()}..{320+ys2.max()}")
modal(a[336:399, 172:242], greenm[336:399, 172:242], "  matrix green fill")
# black grid lines inside matrix: dark ink between cells
seg = darkm[330:405, 165:250]; ys2, xs2 = np.nonzero(seg)
print(f"  matrix dark border ink x {165+xs2.min()}..{165+xs2.max()} y {330+ys2.min()}..{330+ys2.max()}")
# cell letters: dark ink INSIDE green cells
modal(a[336:368, 172:208], darkm[336:368, 172:208], "  cell-a letter color")
# arrow bbox (dark outline)
seg = darkm[340:410, 250:320]; ys2, xs2 = np.nonzero(seg)
print(f"  arrow ink x {250+xs2.min()}..{250+xs2.max()} y {340+ys2.min()}..{340+ys2.max()}")
# arrow interior fill (center)
modal(a[360:375, 280:300], np.ones((15,20), bool), "  arrow interior")
# z square
seg = greenm[340:410, 305:365]; ys2, xs2 = np.nonzero(seg)
print(f"  z square x {305+xs2.min()}..{305+xs2.max()} y {340+ys2.min()}..{340+ys2.max()}")
modal(a[352:383, 314:348], darkm[352:383, 314:348], "  z letter color")
# Pool ( text
seg = darkm[340:410, 358:435]; ys2, xs2 = np.nonzero(seg)
print(f"  'Pool (' ink x {358+xs2.min()}..{358+xs2.max()} y {340+ys2.min()}..{340+ys2.max()}")
modal(a[340:410, 358:435], darkm[340:410, 358:435], "  Pool text color")
# large tiger: photo rectangle = non-white non-panel block; use 'not near-white'
notwhite = (R+G+B < 690)
seg = notwhite[315:425, 420:625]
ys2, xs2 = np.nonzero(seg)
print(f"  large tiger block x {420+xs2.min()}..{420+xs2.max()} y {315+ys2.min()}..{315+ys2.max()}")
# ')' '==' between photos
seg = darkm[340:400, 595:665]; ys2, xs2 = np.nonzero(seg)
print(f"  ') ==' ink x {595+xs2.min()}..{595+xs2.max()} y {340+ys2.min()}..{340+ys2.max()}")
# small tiger
seg = notwhite[335:395, 660:790]
ys2, xs2 = np.nonzero(seg)
print(f"  small tiger block x {660+xs2.min()}..{660+xs2.max()} y {335+ys2.min()}..{335+ys2.max()}")
# caption
seg = bluem[390:420, 640:800]; ys2, xs2 = np.nonzero(seg)
print(f"  caption ink x {640+xs2.min()}..{640+xs2.max()} y {390+ys2.min()}..{390+ys2.max()}")
modal(a[390:420, 640:800], bluem[390:420, 640:800], "  caption color")

print("== bottom strip ==")
for y in (515, 518, 520, 522):
    dk = np.nonzero(a[y].sum(axis=1) < 150)[0]
    print(f"  y={y}: n={len(dk)}", (int(dk.min()), int(dk.max())) if len(dk) else "")
