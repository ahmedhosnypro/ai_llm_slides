from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_020.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[...,0], a[...,1], a[...,2]
red = (r > 120) & (r - g > 60) & (r - b > 60)
inner = red.copy()
inner[:, :55] = False; inner[:, 905:] = False
inner[:60, :] = False; inner[520:, :] = False

# column profile to find letter gaps (word boundaries)
cc = inner.sum(axis=0)
cols = [x for x in range(55,905) if cc[x] > 0]
# find runs
runs, start = [], cols[0]
for i in range(1, len(cols)):
    if cols[i] - cols[i-1] > 4:
        runs.append((start, cols[i-1])); start = cols[i]
runs.append((start, cols[-1]))
print("letter/word runs (x-ranges):", runs[:8], "... total", len(runs))

# 'S' of Self = first run; cap height from its rows
sx0, sx1 = runs[0]
sub = inner[:, sx0:sx1+1]
rows = np.nonzero(sub.sum(axis=1))[0]
print("'S' x", sx0, sx1, "rows", rows.min(), rows.max(), "capH", rows.max()-rows.min()+1)

# 'M' of Mechanism: find the widest run near the right (M is widest glyph 833)
widths = [(x1-x0+1, x0, x1) for x0,x1 in runs]
widths.sort(reverse=True)
print("widest runs:", widths[:4])
for w, x0, x1 in widths[:2]:
    sub = inner[:, x0:x1+1]
    rows = np.nonzero(sub.sum(axis=1))[0]
    print("run x", x0, x1, "w", w, "rows", rows.min(), rows.max(), "h", rows.max()-rows.min()+1)

# 'l' ascender in Self: runs 2nd/3rd ('e','l','f')
for idx in (1,2,3):
    x0,x1 = runs[idx]
    sub = inner[:, x0:x1+1]
    rows = np.nonzero(sub.sum(axis=1))[0]
    print(f"run{idx} x {x0}-{x1} w {x1-x0+1} rows {rows.min()}-{rows.max()} h {rows.max()-rows.min()+1}")

# core color of title ink (mode of strongly-red pixels)
from collections import Counter
ys, xs = np.nonzero(inner)
pix = [tuple(a[y,x]) for y,x in zip(ys[::7], xs[::7])]
print("title ink common colors:", Counter(pix).most_common(5))

# title exact horizontal center
print("title ink center x:", (xs.min()+xs.max())/2, "->", (xs.min()+xs.max())/2/72, "in")
