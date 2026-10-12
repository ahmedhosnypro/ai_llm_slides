#!/usr/bin/env python3
"""PIL-diff: my 002 frame 011 (mapped into true slide coords) vs the imported 001:43
component's render (numeral 11), both 960x540 slide-pt space.

Mapping fitted from THIS frame's four chrome landmarks (landmarks.out):
  left border 58<->42, right 901<->919, top 43<->45, bottom stroke 516<->540:
  frame_x = 17.628 + 0.961232*slide_x ;  frame_y = 0.955556*slide_y
Badge cross-check: yellow-bbox center (877.5,71) -> slide (894.6,74.3) vs house
(893,71) — same accepted JPEG-bbox delta as certified slide_002/015 builds.
"""
from PIL import Image, ImageChops
import json

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
AX, SX, SY = 17.628, 0.961232, 0.955556

frame = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_011.jpg").convert("RGB")
slideimg = frame.transform((960, 540), Image.AFFINE, (SX, 0, AX, 0, SY, 0), resample=Image.BILINEAR, fillcolor=(0, 0, 0))
slideimg.save(f"{SCR}/frame_in_slide_coords.png")

base = Image.open(f"{SCR}/render/pbase-1.png").convert("RGB")
print("base render size:", base.size)
if base.size != (960, 540):
    base = base.resize((960, 540), Image.LANCZOS)
base.save(f"{SCR}/base_960.png")

diff = ImageChops.difference(slideimg, base)
g = diff.convert("L")
px = g.load()
W, H = g.size

TH = 48
cells = {}
for cy in range(0, H, 30):
    for cx in range(0, W, 30):
        n = tot = 0
        for y in range(cy, min(cy + 30, H), 2):
            for x in range(cx, min(cx + 30, W), 2):
                tot += 1
                if px[x, y] > TH:
                    n += 1
        cells[(cx, cy)] = n / max(tot, 1)

hot = {k: v for k, v in cells.items() if v > 0.12}
rows = {}
for (cx, cy), v in sorted(hot.items()):
    rows.setdefault(cy, []).append((cx, v))
print("\nHOT CELLS (frac>0.12) by 30px row band (cy: cx list):")
for cy in sorted(rows):
    xs = [c for c, _ in rows[cy]]
    print(f"  y{cy:3d}..{cy+30:3d}: x {min(xs):3d}..{max(xs)+30:3d}  n={len(xs)}  cells={xs}")

tot = sum(1 for y in range(0, H, 2) for x in range(0, W, 2) if px[x, y] > TH)
print(f"\noverall hot px frac (> {TH}): {tot / ((W//2)*(H//2)):.4f}")

vis = Image.merge("RGB", (g, g, g))
vis.save(f"{SCR}/diff_gray.png")

colhot = [sum(1 for y in range(0, H, 2) if px[x, y] > TH) for x in range(W)]
rowhot = [sum(1 for x in range(0, W, 2) if px[x, y] > TH) for y in range(H)]
json.dump({"colhot": colhot, "rowhot": rowhot}, open(f"{SCR}/diff_profiles.json", "w"))
print("\nrowhot>40 bands:")
inb = False
for y, v in enumerate(rowhot):
    if v > 40 and not inb:
        y0 = y; inb = True
    elif v <= 40 and inb:
        print(f"  y {y0}..{y-1}  peak {max(rowhot[y0:y])}")
        inb = False
if inb:
    print(f"  y {y0}..{H-1}  peak {max(rowhot[y0:H])}")
