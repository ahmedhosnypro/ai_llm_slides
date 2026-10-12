#!/usr/bin/env python3
"""m09_bounds.py — precise bboxes of known elements + mode colors of fills."""
import numpy as np
from PIL import Image
from collections import Counter

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)

def mode_color(x0, x1, y0, y1, exclude_dark=True):
    px = im[y0:y1, x0:x1].reshape(-1, 3)
    q = [tuple(v // 8 * 8) for v in px]
    c = Counter(q)
    for col, n in c.most_common(6):
        if exclude_dark and sum(col) < 240:
            continue
        return col, n
    return c.most_common(1)[0]

def ink_bbox(x0, x1, y0, y1, bg, tol=28):
    """bbox of pixels differing from bg more than tol (max-channel)."""
    reg = im[y0:y1, x0:x1]
    d = np.abs(reg - np.array(bg)).max(axis=2)
    ys, xs = np.where(d > tol)
    if not len(xs):
        return None
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max(), int((d > tol).sum()))

def rep(name, box, bg=None):
    if box is None:
        print(f"{name}: EMPTY")
        return
    x0, x1, y0, y1, n = box
    print(f"{name:28s} frame x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d} (w {x1-x0+1:3d} h {y1-y0+1:3d}) ink {n}")

PEACH = (252, 233, 217); GREEN = (17, 255, 116); ORANGE = (243, 168, 92)
CCFF = (207, 255, 226); GRAYBG = (233, 233, 231)

print("== mode colors ==")
for name, (x0, x1, y0, y1) in [
    ("peach", (160, 200, 140, 180)), ("green overlay", (330, 420, 200, 300)),
    ("orange", (590, 650, 220, 260)), ("ccffcc", (850, 875, 210, 260)),
    ("enc container fill", (250, 268, 262, 265)), ("enc blue box", (230, 260, 268, 274)),
    ("enc gray box", (240, 268, 286, 296)), ("enc pink box", (250, 270, 312, 322)),
    ("enc blue box2", (230, 260, 330, 336)), ("yellow enc", (255, 280, 246, 254)),
    ("dec yellow bar", (727, 733, 260, 300)), ("dec gray box", (770, 820, 205, 235)),
    ("dec blue box2", (760, 820, 256, 262)), ("dec brown mid", (755, 830, 275, 295)),
    ("dec blue box3", (740, 790, 320, 328)), ("dec purple", (740, 800, 340, 385)),
    ("dec brown emb", (745, 820, 410, 450)), ("Nx circle", (160, 175, 320, 340)),
    ("dec teal softmax", (750, 795, 150, 158)), ("title red", (222, 226, 66, 76)),
]:
    c, n = mode_color(x0, x1, y0, y1)
    print(f"{name:20s} mode {c} n={n}  #{c[0]:02X}{c[1]:02X}{c[2]:02X}")

print("\n== element ink bboxes (vs local bg) ==")
jobs = [
    ("Encoder label", (140, 240, 104, 132), PEACH),
    ("enc yellow box+text", (190, 300, 236, 262), PEACH),
    ("enc container zone", (180, 290, 250, 345), PEACH),
    ("Nx circle zone", (140, 200, 290, 352), PEACH),
    ("PE icon+label zone", (180, 300, 352, 400), PEACH),
    ("Output Emb zone", (190, 300, 398, 465), PEACH),
    ("left text lines", (150, 205, 400, 425), PEACH),
    ("Inputs arrow zone", (200, 290, 460, 500), PEACH),
    ("Decoder label zone", (780, 895, 104, 132), CCFF),
    ("dec Output row", (720, 890, 104, 140), ORANGE),
    ("dec softmax/linear", (720, 890, 140, 195), CCFF),
    ("callout1", (566, 712, 140, 168), ORANGE),
    ("callout2", (566, 712, 163, 191), ORANGE),
    ("callout3", (566, 712, 280, 334), ORANGE),
    ("callout4", (566, 712, 336, 365), ORANGE),
    ("dec emb zone", (720, 850, 395, 470), CCFF),
    ("dec bottom yellow", (720, 850, 468, 505), CCFF),
]
for name, (x0, x1, y0, y1), bg in jobs:
    rep(name, ink_bbox(x0, x1, y0, y1, bg), bg)
