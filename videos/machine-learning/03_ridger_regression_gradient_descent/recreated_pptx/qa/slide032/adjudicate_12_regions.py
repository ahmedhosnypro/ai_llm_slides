#!/usr/bin/env python3
"""Adjudicate slide 032 all five crop regions against BOTH images.

960x540 original (1px=1pt), 2001x1125 render (2.0833 render px per frame px).
Every claim is measured here before it is used to change a build.
"""
import numpy as np
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide032"
FRAME = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_032.jpg"
REND = Q + "/render_11.png"

S = 2001.0 / 960.0          # 2.08375 render px per frame px

o = np.array(Image.open(FRAME).convert("RGB")).astype(int)
r = np.array(Image.open(REND).convert("RGB")).astype(int)
H, W = o.shape[:2]
print(f"orig {W}x{H}  render {r.shape[1]}x{r.shape[0]}  scale={S:.6f}")

# trim the house chrome off both so chrome never registers as an ink column
CHROME = dict(panel_x=(112, 1882), panel_y=(94, 1118))

def lum(a):
    return (0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2])

LO = lum(o)
LR = lum(r)

def bbox_ink(a, lo, x0, y0, x1, y1, thr=248, min_ink=3):
    """Bounding box of ink px (lum<thr) inside a rect, rejecting
    rows/cols with fewer than min_ink px (phantom trap)."""
    sub = lo[int(y0):int(y1) + 1, int(x0):int(x1) + 1]
    m = sub < thr
    cols = m.sum(axis=0)
    rows = m.sum(axis=1)
    cols = np.nonzero(cols >= min_ink)[0]
    rows = np.nonzero(rows >= min_ink)[0]
    if not len(cols) or not len(rows):
        return None
    return (x0 + int(cols[0]), y0 + int(rows[0]),
            x0 + int(cols[-1]), y0 + int(rows[-1]))

def report(name, box_r):
    x0, y0, x1, y1 = box_r
    # render box is in render px -> frame px for the original
    fx0, fy0, fx1, fy1 = x0 / S, y0 / S, x1 / S, y1 / S
    print(f"\n=== {name}  render px [{x0},{y0}]-[{x1},{y1}] "
          f"= frame px [{fx0:.1f},{fy0:.1f}]-[{fx1:.1f},{fy1:.1f}] ===")
    bro = bbox_ink(o, LO, fx0 - 2, fy0 - 2, fx1 + 2, fy1 + 2)
    brr = bbox_ink(r, LR, x0, y0, x1, y1)
    if bro and brr:
        print(f"  ink bbox FRAME  x{bro[0]}..{bro[2]} y{bro[1]}..{bro[3]} "
              f"({bro[2]-bro[0]+1}x{bro[3]-bro[1]+1})")
        print(f"  ink bbox RENDER x{brr[0]}..{brr[2]} y{brr[1]}..{brr[3]} "
              f"({brr[2]-brr[0]+1}x{brr[3]-brr[1]+1})")
        rs = (brr[0] / S, brr[1] / S, brr[2] / S, brr[3] / S)
        print(f"  render bbox scaled to frame: x{rs[0]:.1f}..{rs[2]:.1f} "
              f"y{rs[1]:.1f}..{rs[3]:.1f}")
        dw = (rs[2] - rs[0]) - (bro[2] - bro[0])
        dh = (rs[3] - rs[1]) - (bro[3] - bro[1])
        dx0 = rs[0] - bro[0]
        dy0 = rs[1] - bro[1]
        print(f"  delta size  dw={dw:+.1f}pt dh={dh:+.1f}pt")
        print(f"  delta place dx={dx0:+.1f}pt dy={dy0:+.1f}pt")
    else:
        print("  ink bbox: ", bro, brr)
    return bro, brr


REGIONS = {
    # frame-space bboxes taken verbatim from the banked make_crops_10.py table
    "title":    (72, 58, 568, 98),
    "params":   (68, 170, 216, 259),
    "graph":    (565, 58, 818, 316),
    "callouts": (328, 176, 600, 362),
    "table":    (290, 322, 608, 535),
}

for n, b in REGIONS.items():
    x0, y0, x1, y1 = b
    report(n, (int(round(x0 * S)), int(round(y0 * S)),
               int(round(x1 * S)), int(round(y1 * S))))
