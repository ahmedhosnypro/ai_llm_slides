#!/usr/bin/env python3
"""Forensics 4: full-frame classified ASCII map + per-cell fill tables."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_005.jpg").convert("RGB")).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

PAL = {
    "W": (255, 255, 255),   # white
    "G": (233, 233, 231),   # panel gray E9E9E7
    "R": (192, 0, 0),       # C00000 red ink
    "Y": (255, 255, 204),   # FFFFCC pale yellow cell
    "P": (255, 204, 153),   # FFCC99 peach
    "C": (153, 255, 255),   # 99FFFF cyan
    "K": (255, 204, 255),   # FFCCFF pink
    "N": (204, 255, 204),   # CCFFCC pale green
    "B": (191, 191, 191),   # BFBFBF bar gray
    "L": (0, 0, 204),       # 0000CC blue text
    "E": (0, 160, 0),       # 00A000 green
    "S": (255, 153, 153),   # FF9999 salmon kernel
    "F": (255, 255, 0),     # FFFF00 banner yellow
    "D": (60, 60, 60),      # dark (text ink)
}
names = list(PAL.keys())
targets = np.array([PAL[k] for k in names])
flat = im.reshape(-1, 3)
d2 = ((flat[:, None, :] - targets[None, :, :]) ** 2).sum(axis=2)
best = d2.argmin(axis=1)
mind = d2.min(axis=1)
cls = np.array([names[i] for i in best]).reshape(H, W)
cls = cls.reshape(H, W)
cls[mind.reshape(H, W) > 5000] = "?"  # too far from any palette color

# ---- ASCII map: 96 cols x 54 rows (10x10 px blocks) ----
print("ASCII map (10x10px blocks, dominant class; . = G, ? = mixed):")
ORDER = "RYPCKNBLESFDW"
print("    " + "".join(str((i * 10) // 100 % 10) for i in range(96)))
for by in range(54):
    row = []
    for bx in range(96):
        blk = cls[by * 10:(by + 1) * 10, bx * 10:(bx + 1) * 10].ravel()
        cnt = {}
        for c in blk:
            cnt[c] = cnt.get(c, 0) + 1
        # priority: ignore G/W if any strong ink present
        dom = max(cnt.items(), key=lambda kv: kv[1])
        if dom[0] in ("G", "W") and (cnt.get("R", 0) + cnt.get("L", 0) + cnt.get("D", 0)) >= 4:
            best2 = max(((k, v) for k, v in cnt.items() if k in ("R", "L", "D", "E")), key=lambda kv: kv[1])
            row.append(best2[0])
        elif dom[0] == "G":
            row.append(".")
        else:
            row.append(dom[0])
    print(f"{by*10:3d} " + "".join(row))
