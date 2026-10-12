#!/usr/bin/env python3
"""slide033 debug2: ASCII map of render left-center + navy-band source hunt."""
import numpy as np
from PIL import Image

ra = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide033/render_1.png").convert("RGB")).astype(int)
RPT = 72 / 150.0
PX = lambda pt: int(pt / RPT)

def ch(px):
    r, g, b = px
    if r > 246 and g > 246 and b > 246: return "."
    if 222 < r <= 246 and 222 < g <= 246 and 222 < b <= 246: return " "
    if r > 228 and g > 200 and 130 < b < 225 and r - b > 20: return "c"
    if r > 215 and 150 < g < 215 and 100 < b < 180 and r - b > 55: return "o"
    if 140 < r < 215 and g > 175 and 110 < b < 210 and g - b > 20 and g - r > 10: return "g"
    if r < 150 and g > 130 and g - r > 30 and g - b > 30: return "G"
    if r > 115 and g < 85 and b < 85: return "R"
    if 100 < r < 160 and 20 < g < 100 and 20 < b < 110 and r - g > 30: return "M"
    if r < 115 and g < 115 and b < 115: return "k"
    if b > 190 and g > 190 and b - r > 8: return "b"
    if b > 110 and r < 110 and b - r > 40: return "B"
    return ":"

print("=== render map x180..430pt, y95..550pt (step 4pt) ===")
print("     " + "".join(str(int(x / 10) % 10) for x in range(180, 430, 4)))
for ypt in range(95, 550, 4):
    row = "".join(ch(ra[PX(ypt), PX(x)]) for x in range(180, 430, 4))
    print(f"{ypt:3d} {row}")

print()
print("=== navy pixel hunt: y225..245pt — sample colors every 12pt ===")
for ypt in range(224, 246, 2):
    samples = []
    for xpt in range(48, 850, 40):
        px = ra[PX(ypt), PX(xpt)]
        samples.append(f"{xpt}:{px[0]},{px[1]},{px[2]}")
    print(f" y{ypt}: " + " ".join(samples))
