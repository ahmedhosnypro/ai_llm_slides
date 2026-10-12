from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
red = (r > 120) & (g < 90) & (b < 90)

# horizontal border lines: rows where a contiguous red run >= 200px exists
print("-- horizontal red runs >=150px --")
for y in range(H):
    row = red[y]
    xs = np.nonzero(row)[0]
    if len(xs) < 150: continue
    # find longest run
    runs = []
    start = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x - prev > 3:
            runs.append((start, prev)); start = x
        prev = x
    runs.append((start, prev))
    long_runs = [rn for rn in runs if rn[1]-rn[0] >= 150]
    if long_runs:
        print(f"y={y:3d}", long_runs)

print("\n-- vertical red runs >=100px --")
colred = red.sum(axis=0)
for x in range(W):
    if colred[x] < 100: continue
    ys = np.nonzero(red[:, x])[0]
    runs = []
    start = ys[0]; prev = ys[0]
    for y in ys[1:]:
        if y - prev > 3:
            runs.append((start, prev)); start = y
        prev = y
    runs.append((start, prev))
    long_runs = [rn for rn in runs if rn[1]-rn[0] >= 100]
    if long_runs:
        print(f"x={x:3d} n={colred[x]:4d}", long_runs)
