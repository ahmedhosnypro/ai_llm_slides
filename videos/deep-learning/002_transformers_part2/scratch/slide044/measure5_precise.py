#!/usr/bin/env python3
"""Slide 044 — precision pass 5: exact edges, seams, bands, arrows, text colors."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

def runs_of(profile, thr, minlen=1):
    out, inrun = [], False
    for i, v in enumerate(profile):
        if v > thr and not inrun: s0 = i; inrun = True
        elif v <= thr and inrun:
            if i - s0 >= minlen: out.append((s0, i - 1))
            inrun = False
    if inrun: out.append((s0, len(profile) - 1))
    return out

def P(x, y): return tuple(int(v) for v in a[y, x])

print('== A. LEFT CUBE ==')
dark = lum < 130
# front left edge slant: first dark x per row, y186..425
print('left edge (first lum<130 x, y180..430 step 10):', [(y, int(np.where(dark[y, 40:210])[0].min()) + 40 if dark[y, 40:210].any() else -1) for y in range(180, 431, 10)])
# front bottom edge: last dark y per col
print('bottom edge (last dark y, x70..200 step 20):', [(x, int(np.where(dark[350:440, x])[0].max()) + 350 if dark[350:440, x].any() else -1) for x in range(70, 201, 20)])
# right extent of front + side strips at y=300
print('row y=300 classes x55..265:', end=' ')
prev = None
for x in range(55, 266):
    rr, gg, bb = a[300, x]
    c = 'R' if (rr > 150 and gg < 80 and bb < 80) else ('M' if (rr > 140 and bb > 140 and gg < 120) else ('S' if (rr > 190 and 60 < gg < 150 and bb < 110) else ('G' if (gg > 120 and gg - rr > 30 and gg - bb > 30) else ('Y' if (rr > 200 and gg > 190 and bb < 130) else ('N' if (bb > 110 and bb - rr > 20 and rr < 130) else ('k' if lum[300, x] < 130 else '.'))))))
    if c != prev: print(f'{x}{c}', end=' '); prev = c
print()
# row seams (black bands) in front: black rows x80..180
blackish = lum < 60
print('front black row runs (x80..180):', runs_of(blackish[180:440, 80:180].sum(axis=1), 20, 1))
# top bands: color classes per row x100..180, y95..235
print('top-face row colors y95..240 (x100..180 modal):')
for y in range(95, 241, 5):
    cs = []
    for x in range(100, 181):
        rr, gg, bb = a[y, x]
        if rr > 190 and gg > 190 and bb < 130: cs.append('Y')
        elif gg > 110 and gg - rr > 30 and gg - bb > 30: cs.append('G')
        elif rr > 180 and 90 < gg < 190 and bb < 100: cs.append('O')
        elif bb > 110 and bb - rr > 20 and rr < 130: cs.append('N')
        elif lum[y, x] < 130: cs.append('k')
        else: cs.append('.')
    c = Counter(cs).most_common(2)
    print(f'  y{y}: {c}')
# Samples arrow: red strokes y95..185, x40..260 (true red, dark-salmon-proof: g<70 & b<70)
tr2 = (r > 150) & (g < 70) & (b < 70)
print('Samples-arrow true-red row runs y95..185 (x40..260):', runs_of(tr2[95:185, 40:260].sum(axis=1), 2, 1))
for y0, y1 in runs_of(tr2[95:185, 40:260].sum(axis=1), 2, 1):
    xs = np.where(tr2[y0:y1+1, 40:260].sum(axis=0) > 0)[0]
    print(f'  band y{y0}..{y1}: x {xs.min()+40}..{xs.max()+40}')
# Samples text: dark text y104..140
print('Samples text dark bbox y104..142 x60..320:', end=' ')
ys, xs = np.where(dark[104:142, 60:320])
print(f'x {xs.min()+60}..{xs.max()+60} y {ys.min()+104}..{ys.max()+104}' if len(xs) else 'EMPTY')
# Channels arrow + text below front
print('below-front red rows y425..480 (x40..230):', runs_of(tr2[425:480, 40:230].sum(axis=1), 2, 1))
ys, xs = np.where(dark[455:485, 40:230])
print('below-front dark text bbox y455..485:', f'x {xs.min()+40}..{xs.max()+40} y {ys.min()+455}..{ys.max()+455}' if len(xs) else 'EMPTY')
print('text color sample (466..472):', [P(x, 469) for x in (95, 110, 125, 140, 155, 170)])
print('arrow shaft color y437:', [P(x, 437) for x in (80, 120, 160, 190)])

print('== B. GN CUBE ==')
mag = (r > 140) & (b > 140) & (g < 120)
print('GN front rows (x280..330):', runs_of(mag[150:380, 280:330].sum(axis=1), 10, 2))
print('GN front cols (y200..340):', runs_of(mag[200:340, 260:440].sum(axis=0), 10, 2))
print('GN row y=250 classes x270..475:', end=' ')
prev = None
for x in range(270, 476):
    rr, gg, bb = a[250, x]
    c = 'R' if (rr > 150 and gg < 80 and bb < 80) else ('M' if (rr > 140 and bb > 140 and gg < 120) else ('S' if (rr > 190 and 60 < gg < 150 and bb < 110) else ('G' if (gg > 120 and gg - rr > 30 and gg - bb > 30) else ('Y' if (rr > 200 and gg > 190 and bb < 130) else ('N' if (bb > 110 and bb - rr > 20 and rr < 130) else ('k' if lum[250, x] < 130 else '.'))))))
    if c != prev: print(f'{x}{c}', end=' '); prev = c
print()
print('GN seam samples:', [P(x, 250) for x in (274, 352, 385)])
print('GN top bands y95..185 (x300..420 modal):')
for y in range(95, 186, 5):
    cs = []
    for x in range(300, 421):
        rr, gg, bb = a[y, x]
        if rr > 190 and gg > 190 and bb < 130: cs.append('Y')
        elif gg > 110 and gg - rr > 30 and gg - bb > 30: cs.append('G')
        elif rr > 180 and 90 < gg < 190 and bb < 100: cs.append('O')
        elif bb > 110 and bb - rr > 20 and rr < 130: cs.append('N')
        elif lum[y, x] < 130: cs.append('k')
        else: cs.append('.')
    print(f'  y{y}: {Counter(cs).most_common(2)}')
print('GN side strips y=250 x410..475:', [P(x, 250) for x in range(412, 475, 8)])

print('== C. INSTANCE CUBE ==')
print('Inst front rows (x460..510):', runs_of(mag[150:380, 460:510].sum(axis=1), 10, 2))
print('Inst row y=280 classes x450..650:', end=' ')
prev = None
for x in range(450, 651):
    rr, gg, bb = a[280, x]
    c = 'R' if (rr > 150 and gg < 80 and bb < 80) else ('M' if (rr > 140 and bb > 140 and gg < 120) else ('S' if (rr > 190 and 60 < gg < 150 and bb < 110) else ('G' if (gg > 120 and gg - rr > 30 and gg - bb > 30) else ('Y' if (rr > 200 and gg > 190 and bb < 130) else ('N' if (bb > 110 and bb - rr > 20 and rr < 130) else ('k' if lum[280, x] < 130 else '.'))))))
    if c != prev: print(f'{x}{c}', end=' '); prev = c
print()
print('Inst seam/col samples y280:', [P(x, 280) for x in (455, 460, 505, 512, 520, 540, 548, 555, 570, 580, 590, 600, 610, 620)])
print('Inst top bands y100..195 (x480..600 modal):')
for y in range(100, 196, 5):
    cs = []
    for x in range(480, 601):
        rr, gg, bb = a[y, x]
        if rr > 190 and gg > 190 and bb < 130: cs.append('Y')
        elif gg > 110 and gg - rr > 30 and gg - bb > 30: cs.append('G')
        elif rr > 180 and 90 < gg < 190 and bb < 100: cs.append('O')
        elif bb > 110 and bb - rr > 20 and rr < 130: cs.append('N')
        elif lum[y, x] < 130: cs.append('k')
        else: cs.append('.')
    print(f'  y{y}: {Counter(cs).most_common(2)}')

print('== D. RIGHT TENSOR ==')
print('RT front rows (x690..810):', runs_of(mag[140:380, 690:810].sum(axis=1), 10, 2))
print('RT row y=250 classes x640..905:', end=' ')
prev = None
for x in range(640, 906):
    rr, gg, bb = a[250, x]
    c = 'R' if (rr > 150 and gg < 80 and bb < 80) else ('M' if (rr > 140 and bb > 140 and gg < 120) else ('S' if (rr > 190 and 60 < gg < 150 and bb < 110) else ('G' if (gg > 120 and gg - rr > 30 and gg - bb > 30) else ('Y' if (rr > 200 and gg > 190 and bb < 130) else ('N' if (bb > 110 and bb - rr > 20 and rr < 130) else ('k' if lum[250, x] < 130 else '.'))))))
    if c != prev: print(f'{x}{c}', end=' '); prev = c
print()
print('RT rect border samples:', [P(x, 200) for x in (644, 646, 648, 650, 652, 890, 892, 894, 896, 898)])
print('RT rect border vertical extent x648:', [y for y in range(80, 400) if lum[y, 648] < 150][:5], '...', end=' ')
col = lum[:, 648] < 150
ys = np.where(col[60:420])[0]
print(f'y {ys.min()+60}..{ys.max()+60}' if len(ys) else 'none')
print('RT rect top/bottom: x700..800 red-ish row runs y80..400:', runs_of(((r > 140) & (g < 120) & (b < 120))[80:400, 700:800].sum(axis=1), 30, 1))
print('RT top bands y85..175 (x700..800 modal):')
for y in range(85, 176, 5):
    cs = []
    for x in range(700, 801):
        rr, gg, bb = a[y, x]
        if rr > 190 and gg > 190 and bb < 130: cs.append('Y')
        elif gg > 110 and gg - rr > 30 and gg - bb > 30: cs.append('G')
        elif rr > 180 and 90 < gg < 190 and bb < 100: cs.append('O')
        elif bb > 110 and bb - rr > 20 and rr < 130: cs.append('N')
        elif lum[y, x] < 130: cs.append('k')
        else: cs.append('.')
    print(f'  y{y}: {Counter(cs).most_common(2)}')
# FV vertical arrow: red-ish vertical line x600..690?
redish = (r > 140) & (g < 110) & (b < 110)
print('FV arrow: redish col runs y150..340 (x600..695):', runs_of(redish[150:340, 600:695].sum(axis=0), 20, 1))
ys, xs = np.where(dark[150:350, 600:660])
print('FV label strip dark bbox x600..660 y150..350:', f'x {xs.min()+600}..{xs.max()+600} y {ys.min()+150}..{ys.max()+150}' if len(xs) else 'EMPTY')
# Channels h-arrow under RT
print('RT Channels: redish row runs y365..400 (x630..900):', runs_of(redish[365:400, 630:900].sum(axis=1), 5, 1))
ys, xs = np.where(dark[350:372, 630:900])
print('Channels label dark bbox y350..372:', f'x {xs.min()+630}..{xs.max()+630} y {ys.min()+350}..{ys.max()+350}' if len(xs) else 'EMPTY')
# Batch size diagonal: redish in y240..380 x760..910
print('BatchSize: redish row runs y230..385 (x750..915):', runs_of(redish[230:385, 750:915].sum(axis=1), 5, 1))
ys, xs = np.where(dark[230:385, 750:915])
print('BatchSize label dark bbox x750..915 y230..385:', f'x {xs.min()+750}..{xs.max()+750} y {ys.min()+230}..{ys.max()+230}' if len(xs) else 'EMPTY')

print('== E. BOTTOM BOXES + OVAL ==')
blackish2 = lum < 75
print('oval black col runs y450..485 (x600..930):', runs_of(blackish2[450:485, 600:930].sum(axis=0), 10, 2))
print('oval black row runs (x700..870):', runs_of(blackish2[440:500, 700:870].sum(axis=1), 30, 1))
ys, xs = np.where((r > 200) & (g > 190) & (b < 130)[0:0]) if False else (None, None)
yellowy = (r > 200) & (g > 190) & (b < 130)
ys, xs = np.where(yellowy[450:490, 640:930])
print('oval yellow text bbox:', f'x {xs.min()+640}..{xs.max()+640} y {ys.min()+450}..{ys.max()+450}' if len(xs) else 'EMPTY')
# box borders hunt: horizontal lines in x270..430 (group) / x460..860 (instance) / x60..900 (layer)
for (label, x0, x1) in [('group', 270, 430), ('inst', 460, 860), ('layer', 62, 640)]:
    seg = lum[350:515, x0:x1]
    print(f'{label} box: rows where >60% cols are 120<lum<215 (light border?) or lum<130:', end=' ')
    hits = []
    for i in range(seg.shape[0]):
        row = seg[i]
        frac_dark = (row < 130).mean(); frac_mid = ((row > 120) & (row < 215)).mean()
        if frac_dark > 0.5 or frac_mid > 0.6: hits.append((350 + i, round(float(frac_dark), 2), round(float(frac_mid), 2)))
    print(hits[:14])
print('layer box text colors y463..473 x70..250 modal:')
cnt = Counter()
for y in range(462, 475):
    for x in range(66, 260):
        rr, gg, bb = a[y, x]
        if lum[y, x] < 140: cnt[(rr // 40 * 40, gg // 40 * 40, bb // 40 * 40)] += 1
print('  ', cnt.most_common(6))
print('layer box body y481..497 x66..660 color classes:', end=' ')
cnt2 = Counter()
for y in range(480, 498):
    for x in range(66, 660):
        rr, gg, bb = a[y, x]
        if rr > 150 and gg < 90 and bb < 90: cnt2['RED'] += 1
        elif bb > 110 and bb - rr > 40 and rr < 130: cnt2['BLUE'] += 1
        elif gg > 110 and gg - rr > 40 and gg - bb > 40: cnt2['GREEN'] += 1
        elif lum[y, x] < 120: cnt2['BLACK'] += 1
print(dict(cnt2))
print('inst box lines y382..430 colors (x460..900):')
for (y0, y1) in [(380, 394), (398, 415), (416, 432)]:
    cnt3 = Counter()
    for y in range(y0, y1):
        for x in range(460, 900):
            rr, gg, bb = a[y, x]
            if rr > 150 and gg < 90 and bb < 90: cnt3['RED'] += 1
            elif bb > 110 and bb - rr > 40 and rr < 130: cnt3['BLUE'] += 1
            elif gg > 110 and gg - rr > 40 and gg - bb > 40: cnt3['GREEN'] += 1
            elif lum[y, x] < 120: cnt3['BLACK'] += 1
    print(f'  y{y0}..{y1}: {dict(cnt3)}')
print('group box lines y378..432 colors (x265..440):')
for (y0, y1) in [(377, 392), (394, 412), (413, 430)]:
    cnt4 = Counter()
    for y in range(y0, y1):
        for x in range(265, 440):
            rr, gg, bb = a[y, x]
            if rr > 150 and gg < 90 and bb < 90: cnt4['RED'] += 1
            elif bb > 110 and bb - rr > 40 and rr < 130: cnt4['BLUE'] += 1
            elif gg > 110 and gg - rr > 40 and gg - bb > 40: cnt4['GREEN'] += 1
            elif lum[y, x] < 120: cnt4['BLACK'] += 1
    print(f'  y{y0}..{y1}: {dict(cnt4)}')
print('mystery red y455 x462..744 samples:', [P(x, 455) for x in (470, 520, 570, 620, 660, 700, 740)])
print('y462..443?? inst box bottom border hunt x460..860 y435..445:', runs_of(((lum[435:446, 460:860]) < 160).sum(axis=1), 100, 1))
