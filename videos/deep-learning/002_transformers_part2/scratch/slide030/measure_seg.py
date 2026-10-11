#!/usr/bin/env python3
"""Slide 030: segment-level measurement per line band + highlight pills + bracket stems."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
mx = np.maximum(np.maximum(R, G), B); mn = np.minimum(np.minimum(R, G), B)
BLACK = (mx < 110)
RED = (R > 120) & (R - G > 55) & (R - B > 45)
BLUE = (B > 100) & (B - R > 40) & (B - G > 30)
YEL = (R > 200) & (G > 180) & (B < 130)
GRN = (G > 140) & (G - R > 25) & (G - B > 30)

def segs(name, y0, y1, x0, x1, gap=4, masks=None):
    print(f"-- {name} band y{y0}..{y1} x{x0}..{x1}")
    ink = np.zeros((y1 - y0 + 1, x1 - x0 + 1), bool)
    for m in (masks or [BLACK, RED, BLUE]): ink |= m[y0:y1 + 1, x0:x1 + 1]
    cp = ink.sum(axis=0)
    out = []
    x = 0
    while x < len(cp):
        if cp[x] > 0:
            x2 = x; blank = 0
            while x2 < len(cp) - 1:
                if cp[x2 + 1] > 0: x2 += 1; blank = 0
                else:
                    blank += 1
                    if blank >= gap: break
                    x2 += 1
            if x2 - x >= 1:
                ys = np.where(ink[:, x:x2 + 1].any(axis=1))[0]
                kinds = {}
                for mname, m in (("black", BLACK), ("red", RED), ("blue", BLUE), ("YEL", YEL), ("GRN", GRN)):
                    n = int(m[y0:y1 + 1, x0 + x:x0 + x2 + 1].sum())
                    if n > 8: kinds[mname] = n
                # yellow/green pill bbox overlapping this segment
                def pillbbox(m):
                    p = m[y0:y1 + 1, x0 + x:x0 + x2 + 1]
                    if p.sum() < 30: return None
                    ys, xs = np.where(p)
                    return (x0 + x + int(xs.min()), y0 + int(ys.min()), x0 + x + int(xs.max()), y0 + int(ys.max()))
                out.append((x0 + x, x0 + x2, y0 + int(ys[0]), y0 + int(ys[-1]), kinds, pillbbox(YEL), pillbbox(GRN)))
            x = x2 + 1
        else: x += 1
    for s in out:
        print(f"   x{s[0]:3d}..{s[1]:3d} y{s[2]}..{s[3]} {s[4]} YEL={s[5]} GRN={s[6]}")
    return out

# VECTOR BOX rows: label cols vs vector cols
segs("vecbox band1 (label+vec1)", 58, 140, 92, 371)
segs("vecbox band2 (label2+vec2)", 145, 231, 92, 371)
# REMEMBER lines
segs("remember L1", 108, 130, 504, 845)
segs("remember L2", 143, 163, 504, 845)
segs("remember L3", 163, 182, 504, 845)
# DERIVATION lines
segs("deriv L1", 246, 280, 91, 659)
segs("deriv L2", 284, 322, 91, 659)
# MATRIX BOX: full equation band + captions/brace band + blue label
segs("matrix eq band", 345, 438, 90, 614)
segs("matrix captions/brace", 438, 478, 90, 614)
segs("blue label", 478, 497, 90, 614)
# GREEN NOTE lines
segs("note L1", 358, 378, 622, 868)
segs("note L2", 388, 407, 622, 868)
segs("note L3", 407, 430, 622, 868)
segs("note L4", 430, 452, 622, 868)
