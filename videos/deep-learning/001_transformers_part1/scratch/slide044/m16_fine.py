from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
L = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"))
def cls(px,py):
    r,g,b = im[py,px]
    if r>235 and g>235 and b>235: return "."
    if g>r+40 and g>b+40: return "G"
    if r>170 and b>180 and b-g>15 and r-g>5: return "P"
    if r>200 and g>200 and b<215 and g-b>15: return "y"
    if L[py,px]<110: return "#"
    if abs(r-g)<20 and abs(g-b)<20: return "g"
    return "?"
for py in range(84, 294, 2):
    print(f"{py:3d} " + "".join(cls(742+i,py) for i in range(0,162,2)))
