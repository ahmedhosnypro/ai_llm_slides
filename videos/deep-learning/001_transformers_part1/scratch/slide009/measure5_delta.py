#!/usr/bin/env python3
"""Pass 5: verify callout/leader removal; subtitle ink+color; blue callout border/
underlines; blue curve trace; backprop panel presence."""
from PIL import Image
import numpy as np
from scipy import ndimage

A = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
ai = np.asarray(Image.open(A).convert("RGB"), dtype=np.int16)
bi = np.asarray(Image.open(B).convert("RGB"), dtype=np.int16)

print("== REMOVAL CHECKS (slide9 at parent's positions) ==")
# parent callout box (557,402,282,42) fill F6DCDD
reg = bi[402:444, 557:839]
mode = reg.reshape(-1, 3)
vals, counts = np.unique(mode, axis=0, return_counts=True)
top = vals[np.argsort(-counts)[:4]]
print("  slide9 colors in parent-callout region:", [tuple(int(v) for v in t) for t in top])
print("  slide6 same region fill count F6DCDD:", int((np.abs(ai[402:444, 557:839] - np.array([246,220,221])).sum(axis=2) <= 30).sum()))
print("  slide9 same region fill count F6DCDD:", int((np.abs(reg - np.array([246,220,221])).sum(axis=2) <= 30).sum()))
# parent leader line (470,330)-(558,402): red thin line; check red ink presence in slide9
def redink(img):
    R, G, Bc = img[:,:,0], img[:,:,1], img[:,:,2]
    return (R > 120) & (G < 90) & (Bc < 90)
print("  leader-region red ink px: slide6 =", int(redink(ai[330:402, 470:558]).sum()),
      "| slide9 =", int(redink(bi[330:402, 470:558]).sum()))

print("== SUBTITLE '(Challenges)' — ink bbox + color ==")
reg = bi[84:118, 380:560]
R, G, Bc = reg[:,:,0], reg[:,:,1], reg[:,:,2]
# any dark ink
ink = (R + G + Bc) < 420
ys, xs = np.where(ink)
if len(ys):
    print(f"  dark ink bbox: x{xs.min()+380}..{xs.max()+381} y{ys.min()+84}..{ys.max()+85}")
    px = reg[ink]
    vals, counts = np.unique(px, axis=0, return_counts=True)
    print("  darkest modes:", [(tuple(int(v) for v in t), int(c)) for t, c in sorted(zip(vals, counts), key=lambda z: -z[1])[:6]])
# is it blue?
blueink = (Bc > 110) & (Bc - R > 70) & (Bc - G > 60)
ys, xs = np.where(blueink)
print(f"  blue-ink px in subtitle region: {len(ys)}", f"bbox x{xs.min()+380}..{xs.max()+381} y{ys.min()+84}..{ys.max()+85}" if len(ys) else "")
redink_s = (R > 120) & (G < 90) & (Bc < 90)
ys, xs = np.where(redink_s)
print(f"  red-ink px in subtitle region: {len(ys)}", f"bbox x{xs.min()+380}..{xs.max()+381} y{ys.min()+84}..{ys.max()+85}" if len(ys) else "")

print("== BLUE CALLOUT precise ==")
# fill CCE4F7 mask
R, G, Bc = bi[:,:,0], bi[:,:,1], bi[:,:,2]
fill = (np.abs(R-204) < 20) & (np.abs(G-228) < 20) & (np.abs(B-247) < 20)
lab, n = ndimage.label(fill, structure=np.ones((3,3)))
sizes = ndimage.sum(fill, lab, range(1, n+1))
big = np.argmax(sizes) + 1
ys, xs = np.where(lab == big)
print(f"  fill largest comp: x{xs.min()}..{xs.max()+1} y{ys.min()}..{ys.max()+1} (w{xs.max()-xs.min()+1} h{ys.max()-ys.min()+1})")
# border: blue dark line — scan row profiles of dark blue in y120..205 x100..450
darkblue = (Bc > 110) & (Bc - R > 80) & (Bc - G > 70)
win = darkblue[120:205, 100:450]
rows = win.sum(axis=1)
print("  darkblue row profile (y, count) count>8:", [(y+120, int(c)) for y, c in enumerate(rows) if c > 8])
cols = win.sum(axis=0)
print("  darkblue col profile (x, count) count>8:", [(x+100, int(c)) for x, c in enumerate(cols) if c > 8])
# underline check: blue ink rows below text lines
print("  blue ink rows y136..200 (full-width bands):")
rows_all = darkblue[130:200, 100:450].sum(axis=1)
s = None
for i, v in enumerate(rows_all):
    if v >= 2 and s is None: s = i
    elif v < 2 and s is not None:
        print(f"    band y{s+130}..{i+130}")
        s = None

print("== BLUE CURVE trace (slide9) ==")
# blue thin curve from callout right edge (~x438,y165) to encoder dot (~484,328)
curve = (Bc - R > 60) & (Bc - G > 40) & (Bc > 90)
win = curve[150:340, 420:510]
ys, xs = np.where(win)
print(f"  blue curve px: {len(ys)}")
if len(ys):
    # trace: for each row, mean x
    for yy in range(150, 340, 10):
        row = np.where(curve[yy, 420:510])[0]
        if len(row):
            print(f"    y{yy}: x {row.min()+420}..{row.max()+420} (n={len(row)})")

print("== BACKPROP PANEL quick check (white box red border ~x510..912 y316..500) ==")
white = (R > 245) & (G > 245) & (Bc > 245)
lab, n = ndimage.label(white, structure=np.ones((3,3)))
objs = ndimage.find_objects(lab)
for i, sl in enumerate(objs):
    area = int((lab[sl] == i+1).sum())
    if area > 8000:
        y0, y1 = sl[0].start, sl[0].stop; x0, x1 = sl[1].start, sl[1].stop
        print(f"  white comp area={area}: x{x0}..{x1} y{y0}..{y1} (w{x1-x0} h{y1-y0})")
