from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
red = (r > 100) & (g < 100) & (b < 100) & (r - g > 50) & (r - b > 50)

colcount = red[60:500, :].sum(axis=0)
print("col counts 880..920:", [(x, int(colcount[x])) for x in range(895, 915)])
print("col counts 50..70:", [(x, int(colcount[x])) for x in range(52, 68)])

rowcount = red[:, 100:900].sum(axis=1)
print("row counts 38..50:", [(y, int(rowcount[y])) for y in range(38, 50)])
print("row counts 510..525:", [(y, int(rowcount[y])) for y in range(510, 525)])

# right border: count red pixels per column in y 100..450 only (avoid content)
colcount2 = red[100:450, :].sum(axis=0)
print("col counts (y100..450) 890..915:", [(x, int(colcount2[x])) for x in range(890, 915)])
# top border row scan
rowcount2 = red[:, 200:800].sum(axis=1)
print("row counts (x200..800) 38..52:", [(y, int(rowcount2[y])) for y in range(38, 52)])
