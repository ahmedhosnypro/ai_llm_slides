from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
L = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"), dtype=np.int16)
# 1) border color median
bp = [tuple(im[y,x]) for x,y in [(739,150),(740,150),(739,250),(800,81),(801,81),(850,296),(851,296)]]
print("border px:", bp)
# 2) 1px scan of concat->stack arrows zone y149..160, x770..850
print("--- y149..160 dark runs x770..850 (L<130) ---")
for y in range(149,161):
    row = L[y,770:850]<130
    runs=[];s=None
    for i,v in enumerate(row):
        if v and s is None: s=i
        if not v and s is not None: runs.append((770+s,770+i-1)); s=None
    if s is not None: runs.append((770+s,849))
    if runs: print(y, runs)
# 3) stack borders: 1px dark runs (len>20) x740..895, y150..205
print("--- stack zone long dark runs ---")
for y in range(150,206):
    row = L[y,740:895]<110
    runs=[];s=None
    for i,v in enumerate(row):
        if v and s is None: s=i
        if not v and s is not None:
            if i-s>20: runs.append((740+s,740+i-1))
            s=None
    if s is not None and len(row)-s>20: runs.append((740+s,894))
    if runs: print(y, runs)
# 4) bottom boxes: fill samples grid in box A x758..788 y206..236
print("--- boxA fill grid ---")
for y in range(206,238,6):
    print(y, [tuple(int(v) for v in im[y,x]) for x in range(760,790,6)])
# 5) bottom boxes: vertical borders scan y204..242, dark runs per row x750..895 (len>15)
print("--- bottom box borders ---")
for y in range(200,244):
    row = L[y,750:895]<140
    runs=[];s=None
    for i,v in enumerate(row):
        if v and s is None: s=i
        if not v and s is not None:
            if i-s>=8: runs.append((750+s,750+i-1))
            s=None
    if runs: print(y, runs)
