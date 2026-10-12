# Forensics pass 4: x-extents, borders, equation bbox (loose red), slab probes.
from PIL import Image
import json
from collections import Counter

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
im = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
im36 = Image.open(f'{BASE}/unique_slides/slide_036.jpg').convert('RGB')
W, H = im.size
px = im.load()
px36 = im36.load()
out = {}

# 1) title red cols y78..115
tcols = {}
for x in range(45, 916):
    cnt = sum(1 for y in range(76, 116) if (lambda p: p[0] > 120 and p[1] < 110 and p[2] < 110 and p[0] > p[1] + 40)(px[x, y]))
    if cnt > 1: tcols[x] = cnt
xs = sorted(tcols)
out['title_cols'] = dict(x0=xs[0], x1=xs[-1], n=len(xs))

# 2) white panel border cols (loose red r>110,g<90,b<100) over y270..505
pcols = {}
for x in range(45, 916):
    cnt = sum(1 for y in range(270, 505) if (lambda p: p[0] > 110 and p[1] < 90 and p[2] < 100)(px[x, y]))
    if cnt > 60: pcols[x] = cnt
out['panel_border_cols'] = pcols
# top/bottom border rows refined
prows = {}
for y in range(255, 270):
    cnt = sum(1 for x in range(60, 900) if (lambda p: p[0] > 110 and p[1] < 90 and p[2] < 100)(px[x, y]))
    prows[y] = cnt
out['panel_top_rows'] = prows
prows2 = {}
for y in range(505, 520):
    cnt = sum(1 for x in range(60, 900) if (lambda p: p[0] > 110 and p[1] < 90 and p[2] < 100)(px[x, y]))
    prows2[y] = cnt
out['panel_bottom_rows'] = prows2

# 3) black band x-extents
def black_cols(y0, y1, thr=240):
    d = {}
    for x in range(45, 916):
        cnt = sum(1 for y in range(y0, y1+1) if sum(px[x, y]) < thr)
        if cnt > 0: d[x] = cnt
    return d
out['band269_281'] = {k: v for k, v in black_cols(269, 281).items()}
out['band453_479'] = dict(list(black_cols(453, 479).items())[::2])
out['band480_496_black'] = dict(list(black_cols(480, 496).items())[::2])
out['band412'] = black_cols(410, 414)
out['band442_445'] = black_cols(441, 446)
out['band391_398'] = dict(list(black_cols(391, 398).items())[::2])

# 4) equation: loose red (r>110, g<95, b<95, r>g+50) rows+cols in y470..515
erows = {}
for y in range(470, 516):
    cnt = sum(1 for x in range(45, 916) if (lambda p: p[0] > 110 and p[1] < 95 and p[2] < 95 and p[0] > p[1] + 50)(px[x, y]))
    if cnt > 2: erows[y] = cnt
out['eq_loose_rows'] = erows
ecols = {}
for x in range(45, 916):
    cnt = sum(1 for y in range(470, 516) if (lambda p: p[0] > 110 and p[1] < 95 and p[2] < 95 and p[0] > p[1] + 50)(px[x, y]))
    if cnt > 1: ecols[x] = cnt
xs = sorted(ecols)
out['eq_loose_cols'] = dict(x0=xs[0] if xs else None, x1=xs[-1] if xs else None, detail=dict(list(ecols.items())[:80]))

# 5) tan strips at x59 / x895: probe + compare 36
out['x59_probe'] = {y: [list(px[59, y]), list(px36[59, y])] for y in [150, 200, 250, 300, 350, 400, 450, 500]}
out['x895_probe'] = {y: [list(px[895, y]), list(px36[895, y])] for y in [150, 200, 250, 300, 350, 400, 450, 500]}

# 6) slab area modal colors: grid x150..330, y280..445 (10px cells)
def modal(x0, y0, x1, y1):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[px[x, y]] += 1
    return c.most_common(4)
slab_grid = {}
for gy in range(280, 450, 20):
    row = {}
    for gx in range(150, 340, 20):
        row[gx] = modal(gx, gy, gx+20, gy+20)[0]
    slab_grid[gy] = row
out['slab_modal_grid'] = {str(k): {str(kk): list(vv) for kk, vv in v.items()} for k, v in slab_grid.items()}

# slab edges: 8B4513-ish dark brown (110<r<165, 40<g<95, b<45)
scols = {}
for x in range(140, 340):
    cnt = sum(1 for y in range(280, 450) if (lambda p: 110 < p[0] < 175 and 40 < p[1] < 100 and p[2] < 55)(px[x, y]))
    if cnt > 4: scols[x] = cnt
out['slab_dark_cols'] = scols
srows = {}
for y in range(280, 450):
    cnt = sum(1 for x in range(140, 340) if (lambda p: 110 < p[0] < 175 and 40 < p[1] < 100 and p[2] < 55)(px[x, y]))
    if cnt > 4: srows[y] = cnt
out['slab_dark_rows'] = srows

# 7) '=' probe: x470..540, y320..380 — look for cyan 3EAEC6 or dark ink
out['eq_sign_probe'] = {}
for y in range(325, 380, 5):
    row = []
    for x in range(470, 545, 5):
        row.append((x, list(px[x, y])))
    out['eq_sign_probe'][y] = row

# 8) yellow box edges: probe rows 136..140 and 241..247 at x480; cols 63..68 and 900..906 at y190
out['yellowbox_edges'] = {
    'top_rows_x480': {y: list(px[480, y]) for y in range(134, 142)},
    'bot_rows_x480': {y: list(px[480, y]) for y in range(240, 248)},
    'left_cols_y190': {x: list(px[x, 190]) for x in range(60, 70)},
    'right_cols_y190': {x: list(px[x, 190]) for x in range(898, 908)},
}

print(json.dumps(out, indent=0, default=str))
