# v1_scan.py — worker verification scan for slide_059 (frame 960x540)
# Mapping (same as certified 038): slide_x = (fx-18.63)/0.96123, slide_y = fy/0.95556
from PIL import Image
import numpy as np
from collections import Counter

im = np.asarray(Image.open('unique_slides/slide_059.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def sx(fx): return (fx - 18.63) / 0.96123
def sy(fy): return fy / 0.95556
def S(x0, x1, y0, y1, tag):
    print(f"  {tag}: slide x {sx(x0):.1f}..{sx(x1):.1f} y {sy(y0):.1f}..{sy(y1):.1f} "
          f"(w {sx(x1)-sx(x0):.1f} h {sy(y1)-sy(y0):.1f})")

def runs(bools, min_len=1):
    out, s = [], None
    for i, v in enumerate(bools):
        if v and s is None: s = i
        if not v and s is not None:
            if i - s >= min_len: out.append((s, i - 1))
            s = None
    if s is not None: out.append((s, len(bools) - 1))
    return out

def modal(x0, x1, y0, y1, tag, k=4):
    blk = im[y0:y1, x0:x1].reshape(-1, 3)
    c = Counter((int(a) // 8 * 8, int(bb) // 8 * 8, int(cc) // 8 * 8) for a, bb, cc in blk)
    print(f"  {tag} modal:", c.most_common(k))

print("== A. FILL COLORS (modal over empty patches) ==")
modal(100, 150, 470, 500, "input container (left of rows)")
modal(700, 750, 415, 440, "X row between boxes?")
modal(180, 200, 425, 435, "X box1 interior left")
modal(700, 780, 230, 250, "Y row between boxes")
modal(180, 200, 235, 245, "Y box1 interior left")
modal(200, 240, 480, 495, "V row peach interior")
modal(300, 420, 60, 78, "above tan bar / top band bg")
modal(200, 240, 130, 140, "between tan bar and pooled row")

print("== B. INPUT CONTAINER edges ==")
pinkish = (r > 235) & (g > 205) & (g < 235) & (b > 235)  # lilac fill ~ (246,220,247)
print("  lilac rows at col 300:", runs(pinkish[:, 300], 2))
print("  lilac rows at col 700:", runs(pinkish[:, 700], 2))
print("  lilac cols at row 420:", runs(pinkish[420, :], 2)[:3], "...", runs(pinkish[420, :], 2)[-3:])
print("  lilac cols at row 460:", runs(pinkish[460, :], 2)[:3], "...", runs(pinkish[460, :], 2)[-3:])
print("  lilac cols at row 500:", runs(pinkish[500, :], 2)[:3], "...", runs(pinkish[500, :], 2)[-3:])

print("== C. GREEN dashed rect (word-embedding row) ==")
grn = (g - r > 25) & (g - b > 25) & (g > 100) & (g < 215)
print("  green rows at col 300:", runs(grn[:, 300], 0))
print("  green rows at col 550:", runs(grn[:, 550], 0))
print("  green rows at col 850:", runs(grn[:, 850], 0))
print("  green cols at row 412:", runs(grn[412, :], 0)[:6], "...")
print("  green cols at row 444:", runs(grn[444, :], 0)[:6], "...")

print("== D. ORANGE dashed rect + peach ==")
org = (r > 195) & (g > 95) & (g < 185) & (b < 110) & (r - b > 110)
print("  orange rows at col 300:", runs(org[:, 300], 0))
print("  orange rows at col 550:", runs(org[:, 550], 0))
print("  orange rows at col 850:", runs(org[:, 850], 0))
print("  orange cols at row 458:", runs(org[458, :], 0)[:4], "...", runs(org[458, :], 0)[-2:])
print("  orange cols at row 466:", runs(org[466, :], 0)[:4], "...")
print("  orange cols at row 508:", runs(org[508, :], 0)[:4], "...", runs(org[508, :], 0)[-2:])
peach = (abs(r - 253) < 10) & (abs(g - 235) < 14) & (abs(b - 208) < 16)
print("  peach rows at col 300:", runs(peach[:, 300], 1))

print("== E. Y ROW: light-blue fill + blue dashed border ==")
lblu = (abs(r - 214) < 18) & (abs(g - 234) < 14) & (abs(b - 248) < 12)
print("  lightblue rows at col 300:", runs(lblu[:, 300], 1))
print("  lightblue rows at col 700:", runs(lblu[:, 700], 1))
print("  lightblue cols at row 240:", runs(lblu[240, :], 1)[:3], "...", runs(lblu[240, :], 1)[-3:])
blue = (b - r > 50) & (b - g > 40) & (b > 130)
print("  blue(border) rows at col 300:", runs(blue[:, 300], 0))
print("  blue(border) rows at col 700:", runs(blue[:, 700], 0))
print("  blue(border) cols at row 212:", runs(blue[212, :], 0)[:6], "...")
print("  blue(border) cols at row 274:", runs(blue[274, :], 0)[:6], "...")

print("== F. ROSE ENCODER CONTAINER exact ==")
rose = (abs(r - 205) < 30) & (abs(g - 92) < 40) & (abs(b - 92) < 40)
print("  rose rows at col 480:", runs(rose[:, 480], 1))
print("  rose rows at col 200:", runs(rose[:, 200], 1))
print("  rose cols at row 322:", runs(rose[322, :], 2)[:3], "...", runs(rose[322, :], 2)[-3:])
print("  rose cols at row 350:", runs(rose[350, :], 2)[:3], "...", runs(rose[350, :], 2)[-3:])
print("  rose cols at row 375:", runs(rose[375, :], 2)[:3], "...", runs(rose[375, :], 2)[-3:])

print("== G. BARS + white bar text ==")
dr = (r >= 130) & (r < 225) & (g < 80) & (b < 80)
for (y0, y1, tag) in [(276, 300, "bar1"), (298, 321, "bar2"), (350, 372, "bar3")]:
    cols = np.where(dr[y0:y1, :].sum(axis=0) > (y1 - y0) * 0.55)[0]
    rows = np.where(dr[y0:y1, 200:800].sum(axis=1) > 300)[0]
    print(f"  {tag}: x {cols.min()}..{cols.max()}  y {rows.min()+y0}..{rows.max()+y0}")
    S(cols.min(), cols.max(), rows.min() + y0, rows.max() + y0, f"   {tag}")
white = (r > 228) & (g > 228) & (b > 228)
for (y0, y1, tag) in [(280, 298, "bar1 text"), (301, 318, "bar2 text"), (352, 370, "bar3 text")]:
    sub = white[y0:y1, 160:860]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  {tag}: x {xs.min()+160}..{xs.max()+160} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}")
        S(xs.min() + 160, xs.max() + 160, ys.min() + y0, ys.max() + y0, f"   {tag}")
    else:
        print(f"  {tag}: NONE")
sub = white[320:352, 160:880]
ys, xs = np.where(sub)
print(f"  title text: x {xs.min()+160}..{xs.max()+160} y {ys.min()+320}..{ys.max()+320} n={len(xs)}")
S(xs.min() + 160, xs.max() + 160, ys.min() + 320, ys.max() + 320, "   title")

print("== H. ELLIPSIS COLUMNS (between bar2/bar3) vertical profiles ==")
for (x0, x1) in [(254, 262), (312, 320), (379, 386), (617, 624), (690, 697), (757, 764)]:
    colprof = dr[318:352, x0:x1].sum(axis=1)
    rr = runs(colprof > 0, 0)
    print(f"  col x{x0}: darkred row-runs (y+318): {rr}")

print("== I. GAP BOX borders (loose dark mask) ==")
dark = (r < 175) & (g < 175) & (b < 175) & (abs(r - g) < 40) & (abs(g - b) < 40)
print("  dark rows at col 300 (y 150..230):", runs(dark[150:230, 300], 0), "(+150)")
print("  dark rows at col 700 (y 150..230):", runs(dark[150:230, 700], 0), "(+150)")
print("  dark cols at row 200 (x 150..920):", runs(dark[200, 150:920], 0)[:4], "...", runs(dark[200, 150:920], 0)[-4:])
print("  dark cols at row 170 (x 150..920):", runs(dark[170, 150:920], 0)[:6], "...")
print("  dark cols at row 215 (x 150..920):", runs(dark[215, 150:920], 0)[:6], "...")

print("== J. POOLED ROW ==")
ysq = (r > 235) & (g > 235) & (b < 215) & (r - b > 30)
gsq = (g - r > 15) & (g - b > 15) & (g > 235)
psq = (r > 235) & (r - g > 25) & (r - b > 25) & (b < 235)
print("  yellow rows at col 395:", runs(ysq[:, 395], 0))
print("  cell union rows at col 395:", runs((ysq | gsq | psq)[:, 395], 0))
print("  union cols at row 150:", runs((ysq | gsq | psq)[150, 350:700], 0)[:8], "(+350)")
print("  union cols at row 158:", runs((ysq | gsq | psq)[158, 350:700], 0)[:8], "(+350)")
for x0 in range(385, 640, 21):
    blk = im[140:165, x0:x0 + 10].reshape(-1, 3)
    c = Counter((int(a) // 16 * 16, int(bb) // 16 * 16, int(cc) // 16 * 16) for a, bb, cc in blk)
    print(f"    pooled cell x{x0}:", c.most_common(2))

print("== K. FAN LINES y 127..150 ==")
fan = (r > 140) & (r < 235) & (g < 120) & (b < 120) & (r - g > 50)
for y in [128, 132, 136, 140, 144, 148]:
    rr = runs(fan[y, 350:700], 0)
    print(f"  fan y{y}: n={len(rr)} first6={[(a+350,c+350) for a,c in rr[:6]]}")

print("== L. BLOCK ARROWS (blue outline) restricted ==")
blue2 = (b - r > 40) & (b - g > 30) & (b > 110)
for (y0, y1, tag) in [(368, 396, "arrow1 in->enc"), (246, 276, "arrow2 enc->out"),
                      (196, 226, "arrow3 out->GAP"), (148, 168, "arrow4 GAP->pooled")]:
    sub = blue2[y0:y1, 470:550]
    ys, xs = np.where(sub)
    if len(xs):
        print(f"  {tag}: x {xs.min()+470}..{xs.max()+470} y {ys.min()+y0}..{ys.max()+y0} n={len(xs)}")
        S(xs.min() + 470, xs.max() + 470, ys.min() + y0, ys.max() + y0, f"   {tag}")
    else:
        print(f"  {tag}: NONE")

print("== M. TOP BAND ==")
bt = (b - r > 35) & (b - g > 25) & (b > 120)
print("  blue text cols y 55..72:", runs(bt[55:72, 250:700].sum(axis=0) > 1, 4), "(+250)")
print("  OutputClasses bbox:", end=" ")
ys, xs = np.where(bt[52:74, 300:430])
print(f"x {xs.min()+300}..{xs.max()+300} y {ys.min()+52}..{ys.max()+52}")
for (x0, x1, tag) in [(425, 465, "C1"), (498, 540, "C2"), (570, 612, "C3")]:
    ys, xs = np.where(bt[52:80, x0:x1])
    print(f"  {tag}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+52}..{ys.max()+52}")
# stems below C labels
for cx in [440, 512, 585]:
    rr = runs(bt[70:86, cx - 3:cx + 4].any(axis=1), 0)
    print(f"  stem rows near cx={cx} (y+70): {rr}")

print("== N. TAN BAR + Softmax Layer text ==")
tan = (abs(r - 245) < 16) & (abs(g - 203) < 18) & (abs(b - 167) < 22)
print("  tan rows at col 300:", runs(tan[:, 300], 1))
print("  tan rows at col 800:", runs(tan[:, 800], 1))
print("  tan cols at row 86:", runs(tan[86, :], 1)[:3], "...", runs(tan[86, :], 1)[-3:])
print("  tan cols at row 108:", runs(tan[108, :], 1)[:3], "...", runs(tan[108, :], 1)[-3:])
otxt = (r > 190) & (g > 90) & (g < 190) & (b < 110) & (r - b > 90)
ys, xs = np.where(otxt[82:112, 175:290])
print(f"  SoftmaxLayer text: x {xs.min()+175}..{xs.max()+175} y {ys.min()+82}..{ys.max()+82} n={len(xs)}")
S(xs.min() + 175, xs.max() + 175, ys.min() + 82, ys.max() + 82, "   softmax text")

print("== O. CIRCLES + red bases ==")
navy = (b - r > 60) & (b - g > 50) & (b > 110) & (r < 130)
for (x0, x1, tag) in [(415, 465, "c1"), (488, 538, "c2"), (560, 612, "c3")]:
    ys, xs = np.where(navy[78:125, x0:x1])
    print(f"  {tag}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+78}..{ys.max()+78} "
          f"d=({xs.max()-xs.min()+1},{ys.max()-ys.min()+1})")
    S(xs.min() + x0, xs.max() + x0, ys.min() + 78, ys.max() + 78, f"   {tag}")
plusred = (r > 150) & (r < 235) & (g < 110) & (b < 110) & (r - g > 80)
for (x0, x1, tag) in [(420, 465, "base1"), (490, 538, "base2"), (562, 610, "base3")]:
    ys, xs = np.where(plusred[118:135, x0:x1])
    if len(xs):
        print(f"  {tag}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+118}..{ys.max()+118}")
plusys, plusxs = np.where(plusred[420:470, 480:525])
print(f"  plus circle: x {plusxs.min()+480}..{plusxs.max()+480} y {plusys.min()+420}..{plusys.max()+420}")
S(plusxs.min() + 480, plusxs.max() + 480, plusys.min() + 420, plusys.max() + 420, "   plus")

print("== P. LEFT ANNOTATIONS ==")
ink = (abs(r - g) > 35) | (abs(g - b) > 35) | (abs(r - b) > 35)
for (y0, y1, tag) in [(138, 170, "pooled-note"), (288, 352, "output-seq"),
                      (384, 404, "input-seq"), (404, 452, "word-emb"), (452, 510, "position")]:
    sub = ink[y0:y1, 62:150]
    ys, xs = np.where(sub)
    if len(xs):
        rowc = sub.sum(axis=1)
        print(f"  {tag}: x {xs.min()+62}..{xs.max()+62} y {ys.min()+y0}..{ys.max()+y0} "
              f"lines={runs(rowc > 2, 2)} (+{y0})")
        S(xs.min() + 62, xs.max() + 62, ys.min() + y0, ys.max() + y0, f"   {tag}")

print("== Q. TOKEN ROWS: labels / cells / dots / borders ==")
dred = (r < 215) & (r - g > 55) & (r - b > 45) & (r > 80)
sub = dred[410:446, 150:910]
print("  X labels cols:", runs(sub.sum(axis=0) > 0, 2), "(+150)")
btxt = (b - r > 60) & (b - g > 45) & (b > 110) & (r < 150)
sub = btxt[222:262, 150:910]
print("  Y labels cols:", runs(sub.sum(axis=0) > 0, 2), "(+150)")
sub = btxt[468:508, 150:910]
print("  V labels cols:", runs(sub.sum(axis=0) > 0, 2), "(+150)")
# box borders: grayish vertical strokes at row mid
grayln = (abs(r - g) < 25) & (abs(g - b) < 25) & (r > 120) & (r < 205)
sub = grayln[424:432, 150:910]
print("  X-row gray strokes:", runs(sub.sum(axis=0) >= 5, 1), "(+150)")
sub = grayln[238:246, 150:910]
print("  Y-row gray strokes:", runs(sub.sum(axis=0) >= 5, 1), "(+150)")
# dots
gdot = (g - r > 25) & (g - b > 25) & (g > 150) & (g < 235)
sub = gdot[420:438, 590:760]
print("  X-row green dots:", runs(sub.sum(axis=0) > 0, 1), "(+590)")
sub = gdot[474:500, 590:760]
print("  V-row green dots:", runs(sub.sum(axis=0) > 0, 1), "(+590)")
bdot = (b - r > 40) & (b - g > 25) & (b > 150)
sub = bdot[232:252, 590:760]
print("  Y-row blue dots:", runs(sub.sum(axis=0) > 0, 1), "(+590)")
