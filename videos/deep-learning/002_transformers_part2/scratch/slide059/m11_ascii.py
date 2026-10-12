# m11_ascii.py — ASCII color-class maps to disambiguate structure
from PIL import Image
import numpy as np

im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)

def cls(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r>238 and g>238 and b>238: return '.'          # white
    if abs(r-231)<8 and abs(g-233)<8 and abs(b-230)<8: return ' '  # panel gray
    if r>150 and g<80 and b<80 and r-g>90: return 'R'  # dark red (bars/plus)
    if 170<r<225 and 80<g<135 and 90<b<140 and r-g>70: return 'r'  # rose
    if r>235 and 185<g<235 and 140<b<200 and r-b>50: return 't'    # tan
    if b>r+30 and b>110: return 'B'                    # blue/navy
    if g>r+25 and g>b+25 and g>110: return 'G'         # green
    if r>235 and g>235 and b<200: return 'Y'           # yellow
    if r>230 and r-g>30 and r-b>30: return 'P'         # pink/salmon
    if abs(r-g)<25 and abs(g-b)<25 and 120<r<238: return 'w'       # light gray
    return '?'

def amap(x0, x1, y0, y1, step=2, label=""):
    print(f"== {label} (x {x0}..{x1}, y {y0}..{y1}, step {step}) ==")
    hdr = "     " + "".join(str((x//10)%10) if x%10<step else ' ' for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1, step):
        row = "".join(cls(im[y, x]) for x in range(x0, x1, step))
        print(f"{y:4d} {row}")

# 1. circle 1 + label + arrow zone
amap(418, 465, 50, 132, 1, "CIRCLE 1 + C1 label + arrow")
# 2. top band: Output Classes + C labels
amap(315, 615, 50, 95, 2, "TOP BAND labels")
