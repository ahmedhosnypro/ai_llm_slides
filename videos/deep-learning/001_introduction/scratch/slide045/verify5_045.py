#!/usr/bin/env python3
"""verify5_045.py — closed-loop verification of attempt-5 fixes vs the original frame.
Checks every corrected token's ink bbox (org vs render_5, tol ~4pt) + the arrow's red
components. Banked as verify5_out.txt in qa/slide045/."""
import numpy as np
from PIL import Image
from collections import deque

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide045"
ORG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg"
ren = np.asarray(Image.open(f"{QA}/render_5.png").convert("RGB")).astype(int)
org = np.asarray(Image.open(ORG).convert("RGB")).astype(int)
s = ren.shape[0] / 540.0

def ink(im, k=1):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    lum = (r + g + b) / 3
    return (lum < 205) & ~((r - g > 30) & (r - b > 20))

def red(im, k=1):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return (r - g > 25) & (r - b > 15) & (r > 90)

mo, mr = ink(org), ink(ren, s)
ro, rr = red(org), red(ren, s)

def bbox(mask, x0, x1, y0, y1, is_r=False):
    k = s if is_r else 1
    win = mask[int(y0*k):int(y1*k)+1, int(x0*k):int(x1*k)+1]
    ys, xs = np.where(win)
    if len(ys) == 0:
        return None
    return (x0 + xs.min()/k, x0 + xs.max()/k, y0 + ys.min()/k, y0 + ys.max()/k)

CHECKS = [
    # name, window (x0,x1,y0,y1), expected ORG bbox is measured live; we print both
    ("sub_a",   (604, 656, 334, 356)),
    ("dot_a",   (654, 666, 333, 346)),
    ("theta_a", (663, 677, 328, 349)),
    ("ij_a",    (676, 692, 334, 354)),
    ("a_b",     (518, 547, 394, 414)),
    ("sim_b",   (545, 562, 397, 408)),
    ("x_b",     (556, 571, 393, 410)),
    ("T_b",     (568, 582, 390, 406)),
    ("region_b", (556, 618, 402, 416)),
    ("dot_b",   (615, 627, 397, 408)),
    ("theta_b", (625, 641, 392, 411)),
]
print("== TOKEN INK BBOXES (org vs render_5, frame pt, tol 4) ==")
for name, (x0, x1, y0, y1) in CHECKS:
    o = bbox(mo, x0, x1, y0, y1)
    r5 = bbox(mr, x0, x1, y0, y1, True)
    if o is None or r5 is None:
        print(f" {name:9s} org={o} ren={r5}  <-- MISSING")
        continue
    d = [r5[i] - o[i] for i in range(4)]
    bad = any(abs(v) > 4 for v in d)
    print(f" {name:9s} org=({o[0]:6.1f},{o[1]:6.1f},{o[2]:6.1f},{o[3]:6.1f}) "
          f"ren=({r5[0]:6.1f},{r5[1]:6.1f},{r5[2]:6.1f},{r5[3]:6.1f}) "
          f"d=({d[0]:+5.1f},{d[1]:+5.1f},{d[2]:+5.1f},{d[3]:+5.1f}){'  <-- CHECK' if bad else ''}")

print("== ARROW red components (region x560..745 y300..375) ==")
def comps(mask, k, X0, X1, Y0, Y1):
    win = mask[int(Y0*k):int(Y1*k)+1, int(X0*k):int(X1*k)+1]
    lab = np.zeros(win.shape, dtype=bool)
    out = []
    for y in range(win.shape[0]):
        for x in range(win.shape[1]):
            if win[y, x] and not lab[y, x]:
                q = deque([(y, x)]); lab[y, x] = True; pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy+dy, cx+dx
                            if 0 <= ny < win.shape[0] and 0 <= nx < win.shape[1] and win[ny, nx] and not lab[ny, nx]:
                                lab[ny, nx] = True; q.append((ny, nx))
                if len(pts) >= 12:
                    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                    out.append((X0 + min(xs)/k, X0 + max(xs)/k, Y0 + min(ys)/k, Y0 + max(ys)/k, len(pts)))
    return sorted(out, key=lambda t: -t[4])

for nm, m, k in (("org", ro, 1), ("ren", rr, s)):
    cs = comps(m, k, 560, 745, 300, 375)
    print(f" {nm}: " + "; ".join(f"x{a:.0f}..{b:.0f} y{c:.0f}..{d:.0f} (n={n})" for a, b, c, d, n in cs[:4]))

print("== SHAFT-BAND red cols (y346..356 x624..700; org=8 baseline) ==")
for nm, m, k in (("org", ro, 1), ("ren", rr, s)):
    band = m[int(346*k):int(356*k)+1, int(624*k):int(700*k)+1]
    print(f" {nm}: red cols = {int((band.sum(axis=0) > 0).sum())}")
