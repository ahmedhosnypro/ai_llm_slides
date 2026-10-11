#!/usr/bin/env python3
"""Self-check attempt 1, pass C (after build v2): full verification with corrected windows."""
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

def classify(r, g, b):
    if r > 120 and g < 90 and b < 90 and (r - max(g, b)) > 60: return "red"
    if b > 100 and b - r > 60 and b - g > 40: return "blue"
    if r > 200 and g > 200 and b < 210 and (r - b) > 40: return "yellow"
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

ok = lambda d: "OK " if abs(d) <= 0.028 else "!! "

print("== title ==")
tb = bands_of("red", 40, 460, 400, 1600)
if len(tb) >= 2:
    L1, L2 = tb[0], tb[1]
    r1 = xext("red", L1[0], L1[1], 300, 1700)
    r2 = xext("red", L2[0], L2[1], 300, 1700)
    w1 = (r1[-1][1] - r1[0][0] + 1) / PPI * 72
    w2 = (r2[-1][1] - r2[0][0] + 1) / PPI * 72
    print(f"  L1 band {L1} width {w1:.1f}pt (orig 424) {ok(w1-424)} center {ix((r1[0][0]+r1[-1][1])/2):.3f}")
    print(f"  L2 band {L2} width {w2:.1f}pt (orig 252) {ok(w2-252)} pitch {(L2[0]-L1[0])/PPI*72:.1f}pt (target 67)")
    gapword = None
    if len(r1) >= 2:
        # find biggest gap between runs
        gaps = [(r1[i+1][0] - r1[i][1], i) for i in range(len(r1)-1)]
        gmax, gi = max(gaps)
        gapword = gmax / PPI * 72
        print(f"  L1 word gap {gapword:.1f}pt (orig ~41) runs={len(r1)}")

print("== credit block ==")
for b in bands_of("red", 380, 620, 800, 1300):
    r = xext("red", b[0], b[1], 800, 1300)
    if r:
        c = ix((r[0][0] + r[-1][1]) / 2)
        w = (r[-1][1] - r[0][0] + 1) / PPI * 72
        print(f"  PreparedBy top={iy(b[0]):.3f}in (t 2.721 {ok(iy(b[0])-2.721)}) c={c:.3f} (t 7.158 {ok(c-7.158)}) w={w:.1f}pt (orig 112)")
for b in bands_of("blue", 380, 620, 600, 1600):
    r = xext("blue", b[0], b[1], 600, 1600)
    if r:
        c = ix((r[0][0] + r[-1][1]) / 2)
        w = (r[-1][1] - r[0][0] + 1) / PPI * 72
        print(f"  blue top={iy(b[0]):.3f}in c={c:.3f} w={w:.1f}pt")

print("== instructors ==")
for b in bands_of("red", 800, 900, 80, 500):
    r = xext("red", b[0], b[1], 80, 500)
    if r:
        w = (r[-1][1] - r[0][0] + 1) / PPI * 72
        print(f"  heading top={iy(b[0]):.3f}in (t 5.708 {ok(iy(b[0])-5.708)}) left={ix(r[0][0]):.3f} (t 0.778 {ok(ix(r[0][0])-0.778)}) w={w:.1f}pt (orig 120)")
tg = [6.083, 6.431, 6.722, 7.042]
ow = [262, 206, 225, 197]
for i, b in enumerate(bands_of("blue", 880, 1110, 100, 900)):
    r = xext("blue", b[0], b[1], 100, 900)
    t = tg[i] if i < len(tg) else None
    o = ow[i] if i < len(ow) else None
    if r and t:
        w = (r[-1][1] - r[0][0] + 1) / PPI * 72
        print(f"  item{i+1} top={iy(b[0]):.3f}in (t {t} {ok(iy(b[0])-t)}) left={ix(r[0][0]):.3f} (t 1.333 {ok(ix(r[0][0])-1.333)}) w={w:.1f}pt (orig {o})")

print("== logo (window y 930-1090 excludes frame stroke) ==")
def is_canvas(r, g, b): return 218 <= r <= 242 and 220 <= g <= 244 and 217 <= b <= 242
xs, ys = [], []
for y in range(930, 1092):
    for x in range(1200, 1930):
        if not is_canvas(*px[x, y]):
            xs.append(x); ys.append(y)
if xs:
    print(f"  ink x {ix(min(xs)):.3f}-{ix(max(xs)):.3f}in (t 8.250-12.583) y {iy(min(ys)):.3f}-{iy(max(ys)):.3f}in (t 6.401-7.220)")
    print(f"  bottom gap to 7.34: {7.34-iy(max(ys)):.3f}in {ok(7.34-iy(max(ys))-0.12)}")

print("== crosshair ==")
xs, ys = [], []
for y in range(380, 470):
    for x in range(280, 470):
        r, g, b = px[x, y]
        if (232 - r) > 15 and (232 - g) > 15 and (232 - b) > 15:
            xs.append(x); ys.append(y)
if xs:
    print(f"  x {ix(min(xs)):.3f}-{ix(max(xs)):.3f} (t 2.403-2.542) y {iy(min(ys)):.3f}-{iy(max(ys)):.3f} (t 2.750-2.903)")

print("== badge (FFF9C4-aware) ==")
def is_badge_fill(r, g, b): return r > 240 and g > 235 and 170 < b < 225
yb = [y for y in range(30, 160) if any(is_badge_fill(*px[x, y]) for x in range(1840, 1990))]
if yb:
    xb = [x for x in range(1840, 1990) if any(is_badge_fill(*px[x, y]) for y in range(30, 160))]
    print(f"  fill rows {yb[0]}-{yb[-1]} ({iy(yb[0]):.3f}-{iy(yb[-1]):.3f}in; t 0.30-0.80) cols {xb[0]}-{xb[-1]} ({ix(xb[0]):.3f}-{ix(xb[-1]):.3f}in; t 12.48-12.98)")
    dark = [(x, y) for y in range(yb[0], yb[-1]) for x in range(xb[0], xb[-1]) if sum(px[x, y]) < 340]
    if dark:
        dx = [d[0] for d in dark]; dy = [d[1] for d in dark]
        print(f"  numeral '1' ink x {min(dx)}-{max(dx)} y {min(dy)}-{max(dy)} h={(max(dy)-min(dy)+1)/PPI*72:.1f}pt")
else:
    print("  NO FILL FOUND")

print("== colors ==")
c = Counter()
for y in range(80, 260):
    for x in range(500, 1500):
        r, g, b = px[x, y]
        if r > 140 and g < 60: c[(r, g, b)] += 1
print("  title red core:", c.most_common(1))
c = Counter()
for y in range(440, 530):
    for x in range(700, 1500):
        r, g, b = px[x, y]
        if b > 100 and b - r > 60 and b - g > 40: c[(r, g, b)] += 1
print("  name blue core:", c.most_common(1))
print("  canvas:", px[1000, 700])

print("== containment: inner content vs house frame ==")
# frame strokes at ~0.15in (22-24px) and 13.18/7.35in; assert no non-bg ink beyond strokes
def ink_in(x0, x1, y0, y1):
    n = 0
    for y in range(max(0, y0), min(H, y1)):
        for x in range(max(0, x0), min(W, x1)):
            r, g, b = px[x, y]
            if not (218 <= r <= 242 and 220 <= g <= 244 and 217 <= b <= 242):
                n += 1
    return n
print(f"  outside-frame margins (should be 0 beyond strokes): top={ink_in(0, W, 0, 21)} left={ink_in(0, 21, 0, H)} right={ink_in(W-21, W, 0, H)} bottom={ink_in(0, W, H-21, H)}")
print(f"  between stroke and inner edge (should be ~0): top={ink_in(25, W-25, 25, 30)} bottom={ink_in(25, W-25, 1098, 1103)} left={ink_in(25, 30, 25, H-25)} right={ink_in(1973, 1978, 25, H-25)}")
