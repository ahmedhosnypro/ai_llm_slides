#!/usr/bin/env python3
"""Residual maps: classify each pixel in a window into named buckets, print ASCII."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *

def bucket(r, g, b):
    if mint(r, g, b): return 'M'
    if bluegray(r, g, b) or (165 <= r <= 200 and 195 <= b <= 225): return 'B'
    if (160 <= r <= 185 and 195 <= g <= 215 and 205 <= b <= 225): return 'C'  # ADCFD8 cyan-gray
    if 235 <= r <= 255 and 210 <= g <= 245 and 125 <= b <= 190: return 'Y'
    if peach(r, g, b): return '.'
    if red_ink(r, g, b) or dark_red(r, g, b): return 'R'
    if black_ink(r, g, b): return 'K'
    if navy(r, g, b) or blue_mid(r, g, b): return 'N'
    if green_txt(r, g, b) or dkgreen_border(r, g, b): return 'G'
    if white(r, g, b): return 'W'
    if dpgray(r, g, b): return 'D'
    if softpink(r, g, b): return 'P'
    if sigma_cyan(r, g, b): return 'S'
    if yellowbox(r, g, b): return 'y'
    if salmon(r, g, b): return 's'
    if lavender_cell(r, g, b): return 'L'
    if 190 <= r <= 215 and 60 <= g <= 110 and 60 <= b <= 110: return 'p'  # pinkish
    return ' '

def amap(name, x0, x1, y0, y1, step=2):
    print('== %s (x %d..%d, y %d..%d, step %d) ==' % (name, x0, x1 - 1, y0, y1 - 1, step))
    hdr = '     ' + ''.join(str((x // 10) % 10) for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1, step):
        row = ''.join(bucket(*px[x, y]) for x in range(x0, x1, step))
        print('%4d %s' % (y, row))
    print()

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'left'
    if which == 'left':
        amap('input-ellipse + mint', 60, 285, 160, 435, 3)
    elif which == 'dp':
        amap('dot product area', 255, 400, 140, 420, 3)
    elif which == 'mid':
        amap('softmax/sigma/circles', 400, 700, 140, 420, 3)
    elif which == 'right':
        amap('Wv + right container', 620, 900, 140, 430, 3)
    elif which == 'top':
        amap('output box + pills', 250, 700, 110, 215, 2)
    elif which == 'bottom':
        amap('sentence + legend + note', 60, 900, 420, 516, 4)
    elif which == 'title':
        amap('title', 150, 900, 44, 106, 4)
