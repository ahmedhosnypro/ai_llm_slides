#!/usr/bin/env python3
"""measure3.py — slide 025 full-delta verification pass (builder's own).
Measures: panel, title, top strip, dots/rings/neurons, mesh, labels, outboxes,
error bar, class boxes, block arrows, callouts, equation boxes, footer.
1px = 1pt. Output banked as measure3_out.txt."""
import json
from collections import Counter
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide025/measure3_out.txt"
im = Image.open(SRC).convert("RGB")
W, H = im.size
P = im.load()
L = []
def pr(*a):
    s = " ".join(str(x) for x in a)
    L.append(s); print(s)

def modal(x0, y0, x1, y1, pred):
    c = Counter()
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            r, g, b = P[x, y]
            if pred(r, g, b): c[(r, g, b)] += 1
    return c.most_common(6)

def bbox(x0, y0, x1, y1, pred):
    x1 = min(x1, W - 1); y1 = min(y1, H - 1)
    xs, ys = [], []
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if pred(*P[x, y]): xs.append(x); ys.append(y)
    if not xs: return None
    return (min(xs), min(ys), max(xs), max(ys))

beige = lambda r, g, b: 195 <= r <= 245 and 185 <= g <= 235 and 165 <= b <= 225
dark = lambda r, g, b: r < 130 and g < 130 and b < 130
red = lambda r, g, b: r > 140 and g < 90 and b < 90
magenta = lambda r, g, b: r > 140 and g < 110 and b > 140
pink = lambda r, g, b: r > 200 and 120 < g < 200 and b > 170

pr("size", W, H)

# ---- panel: beige row extents at several y ----
pr("== panel beige row extents ==")
for y in [140, 160, 200, 261, 300, 350, 380, 385]:
    xs = [x for x in range(40, 920) if beige(*P[x, y])]
    if xs: pr(f"  y{y}: {min(xs)}..{max(xs)} n={len(xs)}")
    else: pr(f"  y{y}: none")
# panel column extents
for x in [70, 300, 560, 600, 640, 660, 670, 680]:
    ys = [y for y in range(120, 420) if beige(*P[x, y])]
    if ys: pr(f"  x{x}: y {min(ys)}..{max(ys)} n={len(ys)}")
pr("panel modal:", modal(70, 140, 130, 160, beige))

# ---- top strip ----
pr("== top strip ==")
pr("IS pink bbox:", bbox(40, 80, 160, 135, pink))
pr("SL pink bbox:", bbox(560, 70, 700, 135, pink))
pr("IS modal:", modal(62, 98, 124, 123, lambda r, g, b: True))
pr("SL modal:", modal(608, 90, 668, 120, lambda r, g, b: True))
pr("IS ink bbox:", bbox(45, 85, 155, 130, dark))
pr("SL ink bbox:", bbox(575, 75, 695, 130, dark))
# dash line: magenta/pinkish px per row between boxes
pr("dash rows (magenta-ish x135..600):")
for y in range(95, 130):
    xs = [x for x in range(130, 601) if magenta(*P[x, y])]
    if len(xs) >= 3: pr(f"  y{y}: n={len(xs)} x {min(xs)}..{max(xs)}")
# arrowheads: magenta density near ends
pr("left end magenta x120..160:", bbox(118, 95, 165, 130, magenta))
pr("right end magenta x590..615:", bbox(588, 95, 620, 130, magenta))

# ---- neuron rows/cols: green neurons ----
green = lambda r, g, b: 120 < r < 200 and g > 210 and 100 < b < 190
pr("== green neuron col bbox per row band ==")
for (y0, y1) in [(155, 215), (228, 288), (310, 370)]:
    pr(f"  band {y0}..{y1}:", bbox(380, y0, 470, y1, green))
pr("green modal:", modal(408, 165, 446, 200, green))
# white neurons col0/col1: non-beige, non-white circles — detect border+fill via 'not beige and light'
whitish = lambda r, g, b: r > 235 and g > 235 and b > 235
pr("== white fill blobs (col0/col1) row bands ==")
for (y0, y1) in [(155, 215), (228, 288), (310, 370)]:
    for (x0, x1) in [(130, 195), (230, 300)]:
        pr(f"  x{x0}..{x1} y{y0}..{y1}:", bbox(x0, y0, x1, y1, whitish))
# neuron borders: scan for dark outline pixels around expected centers
for cy in [183, 256, 337]:
    row_ink = [x for x in range(120, 300) if dark(*P[x, cy])]
    pr(f"  dark ink at y{cy}: {row_ink[:50]}")

# ---- dots ----
pr("== dots ==", bbox(60, 200, 100, 320, magenta))
pr("== rings right of col0 (gray circles) ==")
grayring = lambda r, g, b: 60 <= r <= 160 and 60 <= g <= 160 and 60 <= b <= 160
for cy in [183, 256, 337]:
    pr(f"  y{cy}:", bbox(185, cy - 12, 245, cy + 12, grayring))

# ---- title (verify) ----
pr("== title ink ==", bbox(280, 55, 700, 100, red))
tred = lambda r, g, b: r > 120 and g < 80 and b < 80
pr("title modal:", modal(330, 70, 640, 88, tred))

# ---- Net labels (red ink above neurons) ----
pr("== Net_i/Net_j red ink bboxes ==")
pr("Net_i:", bbox(195, 130, 250, 172, tred))
pr("Net_j:", bbox(360, 130, 420, 172, tred))
pr("Net_i pointer region red ink:", bbox(228, 180, 260, 205, tred))
pr("Net_j pointer region red ink:", bbox(395, 180, 425, 205, tred))

# ---- O labels ----
pr("== O_i labels (red ink right of col1) ==")
for (y0, y1) in [(165, 210), (238, 283), (319, 364)]:
    pr(f"  band {y0}..{y1}:", bbox(272, y0, 305, y1, tred))
pr("== O_j labels ==")
for (y0, y1) in [(165, 210), (238, 283), (319, 364)]:
    pr(f"  band {y0}..{y1}:", bbox(440, y0, 472, y1, tred))

# ---- w_ji labels (blue ink) ----
blue = lambda r, g, b: b > 120 and r < 100 and g < 100
pr("== w_ji blue ink bboxes (x300..380) ==")
pr("  all:", bbox(295, 160, 395, 290, blue))
pr("  top:", bbox(295, 160, 395, 205, blue))
pr("  mid:", bbox(295, 205, 395, 250, blue))
pr("  low:", bbox(295, 250, 395, 290, blue))

# ---- ports (dark red dots at col1/col2 rims) ----
dr = lambda r, g, b: 100 <= r <= 190 and g < 60 and b < 60
pr("== ports col1 right rim ==")
for cy in [183, 256, 337]:
    pr(f"  y{cy}:", bbox(276, cy - 8, 292, cy + 8, dr))
pr("== ports col2 right rim ==")
for cy in [183, 256, 337]:
    pr(f"  y{cy}:", bbox(440, cy - 8, 456, cy + 8, dr))

# ---- output boxes ----
pr("== output boxes ==")
outw = lambda r, g, b: r > 245 and g > 245 and b > 245
for (y0, y1) in [(160, 205), (235, 280), (318, 365)]:
    pr(f"  band {y0}..{y1} white bbox:", bbox(495, y0, 585, y1, outw))
pr("outbox border modal:", modal(500, 168, 575, 195, lambda r, g, b: not outw(r, g, b) and not beige(r, g, b)))
pr("outbox ink bbox r1:", bbox(495, 165, 585, 200, dark))

# ---- error bar ----
er = lambda r, g, b: 120 <= r <= 200 and g < 70 and b < 70
pr("== error bar ==", bbox(570, 140, 615, 375, er))
pr("err modal:", modal(584, 160, 602, 350, er))
pr("err text modal (bright red on bar):", modal(584, 160, 602, 350, lambda r, g, b: r > 200 and g < 80 and b < 80))

# ---- class boxes ----
cg = lambda r, g, b: 190 <= r <= 245 and g > 230 and 160 <= b <= 225
pr("== class boxes ==")
for (y0, y1) in [(155, 215), (228, 288), (310, 370)]:
    pr(f"  band {y0}..{y1}:", bbox(600, y0, 700, y1, cg))
pr("class modal:", modal(615, 165, 675, 200, cg))
pr("class ink r1:", bbox(600, 160, 700, 210, dark))

# ---- block arrows i/j ----
lav = lambda r, g, b: 190 <= r <= 235 and 190 <= g <= 240 and b > 230
pgreen = lambda r, g, b: 170 <= r <= 225 and g > 215 and 130 <= b <= 200
pr("== i arrow (lavender-ish fill D9E2F3) ==")
blueish = lambda r, g, b: 200 <= r <= 240 and 215 <= g <= 245 and b > 235
pr("  i fill bbox:", bbox(230, 365, 300, 415, blueish))
pr("  j fill bbox:", bbox(395, 365, 465, 415, pgreen))
pr("  j modal:", modal(410, 385, 445, 400, pgreen))
pr("== callouts ==")
pr("  prev bbox:", bbox(200, 380, 330, 445, lav))
pr("  prev modal:", modal(230, 395, 300, 425, lav))
pr("  curr bbox:", bbox(370, 380, 490, 445, pgreen))
pr("  curr modal:", modal(390, 395, 460, 425, pgreen))
pr("  prev ink:", bbox(200, 380, 330, 445, dark))
pr("  curr ink:", bbox(370, 380, 490, 445, dark))

# ---- equation boxes (cream) ----
cream = lambda r, g, b: r > 235 and g > 235 and 150 < b < 225
pr("== cream row extents ==")
for y in [450, 460, 475, 490, 500]:
    xs = [x for x in range(40, 920) if cream(*P[x, y])]
    if xs: pr(f"  y{y}: {min(xs)}..{max(xs)} n={len(xs)}")
# find box column runs at mid height
y = 475
runs, cur = [], None
for x in range(40, 920):
    if cream(*P[x, y]):
        if cur is None: cur = x
    else:
        if cur is not None and x - cur > 20: runs.append((cur, x - 1))
        cur = None
if cur: runs.append((cur, 919))
pr("  cream runs at y475:", runs)
for (bx0, bx1) in runs:
    ys = [yy for yy in range(430, 525) for x in range(bx0, bx1 + 1, 4) if cream(*P[x, yy])]
    pr(f"  box {bx0}..{bx1}: y {min(ys)}..{max(ys)}")
    pr(f"    ink bbox:", bbox(bx0, 435, bx1, 520, dark))
pr("cream modal:", modal(90, 460, 240, 495, cream))

# ---- footer bar ----
blk = lambda r, g, b: r < 60 and g < 60 and b < 60
pr("== footer ==", bbox(20, 505, 940, 540, blk))

# ---- chrome spot check (badge/rule present in frame?) ----
yel = lambda r, g, b: r > 220 and g > 220 and b < 170
pr("badge yellow bbox:", bbox(860, 40, 930, 105, yel))

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("WROTE", OUT)
