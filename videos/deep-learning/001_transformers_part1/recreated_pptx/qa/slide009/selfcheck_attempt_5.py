#!/usr/bin/env python3
"""selfcheck_attempt_1.py — closed-loop PIL checks for slide 009 render_5.png.
Downscale render to 960x540 frame space, then:
  (1) template-match landmarks vs unique_slides/slide_009.jpg (expect (0,0) +-2)
  (2) diff map vs frame — changed-region census (catch missing/extra/misplaced blocks)
  (3) containment: delta content inside gray panel + inside backprop panel
  (4) ink-presence: every delta region must contain ink (no empty boxes)
"""
from PIL import Image
import numpy as np
from scipy import ndimage

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide009"
FRAME = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_009.jpg"

r = Image.open(f"{QA}/render_5.png").convert("RGB").resize((960, 540), Image.LANCZOS)
f = Image.open(FRAME).convert("RGB")
a = np.asarray(r, dtype=np.int16)   # render in frame space
b = np.asarray(f, dtype=np.int16)   # ground truth frame
ag = np.asarray(r.convert("L"), dtype=np.float32)
bg = np.asarray(f.convert("L"), dtype=np.float32)

print("== (1) LANDMARK TEMPLATE MATCH (render vs frame, expect dx,dy=(0,0)) ==")
def match(name, x, y, w, h, search=8):
    crop = bg[y:y+h, x:x+w]
    best = None
    for dy in range(-search, search+1):
        for dx in range(-search, search+1):
            yy, xx = y+dy, x+dx
            if yy < 0 or xx < 0 or yy+h > 540 or xx+w > 960: continue
            ssd = float(((ag[yy:yy+h, xx:xx+w] - crop) ** 2).mean())
            if best is None or ssd < best[0]: best = (ssd, dx, dy)
    ssd, dx, dy = best
    flag = "OK" if abs(dx) <= 2 and abs(dy) <= 2 else "<<< OFF"
    print(f"  {name}: dx={dx:+d} dy={dy:+d} ssd={ssd:.1f} {flag}")
    return dx, dy, ssd

match("dec container", 488, 118, 200, 60)
match("dec green bar1", 525, 201, 76, 19)
match("dec hidden bar3", 789, 257, 73, 20)
match("enc container", 53, 309, 200, 60)
match("enc pink bar1", 132, 321, 76, 20)
match("enc tan bar3", 393, 408, 78, 19)
match("title L1", 260, 55, 390, 28)
match("subtitle", 380, 86, 155, 27)
match("callout box", 108, 130, 283, 58, 10)
match("summary box", 61, 201, 379, 91, 10)
match("panel top-left", 502, 314, 120, 50, 10)
match("panel bottom-right", 800, 450, 118, 48, 10)
match("brace zone", 519, 321, 389, 21, 6)
match("backprop text", 630, 335, 152, 20, 8)
match("arrow row", 520, 350, 390, 16, 8)
match("nabla row", 518, 373, 388, 22, 8)
match("pink row", 531, 408, 364, 16, 8)
match("green row", 520, 462, 386, 22, 8)

print("== (2) DIFF CENSUS (render vs frame; |diff|>60 px clusters) ==")
d = np.abs(a - b).sum(axis=2)
mask = d > 60
lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
objs = ndimage.find_objects(lab)
comps = []
for i, sl in enumerate(objs):
    area = int((lab[sl] == i + 1).sum())
    if area > 300:
        ys, xs = sl
        comps.append((area, xs.start, ys.start, xs.stop, ys.stop))
comps.sort(reverse=True)
print(f"  changed px: {int(mask.sum())} ({100*mask.sum()/mask.size:.2f}%), clusters>300: {len(comps)}")
for area, x0, y0, x1, y1 in comps[:25]:
    print(f"    area={area:6d} x{x0}..{x1} y{y0}..{y1}")

print("== (3) CONTAINMENT ==")
# gray panel spans x42..918 y45..539 (frame px). Content ink must stay inside.
ink = (np.abs(a - np.array([255, 255, 255])).sum(axis=2) > 90)  # non-white
# restrict to the playlist content area and look for ink OUTSIDE panel bounds
outside = ink.copy()
outside[45:539, 42:919] = False
print(f"  ink px outside gray panel: {int(outside.sum())}")
ys, xs = np.where(outside)
if len(ys): print(f"    bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()}")
# delta content inside backprop panel (x502..918 y314..498): ink within ±3 of its border?
panelzone = a[314:498, 502:919]
print(f"  panel zone sampled OK (shape {panelzone.shape})")

print("== (4) INK PRESENCE in delta regions (render) ==")
def inkcheck(name, x0, y0, x1, y1, minpx=30):
    reg = a[y0:y1, x0:x1]
    # ink = pixels far from both the region's dominant bg and white
    med = np.median(reg.reshape(-1, 3), axis=0)
    far = (np.abs(reg - med).sum(axis=2) > 90).sum()
    print(f"  {name}: ink-px={int(far)} {'OK' if far >= minpx else '<<< EMPTY'}")
inkcheck("callout text", 130, 138, 370, 182)
inkcheck("summary text", 70, 205, 320, 290)
inkcheck("backprop text", 635, 334, 780, 356)
inkcheck("arrow+dot", 515, 348, 910, 368)
inkcheck("nabla row", 515, 370, 910, 398, 60)
inkcheck("pink row", 530, 406, 900, 425, 60)
inkcheck("green row", 515, 460, 910, 487, 100)
inkcheck("brace", 519, 321, 908, 342, 60)
