#!/usr/bin/env python3
"""High-res ASCII crops of slide_026 regions (2px cells)."""
from PIL import Image
import numpy as np
import sys

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)

PAL = [
    ("W", (255, 255, 255), 26), ("G", (231, 233, 230), 12), ("g", (196, 219, 161), 22),
    ("B", (18, 189, 232), 60), ("L", (191, 191, 191), 22), ("O", (247, 150, 70), 48),
    ("P", (250, 219, 185), 16), ("T", (96, 190, 135), 50), ("R", (192, 0, 0), 75),
    ("K", (0, 0, 0), 60), ("k", (110, 110, 108), 40), ("Y", (253, 253, 150), 40),
    ("D", (166, 208, 183), 30),
]
chars = np.full(a.shape[:2], ".", dtype="<U1")
dists = np.full(a.shape[:2], 10**9)
for ch, c, tol in PAL:
    d = np.abs(a - np.array(c)).sum(axis=2)
    m = d < tol * 3
    upd = m & (d < dists)
    chars[upd] = ch
    dists[upd] = np.where(d < dists, d, dists)[upd]

def crop(x0, x1, y0, y1, step=2, label=""):
    print(f"== {label} x{x0}..{x1} y{y0}..{y1} step{step} ==")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1, step):
        row = "".join(chars[y, x] for x in range(x0, x1, step))
        print(f"{y:4d} {row}")

which = sys.argv[1] if len(sys.argv) > 1 else "all"
if which in ("all", "blue"):
    crop(226, 396, 232, 396, 2, "BLUEBOX")
if which in ("all", "conttop"):
    crop(390, 680, 185, 300, 2, "CONT_TOP")
if which in ("all", "contbot"):
    crop(390, 680, 340, 475, 2, "CONT_BOT")
if which in ("all", "right"):
    crop(672, 866, 183, 470, 2, "RIGHT_RECT")
