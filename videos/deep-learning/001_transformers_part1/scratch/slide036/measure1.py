from PIL import Image
import numpy as np
im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_036.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print('frame', W, 'x', H)

def close(px, target, tol):
    return (abs(px - np.array(target)).sum(axis=-1) <= tol)

def boxes(mask, name):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(name, 'NONE'); return
    print(f'{name}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  count {len(xs)}')

# green border 00B050
g = close(a, (0,176,80), 120)
boxes(g, 'green_all')
# split green into regions by row bands
ys, xs = np.where(g)
if len(ys):
    import collections
    # cluster rows
    rows = np.zeros(H, bool); rows[ys]=True
    bands=[]; start=None
    for i in range(H):
        if rows[i] and start is None: start=i
        elif not rows[i] and start is not None: bands.append((start,i-1)); start=None
    if start is not None: bands.append((start,H-1))
    for b in bands:
        sel = (ys>=b[0])&(ys<=b[1])
        if sel.sum()>30:
            print(f'  green band y{b[0]}..{b[1]}: x {xs[sel].min()}..{xs[sel].max()} n={sel.sum()}')
