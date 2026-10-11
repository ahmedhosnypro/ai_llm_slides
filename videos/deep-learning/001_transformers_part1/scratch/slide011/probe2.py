#!/usr/bin/env python3
"""Final targeted probes on slide_011.jpg."""
import numpy as np
from PIL import Image

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_011.jpg").convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = a.shape[:2]

def runs_of(idx, gap=2, minlen=1):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i <= p + gap: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return [(s, e) for (s, e) in out if e - s + 1 >= minlen]

def win_ink(name, x0, y0, x1, y1, mask_fn, gap=4):
    m = np.zeros((H, W), bool)
    sub = mask_fn(r[y0:y1, x0:x1], g[y0:y1, x0:x1], b[y0:y1, x0:x1])
    m[y0:y1, x0:x1] = sub
    ys, xs = np.where(m)
    if not len(xs):
        print(f"{name}: NO INK"); return
    print(f"{name}: n={len(xs)} bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]")
    rc = np.bincount(ys, minlength=H)
    for (s, e) in runs_of(np.where(rc >= 1)[0], gap=gap):
        band = m[s:e+1, :]
        cc = np.bincount(np.where(band)[1], minlength=W)
        print(f"   y[{s},{e}] xruns: {runs_of(np.where(cc >= 1)[0], gap=gap)[:16]}")

dark = lambda r, g, b: (r < 140) & (g < 140) & (b < 140)
grayink = lambda r, g, b: (r > 70) & (r < 200) & (np.abs(r - g) < 25) & (np.abs(g - b) < 25) & (np.abs(r - b) < 25)
reddish = lambda r, g, b: (r > 130) & (r - g > 55) & (r - b > 45)
salmon = lambda r, g, b: (r > 215) & (r - b > 25) & (g > 120) & (g < 215) & (b > 110) & (b < 215) & (r - g > 12)

# 1. o-label + arrow windows
win_ink("o1 window", 520, 105, 610, 168, dark, gap=3)
win_ink("o2 window", 655, 105, 745, 168, dark, gap=3)
win_ink("o3 window", 780, 105, 880, 168, dark, gap=3)
# 2. attention box + text
win_ink("attention box/text", 215, 235, 355, 292, grayink, gap=4)
# 3. salmon curves between sub-blocks
win_ink("salmon curves zone", 400, 235, 590, 320, salmon, gap=6)
# 4. red arc zone (between blocks)
win_ink("red arc zone", 440, 245, 540, 345, reddish, gap=5)
# 5. self-loops zone
win_ink("self-loops zone", 630, 275, 850, 345, dark, gap=4)
# 6. fan lines zone (between attention box and orange top)
win_ink("fan lines zone", 110, 270, 480, 310, dark, gap=6)
# 7. x-labels
win_ink("x1 label", 120, 465, 200, 500, dark, gap=3)
win_ink("x2 label", 250, 465, 330, 500, dark, gap=3)
win_ink("x3 label", 385, 465, 460, 500, dark, gap=3)
# 8. vertical input lines precise
win_ink("input line 1", 140, 450, 170, 500, lambda r, g, b: (r < 190) & (np.abs(r-g) < 30) & (np.abs(g-b) < 30), gap=2)
# 9. Decoder label full bbox
win_ink("Decoder label", 660, 88, 790, 115, reddish, gap=3)
# 10. title bbox
win_ink("title", 340, 50, 600, 92, reddish, gap=4)
# 11. subtitle bbox
win_ink("subtitle", 320, 90, 610, 118, lambda r, g, b: (b - r > 40) & (b > 150), gap=4)
# 12. enc-side label
win_ink("enc-side label", 160, 192, 410, 218, lambda r, g, b: (b - r > 40) & (b > 150), gap=4)
# 13. dec-side label
win_ink("dec-side label", 610, 344, 870, 370, lambda r, g, b: (b - r > 40) & (b > 150), gap=4)
# 14. bottom strip probe: mean colors along rows
for yy in (505, 512, 518, 524, 528, 532):
    vals = [tuple(a[yy, xx]) for xx in (60, 150, 250, 350, 440)]
    print(f"row y={yy}: {vals}")
# 15. note box border probe: colors at box edges
print("notebox top edge y=412..416 @x=600:", [tuple(a[yy, 600]) for yy in range(410, 418)])
print("notebox left edge x=458..464 @y=470:", [tuple(a[470, xx]) for xx in range(456, 466)])
print("notebox bottom edge y=518..526 @x=600:", [tuple(a[yy, 600]) for yy in range(516, 527)])
# 16. badge probe
print("badge rows y=53..90 @x=893:", [tuple(a[yy, 893]) for yy in (53, 57, 71, 85, 89)])
print("badge cols x=875..911 @y=71:", [tuple(a[71, xx]) for xx in (875, 879, 893, 907, 911)])
# 17. encoder/decoder block edges precise (row/col scans)
print("orange top edge col x=250, y=300..312:", [tuple(a[yy, 250]) for yy in range(300, 313)])
print("orange bottom edge col x=250, y=446..458:", [tuple(a[yy, 250]) for yy in range(446, 459)])
print("orange left edge row y=380, x=42..54:", [tuple(a[380, xx]) for xx in range(42, 55)])
print("orange right edge row y=380, x=484..496:", [tuple(a[380, xx]) for xx in range(484, 497)])
print("yellow top edge col x=700, y=158..168:", [tuple(a[yy, 700]) for yy in range(158, 169)])
print("yellow bottom edge col x=700, y=278..290:", [tuple(a[yy, 700]) for yy in range(278, 291)])
print("yellow left edge row y=220, x=474..486:", [tuple(a[220, xx]) for xx in range(474, 487)])
print("yellow right edge row y=220, x=896..908:", [tuple(a[220, xx]) for xx in range(896, 909)])
# 18. encoder sub-block edges
print("encsub col x=300, y=220..232:", [tuple(a[yy, 300]) for yy in range(220, 233)])
print("encsub col x=300, y=292..304:", [tuple(a[yy, 300]) for yy in range(292, 305)])
print("encsub row y=260, x=104..118:", [tuple(a[260, xx]) for xx in range(104, 119)])
print("encsub row y=260, x=468..482:", [tuple(a[260, xx]) for xx in range(468, 483)])
# 19. decoder sub-block edges
print("decsub col x=700, y=282..296:", [tuple(a[yy, 700]) for yy in range(282, 297)])
print("decsub col x=700, y=332..344:", [tuple(a[yy, 700]) for yy in range(332, 345)])
print("decsub row y=320, x=492..506:", [tuple(a[320, xx]) for xx in range(492, 507)])
print("decsub row y=320, x=848..862:", [tuple(a[320, xx]) for xx in range(848, 863)])
