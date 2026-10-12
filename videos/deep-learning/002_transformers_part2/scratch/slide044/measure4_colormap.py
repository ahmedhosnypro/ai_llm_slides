#!/usr/bin/env python3
"""Slide 044 — ASCII color map to decode cube/box structure + true-red scans + point colors."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def classify(rr, gg, bb):
    lum = 0.299*rr + 0.587*gg + 0.114*bb
    if lum < 55: return '#'          # black fill
    if lum < 120: return 'k'         # dark ink
    if rr > 150 and gg < 80 and bb < 80: return 'R'   # true red CC0000
    if rr > 150 and gg < 150 and bb > 140: return 'M' # magenta CC44CC
    if rr > 200 and gg > 80 and gg < 190 and bb < 110 and rr-gg > 60: return 'S'  # salmon F07060
    if rr > 200 and gg >= 190 and bb < 120: return 'Y' # yellow
    if gg > 130 and gg-rr > 40 and gg-bb > 40: return 'G' # green
    if rr > 180 and gg > 100 and gg < 190 and bb < 90: return 'O' # orange E08030
    if bb > 110 and bb-rr > 20 and bb-gg > 20 and rr < 130: return 'N'  # navy/blue
    if abs(rr-gg) < 30 and abs(gg-bb) < 30 and lum > 120: return '.'   # light gray/white
    return '?'

def amap(x0, y0, x1, y1, step, label):
    print(f'--- {label} ({x0},{y0})..({x1},{y1}) step {step} (col x10 = {x0+10*step}) ---')
    hdr = '     ' + ''.join(str(((x0+i*step)//10) % 10) for i in range(0, (x1-x0)//step + 1))
    print(hdr)
    for y in range(y0, y1, step):
        row = ''.join(classify(*a[y, x]) for x in range(x0, x1, step))
        print(f'{y:4d} {row}')

amap(30, 60, 330, 480, 6, 'LEFT CUBE + arrows + channels')
amap(250, 60, 500, 360, 6, 'GN CUBE')
amap(430, 80, 680, 380, 6, 'INSTANCE CUBE')
amap(620, 60, 960, 520, 6, 'RIGHT TENSOR + rect + arrows + oval')
amap(250, 355, 930, 515, 6, 'BOTTOM BOXES + oval')

print('== TRUE red mask (r>150,g<80,b<80) scans ==')
tr = (r > 150) & (g < 80) & (b < 80)
def runs_of(profile, thr, minlen=2):
    out, inrun = [], False
    for i, v in enumerate(profile):
        if v > thr and not inrun: s0 = i; inrun = True
        elif v <= thr and inrun:
            if i - s0 >= minlen: out.append((s0, i - 1))
            inrun = False
    if inrun: out.append((s0, len(profile) - 1))
    return out
print('true-red row runs x60..930:', runs_of(tr[:, 60:930].sum(axis=1), 8, 1))
print('true-red col runs y95..365 (x630..930):', runs_of(tr[95:365, 630:930].sum(axis=0), 30, 1))
print('true-red col runs y360..460 (x30..330):', runs_of(tr[360:460, 30:330].sum(axis=0), 3, 1))
print('true-red row runs y360..460 (x30..330):', runs_of(tr[360:460, 30:330].sum(axis=1), 3, 1))

print('== point colors ==')
pts = {
 'title_ink(300,65)': (300, 65), 'header(100,120)': (100, 120),
 'leftfront(100,300)': (100, 300), 'lefttop_band(150,170)': (150, 170),
 'gnfront(300,250)': (300, 250), 'gnright(370,250)': (370, 250),
 'instfront(500,280)': (500, 280), 'instcol(565,280)': (565, 280),
 'rtfront(750,250)': (750, 250), 'oval(800,470)': (800, 470), 'oval2(790,480)': (790, 480),
 'layerbox_bg(300,490)': (300, 490), 'instbox_bg(600,430)': (600, 430),
 'groupbox_bg(350,435)': (350, 435), 'panel_top(500,50)': (500, 50),
 'rect_border(880,200)': (880, 200), 'inside_rect(670,200)': (670, 200),
}
for k, (x, y) in pts.items():
    print(f'{k}: {tuple(a[y, x])}')
