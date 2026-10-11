#!/usr/bin/env python3
"""Forensics 3: targeted measurements on original slide_041.jpg."""
from PIL import Image
from collections import Counter

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
im = Image.open(ORIG).convert("RGB")
px = im.load()

def hexc(c): return f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}"

print("== 1. RED BLOB map x412..456 y414..452 (R>150,G<90,B<90):")
for y in range(414, 453, 2):
    row = ""
    for x in range(412, 457):
        r, g, b = px[x, y]
        row += "#" if (r > 150 and g < 90 and b < 90) else ("+" if r > 120 and g < 120 else ".")
    print(f"  y{y}: {row}")

print("== 2. SCHM circle row y=472, x75..195 color transitions:")
prev = None
for x in range(75, 196):
    c = px[x, 472]
    q = (c[0] // 32, c[1] // 32, c[2] // 32)
    if q != prev:
        print(f"  x={x} {hexc(c)}")
        prev = q

print("== 3. SCHM: K/V circle vertical extent at candidate centers:")
for cx in (124, 129, 157, 162, 166):
    ys = [y for y in range(450, 500) if px[cx, y][2] > px[cx, y][0] + 30 and px[cx, y][2] > 60]
    print(f"  x={cx}: blue-ish y {min(ys) if ys else '-'}..{max(ys) if ys else '-'} n={len(ys)}")

print("== 4. SCHM box interior: Scale/Mask boxes — column scans x=100..160 at y=373 (mask pink) and y=402 (paleyellow):")
for yy, lbl in ((373, "Mask?"), (402, "Scale?")):
    runs = []
    cur = None
    for x in range(60, 195):
        r, g, b = px[x, yy]
        is_pink = r > 200 and 130 < g < 200 and 160 < b < 220
        is_py = r > 220 and g > 210 and 130 < b < 210
        m = is_pink or is_py
        if m and cur is None: cur = x
        elif not m and cur is not None: runs.append((cur, x - 1)); cur = None
    if cur: runs.append((cur, 194))
    print(f"  y={yy} ({lbl}): fill runs {runs}")
    if runs:
        for a, b in runs:
            cxm = (a + b) // 2
            col = [y for y in range(340, 430) if (px[cxm, y][0] > 200 and 130 < px[cxm, y][1] < 200 and 160 < px[cxm, y][2] < 220) or (px[cxm, y][0] > 220 and px[cxm, y][1] > 210 and 130 < px[cxm, y][2] < 210)]
            if col: print(f"    run x{a}..{b}: vertical extent y {min(col)}..{max(col)} at x={cxm}")

print("== 5. DECODER column scanline x=787, y110..512:")
prev = None
for y in range(108, 513):
    c = px[787, y]
    q = (c[0] // 24, c[1] // 24, c[2] // 24)
    if q != prev:
        print(f"  y={y:3d} {hexc(c)}")
        prev = q

print("== 6. Group border colors:")
for (x, y, lbl) in ((680, 270, "enc grp top"), (680, 316, "enc grp bot"), (639, 292, "enc grp left"),
                    (720, 292, "enc grp right"), (680, 268, "enc grp top2"), (680, 266, "enc top3")):
    print(f"  {lbl} ({x},{y}) = {hexc(px[x, y])}")
print("  decoder group: vertical scan x=744 y200..310:", [hexc(px[744, y]) for y in range(200, 311, 20)])
print("  decoder group horiz y=204:", [(x, hexc(px[x, 204])) for x in range(744, 845, 12)])

print("== 7. Sine icons: region maps")
for cx, cy, lbl in ((664, 426, "enc sine?"), (810, 431, "dec sine?")):
    print(f"  {lbl} around ({cx},{cy}):")
    for y in range(cy - 12, cy + 13, 2):
        row = ""
        for x in range(cx - 12, cx + 13):
            r, g, b = px[x, y]
            row += "@" if (r < 100 and g < 100 and b < 100) else "."
        print(f"    y{y}: {row}")

print("== 8. TITLE color: densest red rows x300..700 y50..95:")
best = None
for y in range(45, 100):
    n = sum(1 for x in range(150, 820) if px[x, y][0] > 150 and px[x, y][1] < 90 and px[x, y][2] < 90)
    if best is None or n > best[1]: best = (y, n)
print(f"  densest red row y={best[0]} n={best[1]}")
cnt = Counter()
for x in range(150, 820):
    c = px[x, best[0]]
    if c[0] > 140 and c[1] < 100 and c[2] < 100:
        cnt[(c[0] // 16 * 16, c[1] // 16 * 16, c[2] // 16 * 16)] += 1
print("  title red hist:", [(f"#{r:02X}{g:02X}{b:02X}", n) for (r, g, b), n in cnt.most_common(5)])

print("== 9. ZOOM label color hist x340..470 y216..230:")
cnt = Counter()
for y in range(214, 232):
    for x in range(300, 490):
        c = px[x, y]
        if c[0] > 150 and c[1] < 140 and c[2] < 120 and c[0] - c[2] > 60:
            cnt[(c[0] // 16 * 16, c[1] // 16 * 16, c[2] // 16 * 16)] += 1
print(" ", [(f"#{r:02X}{g:02X}{b:02X}", n) for (r, g, b), n in cnt.most_common(6)])

print("== 10. Panel Encoder/Decoder label colors:")
cnt = Counter()
for y in range(108, 132):
    for x in range(585, 690):
        c = px[x, y]
        if c[0] > 140 and c[1] < 110 and c[2] < 110:
            cnt[(c[0] // 16 * 16, c[1] // 16 * 16, c[2] // 16 * 16)] += 1
print("  Encoder label:", [(f"#{r:02X}{g:02X}{b:02X}", n) for (r, g, b), n in cnt.most_common(4)])
cnt = Counter()
for y in range(126, 152):
    for x in range(750, 860):
        c = px[x, y]
        if c[0] > 140 and c[1] < 110 and c[2] < 110:
            cnt[(c[0] // 16 * 16, c[1] // 16 * 16, c[2] // 16 * 16)] += 1
print("  Decoder label:", [(f"#{r:02X}{g:02X}{b:02X}", n) for (r, g, b), n in cnt.most_common(4)])

print("== 11. Yellow pair y312..323 map x745..795:")
for y in range(308, 328, 2):
    row = ""
    for x in range(745, 796):
        r, g, b = px[x, y]
        row += "Y" if (r > 180 and g > 170 and b < 120) else ("R" if (r > 140 and g < 90) else ".")
    print(f"  y{y}: {row}")

print("== 12. Zoom container border: horizontal y=300 x284..302 and x506..524:")
print("  left:", [(x, hexc(px[x, 300])) for x in range(284, 303)])
print("  right:", [(x, hexc(px[x, 300])) for x in range(505, 524)])
print("  top x=400:", [(y, hexc(px[400, y])) for y in range(205, 222)])
print("  bottom x=400:", [(y, hexc(px[400, y])) for y in range(515, 528)])

print("== 13. ×h region map x458..515 y350..395 (dark px):")
for y in range(350, 396, 2):
    row = ""
    for x in range(458, 516):
        r, g, b = px[x, y]
        row += "@" if (r < 120 and g < 90 and b < 90) else ("r" if (r > 150 and g < 90) else ".")
    print(f"  y{y}: {row}")

print("== 14. Bottom Linear borders: horizontal scans y=420 & y=398, x325..495 (brown/dark transitions):")
for yy in (398, 420, 443):
    prev = None
    out = []
    for x in range(325, 496):
        c = px[x, yy]
        q = (c[0] // 40, c[1] // 40, c[2] // 40)
        if q != prev:
            out.append(f"x{x}:{hexc(c)}")
            prev = q
    print(f"  y={yy}: {' '.join(out[:18])}")

print("== 15. Decoder circle rows: dark-blue/red fills x740..835:")
for yy in (315, 320, 388, 392, 402, 407, 412):
    prev = None
    out = []
    for x in range(740, 836):
        c = px[x, yy]
        q = (c[0] // 40, c[1] // 40, c[2] // 40)
        if q != prev:
            out.append(f"x{x}:{hexc(c)}")
            prev = q
    print(f"  y={yy}: {' '.join(out[:16])}")

print("== 16. Encoder circle row y=407, x630..730:")
prev = None
for x in range(630, 731):
    c = px[x, 407]
    q = (c[0] // 32, c[1] // 32, c[2] // 32)
    if q != prev:
        print(f"  x={x} {hexc(c)}")
        prev = q

print("== 17. Encoder N× text: dark px x600..650 y290..330:")
pts = [(x, y) for y in range(288, 332) for x in range(598, 652) if sum(px[x, y]) < 330]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
else:
    print("  none")
print("== 18. Positional-Encoding gray text encoder (left of ⊕): dark-gray px x585..680 y405..450:")
pts = [(x, y) for y in range(403, 452) for x in range(583, 680) if abs(px[x, y][0]-px[x,y][1]) < 25 and abs(px[x,y][1]-px[x,y][2]) < 25 and 60 < px[x, y][0] < 160]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
print("== 19. decoder gray text right of ⊕ x800..895 y395..450:")
pts = [(x, y) for y in range(393, 452) for x in range(798, 896) if abs(px[x, y][0]-px[x,y][1]) < 25 and abs(px[x,y][1]-px[x,y][2]) < 25 and 60 < px[x, y][0] < 160]
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    print(f"  n={len(pts)} bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)}")
print("== 20. panel fills clean samples:")
print("  enc (620,200):", hexc(px[620, 200]), " enc (700,150):", hexc(px[700, 150]))
print("  dec (860,180):", hexc(px[860, 180]), " dec (865,470):", hexc(px[865, 470]), " dec (830,240):", hexc(px[830, 240]))
print("== 21. red arrow at Output Prob: map x738..756 y112..145:")
for y in range(112, 146, 2):
    row = ""
    for x in range(738, 757):
        r, g, b = px[x, y]
        row += "R" if (r > 140 and g < 90 and b < 90) else "."
    print(f"  y{y}: {row}")
