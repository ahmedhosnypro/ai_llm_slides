from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
red = (r > 130) & (g < 90) & (b < 90)

# Vertical red strokes: columns with many red pixels (panel left/right borders)
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
print("columns with >100 red px:", [(x, int(colcount[x])) for x in range(W) if colcount[x] > 100])
print()
print("rows with >200 red px:", [(y, int(rowcount[y])) for y in range(H) if rowcount[y] > 200])
