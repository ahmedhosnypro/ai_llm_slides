#!/usr/bin/env python3
"""Pass 3: ASCII layout map + corrected color sampling + arrow/border disambiguation."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_040.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# 8px-cell ASCII map
def classify(cell):
    rr, gg, bb = cell[:, 0].mean(), cell[:, 1].mean(), cell[:, 2].mean()
    if rr > 120 and gg < 110 and bb < 110: return "R"          # red
    if rr < 60 and gg < 60 and bb < 60: return "K"            # black
    if bb > rr + 30 and bb > gg + 30 and bb > 90: return "N"  # navy/blue
    if rr > 240 and gg > 240 and bb > 243: return "W"         # pure white
    if rr > 240 and gg > 240 and 200 < bb <= 243: return "Y"  # cream fill
    if abs(rr - 233) < 18 and abs(gg - 233) < 18 and abs(bb - 231) < 18: return "."  # panel gray
    if rr > 245 and gg > 245 and bb > 245: return "W"
    return "?"
out = []
for y in range(0, H, 8):
    row = ""
    for x in range(0, W, 8):
        row += classify(IM[y:y+8, x:x+8])
    out.append(f"{y:3d} {row}")
print("\n".join(out))
print("     " + "".join(str((x // 8) % 10) for x in range(0, W, 8)))

def modal_mask(mask, label):
    px = IM[mask]
    if not len(px):
        print(label, "EMPTY"); return
    vals, counts = np.unique(px, axis=0, return_counts=True)
    order = np.argsort(-counts)[:4]
    print(label + ": " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in order))

red = (r > 120) & (g < 110) & (b < 110)
tm = np.zeros_like(red); tm[50:135, 60:900] = red[50:135, 60:900]
modal_mask(tm, "\ntitle ink")

navy = (b > 90) & (r < 110) & (g < 110) & (b > r + 30) & (b > g + 30)
nm = np.zeros_like(navy); nm[360:520, 45:700] = navy[360:520, 45:700]
modal_mask(nm, "navy text/border modal")

# blue-ish runs with lower threshold (border hunt), long verticals
blue = navy
print("\n--- blue VERT runs >=60 in x 45..700, y 350..530 ---")
for x in range(45, 701):
    ys = np.where(blue[350:530, x])[0] + 350
    if len(ys) > 60:
        runs = []; s = p = ys[0]
        for c in ys[1:]:
            if c == p + 1: p = c
            else: runs.append((s, p)); s = p = c
        runs.append((s, p))
        for (a, bb) in runs:
            if bb - a + 1 >= 60: print(f"x={x}: y {a}..{bb} (len {bb-a+1})")
print("--- blue HORIZ runs >=200 in y 350..530 ---")
for y in range(350, 531):
    xs = np.where(blue[y, 45:700])[0] + 45
    if len(xs) > 200:
        runs = []; s = p = xs[0]
        for c in xs[1:]:
            if c == p + 1: p = c
            else: runs.append((s, p)); s = p = c
        runs.append((s, p))
        for (a, bb) in runs:
            if bb - a + 1 >= 200: print(f"y={y}: x {a}..{bb} (len {bb-a+1})")

# border stroke hunt: sample columns just left of fill (x 48..56) and top rows (y 358..368)
print("\nborder probes:")
for x in [48, 50, 52, 54, 56, 58]:
    col = IM[380:500, x]
    vals, counts = np.unique(col, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    print(f"  col x={x}: " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))
for y in [358, 360, 362, 364, 366, 368]:
    row = IM[y, 100:600]
    vals, counts = np.unique(row, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    print(f"  row y={y}: " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))
for x in [682, 684, 686, 688]:
    col = IM[380:500, x]
    vals, counts = np.unique(col, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    print(f"  right col x={x}: " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))
for y in [512, 514, 516, 518]:
    row = IM[y, 100:600]
    vals, counts = np.unique(row, axis=0, return_counts=True)
    o = np.argsort(-counts)[:2]
    print(f"  bottom row y={y}: " + ", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))

# arrow: pure white (b>=245) hunt in x 630..724, y 370..500
wh = (r >= 245) & (g >= 245) & (b >= 245)
wm = np.zeros_like(wh); wm[370:500, 630:724] = wh[370:500, 630:724]
ys, xs = np.where(wm)
if len(ys):
    print(f"\nARROW pure-white extent: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  n={len(ys)}")
    for y in range(ys.min(), ys.max() + 1, 3):
        xr = np.where(wm[y])[0]
        if len(xr): print(f"  y={y}: x {xr.min()}..{xr.max()} n={len(xr)}")
# arrow red outline, tight window x 660..724
rm = np.zeros_like(red); rm[370:500, 660:724] = red[370:500, 660:724]
ys2, xs2 = np.where(rm)
if len(ys2):
    print(f"ARROW red outline extent: x {xs2.min()}..{xs2.max()}  y {ys2.min()}..{ys2.max()}  n={len(ys2)}")

# what is at y 496..518, x 690..920 (below grid)?
print("\nprobe y=502..512, x=700..910 colors:")
sub = IM[502:513, 700:910].reshape(-1, 3)
vals, counts = np.unique(sub, axis=0, return_counts=True)
o = np.argsort(-counts)[:5]
print(", ".join('#%02X%02X%02X(%d)' % tuple(list(vals[i]) + [counts[i]]) for i in o))
