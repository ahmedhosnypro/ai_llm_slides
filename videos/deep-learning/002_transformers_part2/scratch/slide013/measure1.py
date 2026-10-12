#!/usr/bin/env python3
"""Batch 1: peach panel edges, title lines, input ellipse, mint ellipse interior."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *

# ---- 1. peach panel: edges via row/col scans
print('== PEACH PANEL ==')
r = rowproj(300, 301, 40, 516, peach)
print('col x=300 peach rows:', runs(r), '(offset y+40)')
c = colproj(59, 901, 300, 301, peach)
print('row y=300 peach cols:', runs(c), '(offset x+59)')
# top edge: scan x=800 (right side, away from title?) for peach start
for xx in (150, 400, 800):
    r2 = rowproj(xx, xx + 1, 90, 130, peach)
    print('col x=%d peach rows 90..130:' % xx, runs(r2), '(offset y+90)')
for yy in (140, 480):
    c2 = colproj(59, 150, yy, yy + 1, peach)
    print('row y=%d peach cols 59..150:' % yy, runs(c2), '(offset x+59)')

# ---- 2. title lines: ink in y 44..106 (above peach panel top ~107)
print('\n== TITLE ==')
def anyink(r, g, b):
    return black_ink(r, g, b) or navy(r, g, b) or blue_mid(r, g, b) or red_ink(r, g, b) or dark_red(r, g, b)
bb = bbox(60, 900, 44, 106, anyink)
show('title all-ink', bb)
if bb:
    rp = rowproj(bb[0], bb[1] + 1, 44, 106, anyink)
    print('title row runs:', [(a + 44, b + 44) for a, b in runs(rp)])
    # line 1 horizontal extent
    l1 = bbox(60, 900, 44, 76, anyink)
    l2 = bbox(60, 900, 76, 106, anyink)
    show('title L1', l1)
    show('title L2', l2)
    # color split on L1: black runs vs blue runs vs red runs
    for nm, fn in (('black', black_ink), ('blue', lambda r, g, b: navy(r, g, b) or blue_mid(r, g, b)), ('red', lambda r, g, b: red_ink(r, g, b) or dark_red(r, g, b))):
        b1 = bbox(60, 900, 44, 76, fn)
        b2 = bbox(60, 900, 76, 106, fn)
        show('L1 ' + nm, b1)
        show('L2 ' + nm, b2)

# ---- 3. input embedding ellipse (blue-gray) left side
print('\n== INPUT ELLIPSE (blue-gray) ==')
bb = bbox(59, 215, 90, 440, bluegray)
show('input ellipse bluegray', bb)
if bb:
    rp = rowproj(bb[0], bb[1] + 1, bb[2], bb[3] + 1, bluegray)
    print('rows:', [(a + bb[2], b + bb[2]) for a, b in runs(rp, 2)])
    cp = colproj(bb[0], bb[1] + 1, bb[2], bb[3] + 1, bluegray)
    print('cols:', [(a + bb[0], b + bb[0]) for a, b in runs(cp, 2)])

# cells inside the input ellipse (yellow/salmon/lavender) + red X labels
print('\n== INPUT ELLIPSE CELLS ==')
for nm, fn in (('yellow', lambda r, g, b: 235 <= r <= 255 and 215 <= g <= 245 and 130 <= b <= 185),
               ('salmon', salmon), ('lavender', lavender_cell),
               ('redlabel', lambda r, g, b: red_ink(r, g, b) or dark_red(r, g, b))):
    bb2 = bbox(59, 215, 90, 440, fn)
    show('input ' + nm, bb2)
    if bb2:
        rp = rowproj(bb2[0], bb2[1] + 1, bb2[2], bb2[3] + 1, fn)
        print('  rows:', [(a + bb2[2], b + bb2[2]) for a, b in runs(rp, 2)])

# ---- 4. mint ellipse precise + interior structure
print('\n== MINT ELLIPSE / W_k ==')
bb = bbox(200, 275, 150, 440, mint)
show('mint ellipse', bb)
if bb:
    rp = rowproj(bb[0], bb[1] + 1, bb[2], bb[3] + 1, mint)
    rr = [(a + bb[2], b + bb[2]) for a, b in runs(rp, 2)]
    print('mint rows:', rr)
    # white text inside (W_k labels)
    bw = bbox(bb[0], bb[1] + 1, bb[2], bb[3] + 1, white)
    show('white inside mint', bw)
    if bw:
        rp = rowproj(bw[0], bw[1] + 1, bw[2], bw[3] + 1, white)
        print('white rows:', [(a + bw[2], b + bw[2]) for a, b in runs(rp, 1)])
