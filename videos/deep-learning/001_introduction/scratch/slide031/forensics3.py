#!/usr/bin/env python3
"""Forensics pass 3: chrome check, matrix box, filter-params box, black bar, bullets, fonts."""
from PIL import Image
import numpy as np
from collections import Counter

P = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_031.jpg"
im = Image.open(P).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
lum = a.mean(axis=2)

def modal(box, sel=None):
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    if sel == "dark": sub = sub[sub.mean(axis=1) < 120]
    elif sel == "red": sub = sub[(sub[:,0] > 100) & (sub[:,1] < 90) & (sub[:,2] < 90)]
    if len(sub) == 0: return None, 0
    return Counter(map(tuple, sub)).most_common(1)[0], len(sub)

# 1. chrome presence: red count in cols 40-46, 916-922 over y 46..517; gray fill samples
for x0, x1 in ((40, 47), (915, 923)):
    band = a[46:517, x0:x1]
    redm = (band[:,:,0] > 120) & (band[:,:,1] < 80) & (band[:,:,2] < 80)
    print(f"cols {x0}-{x1}: red px {redm.sum()}, max per col {redm.sum(axis=0).max()}")
print("fill samples (500,60):", tuple(a[60,500]), "(60,300):", tuple(a[300,60]), "(900,300):", tuple(a[300,900]), "(500,40):", tuple(a[40,500]))
# red top line? rows 40..60 red counts
for y in range(40, 62):
    row = a[y, 100:900]
    redm = (row[:,0] > 120) & (row[:,1] < 80) & (row[:,2] < 80)
    if redm.sum() > 30: print("red row", y, redm.sum())

# 2. black bar x extent (row 528)
row = lum[528]
xs = np.where(row < 60)[0]
print("black bar row528 x:", xs.min(), "..", xs.max())

# 3. matrix box: red borders. scan cols 600..900 for vertical red runs in y 388..502
red = (a[:,:,0] > 120) & (a[:,:,1] < 80) & (a[:,:,2] < 80)
for x in range(590, 860):
    c = red[388:502, x].sum()
    if c > 80: print("matrix box red col", x, c)
for y in range(380, 512):
    c = red[y, 600:860].sum()
    if c > 150: print("matrix box red row", y, c)
# matrix ink bbox inside box
mb = lum[389:502, 616:840]
ys, xs = np.where(mb < 150)
print("matrix ink bbox:", 616+xs.min(), 389+ys.min(), 616+xs.max(), 389+ys.max())
print("matrix ink modal dark:", modal((616, 389, 841, 503), "dark"))

# 4. filter params box: scan y 420..490 x 350..640 for borders (blueish or red)
sub = lum[420:495, 350:640]
# vertical borders
for x in range(350, 640):
    col = lum[420:495, x]
    nb = (col < 215).sum()
    if nb > 40: print("fp vline col", x, nb, tuple(a[455, x]))
for y in range(420, 495):
    row = lum[y, 350:640]
    nb = (row < 215).sum()
    if nb > 100: print("fp hline row", y, nb, tuple(a[y, 500]))
# fp text ink
inner = lum[424:488, 356:634]
ys, xs = np.where(inner < 150)
print("fp ink bbox:", 356+xs.min(), 424+ys.min(), 356+xs.max(), 424+ys.max())
print("fp ink modal dark:", modal((356, 424, 635, 489), "dark"))

# 5. bullet bands: column profile of ink in bands 302..323 and 341..357
for b in ((302, 323), (341, 357)):
    seg = lum[b[0]:b[1]+1, 95:500]
    colink = (seg < 190).sum(axis=0)
    runs = []
    x = 0
    while x < len(colink):
        if colink[x] > 0:
            x2 = x
            while x2 < len(colink)-1 and (colink[x2+1] > 0 or (x2+2 < len(colink) and colink[x2+2] > 0)):
                x2 += 1
            runs.append((95+x, 95+x2)); x = x2+1
        else: x += 1
    print(f"band {b} ink col runs (first 6):", runs[:6])

# 6. blue text lines: column profile first runs for x-left and word starts
for b in ((145, 164), (221, 242), (247, 268)):
    seg = lum[b[0]:b[1]+1, 95:900]
    colink = (seg < 190).sum(axis=0)
    xs = np.where(colink > 0)[0]
    print(f"band {b}: x {95+xs.min()}..{95+xs.max()}")
