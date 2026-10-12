#!/usr/bin/env python3
"""Slide 038 forensics pass 8: '=' hunt (fixed mask), X zoom, 7s, pencil, arrows, line2/3 runs, circle ring."""
from PIL import Image
import numpy as np

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_038.jpg').convert('RGB')
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

print("=== light-blue hunt: b>190, b-r>60, g 130..210 in x500..810 y280..460 ===")
lb = (b > 190) & ((b - r) > 60) & (g > 130) & (g < 215)
ys, xs = np.where(lb[280:460, 500:810])
if len(ys):
    print(f"bbox x {xs.min()+500}..{xs.max()+500} y {ys.min()+280}..{ys.max()+280} n={len(ys)}")
    # cluster by x
    for x0, x1 in [(555, 610)]:
        sel = (xs + 500 >= x0) & (xs + 500 <= x1)
        if sel.sum():
            print(f"  in x{x0}..{x1}: n={sel.sum()} y {(ys[sel]+280).min()}..{(ys[sel]+280).max()} x {(xs[sel]+500).min()}..{(xs[sel]+500).max()}")

print()
print("=== any ink at all x552..612 y300..430 (not purple-slab edge) ===")
ink = ((r < 215) | (g < 215) | (b < 215)) & ~((abs(r-232)<14) & (abs(g-232)<14))
for y in range(300, 431, 2):
    xs2 = np.nonzero(ink[y, 552:613])[0] + 552
    if len(xs2) > 2:
        print(f"y={y}: n={len(xs2)} x {xs2.min()}..{xs2.max()} mid={a[y, xs2[len(xs2)//2]]}")

print()
print("=== X zoom x348..380 y330..358 (1px) ===")
def cls(p):
    rr, gg, bb = p
    if rr > 235 and gg > 235 and bb > 235: return '.'
    if rr < 110 and gg < 110 and bb < 110: return '#'
    if rr < 180 and gg < 160: return 'd'
    return ' '
for y in range(330, 359):
    print(f"{y:3d} " + ''.join(cls(a[y, x]) for x in range(348, 381)))

print()
print("=== above stack: x395..560 y295..340 (2px) ===")
for y in range(295, 341, 2):
    row = ''
    for x in range(395, 561, 2):
        row += cls(a[y, x])
    print(f"{y:3d} {row}")
