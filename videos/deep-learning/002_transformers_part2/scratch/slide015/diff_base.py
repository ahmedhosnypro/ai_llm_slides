#!/usr/bin/env python3
"""PIL-diff: my 002 frame (mapped into true slide coords) vs the imported 001:43
component's render (numeral 15), both 960x540 slide-pt space.

Mapping fitted from THIS frame's four chrome landmarks (measure_frame_out.json):
  frame_x = 17.628 + 0.961232*slide_x   (left border 58<->42, right 901<->919)
  frame_y =  0.955556*slide_y           (top border 43<->45, bottom stroke 516<->540)
Badge cross-check: yellow-bbox center (874.5,70.5) -> slide (891.5,73.8) vs house
(893,71) — within the same JPEG-bbox noise slide_002 reported. Same template.
"""
from PIL import Image, ImageChops
import json

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide015"
AX, SX, SY = 17.628, 0.961232, 0.955556

frame = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_015.jpg").convert("RGB")
# resample frame into slide coords (960x540)
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

# block grid report: 32x18 cells of 30px, mean abs ink
TH = 48  # per-pixel gray threshold for "different"
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
# cluster hot cells into row bands
rows = {}
for (cx, cy), v in sorted(hot.items()):
    rows.setdefault(cy, []).append((cx, v))
print("\nHOT CELLS (frac>0.12) by 30px row band (cy: cx list):")
for cy in sorted(rows):
    xs = [c for c, _ in rows[cy]]
    print(f"  y{cy:3d}..{cy+30:3d}: x {min(xs):3d}..{max(xs)+30:3d}  n={len(xs)}  cells={xs}")

# overall
tot = sum(1 for y in range(0, H, 2) for x in range(0, W, 2) if px[x, y] > TH)
print(f"\noverall hot px frac (> {TH}): {tot / ((W//2)*(H//2)):.4f}")

# save heat visualization
vis = Image.merge("RGB", (g, g, g))
vis.save(f"{SCR}/diff_gray.png")

# column profile of hot pixels (which x-bands differ) and row profile
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
