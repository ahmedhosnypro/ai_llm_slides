#!/usr/bin/env python3
# debug2.py — sample colors in arrow bands, box border, relaxed white text, green circle profile.
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_056.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

# 1) blue arrow band y 185..222: count non-background pixels and their colors
band = a[185:222, 150:850]
mask = (np.abs(band[..., 0] - 233) > 25) | (np.abs(band[..., 1] - 233) > 25) | (np.abs(band[..., 2] - 231) > 25)
ys, xs = np.nonzero(mask)
print("blue-arrow band non-bg count:", len(xs))
if len(xs):
    cols = band[ys, xs]
    print("  mean color:", cols.mean(axis=0).round(0), " y-extent frame:", ys.min() + 185, ys.max() + 185, " x-extent:", xs.min() + 150, xs.max() + 150)
    # cluster columns
    colhit = mask.sum(axis=0)
    runs, s = [], None
    for i, v in enumerate(colhit > 0):
        if v and s is None: s = i
        elif not v and s is not None:
            runs.append((s + 150, i - 1 + 150)); s = None
    print("  n runs:", len(runs), "first/last:", runs[:2], runs[-2:] if len(runs) > 2 else "")

# 2) red arrow band y 273..296
band = a[273:296, 150:850]
mask = (band[..., 0] - band[..., 1] > 60) & (band[..., 0] - band[..., 2] > 50)
ys, xs = np.nonzero(mask)
print("red-arrow band count:", len(xs))
if len(xs):
    print("  mean color:", band[ys, xs].mean(axis=0).round(0), " y-extent:", ys.min() + 273, ys.max() + 273)

# 3) green arrow band y 436..460, x 250..700
band = a[436:461, 250:700]
mask = (band[..., 1] - band[..., 0] > 50) & (band[..., 1] - band[..., 2] > 50)
ys, xs = np.nonzero(mask)
print("green-arrow band count:", len(xs))
if len(xs):
    print("  mean color:", band[ys, xs].mean(axis=0).round(0), " y-extent:", ys.min() + 436, ys.max() + 436)
    colhit = mask.sum(axis=0)
    runs, s = [], None
    for i, v in enumerate(colhit > 0):
        if v and s is None: s = i
        elif not v and s is not None:
            runs.append((s + 250, i - 1 + 250)); s = None
    print("  runs:", runs)

# 4) softmax bar white text with relaxed mask
bar = a[228:268, 170:826]
wm = (bar[..., 0] > 190) & (bar[..., 1] > 190) & (bar[..., 2] > 190)
ys, xs = np.nonzero(wm)
print("softmax white text:", len(xs), "bbox x", xs.min() + 170, xs.max() + 170, "y", ys.min() + 228, ys.max() + 228)

# 5) blue bar white text relaxed
bar = a[465:497, 170:826]
wm = (bar[..., 0] > 190) & (bar[..., 1] > 190) & (bar[..., 2] > 190)
ys, xs = np.nonzero(wm)
print("bluebar white text:", len(xs), "bbox x", xs.min() + 170, xs.max() + 170, "y", ys.min() + 465, ys.max() + 465)
# column histogram to see separate blobs (pen cursor?)
colhit = wm.sum(axis=0)
gaps = [i + 170 for i in range(len(colhit)) if colhit[i] == 0]
# print runs
runs, s = [], None
for i, v in enumerate(colhit > 0):
    if v and s is None: s = i
    elif not v and s is not None:
        runs.append((s + 170, i - 1 + 170)); s = None
print("  text runs:", runs)

# 6) green box border: horizontal green rows near top/bottom, vertical cols
green = (g - r > 40) & (g - b > 40) & (g > 100)
rowg = green[280:460, 150:800].sum(axis=1)
print("green rows (top/bottom border candidates):", [(y + 280, int(rowg[y])) for y in range(len(rowg)) if rowg[y] > 200])
colg = green[300:430, 100:860].sum(axis=0)
print("green cols (left/right border candidates):", [(x + 100, int(colg[x])) for x in range(len(colg)) if colg[x] > 60])

# 7) pale green fill left edge at y=360: where does fill start?
row = a[360, 100:200]
print("row y=360 x100..199 r:", [(x + 100, int(row[x - 100][0]), int(row[x - 100][1]), int(row[x - 100][2])) for x in range(100, 200, 8)])

# 8) green circle vertical profile at x=398
col = a[385:440, 398]
gm = (col[:, 1] - col[:, 0] > 40) & (col[:, 1] - col[:, 2] > 40)
print("green circle col x=398 y-extent:", [385 + i for i in range(len(gm)) if gm[i]])

# 9) color samples: pale circle outline, magenta, green circle, line, brace, arrows, bars
def sample(name, x, y):
    print(f"  {name} @({x},{y}):", tuple(a[y, x]))
sample("pale_fill", 197, 159)
sample("pale_outline", 184, 159)
sample("magenta", 197, 335)
sample("green_circle", 398, 409)
sample("bar_softmax", 300, 245)
sample("bar_blue", 300, 480)
sample("box_fill", 300, 380)
sample("box_border_top", 400, 297)
sample("conn_line", 300, 370)

# 10) pen cursor crop around 'Block' end
Image.fromarray(np.uint8(a[460:500, 560:660])).resize((400, 160), Image.NEAREST).save(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide056/crop_cursor.png")
print("saved crop_cursor.png")
