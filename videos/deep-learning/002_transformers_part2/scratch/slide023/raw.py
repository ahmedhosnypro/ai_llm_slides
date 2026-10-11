from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
print("ROW1 box1 top border row 126-127, x 180..236:")
for y in (126,127):
    print(y, [tuple(im[y,x]) for x in range(180, 237, 8)])
print("ROW1 box1 left border col 172..175, y 130..145:")
for x in (172,174):
    print(x, [tuple(im[y,x]) for y in range(130, 146, 4)])
print("ROW1 container top border row 117..119, x 200..870:")
for y in (117,118,119):
    row = im[y, 200:870:40]
    print(y, [tuple(p) for p in row])
print("ROW1 text red sample:", [tuple(im[y,x]) for y,x in ((136,196),(137,197),(136,206))])
print()
print("ROW2 container border rows 184..188 x 200..870:")
for y in (184,185,186,187):
    print(y, [tuple(p) for p in im[y, 200:870:40]])
print("ROW2 box1 borders: col x 172..178 y 196..216, and row 190..193 x 180..235")
for x in (172,174,176):
    print('col',x, [tuple(im[y,x]) for y in range(196,217,4)])
for y in (190,191,192):
    print('row',y, [tuple(im[y,x]) for x in range(180,236,8)])
print("ROW2 text blue sample:", [tuple(im[y,x]) for y,x in ((205,190),(206,191),(207,192))])
print()
print("ROW3 container rows 258..262 x 200..870:")
for y in (258,259,260,261):
    print(y, [tuple(p) for p in im[y, 200:870:40]])
print("ROW3 box1 left border col x 195..206 y 270..292:")
for x in (196,198,200):
    print('col',x, [tuple(im[y,x]) for y in range(270,293,4)])
print("ROW3 box1 top rows 266..270 x 180..236:")
for y in (266,267,268):
    print('row',y, [tuple(im[y,x]) for x in range(180,236,8)])
print("ROW3 text red sample:", [tuple(im[y,x]) for y,x in ((283,205),(284,206))])
