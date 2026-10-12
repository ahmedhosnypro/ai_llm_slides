#!/usr/bin/env python3
"""Slide 043 probe D: v-arrow shaft/label disambiguation, h-arrow shaft trace,
d-arrow + label fine map with a red-only mask (orange excluded)."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== 1. v-region column profile: RED-ONLY (excludes orange) x600..670, y185..300 ===")
redonly = (r > 120) & (g < 120) & (b < 140) & (r - g > 45) & (r - b > 35) & (b < g + 60)
prof = redonly[185:300, 600:670].sum(axis=0)
for i, v in enumerate(prof):
    if v > 0: print(f"  x{600+i}: {int(v)}")

print("=== 2. v-region row profile at x655..660 (suspected shaft) ===")
for y in range(160, 320):
    n = redonly[y, 650:665].sum()
    if n > 0: print(f"  y{y}: n={n}", "".join("X" if redonly[y, x] else "." for x in range(648, 665)))

print("=== 3. h-arrow: red-only rows x650..830, y310..345 ===")
for y in range(310, 346):
    n = redonly[y, 650:830].sum()
    if n > 0:
        xs = np.where(redonly[y, 650:830])[0]
        print(f"  y{y}: n={n} x {xs.min()+650}..{xs.max()+650}", "".join("X" if redonly[y, x] else "." for x in range(655, 820, 2)))

print("=== 4. d-arrow: red-only map x795..900, y225..340 (step 2) ===")
print("      " + "".join(str((x // 10) % 10) for x in range(795, 900, 2)))
for y in range(225, 342, 2):
    row = "".join("X" if redonly[y, x] else "." for x in range(795, 900, 2))
    if "X" in row: print(f"y{y:4d} {row}")

print("=== 5. d-label hunt: pale-red text mask x830..900, y235..330 ===")
pale = (r > 150) & (r - g > 18) & (r - b > 10) & (g < 215) & (b < 215)
for y in range(235, 332, 2):
    n = pale[y, 830:900].sum()
    if n > 2:
        xs = np.where(pale[y, 830:900])[0]
        print(f"  y{y}: n={n} x {xs.min()+830}..{xs.max()+830}")

print("=== 6. v-label strip fine: pale mask x605..665, y185..290 col profile ===")
prof = pale[185:290, 605:665].sum(axis=0)
for i, v in enumerate(prof):
    if v > 0: print(f"  x{605+i}: {int(v)}")

print("=== 7. 'Feature Vector' v-label: row profile at its strip (pale) ===")
for y in range(185, 290, 2):
    n = pale[y, 620:655].sum()
    if n > 0: print(f"  y{y}: n={n}")
