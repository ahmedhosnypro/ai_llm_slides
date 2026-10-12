#!/usr/bin/env python3
"""Pass 6: E1/E6 per-column blue-vs-red counts (run split), slide_039 navy-border cross-check,
zoomed crops for vision gate (E1 line, C1 line)."""
from PIL import Image
from collections import Counter

S060 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_060.jpg"
S039 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_039.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide060"
img = Image.open(S060).convert("RGB")
px = img.load()

def blueish(p):
    r, g, b = p
    return b > 100 and (b - r) > 35 and (b - g) > 25

def reddish(p):
    r, g, b = p
    return r > 110 and (r - g) > 45 and (r - b) > 35

# ---- E1 per-column counts, frame cols 85..320, rows 146..163
print("== E1 columns (col: blue,red) rows 146..163 ==")
runs = []
for x in range(85, 330):
    nb = sum(1 for y in range(146, 164) if blueish(px[x, y]))
    nr = sum(1 for y in range(146, 164) if reddish(px[x, y]))
    runs.append((x, nb, nr))
# compact print: only cols with any ink
s = ""
for x, nb, nr in runs:
    if nb or nr:
        s += f"{x}:{nb}/{nr} "
print(s)

# ---- E6 columns 85..200
print("== E6 columns (col: blue,red) rows 439..455 ==")
s = ""
for x in range(85, 200):
    nb = sum(1 for y in range(439, 456) if blueish(px[x, y]))
    nr = sum(1 for y in range(439, 456) if reddish(px[x, y]))
    if nb or nr:
        s += f"{x}:{nb}/{nr} "
print(s)

# ---- slide_039 summary box border core color (col 72, rows 415..500)
im39 = Image.open(S039).convert("RGB")
p39 = im39.load()
c = Counter()
for y in range(415, 500):
    for x in (71, 72, 73):
        p = p39[x, y]
        if blueish(p) or (p[2] > p[0] and sum(p) < 500):
            c[p] += 1
print("== slide_039 summary box left border cores:", c.most_common(6))

# ---- crops for vision gate
# E1 line: frame x 80..620, y 140..170 (x3)
c1 = img.crop((80, 140, 620, 170)).resize((540 * 3, 30 * 3), Image.LANCZOS)
c1.save(f"{OUT}/crop_E1.png")
# C1 citation line: frame x 118..545, y 162..192 (x4)
c2 = img.crop((118, 162, 545, 192)).resize((427 * 4, 30 * 4), Image.LANCZOS)
c2.save(f"{OUT}/crop_C1.png")
# E4 line (italic): frame x 85..795, y 328..358 (x2)
c3 = img.crop((85, 328, 795, 358)).resize((710 * 2, 30 * 2), Image.LANCZOS)
c3.save(f"{OUT}/crop_E4.png")
print("crops saved")
