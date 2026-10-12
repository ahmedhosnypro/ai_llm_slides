#!/usr/bin/env python3
"""Forensics pass 4: correct ink mask (vs panel gray E9E9E7 / white), def+Remember
borders, starburst, title band, text lines per region."""
from PIL import Image
import numpy as np

im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# ink = clearly darker than white/panel OR strongly colored
mn = a.min(axis=2); mx = a.max(axis=2)
ink = (mn < 205) | (mx - mn > 45)

def bands(y0, y1, x0, x1, minpx=3, label=""):
    print(f"== bands {label} (y{y0}..{y1}, x{x0}..{x1}) ==")
    inband = False; b0 = 0
    for y in range(y0, y1):
        n = int(ink[y, x0:x1].sum())
        if n >= minpx and not inband:
            inband = True; b0 = y
        elif n < minpx and inband:
            inband = False
            ys, xs = np.where(ink[b0:y, x0:x1])
            print(f"  band y{b0}..{y-1} h={y-b0} x{x0+xs.min()}..{x0+xs.max()}")
    if inband:
        ys, xs = np.where(ink[b0:y1, x0:x1])
        print(f"  band y{b0}..{y1-1} h={y1-b0} x{x0+xs.min()}..{x0+xs.max()}")

def modal(y0, y1, x0, x1, bright=False):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    if bright:
        reg = reg[(reg.min(axis=1) > 150)]
    else:
        reg = reg[(reg.min(axis=1) < 205) | (reg.max(axis=1) - reg.min(axis=1) > 45)]
    modal = {}
    for px in reg:
        key = (px[0] // 16 * 16, px[1] // 16 * 16, px[2] // 16 * 16)
        modal[key] = modal.get(key, 0) + 1
    return sorted(modal.items(), key=lambda kv: -kv[1])[:4]

# def box borders — scan y105..215 for full-width ink rows
print("== def box border rows (x100..850 full-width count) ==")
for y in range(105, 215):
    n = int(ink[y, 100:850].sum())
    if n > 600:
        print(f"  y={y} n={n}")
for x in range(60, 90):
    n = int(ink[118:205, x].sum())
    if n > 60: print(f"  defbox-left x={x} n={n}")
for x in range(880, 905):
    n = int(ink[118:205, x].sum())
    if n > 60: print(f"  defbox-right x={x} n={n}")

print("\n== Remember box border rows (full-width) ==")
for y in range(222, 285):
    n = int(ink[y, 100:850].sum())
    if n > 600:
        print(f"  y={y} n={n}")
for x in range(70, 95):
    n = int(ink[235:270, x].sum())
    if n > 20: print(f"  remember-left x={x} n={n}")
for x in range(875, 900):
    n = int(ink[235:270, x].sum())
    if n > 20: print(f"  remember-right x={x} n={n}")
print("  remember bottom-border modal:", modal(275, 277, 150, 800))
print("  remember top-border modal:", modal(229, 231, 150, 800))

print("\n== starburst ==")
yellow = (R > 200) & (G > 185) & (B < 175) & (R - B > 55)
ys, xs = np.where(yellow)
print(f"  yellow bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(ys)}")
redtr = (R - G > 55) & (R - B > 55) & (R > 120)
sub = redtr[30:135, 750:945]
ys2, xs2 = np.where(sub)
if len(ys2):
    print(f"  red-outline bbox x{750+xs2.min()}..{750+xs2.max()} y{30+ys2.min()}..{30+ys2.max()} n={len(ys2)}")

print("\n== title band ==")
bands(50, 105, 60, 940, 3, "title (x60..940)")

print("\n== def box text lines ==")
bands(117, 206, 80, 885, 3, "defbox")
print("  line1 modal:", modal(120, 145, 85, 880))
print("  line3 modal:", modal(168, 195, 85, 880))

print("\n== remember box text lines ==")
bands(233, 274, 85, 878, 3, "remember")
print("  remember text modal:", modal(233, 250, 90, 700))

print("\n== legend box text lines ==")
bands(356, 432, 73, 260, 3, "legend")
print("  legend fill modal (bright):", modal(395, 420, 120, 250, bright=True))
print("  legend border modal y354:", modal(354, 356, 100, 240))

print("\n== equation panel text/bullets ==")
bands(292, 500, 293, 699, 3, "eqpanel (x293..699)")

print("\n== callout text lines ==")
bands(365, 390, 736, 894, 2, "weights-callout")
bands(422, 447, 736, 878, 2, "input-callout")
