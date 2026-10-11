#!/usr/bin/env python3
"""Pass 3: text ink bands (red title/subtitle/captions, olive labels, math text)
+ red dots + new blue callout / gray summary boxes in slide_009.jpg."""
from PIL import Image
import numpy as np
from scipy import ndimage

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(IM).convert("RGB"), dtype=np.int16)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def ink_bands(name, m, axis="y", y0=0, y1=540, x0=0, x1=960, min_run=2):
    """Print row (or col) ink bands of mask m inside a window."""
    win = m[y0:y1, x0:x1]
    if axis == "y":
        prof = win.sum(axis=1)
        runs = []
        s = None
        for i, v in enumerate(prof):
            if v >= min_run and s is None: s = i
            elif v < min_run and s is not None:
                runs.append((s + y0, i + y0)); s = None
        if s is not None: runs.append((s + y0, y1))
        print(f"  {name} rows: {runs}")
    else:
        prof = win.sum(axis=0)
        runs = []
        s = None
        for i, v in enumerate(prof):
            if v >= min_run and s is None: s = i
            elif v < min_run and s is not None:
                runs.append((s + x0, i + x0)); s = None
        if s is not None: runs.append((s + x0, x1))
        print(f"  {name} cols: {runs}")

def bbox(name, m, y0=0, y1=540, x0=0, x1=960):
    win = m[y0:y1, x0:x1]
    ys, xs = np.where(win)
    if len(ys) == 0:
        print(f"  {name}: EMPTY")
        return None
    r = (int(xs.min()) + x0, int(ys.min()) + y0, int(xs.max()) + 1 + x0, int(ys.max()) + 1 + y0)
    print(f"  {name}: x{r[0]}..{r[2]} y{r[1]}..{r[3]} (w{r[2]-r[0]} h{r[3]-r[1]})")
    return r

# red ink (title/captions/labels): strong red, low G/B
red = (R > 120) & (G < 90) & (B < 90)
# dark red variants
red2 = (R > 100) & (R - G > 60) & (R - B > 60)
redm = red | red2

print("== TITLE AREA (y40..120, x100..700) ==")
ink_bands("red title rows", redm, "y", 40, 120, 100, 700)
# line1 cols
ink_bands("title L1 cols", redm, "x", 50, 82, 100, 700)
ink_bands("title L2 cols", redm, "x", 84, 115, 100, 700)

print("== BADGE/DECODER LABEL (y80..115, x600..920) ==")
ink_bands("dec caption rows", redm, "y", 80, 118, 600, 880)
ink_bands("dec caption cols", redm, "x", 84, 115, 600, 880)

print("== ENCODER CAPTION (y495..535, x100..500) ==")
ink_bands("enc caption rows", redm, "y", 495, 535, 100, 500)
ink_bands("enc caption cols", redm, "x", 502, 530, 100, 500)

print("== RED DOTS (decoder first-hidden / encoder final) ==")
# saturated red small blobs
dot = (R > 150) & (G < 70) & (B < 70)
lab, n = ndimage.label(dot, structure=np.ones((3, 3)))
objs = ndimage.find_objects(lab)
for i, sl in enumerate(objs):
    ys, xs = sl
    area = int((lab[sl] == i + 1).sum())
    if area >= 12:
        print(f"  red blob: x{xs.start}..{xs.stop} y{ys.start}..{ys.stop} (w{xs.stop-xs.start} h{ys.stop-ys.start}) area={area}")

print("== BLUE CALLOUT (new) — blue ink + fill ==")
blueink = (B > 120) & (B - R > 70) & (B - G > 60)
bfill = (np.abs(R - 204) < 18) & (np.abs(G - 228) < 18) & (np.abs(B - 247) < 18)
bbox("blue callout fill", bfill, 120, 200, 80, 470)
ink_bands("callout fill rows", bfill, "y", 120, 200, 80, 470)
ink_bands("callout fill cols", bfill, "x", 125, 195, 80, 470)
ink_bands("blue text rows", blueink, "y", 120, 200, 80, 470)
ink_bands("blue text L1 cols", blueink, "x", 140, 162, 80, 470)
ink_bands("blue text L2 cols", blueink, "x", 163, 185, 80, 470)

print("== GRAY SUMMARY BOX (new) ==")
graybox = (np.abs(R - 217) < 12) & (np.abs(G - 217) < 12) & (np.abs(B - 217) < 12)
bbox("gray box fill", graybox, 195, 300, 40, 470)
ink_bands("gray box rows", graybox, "y", 195, 300, 40, 470)
ink_bands("gray box cols", graybox, "x", 200, 295, 40, 470)
# text inside: dark navy / green / red inks
navy = (R < 90) & (G < 90) & (B > 90) & (B - R > 40)
green = (G > 110) & (G - R > 50) & (G - B > 30)
redink = redm
print("  navy rows:", end=" "); ink_bands("navy", navy, "y", 200, 295, 60, 445)
print("  green rows:", end=" "); ink_bands("green", green, "y", 200, 295, 60, 445)
ink_bands("summary red (FAIL)", redm, "y", 200, 295, 60, 445)
ink_bands("summary navy L1 cols", navy, "x", 210, 232, 60, 445)
ink_bands("summary navy L2 cols", navy, "x", 236, 258, 60, 445)
ink_bands("summary navy L3 cols", navy, "x", 262, 284, 60, 445)
ink_bands("summary green L1 cols", green, "x", 210, 232, 60, 445)
ink_bands("summary green L2 cols", green, "x", 236, 258, 60, 445)
ink_bands("summary red L3 cols", redm, "x", 262, 284, 60, 445)

print("== OLIVE MATH LABELS (decoder o/s/softmax) ==")
olive = (R > 110) & (R < 200) & (G > 110) & (G < 200) & (B < 90) & (R - B > 60) & (G - B > 60)
ink_bands("dec o-labels rows", olive, "y", 118, 145, 480, 915)
ink_bands("dec s-labels rows", olive, "y", 270, 295, 480, 915)
ink_bands("dec softmax rows", olive, "y", 160, 200, 480, 915)
ink_bands("dec o1 cols", olive, "x", 120, 142, 480, 915)
ink_bands("dec s1 cols", olive, "x", 276, 295, 480, 915)

print("== ENCODER LABELS ==")
enclab = (np.abs(R - 143) < 45) & (np.abs(G - 110) < 45) & (np.abs(B - 68) < 45)
ink_bands("enc h-labels rows", enclab, "y", 300, 322, 50, 500)
ink_bands("enc h-label cols h1", enclab, "x", 305, 325, 190, 260)
ink_bands("enc emb rows", enclab, "y", 355, 385, 50, 500)
ink_bands("enc x-labels rows", enclab, "y", 465, 495, 50, 500)
