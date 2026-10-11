#!/usr/bin/env python3
"""Per-row fill classification inside encoder/decoder stacks to find exact box extents."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_017.jpg').convert('RGB')
A = np.asarray(im).astype(int)

def cls(px):
    r, g, b = px
    if 238 < r and 222 <= g <= 248 and 200 <= b <= 232: return 'peach'
    if 190 <= r <= 235 and g > 240 and 200 <= b <= 235: return 'palegreen'
    if 110 <= r <= 225 and 70 <= g <= 200 and 20 <= b <= 165 and r > g > b and r-b > 40: return 'tan'
    if 130 <= r <= 225 and 90 <= g <= 200 and 160 <= b <= 240 and b > r >= g: return 'purple'
    if r > 140 and 40 <= g <= 140 and 30 <= b <= 140 and r-g > 55 and r-b > 55: return 'darkred'
    if 150 <= r <= 235 and 195 <= g <= 250 and 130 <= b <= 225 and g > r and g > b: return 'ltgreen'
    if b > 130 and b-r > 55 and b-g > 35: return 'blue'
    if r > 150 and g < 150 and b < 150 and r-g > 60: return 'red'
    if 195 <= r <= 250 and 195 <= g <= 250 and 0 <= b <= 185 and r+g-b > 260: return 'yellow'
    if r < 135 and g < 135 and b < 135: return 'ink'
    if r > 240 and g > 240 and b > 240: return 'white'
    return 'other'

def rowprofile(x0, x1, y0, y1, name):
    print(f"== {name} rows y{y0}..{y1} (x {x0}..{x1}) — count of each fill class per row")
    prev = None
    for y in range(y0, y1+1):
        c = {'tan':0,'purple':0,'darkred':0,'ltgreen':0,'peach':0,'palegreen':0,'blue':0,'red':0,'yellow':0,'ink':0,'other':0,'white':0}
        for x in range(x0, x1+1):
            c[cls(A[y, x])] += 1
        key = (c['tan']>25, c['purple']>25, c['darkred']>25, c['ltgreen']>25, c['yellow']>25, c['blue']>3, c['red']>3)
        sig = ''.join(ch for ch,v in zip('TPDLYBR', key) if v)
        summary = f"tan={c['tan']:3d} pur={c['purple']:3d} drd={c['darkred']:3d} ltg={c['ltgreen']:3d} yel={c['yellow']:3d} blu={c['blue']:2d} red={c['red']:2d} ink={c['ink']:3d} oth={c['other']:3d}"
        if key != prev:
            print(f"  y{y:3d} [{sig:8s}] {summary}")
        prev = key

rowprofile(629, 726, 255, 530, "ENCODER stack (x629-726)")
rowprofile(745, 835, 255, 530, "DECODER stack (x745-835)")
