#!/usr/bin/env python3
"""forensics6.py — independent re-measurement of slide_045.jpg (verify dead builders' numbers).
960x540, 1px = 1pt. Outputs banked to qa/slide045/forensics6_out.txt."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

# masks
red_soft = (r > 130) & (r - g > 40) & (r - b > 30)          # red strokes/text (loose)
red_strict = (r > 150) & (g < 100) & (b < 100)
blue_soft = (b > 130) & (b - r > 30) & (b - g > 20)          # blue strokes
yellow = (r > 200) & (g > 170) & (b < 200) & (r - b > 40)    # pale yellow fill
dark = (r < 120) & (g < 120) & (b < 120)                      # black text/ink

print("== BOX BORDERS: full-width/col stroke scans ==")
# horizontal strokes: rows where red_soft or blue_soft spans wide
for name, mask, x0, x1, y0, y1, thr in [
    ("defbox", blue_soft, 80, 880, 105, 220, 600),
    ("remember", red_soft, 80, 880, 218, 290, 600),
    ("eqpanel", red_soft, 300, 690, 280, 510, 300),
    ("legend", blue_soft, 80, 255, 345, 445, 120),
    ("calloutW", blue_soft, 740, 890, 355, 400, 100),
    ("calloutI", blue_soft, 740, 875, 412, 460, 100),
]:
    rows = np.where(mask[y0:y1, x0:x1].sum(axis=1) >= thr)[0] + y0
    print(f" {name} h-strokes: {runs(rows)}")
    cols = np.where(mask[y0:y1, x0:x1].sum(axis=0) >= (y1 - y0) * 0.55)[0] + x0
    print(f" {name} v-strokes(55%): {runs(cols)}")
    cols2 = np.where(mask[y0:y1, x0:x1].sum(axis=0) >= (y1 - y0) * 0.30)[0] + x0
    print(f" {name} v-strokes(30%): {runs(cols2)}")

print("\n== TITLE band + underline ==")
tb = dark[60:110, 150:930]
rows = np.where(tb.sum(axis=1) > 3)[0] + 60
print(" title ink rows:", runs(rows))
cols = np.where(tb.sum(axis=0) > 0)[0] + 150
print(" title ink cols:", runs(cols))
# red underline (solid red row under title)
for y in range(88, 105):
    n = red_strict[y, 500:800].sum()
    if n > 50: print(f" underline row y={y} x-run:", runs(np.where(red_strict[y, 150:930])[0] + 150), "n=", n)

print("\n== STARBURST (region x770..930 y30..160, excluding chrome rows y<48) ==")
ys, xs = np.where(yellow[48:160, 770:930])
if len(ys): print(f" yellow bbox: x{xs.min()+770}..{xs.max()+770} y{ys.min()+48}..{ys.max()+48} n={len(ys)}")
else: print(" yellow: NONE in region")
ys, xs = np.where(red_soft[48:160, 780:930])
if len(ys): print(f" red-spike bbox: x{xs.min()+780}..{xs.max()+780} y{ys.min()+48}..{ys.max()+48} n={len(ys)}")
# red text 'Important' inside starburst (strict red on yellow/white)
ys, xs = np.where(red_strict[48:160, 780:930])
if len(ys): print(f" red-strict bbox: x{xs.min()+780}..{xs.max()+780} y{ys.min()+48}..{ys.max()+48} n={len(ys)}")
# yellow sample colors
samp = im[95:105, 820:860].reshape(-1, 3)
print(" starburst fill modal:", {tuple(k): int(v) for k, v in zip(*np.unique(samp, axis=0, return_counts=True))} if len(samp) else {})

print("\n== BULLET circles + text (eqpanel interior x300..690) ==")
for (ya, yb, label) in [(292, 315, "b1"), (370, 396, "b2"), (418, 448, "b3")]:
    band = red_soft[ya:yb, 296:340] | dark[ya:yb, 296:340]
    ys, xs = np.where(band)
    if len(ys): print(f" {label} circle/text-left bbox: x{xs.min()+296}..{xs.max()+296} y{ys.min()+ya}..{ys.max()+ya} n={len(ys)}")
    band2 = dark[ya:yb, 340:690] | red_soft[ya:yb, 340:690]
    ys, xs = np.where(band2)
    if len(ys): print(f" {label} text-right bbox: x{xs.min()+340}..{xs.max()+340} y{ys.min()+ya}..{ys.max()+ya} n={len(ys)}")

print("\n== EQUATION ink bboxes (dark math ink, x340..695 interior) ==")
for (ya, yb, label) in [(300, 372, "eq(a)"), (388, 421, "eq(b)"), (421, 497, "eq(c)")]:
    band = dark[ya:yb, 440:695]
    ys, xs = np.where(band)
    if len(ys):
        print(f" {label}: x{xs.min()+440}..{xs.max()+440} y{ys.min()+ya}..{ys.max()+ya} w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1} n={len(ys)}")
        rows = np.where(band.sum(axis=1) > 0)[0] + ya
        print(f"   {label} row-bands: {runs(rows)}")

print("\n== ARROWS (loose red in x620..745 y300..470, excluding panel border x697..704 & callout borders x>732) ==")
mask = red_soft.copy()
mask[:, 695:706] = False   # panel right border
mask[:, 731:] = False      # callout zone
ys, xs = np.where(mask[300:470, 620:731])
if len(ys):
    print(f" arrow-stroke bbox: x{xs.min()+620}..{xs.max()+620} y{ys.min()+300}..{ys.max()+300} n={len(ys)}")
    for yy in range(ys.min() + 300, ys.max() + 301, 4):
        rr = np.where(mask[yy, 620:731])[0] + 620
        if len(rr): print(f"   y={yy}: x{rr.min()}..{rr.max()} n={len(rr)}")
else:
    print(" NO arrow strokes found in corridor")

print("\n== DEFBOX text lines (x80..880, y115..208) ==")
band = dark[115:208, 80:880]
rows = np.where(band.sum(axis=1) > 2)[0] + 115
print(" defbox text rows:", runs(rows))
cols = np.where(band.sum(axis=0) > 0)[0] + 80
print(" defbox text col-extent:", cols.min(), "..", cols.max())
# bold-term check: line 3 leading 'Input' — sample color of line1 text core
samp = im[125:135, 90:400].reshape(-1, 3)
m = samp[(samp.sum(axis=1) < 400)]
if len(m): print(" defbox text dark-core modal:", tuple(np.median(m, axis=0).astype(int)))

print("\n== REMEMBER text lines (x80..880, y228..276) ==")
band = red_soft[228:276, 80:880]
rows = np.where(band.sum(axis=1) > 2)[0] + 228
print(" remember text rows:", runs(rows))
cols = np.where(band.sum(axis=0) > 0)[0] + 80
print(" remember text col-extent:", cols.min(), "..", cols.max())
samp = im[235:246, 90:800].reshape(-1, 3)
m = samp[(r := samp[:, 0]) > 100]
if len(m): print(" remember text modal:", tuple(np.median(m, axis=0).astype(int)))

print("\n== LEGEND text lines (x76..258, y356..432) ==")
band = dark[356:432, 76:258]
rows = np.where(band.sum(axis=1) > 2)[0] + 356
print(" legend text rows:", runs(rows))
cols = np.where(band.sum(axis=0) > 0)[0] + 76
print(" legend text col-extent:", cols.min(), "..", cols.max())
samp = im[400:430, 120:240].reshape(-1, 3)
print(" legend fill modal:", {tuple(k): int(v) for k, v in list(zip(*np.unique(samp, axis=0, return_counts=True)))[:2]})

print("\n== CALLOUT text ==")
for (ya, yb, xa, xb, label) in [(364, 391, 736, 895, "weights"), (422, 449, 735, 878, "input")]:
    band = dark[ya:yb, xa:xb]
    ys, xs = np.where(band)
    if len(ys): print(f" {label}: x{xs.min()+xa}..{xs.max()+xa} y{ys.min()+ya}..{ys.max()+ya} n={len(ys)}")

print("\n== BLACK BAR (bottom) ==")
rows = np.where(dark[500:540, 100:900].sum(axis=1) > 700)[0] + 500
print(" black-bar rows:", runs(rows))
