from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("size", W, H)
r, g, b = a[...,0], a[...,1], a[...,2]

# red ink mask (title, border, bottom rule): strong red dominance
red = (r > 120) & (r - g > 60) & (r - b > 60)
ys, xs = np.nonzero(red)
print("RED ink total px:", len(xs))

# Panel border: find vertical red strokes near x~39-45 and x~915-921 (columns with many red px)
colcount = red.sum(axis=0)
rowcount = red.sum(axis=1)
print("columns with >=300 red px:", [x for x in range(W) if colcount[x] >= 300])
print("rows with >=300 red px:", [y for y in range(H) if rowcount[y] >= 300])

# Bottom rule: red rows in bottom 30 rows
for y in range(H-25, H):
    if rowcount[y] > 50:
        xs_r = np.nonzero(red[y])[0]
        print("bottom rule row", y, "x", xs_r.min(), xs_r.max(), "count", len(xs_r))

# Badge: yellow mask
yellow = (r > 200) & (g > 200) & (b < 160)
ys_y, xs_y = np.nonzero(yellow)
if len(xs_y):
    print("badge yellow bbox x", xs_y.min(), xs_y.max(), "y", ys_y.min(), ys_y.max(),
          "center", (xs_y.min()+xs_y.max())/2, (ys_y.min()+ys_y.max())/2)
# purple ring
purple = (b > 140) & (r > 70) & (r < 180) & (b - g > 40)
ys_p, xs_p = np.nonzero(purple)
if len(xs_p):
    print("purple ring bbox x", xs_p.min(), xs_p.max(), "y", ys_p.min(), ys_p.max(), "count", len(xs_p))

# gray panel extent: rows/cols where pixel ~ E9E9E7
gray = (abs(r-233)<8) & (abs(g-233)<8) & (abs(b-231)<10)
rowg = gray.sum(axis=1); colg = gray.sum(axis=0)
# find panel bounds: first/last row where >600 gray px
rows_g = [y for y in range(H) if rowg[y] > 600]
cols_g = [x for x in range(W) if colg[x] > 400]
print("gray panel rows", rows_g[0], rows_g[-1], "cols", cols_g[0], cols_g[-1])

# Title ink: red pixels inside panel, excluding border cols/rows and bottom rule
inner = red.copy()
inner[:, :55] = False; inner[:, 905:] = False
inner[:60, :] = False; inner[520:, :] = False
ys_t, xs_t = np.nonzero(inner)
print("TITLE ink bbox x", xs_t.min(), xs_t.max(), "y", ys_t.min(), ys_t.max(),
      "center x", (xs_t.min()+xs_t.max())/2, "center y", (ys_t.min()+ys_t.max())/2)
# per-row profile of title ink to find cap height / descender
rr = inner.sum(axis=1)
bands = [y for y in range(60,520) if rr[y] > 3]
print("title rows with ink:", bands[0], "..", bands[-1])
# column profile -> text advance
cc = inner.sum(axis=0)
cols_t = [x for x in range(55,905) if cc[x] > 0]
print("title cols:", cols_t[0], "..", cols_t[-1], "width px:", cols_t[-1]-cols_t[0]+1)
