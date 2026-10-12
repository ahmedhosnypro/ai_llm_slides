#!/usr/bin/env python3
"""Pass 4: yellow box fine structure — left edge, bottom edge, border colors,
cream scatter rows 480..520, title cap/baseline, panel borders of THIS frame."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_040.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# fine ASCII map of the box left region: x 40..130, y 350..525, 2px cells
print("=== fine map x 40..130 (2px cells), y 350..524 ===")
hdr = "     " + "".join(str((x // 2) % 10) for x in range(40, 130, 2))
print(hdr)
for y in range(350, 524, 2):
    row = ""
    for x in range(40, 130, 2):
        c = IM[y, x]
        rr, gg, bb = c
        if rr > 120 and gg < 110 and bb < 110: ch = "R"
        elif rr < 70 and gg < 70 and bb < 70: ch = "K"
        elif bb > rr + 25 and bb > 90: ch = "N"
        elif rr > 244 and gg > 244 and bb > 243: ch = "W"
        elif rr > 240 and gg > 240 and 200 < bb <= 243: ch = "Y"
        elif abs(rr - 233) < 14 and abs(gg - 233) < 14 and abs(bb - 231) < 14: ch = "."
        else: ch = "?"
        row += ch
    print(f"{y:3d}  {row}")

print("\n=== cream pixel col-ranges per row (y 478..520) ===")
cream = (r > 240) & (g > 240) & (b > 210) & (b < 246)
for y in range(478, 521, 2):
    xs = np.where(cream[y, :720])[0]
    if len(xs):
        ranges = []
        s = p = xs[0]
        for c in xs[1:]:
            if c - p <= 6: p = c
            else: ranges.append((s, p)); s = p = c
        ranges.append((s, p))
        print(f"y={y}: n={len(xs)} ranges={ranges[:8]}")
    else:
        print(f"y={y}: none")

print("\n=== interior modal patches ===")
def modal(x0, x1, y0, y1, label):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    o = np.argsort(-counts)[:3]
    print(f"{label}: " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))
modal(200, 400, 420, 430, "box interior between paragraphs")
modal(560, 660, 370, 385, "box interior right of L1")
modal(100, 160, 490, 505, "below L4 (y 490..505)")
modal(60, 66, 400, 460, "x 60..66 strip")
modal(70, 74, 400, 460, "x 70..74 strip")
modal(690, 700, 400, 460, "x 690..700 (right of box)")
modal(150, 550, 360, 361, "top stroke y=360")
modal(150, 550, 362, 363, "top stroke y=362")

# darkest pixels of top stroke = true border color estimate
band = IM[360:365, 100:600].reshape(-1, 3)
lum = band.sum(axis=1)
dark = band[lum < np.percentile(lum, 8)]
vals, counts = np.unique(dark, axis=0, return_counts=True)
o = np.argsort(-counts)[:5]
print("top stroke darkest modal: " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))

# === title metrics ===
red = (r > 120) & (g < 110) & (b < 110)
tmask = np.zeros_like(red); tmask[50:135, 60:900] = red[50:135, 60:900]
colsum = tmask.sum(axis=0)
xs = np.where(colsum > 0)[0]
print(f"\ntitle ink x {xs.min()}..{xs.max()}")
rowsum = tmask.sum(axis=1)
rows = np.where(rowsum > 0)[0]
print(f"title ink y {rows.min()}..{rows.max()}")
# baseline = last row with >40% of max rowsum
strong = np.where(rowsum > 0.4 * rowsum.max())[0]
print(f"title strong rows {strong.min()}..{strong.max()} (baseline ~{strong.max()})")
# 'H' cap: columns 204..218
segH = tmask[:, 204:219]
ysH = np.where(segH.sum(axis=1) > 0)[0]
print(f"'H' cap y {ysH.min()}..{ysH.max()} (cap height {ysH.max()-ysH.min()+1})")
# descender rows (rows below baseline with ink)
desc = rows[rows > strong.max()]
print(f"descender rows: {desc.min() if len(desc) else None}..{desc.max() if len(desc) else None}")

# === panel borders in THIS frame ===
print("\n=== this frame's panel edges ===")
for x in [40, 42, 44, 46, 56, 58, 60, 62, 904, 906, 908, 910, 912, 916, 918]:
    col = IM[200:320, x]
    vals, counts = np.unique(col, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    print(f"  col x={x} (y200..320): " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))
for y in [43, 45, 47, 49]:
    row = IM[y, 200:800]
    vals, counts = np.unique(row, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    print(f"  row y={y} (x200..800): " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))

# === photo borders: exact edges ===
print("\n=== photo red-border edges (long runs) ===")
for y in [154, 155, 156, 157, 158, 317, 318, 319, 320]:
    xs2 = np.where(red[y, :930])[0]
    if len(xs2):
        ranges = []
        s = p = xs2[0]
        for c in xs2[1:]:
            if c - p <= 4: p = c
            else: ranges.append((s, p)); s = p = c
        ranges.append((s, p))
        ranges = [(a, bb) for a, bb in ranges if bb - a >= 25]
        print(f"y={y}: {ranges}")
for x in [95, 96, 97, 98, 99, 401, 402, 403, 404, 405, 430, 431, 432, 433, 434, 728, 729, 730, 731, 732, 724, 725, 726, 886, 887, 888, 889]:
    ys2 = np.where(red[130:520, x])[0] + 130
    if len(ys2):
        ranges = []
        s = p = ys2[0]
        for c in ys2[1:]:
            if c - p <= 4: p = c
            else: ranges.append((s, p)); s = p = c
        ranges.append((s, p))
        ranges = [(a, bb) for a, bb in ranges if bb - a >= 25]
        if ranges: print(f"x={x}: {ranges}")
