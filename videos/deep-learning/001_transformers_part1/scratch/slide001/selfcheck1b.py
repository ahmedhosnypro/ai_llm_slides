#!/usr/bin/env python3
"""Self-check attempt 1, pass B: corrected pixel windows (render 2001x1125 @150.1ppi)."""
from PIL import Image
from collections import Counter

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide001/render_1.png"
im = Image.open(REN).convert("RGB")
W, H = im.size
px = im.load()
PPI = W / 13.33
PPY = H / 7.5

def ix(p): return p / PPI
def iy(p): return p / PPY

def classify(r, g, b):
    if r > 120 and g < 90 and b < 90 and (r - max(g, b)) > 60: return "red"
    if b > 100 and b - r > 60 and b - g > 40: return "blue"
    if r > 200 and g > 200 and b < 160 and (r - b) > 70: return "yellow"
    return None

def bands_of(cls, y0, y1, x0, x1, gap_px=6):
    rows = [y for y in range(y0, min(y1, H)) if any(classify(*px[x, y]) == cls for x in range(x0, x1))]
    out, cur = [], None
    for y in rows:
        if cur is None: cur = [y, y]
        elif y - cur[1] <= gap_px: cur[1] = y
        else: out.append(tuple(cur)); cur = [y, y]
    if cur: out.append(tuple(cur))
    return out

def xext(cls, y0, y1, x0, x1, gap=30):
    cols = [x for x in range(x0, min(x1, W)) if any(classify(*px[x, y]) == cls for y in range(y0, y1 + 1))]
    if not cols: return None
    runs, run = [], None
    for x in cols:
        if run is None: run = [x, x]
        elif x - run[1] <= gap: run[1] = x
        else: runs.append(tuple(run)); run = [x, x]
    if run: runs.append(tuple(run))
    return runs

print("== credit block (rows 380-620) ==")
for b in bands_of("red", 380, 620, 800, 1300):
    r = xext("red", b[0], b[1], 800, 1300)
    if r: print(f"  red band {b} top={iy(b[0]):.3f}in x {ix(r[0][0]):.3f}-{ix(r[-1][1]):.3f} c={ix((r[0][0]+r[-1][1])/2):.3f} (targets: cap-top 2.721, c 7.158)")
for b in bands_of("blue", 380, 620, 600, 1600):
    r = xext("blue", b[0], b[1], 600, 1600)
    if r: print(f"  blue band {b} top={iy(b[0]):.3f}in x {ix(r[0][0]):.3f}-{ix(r[-1][1]):.3f} c={ix((r[0][0]+r[-1][1])/2):.3f} (targets: name cap 3.055 c~7.16 / email 3.416 c~7.16)")

print("== instructors block (rows 800-1120) ==")
for b in bands_of("red", 800, 900, 80, 500):
    r = xext("red", b[0], b[1], 80, 500)
    if r: print(f"  heading rows {b} top={iy(b[0]):.3f}in left={ix(r[0][0]):.3f} (targets: cap 5.708, left 0.778)")
tg = [6.083, 6.431, 6.722, 7.042]
for i, b in enumerate(bands_of("blue", 890, 1115, 100, 900)):
    r = xext("blue", b[0], b[1], 100, 900)
    t = tg[i] if i < len(tg) else None
    if r: print(f"  item{i+1} rows {b} top={iy(b[0]):.3f}in (target {t}) left={ix(r[0][0]):.3f} (t 1.333) right={ix(r[-1][1]):.3f}")

print("== logo (rows 930-1110, x 1200-1930) ==")
def is_canvas(r, g, b): return 218 <= r <= 242 and 220 <= g <= 244 and 217 <= b <= 242
xs, ys = [], []
for y in range(930, min(1110, H)):
    for x in range(1200, min(1930, W)):
        if not is_canvas(*px[x, y]):
            xs.append(x); ys.append(y)
if xs:
    print(f"  ink x {ix(min(xs)):.3f}-{ix(max(xs)):.3f}in (target 8.250-12.583) y {iy(min(ys)):.3f}-{iy(max(ys)):.3f}in (target 6.401-7.220)")
    print(f"  gap to frame inner bottom 7.34: {7.34-iy(max(ys)):.3f}in ; gap right to 13.18: {13.18-ix(max(xs)):.3f}in")

print("== crosshair (rows 380-470, x 280-470) ==")
xs, ys = [], []
for y in range(380, 470):
    for x in range(280, 470):
        r, g, b = px[x, y]
        if (232 - r) > 15 and (232 - g) > 15 and (232 - b) > 15:
            xs.append(x); ys.append(y)
if xs:
    print(f"  bbox x {ix(min(xs)):.3f}-{ix(max(xs)):.3f}in (target 2.403-2.542) y {iy(min(ys)):.3f}-{iy(max(ys)):.3f}in (target 2.750-2.903)")
else:
    print("  NOT FOUND in window")

print("== badge ==")
yb = [y for y in range(30, 160) if any(classify(*px[x, y]) == "yellow" for x in range(1840, 1990))]
if yb:
    xb = [x for x in range(1840, 1990) if any(classify(*px[x, y]) == "yellow" for y in range(30, 160))]
    print(f"  oval rows {yb[0]}-{yb[-1]} ({iy(yb[0]):.3f}-{iy(yb[-1]):.3f}in; target 0.30-0.80) cols {xb[0]}-{xb[-1]} ({ix(xb[0]):.3f}-{ix(xb[-1]):.3f}in; target 12.48-12.98)")
    dark = [(x, y) for y in range(yb[0], yb[-1]) for x in range(xb[0], xb[-1]) if sum(px[x, y]) < 340]
    if dark:
        dx = [d[0] for d in dark]; dy = [d[1] for d in dark]
        print(f"  numeral ink x {min(dx)}-{max(dx)} y {min(dy)}-{max(dy)} (center {ix((min(dx)+max(dx))/2):.3f},{iy((min(dy)+max(dy))/2):.3f})")

print("== colors ==")
c = Counter()
for y in range(80, 200):
    for x in range(600, 1400):
        r, g, b = px[x, y]
        if r > 140 and g < 60: c[(r, g, b)] += 1
print("  title red core:", c.most_common(2))
c = Counter()
for y in range(440, 520):
    for x in range(700, 1500):
        r, g, b = px[x, y]
        if b > 100 and b - r > 60 and b - g > 40: c[(r, g, b)] += 1
print("  credit name blue core:", c.most_common(2))
print("  canvas:", px[1000, 700], " corner-outside-frame:", px[5, 5])

print("== containment (ink outside house frame inner edges 0.16..13.17 / 0.16..7.34in) ==")
bad = 0
for y in range(26, H - 26):
    for x in range(26, W - 26):
        r, g, b = px[x, y]
        if abs(r - 232) < 6 and abs(g - 232) < 6 and abs(b - 232) < 6:
            continue
        # outside frame strokes region? ink beyond inner edges
        if (x < 26 or x > W - 26 or y < 26 or y > H - 26):
            pass
# simpler: scan the 4 border strips between slide edge and frame stroke (0..20px, W-20..W, etc.)
def strip_ink(x0, x1, y0, y1):
    n = 0
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            r, g, b = px[x, y]
            if not (abs(r - 254) < 8 and abs(g - 255) < 8 and abs(b - 253) < 8):
                n += 1
    return n
print(f"  outer-strip non-white pixels: top={strip_ink(0, W, 0, 20)} bottom={strip_ink(0, W, H-20, H)} left={strip_ink(0, 20, 0, H)} right={strip_ink(W-20, W, 0, H)} (expect 0; strips are house-bg gray, counted if not white — see note)")
