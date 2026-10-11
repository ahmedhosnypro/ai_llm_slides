# Pass 7: corridor red map, sentence metrics, icon maps, hatch pitch, border scans.
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_024.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 140) & (g < 120) & (b < 120)

print("== CORRIDOR red map x[140,470] y[280,460] step 3 (cols=110, rows=60)")
print("     " + ''.join(str(((140 + i * 3) // 10) % 10) for i in range(111)))
for yy in range(280, 461, 3):
    row = []
    for i in range(111):
        xx = 140 + i * 3
        n = red[yy:yy + 3, xx:xx + 3].sum()
        row.append('#' if n >= 4 else ('+' if n >= 1 else '.'))
    print(f"y{yy:3d} " + ''.join(row))

# sentence text metrics
blk = (r < 90) & (g < 90) & (b < 90)
sub = blk[105:145, 480:905]
ys, xs = np.nonzero(sub)
print(f"\nSENTENCE ink bbox: x[{480+xs.min()},{480+xs.max()}] y[{105+ys.min()},{105+ys.max()}] w={xs.max()-xs.min()+1}")
# column profile to find word gaps
colsum = sub.sum(axis=0)
runs = []
inrun = False
for i, v in enumerate(colsum):
    if v > 0 and not inrun: start = i; inrun = True
    elif v == 0 and inrun: runs.append((480 + start, 480 + i - 1)); inrun = False
if inrun: runs.append((480 + start, 480 + len(colsum) - 1))
print("word runs:", runs)

def amap(x0, y0, x1, y1, label):
    print(f"== {label} x[{x0},{x1}] y[{y0},{y1}]")
    for yy in range(y0, y1):
        row = []
        for xx in range(x0, x1):
            p = a[yy, xx]
            if b[yy, xx] > 120 and b[yy, xx] - p[0] > 40 and p[1] < b[yy, xx]: c = 'B'
            elif p[0] > 190 and 60 < p[1] < 190 and p[2] < 110: c = 'O'
            elif p[0] > 140 and p[1] < 120 and p[2] < 120: c = 'R'
            elif p[0] > 228 and p[1] > 228 and p[2] > 228: c = 'w'
            elif p[0] < 90 and p[1] < 90 and p[2] < 90: c = '#'
            else: c = '.'
            row.append(c)
        print(''.join(row))

amap(118, 140, 164, 205, "'in' icon wide")
amap(778, 322, 836, 428, "orange icon full")

print("\n-- block arrow hatch scan y=297, x520..648 (dark runs) --")
row = a[297, 520:648]
dark = [(520 + i, tuple(p)) for i, p in enumerate(row) if p[0] < 235 and abs(int(p[0]) - int(p[2])) < 40]
print(''.join('X' if p[0] < 200 and p[0] - p[1] > 20 else ('x' if p[0] < 235 else '.') for p in row))

def scanv(x, y0, y1, label):
    print(f"-- vscan x={x} {label}:")
    for y in range(y0, y1):
        p = a[y, x]
        print(f"   y={y} ({p[0]:3d},{p[1]:3d},{p[2]:3d})")

scanv(268, 236, 246, "Boy(in) top edge")
scanv(202, 94, 102, "'in' top edge")

# input-Boy blue icon bbox via db edges
db = (b > 130) & (b - r > 60) & (g < 140)
lab = None
from scipy import ndimage
l, n = ndimage.label(db)
print("\ndb clusters 25-90px (icon edges):")
for i in range(1, n + 1):
    m = l == i
    s = int(m.sum())
    if 25 <= s <= 200:
        ys2, xs2 = np.nonzero(m)
        h = ys2.max() - ys2.min() + 1
        if h > 30:
            print(f"  x[{xs2.min()},{xs2.max()}] y[{ys2.min()},{ys2.max()}] n={s}")
