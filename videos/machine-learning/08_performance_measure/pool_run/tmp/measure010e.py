from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
im = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(im).astype(int)

# strict blue text: blue dominant, not dark-sum
blue_txt = (a[:, :, 2] > 140) & (a[:, :, 2] - a[:, :, 0] > 50) & (a[:, :, 2] - a[:, :, 1] > 30)
dark = a.sum(axis=2) < 400
red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)

# blue text in formula/precision zone
sub = np.zeros_like(blue_txt); sub[280:360, 330:660] = blue_txt[280:360, 330:660]
ys, xs = np.where(sub)
print('blue text x330-660 y280-360:', (xs.min(), xs.max(), ys.min(), ys.max(), len(xs)) if len(xs) else 'none')
# row bands of blue text
rows = sub.sum(axis=1)
bands = []
inb = False
for y in range(280, 360):
    if rows[y] > 0 and not inb: s = y; inb = True
    if rows[y] == 0 and inb: bands.append((s, y - 1)); inb = False
if inb: bands.append((s, 359))
print('blue text row bands:', bands)
for b0, b1 in bands:
    cols = sub[b0:b1 + 1].sum(axis=0)
    nz = np.where(cols > 0)[0]
    print(f'  band y{b0}-{b1}: x {nz.min()}-{nz.max()}')

# fraction bar: horizontal dark run in x330-540, y295-335
sub2 = np.zeros_like(dark); sub2[295:335, 330:540] = dark[295:335, 330:540]
rows = sub2.sum(axis=1)
print('dark rows y295-335 x330-540:', [(295 + i, int(v)) for i, v in enumerate(rows) if v > 40])

# dark ink bands in x330-540 y290-340 (fraction + precision text)
sub3 = np.zeros_like(dark); sub3[290:340, 330:540] = dark[290:340, 330:540]
rows = sub3.sum(axis=1)
bands = []
inb = False
for y in range(290, 340):
    if rows[y] > 0 and not inb: s = y; inb = True
    if rows[y] == 0 and inb: bands.append((s, y - 1)); inb = False
if inb: bands.append((s, 339))
print('dark bands y290-340 x330-540:', bands)
for b0, b1 in bands:
    cols = sub3[b0:b1 + 1].sum(axis=0)
    nz = np.where(cols > 0)[0]
    print(f'  band y{b0}-{b1}: x {330+nz.min()}-{330+nz.max()}')

# callout boxes: find their borders - non-white rows/cols in x80-330 y318-380
nonwhite = a.sum(axis=2) < 700
sub4 = np.zeros_like(nonwhite); sub4[315:385, 75:335] = nonwhite[315:385, 75:335]
rows = sub4.sum(axis=1)
print('callout zone rows:', [(315 + i, int(v)) for i, v in enumerate(rows) if v > 20])
cols = sub4.sum(axis=0)
print('callout zone cols:', [(75 + i, int(v)) for i, v in enumerate(cols) if v > 20])

# arrows from fraction/denominator to callouts: gray/yellow lines y 330-350 x 100-330
gray = (a.sum(axis=2) > 250) & (a.sum(axis=2) < 620)
sub5 = np.zeros_like(gray); sub5[328:352, 90:340] = gray[328:352, 90:340]
rows = sub5.sum(axis=1)
print('arrow zone rows y328-352:', [(328 + i, int(v)) for i, v in enumerate(rows) if v > 5])
