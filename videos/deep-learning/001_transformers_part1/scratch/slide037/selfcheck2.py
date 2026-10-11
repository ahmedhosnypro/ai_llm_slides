#!/usr/bin/env python3
"""Attempt-2 self-check battery (banked): containment, equations, structure regions."""
import numpy as np
from PIL import Image

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide037"
ren = np.asarray(Image.open(f"{SCR}/render-1.png").convert("RGB")).astype(int)
org = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_037.jpg").convert("RGB")).astype(int)
s = ren.shape[1] / 960.0
ok = True

def ink(img, region, kind, scale=1.0):
    x0, y0, x1, y1 = [int(v * scale) for v in region]
    sub = img[y0:y1, x0:x1]
    R, G, B = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    if kind == "red":
        m = (R > 110) & (R - G > 45) & (R - B > 45)
    elif kind == "dark":
        m = ((R < 130) & (G < 130) & (B < 130)) | ((R > 110) & (R - G > 45) & (R - B > 45))
    else:
        m = (np.abs(R - 247) + np.abs(G - 226) + np.abs(B - 205)) > 70
    ys, xs = np.where(m)
    if len(ys) == 0:
        return None
    return (xs.min() / scale + region[0], ys.min() / scale + region[1],
            xs.max() / scale + region[0], ys.max() / scale + region[1], int(len(ys)))

def cmp(name, region, kind, tol=4):
    global ok
    o = ink(org, region, kind)
    r = ink(ren, region, kind, s)
    fmt = lambda c: "NONE" if c is None else f"x[{c[0]:.0f},{c[2]:.0f}] y[{c[1]:.0f},{c[3]:.0f}] n={c[4]}"
    line = f"{name}: orig {fmt(o)} | mine {fmt(r)}"
    if o is None or r is None:
        if o is None and r is None:
            print(f"  {line}  -> both empty OK")
        else:
            print(f"  {line}  -> MISMATCH (one side empty)")
            ok = False
        return
    dx = max(abs(o[0] - r[0]), abs(o[2] - r[2]))
    dy = max(abs(o[1] - r[1]), abs(o[3] - r[3]))
    verdict = "OK" if (dx <= tol and dy <= tol) else ("SOFT" if (dx <= 6 and dy <= 6) else "FAIL")
    if verdict == "FAIL":
        ok = False
    print(f"  {line}  -> dx={dx:.1f} dy={dy:.1f} {verdict}")

print("== equations (closed-loop, tol 4px frame) ==")
cmp("fraction numerator", (408, 185, 455, 206), "red")
cmp("fraction bar+denom", (408, 204, 458, 234), "red")
cmp("K.q label", (340, 192, 375, 218), "red")
cmp("legend 1xd (a)", (768, 480, 800, 496), "red")
cmp("legend 1xd (b)", (834, 493, 862, 505), "red")
cmp("legend dxd (c)", (826, 504, 856, 516), "red")

print("== titles ==")
cmp("title L1", (60, 50, 860, 80), "dark")
cmp("title L2", (60, 79, 860, 106), "dark")

print("== structure (any-ink bboxes vs peach) ==")
for name, region in [
    ("Y2 block", (540, 115, 628, 150)),
    ("sigma box", (505, 188, 665, 222)),
    ("scaling box", (366, 172, 426, 240)),
    ("softmax top", (453, 188, 495, 230)),
    ("dotbox top", (250, 188, 355, 235)),
    ("pill Similarity", (265, 156, 342, 190)),
    ("pill Proba", (426, 156, 516, 190)),
    ("pill WSUM", (592, 156, 696, 190)),
    ("wk box row1", (148, 228, 198, 264)),
    ("wv box row1", (696, 228, 749, 264)),
    ("k stack row1", (199, 226, 236, 248)),
    ("v stack row1", (664, 226, 702, 248)),
    ("Wq box", (276, 431, 318, 465)),
    ("q2 vec", (301, 409, 341, 429)),
    ("strip", (176, 469, 494, 520)),
    ("legend box", (732, 462, 912, 532)),
    ("left container", (54, 222, 146, 398)),
    ("right container", (751, 222, 849, 398)),
]:
    cmp(name, region, "any")

print("== containment: non-chrome ink outside panel (x42-918, y45-539) ==")
R, G, B = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
nonwhite = (np.abs(R - 255) + np.abs(G - 255) + np.abs(B - 255)) > 40
x0, x1 = int(42 * s), int(918 * s)
y0 = int(45 * s)
out_left = int(nonwhite[y0:, :x0 - 2].sum())
out_right = int(nonwhite[y0:, x1 + 3:].sum())
out_top = int(nonwhite[:y0 - 2, x0:x1].sum())
print(f"   ink px outside panel: left={out_left} right={out_right} top={out_top}")
if out_left + out_right + out_top > 60:
    ok = False
    print("   CONTAINMENT FAIL")
else:
    print("   containment OK")

print("== wrap check: multi-line/text bands ==")
cmp("dot header band", (255, 196, 345, 232), "dark", tol=5)
print()
print("OVERALL:", "PASS" if ok else "FAIL")
