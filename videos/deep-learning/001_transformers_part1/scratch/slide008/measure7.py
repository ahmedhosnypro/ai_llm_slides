#!/usr/bin/env python3
"""Pass 7: leader colors + endpoints; verify absence in slide 6; title column-run shift check."""
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
im = Image.open(BASE + "unique_slides/slide_008.jpg").convert("RGB")
im6 = Image.open(BASE + "unique_slides/slide_006.jpg").convert("RGB")
ld, ld6 = im.load(), im6.load()

def anyink(p):
    r, g, b = p
    return not (r > 243 and g > 243 and b > 243)

# 1. leader pixel colors
print("leader samples:")
for (x, y, tag) in [(207, 298, "vert1"), (368, 296, "vert2"), (400, 280, "callout-leader"),
                    (354, 276, "wait2-diag"), (375, 253, "callout-leader-mid"), (430, 305, "leader-low")]:
    print(f"  ({x},{y}) {tag}: {ld[x, y]}  s6: {ld6[x, y]}")

# 2. verticals inside encoder band (y 306..328) — blue against peach
print("vert1 in encoder band x200..214:")
for y in (310, 315, 320, 325):
    row = [x for x in range(198, 216) if ld[x, y][2] - ld[x, y][0] > 25]
    print(f"  y={y}: {row}")
print("vert2 in encoder band x360..376:")
for y in (310, 315, 320, 325):
    row = [x for x in range(358, 378) if ld[x, y][2] - ld[x, y][0] > 25]
    print(f"  y={y}: {row}")

# 3. absence check in slide 6: region x 180..470, y 250..305 (above encoder) — any ink?
cnt6 = sum(1 for y in range(250, 305) for x in range(180, 470) if anyink(ld6[x, y]))
cnt8 = sum(1 for y in range(250, 305) for x in range(180, 470) if anyink(ld[x, y]))
print(f"ink count x180..470 y250..305: s6={cnt6} s8={cnt8}")
# slide 6: what IS in the leader corridor x330..470 y 210..300?
cnt6b = sum(1 for y in range(210, 300) for x in range(330, 470) if anyink(ld6[x, y]))
print(f"s6 ink x330..470 y210..300: {cnt6b}")

# 4. wait1 diagonal connector? window x 180..210, y 270..294
print("wait1 connector window (x180..212, y268..296):")
for y in range(268, 296):
    row = [x for x in range(180, 212) if anyink(ld[x, y])]
    if row:
        print(f"  y={y}: {min(row)}..{max(row)} n={len(row)}")

# 5. title column runs (word-level) s8 vs s6, band y 55..85
def col_runs(img, x0, x1, y0, y1, pred, gap=6):
    ld_ = img.load()
    cols = [x for x in range(x0, x1) if any(pred(ld_[x, y]) for y in range(y0, y1))]
    runs, s, prev = [], None, -99
    for x in cols:
        if x - prev > gap:
            if s is not None: runs.append((s, prev))
            s = x
        prev = x
    if s is not None: runs.append((s, prev))
    return runs

def redink(p):
    r, g, b = p
    return r > 120 and r - g > 60 and r - b > 60

r8 = col_runs(im, 250, 700, 55, 85, redink)
r6 = col_runs(im6, 250, 700, 55, 85, redink)
print("s8 title word runs:", r8)
print("s6 title word runs:", r6)
if len(r8) == len(r6):
    print("per-run shift:", [ (a[0]-b[0], a[1]-b[1]) for a, b in zip(r8, r6) ])

# 6. (Challenges) COM
def com(img, pred, x0, y0, x1, y1):
    ld_ = img.load()
    sx = sy = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(ld_[x, y]):
                sx += x; sy += y; n += 1
    return (round(sx/n,1), round(sy/n,1), n) if n else None

def blueink(p):
    r, g, b = p
    return b > 110 and b - r > 40 and g < 140

print("(Challenges) com:", com(im, blueink, 300, 80, 620, 118))
print("(Challenges) col runs:", col_runs(im, 300, 620, 85, 113, blueink, gap=8))
# challenges row profile for font size (cap rows vs paren extent)
rows = [(y, sum(1 for x in range(370, 540) if blueink(ld[x, y]))) for y in range(84, 116)]
print("challenges rows:", [r for r in rows if r[1]])
