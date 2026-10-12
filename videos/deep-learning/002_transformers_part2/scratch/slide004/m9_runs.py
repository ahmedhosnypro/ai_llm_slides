#!/usr/bin/env python3
# m9_runs.py — exact vertical color runs down the encoder/decoder column centers in
# the render (certified composition) and the frame (ground truth), plus direct RGB
# probes of the render's encoder-MHA region.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")

def runs(a, x, y0, y1, tol=26):
    out = []
    cur = None; start = y0
    for y in range(y0, y1):
        c = a[y, x]
        if cur is None:
            cur = c; start = y; continue
        if np.abs(c - cur).sum() > tol * 3:
            out.append((start, y - 1, cur.copy()))
            cur = c; start = y
        else:
            cur = 0.7 * cur + 0.3 * c
    out.append((start, y1 - 1, cur.copy()))
    return [(a_, b_, "%02X%02X%02X" % tuple(int(round(q)) for q in c)) for a_, b_, c in out if b_ - a_ >= 2]

def hx(c):
    return "%02X%02X%02X" % tuple(int(round(q)) for q in c)

print("== RENDER encoder column center x=1430 (pt 686.4), y 560..1060 ==")
for a, b, c in runs(render, 1430, 560, 1060):
    print(f"  y {a}..{b} ({a*0.48:.1f}..{b*0.48:.1f} pt) {c}")
print("== RENDER decoder column center x=1662 (pt 785.3), y 240..1060 ==")
for a, b, c in runs(render, 1662, 240, 1060):
    print(f"  y {a}..{b} ({a*0.48:.1f}..{b*0.48:.1f} pt) {c}")

print("\n== FRAME encoder column x=660 (maps to render 1391), y 255..470 ==")
for a, b, c in runs(frame, 660, 255, 470):
    fx0, fy0 = a, b
    rx = ax + sx * 660; ry0 = ay + sy * a; ry1 = ay + sy * b
    print(f"  y {a}..{b} -> render y {ry0:.0f}..{ry1:.0f} (pt {ry0*0.48:.1f}..{ry1*0.48:.1f}) {c}")
print("== FRAME decoder column x=790 (maps to render 1673), y 120..330 ==")
for a, b, c in runs(frame, 790, 120, 330):
    ry0 = ay + sy * a; ry1 = ay + sy * b
    print(f"  y {a}..{b} -> render y {ry0:.0f}..{ry1:.0f} (pt {ry0*0.48:.1f}..{ry1*0.48:.1f}) {c}")

print("\n== direct RGB probes ==")
probes = [
    ("render enc-MHA box center (1430,772)", render, 1430, 772),
    ("render enc-MHA box upper (1430,755)", render, 1430, 755),
    ("render enc-MHA box lower (1430,790)", render, 1430, 790),
    ("render left of box (1250,772)", render, 1250, 772),
    ("render below box (1430,815)", render, 1430, 815),
    ("frame at enc-MHA (660,365)", frame, 660, 365),
    ("frame left of box (600,365)", frame, 600, 365),
    ("frame below box (660,380)", frame, 660, 380),
    ("render dec zone right (1750,600)", render, 1750, 600),
    ("frame dec zone right (815,285)", frame, 815, 285),
]
for name, a, x, y in probes:
    print(f"  {name}: {hx(a[y, x])} {tuple(int(q) for q in a[y, x])}")

# where exactly is orange in the RENDER? connected components on render itself
from scipy import ndimage
r, g, b = render[..., 0], render[..., 1], render[..., 2]
om = (r > 195) & (b < 190) & (g > 120) & (g < 235) & ((r - b) > 45) & ((g - b) > 18)
om[:230, :] = False; om[1060:, :] = False
lab, n = ndimage.label(om)
sizes = ndimage.sum(om, lab, range(1, n + 1))
print("\n== orange components IN THE CERTIFIED RENDER ==")
for k in np.argsort(sizes)[::-1][:10]:
    if sizes[k] < 120: break
    ys, xs = np.where(lab == k + 1)
    print(f"  n={int(sizes[k])} x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} (pt x {xs.min()*0.48:.1f}..{xs.max()*0.48:.1f} y {ys.min()*0.48:.1f}..{ys.max()*0.48:.1f}) core {hx(render[ys[len(ys)//2], xs[len(xs)//2]])}")
