#!/usr/bin/env python3
"""Frame containment check, attempt 3 (playlist-adapted: white canvas + E9E9E7 chrome
panel + white content boxes). Verifies: (1) no content ink in bands just outside the
white algorithm panel; (2) no ink outside the intro box; (3) right half of the lower
slide empty (spec: nothing beyond 58% width below y=38%); (4) nothing outside the
chrome gray panel."""
import numpy as np
from PIL import Image

REN = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide040/render_4.png'
im = np.asarray(Image.open(REN).convert('RGB')).astype(int)
H, W, _ = im.shape
r, g, b = im[:,:,0], im[:,:,1], im[:,:,2]
white = (r>242)&(g>242)&(b>242)
gray  = (np.abs(r-0xE9)<12)&(np.abs(g-0xE9)<12)&(np.abs(b-0xE7)<12)
redline = (r>130)&(r-g>60)&(r-b>60)   # chrome/intro borders
ink = ~(white|gray|redline)

ok = True
def band(name, y0,y1,x0,x1, allow=0):
    global ok
    n = int(ink[y0:y1, x0:x1].sum())
    flag = 'PASS' if n<=allow else 'FAIL'
    if n>allow: ok=False
    print(f'{name:44s} ink_px={n}  [{flag}]')

# white algo panel (content box): x 272..1157, y 443..1084 (render px)
band('outside panel RIGHT (x1165..1185, y450..1080)', 450,1080, 1165,1185)
band('outside panel LEFT  (x248..266, y450..1080)', 450,1080, 248,266)
band('outside panel TOP   (y425..437, x280..1150)', 425,437, 280,1150)
band('outside panel BOTTOM(y1090..1110, x280..1150)', 1090,1110, 280,1150)
# intro box: x 148..1894, y 224..404
band('outside intro RIGHT (x1902..1920, y230..400)', 230,400, 1902,1920)
band('outside intro TOP   (y206..218, x160..1880)', 206,218, 160,1880)
band('outside intro BOTTOM(y410..418, x160..1880)', 410,418, 160,1880)
# right half of lower slide empty: y > 38% (427px), x > 58% (1611px)
band('right-lower empty zone (x1618..1900, y434..1078)', 434,1078, 1618,1900)
# outside chrome gray panel (x 89..1913, y 95..bottom)
band('outside chrome panel LEFT (x60..84, y100..1100)', 100,1100, 60,84)
band('outside chrome panel RIGHT(x1920..1990, y100..1100)', 100,1100, 1920,1990)
print('CONTAINMENT:', 'PASS' if ok else 'FAIL')
