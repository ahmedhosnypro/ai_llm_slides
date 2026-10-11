#!/usr/bin/env python3
"""Pre-judge self-check for slide 002 (attempt K) — PIL closed-loop vs original frame.

Frame ground truth measured on unique_slides/slide_002.jpg (960x540, 1px = 1pt).
Render is 150 dpi (2000x1125): frame_px * (150/72) = render_px.
Checks: chrome colors, panel geometry, text band geometry (=> font sizes),
badge geometry + numeral ink presence, frame containment (panel inner region).
"""
import sys
from PIL import Image

RENDER = sys.argv[1] if len(sys.argv) > 1 else \
    "videos/deep-learning/001_transformers_part1/scratch/slide002/slide-1.png"
S = 150.0 / 72.0  # frame px -> render px

im = Image.open(RENDER).convert("RGB")
w, h = im.size
px = im.load()
print(f"render: {RENDER} {w}x{h} (expect ~2000x1125)")

def is_white(p): return p[0] > 245 and p[1] > 245 and p[2] > 245
def is_red(p): return p[0] > 110 and p[1] < 95 and p[2] < 95
def is_redish(p): return p[0] > 150 and p[1] < 140 and p[2] < 140 and p[0] - p[1] > 40
def is_yellow(p): return p[0] > 220 and p[1] > 210 and p[2] < 200
def is_purple(p): return p[2] > 60 and p[0] < 200 and p[2] > p[1] + 20 and not is_yellow(p)

fails, warns = [], []
def check(name, ok, detail=""):
    print(f"[{'OK ' if ok else 'FAIL'}] {name} {detail}")
    if not ok: fails.append(name + " " + detail)

def hexat(x, y): return "#%02X%02X%02X" % px[x, y]

# --- 1. canvas + panel fill colors
corners = [hexat(5, 5), hexat(w - 6, 5), hexat(5, h - 6), hexat(w - 6, h - 6)]
check("canvas corners white", all(c in ("#FFFFFF", "#FEFFFD", "#FFFEFD") for c in corners), str(corners))
check("panel fill ~E9E9E7", hexat(w // 4, h // 2) in ("#E8E8E8", "#E9E9E7", "#E7E9E6", "#E9E9E9"), hexat(w // 4, h // 2))

# --- 2. panel geometry (text-free rows/cols)
y_probe = int(0.42 * h)   # below texts, above bottom
xs = [x for x in range(w) if not is_white(px[x, y_probe])]
x0, x1 = min(xs), max(xs)
exp_x0, exp_x1 = 37 * S, 923 * S
check("panel left edge", abs(x0 - exp_x0) <= 5, f"{x0} vs {exp_x0:.1f}")
check("panel right edge", abs(x1 - exp_x1) <= 5, f"{x1} vs {exp_x1:.1f}")
x_probe = int(0.10 * w)
ys = [yy for yy in range(h) if not is_white(px[x_probe, yy])]
y0 = min(ys)
check("panel top edge", abs(y0 - 42 * S) <= 5, f"{y0} vs {42 * S:.1f}")
# bottom stroke: dark red present in last rows at mid-x
bot = [yy for yy in range(h - 12, h) if is_red(px[int(0.5 * w), yy])]
check("panel bottom stroke visible", len(bot) >= 1, f"red rows at bottom: {bot}")
# border color sanity: reddish stroke at left edge
rowc = [px[x, y_probe] for x in range(x0, x0 + 8)]
check("left border reddish", any(is_red(p) or is_redish(p) for p in rowc), str([hexat(x, y_probe) for x in range(x0, min(x0 + 4, w))]))

# --- 3. text bands (red text inside panel interior)
def bands(x_range, y_range):
    rows = {}
    for y in range(y_range[0], y_range[1]):
        cnt = sum(1 for x in range(*x_range) if is_red(px[x, y]))
        if cnt: rows[y] = cnt
    out, start, prev = [], None, None
    for y in sorted(rows):
        if start is None: start = y
        elif y - prev > 5: out.append((start, prev)); start = y
        prev = y
    if start is not None: out.append((start, prev))
    res = []
    for a, b in out:
        bxs = [x for y in range(a, b + 1) for x in range(*x_range) if is_red(px[x, y])]
        res.append((a, b, min(bxs), max(bxs)))
    return res

bands_ = bands((int(45 * S), int(915 * S)), (int(50 * S), h - 14))
print("  red text bands (render px):", bands_)
exp = {
    "title":    dict(y=(196, 249.5), x=(245, 710)),
    "subtitle": dict(y=(276.5, 312.5), x=(416, 542)),
    "date":     dict(y=(338, 358.5), x=(436, 545)),
}
names = ["title", "subtitle", "date"]
check("3 text bands present", len(bands_) == 3, f"got {len(bands_)}")
if len(bands_) == 3:
    for (a, b, xa, xb), nm in zip(bands_, names):
        e = exp[nm]
        dy0, dy1 = a - e["y"][0] * S, b - e["y"][1] * S
        dx0, dx1 = xa - e["x"][0] * S, xb - e["x"][1] * S
        hgt = (b - a) / ((e["y"][1] - e["y"][0]) * S)
        wdt = (xb - xa) / ((e["x"][1] - e["x"][0]) * S)
        ok = abs(dy0) <= 6 and abs(dy1) <= 6 and abs(dx0) <= 8 and abs(dx1) <= 8 and 0.94 <= hgt <= 1.06
        check(f"{nm} geometry", ok,
              f"dy0={dy0:+.1f} dy1={dy1:+.1f} dx0={dx0:+.1f} dx1={dx1:+.1f} h_ratio={hgt:.3f} w_ratio={wdt:.3f}")

# --- 4. badge
yel = [(x, y) for y in range(int(40 * S), int(110 * S)) for x in range(int(855 * S), int(925 * S)) if is_yellow(px[x, y])]
if yel:
    yxs = [p[0] for p in yel]; yys = [p[1] for p in yel]
    ey = (876 * S, 911 * S, 57 * S, 86 * S)
    check("badge yellow fill bbox", abs(min(yxs) - ey[0]) <= 8 and abs(max(yxs) - ey[1]) <= 8
          and abs(min(yys) - ey[2]) <= 8 and abs(max(yys) - ey[3]) <= 8,
          f"x {min(yxs)}..{max(yxs)} y {min(yys)}..{max(yys)} exp {ey[0]:.0f}..{ey[1]:.0f}/{ey[2]:.0f}..{ey[3]:.0f}")
else:
    check("badge yellow fill present", False, "no yellow pixels in badge region")
pur = [(x, y) for y in range(int(45 * S), int(100 * S)) for x in range(int(860 * S), int(925 * S)) if is_purple(px[x, y])]
check("badge purple outline present", len(pur) > 40, f"{len(pur)} purple px")
if pur:
    pxs = [p[0] for p in pur]; pys = [p[1] for p in pur]
    check("badge outline bbox", abs(min(pxs) - 872 * S) <= 10 and abs(max(pxs) - 914 * S) <= 10
          and abs(min(pys) - 53 * S) <= 10 and abs(max(pys) - 90 * S) <= 10,
          f"x {min(pxs)}..{max(pxs)} y {min(pys)}..{max(pys)}")
# numeral ink: neutral-dark pixels inside yellow zone
def neutral_dark(p): return max(p) - min(p) < 50 and sum(p) < 340
ink = [(x, y) for y in range(int(58 * S), int(88 * S)) for x in range(int(880 * S), int(906 * S)) if neutral_dark(px[x, y])]
check("badge numeral ink present", len(ink) > 30, f"{len(ink)} ink px")
if ink:
    iys = [p[1] for p in ink]
    check("numeral digit height", abs((max(iys) - min(iys)) - 11 * S) <= 5,
          f"{max(iys) - min(iys)} vs {11 * S:.1f}")

# --- 5. frame containment: no content ink outside panel inner region
#      panel inner: x in (x0+4, x1-4), y in (y0+4, h) — bottom edge intended at slide bottom
inner = [0] * w
viol = []
for y in range(0, y0 - 2):
    for x in range(0, w, 2):
        p = px[x, y]
        if not is_white(p): viol.append((x, y, hexat(x, y)))
for y in range(y0, h, 3):
    for x in list(range(0, x0 - 2, 2)) + list(range(x1 + 3, w, 2)):
        p = px[x, y]
        if not is_white(p): viol.append((x, y, hexat(x, y)))
check("containment: ink only inside panel (+bottom bleed)", len(viol) < 20, f"{len(viol)} outliers {viol[:6]}")

print()
print("SELF-CHECK RESULT:", "PASS" if not fails else f"FAIL ({len(fails)}): " + "; ".join(fails))
sys.exit(0 if not fails else 1)
