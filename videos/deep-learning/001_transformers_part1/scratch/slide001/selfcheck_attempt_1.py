#!/usr/bin/env python3
"""Closed-loop self-check attempt 1: measure render_1.png (2001x1125 @150dpi) vs original targets.
Targets from the original frame (960x540 @72ppi); scale = 150.0375/72 = 2.08385.
"""
from PIL import Image
from collections import Counter

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide001/render_1.png"
im = Image.open(REN).convert("RGB")
W, H = im.size
px = im.load()
PPI = W / 13.33
SC = PPI / 72.0
print(f"render {W}x{H} ppi={PPI:.3f} scale={SC:.4f}")

def inch_x(p): return p / PPI
def inch_y(p): return p / (H / 7.5)

def classify(r, g, b):
    if r > 120 and g < 90 and b < 90 and (r - max(g, b)) > 60: return "red"
    if b > 100 and b - r > 60 and b - g > 40: return "blue"
    if r > 200 and g > 200 and b < 160 and (r - b) > 70: return "yellow"
    return None

# ---- house frame stroke positions
print("\n== frame strokes ==")
for y in (22, 23, 24, 1100, 1101):
    pass
col = [y for y in range(0, 60) if px[1000, y][0] > 120 and px[1000, y][1] < 90]
print(f"  top stroke rows at x=1000: {col[:6]} (expect ~22-24 = 0.15in)")
row = [x for x in range(0, 60) if px[x, 560][0] > 120 and px[x, 560][1] < 90]
print(f"  left stroke cols at y=560: {row[:6]}")

# ---- title lines (red)
print("\n== title ==")
def ink_rows(cls, x0, x1, y0, y1):
    rows = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if classify(*px[x, y]) == cls:
                rows.append(y); break
    return rows

def ink_cols(cls, y0, y1, x0, x1, gap=12):
    cols = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if classify(*px[x, y]) == cls)
        cols.append(n > 0)
    runs, run = [], None
    for i, v in enumerate(cols):
        if v:
            if run is None: run = [i + x0, i + x0]
            run[1] = i + x0
        elif run and (i + x0 - run[1]) > gap:
            runs.append(tuple(run)); run = None
    if run: runs.append(tuple(run))
    return runs

r1 = ink_rows("red", 400, 1600, 40, 450)
# split title L1/L2 by gaps
bands, cur = [], None
for y in r1:
    if cur is None: cur = [y, y]
    elif y - cur[1] <= 4: cur[1] = y
    else: bands.append(tuple(cur)); cur = [y, y]
if cur: bands.append(tuple(cur))
print(f"  red row bands 40-450: {bands}")
if len(bands) >= 2:
    L1, L2 = bands[0], bands[1]
    capL1 = (L1[1] - L1[0] + 1) / SC
    print(f"  L1 rows {L1} cap={(L1[1]-L1[0]+1)/SC:.1f}pt top={inch_y(L1[0]):.3f}in (target cap-top 0.43, cap ~41pt incl AA)")
    print(f"  L2 rows {L2} cap={(L2[1]-L2[0]+1)/SC:.1f}pt top={inch_y(L2[0]):.3f}in (target cap-top {0.28+0.189*57/72+67/72:.3f})")
    print(f"  pitch = {(L2[0]-L1[0])/SC:.1f}pt (target 67)")
    runs = ink_cols("red", L1[0], L1[1], 300, 1700)
    if runs:
        x0, x1 = runs[0][0], runs[-1][1]
        print(f"  L1 ink x {x0}-{x1} ({inch_x(x0):.3f}-{inch_x(x1):.3f}in) center {inch_x((x0+x1)/2):.3f} (orig 3.528-9.403 c6.465; house-centered target 6.665)")
        if len(runs) >= 2:
            print(f"  L1 word gap: {runs[1][0]-runs[0][1]}px ({(runs[1][0]-runs[0][1])/SC:.1f}pt; orig ~41pt)")
    runs2 = ink_cols("red", L2[0], L2[1], 300, 1700)
    if runs2:
        x0, x1 = runs2[0][0], runs2[-1][1]
        print(f"  L2 ink x {x0}-{x1} ({inch_x(x0):.3f}-{inch_x(x1):.3f}in) center {inch_x((x0+x1)/2):.3f} (orig 4.736-8.236 c6.486)")

# ---- credit block (find red 'Prepared By' + blue lines)
print("\n== credit block ==")
redb = [y for y in range(500, 760) if any(classify(*px[x, y]) == "red" for x in range(900, 1100))]
print(f"  'Prepared By' rows: {redb[:1]}..{redb[-1:] if redb else None} top={inch_y(redb[0]):.3f}in" if redb else "  none")
if redb:
    cols = ink_cols("red", redb[0], redb[-1], 800, 1250, gap=30)
    if cols:
        x0, x1 = cols[0][0], cols[-1][1]
        print(f"  ink x {x0}-{x1} center {inch_x((x0+x1)/2):.3f}in (orig center 7.158)")
blueb = []
for y in range(560, 800):
    if any(classify(*px[x, y]) == "blue" for x in range(700, 1500)):
        blueb.append(y)
if blueb:
    bands2, cur = [], None
    for y in blueb:
        if cur is None: cur = [y, y]
        elif y - cur[1] <= 4: cur[1] = y
        else: bands2.append(tuple(cur)); cur = [y, y]
    if cur: bands2.append(tuple(cur))
    for b in bands2:
        cols = ink_cols("blue", b[0], b[1], 600, 1600, gap=30)
        x0, x1 = (cols[0][0], cols[-1][1]) if cols else (0, 0)
        print(f"  blue band rows {b} top={inch_y(b[0]):.3f}in x {inch_x(x0):.3f}-{inch_x(x1):.3f} c={inch_x((x0+x1)/2):.3f}")

# ---- instructors block
print("\n== instructors block ==")
redb = [y for y in range(1050, 1200) if False]
redh = [y for y in range(1000, 1200) if any(classify(*px[x, y]) == "red" for x in range(100, 500))]
print(f"  'Instructors:' rows {redh[0]}-{redh[-1]} top={inch_y(redh[0]):.3f}in (target cap-top 5.708)" if redh else "  heading none")
if redh:
    cols = ink_cols("red", redh[0], redh[-1], 60, 600, gap=30)
    if cols: print(f"  ink left {inch_x(cols[0][0]):.3f}in (target 0.778)")
blueb = [y for y in range(1150, H - 30) if any(classify(*px[x, y]) == "blue" for x in range(150, 800))]
bands3, cur = [], None
for y in blueb:
    if cur is None: cur = [y, y]
    elif y - cur[1] <= 4: cur[1] = y
    else: bands3.append(tuple(cur)); cur = [y, y]
if cur: bands3.append(tuple(cur))
targets = [6.083, 6.431, 6.722, 7.042]
for i, b in enumerate(bands3[:5]):
    cols = ink_cols("blue", b[0], b[1], 100, 900, gap=30)
    x0, x1 = (cols[0][0], cols[-1][1]) if cols else (0, 0)
    t = targets[i] if i < len(targets) else None
    print(f"  item{i+1} rows {b} top={inch_y(b[0]):.3f}in (target {t}) ink left {inch_x(x0):.3f} (target 1.333) right {inch_x(x1):.3f}")

# ---- logo
print("\n== logo ==")
def is_canvas(r, g, b): return 218 <= r <= 242 and 220 <= g <= 244 and 217 <= b <= 242
xs, ys = [], []
for y in range(1250, 1540):
    for x in range(1650, 1930):
        if not is_canvas(*px[x, y]):
            xs.append(x); ys.append(y)
if xs:
    print(f"  ink bbox x {inch_x(min(xs)):.3f}-{inch_x(max(xs)):.3f}in y {inch_y(min(ys)):.3f}-{inch_y(max(ys)):.3f}in (target x 8.25-12.583, y 6.401-7.220)")
    print(f"  bottom gap to house frame inner edge 7.34: {7.34 - inch_y(max(ys)):.3f}in")

# ---- crosshair
print("\n== crosshair ==")
xs, ys = [], []
for y in range(500, 650):
    for x in range(400, 560):
        r, g, b = px[x, y]
        if (232 - r) > 15 and (232 - g) > 15 and (232 - b) > 15:
            xs.append(x); ys.append(y)
if xs:
    print(f"  bbox x {inch_x(min(xs)):.3f}-{inch_x(max(xs)):.3f} y {inch_y(min(ys)):.3f}-{inch_y(max(ys)):.3f} (target 2.403-2.542 / 2.750-2.903)")
else:
    print("  NOT FOUND")

# ---- badge
print("\n== badge ==")
ysel = [y for y in range(30, 150) if any(classify(*px[x, y]) == "yellow" for x in range(1850, 1990))]
if ysel:
    cols = [x for x in range(1850, 1990) if any(classify(*px[x, y]) == "yellow" for y in range(30, 150))]
    print(f"  yellow oval rows {ysel[0]}-{ysel[-1]} cols {cols[0]}-{cols[-1]} (expect x 12.48-12.98in=1872.5-1947.6px, y 0.30-0.80in=45-120px)")
    dark = [(x, y) for y in range(ysel[0], ysel[-1]) for x in range(cols[0], cols[-1]) if sum(px[x, y]) < 330]
    if dark:
        dxs = [d[0] for d in dark]; dys = [d[1] for d in dark]
        print(f"  numeral ink bbox x {min(dxs)}-{max(dxs)} y {min(dys)}-{max(dys)}")

# ---- colors
print("\n== color samples ==")
def mode_region(x0, x1, y0, y1, pred, label):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            if pred(*p): c[p] += 1
    print(f"  {label}: {c.most_common(2)}")
mode_region(400, 1600, 80, 200, lambda r, g, b: r > 140 and g < 60, "title red core")
mode_region(700, 1500, 560, 700, lambda r, g, b: b > 100 and b - r > 60, "credit name blue core")
print(f"  canvas: {px[1000, 900]}, outside-frame corner: {px[5,5]}")
