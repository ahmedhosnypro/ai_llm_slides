#!/usr/bin/env python3
"""m10_clean.py — clean fill colors (text-free stripes), overlay emptiness, corner radius."""
import numpy as np
from PIL import Image

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)

def core(x0, x1, y0, y1):
    """median of the middle 50% brightness pixels (drop text/ink extremes)."""
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    lum = px.sum(axis=1)
    lo, hi = np.percentile(lum, 30), np.percentile(lum, 70)
    sel = px[(lum >= lo) & (lum <= hi)]
    m = np.median(sel, axis=0).astype(int)
    return tuple(m), f"#{m[0]:02X}{m[1]:02X}{m[2]:02X}"

samples = [
    ("peach", 150, 290, 150, 230),
    ("green overlay", 320, 440, 150, 450),
    ("orange", 580, 720, 200, 275),
    ("ccffcc right", 840, 875, 210, 460),
    ("container fill enc", 218, 268, 258, 262),
    ("AddNorm1 blue", 222, 266, 269, 274),
    ("FF gray", 240, 266, 288, 298),
    ("MHA pink", 252, 268, 312, 318),
    ("AddNorm2 blue", 222, 266, 330, 335),
    ("yellow box enc", 250, 286, 244, 256),
    ("yellow bar dec", 727, 733, 255, 305),
    ("dec gray box", 790, 826, 210, 232),
    ("dec blue box2", 760, 820, 255, 262),
    ("dec brown mid", 752, 830, 270, 294),
    ("dec blue box3", 735, 795, 319, 327),
    ("dec purple", 735, 800, 345, 385),
    ("dec brown emb", 740, 824, 405, 425),
    ("Nx circle", 162, 180, 322, 338),
    ("softmax teal", 748, 798, 151, 157),
    ("linear teal", 748, 798, 175, 181),
    ("yellow Output", 762, 792, 112, 121),
    ("dec yellow bot", 752, 788, 476, 486),
]
for name, x0, x1, y0, y1 in samples:
    c, hx = core(x0, x1, y0, y1)
    print(f"{name:18s} {hx}  {c}")

# emptiness of green overlay (std) and ccffcc right of stack
g = im[150:450, 320:440]; print("green overlay std:", g.std(axis=(0, 1)).round(2))
c2 = im[210:460, 840:875]; print("ccffcc right std:", c2.std(axis=(0, 1)).round(2))

# panel corner radius: encoder top-left corner — find for each row y=100..120 the leftmost non-bg pixel
print("\nencoder panel top-left corner profile (x of leftmost non-gray px):")
for y in range(100, 122, 2):
    row = im[y, 125:170]
    d = np.abs(row - np.array([233, 233, 231])).max(axis=1)
    xs = np.where(d > 25)[0]
    print(" y", y, "x", 125 + xs.min() if len(xs) else None)

# panel exact edges: green border runs
print("\npanel border scan: columns where greenish border (x 125..160, y 200..300):")
sub = im[200:300, 125:165]
greenish = (np.abs(sub - np.array([115, 204, 101])).max(axis=2) < 60)
cols = greenish.sum(axis=0)
print(" cols:", {125 + i: int(c) for i, c in enumerate(cols) if c > 40})
sub = im[100:140, 200:470]
greenish = (np.abs(sub - np.array([115, 204, 101])).max(axis=2) < 60)
rows = greenish.sum(axis=1)
print(" top border rows:", {100 + i: int(c) for i, c in enumerate(rows) if c > 100})
