#!/usr/bin/env python3
"""Font metric solving v2 — empirical ink-bbox method.
For each line: solve size by matching rendered ink WIDTH, then verify predicted ink
HEIGHT vs measured; discriminate serif/sans by column-profile correlation at the
solved size (no resampling). Banks results."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json

FR = 'videos/deep-learning/001_introduction/unique_slides/slide_039.jpg'
img = Image.open(FR).convert('RGB')
a = np.asarray(img).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
darkm = (R < 140) & (G < 140) & (B < 140)

LIB = '/usr/share/fonts/liberation/'
DJ = '/usr/share/fonts/TTF/'
CANDS = {
    'serif': LIB + 'LiberationSerif-Regular.ttf',
    'serif-bold': LIB + 'LiberationSerif-Bold.ttf',
    'sans': LIB + 'LiberationSans-Regular.ttf',
    'sans-bold': LIB + 'LiberationSans-Bold.ttf',
    'sans-italic': LIB + 'LiberationSans-Italic.ttf',
    'djserif': DJ + 'DejaVuSerif.ttf' if __import__('os').path.exists(DJ + 'DejaVuSerif.ttf') else LIB + 'LiberationSerif-Regular.ttf',
    'djsans': DJ + 'DejaVuSans.ttf',
}

def render_ink(text, fontkey, size_px):
    f = ImageFont.truetype(CANDS[fontkey], int(round(size_px)))
    W = int(size_px * len(text) * 1.2) + 100
    im = Image.new('L', (W, int(size_px * 3) + 60), 255)
    d = ImageDraw.Draw(im)
    d.text((30, 30), text, font=f, fill=0)
    arr = np.asarray(im)
    ink = arr < 128
    ys, xs = np.where(ink)
    return (float(xs.max() - xs.min() + 1), float(ys.max() - ys.min() + 1)), ink

def solve_by_width(text, fontkey, target_w):
    lo, hi = 4.0, 80.0
    for _ in range(40):
        mid = (lo + hi) / 2
        (w, _h), _ = render_ink(text, fontkey, mid)
        if w < target_w:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 2)

def profile(ink2d):
    cols = ink2d.sum(axis=0).astype(float)
    nz = np.where(cols > 0)[0]
    return cols[nz.min():nz.max() + 1]

def corr(p1, p2):
    n = min(len(p1), len(p2))
    p1, p2 = np.asarray(p1[:n]), np.asarray(p2[:n])
    if p1.std() == 0 or p2.std() == 0:
        return 0.0
    return float(np.corrcoef(p1, p2)[0, 1])

def orig_ink(y0, y1, x0, x1):
    seg = darkm[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(seg)
    return (float(xs.max() - xs.min() + 1), float(ys.max() - ys.min() + 1)), seg

LINES = {
    'title': {'text': 'How many filters we should apply', 'box': (57, 93, 201, 765), 'cands': ['serif-bold', 'sans-bold', 'djsans']},
    'L1_hypothesis': {'text': 'Hypothesis', 'box': (109, 132, 83, 196), 'cands': ['serif-bold', 'sans-bold']},
    'L2_natural': {'text': 'Natural images are stationary', 'box': (136, 159, 83, 361), 'cands': ['serif', 'sans', 'djserif', 'djsans']},
    'L3_visual': {'text': 'Visual features are common for different parts of one or multiple image', 'box': (160, 185, 84, 758), 'cands': ['serif', 'sans', 'djserif', 'djsans']},
    'L4_conclusion': {'text': 'Conclusion', 'box': (215, 235, 83, 196), 'cands': ['serif-bold', 'sans-bold']},
    'L5_itis': {'text': 'It is not required to use different filters for different spatial locations  in the image', 'box': (241, 265, 84, 855), 'cands': ['serif', 'sans', 'djserif', 'djsans']},
    'L6_phrase': {'text': 'apply same filter for ALL positions in the image', 'box': (269, 290, 241, 720), 'cands': ['sans-bold', 'serif-bold'], 'red_only': True},
    'A1': {'text': 'Apply Red filter to detect ears in the whole image (not necessarily in the middle of the image)', 'box': (458, 473, 79, 672), 'cands': ['sans-italic', 'sans', 'serif-italic' if False else 'sans']},
    'A3': {'text': 'Apply Green filter to detect edges in the whole image', 'box': (490, 505, 80, 419), 'cands': ['sans-italic', 'sans']},
}

out = {}
for k, spec in LINES.items():
    y0, y1, x0, x1 = spec['box']
    if k == 'L6_phrase':
        # red ink only
        redm = (R > 140) & (R - G > 60) & (R - B > 60)
        seg = redm[y0:y1 + 1, x0:x1 + 1]
        ys, xs = np.where(seg)
        mw, mh = float(xs.max() - xs.min() + 1), float(ys.max() - ys.min() + 1)
        oprof = profile(seg)
    else:
        (mw, mh), seg = orig_ink(y0, y1, x0, x1)
        oprof = profile(seg)
    res = {}
    for fk in spec['cands']:
        s = solve_by_width(spec['text'], fk, mw)
        (w, h), ink2 = render_ink(spec['text'], fk, s)
        c = corr(oprof, profile(ink2))
        res[fk] = {'size_pt': s, 'pred_h': h, 'meas_h': mh, 'corr': round(c, 4)}
    best = max(res.items(), key=lambda kv: kv[1]['corr'])
    out[k] = {'meas_w': mw, 'meas_h': mh, 'cands': res, 'best': best[0]}
    print(f'{k:15s} meas {mw:.0f}x{mh:.0f}px  best={best[0]} size={best[1]["size_pt"]}predH={best[1]["pred_h"]} corr={best[1]["corr"]}')
    for fk, r in res.items():
        print(f'    {fk:12s} size={r["size_pt"]:6.2f} predH={r["pred_h"]:5.1f} corr={r["corr"]:.4f}')

with open('videos/deep-learning/001_introduction/recreated_pptx/qa/slide039/font_solve2_out.json', 'w') as f:
    json.dump(out, f, indent=1, default=str)
print('BANKED -> qa/slide039/font_solve2_out.json')
