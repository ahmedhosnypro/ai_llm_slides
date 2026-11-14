from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
im = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)

def runs(mask, axis, minlen, label, limit=50):
    out = []
    if axis == 0:
        for y in range(H):
            row = mask[y]; x = 0
            while x < W:
                if row[x]:
                    x0 = x
                    while x < W and row[x]: x += 1
                    if x - x0 >= minlen: out.append((y, x0, x - 1))
                else: x += 1
    else:
        for x in range(W):
            col = mask[:, x]; y = 0
            while y < H:
                if col[y]:
                    y0 = y
                    while y < H and col[y]: y += 1
                    if y - y0 >= minlen: out.append((x, y0, y - 1))
                else: y += 1
    print(label, out[:limit])

# formula box region only
sub = np.zeros_like(red); sub[255:370, 60:540] = red[255:370, 60:540]
runs(sub, 0, 30, 'formula-region red horiz:')
runs(sub, 1, 20, 'formula-region red vert:')

# matrix1 region red grid
sub = np.zeros_like(red); sub[45:165, 665:875] = red[45:165, 665:875]
runs(sub, 0, 15, 'matrix1 red horiz:')
runs(sub, 1, 10, 'matrix1 red vert:')
# matrix2 region red grid
sub = np.zeros_like(red); sub[160:295, 665:875] = red[160:295, 665:875]
runs(sub, 0, 15, 'matrix2 red horiz:')
runs(sub, 1, 10, 'matrix2 red vert:')

# cell fills in matrix2: sample center colors of 4 quadrants
# find grid: use red lines; sample average color in regions
def avg(x0, y0, x1, y1, label):
    r = a[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0)
    print(label, 'avg rgb', r.round(0))

# matrix2 approx cells: panel x674-867 y169-287; guess split x~770, y~228
for (x0, y0, x1, y1, lab) in [(700, 195, 760, 225, 'm2 TL'), (790, 195, 850, 225, 'm2 TR'),
                              (700, 240, 760, 275, 'm2 BL'), (790, 240, 850, 275, 'm2 BR'),
                              (700, 75, 760, 105, 'm1 TL'), (790, 75, 850, 105, 'm1 TR'),
                              (700, 120, 760, 150, 'm1 BL'), (790, 120, 850, 150, 'm1 BR')]:
    avg(x0, y0, x1, y1, lab)

# node circles: red and green filled circles in tree region
grn = (a[:, :, 1] > 140) & (a[:, :, 0] < 120) & (a[:, :, 2] < 120)
sub = np.zeros_like(grn); sub[290:510, 537:882] = grn[290:510, 537:882]
ys, xs = np.where(sub)
# cluster by y bands
import collections
pts = sorted(zip(xs, ys))
clusters = []
used = np.zeros(len(pts), bool)
for i, (x, y) in enumerate(pts):
    if used[i]: continue
    cx, cy, n = x, y, 1
    for j in range(i + 1, len(pts)):
        if used[j]: continue
        x2, y2 = pts[j]
        if abs(x2 - cx) < 40 and abs(y2 - cy) < 40:
            used[j] = True; n += 1
    clusters.append((cx, cy, n))
print('green clusters (x,y,n):', [c for c in clusters if c[2] > 30])
sub = np.zeros_like(red); sub[290:510, 537:882] = red[290:510, 537:882]
ys, xs = np.where(sub)
pts = sorted(zip(xs, ys))
used = np.zeros(len(pts), bool)
clusters = []
for i, (x, y) in enumerate(pts):
    if used[i]: continue
    cx, cy, n = x, y, 1
    for j in range(i + 1, len(pts)):
        if used[j]: continue
        x2, y2 = pts[j]
        if abs(x2 - cx) < 40 and abs(y2 - cy) < 40:
            used[j] = True; n += 1
    clusters.append((cx, cy, n))
print('red clusters (x,y,n):', [c for c in clusters if c[2] > 30])

# caption: red italic text y 405-435, x 80-540
dark = a.sum(axis=2) < 400
sub = np.zeros_like(dark); sub[405:438, 80:540] = dark[405:438, 80:540]
ys, xs = np.where(sub)
print('caption ink:', (xs.min(), xs.max(), ys.min(), ys.max()) if len(xs) else 'none')

# callout arrows: pale yellow lines between y 330-345 x 100-330
yel = (a[:, :, 0] > 240) & (a[:, :, 1] > 230) & (a[:, :, 2] < 210)
sub = np.zeros_like(yel); sub[325:350, 90:340] = yel[325:350, 90:340]
runs(sub, 0, 8, 'callout-arrow yellow horiz:')
