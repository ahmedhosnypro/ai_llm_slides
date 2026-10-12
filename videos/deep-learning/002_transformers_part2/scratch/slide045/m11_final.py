#!/usr/bin/env python3
"""Slide 045 — final measurements (m11): FFN tiles/dots/RELU, annot line structure, dot colors."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
SX, OX, SY = 0.962329, 17.582, 0.955556
def sx_(fx): return (fx - OX) / SX
def sy_(fy): return fy / SY

def to_bands(ys, gap):
    if len(ys) == 0: return []
    b = []; s = ys[0]; p = ys[0]
    for v in ys[1:]:
        if v > p + gap: b.append((s, p)); s = v
        p = v
    b.append((s, p)); return b

print("== 1. tile x-extents: cream fill runs at row 227 (x 165..885) ==")
cream = (np.abs(R - 240) < 22) & (np.abs(G - 232) < 30) & (np.abs(B - 197) < 35) & (R - B > 25)
row = cream[227, 165:885]
cc = np.where(row)[0]
bands = to_bands(cc, 4)
print("  cream runs:", [(a+165, b+165) for a, b in bands])
print("  -> slide:", [(round(sx_(a+165),1), round(sx_(b+165),1)) for a, b in bands])

print("== 2. tile fill + border colors ==")
print("  fill median (x 180..232, y 225..227):", np.median(img[225:228, 180:232].reshape(-1,3), axis=0))
print("  bottom border row 250..252 sample x=200:", [tuple(img[y,200]) for y in range(249,253)])
print("  left border col? sample x 172..178 at y=237:", [tuple(img[237,x]) for x in range(170,180)])
print("  top border? y 222..224 at x=200:", [tuple(img[y,200]) for y in range(221,225)])

print("== 3. green dots per tile (y 227..235) ==")
grn = (G > 130) & (R < 140) & (G - R > 40) & (G - B > 10)
seg = grn[227:236, 165:885]
cc = np.where(seg.sum(axis=0) > 1)[0]
bands = to_bands(cc, 3)
print("  green blob x-bands:", [(a+165, b+165) for a, b in bands])
rr = np.where(seg.sum(axis=1) > 3)[0]
print("  green y extent:", rr.min()+227, rr.max()+227)

print("== 4. purple dots per tile (y 239..247) ==")
pur = (R > 130) & (B > 130) & (R - G > 40) & (B - G > 30)
seg = pur[239:248, 165:885]
cc = np.where(seg.sum(axis=0) > 1)[0]
bands = to_bands(cc, 2)
print(f"  purple blob count: {len(bands)}")
print("  bands:", [(a+165, b+165) for a, b in bands])
rr = np.where(seg.sum(axis=1) > 3)[0]
print("  purple y extent:", rr.min()+239, rr.max()+239)

print("== 5. fan line color (y 234..239, non-cream non-green) ==")
for (x, y) in [(203, 236), (207, 237), (211, 238), (258, 236), (280, 237)]:
    print(f"  ({x},{y}):", tuple(img[y, x]))

print("== 6. RELU red text bbox per tile (y 225..235, x half-right) ==")
redl = (R > 150) & (R - G > 60) & (R - B > 60)
seg = redl[224:236, 165:885]
cc = np.where(seg.sum(axis=0) > 0)[0]
bands = to_bands(cc, 6)
print("  red text x-bands:", [(a+165, b+165) for a, b in bands])
rr = np.where(seg.sum(axis=1) > 0)[0]
if len(rr): print("  red text y extent:", rr.min()+224, rr.max()+224)

print("== 7. blue ellipsis dots inside FFN box (x 610..715, y 215..255) ==")
bl = (B > 110) & (R < 110) & (G < 110)
seg = bl[215:255, 610:715]
cc = np.where(seg.sum(axis=0) > 1)[0]
bands = to_bands(cc, 3)
print("  blue x-bands:", [(a+610, b+610) for a, b in bands])
rr = np.where(seg.sum(axis=1) > 1)[0]
if len(rr): print("  blue y extent:", rr.min()+215, rr.max()+215, "-> slide", round(sy_(rr.min()+215),1), round(sy_(rr.max()+215),1))

print("== 8. annot lines 2/3 cluster structure (gap>10) ==")
blue = (B > 110) & (R < 110) & (G < 110)
for (label, y0, y1) in [("line2", 108, 126), ("line3", 129, 147)]:
    seg = blue[y0:y1, 95:870]
    cc = np.where(seg.sum(axis=0) > 0)[0]
    bands = to_bands(cc, 10)
    print(f"  {label} word-clusters:", [(a+95, b+95) for a, b in bands])

print("== 9. strip dot core color (topY dot1 at 626..632, 172..178) ==")
sub = img[172:179, 626:633].reshape(-1, 3)
dark = sub[(sub[:, 2] > 100) & (sub[:, 0] < 110)]
print("  blue-ish px median:", np.median(dark, axis=0) if len(dark) else "none", "n=", len(dark))
print("  Xrow dot core (626..633, 486..492):", np.median(img[486:493, 626:633].reshape(-1,3), axis=0))

print("== 10. box fill away from ink ==")
print("  (x 300..360, y 219..222):", np.median(img[219:223, 300:360].reshape(-1,3), axis=0))
print("  (x 800..860, y 219..222):", np.median(img[219:223, 800:860].reshape(-1,3), axis=0))

print("== 11. FFN box border cols/rows exact ==")
for x in range(160, 170):
    col = bl[210:250, x]
    if col.mean() > 0.5: print("  FFN left border col:", x, tuple(img[230, x])); break
for x in range(888, 878, -1):
    col = bl[210:250, x]
    if col.mean() > 0.5: print("  FFN right border col:", x, tuple(img[230, x])); break
for y in range(197, 204):
    rowm = bl[y, 170:880]
    if rowm.mean() > 0.5: print("  FFN top border row:", y, tuple(img[y, 400]))
for y in range(261, 254, -1):
    rowm = bl[y, 170:880]
    if rowm.mean() > 0.5: print("  FFN bottom border row:", y, tuple(img[y, 400]))

print("== 12. navy block exact cols (row 440) ==")
navy = (R < 70) & (G < 70) & (B > 100)
row = navy[440, 60:900]
cc = np.where(row)[0]
print("  navy row 440 x:", cc.min()+60, "..", cc.max()+60, "-> slide", round(sx_(cc.min()+60),1), round(sx_(cc.max()+60),1))

print("== 13. gray bar rows exact (col 400) ==")
for y in range(304, 340):
    px = img[y, 400]
    if abs(px[0]-217)<20 and abs(px[1]-217)<20 and abs(px[2]-217)<20:
        print("  gray first row:", y); break
for y in range(340, 304, -1):
    px = img[y, 400]
    if abs(px[0]-217)<20 and abs(px[1]-217)<20 and abs(px[2]-217)<20:
        print("  gray last row:", y); break
