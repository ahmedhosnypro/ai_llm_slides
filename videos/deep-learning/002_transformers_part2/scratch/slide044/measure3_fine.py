#!/usr/bin/env python3
"""Slide 044 — fine pass 3: per-cube grids, arrows, text boxes, oval, title/header metrics."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

def runs_of(profile, thr, minlen=2, lo=0):
    out, inrun = [], False
    for i, v in enumerate(profile):
        if v > thr and not inrun: s0 = i; inrun = True
        elif v <= thr and inrun:
            if i - s0 >= minlen: out.append((s0 + lo, i - 1 + lo))
            inrun = False
    if inrun: out.append((s0 + lo, len(profile) - 1 + lo))
    return out

def colruns(mask, y0, y1, thr=0, minlen=2):
    return runs_of(mask[y0:y1, :].sum(axis=0), thr, minlen)

def rowruns(mask, x0, x1, thr=0, minlen=2):
    return runs_of(mask[:, x0:x1].sum(axis=1), thr, minlen)

red_strict = (r > 150) & (r - g > 80) & (r - b > 80)
red_loose = (r > 150) & (r - g > 30) & (r - b > 30)
mag = (r > 150) & (b > 150) & (g < 120) & (r - g > 60) & (b - g > 60)
sal = (r > 200) & (r - g > 50) & (g - b > 10) & (g > 70)
orange = (r > 200) & (r - g > 90) & (g - b > 40) & (g < 180)
green = (g > 130) & (g - r > 40) & (g - b > 40)
yellowy = (r > 200) & (g > 190) & (b < 120)
navy = (b > 100) & (b - r > 20) & (b - g > 20) & (r < 120) & (g < 120)
dark = lum < 120
black = lum < 60

print('== mystery red rows: x-extents ==')
for yy in (374, 375, 455, 501):
    cols = np.where(red_loose[yy, :])[0]
    if len(cols): print(f'y{yy}: red x {cols.min()}..{cols.max()} n={len(cols)} runs={runs_of(red_loose[yy,:],0,3)[:12]}')

print('== GROUP/INSTANCE boxes: border hunt y360..450 ==')
print('dark row runs y360..460 (x250..870):', rowruns(dark, 250, 870, 100, 1))
print('red row runs y360..460 (x250..870):', rowruns(red_loose, 250, 870, 100, 1))
print('LAYER box: dark row runs y440..515 (x60..700):', rowruns(dark, 60, 700, 100, 1))
print('LAYER box: red row runs y440..515 (x60..700):', rowruns(red_loose, 60, 700, 100, 1))
print('LAYER box: dark col runs y460..500:', colruns(dark, 460, 500, 20, 2)[:6], '...', colruns(dark, 460, 500, 20, 2)[-6:])

print('== LEFT CUBE ==')
print('front salmon row runs (x70..200):', rowruns(sal, 70, 200, 5, 2))
print('front salmon col runs (y240..400):', colruns(sal, 240, 400, 5, 2))
print('top-face rows y120..225 (x60..320): green', rowruns(green, 60, 320, 5, 2), 'orange', rowruns(orange, 60, 320, 5, 2), 'yellow', rowruns(yellowy, 60, 320, 5, 2))
print('side-face cols y240..400 (x195..320): sal', colruns(sal, 240, 400, 5, 2), 'orange', colruns(orange, 240, 400, 5, 2), 'bluegray?')
bluegray = (abs(r - 112) < 45) & (abs(g - 144) < 45) & (abs(b - 175) < 50) & (b - r > 25)
print('  bluegray col runs y240..400 (x195..320):', colruns(bluegray, 240, 400, 3, 2))
print('red arrows left region: strict red row runs y120..460 (x30..320):', rowruns(red_strict, 30, 320, 10, 2))
print('  red col runs y150..250 (x30..320):', colruns(red_strict, 150, 250, 3, 2))
print('  red col runs y420..470 (x30..320):', colruns(red_strict, 420, 470, 3, 2))

print('== GN CUBE (center-left) ==')
print('magenta col runs y200..340 (x260..420):', colruns(mag, 200, 340, 3, 2))
print('magenta row runs (x276..334):', rowruns(mag, 276, 334, 5, 2))
print('salmon/orange col runs y200..340 (x330..420):', colruns(sal, 200, 340, 3, 2), colruns(orange, 200, 340, 3, 2))
print('top rows y70..180 (x250..480): navy', rowruns(navy, 250, 480, 5, 2), 'green', rowruns(green, 250, 480, 5, 2), 'yellow', rowruns(yellowy, 250, 480, 5, 2), 'orange', rowruns(orange, 250, 480, 5, 2))
print('side cols y200..340 (x400..480): yellow', colruns(yellowy, 200, 340, 3, 2), 'orange', colruns(orange, 200, 340, 3, 2), 'bluegray', colruns(bluegray, 200, 340, 3, 2))

print('== INSTANCE CUBE (center-right) ==')
print('magenta col runs y210..360 (x440..600):', colruns(mag, 210, 360, 3, 2))
print('magenta row runs (x457..547):', rowruns(mag, 457, 547, 5, 2))
print('orange col runs y210..360 (x540..620):', colruns(orange, 210, 360, 3, 2), 'sal', colruns(sal, 210, 360, 3, 2))
print('top rows y100..210 (x430..640): navy', rowruns(navy, 430, 640, 5, 2), 'green', rowruns(green, 430, 640, 5, 2), 'yellow', rowruns(yellowy, 430, 640, 5, 2), 'orange', rowruns(orange, 430, 640, 5, 2))
print('side cols y210..360 (x580..660): yellow', colruns(yellowy, 210, 360, 3, 2), 'bluegray', colruns(bluegray, 210, 360, 3, 2))

print('== RIGHT TENSOR + RED RECT ==')
print('red rect: strict red col runs y100..360 (x630..930):', colruns(red_strict, 100, 360, 100, 1))
print('red rect: strict red row runs (x640..930):', rowruns(red_strict, 640, 930, 100, 1))
print('magenta col runs y180..400 (x660..880):', colruns(mag, 180, 400, 3, 2))
print('magenta row runs (x689..818):', rowruns(mag, 689, 818, 5, 2))
print('top rows y74..190 (x640..900): navy', rowruns(navy, 640, 900, 5, 2), 'green', rowruns(green, 640, 900, 5, 2), 'yellow', rowruns(yellowy, 640, 900, 5, 2), 'orange', rowruns(orange, 640, 900, 5, 2))
print('side cols y180..400 (x815..900): yellow', colruns(yellowy, 180, 400, 3, 2), 'orange', colruns(orange, 180, 400, 3, 2), 'bluegray', colruns(bluegray, 180, 400, 3, 2))
print('arrows right: strict red row runs y360..430 (x640..930):', rowruns(red_strict, 640, 930, 10, 2))
print('  strict red col runs y300..380 (x600..930):', colruns(red_strict, 300, 380, 3, 2))
print('  strict red col runs y170..300 (x600..680):', colruns(red_strict, 170, 300, 3, 2))

print('== OVAL ==')
print('black fill row runs (x700..910):', rowruns(black, 700, 910, 30, 2))
print('black fill col runs y450..510 (x550..930):', colruns(black, 450, 510, 20, 2))
print('yellow text in oval: yellowy bbox within black:', end=' ')
ys, xs = np.where(yellowy[440:515, 690:915])
if len(xs): print(f'x {xs.min()+690}..{xs.max()+690} y {ys.min()+440}..{ys.max()+440}')

print('== TITLE metrics ==')
# strict red rows in x160..849
print('title red row runs (x160..849):', rowruns(red_strict, 160, 849, 5, 1))
# per-letter runs to estimate em: gaps
print('== HEADER metrics ==')
blue = (b > 120) & (b - r > 40) & (b - g > 30)
print('L1 col runs y113..133 (x40..300):', colruns(blue, 113, 133, 0, 1)[:8], '... x-extent', end=' ')
ys, xs = np.where(blue[113:133, 40:300])
print(f'{xs.min()+40}..{xs.max()+40}')
ys, xs = np.where(blue[142:162, 40:300])
print('L2 col extent y142..161:', f'{xs.min()+40}..{xs.max()+40}')
print('header row runs (x50..280):', rowruns(blue, 50, 280, 3, 1))

print('== BOTTOM TEXT LINES (per box) ==')
# group box text: dark ink rows within x265..440, y378..445
print('group box dark row runs (x265..440):', rowruns(dark, 265, 440, 3, 1))
print('group box dark col extent per band:', end=' ')
for (y0, y1) in [(378, 396), (400, 420), (422, 442)]:
    ys, xs = np.where(dark[y0:y1, 260:445])
    if len(xs): print(f'y{y0}-{y1}: x {xs.min()+260}..{xs.max()+260};', end=' ')
print()
# instance box text x455..865 y378..445
print('instance box dark row runs (x455..865):', rowruns(dark, 455, 865, 3, 1))
# layer box text y458..500 x62..700
print('layer box dark row runs (x62..700):', rowruns(dark, 62, 700, 3, 1))
