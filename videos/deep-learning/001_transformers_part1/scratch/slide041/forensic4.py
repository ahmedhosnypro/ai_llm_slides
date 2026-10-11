#!/usr/bin/env python3
"""Forensics 4: ASCII maps with color classes to resolve micro-structure."""
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
im = Image.open(ORIG).convert("RGB")
px = im.load()

def cls(c):
    r, g, b = c
    if r > 150 and g < 90 and b < 90: return "R"       # bright red
    if r > 140 and 60 <= g < 150 and b < 110 and r - b > 60: return "O"  # orange-red
    if r < 110 and g < 110 and b < 110: return "@"     # dark
    if b > 120 and b > r + 40 and b > g + 20: return "B"  # blue
    if g > 110 and g > r + 25 and g > b + 25: return "G"  # green
    if r > 120 and b > 120 and r + b > 2 * g + 40: return "P"  # purple
    if r > 200 and g > 180 and b < 140: return "Y"     # yellow
    if r > 190 and 130 < g < 210 and 150 < b < 225: return "p"  # pink
    if r > 180 and g < 120 and b > 140: return "m"     # magenta/pink-purple
    return "."

def mmap(name, x0, x1, y0, y1, step=1):
    print(f"== {name} x{x0}..{x1} y{y0}..{y1} (step {step}) ==")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1, step):
        row = "".join(cls(px[x, y]) for x in range(x0, x1, step))
        print(f"y{y:4d} {row}")

mmap("M1 SDPA stack", 290, 500, 344, 412)
mmap("M2 bottom Linears+circles", 318, 500, 390, 462)
mmap("M3 encoder circles", 622, 732, 388, 424)
mmap("M4 decoder upper (crossMHA/A&N/group)", 738, 845, 168, 290, 2)
mmap("M5 decoder mid (maskedMHA/circles)", 738, 845, 326, 420, 2)
mmap("M6 decoder low (embed/plus)", 738, 845, 408, 452, 2)
mmap("M7 encoder low (plus/embed/inputs)", 622, 735, 415, 515, 2)
mmap("M8 left schematic interior", 60, 196, 318, 470, 2)
mmap("M9 olive-rect top edge + corners", 292, 320, 240, 262)
print("   right-top corner:")
mmap("M9b", 496, 518, 240, 262)
print("== T1 ×h search: orange/dark px x455..525 y348..400:")
pts = [(x, y) for y in range(348, 400) for x in range(455, 526)
       if (px[x, y][0] > 140 and 40 < px[x, y][1] < 150 and px[x, y][2] < 120 and px[x, y][0] - px[x, y][2] > 50)
       or sum(px[x, y]) < 300]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
    from collections import Counter
    cc = Counter(f"#{px[x,y][0]//16*16:02X}{px[x,y][1]//16*16:02X}{px[x,y][2]//16*16:02X}" for x, y in pts)
    print("  colors:", cc.most_common(6))
else:
    print("  none")
print("== T2 zoom label bbox (orange-red) x300..520 y208..242:")
pts = [(x, y) for y in range(208, 243) for x in range(300, 521)
       if px[x, y][0] > 150 and 40 < px[x, y][1] < 150 and px[x, y][2] < 120 and px[x, y][0] - px[x, y][2] > 60]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
print("== T3 left label bbox (red) x25..200 y210..272:")
pts = [(x, y) for y in range(210, 273) for x in range(25, 201)
       if px[x, y][0] > 140 and px[x, y][1] < 110 and px[x, y][2] < 110]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
print("== T4 Encoder label bbox x575..700 y104..140; Decoder label search x740..890 y115..175:")
for (x0, x1, y0, y1, lbl) in ((575, 700, 104, 140, "Encoder"), (740, 890, 115, 175, "Decoder")):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1)
           if px[x, y][0] > 140 and px[x, y][1] < 110 and px[x, y][2] < 110]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        print(f"  {lbl}: n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
    else:
        print(f"  {lbl}: none")
print("== T7 decoder group bottom band colors x=800, y306..330:")
print("  ", [(y, f"#{px[800,y][0]:02X}{px[800,y][1]:02X}{px[800,y][2]:02X}") for y in range(306, 331)])
print("== T8 corner squares 6x6 grids:")
for (cx, cy, lbl) in ((302, 250, "TL"), (505, 250, "TR"), (302, 512, "BL"), (505, 512, "BR")):
    grid = []
    for y in range(cy - 4, cy + 5):
        row = "".join("O" if (px[x, y][1] > px[x, y][0] - 40 and px[x, y][0] < 190 and px[x, y][1] > 90 and px[x, y][2] < 120) else "." for x in range(cx - 5, cx + 6))
        grid.append(row)
    print(f"  {lbl} ({cx},{cy}):", grid)
print("== T9 Inputs text bbox (dark) x630..700 y493..515:")
pts = [(x, y) for y in range(493, 516) for x in range(630, 701) if sum(px[x, y]) < 300]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
print("== T10 'Outputs (shifted right)' text bbox (dark in yellow) x755..820 y488..514:")
pts = [(x, y) for y in range(488, 515) for x in range(755, 821) if sum(px[x, y]) < 300]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
print("== T11 'Output Probabilities' text bbox x755..820 y108..130:")
pts = [(x, y) for y in range(108, 131) for x in range(755, 821) if sum(px[x, y]) < 300]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
print("== T12 Input Embedding box bottom: column x=690 y470..500:")
print("  ", [(y, f"#{px[690,y][0]:02X}{px[690,y][1]:02X}{px[690,y][2]:02X}") for y in range(470, 501, 2)])
print("== T13 Output Embedding box: column x=787 y440..490 + text rows:")
print("  ", [(y, f"#{px[787,y][0]:02X}{px[787,y][1]:02X}{px[787,y][2]:02X}") for y in range(440, 491, 2)])
print("== T14 FF box encoder: row y=310 x630..730 transitions:")
prev = None
for x in range(630, 731):
    c = px[x, 310]
    q = (c[0] // 30, c[1] // 30, c[2] // 30)
    if q != prev:
        print(f"  x={x} #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="  ")
        prev = q
print()
print("== T15 FF box decoder: row y=240 x740..845 transitions:")
prev = None
for x in range(740, 846):
    c = px[x, 240]
    q = (c[0] // 30, c[1] // 30, c[2] // 30)
    if q != prev:
        print(f"  x={x} #{c[0]:02X}{c[1]:02X}{c[2]:02X}", end="  ")
        prev = q
print()
print("== T16 N× decoder bbox (dark) x838..880 y295..325:")
pts = [(x, y) for y in range(295, 326) for x in range(838, 881) if sum(px[x, y]) < 330]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
