from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# looser red
red = (r - g > 35) & (r - b > 35) & (r > 90)
colcount = red.sum(axis=0); rowcount = red.sum(axis=1)
print("cols 890..915:", [(x, int(colcount[x])) for x in range(890,916) if colcount[x]>10])
print("rows 30..60:", [(y, int(rowcount[y])) for y in range(30,61) if rowcount[y]>10])
print("rows 60..80:", [(y, int(rowcount[y])) for y in range(60,81) if rowcount[y]>100])
print("rows 505..522:", [(y, int(rowcount[y])) for y in range(505,523) if rowcount[y]>100])
print("cols 50..70:", [(x, int(colcount[x])) for x in range(50,71) if colcount[x]>100])

# gray panel extent: E9E9E7-ish pixels
gray = (abs(r-233)<12) & (abs(g-233)<12) & (abs(b-231)<14)
graycol = gray.sum(axis=0); grayrow = gray.sum(axis=1)
xs = [x for x in range(W) if graycol[x] > 200]
ys = [y for y in range(H) if grayrow[y] > 200]
print("gray panel x range:", min(xs), max(xs))
print("gray panel y range:", min(ys), max(ys))
# white canvas left of panel?
print("white col sample x=20..58:", [(x,int(((r[:,x]>245)&(g[:,x]>245)&(b[:,x]>245)).sum())) for x in range(20,59,4)])
