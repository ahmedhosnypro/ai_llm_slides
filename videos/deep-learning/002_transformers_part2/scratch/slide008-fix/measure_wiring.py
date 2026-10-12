#!/usr/bin/env python3
"""TASK 1 — Fidelity-fix measurement: the ⊗→Σ wiring in the ORIGINAL frame
(unique_slides/slide_008.jpg, 960x540, 1px = 1pt).

Read-only. Produces:
  * loose-red + any-dark masks over the softmax→rings→Σ band
  * per-row / per-column red profiles to find horizontal feeds and vertical stems
  * exact extents of every structure + arrowhead geometry
Banked output: measure_wiring_out.txt (same dir).
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_008.jpg").convert("RGB")).astype(int)
H, W, _ = frame.shape
R, G, B = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]

# strict red (banked corroboration threshold)
strict = (R >= 140) & (G <= 120) & (B <= 120) & ((R - np.maximum(G, B)) >= 50)
# loose red: catches anti-aliased strokes (pinkish, R dominant)
loose = (R >= 120) & ((R - G) >= 40) & ((R - B) >= 40)
# any-dark: catches non-red strokes if any (dark ink of any hue)
dark = (R + G + B) <= 420

print(f"frame {W}x{H}")
print(f"mask px in ROI x480..670 y195..395: strict={strict[195:395,480:670].sum()} "
      f"loose={loose[195:395,480:670].sum()} dark={dark[195:395,480:670].sum()}")

# ---------- 1) row profile: horizontal structures (feeds) ----------
print("\n=== ROW PROFILE: loose-red count per row, x 490..660 (>=6 px printed) ===")
for y in range(195, 395):
    cnt = int(loose[y, 490:660].sum())
    if cnt >= 6:
        xs = np.nonzero(loose[y, 490:660])[0] + 490
        # longest contiguous run
        runs, start = [], xs[0]
        for i in range(1, len(xs)):
            if xs[i] != xs[i - 1] + 1:
                runs.append((start, xs[i - 1])); start = xs[i]
        runs.append((start, xs[-1]))
        runs_s = " ".join(f"{a}-{b}" for a, b in runs if b - a >= 3)
        print(f"y{y:3d}: n={cnt:3d} runs>=4: {runs_s}")

# ---------- 2) column profile: vertical structures (stems) ----------
print("\n=== COL PROFILE: loose-red count per column, y 212..390 (>=6 px printed) ===")
for x in range(490, 665):
    cnt = int(loose[212:390, x].sum())
    if cnt >= 6:
        ys = np.nonzero(loose[212:390, x])[0] + 212
        runs, start = [], ys[0]
        for i in range(1, len(ys)):
            if ys[i] != ys[i - 1] + 1:
                runs.append((start, ys[i - 1])); start = ys[i]
        runs.append((start, ys[-1]))
        runs_s = " ".join(f"{a}-{b}" for a, b in runs if b - a >= 3)
        print(f"x{x:3d}: n={cnt:3d} runs>=4: {runs_s}")

# ---------- 3) the Σ bar geometry (strict mask, blue-ish box + red? text) ----------
print("\n=== SIGMA BAR (slide 516,194,135,25 -> frame 513.7,185.4..643.4,209.3) ===")
# find non-background ink rows between y 180..215 in x 510..650
bg = np.abs(frame - np.array([251, 226, 193])).sum(axis=2) <= 60  # peach FBE2C1-ish
for y in range(180, 216):
    ink = (~bg[y, 505:655]).sum()
    if ink:
        xs = np.nonzero(~bg[y, 505:655])[0] + 505
        print(f"y{y:3d}: ink={ink:3d} x {xs.min()}..{xs.max()}")

# ---------- 4) sample colors along candidate structures ----------
def sample(y, x0, x1):
    vals = frame[y, x0:x1 + 1]
    return [tuple(int(v) for v in p) for p in vals]

print("\n=== COLOR SAMPLES (rows of interest, every 4px) ===")
for y in (217, 237, 277, 316, 357, 225, 250):
    row = []
    for x in range(500, 655, 6):
        r, g, b = frame[y, x]
        row.append(f"{x}:({r},{g},{b})")
    print(f"y{y}: " + " ".join(row))
