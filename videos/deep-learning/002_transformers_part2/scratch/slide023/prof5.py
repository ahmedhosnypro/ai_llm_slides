from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# any red tint stronger than pink fill (r-g>50)
redtint = (r-g>50)&(r-b>50)&(r>130)
print("ROW3 red-tint per-row (x150..880):")
for y in range(256, 313):
    c = redtint[y,150:880].sum()
    if c: print(f"  y{y}: {c}")
print()
# luma map of row3 box1 bottom zone: min luma per column, rows 290..300
luma = (0.299*r + 0.587*g + 0.114*b)
print("ROW3 luma min per row, y290..302 (x165..235):")
for y in range(290,303):
    seg = luma[y,165:235]
    print(f"  y{y}: min {seg.min():.0f} at x {165+int(seg.argmin())}, mean {seg.mean():.0f}")
print()
# same check for ROW1 boxes' side borders: luma min per row at box1 left edge x 168..178
print("ROW1 luma min per row y124..150 (x166..180):")
for y in range(124,151):
    seg = luma[y,166:180]
    print(f"  y{y}: min {seg.min():.0f}, mean {seg.mean():.0f}")
