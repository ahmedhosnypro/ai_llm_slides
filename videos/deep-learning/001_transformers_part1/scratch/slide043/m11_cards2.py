#!/usr/bin/env python3
"""Card staircase: top edge y and x-extent of each card's top sliver; right edge."""
import numpy as np
from PIL import Image
im = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_043.jpg').convert('RGB')).astype(int)
r,g,b = im[:,:,0], im[:,:,1], im[:,:,2]

def runs_at(y, mask):
    xs = np.where(mask[y])[0]
    if len(xs)==0: return []
    runs=[]; s=xs[0]; p=xs[0]
    for x in xs[1:]:
        if x==p+1: p=x
        else:
            if p-s>=2: runs.append((int(s),int(p)))
            s=p=x
    if p-s>=2: runs.append((int(s),int(p)))
    return runs

masks = {
 'peach':  (abs(r-255)<14)&(abs(g-228)<14)&(abs(b-196)<16),
 'pgreen': (abs(r-204)<14)&(abs(g-255)<14)&(abs(b-204)<14),
 'pyellow':(abs(r-252)<14)&(abs(g-252)<14)&(abs(b-176)<20),
 'lavender':(abs(r-200)<14)&(abs(g-200)<14)&(abs(b-240)<12),
 'salmon': (abs(r-241)<10)&(abs(g-139)<14)&(abs(b-150)<14),
}
for name in ['peach','pgreen','pyellow','lavender','salmon']:
    m = masks[name]
    print(f"== {name}")
    for y in range(185, 285, 2):
        rn = runs_at(y, m)
        if rn: print(f"  y={y}: {rn}")
