#!/usr/bin/env python3
"""Slide 044 — final measurement pass: seams, arrow fine maps, borders, word colors."""
import numpy as np
from PIL import Image
from collections import Counter

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_044.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
lum = 0.299 * r + 0.587 * g + 0.114 * b

def amap(x0, y0, x1, y1, step, label):
    print(f'--- {label} ({x0},{y0})..({x1},{y1}) step {step} ---')
    hdr = '     ' + ''.join(str(((x0 + i * step) // 10) % 10) for i in range((x1 - x0) // step + 1))
    print(hdr)
    for y in range(y0, y1, step):
        row = []
        for x in range(x0, x1, step):
            rr, gg, bb = a[y, x]
            L = 0.299 * rr + 0.587 * gg + 0.114 * bb
            if rr > 190 and gg > 190 and bb < 130: c = 'Y'
            elif gg > 110 and gg - rr > 30 and gg - bb > 30: c = 'G'
            elif rr > 180 and 90 < gg < 190 and bb < 100: c = 'O'
            elif rr > 140 and bb > 140 and gg < 120: c = 'M'
            elif bb > 110 and bb - rr > 20 and rr < 130: c = 'N'
            elif L < 55: c = '#'
            elif L < 130: c = 'k'
            elif rr > 150 and gg < 90 and bb < 90: c = 'R'
            elif rr > 150 and 90 <= gg < 160 and bb < 120: c = 's'
            else: c = '.'
        # noqa
            row.append(c)
        print(f'{y:4d} ' + ''.join(row))

def runs_of(profile, thr, minlen=1):
    out, inrun = [], False
    for i, v in enumerate(profile):
        if v > thr and not inrun: s0 = i; inrun = True
        elif v <= thr and inrun:
            if i - s0 >= minlen: out.append((s0, i - 1))
            inrun = False
    if inrun: out.append((s0, len(profile) - 1))
    return out

print('== 1. LEFT CUBE TOP (fine) ==')
amap(40, 92, 280, 245, 3, 'left cube top face + Samples arrow')
print('== 2. FV arrow region ==')
amap(590, 140, 700, 365, 3, 'Feature Vector arrow + label')
print('== 3. BatchSize region ==')
amap(745, 225, 920, 390, 3, 'Batch size arrow + label')
print('== 4. left front seams: luminance col profile y350..400 mean ==')
prof = lum[350:400, 55:210].mean(axis=0)
print('dark cols (<140):', [x + 55 for x in range(len(prof)) if prof[x] < 140])
prof2 = lum[250:290, 55:210].mean(axis=0)
print('dark cols y250..290 (<140):', [x + 55 for x in range(len(prof2)) if prof2[x] < 140])
print('front row seams: lum row profile x90..180:')
for y in range(225, 430, 3):
    v = lum[y, 90:180].mean()
    if v < 100: print(f'  y{y}: {v:.0f}')
print('== 5. GN front seams ==')
print('GN col profile y250..300 mean, dark(<140):', [x for x in range(270, 425) if lum[250:300, x].mean() < 140])
print('GN row seams x290..330:', [y for y in range(175, 340) if lum[y, 290:330].mean() < 100])
print('== 6. Instance front seams ==')
print('Inst col profile y280..330 dark(<140):', [x for x in range(450, 660) if lum[280:330, x].mean() < 140])
print('Inst row seams x470..540:', [y for y in range(195, 360) if lum[y, 470:540].mean() < 100])
print('== 7. RT front seams ==')
print('RT col profile y230..280 dark(<140):', [x for x in range(680, 900) if lum[230:280, x].mean() < 140])
print('RT row seams x700..800:', [y for y in range(160, 340) if lum[y, 700:800].mean() < 100])
print('== 8. box borders: exact colors ==')
def line_color(y, x0, x1):
    seg = a[y, x0:x1]
    m = seg.mean(axis=0)
    return f'y{y}: rgb({m[0]:.0f},{m[1]:.0f},{m[2]:.0f})'
print('group top y371/372:', line_color(371, 270, 430), line_color(372, 270, 430))
print('group bottom y443/444:', line_color(443, 270, 430), line_color(444, 270, 430))
print('inst top y363/364:', line_color(363, 465, 855), line_color(364, 465, 855))
print('inst bottom y441/442:', line_color(441, 465, 855), line_color(442, 465, 855))
print('layer top y455/456:', line_color(455, 70, 900), line_color(456, 70, 900))
print('layer bottom y500/501:', line_color(500, 70, 900), line_color(501, 70, 900))
print('y509..511:', line_color(509, 70, 900), line_color(510, 70, 900), line_color(511, 70, 900))
# box left/right edges: scan columns for the box fills
print('box vertical borders: group x-scan y400..430 (pale bands):', [x for x in range(250, 460) if 120 < lum[400:430, x].mean() < 225 and lum[400:430, x].std() < 60][:6], '...', [x for x in range(250, 460) if lum[400:430, x].mean() < 235 and abs(lum[400:430, x].mean() - lum[395:400, x].mean()) > 25][:8])
print('inst box left/right: fill extent y400..430 where greenish (g>r):', [x for x in range(440, 900) if (a[400:430, x, 1] - a[400:430, x, 0]).mean() > 8][:3], [x for x in range(440, 900) if (a[400:430, x, 1] - a[400:430, x, 0]).mean() > 8][-3:])
print('layer box left/right: fill extent y470..495 pinkish (r>g):', [x for x in range(40, 930) if (a[470:495, x, 0] - a[470:495, x, 1]).mean() > 12][:3], [x for x in range(40, 930) if (a[470:495, x, 0] - a[470:495, x, 1]).mean() > 12][-3:])
print('I-beam x796 vertical extent:', runs_of((lum[:, 795:798].mean(axis=1) < 150), 0, 1)[:4], '...')
print('== 9. text word colors ==')
def wordcensus(y0, y1, x0, x1, label):
    print(f'{label}:')
    cols = {'R': [], 'B': [], 'G': [], 'K': []}
    for x in range(x0, x1):
        cc = Counter()
        for y in range(y0, y1):
            rr, gg, bb = a[y, x]
            if rr > 150 and gg < 90 and bb < 90: cc['R'] += 1
            elif bb > 110 and bb - rr > 40 and rr < 130: cc['B'] += 1
            elif gg > 110 and gg - rr > 40 and gg - bb > 40: cc['G'] += 1
            elif 0.299 * rr + 0.587 * gg + 0.114 * bb < 120: cc['K'] += 1
        tot = sum(cc.values())
        if tot >= 2: cols[max(cc, key=cc.get)].append(x)
    def runsx(lst):
        if not lst: return []
        out, s0, p = [], lst[0], lst[0]
        for v in lst[1:]:
            if v - p > 6: out.append((s0, p)); s0 = v
            p = v
        out.append((s0, p)); return out
    for k in 'RBGK':
        print(f'  {k}: {runsx(cols[k])}')
wordcensus(377, 393, 260, 445, 'group L1')
wordcensus(394, 413, 260, 445, 'group L2')
wordcensus(414, 431, 260, 445, 'group L3')
wordcensus(372, 394, 460, 900, 'inst L1')
wordcensus(396, 416, 460, 900, 'inst L2')
wordcensus(416, 433, 460, 900, 'inst L3')
wordcensus(458, 476, 60, 910, 'layer L1')
wordcensus(480, 499, 60, 910, 'layer L2')
print('== 10. inst/layer/group line x extents + baselines ==')
darktx = lum < 140
for (label, y0, y1, x0, x1) in [('groupL1', 375, 393, 255, 450), ('groupL2', 394, 413, 255, 450), ('groupL3', 414, 432, 255, 450),
                                 ('instL1', 370, 395, 455, 905), ('instL2', 396, 416, 455, 905), ('instL3', 416, 434, 455, 905),
                                 ('layerL1', 456, 478, 55, 910), ('layerL2', 479, 500, 55, 910)]:
    ys, xs = np.where(darktx[y0:y1, x0:x1])
    if len(xs): print(f'{label}: x {xs.min()+x0}..{xs.max()+x0}  y {ys.min()+y0}..{ys.max()+y0}')
print('== 11. RT rect borders exact ==')
print('rect left border col candidates y200..340:', [x for x in range(630, 690) if lum[200:340, x].mean() < 180 and abs(a[200:340, x, 0] - a[200:340, x, 2]).mean() > 15])
print('rect right border y200..340:', [x for x in range(880, 905) if lum[200:340, x].mean() < 200])
print('samples x640..660 y250:', [(x, tuple(int(v) for v in a[250, x])) for x in range(640, 662, 2)])
print('samples x890..903 y250:', [(x, tuple(int(v) for v in a[250, x])) for x in range(890, 903, 1)])
print('samples x760..780 y92:', [(y, tuple(int(v) for v in a[y, 760])) for y in range(90, 96)])
print('samples x760..780 y362:', [(y, tuple(int(v) for v in a[y, 760])) for y in range(360, 366)])
print('== 12. Channels-arrow RT + heads ==')
redish = (r > 140) & (g < 110) & (b < 110)
print('y372..378 red col runs x630..900:', runs_of(redish[372:379, 630:900].sum(axis=0), 0, 1))
print('== 13. left Channels arrow ==')
print('y434..442 red col runs x40..240:', runs_of(redish[434:443, 40:240].sum(axis=0), 0, 1))
print('== 14. Samples arrow fine: red-ish rows y100..190 x50..280 ==')
print(runs_of(redish[100:190, 50:280].sum(axis=1), 2, 1))
for y0, y1 in runs_of(redish[100:190, 50:280].sum(axis=1), 2, 1):
    xs = np.where(redish[y0:y1 + 1, 50:280].sum(axis=0) > 0)[0]
    print(f'  y{y0+100}..{y1+100}: x {xs.min()+50}..{xs.max()+50}')
print('== 15. GN top face fine ==')
amap(255, 85, 480, 195, 3, 'GN top face')
print('== 16. Instance top fine ==')
amap(440, 95, 665, 210, 3, 'Instance top face')
print('== 17. RT top fine ==')
amap(630, 80, 905, 180, 3, 'RT top face')
