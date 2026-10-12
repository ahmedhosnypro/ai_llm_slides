#!/usr/bin/env python3
"""Global color census of slide_009.jpg inside the chrome (excl. letterbox)."""
import numpy as np
from PIL import Image
from collections import Counter

im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_009.jpg').convert('RGB'))
# inner area of the chrome panel, excluding letterbox rows >=516
inner = im[46:516, 60:901]
q = (inner // 8 * 8).reshape(-1, 3)
cnt = Counter(map(tuple, q))
print('top 40 quantized colors (count, rgb, hexish):')
for c, n in cnt.most_common(40):
    print(f'{n:8d}  {c}  #{c[0]:02X}{c[1]:02X}{c[2]:02X}')
