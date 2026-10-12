#!/usr/bin/env python3
"""Self-check 1 — render_1.png (2001x1125 @150dpi) vs original slide_047.jpg measurements.
Scale: 2001/960 = 2.0844. All targets below are ORIGINAL px multiplied by S."""
from PIL import Image
import numpy as np

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide047/render_1.png"
S = 2001 / 960.0
im = Image.open(REN).convert("RGB")
a = np.asarray(im).astype(int)
print(f"render {im.size}, scale S={S:.4f}")

def t(v):  # original px -> render px
    return v * S

def bbox(x0, y0, x1, y1, pred, label, tgt=None):
    sub = a[int(y0):int(y1), int(x0):int(x1)]
    m = pred(sub)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(f"{label:30s} EMPTY"); return None
    r = (x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max())
    extra = ""
    if tgt:
        d = [round((r[i] - t(tgt[i])) / S, 1) for i in range(4)]
        extra = f"  vs orig {tgt} delta(px@orig): {d}"
    print(f"{label:30s} x {r[0]}..{r[2]} y {r[1]}..{r[3]}{extra}")
    return r

red   = lambda s: (s[:,:,0] > 120) & (s[:,:,0] - s[:,:,1] > 60) & (s[:,:,0] - s[:,:,2] > 60)
dark  = lambda s: (s.sum(axis=2) < 330)
blue  = lambda s: (s[:,:,2] > 110) & (s[:,:,2] - s[:,:,0] > 50) & (s[:,:,2] - s[:,:,1] > 40)
notred = lambda s: ~red(s)
dk_notred = lambda s: (s.sum(axis=2) < 330) & notred(s)
green = lambda s: (s[:,:,1] > 120) & (s[:,:,1] - s[:,:,0] > 40) & (s[:,:,1] - s[:,:,2] > 40)
yellow= lambda s: (s[:,:,0] > 180) & (s[:,:,1] > 170) & (s[:,:,2] < 130)
redf  = lambda s: (s[:,:,0] > 180) & (s[:,:,1] < 90) & (s[:,:,2] < 90)
cyan  = lambda s: (s[:,:,2] > 150) & (s[:,:,1] > 120) & (s[:,:,0] < 140) & (s[:,:,2] - s[:,:,0] > 60)

print("\n-- L-frame lines --")
bbox(100, 0, 1950, 100, red, "top hairline", (58, 43, 901, 43))
sub = a[:, int(t(57)):int(t(61))]
rm = red(sub)
ys = np.nonzero(rm.any(axis=1))[0]
print(f"left line x=58: y {ys.min()/S:.0f}..{ys.max()/S:.0f} (orig target 45..513)")

print("\n-- black bar --")
for y in (int(t(519)), int(t(530))):
    dk = np.nonzero(a[y].sum(axis=1) < 150)[0]
    print(f"  y={y}: dark n={len(dk)}", (int(dk.min()), int(dk.max())) if len(dk) else "")

print("\n-- content box borders --")
sub = a[int(t(215)):int(t(490)), int(t(75)):int(t(880))]
rm = red(sub)
rowcount = rm.sum(axis=1)
rows = [int(t(215)) + i for i, c in enumerate(rowcount) if c > 400]
print("  border rows:", rows[:6], "target", [round(t(219)), round(t(486))])
colcount = rm.sum(axis=0)
cols = [int(t(75)) + j for j, c in enumerate(colcount) if c > 130]
print("  border cols:", cols[:8], "target", [round(t(82)), round(t(874))])

print("\n-- title --")
r = bbox(int(t(60)), int(t(55)), int(t(900)), int(t(110)), red, "title red ink", (140, 72, 825, 92))
b = bbox(int(t(60)), int(t(55)), int(t(900)), int(t(110)), blue, "title blue ink", (448, 67, 542, 100))

print("\n-- intro lines --")
sub = a[int(t(120)):int(t(215)), int(t(60)):int(t(900))]
m = (sub.sum(axis=2) < 520)
rows = m.sum(axis=1)
run = None
for i, v in enumerate(rows):
    y = int(t(120)) + i
    if v > 4 and run is None: run = y
    elif v <= 4 and run is not None:
        seg = a[run:y, int(t(60)):int(t(900))]
        mm = (seg.sum(axis=2) < 520)
        ys2, xs2 = np.nonzero(mm)
        print(f"  line y {run/S:.1f}..{(y-1)/S:.1f} x {xs2.min()/S:.0f}..{xs2.max()/S:.0f}")
        run = None

print("\n-- bullets --")
bbox(int(t(90)), int(t(222)), int(t(560)), int(t(248)), dk_notred, "bullet1 ink", (116, 226, 475, 242))
bbox(int(t(90)), int(t(252)), int(t(560)), int(t(276)), dk_notred, "bullet2 ink", (116, 258, 529, 268))
# rings
seg = a[int(t(225)):int(t(345)), int(t(88)):int(t(106))]
mm = (seg.sum(axis=2) < 700)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    yy = np.sort(np.unique(ys2))
    splits = np.nonzero(np.diff(yy) > 3)[0]
    start = 0
    bands = []
    for idx in list(splits) + [len(yy)-1]:
        bands.append((int(t(225)+yy[start]), int(t(225)+yy[idx]))); start = idx+1
    print(f"  rings y-bands(orig): {[(round(b0/S,1), round(b1/S,1)) for b0,b1 in bands]}  target 229-238/259-269/294-304/333-343")

print("\n-- label boxes --")
bbox(int(t(100)), int(t(282)), int(t(320)), int(t(318)), blue, "box1 blue", (109, 287, 311, 313))
bbox(int(t(100)), int(t(318)), int(t(320)), int(t(356)), blue, "box2 blue", (109, 323, 311, 351))
bbox(int(t(112)), int(t(288)), int(t(308)), int(t(310)), dk_notred, "box1 text", (114, 291, 307, 303))
bbox(int(t(112)), int(t(326)), int(t(308)), int(t(346)), dk_notred, "box2 text", (114, 330, 307, 342))

print("\n-- EQUATIONS closed-loop (ink bands) --")
# eq3 region
e3 = bbox(int(t(310)), int(t(268)), int(t(560)), int(t(322)), dk_notred, "eq3 ink", (317, 284, 536, 312))
# eq4 region
e4 = bbox(int(t(312)), int(t(315)), int(t(470)), int(t(368)), dk_notred, "eq4 ink", (320, 321, 428, 359))

print("\n-- legend --")
lightblue = lambda s: (s[:,:,2] > 200) & (s[:,:,0] > 150) & (s[:,:,0] < 240) & (s[:,:,2] - s[:,:,0] > 15)
bbox(int(t(445)), int(t(340)), int(t(580)), int(t(485)), lightblue, "legend fill", (455, 348, 566, 475))
sub = a[int(t(350)):int(t(480)), int(t(460)):int(t(570))]
mm = (sub.sum(axis=2) < 500)
rows = mm.sum(axis=1)
run = None
bands = []
for i, v in enumerate(rows):
    y = int(t(350)) + i
    if v > 2 and run is None: run = y
    elif v <= 2 and run is not None:
        bands.append((run, y-1)); run = None
if run is not None: bands.append((run, int(t(480))))
print("  text bands(orig):", [(round(b0/S,1), round(b1/S,1)) for b0,b1 in bands], "target 357-368/377-388/396-407/415-430/435-450/454-466")

print("\n-- input grid --")
sub = a[int(t(355)):int(t(495)), int(t(560)):int(t(740))]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
ys2, xs2 = np.nonzero(colored)
print(f"  grid bbox(orig): x {(int(t(560))+xs2.min())/S:.0f}..{(int(t(560))+xs2.max())/S:.0f} y {(int(t(355))+ys2.min())/S:.0f}..{(int(t(355))+ys2.max())/S:.0f}  target 571..726 / 365..483")
# numerals ink
mm = (sub.sum(axis=2) < 260) & notred(sub)
ys2, xs2 = np.nonzero(mm)
if len(xs2):
    print(f"  numerals(orig): x {(int(t(560))+xs2.min())/S:.0f}..{(int(t(560))+xs2.max())/S:.0f} y {(int(t(355))+ys2.min())/S:.0f}..{(int(t(355))+ys2.max())/S:.0f}  target 584..712 / 374..475")

print("\n-- arrow + fraction --")
bbox(int(t(730)), int(t(410)), int(t(770)), int(t(440)), dk_notred, "arrow ink", (738, 422, 757, 431))
seg = a[int(t(395)):int(t(460)), int(t(768)):int(t(793))]
rm = red(seg)
ys2, xs2 = np.nonzero(rm)
if len(xs2):
    print(f"  fraction red(orig): x {(int(t(768))+xs2.min())/S:.0f}..{(int(t(768))+xs2.max())/S:.0f} y {(int(t(395))+ys2.min())/S:.0f}..{(int(t(395))+ys2.max())/S:.0f}  target 775..790 / 405..449")

print("\n-- output grid --")
sub = a[int(t(388)):int(t(465)), int(t(788)):int(t(880))]
colored = green(sub) | yellow(sub) | redf(sub) | cyan(sub)
ys2, xs2 = np.nonzero(colored)
print(f"  out grid bbox(orig): x {(int(t(788))+xs2.min())/S:.0f}..{(int(t(788))+xs2.max())/S:.0f} y {(int(t(388))+ys2.min())/S:.0f}..{(int(t(388))+ys2.max())/S:.0f}  target 796..871 / 396..453")

print("\n-- frame containment: ink outside content box (x 82..875, y 219..487)? --")
# expected outside-ink: L-frame lines + black bar only
sub = a[int(t(222)):int(t(483)), int(t(85)):int(t(872))]
mm = (sub.sum(axis=2) < 700)
ys2, xs2 = np.nonzero(mm)
print(f"  content ink bbox(orig): x {(int(t(85))+xs2.min())/S:.0f}..{(int(t(85))+xs2.max())/S:.0f} y {(int(t(222))+ys2.min())/S:.0f}..{(int(t(222))+ys2.max())/S:.0f}")
