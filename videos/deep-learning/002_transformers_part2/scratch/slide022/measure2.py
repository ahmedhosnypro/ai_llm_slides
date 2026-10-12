from PIL import Image
import numpy as np
from collections import Counter
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg').convert('RGB'))
H, W, _ = im.shape
q = (im//16*16).reshape(-1,3)
cnt = Counter(map(tuple, q))
print("TOP COLORS (16-step quantized):")
for c, n in cnt.most_common(24):
    print(f"  {c} n={n}")
