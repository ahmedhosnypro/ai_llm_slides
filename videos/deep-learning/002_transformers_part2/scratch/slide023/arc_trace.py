from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
bg = (abs(r-233)<14)&(abs(g-233)<14)&(abs(b-231)<16)
pinkfill = (r>235)&(abs(g-224)<24)&(abs(b-224)<24)
nonbg = ~bg & ~pinkfill
print("arc zone box1->box2 (x228..245) and label zone, y 294..322, nonbg nonfill:")
for y in range(294, 323):
    cs = [(x, tuple(im[y,x])) for x in range(222, 315) if nonbg[y,x]]
    if cs: print(f"  y{y}: {cs[:14]}")
