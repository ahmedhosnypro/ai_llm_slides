from PIL import Image
import numpy as np
im = Image.open('unique_slides/slide_059.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# red border ink: strong red, low green/blue
red = (R > 130) & (G < 90) & (B < 90)

# --- left border column: search cols 30..80, count red rows in y 100..450
lcol = max(((y, x) for y in range(100, 450) for x in range(30, 80) if red[y, x]), key=lambda t: t[1])[1]
# right border column: cols 880..935
rcol = max(((y, x) for y in range(100, 450) for x in range(880, 940) if red[y, x]), key=lambda t: t[0])[1]
# top row: rows 20..70, x 200..700 -> min row with red ink
trow = min(y for y in range(20, 70) for x in range(200, 700) if red[y, x])
# bottom stroke: rows 500..540, x 200..700 -> max row with red ink
brow = max(y for y in range(500, 540) for x in range(200, 700) if red[y, x])
print('left col', lcol, 'right col', rcol, 'top row', trow, 'bottom row', brow)

# --- badge: yellow fill FDFD96-ish top right quadrant
yel = (R > 220) & (G > 220) & (B < 180) & (B > 100)
ys, xs = np.where(yel[30:110, 840:940])
if len(xs):
    bx0, bx1, by0, by1 = xs.min()+840, xs.max()+840, ys.min()+30, ys.max()+30
    print('badge yellow bbox x', bx0, bx1, 'y', by0, by1, 'center', (bx0+bx1)/2, (by0+by1)/2, 'd', bx1-bx0, by1-by0)
else:
    print('no badge yellow found in 840..940 x 30..110')
