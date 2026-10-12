from PIL import Image
import numpy as np
im = np.asarray(Image.open('unique_slides/slide_022.jpg').convert('RGB')).astype(int)
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
# gray panel color E8E8E4-ish: r,g in 225..240, b in 222..238, |r-g|<6
gray = (np.abs(r-232)<9) & (np.abs(g-232)<9) & (np.abs(b-229)<10) & (np.abs(r-g)<8)
ys, xs = np.where(gray)
print('gray bbox: x', xs.min(), '..', xs.max(), ' y', ys.min(), '..', ys.max(), 'n', len(ys))
colcount = gray.sum(axis=0)
rowcount = gray.sum(axis=1)
# columns with lots of gray
big_cols = np.where(colcount > 200)[0]
print('gray-heavy columns:', big_cols.min(), '..', big_cols.max(), 'count', len(big_cols))
big_rows = np.where(rowcount > 300)[0]
print('gray-heavy rows:', big_rows.min(), '..', big_rows.max(), 'count', len(big_rows))
# per-column gray extents at specific columns
for x in (43, 60, 100, 500, 900, 915, 917):
    c = np.where(gray[:, x])[0]
    print(f'gray col x={x}: rows {c.min() if len(c) else "-"}..{c.max() if len(c) else "-"} n={len(c)}')
for y in (50, 60, 250, 470, 500, 510):
    c = np.where(gray[y, :])[0]
    print(f'gray row y={y}: cols {c.min() if len(c) else "-"}..{c.max() if len(c) else "-"} n={len(c)}')
# reddish long vertical lines (border candidates)
reddish = (r - g > 30) & (r - b > 20) & (r > 110)
redcount = reddish.sum(axis=0)
vcands = np.where(redcount > 80)[0]
print('reddish-heavy columns:', vcands.tolist())
redrow = reddish.sum(axis=1)
hcands = np.where(redrow > 200)[0]
print('reddish-heavy rows:', hcands.tolist())
