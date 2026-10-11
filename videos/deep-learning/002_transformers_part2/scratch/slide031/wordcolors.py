#!/usr/bin/env python3
"""Per-word ink color of each derivation row via tesseract TSV + PIL sampling."""
import subprocess, os
import numpy as np
from PIL import Image

T = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide031"
img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_031.jpg").convert("RGB")
a = np.asarray(img).astype(int)

# rows: (y0, y1) printed bands (padded)
rows = [("R1", 262, 292), ("R2", 296, 322), ("R3", 335, 360), ("R4", 358, 381),
        ("R5", 394, 419), ("R6", 428, 452), ("R7", 466, 506)]
X0, X1 = 70, 800
for name, y0, y1 in rows:
    crop = img.crop((X0, y0, X1, y1))
    S = 3
    big = crop.resize(((X1 - X0) * S, (y1 - y0) * S), Image.LANCZOS)
    p = f"{T}/tsv_{name}.png"
    big.save(p)
    out = subprocess.run(["tesseract", p, "-", "--psm", "7", "tsv"], capture_output=True, text=True).stdout
    print(f"== {name} (y{y0}..{y1}) ==")
    for line in out.splitlines()[1:]:
        f = line.split("\t")
        if len(f) == 12 and f[11].strip() and float(f[10]) > 20:
            x, y, w, h, word = int(f[6]), int(f[7]), int(f[8]), int(f[9]), f[11]
            ox0, ox1 = X0 + x // S, X0 + (x + w) // S
            oy0, oy1 = y0 + y // S, y0 + (y + h) // S
            sub = a[oy0:oy1 + 1, ox0:ox1 + 1].reshape(-1, 3)
            lum = sub.sum(axis=1)
            idx = np.argsort(lum)[:max(2, len(lum) // 6)]
            m = sub[idx].mean(axis=0).astype(int)
            # classify
            r, g, b = m
            cls = ("RED" if r - g > 45 and r - b > 45 else
                   "BLUE" if b - r > 45 else
                   "CYAN" if b - r > 30 and g - r > 20 else
                   "DARK" if max(r, g, b) < 130 else "PALE")
            print(f"  x{ox0:3d}..{ox1:3d} {word!r:34s} #{r:02X}{g:02X}{b:02X} {cls}")
