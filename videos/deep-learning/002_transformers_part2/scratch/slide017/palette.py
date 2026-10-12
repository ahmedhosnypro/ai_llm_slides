from PIL import Image
import numpy as np
from collections import Counter

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(F)
# quantize to /8 buckets, count, exclude near-white/gray/black
q = (a // 8 * 8).reshape(-1, 3)
cnt = Counter(map(tuple, q))
print("top colors (bucketed, excl achromatic):")
n = 0
for c, k in cnt.most_common(80):
    r, g, b = c
    mx, mn = max(c), min(c)
    if mx - mn < 24:  # achromatic-ish
        continue
    print("  rgb(%3d,%3d,%3d) count %6d" % (r, g, b, k))
    n += 1
    if n >= 40: break
