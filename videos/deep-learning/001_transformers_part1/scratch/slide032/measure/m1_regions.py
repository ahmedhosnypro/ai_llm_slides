# m1_regions.py — PIL/numpy region measurement of unique_slides/slide_032.jpg
# Frame is 960x540, 1px = 1pt. Masks by tolerant color distance, connected bbox via label.
import numpy as np
from PIL import Image
import sys

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_032.jpg"
im = Image.open(F).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print("frame", W, "x", H)

def mask_for(rgb, tol):
    d = np.abs(a - np.array(rgb)).sum(axis=2)
    return d <= tol

def comps(mask, min_px=20):
    # simple connected components via scipy if present, else flood by rows
    try:
        from scipy import ndimage
        lab, n = ndimage.label(mask)
        out = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            if len(xs) < min_px: continue
            out.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(len(xs))))
        return out
    except ImportError:
        # fallback: coarse grid clustering
        ys, xs = np.where(mask)
        return [("noscipy", len(xs), 0, 0, 0)]

targets = {
  "red_border_C00000": ((192, 0, 0), 110),
  "panel_gray_E9E9E7": ((233, 233, 231), 12),
  "badge_yellow_FDFD96": ((253, 253, 150), 60),
  "white_FFFFFF": ((255, 255, 255), 12),
  "pill_EFD9EF": ((239, 217, 239), 40),
  "matrix_FDF3C0": ((253, 243, 192), 50),
  "outcell_F9C9D4": ((249, 201, 212), 45),
  "band_D9D9D9": ((217, 217, 217), 14),
  "input_gray_C0C0C0": ((192, 192, 192), 20),
  "blue_2020C0": ((32, 32, 192), 110),
  "green_1A8A1A": ((26, 138, 26), 100),
  "magenta_B020B0": ((176, 32, 176), 110),
  "orange_E07020": ((224, 112, 32), 100),
}
for name, (rgb, tol) in targets.items():
    m = mask_for(rgb, tol)
    n = int(m.sum())
    if n == 0:
        print(f"{name}: NONE")
        continue
    cs = comps(m, min_px=30)
    cs.sort(key=lambda c: -c[4])
    top = cs[:8]
    print(f"{name}: total_px={n}")
    for (x0, y0, x1, y1, npx) in top:
        print(f"   bbox x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) px={npx}")
