#!/usr/bin/env python3
"""selfcheck_attempt_2.py — closed-loop PIL ink check, render_1 vs original frame targets.
Render: 150dpi PNG of the 13.333x7.5in slide (2000x1125 expected).
Expected render bbox for a frame-px box (fx0,fy0,fx1,fy1):
  rx = ((fx - 18.128)/0.961235) * 2000/960 ;  ry = ((fy + 0.045)/0.956566) * 1125/540
Actual ink bbox measured in a +-10px window around the expectation for the fill color;
PASS if all four edge deltas <= 4 px.
"""
import numpy as np
from PIL import Image
import sys

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide051/render_1.png"
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W, _ = im.shape
print("render size", W, H)

KX = 2000 / 960.0
KY = 1125 / 540.0

def exp_box(fx0, fy0, fx1, fy1):
    x0 = ((fx0 - 18.128) / 0.961235) * KX
    x1 = ((fx1 - 18.128) / 0.961235) * KX
    y0 = ((fy0 + 0.045) / 0.956566) * KY
    y1 = ((fy1 + 0.045) / 0.956566) * KY
    return x0, y0, x1, y1

def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def measure(target, name, tol=4):
    fx0, fy0, fx1, fy1, hexcol, tolc = target
    ex0, ey0, ex1, ey1 = exp_box(fx0, fy0, fx1, fy1)
    c = np.array(hexrgb(hexcol))
    wx0, wy0 = int(ex0) - 12, int(ey0) - 12
    wx1, wy1 = int(ex1) + 12, int(ey1) + 12
    wx0 = max(wx0, 0); wy0 = max(wy0, 0); wx1 = min(wx1, W); wy1 = min(wy1, H)
    win = im[wy0:wy1, wx0:wx1]
    m = np.abs(win - c).max(axis=2) <= tolc
    ys, xs = np.where(m)
    if len(xs) < 8:
        print(f"FAIL {name:24s} NO INK for #{hexcol} in window ({len(xs)} px)")
        return False
    ax0, ax1 = wx0 + xs.min(), wx0 + xs.max()
    ay0, ay1 = wy0 + ys.min(), wy0 + ys.max()
    d = (ax0 - ex0, ay0 - ey0, ax1 - ex1, ay1 - ey1)
    ok = all(abs(v) <= tol for v in d)
    print(f"{'PASS' if ok else 'FAIL'} {name:24s} edges dL={d[0]:+5.1f} dT={d[1]:+5.1f} dR={d[2]:+5.1f} dB={d[3]:+5.1f}")
    return ok

# targets: (fx0, fy0, fx1, fy1, hex, tol)  [frame px, fill hex to find in render]
T = [
    (136, 102, 444, 503, "FBECDB", 12, "enc panel fill"),
    (292, 104, 443, 502, "11FF74", 25, "enc green overlay"),
    (571, 103, 724, 501, "F2A557", 14, "dec orange zone"),
    (727, 103, 875, 501, "C8F8E0", 14, "dec mint zone"),
    (724, 104, 726, 500, "EADFB8", 20, "seam"),
    (224, 58, 737, 81, "C00000", 60, "title ink"),
    (213, 266, 275, 275, "6D99B4", 20, "enc Add&Norm top"),
    (215, 281, 274, 303, "807560", 22, "enc Feed Forward"),
    (214, 330, 275, 339, "6D99B4", 20, "enc Add&Norm bot"),
    (215, 345, 275, 368, "C87E57", 22, "enc MHA"),
    (237, 243, 289, 310, "FFFF00", 25, "enc yellow L"),
    (161, 320, 181, 340, "C8A888", 18, "Nx circle"),
    (215, 428, 281, 462, "B08058", 22, "enc Output Embedding"),
    (214, 469, 224, 492, "C00000", 60, "enc Inputs arrow"),
    (752, 110, 795, 122, "FFFF00", 25, "dec Output box"),
    (738, 143, 799, 154, "A8ECBC", 16, "dec Softmax"),
    (742, 166, 807, 178, "B0E4CE", 16, "dec Linear"),
    (741, 201, 801, 210, "5C9CB7", 20, "dec Add&Norm top"),
    (742, 213, 801, 239, "6E7E62", 22, "dec Feed Forward"),
    (741, 255, 801, 264, "5C9CB7", 20, "dec Add&Norm mid"),
    (742, 271, 801, 293, "B28659", 22, "dec MHA"),
    (742, 318, 799, 328, "6E87E0", 22, "dec Add&Norm low"),
    (737, 331, 813, 390, "CE8ADC", 24, "dec Masked MHA"),
    (575, 145, 655, 161, "FFFFFF", 8, "callout 1"),
    (575, 169, 655, 184, "FFFFFF", 8, "callout 2"),
    (575, 286, 655, 327, "FFFFFF", 8, "callout 3"),
    (575, 343, 655, 358, "FFFFFF", 8, "callout 4"),
    (737, 400, 806, 462, "B8706C", 22, "dec Output Embedding"),
    (751, 474, 795, 488, "FFFF00", 25, "dec yellow bottom"),
    (566, 101, 880, 102, "00A000", 60, "dec panel top border"),
]

targets = [(t[0], t[1], t[2], t[3], t[4], t[5]) for t in T]
names = [t[6] for t in T]
ok = 0
for t, n in zip(targets, names):
    ok += measure(t, n)
print(f"\n== {ok}/{len(targets)} targets within 4px ==")
sys.exit(0 if ok == len(targets) else 1)
