#!/usr/bin/env python3
"""Find long horizontal/vertical structure lines + band edges in slide_049.jpg."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_049.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# dark-ish pixels (any dark structure line)
dark = (r + g + b < 460) & ~((r - g > 50) & (r - b > 50))  # exclude pure red ink

# horizontal lines: rows where x165..890 is mostly dark
seg = dark[:, 170:880]
rowfrac = seg.mean(axis=1)
print("rows with >50% dark across x170-880:")
for y in np.where(rowfrac > 0.5)[0]:
    # sample color at x=520
    print("  y=%d frac=%.2f color@520=%s color@300=%s" % (y, rowfrac[y], tuple(a[y, 520]), tuple(a[y, 300])))

print("rows with >30% dark:")
for y in np.where((rowfrac > 0.3) & (rowfrac <= 0.5))[0]:
    print("  y=%d frac=%.2f color@520=%s" % (y, rowfrac[y], tuple(a[y, 520])))

# vertical lines: columns where y85..510 is often dark
seg2 = dark[85:510, :]
colfrac = seg2.mean(axis=0)
print("cols with >30% dark across y85-510:")
for x in np.where(colfrac > 0.3)[0]:
    print("  x=%d frac=%.2f color@250=%s color@450=%s" % (x, colfrac[x], tuple(a[250, x]), tuple(a[450, x])))

# Y-row / X-row / word-row bands via non-white scan in x180..860
nonwhite = (r < 235) | (g < 235) | (b < 235)
band = nonwhite[:, 185:860]
frac = band.mean(axis=1)
print("row ink fractions y60..520 (only rows >0.25):")
run = []
for y in range(60, 522):
    f = frac[y]
    if f > 0.25: run.append(y)
    else:
        if run: print("   band y %d..%d  maxfrac %.2f  color@mid=%s" % (run[0], run[-1], max(frac[run[0]:run[-1]+1]), tuple(a[(run[0]+run[-1])//2, 500]))); run = []
if run: print("   band y %d..%d" % (run[0], run[-1]))
