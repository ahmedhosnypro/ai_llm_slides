#!/usr/bin/env python3
"""Slide 030 self-check attempt 1: closed-loop PIL verification of the 150dpi render
vs the original frame's measured regions (tolerance ~4px @150dpi per the alignment law).
Render 2001x1125 @150dpi; render_px = slide_pt * 150/72.
  X_r = (fx - 17.63)/0.96123 * 2.08333 ;  Y_r = fy/0.95556 * 2.08333
"""
import json
import numpy as np
from PIL import Image

rend = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide030/render_1.png").convert("RGB")).astype(int)
RH, RW, _ = rend.shape
print(f"render {RW}x{RH}")
EQ = json.load(open("videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_030_manifest.json"))

SX = 2.08333 / 0.96123   # frame dx -> render px
SY = 2.08333 / 0.95556
X = lambda fx: (fx - 17.63) * SX
Y = lambda fy: fy * SY

lum = rend.mean(axis=2)
ink = lum < 150

def edges(x0, y0, x1, y1):
    xs = np.where(ink[y0:y1, x0:x1].sum(axis=0) > 0)[0]
    ys = np.where(ink[y0:y1, x0:x1].sum(axis=1) > 0)[0]
    if len(xs) == 0:
        return None
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)

def check(name, ex_l, ex_t, ex_r, ex_b, tol=4.0, pad=6):
    l, t, r, b = int(ex_l - pad), int(ex_t - pad), int(ex_r + pad), int(ex_b + pad)
    l, t = max(l, 0), max(t, 0)
    r, b = min(r, RW - 1), min(b, RH - 1)
    m = edges(l, t, r, b)
    if m is None:
        print(f"FAIL {name}: NO INK in window ({l},{t})-({r},{b})")
        return False
    dl, dt, dr, db = m[0] - ex_l, m[1] - ex_t, m[2] - ex_r, m[3] - ex_b
    worst = max(abs(dl), abs(dt), abs(dr), abs(db))
    flag = "ok  " if worst <= tol else "FAIL"
    print(f"{flag} {name:10s} edges dL={dl:+.1f} dT={dt:+.1f} dR={dr:+.1f} dB={db:+.1f} (worst {worst:.1f})")
    return worst <= tol

fails = 0
print("== EQUATION SEGMENTS (baseline/inktop anchored) ==")
for name, e in EQ.items():
    if name == "brace":
        continue
    l = X(e["ink_left_frame"])
    if e.get("anchor") == "inktop":
        t = Y(e["ink_top_frame"])
        h = e["h_px"] / 4.0
        b_, t_ = t + h - 2, t + 2  # ink approx (pad 8@600 = 2px@150)
        r_ = l + e["w_px"] / 4.0 - 2
        if not check(name, l + 2, t_, r_, b_):
            fails += 1
        continue
    base = Y(e["baseline_frame"])
    h = e["h_px"] / 4.0
    it = base - e["baseline_frac"] * h + 2
    ib = base + (1 - e["baseline_frac"]) * h - 2
    ir = l + e["w_px"] / 4.0 - 2
    if not check(name, l + 2, it, ir, ib):
        fails += 1

print("== BRACE ==")
e = EQ["brace"]
l, t = X(e["ink_left_frame"]), Y(e["ink_top_frame"])
if not check("brace", l + 2, t + 2, l + e["w_px"] / 4.0 - 2, t + e["h_px"] / 4.0 - 2):
    fails += 1

print("== TEXT ELEMENTS (ink-left + cap-top) ==")
# (label, ink_left_f, cap_top_f, ink_right_f, baseline_f)
texts = [
    ("label1", 102, 88.4, 210, 100),
    ("label2", 104, 182.4, 228, 194),
    ("rememhdr", 512, 112, 588, 122),
    ("caption1", 98, 444.2, 222, 455),
    ("caption2", 490, 453.2, 595, 464),
    ("independ", 230, 481, 479, 495),
    ("noteL1", 634, 360.2, 838, 372),
    ("noteL2", 633, 391.8, 854, 404),
    ("noteL3", 633, 411.5, 828, 423),
    ("noteL4", 633, 437.5, 821, 447),
]
for name, il, it_, ir, ib in texts:
    if not check(name, X(il), Y(it_), X(ir), Y(ib)):
        fails += 1

print("== MINUS RECTS ==")
if not check("minusL2", X(508), Y(302.5), X(511), Y(304.5)):
    fails += 1
if not check("minusM", X(288), Y(410.5), X(291), Y(412.5)):
    fails += 1

print("== FRAME CONTAINMENT (content inside boxes / house frame) ==")
# house frame inner area in render px: chrome panel x 89..1913 (checker), y 95..
xs = np.where(ink[:, :].sum(axis=0) > 0)[0]
print(f"render ink x extent: {xs.min()}..{xs.max()} (house inner ~89..1913)")
ok = xs.min() >= 86 and xs.max() <= 1916
print("ok  " if ok else "FAIL", "content within house frame")
if not ok:
    fails += 1

print("== FILLS / COLOR SAMPLES ==")
def sample(x, y, label):
    px = rend[y, x]
    print(f"{label}: ({px[0]},{px[1]},{px[2]})")
sample(X(600), Y(140), "remember fill (expect ~F9FCCF)")
sample(X(750), Y(430), "note fill (expect ~F0FCE4)")
sample(X(200), Y(170), "vecbox fill (expect white)")
sample(X(300), Y(256), "deriv L1 (t+delta) highlight (expect ~F8FE7A)")
sample(X(460), Y(258), "deriv L1 cos(wd) highlight (expect ~8DCE9B)")
sample(X(500), Y(60), "panel gray (expect ~E9E9E7)")

print(f"\nTOTAL FAILS: {fails}")
