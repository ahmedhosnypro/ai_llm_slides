# Forensics pass 1 for slide 037: overall layout bands + slab identity vs slide 036.
from PIL import Image
import json

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
im = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
im36 = Image.open(f'{BASE}/unique_slides/slide_036.jpg').convert('RGB')
W, H = im.size
px = im.load()
px36 = im36.load()

out = {}

def classify(r, g, b):
    # coarse classifiers tuned to this deck
    if r > 235 and g > 235 and b > 235: return 'white'
    if abs(r-g) < 12 and abs(g-b) < 12 and 200 <= r <= 240: return 'gray'
    if r > 240 and g > 240 and 200 < b < 245: return 'yellowish'  # FFFFE1 = 255,255,225
    if r > 140 and g < 90 and b < 90: return 'red'
    if r < 60 and g < 60 and b < 60: return 'black'
    return 'other'

# 1) vertical band profile: modal class per row (sampled every 2px), x 45..915 (inside chrome)
def row_profile(y):
    from collections import Counter
    c = Counter()
    for x in range(45, 915, 3):
        c[classify(*px[x, y])] += 1
    return c.most_common(3)

bands = []
prev = None
for y in range(0, H, 2):
    top = row_profile(y)[0][0]
    if top != prev:
        bands.append((y, top))
        prev = top
out['band_transitions'] = bands

# 2) pale-yellow box bbox: FFFFE1-ish (r>245,g>245,200<b<240)
ys = []; xs = []
for y in range(0, H, 2):
    for x in range(0, W, 2):
        r, g, b = px[x, y]
        if r > 245 and g > 245 and 205 < b < 240:
            ys.append(y); xs.append(x)
if xs:
    out['yellow_box'] = dict(x0=min(xs), x1=max(xs), y0=min(ys), y1=max(ys))

# 3) red border rectangles: strong red rows/cols (r>150, g<70, b<70)
redrows = []
for y in range(0, H):
    cnt = 0
    for x in range(45, 915, 2):
        r, g, b = px[x, y]
        if r > 150 and g < 80 and b < 80: cnt += 1
    if cnt > 200: redrows.append((y, cnt))
out['red_rows_long'] = redrows
redcols = []
for x in range(45, 915):
    cnt = 0
    for y in range(0, H, 2):
        r, g, b = px[x, y]
        if r > 150 and g < 80 and b < 80: cnt += 1
    if cnt > 60: redcols.append((x, cnt))
out['red_cols_long'] = redcols

# 4) slab identity check: compare the parent's tiles between frames
def region_diff(x0, y0, w, h):
    d = 0; tot = 0; mx = 0
    for y in range(y0, y0+h):
        for x in range(x0, x0+w):
            a = px[x, y]; b = px36[x, y]
            dd = abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])
            tot += 1
            if dd > 60: d += 1
            mx = max(mx, dd)
    return dict(diff_px=d, total=tot, frac=round(d/tot, 4), maxchan=mx)

out['tileA_158_160_245x61_vs36'] = region_diff(158, 160, 245, 61)
out['tileB_158_219_223x176_vs36'] = region_diff(158, 219, 223, 176)
# where IS the slab in 37? scan for orange pixels D2691E-ish (r>150, 60<g<140, b<60)
ox = []; oy = []
for y in range(0, H, 1):
    for x in range(0, W, 1):
        r, g, b = px[x, y]
        if r > 150 and 60 < g < 150 and b < 70:
            ox.append(x); oy.append(y)
if ox:
    out['orange_bbox'] = dict(x0=min(ox), x1=max(ox), y0=min(oy), y1=max(oy), n=len(ox))

# 5) colored filter blobs census (downsampled grid, modal color per 20px cell, x>300)
colors = {
 'cyan': (lambda r,g,b: b>150 and 130<g<210 and r<110),
 'green': (lambda r,g,b: g>140 and r<110 and b<110),
 'red_bright': (lambda r,g,b: r>180 and g<70 and b<70),
 'yellow_sat': (lambda r,g,b: r>200 and g>190 and b<90),
 'purple': (lambda r,g,b: r>90 and r<170 and b>150 and g<100),
 'tan': (lambda r,g,b: 190<r<245 and 150<g<215 and 100<b<175),
}
blob = {}
for name, fn in colors.items():
    pts = []
    for y in range(0, H, 2):
        for x in range(0, W, 2):
            r, g, b = px[x, y]
            if fn(r, g, b): pts.append((x, y))
    if pts:
        xs2 = [p[0] for p in pts]; ys2 = [p[1] for p in pts]
        blob[name] = dict(x0=min(xs2), x1=max(xs2), y0=min(ys2), y1=max(ys2), n=len(pts))
out['color_blobs'] = blob

print(json.dumps(out, indent=1))
