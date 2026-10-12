#!/usr/bin/env python3
"""pm5_bar_arrows.py — slide 034 purple banner + the two red down arrows.

Bar: purple-mask bbox, fill core; text words segmented by column gaps, per-word
bbox/cap-height/center (yellow vs white runs). Arrows: per-row width profile =>
shaft cx/width, head width/height, y-extent.

Output: pm5_bar_arrows_output.txt
"""
import numpy as np
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_034.jpg"
OUT = os.path.join(HERE, "pm5_bar_arrows_output.txt")

AX, SX, SY = 17.891, 0.962062, 0.955556
def FX(fx): return (fx - AX) / SX
def FY(fy): return fy / SY

img = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
s = r + g + b
lines = []
def say(v=""):
    lines.append(v)
    print(v)

say("== PURPLE BANNER ==")
purple = (r > 90) & (r < 210) & (g < 75) & (b > 95) & (b < 215)
win = purple[205:262, 150:905]
ys, xs = np.where(win)
x0, x1, y0, y1 = xs.min() + 150, xs.max() + 150, ys.min() + 205, ys.max() + 205
say(f"  purple bbox x[{x0},{x1}] y[{y0},{y1}]  w={x1-x0+1} h={y1-y0+1}")
say(f"  slide: x {FX(x0):.1f}..{FX(x1):.1f} (w {(FX(x1)-FX(x0)):.1f}pt)  y {FY(y0):.1f}..{FY(y1):.1f} (h {(FY(y1)-FY(y0)):.1f}pt)")
# row/col fill fraction (is it solid?)
rowfill = win.sum(axis=1) / (x1 - x0 + 1)
say(f"  row fill fraction min..max: {rowfill.min():.2f}..{rowfill.max():.2f} (solid ~1.0 in body rows)")
fill_px = img[228:242, 795:855].reshape(-1, 3)
say(f"  fill mean (quiet x795..855 y228..242): #%02X%02X%02X" % tuple(fill_px.mean(axis=0).astype(int)))

# text words: inside bar, non-purple px
inner = img[y0 + 4:y1 - 3, x0 + 4:x1 - 3]
ir, ig, ib = inner[..., 0], inner[..., 1], inner[..., 2]
itext = ((ir > 200) & (ig > 185) & (ib < 185)) | ((ir > 205) & (ig > 205) & (ib > 205))
icol = itext.sum(axis=0)
cols = np.where(icol > 0)[0]
words = []
if len(cols):
    st = cols[0]
    prev = cols[0]
    for c in cols[1:]:
        if c - prev > 6:  # word gap
            words.append((st, prev))
            st = c
        prev = c
    words.append((st, prev))
say(f"  word clusters (col gaps>6): {len(words)}")
names = ["Embedding", "Layer", "to", "Learn", "Position", "Vectors"]
for i, (a, b_) in enumerate(words):
    sub = itext[:, a:b_ + 1]
    ys2 = np.where(sub.any(axis=1))[0]
    name = names[i] if i < len(names) else f"w{i}"
    # cap height: rows from top ink to the row where 90% of ink has appeared
    rowc = sub.sum(axis=1)
    cap_rows = np.where(rowc > 0)[0]
    h = ys2.max() - ys2.min() + 1
    say(f"  {name:20s} x[{a+x0+4},{b_+x0+4}] w={b_-a+1} y[{ys2.min()+y0+4},{ys2.max()+y0+4}] h={h} inkC={(a+b_)/2+x0+4:.1f} -> slide cx {FX((a+b_)/2+x0+4):.1f}")
say("  (per-word cap-height: yellow words show taller glyphs — see crop z_bar_text)")

# split yellow vs white per cluster
for i, (a, b_) in enumerate(words):
    sub_r = ir[:, a:b_ + 1]; sub_g = ig[:, a:b_ + 1]; sub_b = ib[:, a:b_ + 1]
    ym = (sub_r > 200) & (ig > 185) & (sub_b < 185)
    wm = (sub_r > 205) & (sub_g > 205) & (sub_b > 205)
    tot = ym.sum() + wm.sum()
    if tot:
        say(f"  {names[i] if i<len(names) else i}: yellow px {int(ym.sum())} vs white px {int(wm.sum())} -> class {'YELLOW' if ym.sum()>wm.sum() else 'WHITE'}")

say("\n== RED DOWN ARROWS ==")
red = (r - np.maximum(g, b)) > 55
for name, yA, yB in [("arrow1", 172, 218), ("arrow2", 248, 294)]:
    win = red[yA:yB, 495:560]
    ys, xs = np.where(win)
    if not len(xs):
        say(f"  {name}: no red px")
        continue
    x0, x1, y0, y1 = xs.min() + 495, xs.max() + 495, ys.min() + yA, ys.max() + yA
    say(f"  {name}: red bbox x[{x0},{x1}] y[{y0},{y1}] npx={len(xs)}")
    # per-row width profile
    prof = []
    for yy in range(y0, y1 + 1):
        row = np.where(red[yy, 495:560])[0]
        if len(row):
            prof.append((yy, row.min() + 495, row.max() + 495, len(row)))
    for yy, a, b_, n in prof:
        say(f"    row {yy}: x[{a},{b_}] w={b_-a+1} n={n}")
    # summary
    widths = [p[3] for p in prof]
    shaft_rows = [p for p in prof if p[3] <= 10]
    head_rows = [p for p in prof if p[3] > 10]
    if shaft_rows and head_rows:
        scx = np.mean([(p[1] + p[2]) / 2 for p in shaft_rows])
        say(f"  {name}: shaft rows {shaft_rows[0][0]}..{shaft_rows[-1][0]} (n={len(shaft_rows)}) mean w={np.mean(widths[:len(shaft_rows)]):.1f} cx={scx:.1f}; head rows {head_rows[0][0]}..{head_rows[-1][0]} max w={max(p[3] for p in head_rows)}")
        say(f"  {name}: cx->slide {FX(scx):.1f}; y {FY(y0):.1f}..{FY(y1):.1f}")
    core = img[178:206, 520:532]
    m = red[178:206, 520:532]
    if m.sum():
        say(f"  {name}: shaft core #%02X%02X%02X" % tuple(core[m].mean(axis=0).astype(int)))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print(f"\nwrote {OUT}")
