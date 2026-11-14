from PIL import Image
import numpy as np

NS = '/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure'
im = Image.open(NS + '/unique_slides/slide_010.jpg').convert('RGB')
a = np.asarray(im).astype(int)

# column profile over y 255-370, x 60-660: classify each column by dominant feature
red = (a[:, :, 0] > 150) & (a[:, :, 0] - a[:, :, 1] > 70) & (a[:, :, 0] - a[:, :, 2] > 70)
paleblue = (a[:, :, 2] > 235) & (a[:, :, 0] > 220) & (a[:, :, 0] < 245) & (a[:, :, 1] > 230) & (a[:, :, 2] - a[:, :, 0] > 8)
dark = a.sum(axis=2) < 400
white = a.sum(axis=2) > 720

band = slice(255, 370)
prof = []
for x in range(60, 660):
    r = int(red[band, x].sum()); b = int(paleblue[band, x].sum()); d = int(dark[band, x].sum()); w = int(white[band, x].sum())
    prof.append((x, r, b, d, w))
# print compressed: ranges where red>3, blue>10, dark>3

def ranges(idx, thresh):
    out = []
    inb = False
    for x, *vals in prof:
        v = vals[idx]
        if v > thresh and not inb: s = x; inb = True
        if v <= thresh and inb: out.append((s, x - 1)); inb = False
    if inb: out.append((s, 659))
    return out

print('red-border cols:', ranges(0, 3))
print('paleblue cols:', ranges(1, 10))
print('dark-ink cols:', ranges(2, 3))

# row profile of pale blue box region x 330-530
band2 = slice(280, 360)
rows = []
for y in range(280, 360):
    b = int(paleblue[y, 330:530].sum()); r = int(red[y, 330:530].sum()); d = int(dark[y, 330:530].sum())
    rows.append((y, b, r, d))
print('paleblue rows y280-360 (y, blue, red, dark):', [(y, b, r, d) for y, b, r, d in rows if b > 20 or r > 3 or d > 3][:40])

# where exactly is the fraction bar? dark rows in x 340-475
sub = dark[255:370, 340:475]
rows = sub.sum(axis=1)
print('fraction zone rows:', [(255 + i, int(v)) for i, v in enumerate(rows) if v > 0])

# node circles: better detection - filled circle = wide run of saturated color per row
red2 = (a[:, :, 0] > 140) & (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 60)
grn2 = (a[:, :, 1] > 130) & (a[:, :, 0] < 130) & (a[:, :, 2] < 130)
for lab, mask in [('red', red2), ('green', grn2)]:
    sub = np.zeros_like(mask); sub[330:470, 560:880] = mask[330:470, 560:880]
    rows = sub.sum(axis=1)
    peaks = [(330 + i, int(v)) for i, v in enumerate(rows) if v >= 20]
    # group consecutive
    groups = []
    for y, v in peaks:
        if groups and y - groups[-1][-1][0] <= 2: groups[-1].append((y, v))
        else: groups.append([(y, v)])
    print(lab, 'circle row groups:', [(g[0][0], g[-1][0], max(v for _, v in g)) for g in groups])
    # for each group, x extent at max row
    for g in groups:
        ymax = max(g, key=lambda t: t[1])[0]
        xs = np.where(sub[ymax])[0]
        print('   y', g[0][0], '-', g[-1][0], 'maxw', max(v for _, v in g), 'x at max row:', xs.min(), xs.max())
