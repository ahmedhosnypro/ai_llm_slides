from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

def classify(c):
    r, g, b = c
    if r > 235 and g > 235 and b > 235: return 'W'   # white
    if abs(r-g) < 14 and abs(g-b) < 14 and 200 < r < 240: return '.'  # gray bg
    if r > 200 and g > 200 and b < 190: return 'y'   # pale yellow
    if r > 170 and 140 < g < 215 and b < 200 and r > b + 15: return 't'  # tan
    if r > 130 and g < 100 and b < 100: return 'R'   # red ink
    if r < 120 and g < 120 and b < 130: return 'k'   # dark ink
    if b > r + 40 and b > 120: return 'B'            # blue ink
    if r > 180 and b > 180 and g < 160: return 'm'   # pink/magenta
    if r > 180 and g > 220 and b > 220: return 'c'   # cyan
    return '?'

# ASCII map: 4px cells
print("    " + "".join(str((x//100)%10) for x in range(0, W, 4)))
for y in range(0, H, 4):
    row = []
    for x in range(0, W, 4):
        cell = a[y:y+4, x:x+4].reshape(-1, 3)
        # modal class of the cell
        from collections import Counter
        cnt = Counter(classify(tuple(c)) for c in cell)
        row.append(cnt.most_common(1)[0][0])
    print(f"{y:3d} " + "".join(row))
