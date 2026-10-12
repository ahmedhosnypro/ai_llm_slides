#!/usr/bin/env python3
"""measure5.py — component-cluster pass for w_ji labels, tight arrow/callout/eqbox bounds,
border color samples. Banked as measure5_out.txt."""
from collections import Counter
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide025/measure5_out.txt"
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
blue = lambda r, g, b: b > 130 and r < 110 and g < 110
darkish = lambda r, g, b: r < 150 and g < 150 and b < 150
bluish = lambda r, g, b: 195 <= r <= 245 and 210 <= g <= 248 and b > 240
grn = lambda r, g, b: 170 <= r <= 228 and g > 230 and 130 <= b <= 210
lav = lambda r, g, b: 195 <= r <= 240 and 200 <= g <= 245 and b > 240
grn2 = lambda r, g, b: 190 <= r <= 240 and g > 235 and 150 <= b <= 220

# 1) w_ji labels: connected components of blue px in x310..370, y155..270
pr("== w_ji components ==")
pts = [(x, y) for y in range(150, 275) for x in range(305, 375) if blue(*P[x, y])]
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
for c in sorted(comps, key=len, reverse=True)[:6]:
    xs = [p[0] for p in c]; ys = [p[1] for p in c]
    pr(f"  n={len(c)} bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)}) center=({(min(xs)+max(xs))/2},{(min(ys)+max(ys))/2})")

# 2) O labels: components of red px near col rims (exclude mesh lines via y bands)
tred = lambda r, g, b: r > 130 and g < 90 and b < 90
pr("== O label components (x268..310, per row) ==")
for (y0, y1) in [(158, 200), (231, 273), (313, 355)]:
    pts = [(x, y) for y in range(y0, y1) for x in range(266, 312) if tred(*P[x, y])]
    if not pts: pr(f"  y{y0}: none"); continue
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    pr(f"  y{y0}: bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")
pr("== O_j components (x436..480) ==")
for (y0, y1) in [(158, 200), (231, 273), (313, 355)]:
    pts = [(x, y) for y in range(y0, y1) for x in range(436, 482) if tred(*P[x, y])]
    if not pts: pr(f"  y{y0}: none"); continue
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    pr(f"  y{y0}: bbox=({min(xs)},{min(ys)},{max(xs)},{max(ys)})")

# 3) tight block arrows + callouts
pr("== arrows tight ==")
pr("  i fill:", bbox(240, 362, 290, 400, bluish))
pr("  j fill:", bbox(408, 362, 458, 400, grn))
pr("== callouts tight ==")
pr("  prev fill:", bbox(205, 396, 320, 444, lav))
pr("  curr fill:", bbox(375, 396, 485, 444, grn2))
# text ink inside callouts
pr("  prev text:", bbox(210, 400, 315, 440, darkish))
pr("  curr text:", bbox(380, 400, 480, 440, darkish))

# 4) eq boxes: border ring color sample + exact bounds via 'not gray panel' fill
notpanel = lambda r, g, b: not (225 <= r <= 245 and 225 <= g <= 245 and 220 <= b <= 240)
pr("== eq boxes: fill(bright cream) bounds ==")
cream2 = lambda r, g, b: r >= 246 and g >= 246 and b >= 225 and b <= 248
for (x0, x1, tag) in [(60, 285, "box1"), (285, 525, "box2"), (525, 790, "box3")]:
    pr(f"  {tag}:", bbox(x0, 438, x1, 518, cream2))
# border sample: darkest px on box1 perimeter band
pr("  box1 border px sample:", [P[x, 470] for x in range(74, 84)])
pr("  box1 top rows (x150):", [(y, P[150, y]) for y in range(452, 462)])
pr("  box1 bottom rows (x150):", [(y, P[150, y]) for y in range(498, 510)])
pr("  box2 top rows (x400):", [(y, P[400, y]) for y in range(452, 464)])
pr("  box2 left cols (y470):", [(x, P[x, 470]) for x in range(290, 302)])
pr("  box3 left cols (y470):", [(x, P[x, 470]) for x in range(530, 545)])
pr("  box3 right cols (y470):", [(x, P[x, 470]) for x in range(755, 770)])

# 5) IS/SL border samples
pr("== IS border rows (x95) ==")
pr("  ", [(y, P[95, y]) for y in range(90, 100)], [(y, P[95, y]) for y in range(122, 130)])
pr("== SL border rows (x638) ==")
pr("  ", [(y, P[638, y]) for y in range(90, 100)], [(y, P[638, y]) for y in range(120, 128)])
pr("== IS left cols (y110) ==", [(x, P[x, 110]) for x in range(53, 64)])
pr("== SL right cols (y110) ==", [(x, P[x, 110]) for x in range(668, 680)])

# 6) class box border rows
pr("== class1 border rows (x640) ==")
pr("  ", [(y, P[640, y]) for y in range(168, 178)], [(y, P[640, y]) for y in range(186, 196)])
pr("== class1 left cols (y182) ==", [(x, P[x, 182]) for x in range(604, 616)])
pr("== class1 right cols (y182) ==", [(x, P[x, 182]) for x in range(668, 682)])

# 7) outbox border rows
pr("== outbox1 border rows (x530) ==")
pr("  ", [(y, P[530, y]) for y in range(170, 178)], [(y, P[530, y]) for y in range(186, 194)])
pr("== outbox1 left cols (y182) ==", [(x, P[x, 182]) for x in range(496, 506)])
pr("== outbox1 right cols (y182) ==", [(x, P[x, 182]) for x in range(558, 568)])

# 8) green rim port: px grid around (447..458, 177..187) row1
pr("== green rim row1 grid ==")
for y in range(176, 188):
    pr("  ", y, [P[x, y] for x in range(444, 458, 2)])

# 9) callout fills modal
pr("prev fill modal:", Counter(P[x, y] for y in range(405, 430) for x in range(225, 300) if lav(*P[x, y])).most_common(3))
pr("curr fill modal:", Counter(P[x, y] for y in range(405, 430) for x in range(390, 465) if grn2(*P[x, y])).most_common(3))
pr("i arrow fill modal:", Counter(P[x, y] for y in range(365, 395) for x in range(245, 280) if bluish(*P[x, y])).most_common(3))
pr("j arrow fill modal:", Counter(P[x, y] for y in range(365, 395) for x in range(415, 450) if grn(*P[x, y])).most_common(3))

with open(OUT, "w") as f:
    f.write("\n".join(L) + "\n")
print("WROTE", OUT)
