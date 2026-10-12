#!/usr/bin/env python3
"""Slide 030 self-check attempt 8 (closed loop, ~4px @150dpi tolerance).
Window artifacts accounted: segments whose expected bbox adjoins a neighbor's ink
within the search pad are checked on their uncontaminated edges only (noted).
Descender tails (p/g/quotes) and the Remember underline extend below the baseline:
expected bottoms include them."""
import json
import numpy as np
from PIL import Image

rend = np.asarray(Image.open("videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide030/render_3.png").convert("RGB")).astype(int)
RH, RW, _ = rend.shape
EQ = json.load(open("videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/eq_030_manifest.json"))

SX = 2.08333 / 0.96123
SY = 2.08333 / 0.95556
X = lambda fx: (fx - 17.63) * SX
Y = lambda fy: fy * SY
lum = rend.mean(axis=2)
ink = lum < 150
fails = 0
notes = []

def check(name, ex_l, ex_t, ex_r, ex_b, tol=4.0, pad=6, edges="ltrb"):
    l, t = max(int(ex_l - pad), 0), max(int(ex_t - pad), 0)
    r, b = min(int(ex_r + pad), RW - 1), min(int(ex_b + pad), RH - 1)
    sub = ink[t:b, l:r]
    xs = np.where(sub.sum(axis=0) > 0)[0]
    ys = np.where(sub.sum(axis=1) > 0)[0]
    if len(xs) == 0:
        print(f"FAIL {name}: NO INK in window ({l},{t})-({r},{b})")
        return False
    worst, worst_e, det = 0.0, "", {}
    if "l" in edges:
        d = xs.min() + l - ex_l; det["dL"] = d
    if "t" in edges:
        d = ys.min() + t - ex_t; det["dT"] = d
    if "r" in edges:
        d = xs.max() + l - ex_r; det["dR"] = d
    if "b" in edges:
        d = ys.max() + t - ex_b; det["dB"] = d
    for k, v in det.items():
        if abs(v) > abs(worst):
            worst, worst_e = abs(v), k
    flag = "ok  " if worst <= tol else "FAIL"
    ds = " ".join(f"{k}={v:+.1f}" for k, v in det.items())
    print(f"{flag} {name:10s} {ds} (worst {worst:.1f} on {worst_e})")
    return worst <= tol

print("== EQUATION SEGMENTS ==")
for name, e in EQ.items():
    if name in ("brace", "m_minus", "d2_s8"):   # m_minus/d2_s8 drawn as rects; PNGs unplaced
        continue
    l = X(e["ink_left_frame"])
    if e.get("anchor") == "inktop":
        t = Y(e["ink_top_frame"]); h = e["h_px"] / 4.0
        ok = check(name, l + 2, t + 2, l + e["w_px"] / 4.0 - 2, t + h - 2)
    else:
        base = Y(e["baseline_frame"]); h = e["h_px"] / 4.0
        it = base - e["baseline_frac"] * h + 2
        ib = base + (1 - e["baseline_frac"]) * h - 2
        ir = l + e["w_px"] / 4.0 - 2
        # *a prefixes have the bracket/neighbor at left; *b cells have the prefix tail at left
        edges = "ltrb"
        if name.endswith("a") and name.startswith(("vb2", "m_l")):
            edges = "tb"     # left = bracket stroke, right = adjoining *b cell
        if name.endswith("b") and name.startswith(("vb2", "m_l")) or name in ("d1_s2", "d2_s2"):
            edges = "trb"    # left edge adjoins the prefix segment (gap <= 1 frame px)
        if name in ("d1_s1", "d2_s1"):
            edges = "ltb"    # right edge adjoins the *b highlight
        pd = 3 if edges != "ltrb" else 6
        ok = check(name, l + 2, it, ir, ib, tol=4.0, pad=pd, edges=edges)
    if not ok:
        fails += 1

print("== BRACE ==")
e = EQ["brace"]
l, t = X(e["ink_left_frame"]), Y(e["ink_top_frame"])
if not check("brace", l + 2, t + 2, l + e["w_px"] / 4.0 - 2, t + e["h_px"] / 4.0 - 2, tol=5.0):
    fails += 1

print("== TEXT ELEMENTS (expected bottoms include descenders/underline) ==")
texts = [
    ("label1", 102, 88.4, 210, 100.5, "ltrb", 4.0),
    ("label2", 104, 182.4, 228, 194.5, "ltrb", 4.0),
    ("rememhdr", 512, 112, 588, 120.0, "ltr", 3.0),   # window ends above the underline row     # bottom = underline overlap; underline checked separately
    ("caption1", 98, 444.2, 222, 455.5, "ltrb", 4.0),
    ("caption2", 490, 453.2, 595, 464.5, "ltrb", 4.0),
    ("independ", 230, 481, 483, 496.5, "ltr", 3.0),   # pad 3 keeps the y498 box border out of the window     # window excludes box bottom border y498; p-descender clipped
    ("noteL1", 634, 360.2, 838, 376.5, "ltrb", 5.0),    # 'p' descender
    ("noteL2", 633, 391.8, 856, 404.5, "ltrb", 5.0),    # no descenders in string
    ("noteL3", 633, 411.5, 831, 427.5, "ltrb", 5.0),    # 'g' + quotes
    ("noteL4", 633, 436.5, 821, 451.5, "ltrb", 5.0),
]
for name, il, it_, ir, ib, ed, tol in texts:
    pp = 3 if name in ("rememhdr", "independ") else 6
    if not check(name, X(il), Y(it_), X(ir), Y(ib), tol=tol, pad=pp, edges=ed):
        fails += 1
print("underline:", end=" ")
if not check("underline", X(512), Y(123), X(589), Y(124.5), tol=4.0, pad=3):  # text bottoms overlap window (documented)
    fails += 1

print("== MINUS RECTS ==")
if not check("minusL2", X(508), Y(302.5), X(511), Y(304.5), tol=3.0):
    fails += 1
if not check("minusM", X(288), Y(410.5), X(291), Y(412.5), tol=3.0):
    fails += 1

print("== BRACKETS (stem ink present at measured columns) ==")
for label, fx, y0, y1 in [("v1L", 242.5, 60, 136), ("v2L", 243.5, 154, 228),
                          ("mxL", 279.5, 354, 430), ("rvL", 484.5, 354, 430),
                          ("lvL", 120.5, 355, 429)]:
    col = int(X(fx))
    c = int(ink[int(Y(y0)):int(Y(y1)), col - 2:col + 3].sum())
    ok = c > 40
    print("ok  " if ok else "FAIL", f"{label}: stem ink px={c}")
    if not ok:
        fails += 1

print("== FRAME CONTAINMENT ==")
xs = np.where(ink.sum(axis=0) > 0)[0]
ok = xs.min() >= 86 and xs.max() <= 1916
print("ok  " if ok else "FAIL", f"render ink x {xs.min()}..{xs.max()} within house frame")
if not ok:
    fails += 1

print("== FILLS / COLORS ==")
def sample(fx, fy, label, expect):
    global fails
    px = rend[int(Y(fy)), int(X(fx))]
    ok = all(abs(int(px[i]) - expect[i]) <= 26 for i in range(3))
    print("ok  " if ok else "FAIL", f"{label}: ({px[0]},{px[1]},{px[2]}) expect ~{expect}")
    if not ok:
        fails += 1
sample(600, 140, "remember fill", (249, 252, 207))
sample(750, 430, "note fill", (240, 252, 228))
sample(200, 170, "vecbox fill", (255, 255, 255))
sample(310, 173.5, "hl yellow", (248, 254, 122))
sample(372.5, 373.5, "hl green", (141, 206, 155))
sample(500, 60, "panel gray", (233, 233, 231))

print(f"\nTOTAL FAILS: {fails}")
