from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_026.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
# Modal colors of the whole image (quantized)
q = (a//16*16).reshape(-1,3)
c = Counter(map(tuple,q))
print('top colors:', c.most_common(12))
# scan each row: modal color of the row (to find bands of tan/yellow fill)
for y in range(0, H, 4):
    row = a[y]
    qc = Counter(map(tuple,(row//8*8)))
    top = qc.most_common(2)
    if top[0][1] > 200:  # dominant row
        print(y, top[0], top[1])
