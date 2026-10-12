#!/usr/bin/env python3
"""Definitive precise measurements, element by element (frame px)."""
import sys
sys.path.insert(0, '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide013')
from measure_lib import *

def bb(name, x0, x1, y0, y1, fn, minpix=6):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if fn(*px[x, y]):
                xs.append(x)
                ys.append(y)
    if len(xs) < minpix:
        print('%-34s EMPTY (%d px)' % (name, len(xs)))
        return None
    print('%-34s x %3d..%3d  y %3d..%3d  n=%d' % (name, min(xs), max(xs), min(ys), max(ys), len(xs)))
    return (min(xs), max(xs), min(ys), max(ys))

def rowruns(name, bbv, fn, minlen=2):
    if bbv is None: return
    x0, x1, y0, y1 = bbv[0], bbv[1] + 1, bbv[2], bbv[3] + 1
    rp = [any(fn(*px[x, y]) for x in range(x0, x1)) for y in range(y0, y1)]
    print('   %s rows: %s' % (name, [(a + y0, b + y0) for a, b in runs(rp, minlen)]))

def colruns(name, bbv, fn, minlen=2):
    if bbv is None: return
    x0, x1, y0, y1 = bbv[0], bbv[1] + 1, bbv[2], bbv[3] + 1
    cp = [any(fn(*px[x, y]) for y in range(y0, y1)) for x in range(x0, x1)]
    print('   %s cols: %s' % (name, [(a + x0, b + x0) for a, b in runs(cp, minlen)]))

print('====== PILLS ======')
p = bb('Similarity pill fill', 260, 380, 140, 190, pill_fill)
p = bb('Probabilities pill fill', 400, 545, 140, 190, pill_fill)
p = bb('WeightedSUM pill fill', 545, 720, 140, 190, pill_fill)
blue_txt = lambda r, g, b: navy(r, g, b) or blue_mid(r, g, b)
bb('Similarity text', 260, 380, 140, 190, blue_txt)
bb('Probabilities text', 400, 545, 140, 190, blue_txt)
bb('WeightedSUM text', 545, 720, 140, 190, blue_txt)

print('====== DOT PRODUCT BOX ======')
d = bb('DP gray box', 250, 420, 180, 400, dpgray, 50)
rowruns('DP', d, dpgray, 5)
# DP border (darker gray): sample edge colors
print('   DP edge colors row y=250: ', end='')
prev = None
for x in range(255, 290):
    c = '#%02X%02X%02X' % px[x, 250]
    if c != prev:
        print('%d:%s' % (x, c), end=' ')
        prev = c
print()
print('   DP edge colors col x=310: ', end='')
prev = None
for y in range(180, 200):
    c = '#%02X%02X%02X' % px[310, y]
    if c != prev:
        print('%d:%s' % (y, c), end=' ')
        prev = c
print()
print('   DP bottom col x=310 y 375..395: ', end='')
prev = None
for y in range(375, 395):
    c = '#%02X%02X%02X' % px[310, y]
    if c != prev:
        print('%d:%s' % (y, c), end=' ')
        prev = c
print()
# DP title text (dark) inside box top-left
bb('DP title dark text', 270, 360, 192, 215, lambda r, g, b: r <= 130 and g <= 110 and b <= 110)
# K.q red at top-right
bb('DP K.q red', 330, 380, 188, 215, lambda r, g, b: red_ink(r, g, b) or dark_red(r, g, b))
# blue dots (navy core)
bb('DP dots navy', 265, 380, 220, 380, navy)
# dot halos (light blue)
bb('DP dots halo lightblue', 265, 380, 220, 380, lambda r, g, b: 140 <= r <= 190 and 185 <= g <= 215 and 225 <= b <= 250)

print('====== SOFTMAX ======')
sm = bb('softmax pink block', 430, 500, 180, 400, softpink, 50)
rowruns('softmax', sm, softpink, 5)
# soft max rotated text (dark)
bb('softmax text dark', 435, 495, 240, 340, lambda r, g, b: r <= 120 and g <= 90 and b <= 160)

print('====== SIGMA ======')
sg = bb('sigma cyan box', 495, 680, 180, 225, sigma_cyan, 50)
rowruns('sigma', sg, sigma_cyan, 3)
bb('sigma glyph navy', 500, 670, 185, 220, navy)

print('====== MULTIPLY CIRCLES (x~520..600) ======')
# white circles with red border: find red ring pixels in x 500..620, y 225..390
bb('mult red rings', 500, 620, 225, 390, lambda r, g, b: red_ink(r, g, b) or dark_red(r, g, b))
