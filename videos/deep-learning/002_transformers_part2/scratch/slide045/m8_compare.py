#!/usr/bin/env python3
"""Slide 045 vs 038 — decisive comparisons (m8)."""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_045.jpg"
F38 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_038.jpg"
img = np.asarray(Image.open(F).convert("RGB")).astype(int)
img38 = np.asarray(Image.open(F38).convert("RGB")).astype(int)
R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
R38, G38, B38 = img38[:, :, 0], img38[:, :, 1], img38[:, :, 2]

print("== 1. pink-band heights, same mask, both frames ==")
pinkm = (R > 200) & (np.abs(G - 170) < 45) & (np.abs(B - 180) < 45)
pinkm38 = (R38 > 200) & (np.abs(G38 - 170) < 45) & (np.abs(B38 - 180) < 45)
for name, im_mask, zones in [("045", pinkm, [("top", 160, 195), ("mid", 265, 300), ("cont", 370, 402), ("X", 474, 505)]),
                             ("038", pinkm38, [("top", 250, 290), ("mid", 358, 395), ("X", 460, 495)])]:
    for (zn, y0, y1) in zones:
        seg = im_mask[y0:y1, 150:880]
        rr = np.where(seg.sum(axis=1) > 8)[0]
        if len(rr):
            print(f"  {name} {zn}: pink rows {rr.min()+y0}..{rr.max()+y0} (h={rr.max()-rr.min()+1}px = {(rr.max()-rr.min()+1)/0.955556:.1f}pt)")
        else:
            print(f"  {name} {zn}: none")

print("== 2. 038 label ink heights (dred) per row ==")
dred38 = (R38 > 110) & (R38 < 200) & (G38 < 60) & (B38 < 60)
for (zn, y0, y1) in [("top", 255, 285), ("mid", 360, 390), ("X", 462, 492)]:
    seg = dred38[y0:y1, 195:850]
    rr = np.where(seg.sum(axis=1) > 3)[0]
    print(f"  038 {zn}: dred rows {[(int(a+y0)) for a in rr][:30]}")

print("== 3. container left edge raw probe ==")
print("  045 row 302 (container top zone), x 66..200:")
print("   ", [f"{x}:{tuple(img[302, x])}" for x in range(66, 200, 6)])
print("  045 row 342 (between bar and plus), x 66..200:")
print("   ", [f"{x}:{tuple(img[342, x])}" for x in range(66, 200, 6)])
print("  038 row 290 (its container top zone), x 66..200:")
print("   ", [f"{x}:{tuple(img38[290, x])}" for x in range(66, 200, 6)])
print("  038 row 342, x 66..200:")
print("   ", [f"{x}:{tuple(img38[342, x])}" for x in range(66, 200, 6)])
print("  fill medians: 045 (x100..135,y340..365):", np.median(img[340:365, 100:135].reshape(-1,3), axis=0),
      " 038 (x100..135,y330..355):", np.median(img38[330:355, 100:135].reshape(-1,3), axis=0))
print("  fill medians right: 045 (x865..882,y340..365):", np.median(img[340:365, 865:882].reshape(-1,3), axis=0),
      " 038 (x865..882,y330..355):", np.median(img38[330:355, 865:882].reshape(-1,3), axis=0))

print("== 4. gray bar black-text extent (inside bar, margins excluded) ==")
dark = (R < 150) & (G < 150) & (B < 150)
seg = dark[312:332, 182:858]
cc = np.where(seg.sum(axis=0) > 0)[0]
rr = np.where(seg.sum(axis=1) > 0)[0]
print(f"  045 graybar dark ink: x {cc.min()+182}..{cc.max()+182} y {rr.min()+312}..{rr.max()+312}")
# gap structure: find word clusters
def to_bands(ys, gap):
    if len(ys) == 0: return []
    b = []; s = ys[0]; p = ys[0]
    for v in ys[1:]:
        if v > p + gap: b.append((s, p)); s = v
        p = v
    b.append((s, p)); return b
print("   clusters:", [(a+182, b+182) for a, b in to_bands(cc, 8)])
dark38 = (R38 < 150) & (G38 < 150) & (B38 < 150)
seg = dark38[313:332, 170:870]
cc = np.where(seg.sum(axis=0) > 0)[0]
print(f"  038 graybar dark ink: x {cc.min()+170}..{cc.max()+170}")
print("   clusters:", [(a+170, b+170) for a, b in to_bands(cc, 8)])

print("== 5. FFN box: fill + icon tiles ==")
print("  045 FFN fill (x 250..300, y 240..254):", np.median(img[240:254, 250:300].reshape(-1,3), axis=0))
print("  045 FFN fill (x 700..740, y 240..254):", np.median(img[240:254, 700:740].reshape(-1,3), axis=0))
nonwhite = (R < 235) | (G < 235) | (B < 235)
seg = nonwhite[222:250, 170:880]
cc = np.where(seg.sum(axis=0) > 2)[0]
print("  045 FFN nonwhite col clusters (icons):", [(a+170, b+170) for a, b in to_bands(cc, 4)])

print("== 6. annot line2 tail colors (x 690..800, y 111..123) ==")
for x in range(690, 800, 8):
    col = [tuple(img[y, x]) for y in range(112, 123, 3)]
    print(f"   x={x}: {col}")

print("== 7. dots color + size (topY first dot at ~629, y 172..179) ==")
seg = (B > 100) & (R < 100) & (G < 100)
sub = seg[168:186, 620:640]
rr = np.where(sub.any(axis=1))[0]; cc = np.where(sub.any(axis=0))[0]
print(f"  045 topY dot1: y {rr.min()+168}..{rr.max()+168} x {cc.min()+620}..{cc.max()+620} center px {tuple(img[172+ (rr.min()+rr.max())//2 - 168, 629])}")
subg = (G38 > 120) & (R38 < 110) & (B38 < 130) & (G38 - R38 > 40)
print("  038 X dot color sample (590..720, 495..505):", tuple(img38[500, 640]))

print("== 8. panel border color samples ==")
print("  045 panel top (400,159):", tuple(img[159, 400]), " left (65,300):", tuple(img[300, 65]), " right (893,300):", tuple(img[300, 893]), " bottom (400,510):", tuple(img[510, 200]))
print("  045 FFN border (400,200):", tuple(img[200, 400]), " annot border (300,80):", tuple(img[80, 300]), " (300,154):", tuple(img[154, 300]))

print("== 9. FFN title: color split along ink ==")
blue = (B > 110) & (R < 110) & (G < 110)
seg = blue[204:220, 270:790]
cc = np.where(seg.sum(axis=0) > 0)[0]
print("  FFN title blue clusters:", [(a+270, b+270) for a, b in to_bands(cc, 12)])
redl = (R > 150) & (R - G > 40) & (R - B > 40)
seg = redl[204:220, 270:790]
cc = np.where(seg.any(axis=0))[0]
print("  FFN title red-ish clusters:", [(a+270, b+270) for a, b in to_bands(cc, 8)] if len(cc) else "none")

print("== 10. col1 orange curve ink bbox ==")
orange = (R > 195) & (G > 115) & (G < 205) & (B < 115)
seg = orange[345:500, 140:215]
rr = np.where(seg.any(axis=1))[0]; cc = np.where(seg.any(axis=0))[0]
print(f"  045 col1 curve: y {rr.min()+345}..{rr.max()+345} x {cc.min()+140}..{cc.max()+140}")
orange38 = (R38 > 195) & (G38 > 115) & (G38 < 205) & (B38 < 115)
seg = orange38[340:505, 140:215]
rr = np.where(seg.any(axis=1))[0]; cc = np.where(seg.any(axis=0))[0]
print(f"  038 col1 curve: y {rr.min()+340}..{rr.max()+340} x {cc.min()+140}..{cc.max()+140}")

print("== 11. block arrow shape check (045 zone1, col1: x 195..220, y 395..415) ==")
for y in range(396, 414, 2):
    print(f"   y={y}:", [f"{x}:{tuple(img[y, x])}" for x in range(196, 218, 3)])
