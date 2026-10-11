from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

red_s = (r>120)&(r-g>40)&(r-b>40)   # strong red
red_w = (r-g>12)&(r-b>12)&(r>195)   # weak/pale red
blue  = (b-r>28)&(b>150)

print("ROW3 strong-red per-row count (x150..880):")
for y in range(256, 313):
    c = red_s[y,150:880].sum()
    if c: print(f"  y{y}: {c}")
print("ROW1 weak-red per-row count (x150..880):")
for y in range(114, 162):
    c = red_w[y,150:880].sum()
    if c: print(f"  y{y}: {c}")
print("ROW2 blue per-row count (x150..880):")
for y in range(182, 232):
    c = blue[y,150:880].sum()
    if c: print(f"  y{y}: {c}")
