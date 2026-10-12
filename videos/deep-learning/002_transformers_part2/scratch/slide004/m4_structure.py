#!/usr/bin/env python3
# m4_structure.py — is the left panel the same drawing at another offset/scale, or a
# different rendering? Ink-mask ASCII of both + shift search + relaxed border probe.
import numpy as np
from PIL import Image

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
warped = np.asarray(Image.open(S + "/frame_warped.png").convert("RGB"), dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)

def ink(a):
    return a.mean(axis=2) < 150

wi, ri = ink(warped), ink(render)

def ascii_ink(m, x0, x1, y0, y1, w=64, h=28, name=""):
    print(f"\n{name} ink map x{x0}..{x1} y{y0}..{y1}:")
    for cy in range(h):
        row = ""
        for cx in range(w):
            cell = m[y0 + (y1 - y0) * cy // h: y0 + (y1 - y0) * (cy + 1) // h,
                     x0 + (x1 - x0) * cx // w: x0 + (x1 - x0) * (cx + 1) // w]
            f = cell.mean()
            row += " " if f < 0.04 else ("." if f < 0.12 else ("+" if f < 0.3 else "#"))
        print(row)

# left panel interior
ascii_ink(wi, 180, 940, 240, 1080, name="warped frame LEFT")
ascii_ink(ri, 180, 940, 240, 1080, name="render LEFT")

# shift search: does shifting the warped left panel reduce the diff?
best = None
for dy in range(-40, 41, 4):
    for dx in range(-60, 61, 6):
        w2 = np.roll(np.roll(warped, dy, axis=0), dx, axis=1)
        d = np.abs(w2[240:1080, 180:940] - render[240:1080, 180:940]).sum(axis=2).mean()
        if best is None or d < best[0]:
            best = (d, dx, dy)
print(f"\nleft-panel best shift: mean {best[0]:.1f} at dx {best[1]} dy {best[2]} (0,0 mean: "
      f"{np.abs(warped[240:1080, 180:940] - render[240:1080, 180:940]).sum(axis=2).mean():.1f})")

# right panel interior shift search too
best = None
for dy in range(-40, 41, 4):
    for dx in range(-60, 61, 6):
        w2 = np.roll(np.roll(warped, dy, axis=0), dx, axis=1)
        d = np.abs(w2[240:1080, 1200:1900] - render[240:1080, 1200:1900]).sum(axis=2).mean()
        if best is None or d < best[0]:
            best = (d, dx, dy)
print(f"right-panel best shift: mean {best[0]:.1f} at dx {best[1]} dy {best[2]} (0,0 mean: "
      f"{np.abs(warped[240:1080, 1200:1900] - render[240:1080, 1200:1900]).sum(axis=2).mean():.1f})")

# relaxed left-panel border probe on the ORIGINAL frame
frame = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit2.npy")
prof = (frame[150:450, 60:140].mean(axis=2) < 190).sum(axis=0)
for i, v in enumerate(prof):
    if v > 60:
        print(f"frame col {60 + i}: dark rows {v}  (-> render x {ax + sx * (60 + i):.1f})")
