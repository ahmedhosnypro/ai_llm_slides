# Forensics pass 3: calibrated color probes + per-row/col profiles.
from PIL import Image
import json

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
im = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
W, H = im.size
px = im.load()
out = {}

# A) raw pixel probes: border row 262, presumed border cols, bottom rows
out['probe_row262'] = {x: px[x, 262] for x in [44, 45, 46, 100, 480, 900, 914, 915, 916]}
out['probe_row263'] = {x: px[x, 263] for x in [44, 45, 100, 480, 914, 915]}
out['probe_col_scan_y300'] = {x: px[x, 300] for x in [41, 42, 43, 44, 45, 46, 47]}
out['probe_col_scan_y400'] = {x: px[x, 400] for x in [41, 42, 43, 44, 45, 46, 47]}
out['probe_bottom'] = {y: px[480, y] for y in [508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520]}
out['probe_col915'] = {y: px[915, y] for y in [300, 350, 400, 450, 500]}
out['probe_col914'] = {y: px[914, y] for y in [300, 350, 400, 450, 500]}

# B) title red-ink per-row counts y50..140
rows = {}
for y in range(50, 141):
    cnt = sum(1 for x in range(45, 916) if (lambda p: p[0] > 120 and p[1] < 110 and p[2] < 110 and p[0] > p[1] + 40)(px[x, y]))
    if cnt > 2: rows[y] = cnt
out['title_red_rows'] = rows

# C) orange slab D2691E-ish: r 150-235, g 60-160, b<80 per-row + per-col
orows = {}
for y in range(120, 520):
    cnt = sum(1 for x in range(45, 916) if (lambda p: 150 < p[0] < 240 and 60 < p[1] < 160 and p[2] < 80)(px[x, y]))
    if cnt > 3: orows[y] = cnt
out['orange_rows'] = orows
ocols = {}
for x in range(45, 700):
    cnt = sum(1 for y in range(120, 520) if (lambda p: 150 < p[0] < 240 and 60 < p[1] < 160 and p[2] < 80)(px[x, y]))
    if cnt > 3: ocols[x] = cnt
out['orange_cols'] = dict(list(ocols.items()))

# D) tan cube E8C890-ish: per-row/col
def tanf(p): return 195 < p[0] < 250 and 160 < p[1] < 225 and 110 < p[2] < 185
trows = {}
for y in range(120, 520):
    cnt = sum(1 for x in range(45, 916) if tanf(px[x, y]))
    if cnt > 5: trows[y] = cnt
out['tan_rows'] = trows
tcols = {}
for x in range(45, 916):
    cnt = sum(1 for y in range(120, 520) if tanf(px[x, y]))
    if cnt > 5: tcols[x] = cnt
out['tan_cols'] = dict(list(tcols.items()))

# E) black ink rows in panel y264..515 (x45..915), excluding border cols
brows = {}
for y in range(264, 516):
    cnt = sum(1 for x in range(60, 900, 2) if sum(px[x, y]) < 240)
    if cnt > 2: brows[y] = cnt
# group into bands
bands = []
prev = None
for y in sorted(brows):
    if prev is not None and y - prev <= 4: bands[-1][1] = y
    else: bands.append([y, y])
    prev = y
out['black_bands_panel'] = bands
out['black_rows_panel'] = brows

# F) red equation ink: E02020-ish (r>170, g<70, b<70) rows y430..516
erows = {}
for y in range(430, 516):
    cnt = sum(1 for x in range(45, 916) if (lambda p: p[0] > 170 and p[1] < 75 and p[2] < 75)(px[x, y]))
    if cnt > 2: erows[y] = cnt
out['eq_red_rows'] = erows
ecols = {}
for x in range(45, 916):
    cnt = sum(1 for y in range(430, 516) if (lambda p: p[0] > 170 and p[1] < 75 and p[2] < 75)(px[x, y]))
    if cnt > 1: ecols[x] = cnt
out['eq_red_cols'] = dict(list(ecols.items()))

print(json.dumps(out, indent=0))
