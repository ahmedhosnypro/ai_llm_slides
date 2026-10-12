# v2_scan.py — remaining specifics for slide_059
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

def px(x, y): return tuple(int(v) for v in im[y, x])

print("== 1. FAN LINES (light pink/red) y 126..152 ==")
fan = (r > 225) & (g > 130) & (g < 215) & (b > 130) & (b < 215) & (r - b > 30)
for y in [128, 131, 134, 137, 140, 143, 146, 149]:
    rr = runs(fan[y, 380:660], 0)
    print(f"  y{y}: n={len(rr)} runs={[(a+380, c+380) for a, c in rr][:14]}")
ys, xs = np.where(fan[126:150, 380:660])
if len(xs):
    print(f"  fan bbox: x {xs.min()+380}..{xs.max()+380} y {ys.min()+126}..{ys.max()+126} n={len(xs)}")
    S(xs.min() + 380, xs.max() + 380, ys.min() + 126, ys.max() + 126, "   fan")

print("== 2. ARROWS: shape + colors ==")
for (y0, y1, tag) in [(366, 400, "arrow1"), (256, 280, "arrow2"), (204, 228, "arrow3"), (162, 186, "arrow4")]:
    bl = (b - r > 35) & (b - g > 25) & (b > 100)
    prof = [(y, int(bl[y, 495:528].sum())) for y in range(y0, y1)]
    print(f"  {tag} rowprofile x495..528:", [(y, n) for y, n in prof if n > 0])
print("  arrow1 probes:", [(p, px(*p)) for p in [(510, 374), (510, 380), (510, 386), (505, 378), (515, 378)]])
print("  arrow4 probes:", [(p, px(*p)) for p in [(510, 170), (510, 176), (510, 181), (506, 174), (514, 174)]])

print("== 3. SOFTMAX text + top band colors ==")
print("  SoftmaxLayer text probes:", [(p, px(*p)) for p in [(190, 102), (200, 100), (220, 104), (240, 102)]])
print("  OutputClasses probes:", [(p, px(*p)) for p in [(330, 62), (350, 60), (390, 62)]])
print("  C1 probes:", [(p, px(*p)) for p in [(441, 64), (448, 66), (444, 62)]])
print("  input-seq probes:", [(p, px(*p)) for p in [(80, 395), (100, 394), (120, 396)]])
print("  word-emb probes:", [(p, px(*p)) for p in [(90, 413), (110, 412), (100, 426)]])
print("  position probes:", [(p, px(*p)) for p in [(90, 469), (110, 468), (100, 482)]])
print("  pooled-note probes:", [(p, px(*p)) for p in [(100, 147), (120, 146), (110, 160)]])

print("== 4. LEFT ANNOTATIONS full-extent (x 55..210) ==")
ink = (abs(r - g) > 35) | (abs(g - b) > 35) | (abs(r - b) > 35)
for (y0, y1, tag) in [(138, 170, "pooled-note"), (218, 262, "output-seq"),
                      (384, 404, "input-seq"), (404, 452, "word-emb"), (452, 512, "position")]:
    sub = ink[y0:y1, 55:210]
    ys, xs = np.where(sub)
    if len(xs):
        rowc = sub.sum(axis=1)
        ln = runs(rowc > 2, 2)
        print(f"  {tag}: x {xs.min()+55}..{xs.max()+55} y {ys.min()+y0}..{ys.max()+y0} lines={[(a+y0, c+y0) for a, c in ln]}")
        for (a, c) in ln:
            ssub = ink[a + y0:c + y0 + 1, 55:210]
            y2, x2 = np.where(ssub)
            print(f"    line y{a+y0}..{c+y0}: x {x2.min()+55}..{x2.max()+55}")
        S(xs.min() + 55, xs.max() + 55, ys.min() + y0, ys.max() + y0, f"   {tag}")

print("== 5. TAN BAR right edge + circles overlap ==")
tan = (abs(r - 245) < 16) & (abs(g - 203) < 18) & (abs(b - 167) < 22)
for y in [93, 96, 101, 106, 110]:
    rr = runs(tan[y, :], 1)
    print(f"  tan y{y}: first={rr[:2]} last={rr[-2:]}")

print("== 6. BAR TEXT (lighter-than-bar mask per bar) ==")
for (y0, y1, tag) in [(281, 297, "bar1"), (301, 318, "bar2"), (352, 370, "bar3")]:
    m = (r > 195) & (g > 105) & (b > 105)
    sub = m[y0:y1, 160:860]
    ys2, xs2 = np.where(sub)
    if len(xs2):
        print(f"  {tag}: x {xs2.min()+160}..{xs2.max()+160} y {ys2.min()+y0}..{ys2.max()+y0} n={len(xs2)}")
        S(xs2.min() + 160, xs2.max() + 160, ys2.min() + y0, ys2.max() + y0, f"   {tag}")
        blk = im[y0:y1, xs2.min()+160:xs2.max()+160].reshape(-1, 3)
        c = Counter((int(a)//24*24, int(bb)//24*24, int(cc)//24*24) for a, bb, cc in blk)
        print(f"    modal:", c.most_common(4))

print("== 7. GAP text color/extent ==")
m = (r < 150) & (g < 150) & (b < 150)
sub = m[186:212, 200:880]
ys2, xs2 = np.where(sub)
print(f"  GAP text+borders: x {xs2.min()+200}..{xs2.max()+200} y {ys2.min()+186}..{ys2.max()+186}")
blk = im[190:206, 434:623].reshape(-1, 3)
c = Counter((int(a)//24*24, int(bb)//24*24, int(cc)//24*24) for a, bb, cc in blk)
print("  GAP text modal:", c.most_common(3))

print("== 8. X tail labels wide scan (x 720..910) ==")
dred = (r < 220) & (r - g > 45) & (r - b > 35) & (r > 70)
sub = dred[410:446, 720:910]
print("  X tail cols:", runs(sub.sum(axis=0) > 0, 2), "(+720)")
sub = dred[410:446, 150:260]
print("  X head col1 cols:", runs(sub.sum(axis=0) > 0, 2), "(+150)")
# Y tail
btxt = (b - r > 45) & (b - g > 35) & (b > 110) & (r < 160)
sub = btxt[228:256, 720:910]
print("  Y tail cols:", runs(sub.sum(axis=0) > 0, 2), "(+720)")
sub = btxt[228:256, 150:280]
print("  Y head col1-2 cols:", runs(sub.sum(axis=0) > 0, 2), "(+150)")

print("== 9. COLUMN CELL SEQUENCE (row scans at cell mid-height) ==")
for (y, tag) in [(427, "X row"), (242, "Y row"), (487, "V row")]:
    row = im[y, 160:900].astype(int)
    kinds = []
    prev = None
    for i, (rr, gg, bb) in enumerate(row):
        if rr > 240 and gg > 240 and bb > 215 and rr - bb > 25: k = "Y"   # pale yellow
        elif gg > 240 and rr < 245 and gg - rr > 8 and gg - bb > 10: k = "m"  # mint
        elif rr > 240 and 150 < gg < 215 and 140 < bb < 200: k = "p"     # pink
        elif 215 < rr < 245 and 215 < gg < 240 and bb > 235: k = "l"     # lavender
        elif rr > 240 and gg > 225 and 195 < bb < 225: k = "q"           # pink-lilac
        elif rr < 150 and gg < 120: k = "T"                               # dark text
        elif abs(int(rr) - int(gg)) < 20 and abs(int(gg) - int(bb)) < 20 and rr < 215: k = "B"  # border/gray
        else: k = "."
        kinds.append(k)
    s = "".join(kinds)
    comp = []
    cur, n = s[0], 1
    for ch in s[1:]:
        if ch == cur: n += 1
        else:
            comp.append(f"{cur}{n}")
            cur, n = ch, 1
    comp.append(f"{cur}{n}")
    print(f"  {tag} y{y}: {' '.join(comp)}")

print("== 10. pooled row exact band + cell edges ==")
nonbg = ((abs(r - 224) > 12) | (abs(g - 232) > 12) | (abs(b - 224) > 14))
for y in [144, 147, 150, 153, 156, 159, 162, 165, 168]:
    rr = runs(nonbg[y, 380:660], 1)
    print(f"  y{y}: n={len(rr)} first3={[(a+380, c+380) for a, c in rr[:3]]} last={(rr[-1][0]+380, rr[-1][1]+380) if rr else None}")

print("== 11. title text probes ==")
print("  title probes:", [(p, px(*p)) for p in [(420, 334), (450, 335), (500, 334), (550, 336)]])
print("== 12. plus circle color + white + ==")
print("  plus probes:", [(p, px(*p)) for p in [(500, 435), (500, 445), (500, 455), (497, 445), (503, 445)]])
sub = (r > 235) & (g > 235) & (b > 235)
ys2, xs2 = np.where(sub[425:465, 485:515])
if len(xs2):
    print(f"  white + ink: x {xs2.min()+485}..{xs2.max()+485} y {ys2.min()+425}..{ys2.max()+425}")
