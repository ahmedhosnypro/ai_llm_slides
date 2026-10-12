#!/usr/bin/env python3
"""PIL forensics pass 1 — slide_046.jpg (960x540, 1px = 1pt).
Measures: chrome edges, title, bullet block, option boxes, matrix cells,
arrow, z square, Pool( text, tiger photos, ==, caption.
"""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_046.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"size {W}x{H}")

def ink_bbox(x0, y0, x1, y1, pred, label):
    """bbox of pixels satisfying pred inside the window (frame coords)."""
    sub = a[y0:y1, x0:x1]
    m = pred(sub)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"{label:28s} EMPTY in ({x0},{y0})..({x1},{y1})")
        return None
    bx0, bx1 = x0 + xs.min(), x0 + xs.max()
    by0, by1 = y0 + ys.min(), y0 + ys.max()
    print(f"{label:28s} x {bx0}..{bx1}  y {by0}..{by1}  (w {bx1-bx0+1} h {by1-by0+1})")
    return (bx0, by0, bx1, by1)

dark = lambda s: (s.sum(axis=2) < 330)                    # dark ink
red  = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)
blue = lambda s: (s[:,:,2] > 110) & (s[:,:,2] - s[:,:,0] > 50) & (s[:,:,2] - s[:,:,1] > 40)
green= lambda s: (s[:,:,1] > 120) & (s[:,:,1] - s[:,:,0] > 40) & (s[:,:,1] - s[:,:,2] > 40)
grayish = lambda s: (abs(s[:,:,0]-s[:,:,1]) < 14) & (abs(s[:,:,1]-s[:,:,2]) < 14) & (s.sum(axis=2) < 700) & (s.sum(axis=2) > 200)

# --- chrome: panel border (red) scan along a row/col ---
print("\n-- chrome --")
for y in (200, 300, 400):
    row = a[y:y+1]
    xs = np.nonzero(red(row))[0]
    print(f"row y={y}: red-x {xs.min() if len(xs) else '-'}..{xs.max() if len(xs) else '-'} count {len(xs)}")
for x in (100, 480, 860):
    col = a[:, x:x+1]
    ys = np.nonzero(red(col)[:, 0])[0]
    if len(ys):
        # cluster runs
        runs, s = [], ys[0]
        for i in range(1, len(ys)):
            if ys[i] != ys[i-1] + 1:
                runs.append((s, ys[i-1])); s = ys[i]
        runs.append((s, ys[-1]))
        print(f"col x={x}: red-y runs {runs[:8]}")
print("top edge rows 30..60 red col-extent:")
for y in range(30, 62, 2):
    xs = np.nonzero(red(a[y:y+1]))[0]
    if len(xs):
        print(f"  y={y}: x {xs.min()}..{xs.max()} n={len(xs)}")

# panel fill sample (inside panel, away from ink)
print("panel fill samples:", a[300, 200].tolist(), a[430, 700].tolist(), a[250, 500].tolist())
print("outside-left fill sample x=20:", a[300, 20].tolist(), " above panel y=20:", a[20, 480].tolist())

# --- title ---
print("\n-- title --")
ink_bbox(150, 55, 800, 120, red, "title POOLING ink")
# title red sample
tb = ink_bbox(150, 55, 800, 120, red, "  (bbox again)")

# --- bullet block (dark gray text ~#3B3B3B) ---
print("\n-- bullet lines: horizontal ink profiles in x 100..780, y 130..240 --")
sub = a[120:250, 95:790]
m = dark(sub)
rows = m.sum(axis=1)
run = None
for i, v in enumerate(rows):
    y = 120 + i
    if v > 0 and run is None:
        run = y
    elif v == 0 and run is not None:
        seg = a[run:y, 95:790]
        mm = dark(seg)
        ys2, xs2 = np.nonzero(mm)
        print(f"line y {run}..{y-1} h={y-run}  x {95+xs2.min()}..{95+xs2.max()}")
        run = None
if run is not None:
    print(f"line y {run}..249 (open)")

# marker column: hollow circles at left — scan x 100..140 for dark-ish ink per line band
print("\nbullet markers (scan x 98..140):")
for (y0, y1, lbl) in [(145, 170, "main"), (175, 192, "sub1"), (196, 216, "sub2"), (220, 240, "sub3")]:
    seg = a[y0:y1, 98:140]
    mm = (seg.sum(axis=2) < 600)
    ys2, xs2 = np.nonzero(mm)
    if len(xs2):
        print(f"  {lbl}: x {98+xs2.min()}..{98+xs2.max()} y {y0+ys2.min()}..{y0+ys2.max()}")
    else:
        print(f"  {lbl}: none")

# text color sample (middle of a glyph stroke)
print("bullet text color sample:", a[158, 300].tolist())

# --- option boxes (blue outlines) ---
print("\n-- option boxes --")
for (y0, y1, lbl) in [(240, 285, "box1"), (282, 320, "box2")]:
    seg = a[y0:y1, 95:330]
    mm = blue(seg)
    ys2, xs2 = np.nonzero(mm)
    if len(xs2):
        print(f"{lbl} blue-ink x {95+xs2.min()}..{95+xs2.max()} y {y0+ys2.min()}..{y0+ys2.max()}")
# blue color sample
seg = a[250:260, 105:115]
mm = blue(seg)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    px_ = seg[ys2[0], xs2[0]]
    print("box border color sample:", px_.tolist())

# option text ink inside boxes
ink_bbox(120, 245, 300, 275, dark, "box1 text 'Max pooling'")
ink_bbox(120, 285, 310, 310, dark, "box2 text 'Average pooling'")

# --- bottom diagram band ---
print("\n-- diagram band y 320..430 --")
# green cells
ink_bbox(150, 320, 280, 430, green, "2x2 matrix (all green)")
# per-cell: split at midpoints after global bbox
gb = ink_bbox(150, 320, 280, 430, green, "  matrix bbox")
if gb:
    x0, y0, x1, y1 = gb
    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
    for lbl, (cx0, cy0, cx1, cy1) in [("cell a", (x0-2, y0-2, mx+2, my+2)), ("cell b", (mx-2, y0-2, x1+2, my+2)),
                                       ("cell c", (x0-2, my-2, mx+2, y1+2)), ("cell d", (mx-2, my-2, x1+2, y1+2))]:
        ink_bbox(cx0, cy0, cx1, cy1, green, f"  {lbl}")
    print("green fill sample:", a[(y0+y1)//2 - 8, x0 + 6].tolist())
# arrow (dark outline, white fill) right of matrix
ink_bbox(255, 340, 320, 410, dark, "block arrow ink")
# z square
ink_bbox(310, 340, 360, 410, green, "z square")
# italic Pool (
ink_bbox(360, 345, 430, 400, dark, "Pool ( ink")
# large tiger photo — non-panel, non-red region: use variance/colored detection
# tiger is orange/dark photo; detect "photo-ish" = saturated warm or very dark cluster
warm = lambda s: (s[:,:,0] > 100) & (s[:,:,0] - s[:,:,2] > 40)
ink_bbox(410, 310, 620, 430, warm, "large tiger (warm ink)")
# ')' and '==' between photos
ink_bbox(600, 345, 660, 395, dark, ")( == ink")
# small tiger
ink_bbox(655, 330, 790, 400, warm, "small tiger (warm ink)")
# caption blue
ink_bbox(640, 390, 800, 425, blue, "caption 'Size is reduced'")
print("caption color sample:")
seg = a[398:412, 675:780]
mm = blue(seg)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    print(" ", seg[ys2[0], xs2[0]].tolist())

# black bottom strip
print("\n-- bottom strip --")
for y in (520, 525, 530, 535, 538):
    dk = np.nonzero(a[y:y+1].sum(axis=2)[0] < 150)[0]
    print(f"  y={y}: dark n={len(dk)}", (dk.min(), dk.max()) if len(dk) else "")

# badge region in original (top-right) — expect none
print("\n-- badge region in ORIGINAL (x 860..930, y 40..105) --")
seg = a[40:105, 860:930]
yellow = (seg[:,:,0] > 200) & (seg[:,:,1] > 200) & (seg[:,:,2] < 180)
print("yellow px:", int(yellow.sum()))
purple = (seg[:,:,2] > 120) & (seg[:,:,2] - seg[:,:,1] > 30)
print("purple px:", int(purple.sum()))
