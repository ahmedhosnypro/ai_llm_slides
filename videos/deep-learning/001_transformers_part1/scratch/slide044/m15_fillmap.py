from PIL import Image
import numpy as np
im = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("RGB"), dtype=np.int16)
R,G,B = im[...,0], im[...,1], im[...,2]
L = np.asarray(Image.open("unique_slides/slide_044.jpg").convert("L"))
def classify(px, py):
    r,g,b = im[py,px]
    if r>235 and g>235 and b>235: return "."      # white
    if g>r+40 and g>b+40: return "G"               # green
    if r>170 and b>180 and b-g>15 and r-g>5: return "P"  # lavender/purple
    if r>200 and g>200 and b<215 and g-b>15: return "y"  # pale yellow
    if r<110 and g<110 and b<110: return "#"       # dark ink
    if abs(r-g)<20 and abs(g-b)<20: return "g"     # gray
    return "?"
# map every 4th px in interior x742..903 y84..293
print("    " + "".join(str((742+i)//100%10) for i in range(0,162,4)))
for py in range(84, 294, 4):
    row = "".join(classify(742+i, py) for i in range(0,162,4))
    print(f"{py:3d} {row}")
