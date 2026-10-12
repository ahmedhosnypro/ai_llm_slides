from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]
# loose reddish: red clearly dominant over green/blue
red = (r > g + 50) & (r > b + 50) & (r > 110)

print("-- vertical loose-red: cols with >=80 px --")
colred = red.sum(axis=0)
for x in range(W):
    if colred[x] < 80: continue
    ys = np.nonzero(red[:, x])[0]
    runs = []
    start = ys[0]; prev = ys[0]
    for y in ys[1:]:
        if y - prev > 4:
            runs.append((int(start), int(prev))); start = y
        prev = y
    runs.append((int(start), int(prev)))
    print(f"x={x:3d} n={colred[x]:4d} runs={runs}")

print("\n-- horizontal loose-red rows with >=120 px --")
rowred = red.sum(axis=1)
for y in range(H):
    if rowred[y] < 120: continue
    xs = np.nonzero(red[y])[0]
    runs = []
    start = xs[0]; prev = xs[0]
    for x in xs[1:]:
        if x - prev > 4:
            runs.append((int(start), int(prev))); start = x
        prev = x
    runs.append((int(start), int(prev)))
    long = [rn for rn in runs if rn[1]-rn[0] >= 100]
    if long:
        print(f"y={y:3d} n={rowred[y]:4d} longruns={long}")
