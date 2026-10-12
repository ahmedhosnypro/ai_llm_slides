#!/usr/bin/env python3
"""measure6.py — slide 025 closing pass: panel rect, output arrows, rings right,
Sigmas, Net labels, callout/arrow borders, outbox/class borders, dash, IS/SL,
eq box borders, error bar. Banked as measure6_out.txt."""
from collections import Counter
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide025/measure6_out.txt"
im = Image.open(SRC).convert("RGB")
W, H = im.size
P = im.load()
L = []
def pr(*a):
    s = " ".join(str(x) for x in a); L.append(s); print(s)
def bbox(x0, y0, x1, y1, pred):
    x1 = min(x1, W-1); y1 = min(y1, H-1)
    xs, ys = [], []
    for y in range(y0, y1+1):
        for x in range(x0, x1+1):
            if pred(*P[x, y]): xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None

beige = lambda r, g, b: 205 <= r <= 235 and 195 <= g <= 225 and 175 <= b <= 210
red = lambda r, g, b: r > 130 and g < 80 and b < 80
darkred = lambda r, g, b: 100 <= r <= 190 and g < 60 and b < 60
mags = lambda r, g, b: r > 200 and 100 < g < 200 and b > 200      # FF99FF-ish fill
magd = lambda r, g, b: 120 <= r <= 200 and g < 110 and 120 <= b <= 200  # dark magenta 990099/CC00CC-ish
violet = lambda r, g, b: 120 <= r <= 190 and 100 <= g <= 160 and 180 <= b <= 230  # 9080C8
lavb = lambda r, g, b: 120 <= r <= 170 and 130 <= g <= 180 and 170 <= b <= 215    # 8E96BC border
grnb = lambda r, g, b: 100 <= r <= 150 and 145 <= g <= 190 and 70 <= b <= 120     # 7FA85E border
lavf = lambda r, g, b: 205 <= r <= 240 and 220 <= g <= 245 and b > 238            # D9E2F3/DEEBF3 fill
grnf = lambda r, g, b: 185 <= r <= 235 and g >= 245 and 150 <= b <= 205           # C9E3A8/DDFFB8 fill
clsfill = lambda r, g, b: 210 <= r <= 240 and g > 245 and 190 <= b <= 220         # E3FFCF
tanbrd = lambda r, g, b: r < 205 and g < 205 and b < 190                          # eq box dark-tan border
grayring = lambda r, g, b: 60 <= r <= 160 and 60 <= g <= 160 and 60 <= b <= 160

# 1) panel rect: beige row extents at clean rows + column extent at x300
pr("== panel ==")
for y in [137, 140, 200, 300, 370, 383, 385, 386]:
    xs = [x for x in range(40, 760) if beige(*P[x, y])]
    pr(f"  y{y}: {min(xs) if xs else None}..{max(xs) if xs else None} n={len(xs)}")
ys = [y for y in range(100, 420) if beige(*P[300, y])]
pr(f"  x300 col: {min(ys)}..{max(ys)} n={len(ys)}")

# 2) output arrows: red px x448..503 per row
pr("== output arrows (red x448..503) ==")
for cy in [181, 254, 336]:
    pts = [(x, y) for y in range(cy-6, cy+7) for x in range(446, 504) if red(*P[x, y]) or darkred(*P[x, y])]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        pr(f"  cy{cy}: n={len(pts)} bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
    else:
        pr(f"  cy{cy}: none")

# 3) rings between green col and outboxes (gray strokes x452..500)
pr("== rings x450..500 per row ==")
for cy in [181, 254, 336]:
    cols = sorted({x for y in range(cy-8, cy+9) for x in range(450, 502) if grayring(*P[x, y])})
    pr(f"  cy{cy}: {cols[:24]}")

# 4) Sigma presence: red components in left halves
pr("== Sigma red components per neuron ==")
for (x0, x1, cy, tag) in [(138, 182, 181, "col0r1"), (240, 284, 181, "col1r1"),
                          (405, 449, 181, "col2r1"), (138, 182, 336, "col0r3")]:
    pts = [(x, y) for y in range(cy-17, cy+18) for x in range(x0, x1+1) if red(*P[x, y])]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        pr(f"  {tag}: n={len(pts)} bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
    else:
        pr(f"  {tag}: none")

# 5) Net labels: red components
pr("== Net labels ==")
for (x0, y0, x1, y1, tag) in [(195, 130, 270, 200, "Net_i zone"), (355, 130, 430, 210, "Net_j zone")]:
    pts = [(x, y) for y in range(y0, y1+1) for x in range(x0, x1+1) if red(*P[x, y])]
    seen, comps = set(), []
    for p in pts:
        if p in seen: continue
        stack, comp = [p], []
        seen.add(p)
        while stack:
            cx, cy = stack.pop(); comp.append((cx, cy))
            for dx in (-2, -1, 0, 1, 2):
                for dy in (-2, -1, 0, 1, 2):
                    q = (cx+dx, cy+dy)
                    if q not in seen and q in pts:
                        seen.add(q); stack.append(q)
        comps.append(comp)
    for c in sorted(comps, key=len, reverse=True)[:5]:
        xs = [p[0] for p in c]; ys = [p[1] for p in c]
        pr(f"  {tag}: n={len(c)} bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")

# 6) callout + block arrow borders/fills
pr("== callouts/arrows ==")
pr("  prev border:", bbox(200, 390, 330, 445, lavb))
pr("  curr border:", bbox(370, 390, 490, 445, grnb))
pr("  i arrow outline:", bbox(225, 355, 315, 400, lambda r, g, b: lavb(r, g, b) and (b - r) > 30))
pr("  i arrow fill:", bbox(225, 355, 315, 399, lavf))
pr("  j arrow fill:", bbox(380, 355, 480, 399, grnf))
pr("  j arrow outline:", bbox(380, 355, 480, 400, lambda r, g, b: grnb(r, g, b) and (g - r) > 25))
pr("  k arrow? fill (tan):", bbox(540, 355, 640, 400, lambda r, g, b: 225 <= r <= 250 and 190 <= g <= 225 and 130 <= b <= 175))
pr("  next callout? (tan):", bbox(540, 420, 650, 470, lambda r, g, b: 225 <= r <= 250 and 190 <= g <= 225 and 130 <= b <= 175))

# 7) outboxes violet borders
pr("== outboxes (violet border bbox) ==")
for (y0, y1) in [(165, 200), (238, 273), (320, 355)]:
    pr(f"  y{y0}:", bbox(490, y0, 575, y1, violet))

# 8) class boxes: fill bbox rows 1-3
pr("== class boxes (fill) ==")
for (y0, y1) in [(165, 200), (238, 273), (320, 355)]:
    pr(f"  y{y0}:", bbox(595, y0, 700, y1, clsfill))

# 9) dash line
pr("== dash line (dark magenta y100..125) ==")
pts = [(x, y) for y in range(100, 126) for x in range(100, 610) if magd(*P[x, y])]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    pr(f"  n={len(pts)} bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
    rows = Counter(p[1] for p in pts)
    pr("  top rows:", sorted(rows.items())[:6])

# 10) IS/SL magenta fills
pr("== IS/SL fills ==")
pr("  IS fill:", bbox(45, 75, 175, 145, mags))
pr("  SL fill:", bbox(580, 75, 690, 145, mags))

# 11) eq boxes: tan border bboxes + border color
pr("== eq boxes (tan border) ==")
for (x0, x1, tag) in [(55, 275, "box1"), (276, 525, "box2"), (526, 780, "box3")]:
    bb = bbox(x0, 438, x1, 517, tanbrd)
    pr(f"  {tag}:", bb)
cnt = Counter(P[x, y] for y in range(455, 505) for x in range(70, 250) if tanbrd(*P[x, y]))
pr("  box1 border modal:", cnt.most_common(5))

# 12) error bar
pr("== error bar (dark red) ==")
pr("  ", bbox(570, 140, 615, 375, darkred))

# 13) black bar top row
for y in range(512, 524):
    row = [x for x in range(40, 920) if sum(P[x, y]) < 200]
    if len(row) > 400:
        pr(f"== black bar first full row: {y} (n={len(row)}, {min(row)}..{max(row)})"); break

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("WROTE", OUT)
