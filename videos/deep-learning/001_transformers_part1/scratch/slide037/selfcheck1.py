#!/usr/bin/env python3
"""Self-check battery for slide 037 attempt 1: coarse map + containment + equations."""
import numpy as np
from PIL import Image

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide037"
ren = Image.open(f"{SCR}/render-1.png").convert("RGB")
a = np.asarray(ren).astype(int)
H, W, _ = a.shape
print(f"render size {W}x{H}")
s = W / 960.0  # frame-px -> render-px scale

PAL = {
    ".": (247, 226, 205), "t": (219, 203, 188), "T": (168, 133, 124),
    "Y": (250, 243, 111), "y": (252, 254, 221), "v": (247, 223, 249),
    "s": (235, 253, 253), "g": (231, 254, 233), "G": (146, 208, 80),
    "k": (0, 176, 80), "K": (255, 255, 0), "M": (255, 102, 204),
    "R": (255, 0, 0), "r": (139, 0, 10), "B": (0, 0, 204), "b": (60, 58, 179),
    "x": (0, 0, 0), "d": (120, 100, 90), "W": (255, 255, 255), "P": (231, 233, 230),
}
step_r = int(round(10 * s))
print("coarse map (each char = ~10 frame px):")
print("   " + "".join(str((i // 10) % 10) for i in range(0, 960, 10)))
for fy in range(0, 540, 10):
    line = []
    for fx in range(0, 960, 10):
        y0, y1 = int(fy * s), int((fy + 10) * s)
        x0, x1 = int(fx * s), int((fx + 10) * s)
        block = a[y0:y1, x0:x1].reshape(-1, 3)
        med = np.median(block, axis=0)
        best = min(PAL.items(), key=lambda kv: np.abs(med - np.array(kv[1])).max())
        line.append(best[0])
    print(f"{fy:3d}" + "".join(line))
