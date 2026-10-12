#!/usr/bin/env python3
"""Font metric solving for slide_039 from Liberation fonts (metric-compatible with
Times New Roman / Arial). Solves pt size from measured ink width; checks serif-vs-sans
for the white-box body by column-profile correlation. Banks results."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json

FR = 'videos/deep-learning/001_introduction/unique_slides/slide_039.jpg'
img = Image.open(FR).convert('RGB')
a = np.asarray(img).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
darkm = (R < 140) & (G < 140) & (B < 140)  # text ink (incl AA fringe)

LIB = '/usr/share/fonts/liberation/'
FONTS = {
    'serif': LIB + 'LiberationSerif-Regular.ttf',
    'serif-bold': LIB + 'LiberationSerif-Bold.ttf',
    'sans': LIB + 'LiberationSans-Regular.ttf',
    'sans-bold': LIB + 'LiberationSans-Bold.ttf',
    'sans-italic': LIB + 'LiberationSans-Italic.ttf',
}
_cache = {}
def ink_width(text, fontkey, px100=200):
    if fontkey not in _cache:
        _cache[fontkey] = ImageFont.truetype(FONTS[fontkey], px100)
    f = _cache[fontkey]
    im = Image.new('L', (int(px100 * len(text) * 0.8) + 100, px100 * 2), 255)
    d = ImageDraw.Draw(im)
    d.text((20, 20), text, font=f, fill=0)
    arr = np.asarray(im)
    cols = np.where((arr < 128).any(axis=0))[0]
    return float(cols.max() - cols.min() + 1)

def solve(text, fontkey, measured_px):
    w100 = ink_width(text, fontkey)
    return round(100.0 * measured_px / w100, 2)

LINES = {
    # name: (text, fontkey, measured ink width px)
    'title': ('How many filters we should apply', 'serif-bold', 763 - 203 + 1),
    'L1_hypothesis': ('Hypothesis', 'serif-bold', 193 - 85 + 1),
    'L2_natural': ('Natural images are stationary', 'serif', 358 - 85 + 1),
    'L3_visual': ('Visual features are common for different parts of one or multiple image', 'serif', 756 - 86 + 1),
    'L4_conclusion': ('Conclusion', 'serif-bold', 194 - 85 + 1),
    'L5_itis': ('It is not required to use different filters for different spatial locations  in the image', 'serif', 853 - 86 + 1),
    'L6_paren': ('(in other words, ', 'serif', None),
    'L6_phrase': ('apply same filter for ALL positions in the image', 'sans-bold', 718 - 243 + 1),
    'A1': ('Apply Red filter to detect ears in the whole image (not necessarily in the middle of the image)', 'sans-italic', 670 - 81 + 1),
    'A3': ('Apply Green filter to detect edges in the whole image', 'sans-italic', 417 - 82 + 1),
}

out = {}
for k, (txt, fk, mw) in LINES.items():
    if mw is None:
        continue
    s = solve(txt, fk, mw)
    out[k] = {'font': fk, 'measured_px': mw, 'solved_pt': s}
    print(f'{k:16s} {fk:12s} measured={mw:4d}px  solved={s}pt')

# serif vs sans for L2: correlation of column ink profiles at solved sizes
def render_profile(text, fontkey, size_px):
    f = ImageFont.truetype(FONTS[fontkey], int(round(size_px)))
    im = Image.new('L', (int(size_px * len(text)) + 60, int(size_px * 2.4)), 255)
    d = ImageDraw.Draw(im)
    d.text((20, 20), text, font=f, fill=0)
    arr = np.asarray(im)
    cols = (arr < 128).sum(axis=0)
    nz = np.where(cols > 0)[0]
    return cols[nz.min():nz.max() + 1].astype(float)

def orig_profile(y0, y1, x0, x1):
    seg = darkm[y0:y1 + 1, x0:x1 + 1]
    prof = seg.sum(axis=0).astype(float)
    return prof

def corr(p1, p2):
    n = min(len(p1), len(p2))
    p1, p2 = p1[:n], p2[:n]
    if p1.std() == 0 or p2.std() == 0:
        return 0.0
    return float(np.corrcoef(p1, p2)[0, 1])

# L2 crop: rows 136..158, x 83..361
op = orig_profile(136, 158, 83, 361)
for fk in ('serif', 'sans'):
    s = out['L2_natural']['solved_pt']
    rp = render_profile('Natural images are stationary', fk, s)
    # normalize lengths by resampling render profile to original length
    xs = np.linspace(0, len(rp) - 1, len(op))
    rp2 = np.interp(xs, np.arange(len(rp)), rp)
    print(f'L2 font test {fk}: corr={corr(op, rp2):.4f}')
    out[f'L2_corr_{fk}'] = corr(op, rp2)

# A2 segments: blue runs in rows 476-487
bluem = (B > 130) & (B - R > 40) & (B - G > 40)
seg = bluem[476:488, 60:450]
cols = np.where(seg.any(axis=0))[0]
runs = []
s = None
prev = None
for c in cols:
    if s is None:
        s = c
    elif c - prev > 3:
        runs.append((s + 60, prev + 60)); s = c
    prev = c
if s is not None:
    runs.append((s + 60, prev + 60))
print('A2 blue ink runs:', runs)
out['A2_runs'] = [[int(r[0]), int(r[1])] for r in runs]

# A1 segments: red word bounds + blue runs
redm = (R > 140) & (R - G > 60) & (R - B > 60)
seg1 = (bluem | redm)[460:472, 60:700]
cols1 = np.where(seg1.any(axis=0))[0]
runs1 = []
s = None; prev = None
for c in cols1:
    if s is None:
        s = c
    elif c - prev > 3:
        runs1.append((s + 60, prev + 60)); s = c
    prev = c
if s is not None:
    runs1.append((s + 60, prev + 60))
print('A1 ink runs (blue|red):', runs1[:8])
out['A1_runs'] = [[int(r[0]), int(r[1])] for r in runs1]
redcols = np.where(redm[460:472, 60:700].any(axis=0))[0]
print('A1 red word x:', redcols.min() + 60, redcols.max() + 60)
out['A1_red_x'] = [int(redcols.min() + 60), int(redcols.max() + 60)]

# A3 green word bounds
greenm = (G > 90) & (G - R > 20) & (G - B > 20)
gcols = np.where(greenm[492:504, 60:450].any(axis=0))[0]
print('A3 green word x:', gcols.min() + 60, gcols.max() + 60)
out['A3_green_x'] = [int(gcols.min() + 60), int(gcols.max() + 60)]

# L6: paren segment widths; black '(' run and ')' position
seg6 = darkm[269:290, 60:780]
cols6 = np.where(seg6.any(axis=0))[0]
runs6 = []
s = None; prev = None
for c in cols6:
    if s is None:
        s = c
    elif c - prev > 4:
        runs6.append((s + 60, prev + 60)); s = c
    prev = c
runs6.append((s + 60, prev + 60))
print('L6 ink runs:', runs6)
out['L6_runs'] = [[int(r[0]), int(r[1])] for r in runs6]

# per-line band bottoms for baselines (already measured); record here
out['bands_whitebox'] = [[111, 130], [138, 157], [162, 183], [217, 233], [243, 263], [269, 289]]
out['bands_annot'] = [[460, 471], [476, 487], [492, 503]]

# cursor region pixel dump
print('cursor area rows 348..372, x 436..462:')
for y in range(348, 373, 3):
    print(' y=%d:' % y, ' '.join('%d,(%d,%d,%d)' % (x, *a[y, x]) for x in range(436, 463, 3)))

with open('videos/deep-learning/001_introduction/recreated_pptx/qa/slide039/font_solve_out.json', 'w') as f:
    json.dump(out, f, indent=1)
print('BANKED -> qa/slide039/font_solve_out.json')
