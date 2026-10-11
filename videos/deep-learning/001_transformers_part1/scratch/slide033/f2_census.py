#!/usr/bin/env python3
"""Forensics pass 2: dominant-color census inside the peach panel + panel border."""
import numpy as np
from PIL import Image
from collections import Counter

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_033.jpg"
a = np.asarray(Image.open(IMG).convert("RGB")).astype(int)

# panel interior
sub = a[110:520, 54:865]
q = (sub // 8 * 8).reshape(-1, 3)
cnt = Counter(map(tuple, q))
print("== top 25 colors inside panel (quantized /8) ==")
tot = sub.shape[0] * sub.shape[1]
for c, n in cnt.most_common(25):
    print(f"  {c}  {n}  {100*n/tot:.2f}%")

# exact-ish census (no quantization)
cnt2 = Counter(map(tuple, sub.reshape(-1, 3)))
print("== top 15 exact colors in panel ==")
for c, n in cnt2.most_common(15):
    print(f"  {c}  {n}  {100*n/(tot):.2f}%")

# canvas + chrome check rows
print("== rows 0..12 col 480:", [tuple(a[y, 480]) for y in (0, 3, 6, 10, 20, 30)])
print("== col 30..60 row 300:", [tuple(a[300, x]) for x in (30, 40, 42, 44, 48, 52, 56)])
print("== badge region rows 40..100 col 860..930 unique-ish:")
from collections import Counter
bc = Counter(map(tuple, a[40:105, 855:935].reshape(-1, 3)))
for c, n in bc.most_common(8):
    print("   ", c, n)
