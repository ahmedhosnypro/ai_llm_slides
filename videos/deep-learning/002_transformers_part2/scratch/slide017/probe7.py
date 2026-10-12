#!/usr/bin/env python3
"""Probe 7: legend + wochips windows, frame vs parent, slide coords."""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.int16)
P = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png"
).convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.int16)
AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500

def sample(img, sx, sy):
    if img is F:
        fx, fy = AX + SX * sx, AY + SY * sy
    else:
        fx, fy = float(sx), float(sy)
    return img[int(round(fy)), int(round(fx))]

def runs(img, sy, sx0, sx1, tol=30):
    out, cur = [], None
    for sx in range(sx0, sx1):
        c = sample(img, sx, sy)
        if cur and abs(int(c[0])-cur[1][0]) + abs(int(c[1])-cur[1][1]) + abs(int(c[2])-cur[1][2]) <= tol:
            cur[2] = sx
        else:
            if cur and cur[2] - cur[0] >= 1:
                out.append((cur[0], cur[2], "%02X%02X%02X" % tuple(int(v) for v in cur[1])))
            cur = [sx, tuple(int(v) for v in c), sx]
    if cur:
        out.append((cur[0], cur[2], "%02X%02X%02X" % tuple(int(v) for v in cur[1])))
    return out

def show(tag, img, sy, x0, x1):
    print(f"  {tag:6s} y{sy}: " + " | ".join(f"{a}-{b}:{h}" for a, b, h in runs(img, sy, x0, x1)))

print("== LEGEND window x728..915 ==")
for sy in (465, 470, 474, 478, 483, 490, 498, 504, 510, 518, 524, 529):
    show("frame", F, sy, 728, 915)
    show("parent", P, sy, 728, 915)
    print()

print("== LEGEND green dashed border scan (columns x738/905, rows) ==")
for img, tag in ((F, "frame"), (P, "parent")):
    for sx in (738, 905):
        ys = []
        for sy in range(455, 545):
            c = sample(img, sx, sy)
            if c[1] > 110 and int(c[1]) - int(c[0]) > 20 and int(c[1]) - int(c[2]) > 10:
                ys.append(sy)
        print(f"  {tag} x{sx}: green rows {ys[:6]}..{ys[-6:] if len(ys)>6 else ''} n={len(ys)}")

print()
print("== WOCHIPS window: rear-layer W columns (from an_zS5: h=5 col slide x~748..770 y~460..520; h=4 col x~710..732 y~469..529) ==")
for sy in (455, 465, 472, 480, 488, 496, 504, 512, 520):
    show("frame", F, sy, 700, 800)
    show("parent", P, sy, 700, 800)
    print()
