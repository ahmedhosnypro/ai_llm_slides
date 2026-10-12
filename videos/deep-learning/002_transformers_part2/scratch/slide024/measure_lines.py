#!/usr/bin/env python3
"""Measure rules-box text lines (x-extents, colors, red ink, underlines) and
compare subtitle metrics frame23 vs frame24."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
img24 = np.asarray(Image.open(f"{V}/unique_slides/slide_024.jpg").convert("RGB")).astype(int)
img23 = np.asarray(Image.open(f"{V}/unique_slides/slide_023.jpg").convert("RGB")).astype(int)

sx = (899 - 58) / (919.0 - 42.0); a = 58 - sx * 42.0
sy = (516 - 43) / (540.0 - 45.0); b = 43 - sy * 45.0
def S(fx, fy): return ((fx - a) / sx, (fy - b) / sy)

def ink_runs(img, y0, y1, x0=40, x1=920, min_gap=3):
    """per-band ink columns; blue and red separately"""
    reg = img[y0:y1, x0:x1]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    blue = (bl > 110) & (bl > r + 40)
    red = (r > 120) & (r > bl + 50) & (g < r - 40)
    return blue, red, reg

# ---- rules box lines: frame bands ----
bands = [(365, 382, "L1"), (388, 404, "L2"), (410, 427, "L3"),
         (432, 448, "L4"), (454, 470, "L5"), (476, 492, "L6")]
for y0, y1, tag in bands:
    blue, red, reg = ink_runs(img24, y0, y1, 60, 920)
    if blue.any():
        bx = np.where(blue.any(axis=0))[0]
        x0f, x1f = bx[0] + 60, bx[-1] + 60
        s0, _ = S(x0f, 0); s1, _ = S(x1f, 0)
        print(f"{tag}: blue ink frame x {x0f}..{x1f} -> slide x {s0:.1f}..{s1:.1f} (w {s1-s0:.1f})")
    if red.any():
        rx = np.where(red.any(axis=0))[0]
        print(f"   RED ink cols frame {rx[0]+60}..{rx[-1]+60} count {red.sum()}")

# red ink anywhere in the rules box?
reg = img24[348:503, 74:887]
r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
red = (r > 120) & (r > bl + 50) & (g < r - 40)
print("red px in rules box:", int(red.sum()))
if red.any():
    ys_, xs_ = np.where(red)
    print("red bbox frame x", xs_.min()+74, "..", xs_.max()+74, " y", ys_.min()+348, "..", ys_.max()+348)

# underline detection: horizontal blue runs longer than 25px in each band (underlines are thin)
print("\nunderline candidates (blue runs >= 25px in-band rows):")
for y0, y1, tag in bands:
    reg = img24[y0:y1+6, 60:920]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    blue = (bl > 100) & (bl > r + 30)
    for yy in range(reg.shape[0]):
        row = blue[yy]
        # find runs
        d = np.diff(np.concatenate(([0], row.astype(int), [0])))
        starts = np.where(d == 1)[0]; ends = np.where(d == -1)[0]
        for s_, e_ in zip(starts, ends):
            if e_ - s_ >= 25:
                print(f"  {tag} row {y0+yy}: run x {s_+60}..{e_+60-1} (len {e_-s_})")

# ---- subtitle comparison 23 vs 24 ----
print("\n--- subtitle ink comparison ---")
for img, n in ((img23, 23), (img24, 24)):
    reg = img[75:115, 250:800]
    r, g, bl = reg[..., 0], reg[..., 1], reg[..., 2]
    blue = (bl > 110) & (bl > r + 40)
    yel = (r > 225) & (g > 225) & (bl < 200)
    if blue.any():
        bx = np.where(blue.any(axis=0))[0]; by = np.where(blue.any(axis=1))[0]
        s0, sy0 = S(bx[0] + 250, by[0] + 75); s1, sy1 = S(bx[-1] + 250, by[-1] + 75)
        print(f"frame{n} subtitle ink: frame x {bx[0]+250}..{bx[-1]+250} y {by[0]+75}..{by[-1]+75} "
              f"-> slide x {s0:.1f}..{s1:.1f} (w {s1-s0:.1f}) y {sy0:.1f}..{sy1:.1f} (h {sy1-sy0:.1f})")
    if yel.any():
        yx = np.where(yel.any(axis=0))[0]; yy = np.where(yel.any(axis=1))[0]
        s0, sy0 = S(yx[0] + 250, yy[0] + 75); s1, sy1 = S(yx[-1] + 250, yy[-1] + 75)
        print(f"frame{n} yellow bbox: frame x {yx[0]+250}..{yx[-1]+250} y {yy[0]+75}..{yy[-1]+75} "
              f"-> slide x {s0:.1f}..{s1:.1f} y {sy0:.1f}..{sy1:.1f}")

# frame23's subtitle string is known: "(Normalize Seq. Length to \u201c1\u201d)" @22.5pt bold.
# frame24 string "(Rules Controlling Good Positional Encoder)" — solve em from width:
# Arial bold advance for that string (units/1000): compute below.
from fontTools.ttLib import TTFont
import glob
cands = glob.glob("/usr/share/fonts/**/Arial*", recursive=True) + glob.glob("/usr/share/fonts/**/LiberationSans*", recursive=True)
print("\nfont candidates:", cands[:4])
