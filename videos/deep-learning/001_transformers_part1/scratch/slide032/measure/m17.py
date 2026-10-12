# m17.py — fresh frame-vs-render_2 measurements for the selfcheck-1b FIX items.
# Windows are chosen tight and printed with per-row/column detail where the
# earlier banked logs were ambiguous (title top rows, out-row left ink, band right).
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
RN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide032/render_2.png"
f = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r = np.asarray(Image.open(RN).convert("RGB")).astype(int)
S = r.shape[1] / f.shape[1]

def ink(img, x0, y0, x1, y1, thr=68):
    reg = img[y0:y1, x0:x1]
    mx = reg.max(axis=2); mn = reg.min(axis=2); sat = mx - mn
    white = (mx >= 238) & (sat <= 14)
    gray = (np.abs(reg[:, :, 0] - reg[:, :, 1]) <= 8) & (np.abs(reg[:, :, 1] - reg[:, :, 2]) <= 8) & (mx >= 200) & (mx < 246)
    m = ~(white | gray)
    ys, xs = np.where(m)
    if len(xs) == 0: return None
    return (int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0, int(m.sum()))

def colmask(img, x0, y0, x1, y1, target, tol=40):
    reg = img[y0:y1, x0:x1]
    d = np.abs(reg - np.array(target)).sum(axis=2)
    m = d < tol * 3
    ys, xs = np.where(m)
    if len(xs) == 0: return None
    return (int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + x0, int(ys.max()) + y0, int(m.sum()))

def cmp(name, fb, rb):
    if fb is None or rb is None:
        print(f"{name:24s} MISSING frame={fb} render={rb}"); return
    d = [rb[i] / S - fb[i] for i in range(4)]
    worst = max(abs(v) for v in d)
    print(f"{name:24s} frame=({fb[0]},{fb[1]},{fb[2]},{fb[3]}) n={fb[4]:6d}  render=({rb[0]:6.1f},{rb[1]:6.1f},{rb[2]:6.1f},{rb[3]:6.1f}) n={rb[4]:6d}  d=({d[0]:+.1f},{d[1]:+.1f},{d[2]:+.1f},{d[3]:+.1f}) worst={worst:.1f}")

print("== eq panel border (dark red ink, excl. contents window is whole panel) ==")
cmp("eq panel", ink(f, 40, 55, 485, 295), ink(r, int(40 * S), int(55 * S), int(485 * S), int(295 * S)))
# columns of the border stroke at a content-free row (y=75, above matrix top)
for img, nm in ((f, "frame"), (r, "render")):
    row = img[75, 40:485]
    mx = row.max(axis=1); mn = row.min(axis=1); sat = mx - mn
    white = (mx >= 238) & (sat <= 14)
    m = ~white
    xs = np.where(m)[0] + 40
    print(f"  {nm} border cols @y75: {list(xs)}")

print("== matrix pink region (color mask pink ~F7C7CB) ==")
cmp("matrix pink", colmask(f, 200, 70, 395, 275, (247, 199, 203), 45), None)
rb_m = colmask(r, int(200 * S), int(70 * S), int(395 * S), int(275 * S), (247, 199, 203), 45)
if rb_m: print(f"  render pink bbox=({rb_m[0]:.0f},{rb_m[1]:.0f},{rb_m[2]:.0f},{rb_m[3]:.0f}) n={rb_m[4]} (frame-scale)")

print("== title detail: per-row ink + mean color, frame x555..870 ==")
for y in range(108, 148, 2):
    row = f[y, 555:870]
    mx = row.max(axis=1); mn = row.min(axis=1); sat = mx - mn
    white = (mx >= 238) & (sat <= 14)
    m = ~white
    n = int(m.sum())
    if n:
        mean = row[m].mean(axis=0).astype(int)
        xs = np.where(m)[0] + 555
        print(f"  f y={y}: n={n:3d} x {xs.min()}..{xs.max()} mean={tuple(mean)}")

print("== title bbox compare (window 555..870 x 105..148) ==")
cmp("title", ink(f, 555, 105, 870, 148), ink(r, int(555 * S), int(105 * S), int(870 * S), int(148 * S)))

print("== arrow bbox (window 465..575 x 128..252) ==")
cmp("arrow", ink(f, 465, 128, 575, 252), ink(r, int(465 * S), int(128 * S), int(575 * S), int(252 * S)))
# frame arrow: row profile of left edge for the tail
for img, nm in ((f, "frame"), (r, "render")):
    prof = []
    for y in (150, 155, 160, 170, 200, 220, 235):
        reg = img[y, 465:575]
        mx = reg.max(axis=1); mn = reg.min(axis=1); sat = mx - mn
        white = (mx >= 238) & (sat <= 14)
        m = ~white
        xs = np.where(m)[0]
        prof.append(f"y{y}:{(xs.min()+465) if len(xs) else '-'}..{(xs.max()+465) if len(xs) else '-'}")
    print(f"  {nm} arrow rows:", " ".join(prof))

print("== band right region (window 800..905 x 300..440) ==")
cmp("band right ink", ink(f, 800, 300, 905, 440), ink(r, int(800 * S), int(300 * S), int(905 * S), int(440 * S)))
for img, nm in ((f, "frame"), (r, "render")):
    cols = []
    for x in range(884, 900):
        col = img[320:420, x]
        mx = col.max(axis=1); mn = col.min(axis=1); sat = mx - mn
        white = (mx >= 238) & (sat <= 14)
        gray = (np.abs(col[:, 0] - col[:, 1]) <= 8) & (np.abs(col[:, 1] - col[:, 2]) <= 8) & (mx >= 200) & (mx < 246)
        m = ~(white | gray)
        if m.any(): cols.append(x)
    print(f"  {nm} ink cols 884..900: {cols}")

print("== stair labels (tight windows, color-specific) ==")
LBL = {"red": (168, 64, 78), "blue": (50, 37, 158), "green": (78, 142, 77)}
lbls = [
    ("W11", 510, 312, 542, 332, "red"), ("W12", 568, 324, 600, 344, "red"),
    ("W13", 611, 340, 643, 360, "red"), ("W14", 685, 370, 717, 392, "red"),
    ("b1", 624, 312, 656, 334, "blue"), ("b2", 665, 330, 697, 352, "blue"),
    ("b3", 702, 348, 734, 372, "blue"), ("b4", 750, 376, 782, 398, "blue"),
    ("W41", 756, 320, 788, 342, "green"), ("W42", 782, 336, 814, 358, "green"),
    ("W43", 810, 355, 842, 378, "green"), ("W44", 843, 380, 875, 404, "green"),
    ("WQ", 488, 360, 534, 402, "red"),
]
for nm, x0, y0, x1, y1, col in lbls:
    fb = colmask(f, x0, y0, x1, y1, LBL[col], 60)
    rb = colmask(r, int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S), LBL[col], 60)
    if fb is None:
        print(f"  {nm:4s} frame MISSING in window"); continue
    if rb is None:
        print(f"  {nm:4s} frame=({fb[0]},{fb[1]},{fb[2]},{fb[3]}) n={fb[4]:4d}  render MISSING")
        continue
    w_f = fb[2] - fb[0]; h_f = fb[3] - fb[1]
    w_r = (rb[2] - rb[0]) / S; h_r = (rb[3] - rb[1]) / S
    print(f"  {nm:4s} frame=({fb[0]},{fb[1]},{fb[2]},{fb[3]}) {w_f}x{h_f}  render={w_r:.1f}x{h_r:.1f} @({rb[0]/S:.1f},{rb[1]/S:.1f})")

print("== out circles row (clean window 512..890 x 252..314) ==")
cmp("out row", ink(f, 512, 252, 890, 314), ink(r, int(512 * S), int(252 * S), int(890 * S), int(314 * S)))
print("== mystery: frame ink x478..545 y246..314 (left of first circle) ==")
fb = ink(f, 478, 246, 545, 314)
rb = ink(r, int(478 * S), int(246 * S), int(545 * S), int(314 * S))
print(f"  frame={fb}  render={None if rb is None else tuple(round(v/S,1) if i<4 else v for i,v in enumerate(rb))}")
for y in (250, 260, 270, 280, 290, 300):
    row = f[y, 478:545]
    mx = row.max(axis=1); mn = row.min(axis=1); sat = mx - mn
    white = (mx >= 238) & (sat <= 14)
    m = ~white
    xs = np.where(m)[0]
    if len(xs):
        px = row[m]
        print(f"  f y={y}: n={len(xs)} x {xs.min()+478}..{xs.max()+478} mean={tuple(px.mean(axis=0).astype(int))}")
