from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
L = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"), dtype=np.int16)
print("--- 1px dark(L<150) runs y200..292 x744..896 ---")
for y in range(200,293):
    row = L[y,744:896]<150
    runs=[];s=None
    for i,v in enumerate(row):
        if v and s is None: s=i
        if not v and s is not None: runs.append((744+s,744+i-1)); s=None
    if s is not None: runs.append((744+s,895))
    if runs: print(y, runs)
print("--- fill samples ---")
for x,y in [(760,210),(770,232),(800,210),(812,232),(845,210),(860,232),(770,250),(810,250),(855,250),(770,284),(809,284),(858,284)]:
    print((x,y), tuple(int(v) for v in im[y,x]))
