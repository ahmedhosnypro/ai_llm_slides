#!/usr/bin/env python3
"""Pass 6: exhaustive corridor scan for leaders; wait-box edge/border; blue-ish pixel census."""
from PIL import Image
import collections

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
im6 = Image.open(BASE + "unique_slides/slide_006.jpg").convert("RGB")
ld = im.load()

# 1. census of EVERY non-background pixel color class in corridor y 292..332, x 0..500
c = collections.Counter()
for y in range(292, 333):
    for x in range(0, 500):
        p = ld[x, y]
        r, g, b = p
        if r > 246 and g > 246 and b > 246: continue   # white
        if 210 < r < 240 and g > 240 and b > 240: continue  # lightblue fill
        c[(p[0]//16*16, p[1]//16*16, p[2]//16*16)] += 1
print("corridor y292..332 color classes:", c.most_common(12))

# 2. same for right-of-callout region x 326..500, y 165..300 (excluding wait2 x213..345 rows)
c2 = collections.Counter()
for y in range(165, 300):
    for x in range(326, 500):
        if 213 <= x <= 345 and 253 <= y <= 291: continue  # wait2 box
        p = ld[x, y]
        r, g, b = p
        if r > 246 and g > 246 and b > 246: continue
        if 210 < r < 240 and g > 240 and b > 240: continue
        c2[(p[0]//16*16, p[1]//16*16, p[2]//16*16)] += 1
print("right-of-callout color classes:", c2.most_common(12))

# 3. where exactly are non-white pixels in corridor? per-row runs of "any ink"
def anyink(p):
    r, g, b = p
    return not (r > 243 and g > 243 and b > 243)
print("corridor per-row ink runs (y292..332):")
for y in range(292, 333):
    row = [x for x in range(0, 500) if anyink(ld[x, y])]
    if row:
        runs, s, prev = [], None, -10
        for x in row:
            if x - prev > 6:
                if s is not None: runs.append((s, prev))
                s = x
            prev = x
        runs.append((s, prev))
        print(f"  y={y}: {runs}")

# 4. right-of-callout per-row ink runs (x 346..500, y 165..300)
print("right-of-callout ink runs (x346..500):")
for y in range(165, 300):
    row = [x for x in range(346, 500) if anyink(ld[x, y])]
    if row:
        runs, s, prev = [], None, -10
        for x in row:
            if x - prev > 6:
                if s is not None: runs.append((s, prev))
                s = x
            prev = x
        runs.append((s, prev))
        print(f"  y={y}: {runs}")

# 5. wait box edges (border check) — top edge of wait1 (y 254..258 at x 70..170) and wait2 (y 252..256)
print("wait1 top edge y=254..259 at x=80,120,160:")
for y in range(253, 260):
    print(f"  y={y}: {ld[80, y]} {ld[120, y]} {ld[160, y]}")
print("wait2 top edge y=252..258 at x=240,280,320:")
for y in range(251, 258):
    print(f"  y={y}: {ld[240, y]} {ld[280, y]} {ld[320, y]}")
print("wait1 left edge x=48..56 at y=275:", [ld[x, 275] for x in range(48, 57)])
