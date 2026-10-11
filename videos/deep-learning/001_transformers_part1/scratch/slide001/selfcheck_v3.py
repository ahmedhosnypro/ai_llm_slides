#!/usr/bin/env python3
"""Self-check v3 (playlist chrome + measured content): render_1.png vs original targets."""
from PIL import Image
from collections import Counter

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide001/render_1.png"
im = Image.open(REN).convert("RGB")
W, H = im.size
px = im.load()
PPI = W / 13.33
PPY = H / 7.5
ix = lambda p: p / PPI
iy = lambda p: p / PPY
K = PPI / 72.0  # render px per original px

def classify(r, g, b):
    if r > 120 and g < 90 and b < 90 and (r - max(g, b)) > 60: return "red"
    if b > 100 and b - r > 60 and b - g > 40: return "blue"
    if r > 240 and g > 235 and 170 < b < 225: return "badgefill"
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

def report(name, got, target, tol=0.028):
    d = got - target
    print(f"  {name}: {got:.3f}in (target {target:.3f}, d={d:+.3f}) {'OK' if abs(d) <= tol else '!!'}")

print("== title (target cap tops 1.903 / 2.833, ink centers 6.465/6.486, widths 424/252pt, pitch 67pt) ==")
tb = bands_of("red", 250, 560, 300, 1700)
if len(tb) >= 2:
    L1, L2 = tb[0], tb[1]
    r1 = xext("red", L1[0], L1[1], 200, 1800)
    r2 = xext("red", L2[0], L2[1], 200, 1800)
    report("L1 cap top", iy(L1[0]), 1.903)
    report("L2 cap top", iy(L2[0]), 2.833)
    print(f"  pitch {(L2[0]-L1[0])/K/72*72:.1f}pt = {(L2[0]-L1[0])/K:.1f} orig-px (target 67)")
    c1 = ix((r1[0][0] + r1[-1][1]) / 2); c2 = ix((r2[0][0] + r2[-1][1]) / 2)
    report("L1 ink center", c1, 6.465)
    report("L2 ink center", c2, 6.486)
    w1 = (r1[-1][1] - r1[0][0] + 1) / K
    w2 = (r2[-1][1] - r2[0][0] + 1) / K
    print(f"  L1 width {w1:.1f} orig-px (target 424), L2 width {w2:.1f} (target 252)")
    if len(r1) >= 2:
        gaps = [(r1[i+1][0] - r1[i][1]) for i in range(len(r1)-1)]
        print(f"  L1 word gap {max(gaps)/K:.1f} orig-px (target ~41), letter-runs={len(r1)}")

print("== credit block (cap tops 4.194/4.528/4.889, center 7.158, widths 112/287/220pt) ==")
for b in bands_of("red", 550, 720, 800, 1300):
    r = xext("red", b[0], b[1], 800, 1300)
    if r:
        report("PreparedBy cap top", iy(b[0]), 4.194)
        c = ix((r[0][0] + r[-1][1]) / 2)
        report("PreparedBy center", c, 7.158)
        print(f"  width {(r[-1][1]-r[0][0]+1)/K:.1f} orig-px (target 112)")
for i, b in enumerate(bands_of("blue", 560, 780, 600, 1600)):
    r = xext("blue", b[0], b[1], 600, 1600)
    if r:
        t = [4.528, 4.889][i] if i < 2 else None
        o = [287, 220][i] if i < 2 else None
        c = ix((r[0][0] + r[-1][1]) / 2)
        report(f"credit line{i+1} top", iy(b[0]), t)
        report(f"credit line{i+1} center", c, 7.158)
        print(f"  width {(r[-1][1]-r[0][0]+1)/K:.1f} orig-px (target {o})")

print("== instructors (cap tops 5.708/6.083/6.431/6.722/7.042, lefts 0.778/1.333) ==")
for b in bands_of("red", 800, 900, 80, 500):
    r = xext("red", b[0], b[1], 80, 500)
    if r:
        report("heading cap top", iy(b[0]), 5.708)
        report("heading left", ix(r[0][0]), 0.778)
tg = [6.083, 6.431, 6.722, 7.042]
ow = [262, 206, 225, 197]
for i, b in enumerate(bands_of("blue", 880, 1115, 100, 900)):
    r = xext("blue", b[0], b[1], 100, 900)
    if r and i < 4:
        report(f"item{i+1} top", iy(b[0]), tg[i])
        report(f"item{i+1} left", ix(r[0][0]), 1.333)
        print(f"  width {(r[-1][1]-r[0][0]+1)/K:.1f} orig-px (target {ow[i]})")

print("== logo (target x 8.25-12.583, y 6.5-7.306) ==")
def is_panel(r, g, b): return 222 <= r <= 240 and 222 <= g <= 240 and 220 <= b <= 238
xs, ys = [], []
for y in range(940, 1090):
    for x in range(1200, 1930):
        if not is_panel(*px[x, y]):
            xs.append(x); ys.append(y)
if xs:
    report("logo left", ix(min(xs)), 8.25)
    report("logo top", iy(min(ys)), 6.5)
    print(f"  right {ix(max(xs)):.3f} (t 12.583) bottom {iy(max(ys)):.3f} (t 7.306)")

print("== crosshair (target 2.403-2.542 / 2.750-2.903) ==")
xs, ys = [], []
for y in range(380, 470):
    for x in range(280, 470):
        r, g, b = px[x, y]
        if (233 - r) > 15 and (233 - g) > 15 and (231 - b) > 15:
            xs.append(x); ys.append(y)
if xs:
    print(f"  x {ix(min(xs)):.3f}-{ix(max(xs)):.3f} y {iy(min(ys)):.3f}-{iy(max(ys)):.3f}")

print("== badge (playlist chrome: circle d36px c(893,71) FDFD96 + 6A5ACD ring) ==")
yb = bands_of("badgefill", 30, 200, 1780, 1990, gap_px=4)
if yb:
    b = yb[0]
    xb = [x for x in range(1780, 1990) if any(classify(*px[x, y]) == "badgefill" for y in range(b[0], b[1]))]
    cx = (xb[0] + xb[-1]) / 2 / K; cy = (b[0] + b[-1]) / 2 / K
    d = (xb[-1] - xb[0] + 1) / K
    print(f"  fill center ({cx:.1f},{cy:.1f}) orig-px (target 893,71), d={d:.1f}px (target 36)")
    # ring color sample at left edge of fill
    ring = px[xb[0] - 3, (b[0] + b[-1]) // 2]
    print(f"  ring sample {ring} (target 6A5ACD=(106,90,205) family)")
    dark = [(x, y) for y in range(b[0], b[1]) for x in range(xb[0], xb[-1]) if sum(px[x, y]) < 340]
    if dark:
        dy = [d2[1] for d2 in dark]
        print(f"  numeral ink h {(max(dy)-min(dy)+1)/K:.1f} orig-px")

print("== colors / canvas ==")
c = Counter()
for y in range(280, 480):
    for x in range(500, 1500):
        r, g, b = px[x, y]
        if r > 140 and g < 60: c[(r, g, b)] += 1
print("  title red core:", c.most_common(1), "(target C00000)")
print("  canvas corner:", px[5, 5], "(target FFFFFF)")
print("  panel:", px[1000, 700], "(target E9E9E7)")

print("== containment: content vs chrome ==")
def ink_outside_panel():
    # ink = not white, not panel gray, not red border rows/cols; scan margins beyond chrome
    n = 0
    for y in range(0, 92):          # above panel top (45px*2.0849=94) minus border
        for x in range(0, W, 2):
            r, g, b = px[x, y]
            if not (r > 246 and g > 246 and b > 246): n += 1
    return n
print(f"  non-white px above panel border zone: {ink_outside_panel()} (border AA only expected)")
# left of panel border (x < 87px@150), y in panel range
n = sum(1 for y in range(100, H - 5) for x in range(0, 86) if not all(v > 246 for v in px[x, y]))
print(f"  non-white px left of border zone: {n}")
n = sum(1 for y in range(100, H - 5) for x in range(W - 40, W) if not all(v > 246 for v in px[x, y]))
print(f"  non-white px right of border zone: {n} (border AA expected)")
