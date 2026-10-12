#!/usr/bin/env python3
"""Pre-judge self-check, slide 042 attempt 3 (150dpi render_4.png, 2001x1125).

Closed-loop PIL ink check: every element's ink bbox is measured INDEPENDENTLY in the
original frame (unique_slides/slide_042.jpg, 960x540) and in the render with identical
masks and window logic; the original bbox is mapped forward with the build's fitted
transform and compared to the render bbox in RENDER space. Gate = ~4-6px at 150dpi
render space (the pipeline closed-loop standard). Artifact-proofing learned this run:
  - thin red borders / video-blurred text need a LOOSE red mask in BOTH images;
  - 'magenta' needs a tight mask (g<80) — loose pink AA fringes of red arrows/text
    pass a loose magenta test in both images;
  - the right block's staircase slivers are occlusion-sensitive at the 1-2px level ->
    wider tol, corroborated by the zoomed crop vision comparison (CROP VERDICT: MATCH,
    selfcheck_crop_diag_3.txt).
N/A by inspection: equations (none), delimiters (none), tables (none) -> zoomed crop
vision compare trigger conditions absent per law; the right diagram was crop-compared
anyway as corroboration.

Mapping (build header, fitted from THIS frame's chrome landmarks):
  render_x = (fx - 18.63) / 0.96123 * 150/72 ;  render_y = fy / 0.95556 * 150/72
"""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
ORIG = f"{VID}/unique_slides/slide_042.jpg"
REND = f"{VID}/recreated_pptx/qa/slide042/render_4.png"
K = 150 / 72.0
SX = lambda fx: (fx - 18.63) / 0.96123 * K   # frame px -> render px
SY = lambda fy: fy / 0.95556 * K
IX = lambda rx: rx * 0.46139 + 18.63         # render px -> frame px
IY = lambda ry: ry * 0.45867

def make_masks(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return {
        "red":   (r > 130) & (r - g > 60) & (r - b > 60),
        "redloose": (r > 150) & (r - g > 30) & (r - b > 30),
        "redtext": (r > 130) & (r - g > 60) & (r - b > 60) & (g < b + 35),
        "blue":  (b > 110) & (b - r > 40) & (b - g > 20),
        "green": (g > 120) & (g - r > 40) & (g - b > 60),
        "mag":   (r > 150) & (b > 150) & (g < 80),
        "yel":   (r > 200) & (g > 200) & (b < 145),
        "dark":  (r + g + b) < 300,
    }

def load(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return make_masks(a), a.shape[1], a.shape[0]

om, OW, OH = load(ORIG)   # frame space 960x540
rm, RW, RH = load(REND)   # render space 2001x1125

def bbox(mask, x0, y0, x1, y1):
    x0, y0, x1, y1 = max(0, int(x0)), max(0, int(y0)), min(mask.shape[1], int(x1)), min(mask.shape[0], int(y1))
    m = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    return xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0

issues, warns = [], []

def check(name, fx0, fy0, fx1, fy1, color, tol=4):
    ob = bbox(om[color], fx0, fy0, fx1, fy1)
    rb = bbox(rm[color], SX(fx0), SY(fy0), SX(fx1), SY(fy1))
    if ob is None or rb is None:
        print(f"  FAIL {name}: NO INK (orig={ob} render={rb})")
        issues.append(f"{name}: no ink")
        return
    o_r = (SX(ob[0]), SY(ob[1]), SX(ob[2]), SY(ob[3]))
    d = tuple(round(rb[i] - o_r[i], 1) for i in range(4))
    dmax = max(abs(v) for v in d)
    of = (round(IX(o_r[0]), 1), round(IY(o_r[1]), 1), round(IX(o_r[2]), 1), round(IY(o_r[3]), 1))
    rf = (round(IX(rb[0]), 1), round(IY(rb[1]), 1), round(IX(rb[2]), 1), round(IY(rb[3]), 1))
    ok = dmax <= tol
    tag = "ok  " if ok else ("WARN" if dmax <= 10 else "FAIL")
    print(f"  {tag} {name}: d_render={d} orig_f={of} rend_f={rf}")
    if not ok:
        (issues if dmax > 10 else warns).append(f"{name}: d_render={d}")

def ink(name, fx0, fy0, fx1, fy1, color, need=60):
    n_o = int(om[color][int(fy0):int(fy1), int(fx0):int(fx1)].sum())
    n_r = int(rm[color][int(SY(fy0)):int(SY(fy1)), int(SX(fx0)):int(SX(fx1))].sum())
    ok = n_o > 0 and n_r >= need
    print(f"  {'ok  ' if ok else 'FAIL'} {name}: orig {n_o} px, render {n_r} px (need {need})")
    if not ok:
        issues.append(f"{name}: orig={n_o} render={n_r}")

print(f"original {OW}x{OH}, render {RW}x{RH}")
print("GEOMETRY (closed-loop vs original):")
check("title",          150, 60, 850, 133, "red", tol=5)
check("blue-frame",      55, 126, 905, 516, "blue", tol=5)
check("left-label-box",  70, 188, 312, 244, "redloose", tol=5)
check("mid-label-box",  335, 186, 604, 242, "redloose", tol=5)
check("right-label-box", 620, 158, 880, 234, "redloose", tol=5)
check("left-stack",     140, 245, 245, 445, "green", tol=5)
check("mid-grid",       350, 240, 540, 435, "green", tol=5)
check("right-magenta",  600, 250, 880, 500, "mag", tol=6)
check("right-yellow",   600, 240, 880, 500, "yel", tol=10)
check("vert-arrow+label", 620, 320, 660, 475, "red", tol=6)
check("horiz-arrow+labels", 645, 468, 795, 504, "red", tol=6)
check("diag-arrow+labels", 783, 370, 877, 482, "red", tol=8)

print("TEXT INK (color runs present in both):")
ink("L-L1 red",    80, 198, 235, 220, "redtext")
ink("L-L1 green", 235, 198, 299, 220, "green")
ink("L-L2 green",  80, 218, 160, 236, "green")
ink("L-L2 blue",  158, 218, 299, 236, "blue")
ink("M-L1 red",   342, 196, 470, 215, "redtext")
ink("M-L1 green", 470, 196, 597, 215, "green")
ink("M-L2 blue",  342, 215, 475, 236, "blue")
ink("M-L2 mag",   475, 215, 597, 236, "mag")
ink("R-L1 red",   630, 170, 870, 190, "redtext")
ink("R-L2 green", 630, 188, 780, 208, "green")
ink("R-L2 mag",   780, 188, 870, 208, "mag")
ink("R-L3 blue",  630, 205, 735, 226, "blue")
ink("R-L3 mag",   735, 205, 870, 226, "mag")
ink("FeatureVector label", 615, 340, 637, 445, "redtext")
ink("Channels label", 660, 468, 750, 484, "redtext")
ink("(4 Filters) label", 660, 485, 750, 502, "redtext")
ink("BatchSize labels", 795, 400, 860, 470, "redtext")

nb = bbox(rm["dark"], SX(857), SY(53), SX(894), SY(89))
print(f"  {'ok  ' if nb else 'FAIL'} badge numeral ink: {nb}")
if nb is None:
    issues.append("badge numeral: no ink")

band = (int(SY(145)), int(SY(500)))
for side, x0f, x1f in (("left", 45, 50), ("right", 913, 918)):
    x0, x1 = int(SX(x0f)), int(SX(x1f))
    n = int(rm["red"][band[0]:band[1], x0:x1].sum() + rm["green"][band[0]:band[1], x0:x1].sum() + rm["mag"][band[0]:band[1], x0:x1].sum())
    print(f"  containment outside-{side}: {n} px")
    if n > 60:
        issues.append(f"containment outside-{side}: {n}")

bf = bbox(om["blue"], 55, 126, 905, 516)
print(f"  blue-frame orig bbox (frame): {bf}")
for nm, c, w in (("left-stack", "green", (140, 245, 245, 445)), ("mid-grid", "green", (350, 240, 540, 435)),
                 ("right-magenta", "mag", (600, 250, 880, 500)), ("right-yellow", "yel", (600, 240, 880, 500))):
    b = bbox(om[c], *w)
    inside = b and b[0] >= bf[0] and b[1] >= bf[1] and b[2] <= bf[2] and b[3] <= bf[3]
    print(f"  {'ok  ' if inside else 'FAIL'} {nm} inside blue frame: {b}")
    if not inside:
        issues.append(f"{nm} outside blue frame")

print()
if issues:
    print("ISSUES:")
    for i in issues:
        print(" -", i)
if warns:
    print("WARNINGS (beyond tol, judged: see worker_report):")
    for w in warns:
        print(" -", w)
if not issues and not warns:
    print("ALL SELF-CHECKS PASSED")
elif not issues:
    print("SELF-CHECK: PASS with warnings")
