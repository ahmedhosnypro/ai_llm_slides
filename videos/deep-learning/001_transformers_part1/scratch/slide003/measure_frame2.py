from PIL import Image
import numpy as np

im = Image.open('unique_slides/slide_003.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# looser red mask
red = (r > 120) & (r - g > 50) & (r - b > 50)
print("total red px:", red.sum())

# column profile in title band
band = red[30:110, :]
cols = band.sum(axis=0)
nz = np.where(cols > 0)[0]
print("title band red cols min/max:", nz.min(), nz.max())
# find word clusters (gaps > 8px)
clusters = []
start = nz[0]; prev = nz[0]
for x in nz[1:]:
    if x - prev > 8:
        clusters.append((start, prev)); start = x
    prev = x
clusters.append((start, prev))
print("title word clusters (x-ranges):", clusters)

# red frame: scan full slide for long horizontal / vertical red runs
row_red = red.sum(axis=1)
col_red = red.sum(axis=0)
print("rows with >300 red px:", [int(y) for y in np.where(row_red > 300)[0]])
print("cols with >200 red px:", [int(x) for x in np.where(col_red > 200)[0]])

# vertical border lines: columns where red spans many rows
for x in np.where(col_red > 150)[0]:
    ys = np.where(red[:, x])[0]
    print(f"  col x={x}: red y=[{ys.min()},{ys.max()}] count={red[:,x].sum()}")

# horizontal border lines
for y in np.where(row_red > 150)[0]:
    xs = np.where(red[y, :])[0]
    print(f"  row y={y}: red x=[{xs.min()},{xs.max()}] count={red[y,:].sum()}")

# title band: check for ink just left of 225 and right of 619 with even looser mask
loose = (r - g > 35) & (r - b > 35) & (r > 100)
band2 = loose[30:110, :]
cols2 = np.where(band2.sum(axis=0) > 0)[0]
print("loose title cols:", cols2.min(), cols2.max())
# vertical extent of loose title
rows2 = np.where(band2.sum(axis=1) > 0)[0]
print("loose title rows (offset+30):", rows2.min()+30, rows2.max()+30)
