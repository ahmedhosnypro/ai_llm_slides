# Forensics pass 2 for slide 037: fine bboxes + slab template matching.
from PIL import Image
import json

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
im = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
im36 = Image.open(f'{BASE}/unique_slides/slide_036.jpg').convert('RGB')
W, H = im.size
px = im.load()
px36 = im36.load()
out = {}

# A) title ink bbox: reddish/dark ink in y70..135 (non-gray, non-white)
xs, ys = [], []
for y in range(60, 136):
    for x in range(45, 916):
        r, g, b = px[x, y]
        if not (abs(r-g) < 25 and abs(g-b) < 25 and r > 170):  # not gray/white
            if r > g + 40 and r > b + 40:  # reddish
                xs.append(x); ys.append(y)
out['title_ink'] = dict(x0=min(xs), x1=max(xs), y0=min(ys), y1=max(ys), n=len(xs)) if xs else None

# B) yellow box: per-row yellowish count; per-col yellowish count
rows = []
for y in range(120, 270):
    cnt = sum(1 for x in range(45, 916, 2)
              if (lambda p: p[0] > 245 and p[1] > 245 and 200 < p[2] < 242)(px[x, y]))
    rows.append((y, cnt))
yb = [y for y, c in rows if c > 100]
out['yellow_rows_span'] = (min(yb), max(yb)) if yb else None
cols = []
for x in range(45, 916):
    cnt = sum(1 for y in range(138, 246, 2)
              if (lambda p: p[0] > 245 and p[1] > 245 and 200 < p[2] < 242)(px[x, y]))
    cols.append((x, cnt))
xb = [x for x, c in cols if c > 20]
out['yellow_cols_span'] = (min(xb), max(xb)) if xb else None

# text lines inside yellow box: rows with dark ink
dark_rows = []
for y in range(130, 250):
    cnt = sum(1 for x in range(60, 900, 2) if sum(px[x, y]) < 260)
    if cnt > 3: dark_rows.append(y)
# group consecutive
groups = []
for y in dark_rows:
    if groups and y - groups[-1][1] <= 3: groups[-1][1] = y
    else: groups.append([y, y])
out['yellow_text_lines'] = groups

# C) panel border: strong-red rows around 255..275 and columns
def redrow(y):
    return sum(1 for x in range(45, 916) if (lambda p: p[0] > 150 and p[1] < 80 and p[2] < 80)(px[x, y]))
rr = {y: redrow(y) for y in range(250, 280)}
out['red_rows_250_280'] = {y: c for y, c in rr.items() if c > 50}
def redcol(x):
    return sum(1 for y in range(250, 519) if (lambda p: p[0] > 150 and p[1] < 80 and p[2] < 80)(px[x, y]))
rc = {x: redcol(x) for x in range(45, 916)}
out['red_cols_250_519'] = {x: c for x, c in rc.items() if c > 100}
# bottom border near 510..519
rr2 = {y: redrow(y) for y in range(505, 520)}
out['red_rows_505_520'] = {y: c for y, c in rr2.items() if c > 50}

# D) slab template match: slide36 tile A (158,160,245,61) and tile B (158,219,223,176)
#    search in slide37 for best offset by mean abs diff on a coarse grid then refine.
def match(tile_box, search_box, step=4):
    tx, ty, tw, th = tile_box
    sx0, sy0, sx1, sy1 = search_box
    best = None
    tile = im36.crop((tx, ty, tx+tw, ty+th))
    tp = tile.load()
    for oy in range(sy0, sy1, step):
        for ox in range(sx0, sx1, step):
            if oy+th > H or ox+tw > W: continue
            s = 0; n = 0
            for y in range(0, th, 6):
                for x in range(0, tw, 6):
                    a = tp[x, y]; b = px[ox+x, oy+y]
                    s += abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]); n += 1
            v = s / n
            if best is None or v < best[0]: best = (v, ox, oy)
    return best

bA = match((158, 160, 245, 61), (40, 120, 400, 360))
out['tileA_best'] = bA
bB = match((158, 219, 223, 176), (40, 140, 400, 380))
out['tileB_best'] = bB
# refine tileA at step 1 around best
if bA:
    v0, ox0, oy0 = bA
    best = None
    tile = im36.crop((158, 160, 158+245, 160+61)); tp = tile.load()
    for oy in range(oy0-5, oy0+6):
        for ox in range(ox0-5, ox0+6):
            if oy+61 > H or ox+245 > W: continue
            s = 0; n = 0
            for y in range(0, 61, 3):
                for x in range(0, 245, 3):
                    a = tp[x, y]; b = px[ox+x, oy+y]
                    s += abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2]); n += 1
            v = s/n
            if best is None or v < best[0]: best = (v, ox, oy)
    out['tileA_best_fine'] = best

print(json.dumps(out, indent=1))
