#!/usr/bin/env python3
"""Forensics pass 2b — slide_025.jpg. Chrome borders (fixed), title metrics, top strip."""
import numpy as np
from PIL import Image, ImageFont, ImageDraw

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_025.jpg"
im = Image.open(ORIG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]

# ---- chrome borders (looser red: catch the dark hairline) ----
hair = (R > 90) & (G < 90) & (B < 90) & (R > G + 40) & (R > B + 30)
print("== left border column x57..60: row runs (hairline mask) ==")
lb = hair[:, 56:61].sum(axis=1)
ys = np.where(lb >= 1)[0]
runs = []
s = ys[0]; p = ys[0]
for y in ys[1:]:
    if y - p > 4:
        runs.append((s, p)); s = y
    p = y
runs.append((s, p))
print(f"  runs: {runs}")
print("== top rule rows 40..48, x extent (hairline mask) ==")
for y in range(40, 49):
    xs = np.where(hair[y])[0]
    if len(xs) > 2:
        print(f"  y{y}: x {xs.min()}..{xs.max()} n={len(xs)}")
print("== gray panel bounds (E8E8E8 +/-5) ==")
gray = (abs(R - 232) <= 5) & (abs(G - 232) <= 5) & (abs(B - 232) <= 5)
rows = gray.sum(axis=1)
ys = np.where(rows > 200)[0]
print(f"  gray rows {ys.min()}..{ys.max()}; row270 x extent:")
xs = np.where(gray[270])[0]
print(f"  x {xs.min()}..{xs.max()}")
# panel edge transition at y=270
print("  transition x50..66:", [f"{x}:{tuple(int(v) for v in a[270,x])}" for x in range(50, 67)])
print("  transition x895..915:", [f"{x}:{tuple(int(v) for v in a[270,x])}" for x in range(895, 916)])
print("  panel top/bottom at x=200:")
for y in [40, 44, 46, 48, 50, 510, 515, 517, 518, 520]:
    print(f"    y{y}: {tuple(int(v) for v in a[y,200])}")

# ---- title: red text mask ----
redt = (R > 130) & (G < 110) & (B < 110) & (R > G + 50)
treg = redt[55:100, 300:670]
ys, xs = np.where(treg)
x0, x1 = 300 + xs.min(), 300 + xs.max()
y0, y1 = 55 + ys.min(), 55 + ys.max()
print(f"\n== TITLE ink bbox: x {x0}..{x1} (w {x1-x0+1}, center {(x0+x1)/2:.1f}), y {y0}..{y1} (h {y1-y0+1}) ==")
# row profile for cap/baseline
rp = redt[y0:y1 + 1, x0:x1 + 1].sum(axis=1)
for i, n in enumerate(rp):
    print(f"  y{y0+i}: {int(n)}")
# modal color of strong red pixels
tp = a[y0:y1 + 1, x0:x1 + 1][redt[y0:y1 + 1, x0:x1 + 1]]
q = tp // 8 * 8
vals, counts = np.unique(q.reshape(-1, 3), axis=0, return_counts=True)
top = vals[np.argsort(-counts)][:4]
print("  modal rgb:", [list(map(int, v)) for v in top], "counts", list(map(int, np.sort(counts)[::-1][:4])))
# per-word x gaps (columns with no ink)
cp = redt[y0:y1 + 1, x0:x1 + 1].sum(axis=0)
gaps = []
in_g = False
for i, n in enumerate(cp):
    if n == 0 and not in_g:
        gs, in_g = i, True
    elif n > 0 and in_g:
        gaps.append((x0 + gs, x0 + i - 1)); in_g = False
if in_g:
    gaps.append((x0 + gs, x0 + len(cp) - 1))
print("  column gaps (>=3 px):", [g for g in gaps if g[1] - g[0] >= 2])

# ---- advance fits for the full title ----
FONTS = {
    "Arial": "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    "ArialBold": "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
}
TITLE = "Neural Network Model"
target = x1 - x0 + 1
print(f"\n  target ink width {target}px")
for fn, path in FONTS.items():
    for size in range(26, 42):
        f = ImageFont.truetype(path, size)
        adv = f.getlength(TITLE)
        if abs(adv - target) < 14:
            print(f"  {fn} {size}pt advance {adv:.1f} (delta {adv-target:+.1f})")

# ---- top strip: pink boxes ----
print("\n== pink boxes (FF99CC core) ==")
pinkc = (R > 230) & (G > 110) & (G < 190) & (B > 160) & (B < 225)
sub = pinkc[88:132, :]
rows = sub.sum(axis=1)
ys = np.where(rows > 3)[0]
print("  core rows:", 88 + ys.min(), "..", 88 + ys.max())
# left box: x extent per row band
cp = pinkc[88:132, :].sum(axis=0)
xs = np.where(cp > 2)[0]
runs = []
s = xs[0]; p = xs[0]
for x in xs[1:]:
    if x - p > 6:
        runs.append((s, p)); s = x
    p = x
runs.append((s, p))
print("  pink x runs:", runs)

# left box precise: borders are dark; probe rows/cols
def box_probe(x0b, x1b, y0b, y1b, label):
    print(f"  -- {label} region x{x0b}..{x1b} y{y0b}..{y1b}")
    dark = (R < 110) & (G < 110) & (B < 110)
    d = dark[y0b:y1b + 1, x0b:x1b + 1]
    ys2, xs2 = np.where(d)
    if len(ys2):
        print(f"     dark ink x {x0b+xs2.min()}..{x0b+xs2.max()}, y {y0b+ys2.min()}..{y0b+ys2.max()}")
    # border ring: first/last row with pink core
    pk = pinkc[y0b:y1b + 1, x0b:x1b + 1]
    rr = pk.sum(axis=1); cc = pk.sum(axis=0)
    rys = np.where(rr > 3)[0]; cxs = np.where(cc > 2)[0]
    print(f"     pink core y {y0b+rys.min()}..{y0b+rys.max()}, x {x0b+cxs.min()}..{x0b+cxs.max()}")
    # fill modal
    fill = a[y0b:y1b + 1, x0b:x1b + 1][pk]
    fq = fill // 8 * 8
    vals, counts = np.unique(fq.reshape(-1, 3), axis=0, return_counts=True)
    t = vals[np.argsort(-counts)][:2]
    print(f"     fill modal: {[list(map(int, v)) for v in t]} counts {list(map(int, np.sort(counts)[::-1][:2]))}")

box_probe(55, 140, 90, 130, "Input Samples box")
box_probe(600, 680, 90, 130, "Sample Label box")

# ---- dotted magenta line ----
print("\n== dotted magenta line: strict magenta (R>140, G<90, B>140) in y100..125, x140..600 ==")
mag = (R > 140) & (G < 90) & (B > 140)
seg = mag[100:126, 140:600]
rp = seg.sum(axis=1)
for i, n in enumerate(rp):
    if n:
        print(f"  y{100+i}: {int(n)} px")
rowy = 100 + int(np.argmax(rp))
xs = np.where(mag[rowy, 140:600])[0] + 140
if len(xs):
    diffs = np.diff(xs)
    print(f"  line row y{rowy}: {len(xs)} dots, x {xs.min()}..{xs.max()}, gap histogram:",
          dict(zip(*np.unique(diffs, return_counts=True))))
# arrowheads: any magenta triangle near x~130..140 (left end) or x~595..615 (right end)?
print("  magenta near left end x128..142, y100..125:")
ys2, xs2 = np.where(mag[100:126, 128:143])
print(f"    {len(ys2)} px, x {128+xs2.min()}..{128+xs2.max()}, y {100+ys2.min()}..{100+ys2.max()}" if len(ys2) else "    none")
print("  magenta near right end x592..612, y100..125:")
ys2, xs2 = np.where(mag[100:126, 592:613])
print(f"    {len(ys2)} px, x {592+xs2.min()}..{592+xs2.max()}, y {100+ys2.min()}..{100+ys2.max()}" if len(ys2) else "    none")
