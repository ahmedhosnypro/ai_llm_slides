from PIL import Image
import numpy as np
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_023.jpg').convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]

# ink = differs from gray panel bg E9E9E7 and from white canvas; restrict to panel interior
ink = (abs(r-233) + abs(g-233) + abs(b-231)) > 60
# exclude red chrome border strokes region
ink[:47,:] = False; ink[518:,:] = False
ink[:, :61] = False; ink[:, 900:] = False

rowink = ink.sum(axis=1)
# find bands
bands = []
y = 0
while y < 518:
    if rowink[y] > 3:
        y0 = y
        while y < 518 and rowink[y] > 3: y += 1
        # merge close bands
        bands.append([y0, y-1])
    else:
        y += 1
# merge bands separated by <=2 rows
merged = []
for bn in bands:
    if merged and bn[0] - merged[-1][1] <= 2:
        merged[-1][1] = bn[1]
    else:
        merged.append(bn)
for (y0, y1) in merged:
    sub = ink[y0:y1+1, :]
    xs = np.where(sub.any(axis=0))[0]
    print(f"band y {y0}..{y1}  x {xs.min()}..{xs.max()}  inkpx {int(sub.sum())}")
