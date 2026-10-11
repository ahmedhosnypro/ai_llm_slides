#!/usr/bin/env python3
"""Fine ASCII ink maps of critical regions (1px resolution)."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def glyph(x0, x1, y0, y1, name):
    print(f"== {name} x{x0}..{x1} y{y0}..{y1} (1px/char)")
    hdr1 = '     ' + ''.join(str((x0+i)//100 % 10) if (x0+i) % 10 == 0 else ' ' for i in range(x1-x0+1))
    hdr2 = '     ' + ''.join(str((x0+i)//10 % 10) if (x0+i) % 10 == 0 else ' ' for i in range(x1-x0+1))
    print(hdr1); print(hdr2)
    for y in range(y0, y1+1):
        line = []
        for x in range(x0, x1+1):
            r, g, b = A[y, x]
            if r < 130 and g < 130 and b < 130: c = '#'
            elif r > 150 and g < 140 and b < 140 and r-g > 55: c = 'R'
            elif b > 130 and b-r > 50: c = 'B'
            elif r > 200 and g > 200 and b < 190: c = 'Y'
            elif r > 150 and 60 <= g <= 160 and 40 <= b <= 130 and r-g > 30: c = 't'
            elif 130 <= r <= 230 and 80 <= g <= 150 and 150 <= b <= 230: c = 'P'
            elif 150 <= r <= 235 and 190 <= g <= 250 and 120 <= b <= 225 and g > r: c = 'L'
            elif r > 235 and g > 225 and b > 195: c = '.'
            else: c = '?'
            line.append(c)
        print(f"{y:3d}  {''.join(line)}")

glyph(640, 720, 486, 524, "ENCODER bottom: arrow + Inputs label")
glyph(745, 850, 486, 524, "DECODER bottom: arrow + Outputs label")
