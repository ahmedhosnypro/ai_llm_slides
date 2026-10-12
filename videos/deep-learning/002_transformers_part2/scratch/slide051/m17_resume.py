#!/usr/bin/env python3
# m17_resume.py — embedding-box checks + navy badge census.
from collections import deque
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
orig = Image.open(f"{ROOT}/unique_slides/slide_051.jpg").convert("RGB")
r4 = Image.open(f"{ROOT}/recreated_pptx/qa/slide051/render_4.png").convert("RGB")
SX = lambda fx: (fx - 18.128) / 0.961235
SY = lambda fy: (fy + 0.045) / 0.956566
K = 150.0 / 72.0

def q(r, g, b):
    if g > 100 and g < 190 and r < 100 and b < 100: return "d"   # dark green
    if b > 100 and r < 90 and g < 90: return "N"
    if r < 95 and g < 95 and b < 95: return "k"
    if g > 150 and g > r + 40 and g > b + 40: return "G"
    if 150 < r < 215 and 140 < g < 215 and 90 < b < 170: return "o"
    if r > 225 and g > 245 and b > 205: return "."
    if r > 150 and 90 < g < 200 and b < 130 and r > b + 40: return "T"
    if b > 150 and r < 150 and g < 160: return "b"
    if r > 170 and g < 160 and b > 170: return "P"
    if r > 200 and g > 200 and b > 200: return "w"
    return "?"

def dump(img, fx0, fy0, fx1, fy1, step, label, to_rend=False):
    print(f"--- {label} frame ({fx0},{fy0})-({fx1},{fy1}) step {step}")
    xs = list(range(fx0, fx1 + 1, step))
    print("      " + "".join(f"{x % 10}" for x in xs))
    for fy in range(fy0, fy1 + 1, step):
        row = f"y{fy:<4d}"
        for fx in xs:
            if to_rend:
                px = img.getpixel((min(int(SX(fx) * K), img.size[0] - 1), min(int(SY(fy) * K), img.size[1] - 1)))
            else:
                px = img.getpixel((fx, fy))
            row += q(*px)
        print(row)

# 1) encoder bottom: embedding box + green check at lower-left?
dump(orig, 193, 396, 240, 468, 2, "ORIG encoder bottom-left (embedding check?)")
# 2) decoder: left of embedding box (dark-brown check?)
dump(orig, 718, 412, 745, 458, 2, "ORIG decoder left-of-embedding (dark check?)")
# 3) b-channel split test x782..812 y398..440 (brown icon vs maroon box?)
print("--- ORIG b-channel split x782..812 y398..440 step 2: (r,g,b) at selected cols")
for y in range(398, 441, 4):
    row = f"y{y:<4d}"
    for x in range(782, 813, 3):
        r, g, b = orig.getpixel((x, y))
        row += f"({r:3},{g:3},{b:3})"
    print(row)
# 4) navy census, orig + render4
def navy(img, fx0, fy0, fx1, fy1, to_rend=False):
    hits = []
    for fy in range(fy0, fy1):
        for fx in range(fx0, fx1):
            if to_rend:
                r, g, b = img.getpixel((min(int(SX(fx) * K), img.size[0] - 1), min(int(SY(fy) * K), img.size[1] - 1)))
            else:
                r, g, b = img.getpixel((fx, fy))
            if b > 110 and r < 90 and g < 90:
                hits.append((fx, fy))
    clusters = []
    for (i, j) in hits:
        placed = False
        for c in clusters:
            if abs(c[0] / c[2] - i) < 13 and abs(c[1] / c[2] - j) < 13:
                c[0] += i; c[1] += j; c[2] += 1
                placed = True
                break
        if not placed:
            clusters.append([i, j, 1])
    return sorted([(round(c[0] / c[2]), round(c[1] / c[2]), c[2]) for c in clusters if c[2] >= 6], key=lambda t: (t[1], t[0]))

print("--- ORIG navy census decoder stack x728..830 y188..392:")
print(navy(orig, 728, 188, 830, 392))
print("--- RENDER4 navy census same region:")
print(navy(r4, 728, 188, 830, 392, to_rend=True))
print("--- ORIG navy census encoder x196..290 y245..340:")
print(navy(orig, 196, 245, 290, 340))
print("--- RENDER4 navy census encoder:")
print(navy(r4, 196, 245, 290, 340, to_rend=True))
