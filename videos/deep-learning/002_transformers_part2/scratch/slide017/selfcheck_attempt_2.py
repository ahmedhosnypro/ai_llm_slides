#!/usr/bin/env python3
"""Closed-loop self-check attempt 2 (swoosh delta): render_2.png vs slide_017.jpg frame.
Checks: (1) swoosh stroke core color + head/tail extents in the render vs the frame;
(2) label ink band; (3) inheritance: render_2 vs render_1 differ ONLY in the swoosh zone."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
R2 = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide017/render_2.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.int16)
R1 = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide017/render_1.png").convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.int16)
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.int16)
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500
def fpx(sx, sy): return F[int(round(AY + SY * sy)), int(round(AX + SX * sx))]
def r2px(sx, sy): return R2[sy, sx]
def redmask(c):
    r, g, b = int(c[0]), int(c[1]), int(c[2])
    return r > 150 and g < 110 and b < 110 and (r - g) > 60

print("== 1. swoosh stroke core (darkest red along matched sample points) ==")
def darkest(sampler, pts):
    best = None
    for sx, sy in pts:
        c = sampler(sx, sy); s = int(c[0]) + int(c[1]) + int(c[2])
        if best is None or s < best[0]: best = (s, tuple(int(v) for v in c), sx, sy)
    return best
fpts = [(660,425),(680,415),(700,400),(720,385),(740,370),(760,355),(700,395),(710,390)]
print("  frame  :", darkest(fpx, fpts))
print("  render2:", darkest(r2px, fpts))

print("== 2. swoosh extent (bright-red ink bbox in slide window x540..820 y300..500) ==")
for name, fn in (("frame", fpx), ("render2", r2px)):
    pts = [(sx, sy) for sy in range(300, 500) for sx in range(540, 820) if redmask(fn(sx, sy))]
    a = np.array(pts)
    print(f"  {name}: n={len(a)} bbox x{a[:,0].min()}..{a[:,0].max()} y{a[:,1].min()}..{a[:,1].max()}")

print("== 3. head zone ink (x770..810, y325..365) ==")
for name, fn in (("frame", fpx), ("render2", r2px)):
    n = sum(1 for sy in range(325, 366) for sx in range(770, 811) if redmask(fn(sx, sy)))
    print(f"  {name}: {n} red px")

print("== 4. label ink band (blue-ish, x740..840 y330..395) ==")
import colorsys
def blue(c):
    r, g, b = c[0]/255.0, c[1]/255.0, c[2]/255.0
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return s > 0.30 and v > 0.28 and 0.55 <= h <= 0.73
for name, fn in (("frame", fpx), ("render2", r2px)):
    pts = [(sx, sy) for sy in range(330, 396) for sx in range(740, 841) if blue(fn(sx, sy))]
    a = np.array(pts)
    if len(a):
        print(f"  {name}: n={len(a)} bbox x{a[:,0].min()}..{a[:,0].max()} y{a[:,1].min()}..{a[:,1].max()} center ({a[:,0].mean():.0f},{a[:,1].mean():.0f})")
    else:
        print(f"  {name}: none")

print("== 5. inheritance: render_2 vs render_1 changed px outside swoosh zone ==")
d = np.abs(R2 - R1).sum(axis=2) > 90
zmask = np.zeros_like(d); zmask[300:500, 540:820] = True
print(f"  changed total {int(d.sum())}  inside swoosh zone {int((d & zmask).sum())}  OUTSIDE {int((d & ~zmask).sum())}")
out = d & ~zmask
for ty in range(0, 540, 30):
    for tx in range(0, 960, 40):
        n = int(out[ty:ty+30, tx:tx+40].sum())
        if n >= 40:
            print(f"    outside tile x{tx} y{ty}: {n}")
