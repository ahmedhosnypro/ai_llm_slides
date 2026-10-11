from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
red = (r > 110) & (r - g > 50) & (r - b > 50)

colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
top_cols = sorted(range(W), key=lambda x: -colcount[x])[:12]
top_rows = sorted(range(H), key=lambda y: -rowcount[y])[:12]
print("top cols:", sorted([(x, int(colcount[x])) for x in top_cols]))
print("top rows:", sorted([(y, int(rowcount[y])) for y in top_rows]))

# Black letterbox: rows that are near-black across most of width
dark = (r < 40) & (g < 40) & (b < 40)
darkrow = dark.sum(axis=1)
print("rows >800 dark px:", [y for y in range(H) if darkrow[y] > 800])
