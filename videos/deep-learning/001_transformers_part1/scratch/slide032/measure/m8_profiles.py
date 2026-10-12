# m8_profiles.py — raw pixel profiles through the matrix
import numpy as np
from PIL import Image
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
a = np.asarray(Image.open(F).convert("RGB")).astype(int)
print("=== vertical profile x=240 (cell1, avoids text?) y=82..262")
for y in range(82,263,1):
    r,g,b = a[y,240]
    tag = ""
    if max(r,g,b)<235: tag=" <== non-white"
    print(f"y{y:3d} #{r:02X}{g:02X}{b:02X}{tag}")
