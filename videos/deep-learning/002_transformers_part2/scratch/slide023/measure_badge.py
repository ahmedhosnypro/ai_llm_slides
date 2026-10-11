from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# badge yellow FDFD96
yellow = (r>230) & (g>230) & (b>110) & (b<200)
ys, xs = np.where(yellow[40:110, 840:930])
ys += 40; xs += 840
print("badge bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max())
print("badge center", (xs.min()+xs.max())/2, (ys.min()+ys.max())/2, "d", xs.max()-xs.min()+1, ys.max()-ys.min()+1)
