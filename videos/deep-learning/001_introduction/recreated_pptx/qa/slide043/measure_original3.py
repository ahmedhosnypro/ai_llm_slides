#!/usr/bin/env python3
"""Third forensics pass on slide_043.jpg: background map (gray vs white), blue box
borders, 3x3 + 1x1 orange-bordered cell rectangles, 5x5 border lines/colors,
number metrics, bullet markers, font fingerprints."""
import numpy as np
from PIL import Image, ImageFont

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_043.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def px(x, y):
    return '#%02X%02X%02X' % tuple(IM[y, x])

def modal(x0, x1, y0, y1, label):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    top = vals[np.argsort(-counts)[:3]]
    cnts = np.sort(counts)[::-1][:3]
    print(f"{label}: modal {['#%02X%02X%02X' % tuple(v) for v in top]} counts {list(cnts)}")

# ---------- background map ----------
print("--- background point samples ---")
pts = [
    (100, 60, "above inner panel, below chrome top"),
    (200, 100, "title row bg"),
    (880, 100, "title row bg right"),
    (100, 150, "bullets bg left"),
    (400, 150, "bullets bg mid"),
    (820, 150, "bullets bg right (inside inner panel)"),
    (870, 150, "between inner panel(845) and chrome right(~903)"),
    (895, 300, "same strip lower"),
    (460, 230, "between Image label and grid"),
    (460, 350, "between grids lower"),
    (470, 310, "beside arrow1"),
    (660, 350, "below arrow2/3x3"),
    (200, 386, "between inner panel bottom & box"),
    (500, 388, "same mid"),
    (200, 470, "inside blue box left"),
    (700, 470, "inside blue box right"),
    (100, 515, "below blue box, above black strip"),
    (930, 300, "canvas outside chrome right"),
    (46, 300, "canvas outside chrome left (x<57)"),
    (300, 522, "black strip row"),
]
for x, y, lbl in pts:
    print(f"  ({x:4d},{y:3d}) {lbl}: {px(x, y)}")

# ---------- blue box borders precise ----------
print("\n--- blue box ---")
blue = (b > 110) & (b > r + 25) & (b > g + 15)
for y in range(380, 525):
    xs2 = np.where(blue[y, 50:930])[0] + 50
    if len(xs2) > 150:
        print(f"  blue row y={y}: n={len(xs2)} x {xs2.min()}..{xs2.max()}")
for x in range(55, 100):
    ys2 = np.where(blue[380:525, x])[0] + 380
    if len(ys2) > 40:
        print(f"  blue col x={x}: n={len(ys2)} y {ys2.min()}..{ys2.max()}")
for x in range(855, 920):
    ys2 = np.where(blue[380:525, x])[0] + 380
    if len(ys2) > 40:
        print(f"  blue col x={x}: n={len(ys2)} y {ys2.min()}..{ys2.max()}")
modal(300, 700, 395, 398, "top border zone")
modal(300, 700, 508, 512, "bottom border zone")

# ---------- 3x3 + 18-cell: orange border profiling ----------
print("\n--- orange-ish border mask profiling (3x3 region x490..690 y235..375) ---")
orange = (r > 130) & (g > 70) & (g < 180) & (b < 120) & (r > b + 60)
om = np.zeros_like(orange)
om[235:375, 490:690] = orange[235:375, 490:690]
colprof = om.sum(axis=0)
cc = [int(c) for c in np.where(colprof > 25)[0]]
print("orange cols n>25:", cc)
rowprof = om.sum(axis=1)
rr = [int(c) for c in np.where(rowprof > 25)[0]]
print("orange rows n>25:", rr)
modal(530, 560, 246, 250, "3x3 cell top border zone sample")
print("\n--- 18-cell region x720..800 y280..330 ---")
om2 = np.zeros_like(orange)
om2[280:330, 720:800] = orange[280:330, 720:800]
ys2, xs2 = np.where(om2)
if len(ys2):
    print(f"18-cell orange border bbox: x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()}")

# ---------- 5x5 border lines ----------
print("\n--- 5x5 border profiling (dark<170, x238..445 y222..382) ---")
darkish = (r < 170) & (g < 170) & (b < 170)
dm = np.zeros_like(darkish)
dm[222:382, 238:445] = darkish[222:382, 238:445]
colprof = dm.sum(axis=0)
cc = [int(c) for c in np.where(colprof > 80)[0]]
print("dark cols n>80:", cc)
rowprof = dm.sum(axis=1)
rr = [int(c) for c in np.where(rowprof > 80)[0]]
print("dark rows n>80:", rr)
modal(250, 270, 256, 259, "5x5 horiz border sample (y~257, between rows 0/1, away from numbers)")
modal(283, 286, 240, 250, "5x5 vert border sample (x~284, between cols 0/1)")

# ---------- number metrics ----------
print("\n--- number ink heights (5x5 digits '1','0'; 3x3 digits; '18') ---")
dark = (r < 100) & (g < 100) & (b < 100)
def ink(x0, x1, y0, y1, label):
    m = np.zeros_like(dark)
    m[y0:y1, x0:x1] = dark[y0:y1, x0:x1]
    ys2, xs2 = np.where(m)
    if not len(ys2):
        print(f"{label}: EMPTY")
        return
    print(f"{label}: x {x0+xs2.min()}..{x0+xs2.max()} y {y0+ys2.min()}..{y0+ys2.max()} "
          f"(w {xs2.max()-xs2.min()+1} h {ys2.max()-ys2.min()+1})")
ink(255, 275, 230, 256, "5x5 (0,0) '1'")
ink(293, 315, 230, 256, "5x5 (0,1) '1'")
ink(410, 432, 230, 256, "5x5 (0,4) '0'")
ink(255, 275, 290, 318, "5x5 (2,0) '0'")
ink(524, 545, 252, 276, "3x3 (0,0) '4'")
ink(577, 597, 252, 276, "3x3 (0,1) '3'")
ink(748, 780, 294, 318, "1x1 '18'")

# ---------- bullet markers ----------
print("\n--- bullet markers (hollow circles, x115..150) ---")
panelish = (np.abs(r-233) < 20) & (np.abs(g-233) < 20) & (np.abs(b-231) < 20)
darkm = (r < 170) & (g < 170) & (b < 170)
nonbg = ~panelish & ~darkm & ~((r > 245) & (g > 245) & (b > 245))
mm = np.zeros_like(nonbg)
mm[115:210, 115:150] = nonbg[115:210, 115:150]
proj = mm.sum(axis=1)
idx = np.where(proj > 1)[0]
bands = []
if len(idx):
    s = p = idx[0]
    for c in idx[1:]:
        if c - p <= 3:
            p = c
        else:
            bands.append((int(s), int(p)))
            s = p = c
    bands.append((int(s), int(p)))
print("marker row bands:", bands)
for (y0, y1) in bands:
    m = mm[y0:y1+1]
    xs2 = np.where(m.sum(axis=0) > 0)[0] + 115
    print(f"  marker y {y0}..{y1}: x {xs2.min()}..{xs2.max()} (h {y1-y0+1} w {xs2.max()-xs2.min()+1})")
    cx = (xs2.min() + xs2.max()) // 2
    modal(cx-2, cx+2, (y0+y1)//2 - 1, (y0+y1)//2 + 1, f"  marker@{y0} color")

# ---------- font fingerprints ----------
print("\n--- font fingerprints ---")
FONTS = {
    "TimesB": "/usr/share/fonts/TTF/Timesb.ttf",
    "Times": "/usr/share/fonts/TTF/Times.ttf",
    "ArialB": "/usr/share/fonts/TTF/Arialbd.TTF",
    "Arial": "/usr/share/fonts/TTF/Arial.TTF",
    "GeorgiaB": "/usr/share/fonts/TTF/Georgiab.ttf",
    "Comic": "/usr/share/fonts/truetype/comic/ComicNeue-Regular.ttf",
}
import os
for k, v in list(FONTS.items()):
    if not os.path.exists(v):
        print(f"  (missing {k}: {v})")

def solve(text, target_w, fonts, bold_only=False, lo=100, hi=400):
    results = []
    for name, path in fonts.items():
        if not os.path.exists(path):
            continue
        best = None
        for s10 in range(lo, hi):
            f = ImageFont.truetype(path, s10)
            bb = f.getbbox(text)
            w = bb[2] - bb[0]
            if best is None or abs(w - target_w * 10) < best[0]:
                best = (abs(w - target_w * 10), s10 / 10.0, w / 10.0)
        results.append((best[0] / 10.0, name, best[1], best[2]))
    results.sort()
    for err, name, size, w in results:
        print(f"  {name}: best {size:.1f}pt -> w {w:.1f} (target {target_w}, err {err:.1f}px)")

print("TITLE 'Problem: Image will vanish  if applying more filters in cascade' target 768:")
solve("Problem: Image will vanish  if applying more filters in cascade", 768,
      {k: v for k, v in FONTS.items() if k in ("TimesB", "ArialB", "GeorgiaB")}, lo=200, hi=420)
print("word fingerprint 'Problem:' target 126:")
solve("Problem:", 126, {k: v for k, v in FONTS.items() if k in ("TimesB", "ArialB", "GeorgiaB")}, lo=200, hi=420)
print("word fingerprint 'cascade' target 90:")
solve("cascade", 90, {k: v for k, v in FONTS.items() if k in ("TimesB", "ArialB", "GeorgiaB")}, lo=200, hi=420)

print("BULLET1 'Our images get smaller and smaller' target 350 (x148..497):")
solve("Our images get smaller and smaller", 350,
      {k: v for k, v in FONTS.items() if k in ("Times", "Arial")}, lo=120, hi=300)
print("BULLET2 'Not too deep architectures' target 267 (x149..415):")
solve("Not too deep architectures", 267,
      {k: v for k, v in FONTS.items() if k in ("Times", "Arial")}, lo=120, hi=300)
print("BULLET3 'Details are lost' target 141 (x149..289):")
solve("Details are lost", 141,
      {k: v for k, v in FONTS.items() if k in ("Times", "Arial")}, lo=120, hi=300)

print("NAVY L2 'After apply one filter  of size 3x3, output will be3x3' target 445 (x89..533):")
solve("After apply one filter  of size 3x3, output will be3x3", 445,
      {k: v for k, v in FONTS.items() if k in ("Times", "TimesB", "Arial", "ArialB")}, lo=120, hi=320)
print("NAVY L1 bold 'Original 5x5' target 111 (x88..198):")
solve("Original 5x5", 111,
      {k: v for k, v in FONTS.items() if k in ("Times", "TimesB", "Arial", "ArialB")}, lo=120, hi=320)
print("NAVY L3 'After applying second filter on the output (cascaded filters)' target 499 (x88..586):")
solve("After applying second filter on the output (cascaded filters)", 499,
      {k: v for k, v in FONTS.items() if k in ("Times", "Arial")}, lo=120, hi=320)
print("NAVY L4 'Output will be 1x1' target 154 (x88..241):")
solve("Output will be 1x1", 154,
      {k: v for k, v in FONTS.items() if k in ("Times", "Arial")}, lo=120, hi=320)
