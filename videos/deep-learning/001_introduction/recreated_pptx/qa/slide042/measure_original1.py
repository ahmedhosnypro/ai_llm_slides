#!/usr/bin/env python3
"""Slide 042 forensics pass 1 — measure every region's ink bbox + modal colors from the
ground-truth frame videos/deep-learning/001_introduction/unique_slides/slide_042.jpg
(960x540, 1px = 1pt = 1/72 in).
Regions (spec %): title 0-15%h; input slab 8-30%w 30-65%h; filter stack 28-48%w 35-60%h;
= sign 50-55%w 45-52%h; output box 58-92%w 25-65%h; equation box 35-55%w 60-85%h;
legend 10-25%w 68-92%h."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_042.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
print(f"frame {W}x{H}")
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def modal(x0, x1, y0, y1, label, mask=None):
    reg = IM[y0:y1+1, x0:x1+1].reshape(-1, 3)
    if mask is not None:
        reg = mask[y0:y1+1, x0:x1+1]
        reg = reg.reshape(-1, 3)
        reg = reg[(reg[:, 0] + reg[:, 1] + reg[:, 2]) >= 0]
    vals, counts = np.unique(reg, axis=0, return_counts=True)
    order = np.argsort(-counts)[:4]
    print(f"{label}: " + ", ".join('#%02X%02X%02X(%d)' % (*vals[i], counts[i]) for i in order))

def bbox(mask, x0, x1, y0, y1, label, minpix=1):
    sub = np.zeros_like(mask)
    sub[y0:y1+1, x0:x1+1] = mask[y0:y1+1, x0:x1+1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        print(f"{label}: EMPTY"); return None
    print(f"{label}: x {xs.min()}..{xs.max()}  y {ys.min()}..{ys.max()}  (n={len(xs)})")
    return (xs.min(), xs.max(), ys.min(), ys.max())

# ---- global background / chrome sanity ----
modal(5, 35, 100, 300, "canvas (left margin)")
modal(400, 560, 150, 180, "panel area above volumes")

# ---- red masks: title + panel border + red filter slice ----
red = (r > 130) & (g < 100) & (b < 100)
print("\n--- RED ink ---")
bbox(red, 0, W, 40, 130, "title red ink (y40-130)")
# panel border: long red runs
print("red horiz runs >=100px (y 120..540):")
for y in range(120, 540):
    xs = np.where(red[y])[0]
    if len(xs) >= 100:
        runs = []; s = p = xs[0]
        for c in xs[1:]:
            if c <= p + 2: p = c
            else: runs.append((s, p)); s = p = c
        runs.append((s, p))
        for (a, bb) in runs:
            if bb - a + 1 >= 100: print(f"  y={y}: x {a}..{bb} len {bb-a+1}")
print("red vert runs >=100px (x 0..960):")
for x in range(0, 960):
    ys = np.where(red[:, x])[0]
    if len(ys) >= 100:
        runs = []; s = p = ys[0]
        for c in ys[1:]:
            if c <= p + 2: p = c
            else: runs.append((s, p)); s = p = c
        runs.append((s, p))
        for (a, bb) in runs:
            if bb - a + 1 >= 100: print(f"  x={x}: y {a}..{bb} len {bb-a+1}")

# ---- title metrics ----
tmask = np.zeros_like(red); tmask[40:130, 40:920] = red[40:130, 40:920]
ys = np.where(tmask.sum(axis=1) > 0)[0]
xs = np.where(tmask.sum(axis=0) > 0)[0]
print(f"title ink: x {xs.min()}..{xs.max()} (center {(xs.min()+xs.max())/2})  y {ys.min()}..{ys.max()}")
modal(0, W, 0, H, "title ink modal", mask=tmask)
# cap height of 'O' in Output: first ink cols
segO = tmask[:, xs.min():xs.min()+22]
ysO = np.where(segO.sum(axis=1) > 0)[0]
print(f"'O' cap: y {ysO.min()}..{ysO.max()} cap-height {ysO.max()-ysO.min()+1}")
# descender: 'p' in Output
print("title rows profile (rowsum>0):", ys.min(), ys.max())

# ---- input slab oranges ----
print("\n--- INPUT SLAB oranges ---")
orange_mid = (r > 160) & (r < 215) & (g > 90) & (g < 135) & (b < 80)          # C87137-ish front
orange_light = (r > 215) & (g > 130) & (g < 175) & (b > 60) & (b < 110)       # E09050 top
orange_dark = (r > 140) & (r < 185) & (g > 70) & (g < 105) & (b < 60)         # A85B28 side
modal(60, 320, 150, 370, "input slab region modal")
bbox(orange_mid, 40, 340, 130, 400, "input front-face mask")
bbox(orange_light, 40, 340, 130, 400, "input top-face mask")
bbox(orange_dark, 40, 340, 130, 400, "input side-face mask")

# ---- filter stack colors ----
print("\n--- FILTER STACK ---")
modal(250, 480, 170, 340, "filter stack region modal")
cyan = (b > 200) & (g > 180) & (r < 180)
green = (g > 140) & (r < 110) & (b < 140)
redf = (r > 200) & (g < 110) & (b < 110)
yellow = (r > 220) & (g > 210) & (b < 140)
purple = (r > 160) & (r < 210) & (b > 190) & (g < 190)
bbox(cyan, 250, 500, 150, 360, "cyan slice")
bbox(green, 250, 500, 150, 360, "green slice")
bbox(redf, 250, 500, 150, 360, "red slice")
bbox(yellow, 250, 500, 150, 360, "yellow slice")
bbox(purple, 250, 500, 150, 360, "purple slice")

# ---- equals sign (black ink, center) ----
print("\n--- EQUALS + OUTPUT BOX ---")
black = (r < 90) & (g < 90) & (b < 90)
bbox(black, 470, 545, 230, 300, "= sign black ink (470-545, 230-300)")

modal(540, 900, 120, 370, "output box region modal")
tan_front = (r > 225) & (g > 200) & (g < 235) & (b > 145) & (b < 185)   # F0DCA8-ish
tan_top = (r > 215) & (g > 185) & (b > 120) & (b < 155)                  # E3C98A-ish
tan_side = (r > 195) & (r < 235) & (g > 165) & (g < 200) & (b > 90) & (b < 130)  # D9B96E-ish
bbox(tan_front, 530, 920, 110, 380, "output front-face mask")
bbox(tan_top, 530, 920, 110, 380, "output top-face mask")
bbox(tan_side, 530, 920, 110, 380, "output side-face mask")

# ---- equation box ----
print("\n--- EQUATION BOX ---")
white = (r > 235) & (g > 235) & (b > 235)
bbox(white, 320, 545, 300, 480, "equation box white (320-545, 300-480)")
bbox(black, 320, 545, 300, 480, "equation box region black ink (border+text)")
modal(320, 545, 300, 480, "equation box region modal")

# ---- legend ----
print("\n--- LEGEND ---")
blueleg = (b > 120) & (r < 110) & (g < 110) & (b > r + 50)
bbox(blueleg, 60, 300, 350, 520, "legend blue symbols (60-300, 350-520)")
bbox(black, 60, 300, 350, 520, "legend black text (60-300, 350-520)")
modal(60, 300, 350, 520, "legend region modal")

# ---- black bottom strip ----
print("\n--- BOTTOM STRIP ---")
dark_rows = [y for y in range(500, H) if (IM[y].sum(axis=1) < 200).sum() > 500]
print("dark full-width rows:", dark_rows[:5], "...", dark_rows[-5:] if dark_rows else "none")
