#!/usr/bin/env python3
"""Slide 043 worker probe: right stack fit, arrows (loose mask), box borders,
text-run disambiguation, title em. All coordinates in FRAME px (960x540)."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== 1. RIGHT STACK: front grid fit ===")
# magenta front mask (core + mid tones; avoid pink AA)
mag = (r > 110) & (g < 60) & (b > 110) & (b - g > 80) & (r - g > 90)
# front face region
sub = mag[150:320, 660:805]
ys, xs = np.where(sub)
print("magenta front bbox: x", xs.min() + 660, "..", xs.max() + 660, " y", ys.min() + 150, "..", ys.max() + 150)
# vertical profile: rows via horizontal dark slivers -> count magenta rows at col x=680
col = mag[:, 680]
runs = []
cur = False
for y in range(140, 330):
    if col[y] and not cur:
        start = y; cur = True
    elif not col[y] and cur:
        runs.append((start, y - 1)); cur = False
print("magenta row-runs at x=680:", runs)
# horizontal: col-runs at row y=250
row = mag[250, :]
runs = []
cur = False
for x in range(650, 810):
    if row[x] and not cur:
        start = x; cur = True
    elif not row[x] and cur:
        runs.append((start, x - 1)); cur = False
if cur: runs.append((start, 809))
print("magenta col-runs at y=250:", runs)

print("=== 2. RIGHT STACK: rear staircase sliver boundaries at 3 rows ===")
for y in [200, 250, 290]:
    rowrgb = a[y, 795:880]
    # classify
    tags = []
    for x in range(795, 880):
        rr, gg, bb = a[y, x]
        if gg > 180 and rr < 180 and bb < 100: t = "G"
        elif rr > 200 and 80 <= gg < 160 and bb < 90: t = "O"
        elif rr > 200 and gg > 190 and bb < 120: t = "Y"
        elif 90 <= rr < 160 and 130 <= gg < 190 and bb > 170: t = "B"
        elif rr > 110 and gg < 70 and bb > 110 and bb - gg > 80: t = "M"
        else: t = "."
        tags.append(t)
    s = "".join(tags)
    # compress
    out = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]: j += 1
        if s[i] != ".": out.append(f"{795+i}-{795+j-1}:{s[i]}")
        i = j
    print(f"y={y}:", " ".join(out))

print("=== 3. REAR LAYER dy: yellow column (x=840) top vs magenta top ===")
# yellow mask at x 830..860
ymask = (r > 200) & (g > 190) & (b < 130)
for x in [835, 840, 845]:
    colv = ymask[:, x]
    ys = [y for y in range(80, 330) if colv[y]]
    if ys: print(f"x={x} yellow y {ys[0]}..{ys[-1]}")
# bluegray mask at x 855..870
bmask = (r > 90) & (r < 170) & (g > 120) & (g < 200) & (b > 170)
for x in [855, 860, 865]:
    colv = bmask[:, x]
    ys = [y for y in range(80, 330) if colv[y]]
    if ys: print(f"x={x} bluegray y {ys[0]}..{ys[-1]}")

print("=== 4. TOP dark slivers above right-stack front (x=700) raw ===")
for y in range(128, 160):
    print(f"  (700,{y})#{a[y,700,0]:02X}{a[y,700,1]:02X}{a[y,700,2]:02X}", end="")
    if (y - 127) % 6 == 0: print()
print()

print("=== 5. ARROWS with LOOSE red mask (r>120, r-g>40, r-b>30, g<130) ===")
redm = (r > 120) & (r - g > 40) & (r - b > 30) & (g < 130) & (b < 160)
def bbox(x0, x1, y0, y1, tag):
    sub = redm[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(tag, "EMPTY"); return
    print(f"{tag}: x {xs.min()+x0}..{xs.max()+x0}  y {ys.min()+y0}..{ys.max()+y0}  n={len(xs)}")
    return xs.min()+x0, xs.max()+x0, ys.min()+y0, ys.max()+y0
# vertical arrow: left of right-stack (x 615..665)
bbox(610, 664, 140, 360, "v-arrow region")
# shaft columns
sub = redm[150:350, 610:664]
cc = np.bincount(sub.nonzero()[1] + 610, minlength=700)
top = sorted(range(610, 664), key=lambda x: -cc[x])[:6]
print("v-arrow dense cols:", [(x, int(cc[x])) for x in sorted(top)])
# v-arrow vertical extent at shaft x
sx = 645
ys = [y for y in range(140, 360) if redm[y, sx] or redm[y, sx-1] or redm[y, sx+1]]
print(f"v-arrow ink at x{sx-1}..{sx+1}: y {min(ys)}..{max(ys)}")
# horizontal arrow: below right stack (y 460..500)
bbox(580, 850, 455, 510, "h-arrow region")
sub = redm[455:510, 580:850]
rr = np.bincount(sub.nonzero()[0] + 455, minlength=600)
top = sorted(range(455, 510), key=lambda y: -rr[y])[:6]
print("h-arrow dense rows:", [(y, int(rr[y])) for y in sorted(top)])
# horizontal ink extent at shaft rows
ys_h = sorted(top)[:3]
xs_all = []
for y in ys_h:
    xs_all += [x for x in range(580, 850) if redm[y, x]]
print("h-arrow ink x at rows", ys_h, ":", min(xs_all), "..", max(xs_all))
# diagonal arrow: right of stack (x 795..915, y 230..400)
bbox(795, 915, 230, 410, "diag-arrow region")
# label regions
bbox(610, 664, 150, 360, "v-label+arrow all")
print("=== 6. 'Feature Vector' v-label strip (x 612..642, loose pink) ===")
pink = (r > 130) & (r - g > 25) & (r - b > 20)
sub = pink[150:360, 612:643]
ys, xs = np.where(sub)
if len(xs): print("v-label bbox: x", xs.min()+612, "..", xs.max()+612, " y", ys.min()+150, "..", ys.max()+150, " n=", len(xs))

print("=== 7. h-labels (Channels) rows ===")
sub = pink[455:510, 580:850]
ys, xs = np.where(sub)
print("h region loose bbox: x", xs.min()+580, "..", xs.max()+580, " y", ys.min()+455, "..", ys.max()+455)
# row profile
for y in range(458, 500):
    n = pink[y, 580:850].sum()
    if n > 3: print(f"  y{y}: {n}")

print("=== 8. diag labels (Batch size) region x800..915 y240..400 loose ===")
sub = pink[240:400, 800:915]
ys, xs = np.where(sub)
if len(xs): print("diag loose bbox: x", xs.min()+800, "..", xs.max()+800, " y", ys.min()+240, "..", ys.max()+240, " n=", len(xs))

print("=== 9. CALLOUT box border rect (loose red, vertical strokes) ===")
loose_red = (r > 140) & (r - g > 40) & (r - b > 30) & (g < b + 40)
sub = loose_red[160:280, 320:660]
cc = sub.sum(axis=0)
cols = [320 + i for i, v in enumerate(cc) if v > 60]
print("callout border cols(>60 rows):", cols)
sub2 = loose_red[160:280, 320:660]
rws = sub2.sum(axis=1)
rows = [160 + i for i, v in enumerate(rws) if v > 150]
print("callout border rows(>150 cols):", rows)

print("=== 10. BOTTOM box border (green) ===")
grn = (g > 90) & (g - r > 25) & (g - b > 25)
sub = grn[340:510, 60:900]
cc = sub.sum(axis=0)
cols = [60 + i for i, v in enumerate(cc) if v > 100]
print("green border cols(>100):", cols)
rws = sub.sum(axis=1)
rows = [340 + i for i, v in enumerate(rws) if v > 300]
print("green border rows(>300):", rows)

print("=== 11. B-L3 '(Constrain)' color cores (x715..835, y470..495) ===")
sub = a[470:495, 715:835]
dark = (sub[:, :, 0] < 120) & (sub[:, :, 1] < 120) & (sub[:, :, 2] < 120)
ys, xs = np.where(dark)
print("dark-core count:", len(xs))
if len(xs):
    samples = [tuple(sub[ys[i], xs[i]]) for i in range(0, len(xs), max(1, len(xs)//8))]
    print("dark core samples:", samples)
    print("dark x range:", xs.min()+715, "..", xs.max()+715)
red_core = (sub[:, :, 0] > 140) & (sub[:, :, 0] - sub[:, :, 1] > 60)
ys2, xs2 = np.where(red_core)
print("red-core x range in window:", (xs2.min()+715, xs2.max()+715) if len(xs2) else None, "n=", len(xs2))
# also check B-L2 black "(Source of Error)" x extent
sub2 = a[429:447, 600:850]
dark2 = (sub2[:, :, 0] < 110) & (sub2[:, :, 1] < 110) & (sub2[:, :, 2] < 110)
ys3, xs3 = np.where(dark2)
if len(xs3): print("B-L2 dark cores x:", xs3.min()+600, "..", xs3.max()+600, "n=", len(xs3))

print("=== 12. C-L3 blue extent precise (y223..236, per-col blue count) ===")
blue = (b - r > 40) & (b - g > 20) & (b > 80)
sub = blue[223:237, 340:640]
cc = sub.sum(axis=0)
runs = []
cur = False
for i, v in enumerate(cc):
    if v > 0 and not cur: start = i; cur = True
    elif v == 0 and cur:
        runs.append((340 + start, 340 + i - 1)); cur = False
if cur: runs.append((340 + start, 639))
print("C-L3 blue col-runs:", runs)
# C-L2 red extent precise
redc = (r - g > 60) & (r - b > 60) & (g < b + 35)
sub = redc[198:216, 340:640]
cc = sub.sum(axis=0)
runs = []
cur = False
for i, v in enumerate(cc):
    if v > 0 and not cur: start = i; cur = True
    elif v == 0 and cur:
        runs.append((340 + start, 340 + i - 1)); cur = False
if cur: runs.append((340 + start, 639))
print("C-L2 red col-runs:", runs)
# C-L1 red extent
sub = redc[178:194, 330:640]
ys, xs = np.where(sub)
print("C-L1 red bbox x:", xs.min()+330, "..", xs.max()+330, " y:", ys.min()+178, "..", ys.max()+178)
# C-L4 green extent + underline row
green = (g - r > 30) & (g - b > 30) & (g > 100)
sub = green[242:262, 380:570]
ys, xs = np.where(sub)
print("C-L4 green bbox x:", xs.min()+380, "..", xs.max()+380, " y:", ys.min()+242, "..", ys.max()+242)
# per-row green counts (underline detection)
for y in range(244, 262):
    n = green[y, 380:570].sum()
    if n > 20: print(f"  C-L4 y{y}: green n={n}")

print("=== 13. text baselines: bottom lines per-row ink (x90..860) ===")
ink3 = (r < 170) | redc | blue | green
ink3[:, :90] = False; ink3[:, 860:] = False
for tag, y0, y1 in [("B-L1a", 366, 386), ("B-L1b", 384, 408), ("B-L2", 425, 450), ("B-L3", 468, 496)]:
    prof = [(y, int(ink3[y, 90:860].sum())) for y in range(y0, y1)]
    nz = [p for p in prof if p[1] > 5]
    print(f"{tag}: ink rows {nz[0][0]}..{nz[-1][0]}" if nz else f"{tag}: none", " peak:", max(prof, key=lambda p: p[1]))
# callout text baselines
for tag, y0, y1 in [("C-L1", 176, 196), ("C-L2", 196, 218), ("C-L3", 219, 240), ("C-L4", 241, 262)]:
    prof = [(y, int(ink3[y, 340:620].sum())) for y in range(y0, y1)]
    nz = [p for p in prof if p[1] > 5]
    print(f"{tag}: ink rows {nz[0][0]}..{nz[-1][0]}" if nz else f"{tag}: none", " peak:", max(prof, key=lambda p: p[1]))

print("=== 14. title ink bbox (strict red core) ===")
sub = redc[50:100, 200:850]
ys, xs = np.where(sub)
print("title red-core bbox: x", xs.min()+200, "..", xs.max()+200, " y", ys.min()+50, "..", ys.max()+50)

print("=== 15. pencil icon (x345..405, y232..262) colors ===")
sub = a[232:262, 345:405]
nonbg = (np.abs(sub[:, :, 0] - 250) + np.abs(sub[:, :, 1] - 251) + np.abs(sub[:, :, 2] - 235)) > 90
ys, xs = np.where(nonbg)
print("pencil ink bbox: x", xs.min()+345, "..", xs.max()+345, " y", ys.min()+232, "..", ys.max()+232, " n=", len(xs))
cols = {}
for i in range(0, len(xs), max(1, len(xs)//10)):
    px = tuple(sub[ys[i], xs[i]])
    cols[px] = cols.get(px, 0) + 1
print("pencil color samples:", list(cols.items())[:10])
