#!/usr/bin/env python3
"""Probe round 3: callout row profiles, Values box, thin-arrow absence."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
A = np.asarray(Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB"), dtype=np.int16)

def px(x, y):
    return "%02X%02X%02X" % tuple(int(v) for v in A[y, x])

def cls(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if r > 130 and r - g > 60 and r - b > 60: return "R"
    if 120 < r < 215 and g < 140 and b > 130 and b - g > 35: return "M"
    if r > 235 and g > 235 and b > 235: return "w"
    if b >= g - 2 and g > r + 4 and b > 230: return "c"
    if r > 240 and g > 220 and b < 215: return "y"
    if r > 200 and 160 < g < 220 and 130 < b < 185: return "T"  # tan
    return "."

print("== c1 row profile (dark+mag px per row, x316..489) ==")
reg = A[138:190, 316:489]
m = ((reg.sum(axis=2) < 330) | ((reg[:, :, 0] > 120) & (reg[:, :, 0] < 215) & (reg[:, :, 1] < 140) & (reg[:, :, 2] > 130)))
for i, y in enumerate(range(138, 190)):
    n = int(m[i].sum())
    if n: print(f" y{y}: {n}")

print("== c2 row profile (x635..845) ==")
reg = A[138:190, 635:845]
m = ((reg.sum(axis=2) < 330) | ((reg[:, :, 0] > 120) & (reg[:, :, 0] < 215) & (reg[:, :, 1] < 140) & (reg[:, :, 2] > 130)))
for i, y in enumerate(range(138, 190)):
    n = int(m[i].sum())
    if n: print(f" y{y}: {n}")

print("== Values box ASCII x735..845 y180..225 ==")
print("     " + "".join(str((735 + i) // 10 % 10) for i in range(0, 110)))
for y in range(180, 226, 1):
    print(f"y{y:3d} " + "".join(cls(A[y, 735 + i]) for i in range(0, 110)))

print("== KEYs box ASCII x58..142 y184..220 ==")
print("     " + "".join(str((58 + i) // 10 % 10) for i in range(0, 84)))
for y in range(184, 221, 1):
    print(f"y{y:3d} " + "".join(cls(A[y, 58 + i]) for i in range(0, 84)))

print("== thin-arrow absence: red px in x272..500 y404..470 (child) ==")
reg = A[404:470, 272:500]
m = (reg[:, :, 0] > 130) & (reg[:, :, 0] - reg[:, :, 1] > 60) & (reg[:, :, 0] - reg[:, :, 2] > 60)
ys, xs = np.nonzero(m)
print(" count:", len(xs), ("bbox x%d..%d y%d..%d" % (272 + xs.min(), 272 + xs.max(), 404 + ys.min(), 404 + ys.max())) if len(xs) else "")

print("== query box text colors: L1 core probes ==")
for pt in [(160, 432), (170, 433), (180, 434), (190, 433)]:
    print(f" ({pt[0]},{pt[1]}) {px(*pt)}")
print(" L2 core probes:")
for pt in [(140, 447), (150, 448), (170, 448), (190, 448)]:
    print(f" ({pt[0]},{pt[1]}) {px(*pt)}")

print("== result box red noun cores ==")
for pt in [(610, 448), (620, 449), (760, 449), (740, 486), (750, 487)]:
    print(f" ({pt[0]},{pt[1]}) {px(*pt)}")

print("== K/V/Q badge circle fill cores ==")
for pt in [(155, 336), (170, 350), (740, 336), (754, 350), (251, 432), (265, 447)]:
    print(f" ({pt[0]},{pt[1]}) {px(*pt)}")

print("== 'All' word color check (x274..296 y84..96) darkest ==")
reg = A[84:97, 272:298]
i = reg.reshape(-1, 3).sum(axis=1).argmin()
print(" darkest in 'All':", "%02X%02X%02X" % tuple(reg.reshape(-1, 3)[i]))
reg = A[84:97, 306:352]
i = reg.reshape(-1, 3).sum(axis=1).argmin()
print(" darkest in 'Keys':", "%02X%02X%02X" % tuple(reg.reshape(-1, 3)[i]))

print("== title: does '{Key-Value}' really have braces? ink runs y58..76 x520..700 ==")
reg = A[56:78, 500:780]
m = reg.sum(axis=2) < 330
cols = np.nonzero(m.sum(axis=0) > 0)[0] + 500
def runs(cols, gap=5):
    out = []
    if len(cols) == 0: return out
    s = p = cols[0]
    for c in cols[1:]:
        if c - p > gap:
            out.append((s, p)); s = c
        p = c
    out.append((s, p)); return out
print(" title ink runs (x500..780):", runs(cols))
