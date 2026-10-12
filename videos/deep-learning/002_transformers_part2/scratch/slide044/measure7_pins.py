#!/usr/bin/env python3
"""Slide 044 — pass 7: FINAL geometry pins (samples not profiles)."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

def P(x, y): return tuple(int(v) for v in a[y, x])

print('== L-CUBE front-left/bottom/right edges ==')
for y in (250, 280, 310, 340, 370, 400, 418):
    row = lum[y]
    xs = np.where(row[55:280] < 140)[0]
    if len(xs):
        xs = xs + 55
        # find contiguous main run
        print(f'y{y}: ink {xs.min()}..{xs.max()}')
print('L bottom: last ink y per col:', [(x, int(np.where(lum[300:445, x] < 140)[0].max()) + 300) for x in (80, 120, 160, 195)])
print('L front color cells:', [P(x, 300) for x in (80, 110, 140, 170, 190)])
print('L side strip colors y300:', [(x, P(x, 300)) for x in range(196, 272, 6)])
print('L side strips vertical extent x210, x240, x260:', [int(np.where(lum[150:440, x] < 160)[0].min()) + 150 for x in (210, 240, 260)], [int(np.where(lum[150:440, x] < 160)[0].max()) + 150 for x in (210, 240, 260)])
print('== top band edge slant: left cube ==')
for y in (100, 112, 130, 148, 166, 184):
    xs = np.where(lum[y, 40:280] < 140)[0]
    print(f'y{y}: ink x {xs.min()+40 if len(xs) else -1}..{xs.max()+40 if len(xs) else -1} n={len(xs)}')
print('== GN front edges ==')
for y in (190, 220, 250, 280, 310, 328):
    xs = np.where(lum[y, 260:480] < 140)[0]
    print(f'y{y}: ink {xs.min()+260 if len(xs) else -1}..{xs.max()+260 if len(xs) else -1}')
print('GN bottom per col:', [(x, int(np.where(lum[300:380, x] < 140)[0].max()) + 300) for x in (285, 320, 355, 390, 405)])
print('GN front colors:', [P(x, 250) for x in (290, 320, 350, 380, 400)], 'row y322:', [P(x, 322) for x in (290, 350, 400)])
print('== Instance edges ==')
for y in (210, 240, 270, 300, 330, 348):
    xs = np.where(lum[y, 440:665] < 140)[0]
    print(f'y{y}: ink {xs.min()+440 if len(xs) else -1}..{xs.max()+440 if len(xs) else -1}')
print('Inst bottom per col:', [(x, int(np.where(lum[300:375, x] < 140)[0].max()) + 300) for x in (465, 500, 540, 570, 600)])
print('Inst front colors y300:', [P(x, 300) for x in (470, 500, 530, 555, 580)])
print('Inst side strips y300:', [(x, P(x, 300)) for x in range(586, 652, 5)])
print('== RT edges ==')
for y in (175, 200, 230, 260, 290, 320, 328):
    xs = np.where(lum[y, 655:910] < 150)[0]
    print(f'y{y}: ink {xs.min()+655 if len(xs) else -1}..{xs.max()+655 if len(xs) else -1}')
print('RT bottom per col:', [(x, int(np.where(lum[300:345, x] < 150)[0].max()) + 300) for x in (700, 740, 780, 815)])
print('RT front colors y250:', [P(x, 250) for x in (700, 740, 780, 810)], 'y300:', [P(x, 300) for x in (700, 780, 815)])
print('RT top-left slant: first ink x per row y95..175:', [(y, int(np.where(lum[y, 655:900] < 150)[0].min()) + 655) for y in range(95, 176, 8)])
print('== FV arrow ==')
print('FV shaft: x-runs of red-ish y200..330:', [x for x in range(595, 690) if ((a[200:330, x, 0] > 130) & (a[200:330, x, 1] < 120) & (a[200:330, x, 2] < 120)).sum() > 60])
print('FV shaft color:', [P(659, y) for y in (160, 200, 240, 280, 320)])
print('FV heads: red-ish y95..175 x600..680 rows:', [y for y in range(95, 175) if ((a[y, 600:680, 0] > 130) & (a[y, 600:680, 1] < 120) & (a[y, 600:680, 2] < 120)).sum() > 5])
print('FV bottom tip: red-ish y330..360:', [y for y in range(330, 362) if ((a[y, 600:680, 0] > 130) & (a[y, 600:680, 1] < 120) & (a[y, 600:680, 2] < 120)).sum() > 5])
print('label strip x-runs y180..340 (dark, x595..655):', [x for x in range(595, 656) if (lum[180:340, x] < 120).sum() > 20])
print('== BatchSize arrow ==')
print('BS shaft: red-ish in y230..360 x780..905:', [(y, np.where((a[y, 780:905, 0] > 130) & (a[y, 780:905, 1] < 120) & (a[y, 780:905, 2] < 120))[0].min() + 780) for y in range(230, 361, 10) if ((a[y, 780:905, 0] > 130) & (a[y, 780:905, 1] < 120) & (a[y, 780:905, 2] < 120)).sum() > 0])
print('BS label: dark bbox x770..880 y240..300:', end=' ')
ys, xs = np.where(lum[240:300, 770:880] < 120)
print(f'x {xs.min()+770}..{xs.max()+770} y {ys.min()+240}..{ys.max()+240}' if len(xs) else 'EMPTY')
print('BS label color cores:', [P(x, y) for (x, y) in [(800, 260), (820, 270), (840, 285), (790, 290), (850, 255)]])
print('== left Channels arrow ==')
print('shaft y-extent x120..180:', [y for y in range(425, 450) if ((a[y, 120:180, 0] > 130) & (a[y, 120:180, 1] < 130) & (a[y, 120:180, 2] < 130)).sum() > 20])
print('shaft tips: red col runs y434..440:', [x for x in range(40, 250) if ((a[434:441, x, 0] > 130) & (a[434:441, x, 1] < 130) & (a[434:441, x, 2] < 130)).sum() > 2][:6], '...', [x for x in range(40, 250) if ((a[434:441, x, 0] > 130) & (a[434:441, x, 1] < 130) & (a[434:441, x, 2] < 130)).sum() > 2][-6:])
print('Channels label: dark bbox y455..490 x50..240:', end=' ')
ys, xs = np.where(lum[455:490, 50:240] < 130)
print(f'x {xs.min()+50}..{xs.max()+50} y {ys.min()+455}..{ys.max()+455}' if len(xs) else 'EMPTY')
print('label core colors:', [P(x, y) for (x, y) in [(90, 469), (110, 469), (130, 469), (150, 469), (100, 476)]])
print('== RT Channels arrow ==')
print('shaft rows y368..382 x640..900:', [y for y in range(368, 383) if ((a[y, 640:900, 0] > 130) & (a[y, 640:900, 1] < 130) & (a[y, 640:900, 2] < 130)).sum() > 40])
print('tips: red col runs y372..380:', [x for x in range(630, 910) if ((a[372:381, x, 0] > 130) & (a[372:381, x, 1] < 130) & (a[372:381, x, 2] < 130)).sum() > 2][:6], '...', [x for x in range(630, 910) if ((a[372:381, x, 0] > 130) & (a[372:381, x, 1] < 130) & (a[372:381, x, 2] < 130)).sum() > 2][-6:])
print('RT Channels label: dark bbox y348..372 x650..760:', end=' ')
ys, xs = np.where(lum[348:372, 650:760] < 130)
print(f'x {xs.min()+650}..{xs.max()+650} y {ys.min()+348}..{ys.max()+348}' if len(xs) else 'EMPTY')
print('label cores:', [P(x, y) for (x, y) in [(680, 358), (700, 358), (720, 360)]])
print('== Samples arrow FINAL ==')
# the diagonal arrow: look for reddish diagonal between (60..210, 100..175)
print('reddish diag mask rows y100..180:', [(y, [x for x in range(50, 230) if a[y, x, 0] > 140 and a[y, x, 1] < 110 and a[y, x, 2] < 110]) for y in range(100, 181, 10)])
print('== GN navy band full row ==')
print('y88 navy x-extent:', np.where((a[88, :, 2] > 110) & (a[88, :, 2] - a[88, :, 0] > 20) & (a[88, :, 0] < 130))[0].min(), np.where((a[88, :, 2] > 110) & (a[88, :, 2] - a[88, :, 0] > 20) & (a[88, :, 0] < 130))[0].max())
print('y89..90 navy extent:', np.where((a[90, :, 2] > 110) & (a[90, :, 2] - a[90, :, 0] > 20) & (a[90, :, 0] < 130))[0].min(), np.where((a[90, :, 2] > 110) & (a[90, :, 2] - a[90, :, 0] > 20) & (a[90, :, 0] < 130))[0].max())
print('navy row y112 extent:', np.where((a[112, :, 2] > 110) & (a[112, :, 2] - a[112, :, 0] > 20) & (a[112, :, 0] < 130))[0].min(), np.where((a[112, :, 2] > 110) & (a[112, :, 2] - a[112, :, 0] > 20) & (a[112, :, 0] < 130))[0].max())
print('navy row y134 extent:', np.where((a[134, :, 2] > 110) & (a[134, :, 2] - a[134, :, 0] > 20) & (a[134, :, 0] < 130))[0].min(), np.where((a[134, :, 2] > 110) & (a[134, :, 2] - a[134, :, 0] > 20) & (a[134, :, 0] < 130))[0].max())
print('Inst navy y134 extent:', np.where((a[134, :, 2] > 110) & (a[134, :, 2] - a[134, :, 0] > 20) & (a[134, :, 0] < 130))[0].min(), np.where((a[134, :, 2] > 110) & (a[134, :, 2] - a[134, :, 0] > 20) & (a[134, :, 0] < 130))[0].max())
print('navy rows around x500:', [y for y in range(80, 220) if a[y, 500, 2] > 110 and a[y, 500, 2] - a[y, 500, 0] > 20 and a[y, 500, 0] < 130])
print('navy rows around x750:', [y for y in range(80, 220) if a[y, 750, 2] > 110 and a[y, 750, 2] - a[y, 750, 0] > 20 and a[y, 750, 0] < 130])
print('== title/header exact ==')
ys, xs = np.where((r > 150) & (g < 90) & (b < 90)[0:0]) if False else (None, None)
tr = (r > 150) & (g < 90) & (b < 90)
ys, xs = np.where(tr[50:100, 100:900])
print('title bbox:', xs.min() + 100, xs.max() + 100, ys.min() + 50, ys.max() + 50)
blu = (b > 120) & (b - r > 40) & (b - g > 30)
ys, xs = np.where(blu[105:140, 50:300])
print('hdrL1 bbox:', xs.min() + 50, xs.max() + 50, ys.min() + 105, ys.max() + 105)
ys, xs = np.where(blu[135:170, 50:300])
print('hdrL2 bbox:', xs.min() + 50, xs.max() + 50, ys.min() + 135, ys.max() + 135)
print('hdr color core:', P(100, 125), P(150, 125), P(120, 152))
print('title color core:', P(300, 65), P(400, 70))
print('== oval final ==')
blk = lum < 75
ys, xs = np.where(blk[448:485, 700:910])
print('oval bbox x', xs.min() + 700, xs.max() + 700, 'y', ys.min() + 448, ys.max() + 448)
print('oval row profile (x700..880):', [(y, int((lum[y, 700:880] < 75).sum())) for y in range(448, 486, 2)])
yel = (r > 190) & (g > 170) & (b < 140)
ys, xs = np.where(yel[455:478, 730:890])
print('oval text bbox x', xs.min() + 730, xs.max() + 730, 'y', ys.min() + 455, ys.max() + 455)
print('== box borders left/right cols ==')
for label, y0, y1, xr in [('group', 396, 412, range(250, 280)), ('groupR', 396, 412, range(420, 450)), ('instL', 396, 412, range(455, 485)), ('instR', 396, 412, range(855, 890)), ('layerL', 470, 495, range(50, 80)), ('layerR', 470, 495, range(895, 915))]:
    print(label, [(x, P(x, (y0 + y1) // 2), round(float(lum[y0:y1, x].mean()))) for x in xr])
