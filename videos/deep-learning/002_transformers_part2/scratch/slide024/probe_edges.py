#!/usr/bin/env python3
"""Probe raw pixel colors near expected chrome borders (slide_002 mapping)."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
H, W, _ = img.shape

# expected edges under slide_002-like mapping: L~59 R~902 T~43 B~516
print("row y=250, x 50..70:", [tuple(img[250, x]) for x in range(54, 66)])
print("row y=250, x 895..910:", [tuple(img[250, x]) for x in range(897, 909)])
print("col x=480, y 38..50:", [tuple(img[y, 480]) for y in range(38, 50)])
print("col x=480, y 510..525:", [tuple(img[y, 480]) for y in range(510, 526)])
print("col x=850, y 38..50:", [tuple(img[y, 850]) for y in range(38, 50)])
print("col x=850, y 510..525:", [tuple(img[y, 850]) for y in range(510, 526)])
# what was the red at (135,480)?
print("col x=480, y 130..142:", [tuple(img[y, 480]) for y in range(130, 143)])
# sample panel interior + canvas
print("canvas corner (5,5):", tuple(img[5, 5]), " (30,300):", tuple(img[300, 30]))
print("panel interior (250,480):", tuple(img[250, 480]))
