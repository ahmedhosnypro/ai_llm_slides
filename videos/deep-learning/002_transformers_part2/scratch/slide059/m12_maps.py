# m12_maps.py — encoder container map, row token maps, pixel probes
from PIL import Image
import numpy as np

im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)

def cls(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r>238 and g>238 and b>238: return '.'
    if abs(r-231)<8 and abs(g-233)<8 and abs(b-230)<8: return ' '
    if r>150 and g<80 and b<80 and r-g>90: return 'R'
    if 170<r<225 and 80<g<135 and 90<b<140 and r-g>70: return 'r'
    if r>235 and 185<g<235 and 140<b<200 and r-b>50: return 't'
    if b>r+30 and b>110: return 'B'
    if g>r+25 and g>b+25 and g>110: return 'G'
    if r>235 and g>235 and b<200: return 'Y'
    if r>230 and r-g>30 and r-b>30: return 'P'
    if abs(r-g)<25 and abs(g-b)<25 and 120<r<238: return 'w'
    return '?'

def amap(x0, x1, y0, y1, step=2, label=""):
    print(f"== {label} (x {x0}..{x1}, y {y0}..{y1}, step {step}) ==")
    for y in range(y0, y1, step):
        print(f"{y:4d} " + "".join(cls(im[y, x]) for x in range(x0, x1, step)))

def probe(pts, label):
    print(f"== {label} ==")
    for (x, y) in pts:
        print(f"  ({x},{y}): {tuple(int(v) for v in im[y,x])}")

# encoder container full (step 3)
amap(141, 879, 275, 374, 3, "ENCODER CONTAINER")
