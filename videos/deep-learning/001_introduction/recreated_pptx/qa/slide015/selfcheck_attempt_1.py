#!/usr/bin/env python3
"""Closed-loop self-check attempt 1 for slide_015: compare the 150dpi render against
the PIL-measured ground-truth bands of the original frame (2001x1125 render; scale
S = 2001/960 render px per frame px; tolerance ~4 render px ~ 1.9 frame px)."""
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide015/render_1.png"
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = W / 960.0
print(f"render {W}x{H}, scale {S:.4f} render-px per frame-px; tol ~4 render px")
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
red = (r > 120) & (g < 110) & (b < 110)
fails = []

def band(y0, y1, x0, x1):
    m = red[y0:y1+1, x0:x1+1]
    ys, xs = np.where(m)
    return (ys.min()+y0, ys.max()+y0, xs.min()+x0, xs.max()+x0, int(m.sum()))

EXPECT = [
    ("L1 '[2] Machine Learning'", 189, 242, 219, 761),
    ("L2 'vs'", 270, 289, 471, 507),
    ("L3 'Deep Learning'", 320, 372, 304, 674),
]
for name, e0, e1, e2, e3 in EXPECT:
    # search window around expected band (in render px)
    wy0, wy1 = int((e0-15)*S), int((e1+15)*S)
    wx0, wx1 = int((e2-40)*S), int((e3+40)*S)
    ry0, ry1, rx0, rx1, n = band(wy0, wy1, wx0, wx1)
    f0, f1, f2, f3 = ry0/S, ry1/S, rx0/S, rx1/S
    d = (abs(f0-e0), abs(f1-e1), abs(f2-e2), abs(f3-e3))
    cx = (f2+f3)/2; ecx = (e2+e3)/2
    ok = max(d) <= 4.0 and abs(cx-ecx) <= 4.0
    print(f"{name}: frame rows {f0:.1f}..{f1:.1f} (exp {e0}..{e1}, d {d[0]:.1f}/{d[1]:.1f}), "
          f"cols {f2:.1f}..{f3:.1f} (exp {e2}..{e3}, d {d[2]:.1f}/{d[3]:.1f}), "
          f"w {f3-f2:.1f} (exp {e3-e2}), cx {cx:.1f} (exp {ecx:.1f}, d {abs(cx-ecx):.1f}) "
          f"ink={n} -> {'OK' if ok else 'FAIL'}")
    if not ok: fails.append(name)

# text core color in render (5x5 all-red) within L1 band area
core_red = red.copy()
core_red[:int(180*S), :] = False; core_red[int(380*S):, :] = False
core_red[:, :int(100*S)] = False; core_red[:, int(880*S):] = False
core = np.zeros_like(core_red)
rr, cc = np.where(core_red)
for y, x in zip(rr, cc):
    if core_red[y-2:y+3, x-2:x+3].all(): core[y, x] = True
ys, xs = np.where(core)
if len(ys):
    ink = im[ys, xs]
    print(f"render text core mean: #{int(ink[:,0].mean()):02X}{int(ink[:,1].mean()):02X}{int(ink[:,2].mean()):02X} n={len(ys)} (target B3000C)")
else:
    print("render text core: NO CORE PIXELS"); fails.append("core color")

# containment: title ink well inside panel (x 89..1913 render)
trows = np.where(red[int(80*S):int(510*S)].sum(axis=1) > 3)[0]
allx = np.where(red[int(80*S):int(510*S)].sum(axis=0) > 0)[0]
print(f"title ink cols {allx.min()}..{allx.max()} render (panel 89..1913): inside = {allx.min()>95 and allx.max()<1907}")

print("RESULT:", "PASS" if not fails else f"FAIL {fails}")
