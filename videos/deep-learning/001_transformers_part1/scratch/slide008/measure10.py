#!/usr/bin/env python3
"""Decisive underline check with LOOSE mask (washed lines have b-r 20..40, g 150..220)."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
ld = im.load()

def loose(p):
    r, g, b = p
    return b - r > 20 and b > 130 and g < 235 and not (r > 215 and g > 245)

print("wait1 'Wait' zone x100..140, rows 262..282 (loose mask):")
for y in range(262, 283):
    row = [x for x in range(95, 150) if loose(ld[x, y])]
    print(f"  y={y}: n={len(row)} {min(row) if row else '-'}..{max(row) if row else '-'}")
print("wait2 'Wait' zone x255..305, rows 259..279 (loose mask):")
for y in range(259, 280):
    row = [x for x in range(255, 310) if loose(ld[x, y])]
    print(f"  y={y}: n={len(row)} {min(row) if row else '-'}..{max(row) if row else '-'}")
print("callout underline row 197 (loose, x77..293) + core colors:")
row = [x for x in range(70, 300) if loose(ld[x, y]) for y in [197]]
print("  n:", len(row))
print("  cores:", ld[120, 197], ld[180, 197], ld[250, 197])
print("callout gap rows 198..201 x70..300 (loose):")
for y in range(198, 202):
    n = sum(1 for x in range(70, 300) if loose(ld[x, y]))
    print(f"  y={y}: n={n}")
# raw pixel dump: wait1 rows 270..276 at a few x positions under 'Wait'
print("raw wait1 (x, y270..276):")
for x in (110, 120, 128, 135):
    print(f"  x={x}:", [ld[x, y] for y in range(270, 277)])
