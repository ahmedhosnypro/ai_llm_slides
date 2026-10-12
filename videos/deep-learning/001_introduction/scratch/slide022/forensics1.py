from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/001_introduction/unique_slides/slide_022.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print("size", W, "x", H)
r, g, b = a[:,:,0], a[:,:,1], a[:,:,2]

# Red-ish ink mask (C00000 / FF0000 family): strong red, low green/blue
red = (r > 120) & (g < 90) & (b < 90)
# Dark ink (black/navy text)
dark = (r < 110) & (g < 110) & (b < 130)

def bbox(mask, x0=0, y0=0, x1=W, y1=H):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: return None
    return (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), int(sub.sum()))

# 1) red structure rows/cols: which rows have many red px (box borders + title)
rowred = red.sum(axis=1)
print("\n-- rows with >40 red px --")
for y in range(H):
    if rowred[y] > 40:
        xs = np.nonzero(red[y])[0]
        print(f"y={y:3d} n={rowred[y]:4d} x[{xs.min()}..{xs.max()}]")
