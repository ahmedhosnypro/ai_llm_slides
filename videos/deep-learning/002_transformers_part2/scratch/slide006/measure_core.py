#!/usr/bin/env python3
"""Blue core color + localize lower-half non-bg pixels."""
from PIL import Image
import numpy as np
from collections import Counter

p = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(p).convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

# most-saturated blue pixels per agenda band
bands = [(147,161),(187,201),(229,247),(269,283),(309,323),(353,367)]
for k,(y0,y1) in enumerate(bands,1):
    sub = a[y0:y1+1, 100:500]
    sat = sub[:,:,2] - (sub[:,:,0]+sub[:,:,1])//2
    idx = np.argsort(sat.ravel())[-12:]
    px = sub.reshape(-1,3)[idx]
    print(f"L{k} most-blue px:", [tuple(q) for q in px])

# where are the non-bg lower-half pixels?
sub = a[380:515, 45:915]
nonbg = (np.abs(sub[:,:,0]-233)>40) | (np.abs(sub[:,:,1]-233)>40) | (np.abs(sub[:,:,2]-231)>40)
nys, nxs = np.where(nonbg)
rows = Counter(nys + 380)
print("\nnon-bg rows histogram (top 12):", rows.most_common(12))
cols = Counter((nxs + 45) // 50 * 50)
print("non-bg col buckets:", sorted(cols.items())[:20])
