#!/usr/bin/env python3
"""measure7_vecdump.py — direct RGB strip dumps through the vector band to resolve structure."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
img = np.asarray(Image.open(FR).convert("RGB")).astype(int)

print("VERTICAL STRIPS through vector band (x fixed, y 288..352):")
for x in [185, 200, 260, 400, 560, 660, 700, 800, 860, 880]:
    print(f"\n-- x={x} --")
    for y in range(288, 353, 2):
        p = img[y, x]
        tag = ""
        rr, gg, bb = int(p[0]), int(p[1]), int(p[2])
        if rr > 240 and gg < 200: tag = "PINKISH"
        elif rr > 200 and gg > 200 and bb > 200 and not (abs(rr - 233) < 12): tag = "LIGHT"
        elif rr < 150 and gg < 150: tag = "DARK"
        print(f"  y{y}: ({rr:3d},{gg:3d},{bb:3d}) {tag}")

print("\nHORIZONTAL STRIP y=295 (above boxes), x 170..890 every 20px:")
row = []
for x in range(170, 890, 20):
    p = img[295, x]
    row.append(f"x{x}:({p[0]},{p[1]},{p[2]})")
print("  " + " ".join(row))

print("\nHORIZONTAL STRIP y=310 (through boxes), x 170..890 every 20px:")
row = []
for x in range(170, 890, 20):
    p = img[310, x]
    row.append(f"x{x}:({p[0]},{p[1]},{p[2]})")
print("  " + " ".join(row))

print("\nHORIZONTAL STRIP y=331 (below boxes?), x 170..890 every 20px:")
row = []
for x in range(170, 890, 20):
    p = img[331, x]
    row.append(f"x{x}:({p[0]},{p[1]},{p[2]})")
print("  " + " ".join(row))

print("\nHORIZONTAL STRIP y=343 (dash/solid?), x 170..890 every 10px:")
row = []
for x in range(170, 890, 10):
    p = img[343, x]
    row.append(f"x{x}:({p[0]},{p[1]},{p[2]})")
print("  " + " ".join(row))
