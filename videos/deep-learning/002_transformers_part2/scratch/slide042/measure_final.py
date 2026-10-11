#!/usr/bin/env python3
"""Final measurements: 1px cube map, loose red scan (vertical arrow), bottom label
text bands, magenta shading grid, diagonal arrow fit."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)

def cls(px):
    R, G, B = int(px[0]), int(px[1]), int(px[2])
    if R > 240 and G > 240 and B > 235: return "."
    if R > 140 and G < 120 and B < 120 and R - G > 50 and R - B > 50: return "R"
    if B > 120 and B - R > 30 and B - G > 20: return "B"
    if G > 170 and G - R > 60 and G - B > 60: return "G"
    if G > 90 and G - R > 20 and G - B > 40: return "d"
    if R > 120 and B > 120 and G < 110: return "M"
    if R > 170 and G > 150 and B < 130: return "Y"
    if R > 170 and 80 < G < 170 and B < 100: return "O"
    if R < 100 and G < 100 and B < 100: return "K"
    return "?"

print("ONE CUBE of middle grid, 1px: x376..414, y250..296")
print("     " + "".join(str(x % 10) for x in range(376, 415)))
for y in range(250, 297):
    print(f"{y:4d} " + "".join(cls(a[y, x]) for x in range(376, 415)))

print()
print("ONE CUBE of left stack, 1px: x164..214, y256..306")
print("     " + "".join(str(x % 10) for x in range(164, 215)))
for y in range(256, 307):
    print(f"{y:4d} " + "".join(cls(a[y, x]) for x in range(164, 215)))

print()
print("LOOSE RED SCAN x580..665, y275..485 (r>110, r-g>35, r-b>35):")
redl = (a[:, :, 0] > 110) & (a[:, :, 0] - a[:, :, 1] > 35) & (a[:, :, 0] - a[:, :, 2] > 35)
for y in range(275, 486, 2):
    xs = np.nonzero(redl[y, 580:666])[0]
    if len(xs): print(f"  y{y}: x {580+xs.min()}..{580+xs.max()} n={len(xs)}")

print()
print("BOTTOM LABEL TEXT: red ink bands x640..760, y470..515")
sub = np.zeros((540, 960), bool); sub[470:515, 640:760] = redl[470:515, 640:760]
rows = sub.sum(axis=1)
inb = False
for i, v in enumerate(rows):
    if v > 0 and not inb: st, inb = i, True
    elif v == 0 and inb:
        seg = sub[st:i]
        xs = np.nonzero(seg.any(axis=0))[0]
        print(f"  band y{st}..{i-1} x {640+xs.min()}..{640+xs.max()} n={int(seg.sum())}")
        inb = False

print()
print("DIAGONAL region red bits x825..885, y395..475:")
for y in range(395, 476, 2):
    xs = np.nonzero(redl[y, 825:886])[0]
    if len(xs): print(f"  y{y}: " + ",".join(str(825 + x) for x in xs))

print()
print("MAGENTA FACE shading grid (x660..780 step 20, y330..460 step 20):")
for y in range(330, 461, 20):
    print("  " + " ".join(f"({x},{y}){tuple(int(v) for v in a[y, x])}" for x in range(660, 781, 30)))
