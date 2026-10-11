#!/usr/bin/env python3
"""Consolidated pre-judge self-check, attempt 1 (final build, playlist chrome).
Banks: PIL geometry vs original targets, chrome colors, containment, badge/logo.
Run: python3 selfcheck_attempt_1.py > selfcheck_attempt_1_output.txt
"""
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
K = PPI / 72.0

def classify(r, g, b):
    if r > 120 and g < 90 and b < 90 and (r - max(g, b)) > 60: return "red"
    if b > 100 and b - r > 60 and b - g > 40: return "blue"
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

FAILS = []
def chk(name, got, target, tol=0.028):
    d = got - target
    s = f"  {name}: {got:.3f}in (target {target:.3f}, d={d:+.3f}) {'OK' if abs(d) <= tol else '!!'}"
    print(s)
    if abs(d) > tol: FAILS.append(name)

print("== title (targets: cap tops 1.903/2.833, centers 6.465/6.486, widths 424/252, pitch 67) ==")
tb = bands_of("red", 250, 560, 300, 1700)
L1, L2 = tb[0], tb[1]
chk("L1 cap top", iy(L1[0]), 1.903)
chk("L2 cap top", iy(L2[0]), 2.833)
print(f"  pitch {(L2[0]-L1[0])/K:.1f} orig-px (t 67; LO renders exact-67 as ~66; PowerPoint true)")
r1 = xext("red", L1[0], L1[1], 200, 1800)
r2 = xext("red", L2[0], L2[1], 200, 1800)
chk("L1 ink center", ix((r1[0][0]+r1[-1][1])/2), 6.465)
chk("L2 ink center", ix((r2[0][0]+r2[-1][1])/2), 6.486)
print(f"  L1 width {(r1[-1][1]-r1[0][0]+1)/K:.1f} (t 424), L2 width {(r2[-1][1]-r2[0][0]+1)/K:.1f} (t 252), word gap {(max(r1[i+1][0]-r1[i][1] for i in range(len(r1)-1)))/K:.1f} (t ~41)")

print("== credit block (cap tops 4.194/4.528/4.889; center 7.158; widths 112/287/220) ==")
for b in bands_of("red", 550, 720, 800, 1300):
    r = xext("red", b[0], b[1], 800, 1300)
    if r:
        chk("PreparedBy cap top", iy(b[0]), 4.194)
        chk("PreparedBy center", ix((r[0][0]+r[-1][1])/2), 7.158)
        print(f"  width {(r[-1][1]-r[0][0]+1)/K:.1f} (t 112)")
for i, b in enumerate(bands_of("blue", 560, 780, 600, 1600)):
    r = xext("blue", b[0], b[1], 600, 1600)
    if r and i < 2:
        chk(f"credit line{i+1} top", iy(b[0]), [4.528, 4.889][i])
        chk(f"credit line{i+1} center", ix((r[0][0]+r[-1][1])/2), 7.158)
        print(f"  width {(r[-1][1]-r[0][0]+1)/K:.1f} (t {[287,220][i]})")

print("== instructors (cap tops 5.708/6.083/6.431/6.722/7.042; lefts 0.778/1.333) ==")
hb = bands_of("red", 820, 900, 110, 500)
r = xext("red", hb[0][0], hb[0][1], 110, 500)
chk("heading cap top", iy(hb[0][0]), 5.708)
chk("heading left", ix(r[0][0]), 0.778)
print(f"  width {(r[-1][1]-r[0][0]+1)/K:.1f} (t 120)")
tg = [6.083, 6.431, 6.722, 7.042]; ow = [262, 206, 225, 197]
for i, b in enumerate(bands_of("blue", 880, 1115, 100, 900)):
    r = xext("blue", b[0], b[1], 100, 900)
    if r and i < 4:
        chk(f"item{i+1} top", iy(b[0]), tg[i])
        chk(f"item{i+1} left", ix(r[0][0]), 1.333)
        print(f"  width {(r[-1][1]-r[0][0]+1)/K:.1f} (t {ow[i]})")

print("== logo (target 8.25-12.583 x 6.5-7.306) ==")
def is_panel(rr, g, b): return 222 <= rr <= 240 and 222 <= g <= 240 and 220 <= b <= 238
xs, ys = [], []
for y in range(940, 1112):
    for x in range(1200, 1900):
        if not is_panel(*px[x, y]):
            xs.append(x); ys.append(y)
chk("logo left", ix(min(xs)), 8.25)
chk("logo top", iy(min(ys)), 6.5)
print(f"  right {ix(max(xs)):.3f} (t 12.583) bottom {iy(max(ys)):.3f} (t 7.306)")

print("== crosshair (target 2.403-2.542 / 2.750-2.903) ==")
xs, ys = [], []
for y in range(380, 470):
    for x in range(280, 470):
        rr, g, b = px[x, y]
        if (233 - rr) > 15 and (233 - g) > 15 and (231 - b) > 15:
            xs.append(x); ys.append(y)
print(f"  x {ix(min(xs)):.3f}-{ix(max(xs)):.3f} y {iy(min(ys)):.3f}-{iy(max(ys)):.3f}")

print("== badge (circle d36 c(893,71) FDFD96 fill + 6A5ACD ring + numeral) ==")
def is_fill(rr, g, b): return rr > 240 and g > 240 and 110 < b < 200
yb = [y for y in range(30, 220) if any(is_fill(*px[x, y]) for x in range(1780, 1990))]
xb = [x for x in range(1780, 1990) if any(is_fill(*px[x, y]) for y in range(30, 220))]
cx = (xb[0]+xb[-1])/2/K/72; cy = (yb[0]+yb[-1])/2/K/72  # orig-px -> inches
chk("badge cx", cx, 12.403, 0.03); chk("badge cy", cy, 0.986, 0.03)
print(f"  fill d={(xb[-1]-xb[0]+1)/K:.1f}px (t 36 incl 2pt ring), ring sample {px[xb[0]-4,(yb[0]+yb[-1])//2]} (t 6A5ACD)")
dark = [(x,y) for y in range(yb[0], yb[-1]) for x in range(xb[0], xb[-1]) if sum(px[x,y]) < 340]
print(f"  numeral ink present: {bool(dark)}")

print("== colors ==")
c = Counter()
for y in range(280, 480):
    for x in range(500, 1500):
        rr, g, b = px[x, y]
        if rr > 140 and g < 60: c[(rr, g, b)] += 1
print(f"  title red core {c.most_common(1)[0][0]} (t C00000=(192,0,0))")
c = Counter()
for y in range(580, 700):
    for x in range(700, 1500):
        rr, g, b = px[x, y]
        if b > 100 and b - rr > 60 and b - g > 40: c[(rr, g, b)] += 1
print(f"  name blue core {c.most_common(1)[0][0]} (t 000090=(0,0,144), frame-measured mode)")
print(f"  canvas {px[5,5]} (t FFFFFF), panel {px[1000,700]} (t E9E9E7=(233,233,231))")

print("== containment: white-canvas band check (adapted inner-frame-budget) ==")
import numpy as np
a = np.asarray(im).astype(int)
ink = (np.abs(a - np.array([255,255,255])).sum(axis=2) > 40)
def pxi(v): return int(round(v * PPI))
x0, y0, x1, y1 = pxi(0.5833), pxi(0.625), pxi(0.5833+12.1806), pxi(0.625+6.875)
bnd = pxi(0.06)
bands = {"top": ink[y0-bnd:y0-3, x0+3:x1-3], "bottom": ink[y1+3:min(H, y1+bnd), x0+3:x1-3],
         "left": ink[y0+3:y1-3, x0-bnd:x0-3], "right": ink[y0+3:y1-3, x1+3:x1+bnd]}
bad = {k2: int(v.sum()) for k2, v in bands.items()}
print(f"  ink-px outside panel bands: {bad} -> {'PASS' if all(v==0 for v in bad.values()) else 'FAIL'}")
if not all(v == 0 for v in bad.values()): FAILS.append("containment")

print(f"\nSELF-CHECK RESULT: {'ALL PASS' if not FAILS else 'FAIL: ' + ', '.join(FAILS)}")
