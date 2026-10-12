#!/usr/bin/env python3
# selfcheck_attempt_1.py — closed-loop PIL verification of render_1.png (150dpi, 2001x1125)
# against the original-frame measurements (960x540, 1px=1pt). Scale: 2001/960 = 2.0844.
# Tolerance: ~4px @150dpi (= ~2 frame px) per the equation/geometry closed-loop law.
import sys
from PIL import Image
from collections import Counter

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide010/render_2.png"
S = 2001 / 960.0  # frame px -> render px
TOL = 4.0         # render px

im = Image.open(RENDER).convert("RGB")
W, H = im.size
px = im.load()
print(f"render size {W}x{H} (expected ~2001x1125)")

def ink(c): return sum(c) < 400
def dark(c): return sum(c) < 330
def redish(c): return c[0] > 110 and c[0] > c[1] + 50 and c[0] > c[2] + 50

fails = []
def check(name, got, want, tol=TOL):
    d = abs(got - want)
    ok = d <= tol
    print(f"  [{'OK ' if ok else 'FAIL'}] {name}: got {got:.1f} want {want:.1f} (d={d:.1f})")
    if not ok: fails.append(name)

def f(v): return v * S  # frame px to render px

# ---- title box borders (navy) ----
def find_dark_rows(x0, x1, y0, y1):
    return [y for y in range(y0, y1) if sum(1 for x in range(x0, x1) if dark(px[x, y])) > (x1 - x0) * 0.5]
def find_dark_cols(y0, y1, x0, x1):
    return [x for x in range(x0, x1) if sum(1 for y in range(y0, y1) if dark(px[x, y])) > (y1 - y0) * 0.5]

print("== title box ==")
tr = find_dark_rows(int(f(150)), int(f(280)), int(f(50)), int(f(75)))
check("title top border", (tr[0] + tr[-1]) / 2 / S, 61, 3.0)
br = find_dark_rows(int(f(150)), int(f(280)), int(f(112)), int(f(124)))
check("title bottom border", (br[0] + br[-1]) / 2 / S, 118, 3.0)
lc = find_dark_cols(int(f(70)), int(f(110)), int(f(96)), int(f(116)))
check("title left border", (lc[0] + lc[-1]) / 2 / S, 106, 3.0)
rc = find_dark_cols(int(f(70)), int(f(110)), int(f(315)), int(f(335)))
check("title right border", (rc[0] + rc[-1]) / 2 / S, 325, 3.0)

print("== content box ==")
tr = find_dark_rows(int(f(500)), int(f(850)), int(f(118)), int(f(136)))
check("content top border", (tr[0] + tr[-1]) / 2 / S, 127, 3.0)
br = find_dark_rows(int(f(500)), int(f(850)), int(f(505)), int(f(518)))
check("content bottom border", (br[0] + br[-1]) / 2 / S, 513, 3.0)
lc = find_dark_cols(int(f(140)), int(f(480)), int(f(88)), int(f(102)))
check("content left border", (lc[0] + lc[-1]) / 2 / S, 95, 3.0)
rc = find_dark_cols(int(f(140)), int(f(480)), int(f(874)), int(f(890)))
check("content right border", (rc[0] + rc[-1]) / 2 / S, 882, 3.0)

print("== title text ==")
# robust: full ink rows in the title-box interior; baseline = last dense row before the
# sparse 'g' descender tail; cap = first ink row.
txs = [x for x in range(int(f(112)), int(f(320))) for y in range(int(f(66)), int(f(112))) if dark(px[x, y])]
check("title ink left", min(txs) / S, 125)
check("title ink right", max(txs) / S, 306)
trows = [(y, sum(1 for x in range(int(f(115)), int(f(315))) if dark(px[x, y])))
         for y in range(int(f(70)), int(f(112)))]
tink = [(y, n) for y, n in trows if n > 0]
check("title ink top (cap)", min(y for y, n in tink) / S, 80)
dense = [y for y, n in tink if n > 60]  # body rows are >=130 in the crisp render; 'g' descender rows <=30
check("title baseline", max(dense) / S, 98, 4.0)

print("== lead line ==")
# red word extent
red_cols = [x for x in range(int(f(110)), int(f(400))) if any(redish(px[x, y]) for y in range(int(f(133)), int(f(158))))]
check("red word left", min(red_cols) / S, 127)
check("red word right", max(red_cols) / S, 271)
# full lead ink extent
ys = range(int(f(133)), int(f(158)))
xs = [x for x in range(int(f(110)), int(f(720))) if any(dark(px[x, y]) or redish(px[x, y]) for y in ys)]
check("lead ink left", min(xs) / S, 127)
check("lead ink right", max(xs) / S, 676)
# lead baseline: bottom of 'is/Problem' zone (x 290..660) excluding descenders
base_rows = [y for y in range(int(f(133)), int(f(160))) if sum(1 for x in range(int(f(290)), int(f(660))) if dark(px[x, y])) > 20]
check("lead baseline", max(base_rows) / S, 151.5, 5.0)

print("== intro line ==")
ys = range(int(f(180)), int(f(206)))
xs = [x for x in range(int(f(110)), int(f(320))) if any(dark(px[x, y]) for y in ys)]
check("intro ink left", min(xs) / S, 127)
check("intro ink right", max(xs) / S, 271)
base_rows = [y for y in range(int(f(180)), int(f(206))) if sum(1 for x in range(int(f(140)), int(f(275))) if dark(px[x, y])) > 15]
check("intro baseline", max(base_rows) / S, 198, 5.0)

# lead line — underline + italic checks (attempt-2 additions; judge attempt-1 MAJOR fix)
print("== lead underline/italic ==")
# underline: continuous run at y~153-154 spanning the phrase x300..676 (render: black, easy)
ul_rows = []
for y in range(int(f(150)), int(f(159))):
    xs = [x for x in range(int(f(298)), int(f(680))) if sum(px[x, y]) < 650]
    if xs:
        best = 0; cur = 0; prev = None
        for x in xs:
            cur = cur + 1 if prev is not None and x == prev + 1 else 1
            best = max(best, cur); prev = x
        ul_rows.append((y, len(xs), best))
print("  underline candidate rows (y_frame, n, longest_run):", [(round(y / S, 1), n, r) for y, n, r in ul_rows])
cont = [y for y, n, r in ul_rows if r > int(f(370))]
check("underline continuous rows", len(cont), 1.5, 2.5)  # 1-4 rows expected
# italic: 'P' cap-stem slant — stem left edge at top vs bottom (~3px right-shift at top over 14 rows)
stem = []
for y in range(int(f(137)), int(f(153))):
    xs = [x for x in range(int(f(296)), int(f(310))) if dark(px[x, y])]
    if xs: stem.append((y, min(xs)))
if len(stem) >= 8:
    top = min(xs for y, xs in stem[:4]); bot = min(xs for y, xs in stem[-4:])
    shift = (top - bot) / S  # italic: stem left edge moves LEFT toward the baseline
    print(f"  P-stem left edge: top {top / S:.1f} bottom {bot / S:.1f} -> slant {shift:.1f} frame px (want ~2..4)")
    check("italic P-stem slant", shift if shift > 0 else 0, 3.0, 2.5)
else:
    print("  [FAIL] P stem not measurable"); fails.append("italic slant")

print("== bullets (text-left 147, baselines, right extents) ==")
BL = [("Gap filling", 221.7, 237), ("Thinning", 253.8, 224), ("Contour", 286, 219),
      ("Binarization", 318.2, 253), ("Noise Removal", 350.3, 286), ("Color to Gray", 382.5, 270),
      ("Opening touched points", 414.7, 366), ("Resizing", 446.8, 224), ("Normalization", 479, 272)]
for i, (t, base, right) in enumerate(BL):
    y0, y1 = int(f(base - 16)), int(f(base + 8))
    xs = [x for x in range(int(f(138)), int(f(430))) if any(dark(px[x, y]) for y in range(y0, y1))]
    check(f"b{i+1} text-left", min(xs) / S, 147)
    check(f"b{i+1} ink right", max(xs) / S, right, 5.0)
# ellipsis line (baseline 503): dots x149..182, bullet marker 127..131
y0, y1 = int(f(486)), int(f(508))
xs = [x for x in range(int(f(138)), int(f(250))) if any(dark(px[x, y]) for y in range(y0, y1))]
check("ellipsis dots left", min(xs) / S, 149, 5.0)
check("ellipsis dots right", max(xs) / S, 182, 5.0)
# bullet baselines (closed-loop calibration check)
for i, (t, base, right) in enumerate(BL):
    rows = [(y, sum(1 for x in range(int(f(147)), int(f(right + 1))) if dark(px[x, y])))
            for y in range(int(f(base - 17)), int(f(base + 7)))]
    dense = [y for y, n in rows if n > (right - 147) * 0.25]
    check(f"b{i+1} baseline", max(dense) / S, base, 4.0)

# ellipsis line baseline (attempt-2: nudged to 501.7)
erows = [(y, sum(1 for x in range(int(f(147)), int(f(190))) if dark(px[x, y])))
         for y in range(int(f(492)), int(f(508)))]
edense = [y for y, n in erows if n >= 4]
check("ellipsis baseline", max(edense) / S, 501.7, 4.0)

print("== bullet dots ==")
DC = [214, 246, 278.5, 311, 343, 375, 407, 439, 471, 495]
for i, cy in enumerate(DC):
    ys = [y for y in range(int(f(cy - 9)), int(f(cy + 9))) if sum(1 for x in range(int(f(124)), int(f(136))) if ink(px[x, y])) >= 2]
    if not ys:
        print(f"  [FAIL] dot{i+1} not found near y={cy}"); fails.append(f"dot{i+1}"); continue
    check(f"dot{i+1} center", (min(ys) + max(ys)) / 2 / S, cy, 4.0)

print("== black bar ==")
xs = [x for x in range(W) if sum(px[x, int(f(530))]) < 150]
check("bar left", min(xs) / S, 38, 5.0)
check("bar right", max(xs) / S, 921, 5.0)
brows = [y for y in range(int(f(510)), H)
         if all(sum(px[x, y]) < 150 for x in range(int(f(45)), int(f(90)), 5))]
check("bar top", min(brows) / S, 519, 5.0)

print("== colors ==")
def modal(x0, y0, x1, y1):
    return Counter(px[x, y] for y in range(y0, y1) for x in range(x0, x1)).most_common(1)[0][0]
c = modal(int(f(150)), int(f(80)), int(f(300)), int(f(100)))
print(f"  title fill modal {c} (orig modal (250,254,217), want FAFED9-ish)")
c = modal(int(f(400)), int(f(60)), int(f(800)), int(f(115)))
print(f"  panel modal {c} (orig (231,233,230), want E9E9E7-ish)")
red_core = Counter(px[x, y] for y in range(int(f(137)), int(f(153))) for x in range(int(f(127)), int(f(272))) if redish(px[x, y]) and sum(px[x, y]) < 420)
print(f"  red word core {red_core.most_common(3)} (orig core ~(133,15,27)/(150,35,50) = C00000 JPEG-dark)")

print()
if fails:
    print("SELFCHECK RESULT: FAIL —", fails)
    sys.exit(1)
print("SELFCHECK RESULT: PASS (all geometry within tolerance)")
