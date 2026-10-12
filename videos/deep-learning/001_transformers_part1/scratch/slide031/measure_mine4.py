#!/usr/bin/env python3
"""Final precision pass for slide_031.jpg build geometry."""
from PIL import Image
from collections import Counter

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()
def c(x, y): return px[x, y]

def bb(pred, x0, y0, x1, y1):
    xs = []; ys = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(c(x, y)):
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None
def rep(name, b):
    if b is None: print(f"  {name}: NONE"); return
    print(f"  {name}: x {b[0]}..{b[2]} y {b[1]}..{b[3]} w={b[2]-b[0]+1} h={b[3]-b[1]+1} n={b[4]}")

isw = lambda cc: cc[0] > 244 and cc[1] > 244 and cc[2] > 244
pred_red = lambda cc: cc[0] > 120 and cc[0] - cc[1] > 50 and cc[0] - cc[2] > 50
pred_blue = lambda cc: cc[2] > 110 and cc[2] - cc[0] > 40 and cc[2] - cc[1] > 30
pred_grn = lambda cc: cc[1] > 85 and cc[1] - cc[0] > 20 and cc[1] - cc[2] > 20
pred_dark = lambda cc: sum(cc) < 350
pred_yel = lambda cc: cc[0] > 235 and cc[1] > 210 and cc[2] < 175

print("=== 1. INPUT PILLS (outline scan: strongly-saturated stroke rows near pill) ===")
# Q pill: find its outline — scan for vertical strokes in x60..230
for x in range(60, 235):
    ys = [y for y in range(120, 180) if sum(c(x, y)) < 480 and not isw(c(x, y))]
    if len(ys) > 30:
        mc = tuple(round(sum(cc[i] for cc in (c(x, y) for y in ys)) / len(ys)) for i in range(3))
        print(f"  Q pill stroke col x={x}: n={len(ys)} y {min(ys)}..{max(ys)} mean={mc}")
# pill vertical extent at its mid x
x = 150
ys = [y for y in range(115, 185) if sum(c(x, y)) < 480 and not isw(c(x, y))]
print(f"  Q pill extent at x=150: y {min(ys)}..{max(ys)}")
# circles inside Q pill: dark-red ring bboxes — scan 4 windows
print("  Q pill circles (red rings):")
for i, (cx0, cx1) in enumerate([(78, 112), (112, 146), (146, 180), (180, 214)]):
    rep(f"circle{i+1}", bb(pred_red, cx0, 125, cx1, 180))
print("  Q pill fill sample:", c(100, 135), c(210, 160), c(95, 168))
print("  Q brackets: [ at?", bb(pred_red, 78, 130, 95, 175), "] at?", bb(pred_red, 200, 130, 220, 175))

print("\n=== 2. MATRIX CONTAINERS ===")
def container(x0, x1, y0, y1, label):
    # non-white, non-ink bounds
    xs = []; ys = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            cc = c(x, y)
            if not isw(cc) and sum(cc) > 380:
                xs.append(x); ys.append(y)
    print(f"  {label}: x {min(xs)}..{max(xs)} y {min(ys)}..{max(ys)} w={max(xs)-min(xs)+1} h={max(ys)-min(ys)+1}")
    return min(xs), min(ys), max(xs), max(ys)
qC = container(196, 420, 108, 300, "Q container")
vC = container(618, 835, 108, 300, "V container")
kC = container(196, 420, 325, 515, "K container")
print("  container fills:", "Q", c(240, 160), c(300, 250), "V", c(660, 160), c(720, 250), "K", c(240, 380), c(300, 470))
print("  grid line color:", "Q", c(258, 156), "V", c(678, 156), "K", c(258, 373))
# chip fill + text core colors per row
def rowtext(x0, x1, y0, y1, label):
    reds = blues = grns = mag = ors = darks = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            cc = c(x, y)
            r, g, b = cc
            if b > 100 and b - r > 50 and b - g > 40: blues += 1
            elif r > 100 and r - b > 60 and g < 100: mag += 1
            elif r > 100 and g > 60 and g < 140 and b < 60: ors += 1
            elif g > 90 and g - r > 30 and g - b > 30: grns += 1
            elif pred_red(cc): reds += 1
            elif sum(cc) < 300: darks += 1
    print(f"  {label}: blue={blues} magenta={mag} orange={ors} green={grns} red={reds} dark={darks}")
print("  Q matrix row text classification:")
rowtext(220, 372, 125, 158, "Q r1")
rowtext(220, 372, 165, 200, "Q r2")
rowtext(220, 372, 210, 245, "Q r3")
rowtext(220, 372, 252, 288, "Q r4")
# chip bounds: pale-yellow
pred_chip = lambda cc: cc[0] > 238 and cc[1] > 213 and 145 < cc[2] < 215 and cc[0] - cc[2] > 40
print("  Q chips bbox:", bb(pred_chip, 196, 108, 420, 300))
print("  V chips bbox:", bb(pred_chip, 618, 108, 835, 300))
print("  K chips bbox:", bb(pred_chip, 196, 325, 420, 515))

print("\n=== 3. MATRIX SIDE LABELS ===")
rep("Q X2 (red big)", bb(pred_red, 60, 175, 200, 240))
rep("Q 1xd", bb(lambda cc: sum(cc) < 420, 100, 175, 210, 200))
rep("V X2 (red big)", bb(pred_red, 480, 175, 620, 240))
rep("V 1xd", bb(lambda cc: sum(cc) < 420, 520, 175, 630, 200))
rep("K X2 (red big)", bb(pred_red, 60, 390, 200, 455))
rep("K 1xd", bb(lambda cc: sum(cc) < 420, 100, 390, 210, 415))
rep("Q W_Q", bb(pred_red, 200, 245, 340, 300))
rep("V W_V", bb(pred_red, 620, 245, 760, 300))
rep("K W_K", bb(pred_red, 200, 460, 340, 515))
rep("Q dxd", bb(lambda cc: sum(cc) < 420, 330, 245, 420, 300))
rep("V dxd", bb(lambda cc: sum(cc) < 420, 750, 245, 840, 300))
rep("K dxd", bb(lambda cc: sum(cc) < 420, 330, 460, 420, 515))
print("  label core colors: Q X2", c(130, 190), "Q 1xd", c(200, 183), "Q W_Q", c(210, 255), "Q dxd", c(360, 265), "V W_V", c(630, 255), "V dxd", c(780, 262), "K W_K", c(210, 470), "K dxd", c(360, 480))
rep("Q equals", bb(pred_red, 378, 180, 408, 230))
rep("V equals", bb(pred_red, 795, 180, 825, 230))
rep("K equals", bb(pred_red, 378, 395, 408, 445))
print("  equals sample:", c(393, 200), c(393, 207), c(810, 200), c(393, 415))
rep("Q role Q", bb(pred_red, 400, 88, 460, 118))
rep("V role V", bb(pred_blue, 795, 88, 860, 118))
rep("K role K", bb(pred_grn, 400, 300, 460, 332))

print("\n=== 4. OUTPUT CAPSULES ===")
for (x0, x1, y0, y1, lbl) in [(405, 462, 112, 302, "Q"), (822, 880, 112, 302, "V"), (405, 462, 330, 512, "K")]:
    # outline strokes
    cols = []
    for x in range(x0 - 4, x1 + 5):
        ys = [y for y in range(y0, y1) if pred_red(c(x, y))]
        if len(ys) > (y1 - y0) * 0.5: cols.append((x, len(ys), min(ys), max(ys)))
    print(f"  {lbl} outcap red-outline cols: {cols}")
    # fill
    fills = Counter()
    for y in range(y0, y1, 2):
        for x in range(x0, x1, 2):
            cc = c(x, y)
            if not isw(cc): fills[(cc[0] // 24 * 24, cc[1] // 24 * 24, cc[2] // 24 * 24)] += 1
    print(f"  {lbl} outcap fills: {fills.most_common(4)}")
    # chip bboxes (pale-yellow)
    rep(f"{lbl} chips", bb(pred_chip, x0 - 2, y0 - 2, x1 + 3, y1 + 3))
# chip rows within Q outcap: yellow runs at x=430
runs = []; inw = False; start = 0
for y in range(108, 305):
    t = pred_chip(c(430, y))
    if t and not inw: inw = True; start = y
    elif not t and inw:
        inw = False
        if y - start > 8: runs.append((start, y - 1))
print("  Q outcap chip rows at x=430:", runs)
runs = []; inw = False
for y in range(325, 515):
    t = pred_chip(c(430, y))
    if t and not inw: inw = True; start = y
    elif not t and inw:
        inw = False
        if y - start > 8: runs.append((start, y - 1))
print("  K outcap chip rows at x=430:", runs)
runs = []; inw = False
for y in range(108, 305):
    t = pred_chip(c(850, y))
    if t and not inw: inw = True; start = y
    elif not t and inw:
        inw = False
        if y - start > 8: runs.append((start, y - 1))
print("  V outcap chip rows at x=850:", runs)
# chip cols
runs = []; inw = False
for x in range(405, 465):
    t = pred_chip(c(x, 140))
    if t and not inw: inw = True; start = x
    elif not t and inw:
        inw = False
        if x - start > 8: runs.append((start, x - 1))
if inw: runs.append((start, 464))
print("  Q outcap chip cols at y=140:", runs)

print("\n=== 5. CALLOUTS ===")
for (x0, x1, y0, y1, lbl) in [(438, 695, 265, 322, "callout1"), (692, 928, 298, 352, "callout2"), (438, 695, 326, 382, "callout3")]:
    rep(lbl + " any-ink", bb(lambda cc: not isw(cc) and sum(cc) < 690, x0, y0, x1, y1))
    # fill = modal non-white color in center
    fills = Counter()
    for y in range(y0 + 6, y1 - 6, 2):
        for x in range(x0 + 6, x1 - 6, 2):
            cc = c(x, y)
            if not isw(cc): fills[(cc[0] // 20 * 20, cc[1] // 20 * 20, cc[2] // 20 * 20)] += 1
    print(f"    fills: {fills.most_common(5)}")
    # border color votes (outer ring band)
    votes = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            cc = c(x, y)
            r, g, b = cc
            if r > 120 and r - g > 55 and r - b > 55: votes["red"] += 1
            elif b > 110 and b - r > 45 and b - g > 30: votes["blue"] += 1
            elif g > 80 and g - r > 25 and g - b > 25: votes["green"] += 1
            elif sum(cc) < 340: votes["dark"] += 1
    print(f"    border votes: {dict(votes)}")

print("\n=== 6. YELLOW + NOTE BOX ===")
rep("yellow box", bb(pred_yel, 600, 370, 940, 450))
print("  yellow sample:", c(700, 395), c(800, 420))
rep("emphasis text (red)", bb(pred_red, 650, 375, 900, 445))
rep("note box ink", bb(lambda cc: not isw(cc) and sum(cc) < 690, 440, 440, 935, 535))
print("  note border sample rows: y449", c(700, 449), " y518", c(700, 518), " x491", c(491, 480), " x903", c(903, 480))
rep("note text blue", bb(pred_blue, 445, 445, 930, 530))
rep("note text red", bb(pred_red, 445, 445, 930, 530))

print("\n=== 7. TITLE / SUBTITLE / BADGE ===")
rep("title ink (no badge)", bb(pred_dark, 60, 44, 860, 70))
rep("title highlight", bb(pred_yel, 60, 40, 860, 80))
rep("subtitle ink (no badge)", bb(lambda cc: sum(cc) < 620, 60, 71, 860, 93))
rep("subtitle red", bb(pred_red, 60, 71, 860, 93))
print("  subtitle red x-clusters:")
sred = sorted(set(x for x in range(60, 870) for y in range(71, 93) if pred_red(c(x, y))))
runs = []
if sred:
    s = p = sred[0]
    for x in sred[1:]:
        if x - p > 8: runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
print("   ", runs)
print("  badge check (should be house):", bb(pred_yel, 860, 50, 925, 95))

print("\n=== 8. PEACH EDGES refine ===")
for row in (150, 300, 450, 520):
    xs = [x for x in range(30, W) if 235 <= c(x, row)[0] <= 258 and c(x, row)[0] - c(x, row)[2] > 22 and c(x, row)[0] - c(x, row)[1] > 10]
    if xs: print(f"  row{row}: peach x {min(xs)}..{max(xs)}")
for col in (60, 480, 890):
    ys = [y for y in range(70, H) if 235 <= c(col, y)[0] <= 258 and c(col, y)[0] - c(col, y)[2] > 22 and c(col, y)[0] - c(col, y)[1] > 10]
    if ys: print(f"  col{col}: peach y {min(ys)}..{max(ys)}")
