from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
im = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def avg(x0, y0, x1, y1, label):
    r = a[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0)
    print(label, 'avg rgb', r.round(0))

# matrix2 cell centers with grid x705-801-857, y192-253-283
avg(715, 200, 790, 245, 'm2 cell 18 (TL)')
avg(810, 200, 850, 245, 'm2 cell 12 (TR)')
avg(715, 258, 790, 278, 'm2 cell 10 (BL)')
avg(810, 258, 850, 278, 'm2 cell 60 (BR)')
# matrix1 cell centers: grid x699-~792-857, y78-125-150
avg(705, 85, 785, 118, 'm1 cell TP (TL)')
avg(800, 85, 850, 118, 'm1 cell FN (TR)')
avg(705, 128, 785, 146, 'm1 cell FP (BL)')
avg(800, 128, 850, 146, 'm1 cell TN (BR)')

# fraction location: dark ink in x320-470, y255-370, column profile
dark = a.sum(axis=2) < 400
sub = dark[255:370, 320:470]
cols = sub.sum(axis=0)
rows = sub.sum(axis=1)
nz = np.where(cols > 0)[0]
print('fraction-region ink cols x:', (320 + nz.min(), 320 + nz.max()) if len(nz) else 'none')
nzr = np.where(rows > 0)[0]
print('fraction-region ink rows y:', (255 + nzr.min(), 255 + nzr.max()) if len(nzr) else 'none')
# row bands
bands = []
inb = False
for i, v in enumerate(rows):
    if v > 0 and not inb: s = i; inb = True
    if v == 0 and inb: bands.append((255 + s, 255 + i - 1)); inb = False
if inb: bands.append((255 + s, 255 + len(rows) - 1))
print('fraction-region row bands:', bands)

# precision text: dark ink x460-640 y285-350
sub = dark[285:350, 460:640]
cols = sub.sum(axis=0); rows = sub.sum(axis=1)
nz = np.where(cols > 0)[0]; nzr = np.where(rows > 0)[0]
print('precision ink x:', (460 + nz.min(), 460 + nz.max()), 'y:', (285 + nzr.min(), 285 + nzr.max()))

# plane columns: gray ink (sum 250-600) rows in x588-678 and x764-854
gray = (a.sum(axis=2) > 250) & (a.sum(axis=2) < 620)
for x0, x1, lab in [(588, 678, 'pos plane'), (764, 854, 'neg plane')]:
    rows = gray[300:400, x0:x1].sum(axis=1)
    nzr = np.where(rows > 2)[0]
    print(lab, 'ink rows y:', (300 + nzr.min(), 300 + nzr.max()) if len(nzr) else 'none')
    cols = gray[300:400, x0:x1].sum(axis=0)
    nz = np.where(cols > 2)[0]
    print(lab, 'ink cols x:', (x0 + nz.min(), x0 + nz.max()) if len(nz) else 'none')

# node circles: sample dominant color in 25x25 windows at candidate centers
red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
grn = (a[:, :, 1] > 140) & (a[:, :, 0] < 120) & (a[:, :, 2] < 120)
for cx, cy, lab in [(642, 367, 'node30'), (807, 367, 'node70'), (592, 437, 'node18'),
                    (687, 437, 'node12'), (757, 437, 'node60'), (852, 437, 'node10')]:
    w = slice(cy - 12, cy + 13), slice(cx - 12, cx + 13)
    r = int(red[w].sum()); g = int(grn[w].sum())
    print(lab, 'red px', r, 'green px', g)

# find actual circle centers: scan for rows where red/green fill is wide (circle diameter ~30px)
for lab, mask in [('red', red), ('green', grn)]:
    sub = np.zeros_like(mask); sub[330:470, 560:880] = mask[330:470, 560:880]
    rows = sub.sum(axis=1)
    peaks = [(330 + i, int(v)) for i, v in enumerate(rows) if v > 18]
    print(lab, 'circle rows (y, width):', peaks)

# caption: red-ish italic text y 405-435
sub = np.zeros_like(red); sub[403:438, 80:560] = red[403:438, 80:560]
ys, xs = np.where(sub)
print('caption red ink x:', (xs.min(), xs.max()), 'y:', (ys.min(), ys.max()), 'n=', len(xs))
# also dark caption
dsub = np.zeros_like(dark); dsub[403:438, 80:560] = dark[403:438, 80:560]
ys, xs = np.where(dsub)
print('caption dark ink x:', (xs.min(), xs.max()), 'y:', (ys.min(), ys.max()), 'n=', len(xs))

# callout boxes: fills in y 320-375 x 80-330
for y0, y1 in [(320, 375)]:
    for x0, x1 in [(80, 200), (200, 330)]:
        r = a[y0:y1, x0:x1].reshape(-1, 3).mean(axis=0)
        print(f'callout region x{x0}-{x1} y{y0}-{y1} avg', r.round(0))
# callout box borders (thin lines) - find horiz lines of any non-white in y 318-378
nonwhite = a.sum(axis=2) < 720
sub = np.zeros_like(nonwhite); sub[318:380, 80:330] = nonwhite[318:380, 80:330]
rows = sub.sum(axis=1)
print('callout rows with ink:', [(318 + i, int(v)) for i, v in enumerate(rows) if v > 30])
