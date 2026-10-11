from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

bg = (abs(r-233)<14)&(abs(g-233)<14)&(abs(b-231)<16)
ink = ~bg
print("non-bg rows 305..350 (x150..899):")
for y in range(305, 351):
    c = ink[y, 150:899].sum()
    if c: print(f"  y{y}: {int(c)}")
# sample colors in row 312-316
print("row 313 non-bg pixels:", [(x, tuple(im[313,x])) for x in range(150,899) if not bg[313,x]][:40])
print("row 315 non-bg pixels:", [(x, tuple(im[315,x])) for x in range(150,899) if not bg[315,x]][:40])
print("row 318 non-bg pixels:", [(x, tuple(im[318,x])) for x in range(150,899) if not bg[318,x]][:40])
