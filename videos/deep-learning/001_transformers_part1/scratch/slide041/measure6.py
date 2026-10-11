import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg").convert("RGB")).astype(int)

def runs(axis_vals, label, tol=14, minrun=2, off=0):
    print(f"--- {label} ---")
    vals = [tuple(int(v) for v in px) for px in axis_vals]
    start = 0; cur = list(vals[0]); out = []
    for i in range(1, len(vals)):
        if abs(vals[i][0]-cur[0])>tol or abs(vals[i][1]-cur[1])>tol or abs(vals[i][2]-cur[2])>tol:
            out.append((start, i-1, tuple(cur))); start = i; cur = list(vals[i])
        else:
            for j in range(3): cur[j] = int(cur[j]*0.85 + vals[i][j]*0.15)
    out.append((start, len(vals)-1, tuple(cur)))
    for s,e,c in out:
        if e-s >= minrun:
            print(f"  {s+off:4d}..{e+off:4d} ({e-s+1:3d}px) rgb{c}")

# center zoom: rows through suspected internals (abs x)
for y in (255, 270, 285, 310, 330, 345, 415, 425, 450, 475, 490, 500, 510, 520):
    runs(im[y, 280:530, :], f"row y={y} (abs, x+280)")
# cols through center zoom (abs y)
for x in (330, 360, 500, 515):
    runs(im[:, x, :], f"col x={x}")
# red mask details in center zoom
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
red = (r>150)&(g<90)&(b<90)
red[:, :270] = False; red[:, 545:] = False; red[:100, :] = False
ys, xs = np.where(red)
print("center-zoom red ink: x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max())
# purple mask in center zoom (V/K circles 7B4FA0)
pur = (abs(r-123)<40)&(abs(g-79)<40)&(abs(b-160)<40)
pur[:, :270] = False; pur[:, 545:] = False; pur[:240, :] = False
ys, xs = np.where(pur)
if len(xs): print("center-zoom purple ink: x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max(), " n=", len(xs))
else: print("center-zoom purple ink: NONE")
