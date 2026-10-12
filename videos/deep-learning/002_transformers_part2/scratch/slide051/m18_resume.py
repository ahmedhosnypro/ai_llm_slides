#!/usr/bin/env python3
# m18_resume.py — verify the crop-comparison findings in the original frame.
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")

def raw(x0, y0, x1, y1, step, label):
    print(f"--- {label} ({x0}..{x1}, {y0}..{y1}) step {step}")
    print("      " + "".join(f"{x % 10}" for x in range(x0, x1 + 1, step)))
    for y in range(y0, y1 + 1, step):
        row = f"y{y:<4d}"
        for x in range(x0, x1 + 1, step):
            r, g, b = orig.getpixel((x, y))
            row += f"({r:3},{g:3},{b:3})"
        print(row)

def q(r, g, b):
    if b > 100 and r < 90 and g < 90: return "N"
    if r < 95 and g < 95 and b < 95: return "k"
    if g > 150 and g > r + 40 and g > b + 40: return "G"
    if r > 225 and g > 245 and b > 205: return "."
    if r > 225 and g > 130 and b < 135 and g < 215: return "O"
    if r > 150 and 90 < g < 200 and b < 130 and r > b + 40: return "T"
    if b > 150 and r < 150 and g < 160: return "b"
    if r > 170 and g < 160 and b > 170: return "P"
    if r > 200 and g > 200 and b > 200: return "w"
    if r > 140 and g > 140 and b < 110: return "y"
    if r > 150 and g < 110 and b < 110: return "R"  # red
    return "?"

def cls(x0, y0, x1, y1, step, label):
    print(f"--- {label} ({x0}..{x1}, {y0}..{y1}) step {step}")
    print("      " + "".join(f"{x % 10}" for x in range(x0, x1 + 1, step)))
    for y in range(y0, y1 + 1, step):
        row = f"y{y:<4d}"
        for x in range(x0, x1 + 1, step):
            row += q(*orig.getpixel((x, y)))
        print(row)

# 1) decoder QKV row (container bottom)
cls(725, 366, 800, 386, 2, "ORIG decoder QKV row")
# 2) decoder MHA-input circles (y~304)
cls(728, 296, 775, 313, 2, "ORIG decoder MHA-input circles")
# 3) inter-box connector gaps x760-780
cls(758, 208, 782, 335, 2, "ORIG decoder stack gaps x758-782")
# 4) plus/swirl hunt below the embedding box / near PE path
raw(712, 438, 762, 478, 3, "ORIG decoder below-embedding (plus/swirl hunt)")
# 5) encoder residual bus joints
cls(192, 262, 218, 348, 2, "ORIG encoder residual bus joints")
