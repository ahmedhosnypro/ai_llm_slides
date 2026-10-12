#!/usr/bin/env python3
"""V/K precise geometry: matrix gutters, capsules, outcaps, pills."""
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_031.jpg").convert("RGB")
W, H = im.size
px = im.load()

def gaps_row(y, x0, x1, minw=1):
    out = []; inrun = False; s = 0
    for x in range(x0, x1):
        c = px[x, y]
        w = c[0] > 240 and c[1] > 240 and c[2] > 240
        if w and not inrun: inrun = True; s = x
        elif not w and inrun:
            inrun = False
            if x - s >= minw: out.append((s, x - 1))
    if inrun: out.append((s, x1 - 1))
    return out

def gaps_col(x, y0, y1, minw=1):
    out = []; inrun = False; s = 0
    for y in range(y0, y1):
        c = px[x, y]
        w = c[0] > 240 and c[1] > 240 and c[2] > 240
        if w and not inrun: inrun = True; s = y
        elif not w and inrun:
            inrun = False
            if y - s >= minw: out.append((s, y - 1))
    if inrun: out.append((s, y1 - 1))
    return out

print("== V matrix gutters ==")
for y in [140, 145, 210, 215, 250]:
    print(f"  y={y} white gaps x615..800:", gaps_row(y, 615, 800))
for x in [640, 700, 760]:
    print(f"  x={x} white gaps y112..295:", gaps_col(x, 112, 295))

print("== K matrix gutters ==")
for y in [378, 380, 418, 420, 458]:
    print(f"  y={y} white gaps x215..385:", gaps_row(y, 215, 385))
for x in [240, 300, 360]:
    print(f"  x={x} white gaps y328..512:", gaps_col(x, 328, 512))

print("== Q matrix re-verify (clean gutter row) ==")
for y in [152, 153, 193, 235]:
    print(f"  y={y} white gaps x215..380:", gaps_row(y, 215, 380))

print("== V outcap ==")
def strokes(p, x0, x1, y0, y1, minn):
    out = []
    for x in range(x0, x1):
        n = sum(1 for y in range(y0, y1) if p(px[x, y]))
        if n >= minn: out.append((x, n))
    return out
blue = lambda c: c[2] > 120 and c[2] - c[0] > 40 and c[2] - c[1] > 30
red = lambda c: c[0] > 120 and c[0] - c[1] > 50 and c[0] - c[2] > 50
green = lambda c: c[1] > 100 and c[1] - c[0] > 30 and c[1] - c[2] > 30
print("  blue strokes x800..895 (y120..280):", strokes(blue, 800, 895, 120, 280, 60))
for x in [822, 840, 856]:
    print(f"  x={x} nonwhite runs y110..295:", gaps_col(x, 110, 295, 99)[:2], "...")
print("  V outcap tiles (cream) rows: col x=835 gaps:")
print("   ", gaps_col(835, 115, 290, 3))

print("== K outcap ==")
print("  green strokes x400..470 (y330..500):", strokes(green, 400, 470, 330, 500, 60))
for x in [418, 435, 450]:
    print(f"  x={x} white gaps y325..515:", gaps_col(x, 325, 515, 3))

print("== V pill: red verticals x480..640 (y130..175) ==")
print(" ", strokes(red, 480, 640, 130, 175, 8))
print("== V pill nonwhite row extents ==")
for y in [140, 155, 170]:
    xs = [x for x in range(475, 640) if sum(px[x, y]) < 720 or (px[x, y][0] > 240 and px[x, y][1] < 230)]
    print(f"  y={y}: ink x {min(xs) if xs else '-'}..{max(xs) if xs else '-'} n={len(xs)}")

print("== K pill: red verticals x55..215 (y345..395) ==")
print(" ", strokes(red, 55, 215, 345, 395, 8))
print("== K pill nonwhite row extents ==")
for y in [355, 370, 385]:
    xs = [x for x in range(50, 220) if sum(px[x, y]) < 720 or (px[x, y][0] > 240 and px[x, y][1] < 230)]
    print(f"  y={y}: ink x {min(xs) if xs else '-'}..{max(xs) if xs else '-'} n={len(xs)}")

print("== Q pill: red verticals x60..215 (y132..175) ==")
print(" ", strokes(red, 60, 215, 132, 175, 8))

print("== capsule pill fills (mode-ish samples) ==")
print("  Q pill interior between circles:", [px[x, y] for x, y in [(105, 143), (130, 162), (155, 143), (180, 160)]])
print("  Q pill outline:", [px[x, y] for x, y in [(137, 137), (137, 169), (72, 152), (204, 152)]])
print("  V pill outline:", [px[x, y] for x, y in [(555, 137), (555, 169), (490, 152), (618, 152)]])
print("  circle fills Q:", [px[x, y] for x, y in [(96, 152), (121, 152), (146, 152), (171, 152)]])
print("  V outcap fill:", [px[x, y] for x, y in [(830, 160), (845, 200), (838, 250)]])
print("  K outcap fill:", [px[x, y] for x, y in [(428, 375), (443, 415), (433, 465)]])
print("  K matrix bg:", [px[x, y] for x, y in [(224, 345), (259, 420), (375, 480), (300, 500)]])
print("  V matrix bg:", [px[x, y] for x, y in [(626, 130), (661, 215), (788, 260), (700, 285)]])
print("  tile fills:", [px[x, y] for x, y in [(240, 140), (276, 140), (312, 140), (348, 140), (700, 140), (736, 140), (240, 355), (348, 355)]])
print("  V outcap tiles:", [px[x, y] for x, y in [(832, 140), (846, 140), (832, 178), (846, 178)]])
print("  K outcap tiles:", [px[x, y] for x, y in [(425, 355), (443, 355), (425, 395), (443, 395)]])

print("== V/K label zones (red means) ==")
def mean_in(x0, y0, x1, y1, keep, label):
    tot = [0, 0, 0]; n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if keep(c):
                for i in range(3): tot[i] += c[i]
                n += 1
    if n: 
        m = tuple(t // n for t in tot)
        print(f"  {label}: #{m[0]:02X}{m[1]:02X}{m[2]:02X} n={n}")
    else:
        print(f"  {label}: none")
mean_in(592, 172, 622, 188, lambda c: sum(c) < 400, "V '1xd' zone")
mean_in(505, 180, 545, 215, lambda c: sum(c) < 400, "V 'X2' zone")
mean_in(585, 225, 625, 260, lambda c: sum(c) < 400, "V 'W_V' zone")
mean_in(172, 429, 212, 458, lambda c: sum(c) < 400, "K 'W_K' zone")
mean_in(105, 380, 145, 415, lambda c: sum(c) < 400, "K 'X2' zone")
print("== V/K role letters ==")
mean_in(815, 96, 850, 116, lambda c: sum(c) < 500, "V role 'V'")
mean_in(412, 308, 448, 332, lambda c: sum(c) < 500, "K role 'K'")
print("== V/K '=' ==")
mean_in(795, 195, 825, 215, lambda c: sum(c) < 400, "V '='")
mean_in(385, 392, 415, 412, lambda c: sum(c) < 400, "K '='")
print("== badge numeral zone ==")
mean_in(878, 58, 908, 86, lambda c: sum(c) < 400, "badge numeral ink")
