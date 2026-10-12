from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
print("--- samples in slab strip (y=370) ---")
for x in range(385, 800, 15):
    print(x, tuple(a[370, x]))
print("--- y=510 row samples ---")
for x in (100, 200, 300, 400, 500, 700):
    print(x, tuple(a[510, x]), tuple(a[511, x]), tuple(a[508, x]))
print("--- purple slab vertical extent at x=520,530 ---")
for x in (520, 530, 545):
    col = a[:, x]
    for y in range(330, 405):
        rr, gg, bb = col[y]
        if abs(rr-128)<60 and bb>80 and gg<90 and not (rr>180):
            pass
# simpler: print colors x=520 y 335..400
print("--- x=520 col ---")
for y in range(333, 402, 2):
    print(y, tuple(a[y, 520]))
