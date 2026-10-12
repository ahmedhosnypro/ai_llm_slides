#!/usr/bin/env python3
# m8_scans.py — color-class ASCII of the right panel (render vs warped frame) +
# native frame scanlines through the two highlight regions.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
warped = np.asarray(Image.open(S + "/frame_warped_contentfit.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")

CL = [("W", "FFFFFF"), ("P", "FDEDDD"), ("M", "CEFFE1"), ("Y", "F5E6A8"),
      ("B", "9DC3E6"), ("L", "C5C0E8"), ("S", "C9E7C0"), ("K", "F2C1CE")]
def classify(a):
    H, W = a.shape[:2]
    out = np.empty((H, W), dtype="<U1")
    d = np.stack([np.abs(a - np.array([int(h[i:i+2], 16) for i in (0, 2, 4)])).sum(axis=2) for _, h in CL], axis=0)
    best = d.argmin(axis=0)
    bestd = d.min(axis=0)
    lab = np.array([c for c, _ in CL])[best]
    lab[bestd > 150] = "?"
    ink = a.mean(axis=2) < 110
    lab[ink] = "#"
    orange = (a[..., 0] > 195) & (a[..., 2] < 185) & ((a[..., 0] - a[..., 2]) > 50) & (a[..., 1] > 110) & (a[..., 1] < 225) & ((a[..., 1] - a[..., 2]) > 15)
    lab[orange] = "O"
    return lab

lr = classify(render); lw = classify(warped)
print("render right panel (x1190..1910 y230..1060):")
for cy in range(40):
    row = ""
    for cx in range(60):
        cell = lr[230 + (830 * cy) // 40: 230 + (830 * (cy + 1)) // 40,
                  1190 + (720 * cx) // 60: 1190 + (720 * (cx + 1)) // 60]
        vals, cnt = np.unique(cell, return_counts=True)
        row += vals[cnt.argmax()]
    print(row)
print("\nwarped frame right panel:")
for cy in range(40):
    row = ""
    for cx in range(60):
        cell = lw[230 + (830 * cy) // 40: 230 + (830 * (cy + 1)) // 40,
                  1190 + (720 * cx) // 60: 1190 + (720 * (cx + 1)) // 60]
        vals, cnt = np.unique(cell, return_counts=True)
        row += vals[cnt.argmax()]
    print(row)

# native frame scanlines: horizontal at several y through each highlight zone
def scanrow(y, x0, x1, step=4):
    out = []
    for x in range(x0, x1, step):
        c = frame[y, x]
        out.append(f"{x}:{int(c[0])},{int(c[1])},{int(c[2])}")
    return " ".join(out)

print("\nframe scan rows through lower-left highlight (frame y 340..390):")
for y in (342, 352, 362, 372, 382, 388):
    print(f"y={y}: {scanrow(y, 565, 725)}")
print("\nframe scan rows through upper-right highlight (frame y 265..312):")
for y in (266, 276, 286, 296, 306, 311):
    print(f"y={y}: {scanrow(y, 735, 880)}")
print("\nframe scan cols (vertical extent) x 590,620,660,700:")
for x in (590, 620, 660, 700):
    col = []
    for y in range(330, 400, 3):
        c = frame[y, x]
        col.append(f"{y}:{int(c[0])},{int(c[1])},{int(c[2])}")
    print(f"x={x}: " + " ".join(col))
for x in (750, 790, 830, 865):
    col = []
    for y in range(255, 325, 3):
        c = frame[y, x]
        col.append(f"{y}:{int(c[0])},{int(c[1])},{int(c[2])}")
    print(f"x={x}: " + " ".join(col))
