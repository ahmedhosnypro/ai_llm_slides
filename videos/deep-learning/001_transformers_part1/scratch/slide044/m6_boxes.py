from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"))
def runs_in_row(y, x0=742, x1=904, thresh=150):
    row = im[y, x0:x1] < thresh
    out = []
    s = None
    for i, v in enumerate(row):
        if v and s is None: s = i
        if not v and s is not None:
            out.append((x0+s, x0+i-1)); s = None
    if s is not None: out.append((x0+s, x0+x1-1-x0))
    return out
# Find horizontal box borders: rows where a run spans >60px
print("--- long horizontal runs (>60px) ---")
for y in range(84, 294):
    rr = [r for r in runs_in_row(y) if r[1]-r[0] > 60]
    if rr: print(y, rr)
