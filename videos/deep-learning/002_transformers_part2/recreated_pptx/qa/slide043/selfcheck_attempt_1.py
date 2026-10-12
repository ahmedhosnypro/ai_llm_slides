#!/usr/bin/env python3
"""Slide 043 self-check attempt 1: closed-loop render-vs-original band comparison.
Render 2001x1125 @150dpi; frame-px equivalent = render_px * 72/150 mapped back via
the inverse transform. All comparisons reported in FRAME px (960x540)."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide043/render_1.png"
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_043.jpg"

ren = np.asarray(Image.open(R).convert("RGB")).astype(int)
fra = np.asarray(Image.open(F).convert("RGB")).astype(int)

# render px -> frame px: frame_x = px*(72/150)*0.96123 + 18.63 ; frame_y = py*(72/150)*0.95556
def px2fx(px): return px * (72 / 150) * 0.96123 + 18.63
def px2fy(py): return py * (72 / 150) * 0.95556
def fx2px(fx): return (fx - 18.63) / 0.96123 * 150 / 72
def fy2py(fy): return fy / 0.95556 * 150 / 72

def band(im, mask_fn, x0, x1, y0, y1, axis):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    m = mask_fn(r, g, b)[y0:y1, x0:x1]
    if axis == "rows":
        prof = m.sum(axis=1)
    else:
        prof = m.sum(axis=0)
    nz = np.where(prof > (2 if axis == "rows" else 2))[0]
    if not len(nz): return None
    return (nz.min() + (y0 if axis == "rows" else x0), nz.max() + (y0 if axis == "rows" else x0))

redc = lambda r, g, b: (r > 130) & (r - g > 50) & (r - b > 40) & (g < b + 35)
mag = lambda r, g, b: (r > 110) & (g < 60) & (b > 110) & (b - g > 80) & (r - g > 90)
blue = lambda r, g, b: (b - r > 40) & (b - g > 20) & (b > 80)
grn = lambda r, g, b: (g - r > 30) & (g - b > 30) & (g > 100)
dark = lambda r, g, b: (r < 110) & (g < 110) & (b < 110)

results = []
def cmp(tag, orig, rend, tol=3.0):
    if orig is None or rend is None:
        results.append(f"{tag}: MISSING orig={orig} rend={rend}")
        return
    d = max(abs(orig[0] - rend[0]), abs(orig[1] - rend[1]))
    ok = "OK " if d <= tol else "DIFF"
    results.append(f"{tag}: orig {orig} rend {rend}  max|d|={d:.1f}fp (tol {tol}) {ok}")

# --- title (red core) ---
o = band(fra, redc, 200, 850, 50, 100, "rows"); rr = band(ren, redc, int(fx2px(200)), int(fx2px(850)), int(fy2py(50)), int(fy2py(100)), "rows")
cmp("title rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 2.5)
o = band(fra, redc, 200, 850, 50, 100, "cols"); rr = band(ren, redc, int(fx2px(200)), int(fx2px(850)), int(fy2py(50)), int(fy2py(100)), "cols")
cmp("title cols", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 3.5)

# --- right stack magenta front ---
o = band(fra, mag, 650, 810, 140, 330, "rows"); rr = band(ren, mag, int(fx2px(650)), int(fx2px(810)), int(fy2py(140)), int(fy2py(330)), "rows")
cmp("RS front rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 3.0)
o = band(fra, mag, 650, 810, 140, 330, "cols"); rr = band(ren, mag, int(fx2px(650)), int(fx2px(810)), int(fy2py(140)), int(fy2py(330)), "cols")
cmp("RS front cols", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 3.0)

# --- right stack slivers at y=210 (G/O/Y/B boundaries) ---
def slivers(im, y, x0=795, x1=880):
    out = []
    for x in range(x0, x1):
        px_r, px_g, px_b = im[y, x]
        t = None
        if px_g > 180 and px_r < 190 and px_b < 110: t = "G"
        elif px_r > 200 and 80 <= px_g < 160 and px_b < 90: t = "O"
        elif px_r > 200 and px_g > 190 and px_b < 130: t = "Y"
        elif 90 <= px_r < 180 and 110 <= px_g < 200 and px_b > 160: t = "B"
        if t and (not out or out[-1][2] != t): out.append((x, x, t))
        elif t: out[-1] = (out[-1][0], x, t)
    return [s for s in out if s[1] - s[0] >= 2]
ys_rend = [int(fy2py(210)), int(fy2py(250))]
print("RS slivers orig y210:", slivers(fra, 210))
def slivers_rend(fy):
    py = int(fy2py(fy))
    out = []
    prev = None
    for fx in range(795, 880):
        px = int(fx2px(fx)); px_r, px_g, px_b = ren[py, px]
        t = None
        if px_g > 180 and px_r < 190 and px_b < 110: t = "G"
        elif px_r > 200 and 80 <= px_g < 160 and px_b < 90: t = "O"
        elif px_r > 200 and px_g > 190 and px_b < 130: t = "Y"
        elif 90 <= px_r < 180 and 110 <= px_g < 200 and px_b > 160: t = "B"
        if t and (not out or out[-1][2] != t): out.append([fx, fx, t])
        elif t: out[-1][1] = fx
    return [tuple(s) for s in out if s[1]-s[0] >= 2]
print("RS slivers rend y210:", slivers_rend(210))
print("RS slivers rend y250:", slivers_rend(250))
print("RS slivers orig y250:", slivers(fra, 250))

# --- left stack magenta front ---
o = band(fra, mag, 100, 215, 150, 350, "rows"); rr = band(ren, mag, int(fx2px(100)), int(fx2px(215)), int(fy2py(150)), int(fy2py(350)), "rows")
cmp("LS front rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 3.0)
o = band(fra, mag, 100, 215, 150, 350, "cols"); rr = band(ren, mag, int(fx2px(100)), int(fx2px(215)), int(fy2py(150)), int(fy2py(350)), "cols")
cmp("LS front cols", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 3.0)

# --- left stack mass silhouette (non-panel ink) at rows 150/210/270/330 ---
panel = lambda r, g, b: (abs(r - 233) < 14) & (abs(g - 233) < 14) & (abs(b - 231) < 16)
for fy in [150, 210, 270, 330]:
    def inkrow_fr(y):
        r, g, b = fra[y, :, 0], fra[y, :, 1], fra[y, :, 2]
        m = ~panel(r, g, b)
        xs = np.where(m[100:340])[0]
        return (xs.min() + 100, xs.max() + 100) if len(xs) else None
    def inkrow_ren(fy):
        py = int(fy2py(fy))
        xs = []
        for fx in range(100, 340):
            px = int(fx2px(fx))
            c = ren[py, px]
            if not (abs(c[0]-233) < 14 and abs(c[1]-233) < 14 and abs(c[2]-231) < 16):
                xs.append(fx)
        return (xs[0], xs[-1]) if xs else None
    o = inkrow_fr(fy)
    rr = inkrow_ren(fy)
    if o and rr: cmp(f"LS mass row y{fy}", o, rr, 6.0)
    else: results.append(f"LS mass row y{fy}: orig={o} rend={rr}")

# --- callout box: cream fill + red border ---
cream = lambda r, g, b: (r > 240) & (g > 240) & (b > 200) & (b < 245)
o = band(fra, cream, 320, 660, 160, 280, "cols"); rr = band(ren, cream, int(fx2px(320)), int(fx2px(660)), int(fy2py(160)), int(fy2py(280)), "cols")
cmp("callout cream cols", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 4.0)
o = band(fra, cream, 320, 660, 160, 280, "rows"); rr = band(ren, cream, int(fx2px(320)), int(fx2px(660)), int(fy2py(160)), int(fy2py(280)), "rows")
cmp("callout cream rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 4.0)
# callout text lines (ink in x340..620)
ink = lambda r, g, b: (r < 170) | ((r - g > 60) & (r - b > 60)) | ((b - r > 40) & (b > 80)) | ((g - r > 30) & (g - b > 30))
for tag, y0, y1 in [("C-L1", 176, 196), ("C-L2", 196, 219), ("C-L3", 219, 240), ("C-L4", 241, 262)]:
    o = band(fra, ink, 336, 620, y0, y1, "rows")
    rr = band(ren, ink, int(fx2px(336)), int(fx2px(620)), int(fy2py(y0)), int(fy2py(y1)), "rows")
    cmp(f"{tag} rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 3.0)

# --- bottom box: green border + text bands ---
o = band(fra, grn, 60, 900, 340, 510, "rows"); rr = band(ren, grn, int(fx2px(60)), int(fx2px(900)), int(fy2py(340)), int(fy2py(510)), "rows")
cmp("bottom green rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 3.0)
o = band(fra, grn, 60, 900, 340, 510, "cols"); rr = band(ren, grn, int(fx2px(60)), int(fx2px(900)), int(fy2py(340)), int(fy2py(510)), "cols")
cmp("bottom green cols", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 3.0)
ink2 = lambda r, g, b: (r < 170) | ((r - g > 60) & (r - b > 60)) | ((b - r > 40) & (b > 80))
for tag, y0, y1 in [("B-L1a", 364, 384), ("B-L1b", 385, 407), ("B-L2", 428, 450), ("B-L3", 471, 493)]:
    o = band(fra, ink2, 88, 850, y0, y1, "rows")
    rr = band(ren, ink2, int(fx2px(88)), int(fx2px(850)), int(fy2py(y0)), int(fy2py(y1)), "rows")
    cmp(f"{tag} rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 3.0)
# B-L1a/B-L1b/B-L2/B-L3 x-extents
for tag, y0, y1 in [("B-L1a x", 366, 382), ("B-L1b x", 388, 404), ("B-L2 x", 431, 447), ("B-L3 x", 474, 490)]:
    o = band(fra, ink2, 88, 860, y0, y1, "cols")
    rr = band(ren, ink2, int(fx2px(88)), int(fx2px(860)), int(fy2py(y0)), int(fy2py(y1)), "cols")
    cmp(f"{tag}", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 5.0)

# --- arrows: v shaft x, h shaft y, d line ---
# v-arrow red ink column profile x630..670 (excl block edge)
o = band(fra, redc, 630, 668, 185, 300, "cols"); rr = band(ren, redc, int(fx2px(630)), int(fx2px(668)), int(fy2py(185)), int(fy2py(300)), "cols")
cmp("v-arrow/label cols", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 4.0)
# h-arrow: red ink rows y325..340
wash = lambda r, g, b: (r > 150) & (r - g > 25) & (r - b > 15) & (g < 190)
o = band(fra, wash, 660, 800, 326, 340, "rows"); rr = band(ren, wash, int(fx2px(660)), int(fx2px(800)), int(fy2py(326)), int(fy2py(340)), "rows")
cmp("h-arrow rows", o, None if rr is None else (px2fy(rr[0]), px2fy(rr[1])), 3.0)
# Channels text cols
o = band(fra, redc, 680, 760, 315, 330, "cols"); rr = band(ren, redc, int(fx2px(680)), int(fx2px(760)), int(fy2py(315)), int(fy2py(330)), "cols")
cmp("Channels cols", o, None if rr is None else (px2fx(rr[0]), px2fx(rr[1])), 4.0)

print("\n".join(results))
