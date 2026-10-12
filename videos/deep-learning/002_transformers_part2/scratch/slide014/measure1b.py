#!/usr/bin/env python3
# measure1b.py — refined title/subtitle bands, right-border fade, badge numeral, top rule
import os
os.environ.setdefault("TMPDIR", os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import numpy as np

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2'
a = np.asarray(Image.open(BASE + '/unique_slides/slide_014.jpg').convert('RGB')).astype(int)
H, W = a.shape[:2]

def spans(cols, off=0):
    out, s = [], None
    for i, v in enumerate(cols):
        if v and s is None: s = i
        if not v and s is not None: out.append((off + s, off + i - 1)); s = None
    if s is not None: out.append((off + s, off + len(cols) - 1))
    return out

def col_spans(y0, y1, x0, x1, thr=200, sat=60):
    sub = a[y0:y1, x0:x1]
    m = (sub.max(axis=2) - sub.min(axis=2) > sat) | (sub.max(axis=2) < thr - 60)
    return spans(m.any(axis=0), x0)

def row_spans(x0, x1, y0, y1, thr=200, sat=60):
    sub = a[y0:y1, x0:x1]
    m = (sub.max(axis=2) - sub.min(axis=2) > sat) | (sub.max(axis=2) < thr - 60)
    return spans(m.any(axis=1), y0)

def med_mask(y0, y1, x0, x1, pred):
    pts = [a[y, x] for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if pred(a[y, x])]
    if not pts: return None, 0
    return tuple(int(v) for v in np.median(np.array(pts), axis=0)), len(pts)

print("--- right border fade scan (fy=300, fx 890..940, red-dominant>40) ---")
for x in range(890, 941):
    r, g, b = a[300, x]
    if r - max(g, b) > 25: print(f"  fx {x}: {tuple(int(v) for v in a[300, x])}")

print("\n--- top rule scan (fx=460, fy 0..50) any non-white ---")
for y in range(0, 50):
    r, g, b = a[y, 460]
    if not (r > 245 and g > 245 and b > 245): print(f"  fy {y}: {tuple(int(v) for v in a[y, 460])}")

print("\n--- TITLE text proper (fx 150..830, fy 45..80) ---")
trs = row_spans(150, 830, 45, 80)
print("rows:", trs)
tsp = col_spans(48, 74, 150, 830)
print("col spans:", tsp)
if tsp:
    print(f"title ink fx {tsp[0][0]}..{tsp[-1][1]}  cx {(tsp[0][0]+tsp[-1][1])/2}")
    m, n = med_mask(48, 74, tsp[0][0], tsp[-1][1], lambda p: p[0] > 130 and p[0] - max(p[1], p[2]) > 70)
    print("red core:", m, "n=", n)
    # cap-height rows within the main span
    rs = row_spans(tsp[0][0], tsp[-1][1], 45, 80)
    print("title glyph rows:", rs)

print("\n--- SUBTITLE proper (fx 115..905, fy 78..100) ---")
srs = row_spans(115, 905, 76, 102)
print("rows:", srs)
ssp = col_spans(80, 96, 115, 905)
print(f"subtitle ink fx {ssp[0][0]}..{ssp[-1][1]} nspans={len(ssp)}")
m, n = med_mask(80, 96, ssp[0][0], ssp[-1][1], lambda p: p[2] > 130 and p[2] - p[0] > 50)
print("blue core:", m, "n=", n)
mg, ng = med_mask(80, 96, ssp[0][0], ssp[-1][1], lambda p: p[1] > 110 and p[1] - p[0] > 40 and p[1] - p[2] > 40)
print("green core:", mg, "n=", ng)
mr, nr = med_mask(80, 96, ssp[0][0], ssp[-1][1], lambda p: p[0] > 130 and p[0] - max(p[1], p[2]) > 70)
print("red core (ALL Words):", mr, "n=", nr)

print("\n--- badge numeral tight scan (fx 862..891, fy 58..84, inside ring) ---")
# dark pixels well inside the yellow disc
pts = [(x, y) for y in range(60, 83) for x in range(864, 889) if sum(a[y, x]) < 400]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"numeral ink bbox fx {min(xs)}..{max(xs)} fy {min(ys)}..{max(ys)} n={len(pts)}")
    dark = np.array([a[y, x] for y in range(min(ys), max(ys) + 1) for x in range(min(xs), max(xs) + 1) if sum(a[y, x]) < 330])
    print("darkest median:", tuple(int(v) for v in np.median(dark, axis=0)) if len(dark) else None, "n=", len(dark))
    # reddish numeral?
    reds = np.array([a[y, x] for y in range(min(ys), max(ys) + 1) for x in range(min(xs), max(xs) + 1) if a[y, x][0] > 90 and a[y, x][0] - max(a[y, x][1], a[y, x][2]) > 40])
    print("reddish count:", len(reds), "median:", tuple(int(v) for v in np.median(reds, axis=0)) if len(reds) else None)

print("\n--- FLOATING X5 BOX (subtitle top-left overlap; fx 60..115, fy 60..110) ---")
# white box: find white-ish region over gray panel / subtitle
ws = [(x, y) for y in range(58, 112) for x in range(60, 118) if all(v > 246 for v in a[y, x])]
if ws:
    xs = [p[0] for p in ws]; ys = [p[1] for p in ws]
    print(f"white-ish blob fx {min(xs)}..{max(xs)} fy {min(ys)}..{max(ys)} n={len(ws)}")
xsp = col_spans(60, 110, 58, 120)
print("ink col spans in region:", xsp)
rsp = row_spans(58, 120, 58, 112)
print("ink row spans in region:", rsp)
