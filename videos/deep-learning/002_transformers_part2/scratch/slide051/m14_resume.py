#!/usr/bin/env python3
# m14_resume.py — fine pixel-grid dumps for the remaining 002:51 judge regions.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r4 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_4.png").convert("RGB")
SX = lambda fx: (fx - 18.128) / 0.961235
SY = lambda fy: (fy + 0.045) / 0.956566
K = 150.0 / 72.0

def q(r, g, b):
    """short class tag"""
    if b > 100 and r < 90 and g < 90: return "N"      # navy
    if r < 90 and g < 90 and b < 90: return "k"       # dark
    if g > 150 and g > r + 40 and g > b + 40: return "G"  # saturated green
    if r > 235 and g > 245 and b > 210: return "."    # mint bg
    if r > 230 and g > 140 and b < 130: return "O"    # orange
    if r > 150 and 100 < g < 200 and b < 120 and r > b + 50: return "T"  # tan/brown
    if r > 170 and 90 < g < 140 and 90 < b < 140: return "M"  # maroon
    if b > 150 and r < 150 and g < 160: return "b"    # blue/indigo
    if r > 170 and g < 160 and b > 170: return "P"    # purple
    if r > 200 and g > 200 and b > 200: return "w"    # white/light
    if r > 140 and g > 140 and b < 110: return "y"    # yellow-olive
    return "?"

def dump(img, x0, y0, x1, y1, to_frame, step=2, label=""):
    print(f"--- {label} ({x0}..{x1}, {y0}..{y1}) step={step}")
    xs = list(range(x0, x1 + 1, step))
    print("      " + "".join(f"{x % 100:<2d}"[0] for x in xs))
    print("      " + "".join(f"{x % 10}" for x in xs))
    for y in range(y0, y1 + 1, step):
        row = f"y{y:<4d}" if step >= 2 else f"y{y:<3d}"
        for x in xs:
            fx, fy = to_frame(x, y)
            r, g, b = img.getpixel((min(max(int(fx), 0), img.size[0] - 1), min(max(int(fy), 0), img.size[1] - 1)))
            row += q(r, g, b) + ("" if step <= 2 else " ")
        print(row)

o2f = lambda x, y: (x, y)
r2f = lambda x, y: (x / K * 0.961235 + 18.128, y / K * 0.956566 - 0.045)

# 1) hunt the tan "Nx" circle right of the decoder MHA block
dump(orig, 818, 240, 895, 315, o2f, 3, "ORIG decoder far-right band (Nx hunt)")
# 2) decoder bottom: embedding box / PE icon / label / dark check
dump(orig, 726, 392, 878, 470, o2f, 4, "ORIG decoder bottom (PE + embedding)")
# 3) encoder norm box 1 fine
dump(orig, 200, 256, 286, 286, o2f, 2, "ORIG encoder norm box1")
# 4) encoder norm box 2 fine
dump(orig, 200, 324, 286, 354, o2f, 2, "ORIG encoder norm box2")
# 5) render_4 same norm box1 region for comparison
dump(r4, int(SX(200) * K), int(SY(256) * K), int(SX(286) * K), int(SY(286) * K), r2f, 4, "RENDER4 encoder norm box1")
