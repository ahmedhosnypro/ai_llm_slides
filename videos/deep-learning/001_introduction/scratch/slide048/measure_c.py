#!/usr/bin/env python3
"""Pass C: targeted pixel probes for slide_048 geometry open questions."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_048.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def reddish(sub):
    rr, gg, bb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    return (rr > 130) & (rr - gg > 40) & (rr - bb > 40)

def runs(idx, gap=2):
    out = []; s = p = None
    for i in idx:
        if s is None: s = p = i
        elif i <= p + gap: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

print("== 1. top border probe: rows 38..56, reddish count across x 55..900 ==")
for y in range(38, 57):
    m = reddish(im[y:y+1, 55:900])
    n = m.sum()
    if n:
        xs = np.where(m[0])[0] + 55
        print(f"  y={y}: n={n} x {xs.min()}..{xs.max()}")

print("== 2. right border probe: cols 886..900, rows 50..140 reddish per row ==")
for y in range(50, 141):
    m = reddish(im[y:y+1, 886:901])
    n = m.sum()
    if n >= 2:
        xs = np.where(m[0])[0] + 886
        print(f"  y={y}: n={n} x {xs.min()}..{xs.max()}")

print("== 3. bottom line probe rows 443..453: reddish runs per row (x 55..900) ==")
for y in range(443, 454):
    m = reddish(im[y:y+1, 55:900])
    xs = np.where(m[0])[0]
    if len(xs):
        rr = runs(list(xs), gap=4)
        print(f"  y={y}: n={len(xs)} runs {rr[:8]}{'...' if len(rr)>8 else ''} (last {rr[-1] if rr else ''})")

print("== 4. left border bottom col 55..62 rows 445..520 reddish ==")
for y in range(445, 521):
    m = reddish(im[y:y+1, 55:63])
    n = m.sum()
    if n:
        xs = np.where(m[0])[0] + 55
        print(f"  y={y}: n={n} x {xs.min()}..{xs.max()}")

print("== 5. arrow shaft rows 452..470, x 55..845: reddish runs (loose) ==")
rr_, gg_, bb_ = r, g, b
loose = (rr_ > 150) & (rr_ - gg_ > 25) & (rr_ - bb_ > 25)
for y in range(452, 471):
    xs = np.where(loose[y, 55:845])[0]
    if len(xs):
        print(f"  y={y}: n={len(xs)} x {xs.min()+55}..{xs.max()+55}")

print("== 6. Conv labels: reddish pixels y 288..315, x 220..310 and x 465..550 ==")
for (x0, x1, tag) in [(220, 310, 'slab1'), (465, 550, 'slab4')]:
    sub = loose[288:316, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  {tag}: n={len(ys)} x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+288}..{ys.max()+288}")
    else:
        print(f"  {tag}: none")

print("== 7. divider pattern row 267..270 runs min gap=1 ==")
for y in range(266, 272):
    xs = np.where(reddish(im[y:y+1, 55:900]))[0]
    if len(xs):
        rr = runs(list(xs), gap=1)
        print(f"  y={y}: n={len(xs)} ndashes={len(rr)} first5 {rr[:5]} widths {[e-s+1 for s,e in rr[:10]]}")

print("== 8. pink band grid y 214..227 x 380..455 (every 2px) ==")
for y in range(214, 228, 2):
    row = []
    for x in range(380, 456, 6):
        px = im[y, x]
        row.append(f"{x}:{px[0]},{px[1]},{px[2]}")
    print("  " + " ".join(row))

print("== 9. photos: non-background masks ==")
# background: white or panel gray E9E9E7 (within tol)
bg = ((r > 215) & (g > 215) & (b > 215)) | ((abs(r-233) < 14) & (abs(g-233) < 14) & (abs(b-231) < 16))
def photo_bbox(x0, x1, y0, y1, name):
    sub = ~bg[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  {name}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
photo_bbox(230, 380, 180, 265, "cat meme region")
photo_bbox(115, 220, 305, 425, "siamese region")

print("== 10. white text in NN block1 (449..476,186..256) rows ==")
sub = im[186:257, 450:476]
wt = (sub[:, :, 0] > 190) & (sub[:, :, 1] > 190) & (sub[:, :, 2] > 190)
ys, xs = np.where(wt)
print(f"  white n={len(ys)} y {ys.min()+186}..{ys.max()+186} x {xs.min()+450}..{xs.max()+450}")
rowsum = wt.sum(axis=1)
bands = runs(list(np.where(rowsum > 0)[0]), gap=2)
print(f"  white bands (y+186): {[(s+186, e+186) for s, e in bands]}")

print("== 11. slab1 skew: orange x-extent at y=316, y=370, y=424 ==")
orange = (r > 150) & (g > 80) & (g < 180) & (b < 90) & (r - b > 90)
for y in (316, 340, 370, 400, 424):
    xs = np.where(orange[y, 220:300])[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()+220}..{xs.max()+220}")

print("== 12. label boxes blue border thickness/corners: box1 (242..379,155..182) ==")
blue = (b - r > 40) & (b - g > 30) & (b > 110)
for y in (155, 156, 157, 168, 181, 182):
    xs = np.where(blue[y, 235:390])[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()+235}..{xs.max()+235} n={len(xs)}")

print("== 13. panel gray samples ==")
for (x, y, tag) in [(100, 200, 'inside frame'), (30, 270, 'left of frame'), (480, 30, 'above frame'),
                    (480, 470, 'below box'), (480, 500, 'lower'), (930, 270, 'right of frame'),
                    (70, 60, 'top-left inside'), (850, 430, 'bottom-right inside')]:
    print(f"  ({x},{y}) {tag}: {tuple(im[y, x])}")

print("== 14. black strip rows ==")
dark = (r < 60) & (g < 60) & (b < 60)
for y in (516, 518, 519, 520, 539):
    xs = np.where(dark[y, :])[0]
    print(f"  y={y}: n={len(xs)} {'x %d..%d' % (xs.min(), xs.max()) if len(xs) else ''}")

print("== 15. Non Linearity: blue comps y 408..445 x 250..660 ==")
from scipy import ndimage
lab, n = ndimage.label(blue[408:446, 250:660])
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) >= 6:
        print(f"  comp: x {xs.min()+250}..{xs.max()+250} y {ys.min()+408}..{ys.max()+408} n={len(ys)}")

print("== 16. tag red text rows: x 387..422 y 155..185 ==")
sub = reddish(im[155:186, 387:423])
ys, xs = np.where(sub)
if len(ys):
    print(f"  red n={len(ys)} y {ys.min()+155}..{ys.max()+155} x {xs.min()+387}..{xs.max()+387}")
    rowsum = sub.sum(axis=1)
    print(f"  per-row: {[int(v) for v in rowsum]}")

print("== 17. caption full extent incl washed: loose red y 465..482 x 55..900 ==")
ys, xs = np.where(loose[465:483, 55:900])
print(f"  n={len(ys)} x {xs.min()+55}..{xs.max()+55} y {ys.min()+465}..{ys.max()+465}")

print("== 18. arrows between NN blocks: dark pixels y 215..230 x 477..500 ==")
darkish = (r < 120) & (g < 120) & (b < 120)
for (x0, x1, tag) in [(477, 497, 'NN b1-b2'), (524, 544, 'NN b2-b3'), (666, 685, 'NN b5-Loss'),
                      (289, 310, 'CNN s1-s2'), (695, 734, 'CNN s6-L5')]:
    sub = darkish[205:245, x0:x1]
    ys, xs = np.where(sub)
    if len(ys):
        print(f"  {tag}: n={len(ys)} x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+205}..{ys.max()+205}")
    else:
        print(f"  {tag}: none")
