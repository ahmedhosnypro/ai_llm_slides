from PIL import Image
import numpy as np
from collections import Counter
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_012.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

# 1. Raw look at rows 36..50 at a few x positions (top rule / chrome border zone)
print("== rows 36..50 raw at x=200, x=480, x=700 ==")
for y in range(36, 51):
    print(y, tuple(a[y,200]), tuple(a[y,480]), tuple(a[y,700]))

# 2. Column profiles: where is the chrome panel left/right border (red C00000-ish) columns
print("\n== red-ish px per column, rows 0..540 (R-B>60, R-G>60) ==")
cols = {}
for x in range(W):
    red = sum(1 for y in range(H) if a[y,x,0]-a[y,x,1]>60 and a[y,x,0]-a[y,x,2]>60 and a[y,x,0]>110)
    if red > 30: cols[x] = red
for x in sorted(cols): print(" col", x, cols[x])

# 3. Title box border: exact edges rows 75..85, 135..145; cols
print("\n== title box rows 75..85, cols 85..100 (blue-ish) ==")
for y in range(75, 86):
    bl = [x for x in range(85, 380) if a[y,x,2]-a[y,x,0]>25 and a[y,x,2]>80]
    if bl: print(" row", y, bl[0], "..", bl[-1], "n=", len(bl), "modal", Counter(tuple(a[y,x]) for x in bl).most_common(2))
for y in range(133, 146):
    bl = [x for x in range(85, 380) if a[y,x,2]-a[y,x,0]>25 and a[y,x,2]>80]
    if bl: print(" row", y, bl[0], "..", bl[-1], "n=", len(bl), "modal", Counter(tuple(a[y,x]) for x in bl).most_common(2))
print("\n== title box cols: for each col 85..375, count blue-ish rows 79..140 ==")
for x in range(85, 378):
    bl = sum(1 for y in range(79, 141) if a[y,x,2]-a[y,x,0]>25 and a[y,x,2]>80)
    if bl > 30: print(" col", x, bl, tuple(a[108, x]))
