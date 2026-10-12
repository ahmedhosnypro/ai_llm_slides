#!/usr/bin/env python3
"""selfcheck_attempt_3.py — closed-loop PIL ink check v3 (exact-hex tolerances).
Render colors are EXACT pptxgenjs hex (LO, no JPEG) -> tol 10 for solid fills,
40 for red strokes with anti-aliasing. Windows exclude known adjacent fringes.
"""
import numpy as np
from PIL import Image
import sys

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide051/render_3.png"
im = np.asarray(Image.open(REN).convert("RGB")).astype(int)
H, W, _ = im.shape
KX, KY = 2000 / 960.0, 1125 / 540.0

def exp_box(fx0, fy0, fx1, fy1):
    return (((fx0 - 18.128) / 0.961235) * KX, ((fy0 + 0.045) / 0.956566) * KY,
            ((fx1 - 18.128) / 0.961235) * KX, ((fy1 + 0.045) / 0.956566) * KY)

def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def measure(t):
    fx0, fy0, fx1, fy1, hexcol, tolc, name, pad = t
    ex0, ey0, ex1, ey1 = exp_box(fx0, fy0, fx1, fy1)
    c = np.array(hexrgb(hexcol))
    wx0, wy0 = int(ex0) - pad, int(ey0) - pad
    wx1, wy1 = int(ex1) + pad, int(ey1) + pad
    wx0 = max(wx0, 0); wy0 = max(wy0, 0); wx1 = min(wx1, W); wy1 = min(wy1, H)
    m = np.abs(im[wy0:wy1, wx0:wx1] - c).max(axis=2) <= tolc
    ys, xs = np.where(m)
    if len(xs) < 8:
        print(f"FAIL {name:24s} NO INK for #{hexcol} ({len(xs)} px)")
        return False
    ax0, ax1 = wx0 + xs.min(), wx0 + xs.max()
    ay0, ay1 = wy0 + ys.min(), wy0 + ys.max()
    d = (ax0 - ex0, ay0 - ey0, ax1 - ex1, ay1 - ey1)
    ok = all(abs(v) <= 4 for v in d)
    print(f"{'PASS' if ok else 'FAIL'} {name:24s} dL={d[0]:+5.1f} dT={d[1]:+5.1f} dR={d[2]:+5.1f} dB={d[3]:+5.1f}")
    return ok

T = [
    (136, 102, 444, 503, "FBECDB", 10, "enc panel fill", 6),
    (292, 104, 443, 502, "11FF74", 10, "enc green overlay", 6),
    (571, 103, 724, 501, "F2A557", 10, "dec orange zone", 6),
    (727, 103, 875, 501, "C8F8E0", 10, "dec mint zone", 6),
    (724, 300, 726, 460, "EADFB8", 10, "seam (mid rows)", 6),
    (224, 58, 737, 81, "C00000", 40, "title ink", 8),
    (213, 266, 275, 275, "6D99B4", 10, "enc Add&Norm top", 5),
    (215, 281, 274, 303, "807560", 10, "enc Feed Forward", 5),
    (214, 330, 275, 339, "6D99B4", 10, "enc Add&Norm bot", 5),
    (215, 345, 275, 368, "C87E57", 10, "enc MHA fill", 5),
    (237, 243, 289, 257, "FFFF00", 10, "enc yellow bar", 5),
    (161, 320, 181, 340, "C8A888", 10, "Nx circle", 5),
    (211, 400, 281, 462, "B08058", 10, "enc Output Embedding", 5),
    (215.5, 477, 223.5, 491, "C00000", 40, "enc Inputs arrow", 5),
    (752, 110, 795, 122, "FFFF00", 10, "dec Output box", 5),
    (744, 148, 796, 152, "A8ECBC", 10, "dec Softmax (mid rows)", 5),
    (748, 170, 800, 175, "B0E4CE", 10, "dec Linear (mid rows)", 5),
    (741, 201, 801, 210, "5C9CB7", 10, "dec Add&Norm top", 5),
    (742, 213, 801, 239, "6E7E62", 10, "dec Feed Forward", 5),
    (741, 255, 801, 264, "5C9CB7", 10, "dec Add&Norm mid", 5),
    (748, 273, 796, 292, "B28659", 10, "dec MHA fill", 5),
    (745, 320, 797, 327, "6E87E0", 10, "dec Add&Norm low", 5),
    (745, 340, 806, 382, "CE8ADC", 10, "dec Masked MHA", 5),
    (578, 148, 653, 159, "FFFFFF", 6, "callout 1", 5),
    (578, 172, 653, 182, "FFFFFF", 6, "callout 2", 5),
    (578, 289, 653, 325, "FFFFFF", 6, "callout 3", 5),
    (578, 346, 653, 356, "FFFFFF", 6, "callout 4", 5),
    (745, 408, 800, 455, "B8706C", 10, "dec Output Embedding", 5),
    (755, 476, 792, 487, "FFFF00", 10, "dec yellow bottom", 5),
    (660, 149, 698, 158, "C00000", 40, "callout 1 arrow", 5),
    (666, 299, 698, 311, "C00000", 40, "callout 3 arrow", 5),
    (265, 380, 275, 391, "C00000", 40, "enc Q circle", 5),
]
ok = 0
for t in T:
    ok += measure(t)
print(f"\n== {ok}/{len(T)} targets within 4px ==")
sys.exit(0 if ok == len(T) else 1)
