#!/usr/bin/env python3
"""forensics8.py — final probes: eq(a) '=' zone, bullets, arrow2, arrow1 shaft, callout colors,
fills, chrome samples. Banked to qa/slide045/forensics8_out.txt."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
lum = (r + g + b) / 3

def runs(idx):
    out, s, p = [], None, None
    for i in idx:
        if s is None: s = p = i
        elif i == p + 1: p = i
        else: out.append((s, p)); s = p = i
    if s is not None: out.append((s, p))
    return out

ink_loose = lum < 195   # anything darkish
ink_mid = lum < 160

print("== eq(a) '=' zone: x488..528 y315..370, col runs (loose) ==")
prof = ink_loose[315:370, 488:528].sum(axis=0)
print(" cols:", runs(np.where(prof > 0)[0] + 488))
for yy in range(318, 366, 2):
    rr = np.where(ink_loose[yy, 488:528])[0] + 488
    if len(rr): print(f"  y={yy}: {runs(rr)}")

print("\n== eq(a) row profile (loose, x470..696) ==")
rp = ink_loose[296:372, 470:696].sum(axis=1)
print(" rows:", runs(np.where(rp > 2)[0] + 296))

print("\n== bullets: per-row col runs x292..352 (loose) ==")
for (ya, yb, lb) in [(296, 312, "b1"), (374, 392, "b2"), (422, 440, "b3")]:
    print(f" {lb}:")
    for yy in range(ya, yb):
        rr = np.where(ink_loose[yy, 292:352])[0] + 292
        if len(rr): print(f"  y={yy}: {runs(rr)}")

print("\n== arrow2 broad search x430..740 y408..502 (red_very, per-row) ==")
red_very = (r - g > 20) & (r - b > 12) & (r > 150) & (g < 220)
m = red_very.copy(); m[:, 695:706] = False  # hide border cols
found = False
for yy in range(408, 502):
    rr = np.where(m[yy, 430:740])[0] + 430
    if len(rr):
        found = True
        print(f"  y={yy}: {runs(rr)} n={len(rr)}")
if not found: print("  NOTHING found")

print("\n== arrow1 shaft detail x700..748 y332..390 (red_very per-row) ==")
m2 = red_very.copy(); m2[:, :703] = False
for yy in range(332, 390):
    rr = np.where(m2[yy, 700:748])[0] + 700
    if len(rr): print(f"  y={yy}: {runs(rr)} n={len(rr)}")

print("\n== callout text color zones ==")
blue_t = (b > 120) & (b - r > 60) & (b - g > 40)
black_t = (lum < 120) & (b - r < 60)
for (ya, yb, xa, xb, lb) in [(367, 390, 738, 893, "weights"), (424, 448, 737, 877, "input")]:
    for (zx0, zx1, zl) in [(xa, xa + 60, "lead"), (xa + 60, xb, "tail")]:
        nb = blue_t[ya:yb, zx0:zx1].sum(); nk = black_t[ya:yb, zx0:zx1].sum()
        print(f" {lb} {zl} x{zx0}..{zx1}: blue={nb} black={nk}")

print("\n== fills ==")
for (ya, yb, xa, xb, lb) in [(196, 205, 300, 800, "defbox-fill"), (300, 480, 310, 460, "eqpanel-fill"),
                              (262, 272, 300, 800, "remember-fill"), (60, 110, 100, 400, "panel-gray"),
                              (95, 110, 830, 850, "starburst-fill-b")]:
    samp = im[ya:yb, xa:xb].reshape(-1, 3)
    print(f" {lb}: median {tuple(np.median(samp, axis=0).astype(int))}")

print("\n== chrome (original) ==")
samp = im[100:110, 20:40].reshape(-1, 3)
print(f" outside-panel (x20..40): median {tuple(np.median(samp, axis=0).astype(int))}")
red_row = np.where(((r > 120) & (g < 110) & (b < 110))[42:48, 100:800].sum(axis=1) > 400)[0] + 42
print(f" chrome top red rows: {runs(red_row)}")
col = np.where(((r > 120) & (g < 110) & (b < 110))[:, 56:60].sum(axis=0) > 300)[0] + 56
print(f" chrome left red cols: {runs(col)}")

print("\n== eq(b), eq(c) row bands (loose) ==")
for (ya, yb, xa, xb, lb) in [(388, 418, 515, 645, "eq(b)"), (420, 495, 435, 685, "eq(c)")]:
    rp = ink_loose[ya:yb, xa:xb].sum(axis=1)
    print(f" {lb} rows:", runs(np.where(rp > 2)[0] + ya))
    cp = ink_loose[ya:yb, xa:xb].sum(axis=0)
    print(f" {lb} cols:", runs(np.where(cp > 0)[0] + xa))

print("\n== title serif feet / baseline ==")
anyt = ink_loose[66:104, 190:780]
for yy in range(86, 100):
    rr = np.where(anyt[yy - 66])[0] + 190
    print(f" y={yy}: n={len(rr)} {runs(rr)[:8]}{'...' if len(rr)>30 else ''}")
