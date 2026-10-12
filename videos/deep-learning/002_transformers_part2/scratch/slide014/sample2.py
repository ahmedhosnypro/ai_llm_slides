from PIL import Image
import numpy as np
im = Image.open('videos/deep-learning/002_transformers_part2/unique_slides/slide_014.jpg').convert('RGB')
A = np.asarray(im).astype(int)
r = A[:,:,0]; g = A[:,:,1]; b = A[:,:,2]
def seg(y=None, x=None, a=None, bnd=None, mask=None, label=""):
    """print runs of a mask along a row (y) or column (x)"""
    if y is not None:
        m = mask[y, a:bnd]; coords = np.arange(a, bnd)
    else:
        m = mask[a:bnd, x]; coords = np.arange(a, bnd)
    idx = np.nonzero(m)[0]
    if len(idx)==0: print(f"{label}: empty"); return
    runs=[]; s=idx[0]; p=idx[0]
    for v in idx[1:]:
        if v-p>2: runs.append((coords[s], coords[p])); s=v
        p=v
    runs.append((coords[s], coords[p]))
    print(f"{label}: {runs}")

BLUE = (b-r>60)&(b-g>50)&(b>110)
PEACH = (abs(r-245)<25)&(abs(g-203)<30)&(abs(b-167)<35)&(r-g>20)&(g-b>15)
MAROON = (r>80)&(r<190)&(g<75)&(b<75)&(r-g>40)
PINK = (r>235)&(abs(g-182)<25)&(abs(b-193)<25)&(r-g>45)
LGREEN = (g>210)&(abs(r-144)<45)&(abs(b-144)<50)
CYANP = (abs(r-173)<40)&(abs(g-216)<35)&(abs(b-230)<35)
RED = (r>150)&(r-g>80)&(r-b>80)
DARK = (r<95)&(g<95)&(b<95)

print("== schematic blue border columns (fy 260..500) ==")
for x in range(880, 915):
    cnt = BLUE[260:500, x].sum()
    if cnt > 50: print(f"  blue col x={x} count={cnt}")
print("== schematic blue border rows (fx 310..880) ==")
for y in list(range(243, 258))+list(range(500, 518)):
    cnt = BLUE[y, 310:880].sum()
    if cnt > 100: print(f"  blue row y={y} count={cnt}")
print("== design box maroon border ==")
seg(y=180, a=300, bnd=310, mask=MAROON, label="left border cols @y180 (scan 295..320)")
for x in range(295, 325):
    cnt = MAROON[140:235, x].sum()
    if cnt > 30: print(f"  maroon col x={x} count={cnt}")
for x in range(880, 912):
    cnt = MAROON[140:235, x].sum()
    if cnt > 30: print(f"  maroon col x={x} count={cnt}")
for y in range(130, 148):
    cnt = MAROON[y, 315:890].sum()
    if cnt > 100: print(f"  maroon row y={y} count={cnt}")
for y in range(230, 250):
    cnt = MAROON[y, 315:890].sum()
    if cnt > 100: print(f"  maroon row y={y} count={cnt}")
print("== Y rows: peach row-runs in fx 305..460 ==")
seg(x=None, y=None, a=305, bnd=460, mask=PEACH[240:515, 305:460], label="rows")
rows = np.nonzero(PEACH[240:515, 305:460].sum(axis=1) > 60)[0] + 240
runs=[]; s=rows[0]; p=rows[0]
for v in rows[1:]:
    if v-p>3: runs.append((s,p)); s=v
    p=v
runs.append((s,p))
print("  peach row runs:", runs)
print("== Y row cols (band fy 455..500) ==")
cols = np.nonzero(PEACH[455:500, 295:470].sum(axis=0) > 10)[0] + 295
print("  peach cols:", cols.min(), "..", cols.max())
print("== zero boxes: pale green col runs @ fy band ==")
seg(y=310, a=840, bnd=895, mask=LGREEN, label="LGREEN row y=310 fx840..895")
for y in [300, 320, 340, 355, 375, 390, 410, 430, 450, 460]:
    seg(y=y, a=838, bnd=895, mask=LGREEN, label=f"LGREEN y={y}")
print("== matrix panel bounds ==")
MP = (g-r>14)&(g-b>14)&(g>210)&(b>r)
ys = np.nonzero(MP[240:515, 620:840].sum(axis=1) > 100)[0] + 240
print("  panel rows:", ys.min(), "..", ys.max())
xs = np.nonzero(MP[300:460, 600:900].sum(axis=0) > 50)[0] + 600
runs=[]; s=xs[0]; p=xs[0]
for v in xs[1:]:
    if v-p>4: runs.append((s,p)); s=v
    p=v
runs.append((s,p))
print("  panel col runs:", runs)
