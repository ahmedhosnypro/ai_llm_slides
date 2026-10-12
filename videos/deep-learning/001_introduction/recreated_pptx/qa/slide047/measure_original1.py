#!/usr/bin/env python3
"""PIL forensics pass 1 — slide_047.jpg (960x540, 1px = 1pt).
Measures: chrome, title, intro lines, white content box, bullet lines,
blue label boxes, Where legend box, 4x4 input grid cells, arrow, 1/2 fraction,
2x2 output grid, bottom strip, badge region.
"""
from PIL import Image
import numpy as np

IMG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_047.jpg"
im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"size {W}x{H}")

def ink_bbox(x0, y0, x1, y1, pred, label):
    sub = a[y0:y1, x0:x1]
    m = pred(sub)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"{label:34s} EMPTY in ({x0},{y0})..({x1},{y1})")
        return None
    bx0, bx1 = x0 + xs.min(), x0 + xs.max()
    by0, by1 = y0 + ys.min(), y0 + ys.max()
    print(f"{label:34s} x {bx0}..{bx1}  y {by0}..{by1}  (w {bx1-bx0+1} h {by1-by0+1})")
    return (bx0, by0, bx1, by1)

dark  = lambda s: (s.sum(axis=2) < 330)
red   = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)
blue  = lambda s: (s[:,:,2] > 110) & (s[:,:,2] - s[:,:,0] > 50) & (s[:,:,2] - s[:,:,1] > 40)
green = lambda s: (s[:,:,1] > 120) & (s[:,:,1] - s[:,:,0] > 40) & (s[:,:,1] - s[:,:,2] > 40)
yellow= lambda s: (s[:,:,0] > 180) & (s[:,:,1] > 170) & (s[:,:,2] < 130)
cyan  = lambda s: (s[:,:,2] > 150) & (s[:,:,1] > 120) & (s[:,:,0] < 140) & (s[:,:,2] - s[:,:,0] > 60)
white = lambda s: (s[:,:,0] > 235) & (s[:,:,1] > 235) & (s[:,:,2] > 235)

# --- chrome ---
print("\n-- chrome --")
for y in (200, 300, 400):
    xs = np.nonzero(red(a[y:y+1]))[0]
    print(f"row y={y}: red-x {xs.min() if len(xs) else '-'}..{xs.max() if len(xs) else '-'} count {len(xs)}")
for x in (100, 480, 860):
    ys = np.nonzero(red(a[:, x:x+1])[:, 0])[0]
    if len(ys):
        runs, s = [], ys[0]
        for i in range(1, len(ys)):
            if ys[i] != ys[i-1] + 1:
                runs.append((int(s), int(ys[i-1]))); s = ys[i]
        runs.append((int(s), int(ys[-1])))
        print(f"col x={x}: red-y runs {runs[:10]}")
print("panel fill samples:", a[300, 200].tolist(), a[230, 700].tolist(), a[250, 500].tolist())
print("outside fill x=20:", a[300, 20].tolist(), " y=20:", a[20, 480].tolist())

# --- badge region in ORIGINAL (top-right) ---
print("\n-- badge region in ORIGINAL (x 860..930, y 40..105) --")
seg = a[40:105, 860:930]
yel = (seg[:,:,0] > 200) & (seg[:,:,1] > 200) & (seg[:,:,2] < 180)
print("yellow px:", int(yel.sum()))
pur = (seg[:,:,2] > 120) & (seg[:,:,2] - seg[:,:,1] > 30)
print("purple px:", int(pur.sum()))

# --- title (red ink, with maybe blue 'Layer') ---
print("\n-- title --")
ink_bbox(60, 40, 900, 120, red, "title red ink")
ink_bbox(60, 40, 900, 120, blue, "title blue ink")
ink_bbox(60, 40, 900, 120, lambda s: (s.sum(axis=2) < 400), "title all-dark ink")
print("title red sample:", a[60, 300].tolist())

# --- intro lines (red + dark blue), y 100..200 ---
print("\n-- intro lines: horizontal ink profiles y 100..200, x 60..900 --")
sub = a[100:200, 60:900]
m = (sub.sum(axis=2) < 480)
rows = m.sum(axis=1)
run = None
for i, v in enumerate(rows):
    y = 100 + i
    if v > 2 and run is None:
        run = y
    elif v <= 2 and run is not None:
        seg2 = a[run:y, 60:900]
        mm = (seg2.sum(axis=2) < 480)
        ys2, xs2 = np.nonzero(mm)
        # split colors
        rmask = red(seg2); bmask = blue(seg2)
        ry, rx = np.nonzero(rmask); by, bx = np.nonzero(bmask)
        print(f"line y {run}..{y-1} h={y-run}  x {60+xs2.min()}..{60+xs2.max()}"
              + (f"  red_x {60+rx.min()}..{60+rx.max()}" if len(rx) else "")
              + (f"  blue_x {60+bx.min()}..{60+bx.max()}" if len(bx) else ""))
        run = None
if run is not None:
    print(f"line y {run}..199 (open)")
# color samples
print("intro line1 color sample:", a[125, 120].tolist())

# --- white content box ---
print("\n-- white content box --")
ink_bbox(40, 190, 920, 520, red, "content box red border (all red)")
# red border strokes: find columns with many red pixels in y 200..500
sub = a[200:500, :]
rm = red(sub)
colcount = rm.sum(axis=0)
cols = np.nonzero(colcount > 50)[0]
print("red-border columns (count>50):", cols[:20], "..." if len(cols) > 20 else "")
sub2 = a[:, 100:860]
rm2 = red(sub2)
rowcount = rm2.sum(axis=1)
rowsr = np.nonzero(rowcount > 50)[0]
print("red-border rows (count>50):", rowsr[:20], "..." if len(rowsr) > 20 else "")
print("inside-box fill sample:", a[300, 400].tolist(), a[250, 800].tolist())

# --- bullet lines inside box (left half), y 210..350, x 90..540 ---
print("\n-- bullet lines: profiles x 90..540, y 205..360 --")
sub = a[205:360, 90:540]
m = (sub.sum(axis=2) < 500)
rows = m.sum(axis=1)
run = None
for i, v in enumerate(rows):
    y = 205 + i
    if v > 1 and run is None:
        run = y
    elif v <= 1 and run is not None:
        seg2 = a[run:y, 90:540]
        mm = (seg2.sum(axis=2) < 500)
        ys2, xs2 = np.nonzero(mm)
        bmask = blue(seg2)
        by, bx = np.nonzero(bmask)
        print(f"line y {run}..{y-1} h={y-run}  x {90+xs2.min()}..{90+xs2.max()}"
              + (f"  blue_x {90+bx.min()}..{90+bx.max()}  blue_y {run+by.min()}..{run+by.max()}" if len(bx) else ""))
        run = None
if run is not None:
    print(f"line y {run}..359 (open)")
# bullet markers: orange/red rings at left
print("\nbullet markers (scan x 90..130, y 205..360):")
orange = lambda s: (s[:,:,0] > 150) & (s[:,:,1] > 60) & (s[:,:,1] < 160) & (s[:,:,2] < 90)
seg = a[205:360, 88:132]
om = orange(seg)
ys2, xs2 = np.nonzero(om)
if len(xs2):
    print(f"  orange ink x {88+xs2.min()}..{88+xs2.max()} y {205+ys2.min()}..{205+ys2.max()} count {len(xs2)}")
    # cluster by y
    yy = np.sort(np.unique(ys2))
    splits = np.nonzero(np.diff(yy) > 3)[0]
    start = 0
    for k, idx in enumerate(list(splits) + [len(yy)-1]):
        band = yy[start:idx+1]
        bm = om[band.min():band.max()+1]
        bys, bxs = np.nonzero(bm)
        print(f"  marker band y {205+band.min()}..{205+band.max()} x {88+bxs.min()}..{88+bxs.max()}")
        start = idx + 1
else:
    print("  none")
print("marker color sample:", a[225, 105].tolist())

# --- Where legend box (light blue fill + red border), x 440..570, y 330..490 ---
print("\n-- Where legend box --")
lightblue = lambda s: (s[:,:,2] > 200) & (s[:,:,0] > 150) & (s[:,:,0] < 230) & (s[:,:,2] - s[:,:,0] > 20)
ink_bbox(420, 320, 600, 500, lightblue, "legend light-blue fill")
ink_bbox(420, 320, 600, 500, red, "legend red ink")
print("legend fill sample:", a[400, 480].tolist())
# rows inside legend
sub = a[330:500, 430:600]
m = (sub.sum(axis=2) < 480)
rows = m.sum(axis=1)
run = None
bands = []
for i, v in enumerate(rows):
    y = 330 + i
    if v > 1 and run is None:
        run = y
    elif v <= 1 and run is not None:
        bands.append((run, y-1)); run = None
if run is not None:
    bands.append((run, 499))
print("legend text bands:", bands)

# --- 4x4 input grid: colored cells x 550..750, y 340..490 ---
print("\n-- 4x4 input grid --")
for nm, pred in [("green", green), ("yellow", yellow), ("red-fill", lambda s: (s[:,:,0] > 180) & (s[:,:,1] < 90) & (s[:,:,2] < 90)), ("cyan", cyan)]:
    ink_bbox(540, 330, 760, 500, pred, f"grid {nm} cells")
# vertical/horizontal cell edges: find the grid columns by color-fill column profiles
seg = a[340:490, 540:760]
colored = green(seg) | yellow(seg) | (seg[:,:,0] > 180) & (seg[:,:,1] < 90) & (seg[:,:,2] < 90) | cyan(seg)
colcount = colored.sum(axis=0)
cc = np.nonzero(colcount > 20)[0]
if len(cc):
    print(f"grid colored cols x {540+cc.min()}..{540+cc.max()} n={len(cc)}")
rowcount = colored.sum(axis=1)
rr = np.nonzero(rowcount > 20)[0]
if len(rr):
    print(f"grid colored rows y {340+rr.min()}..{340+rr.max()} n={len(rr)}")
# fill samples per quadrant
print("fill samples TL/TR/BL/BR:", a[370, 580].tolist(), a[370, 700].tolist(), a[450, 580].tolist(), a[450, 700].tolist())

# --- arrow between grids ---
print("\n-- arrow + fraction + output grid --")
ink_bbox(720, 350, 790, 470, dark, "arrow dark ink")
ink_bbox(770, 350, 820, 470, red, "red 1/2 fraction ink")
ink_bbox(800, 340, 920, 500, green, "out-grid green cell")
ink_bbox(800, 340, 920, 500, yellow, "out-grid yellow cell")
ink_bbox(800, 340, 920, 500, lambda s: (s[:,:,0] > 180) & (s[:,:,1] < 90) & (s[:,:,2] < 90), "out-grid red cell")
ink_bbox(800, 340, 920, 500, cyan, "out-grid cyan cell")

# --- bottom strip ---
print("\n-- bottom strip --")
for y in (515, 520, 525, 530, 535, 538):
    dk = np.nonzero(a[y:y+1].sum(axis=2)[0] < 150)[0]
    print(f"  y={y}: dark n={len(dk)}", (int(dk.min()), int(dk.max())) if len(dk) else "")
