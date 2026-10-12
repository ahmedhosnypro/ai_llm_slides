#!/usr/bin/env python3
"""PIL forensics for 001_introduction slide_001.jpg (960x540, 1px = 1pt).
Measures every content element's ink geometry + colors for the recreation build."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_001.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
print(f"frame {W}x{H}")
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def bbox(mask, x0=0, x1=W, y0=0, y1=H, label=""):
    m = np.zeros_like(mask)
    m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if not len(ys):
        print(f"{label}: NO INK")
        return None
    # core color: modal color of the mask pixels
    px = IM[m]
    print(f"{label}: x {xs.min()}-{xs.max()} (w {xs.max()-xs.min()+1}), y {ys.min()}-{ys.max()} "
          f"(h {ys.max()-ys.min()+1}) | in: x {xs.min()/72:.3f}-{(xs.max()+1)/72:.3f}in, "
          f"y {ys.min()/72:.3f}-{(ys.max()+1)/72:.3f}in | n={len(ys)} core~{np.median(px,axis=0).astype(int)}")
    return xs.min(), xs.max(), ys.min(), ys.max()

# background sample (panel interior, away from ink)
print("bg sample @(30,300):", IM[300, 30], " @(470,480):", IM[470, 480], " @(100,700):", IM[100, 700])

# dark masks
red = (r > 130) & (g < 90) & (b < 90)                      # C00000-ish title/labels
darkred = (r > 90) & (r < 180) & (g < 70) & (b < 70)       # 8B1A1A-ish rule
blue = (b > 110) & (r < 90) & (g < 90)                     # navy/blue text
teal = (g > 130) & (b > 130) & (r < 120) & (abs(g - b) < 60)  # logo emblem
dark = (r < 80) & (g < 80) & (b < 80)                      # black-ish ink

# 1. top rule: scan full width for horizontal red-ish line in top 20% rows
print("\n--- top rule region (rows 0..80) ---")
for y in range(0, 80):
    row = darkred[y]
    if row.sum() > 100:
        xs = np.where(row)[0]
        print(f"row {y}: n={row.sum()} x {xs.min()}-{xs.max()} color~{np.median(IM[y][row],axis=0).astype(int)}")

# 2. title block: red ink in upper area
print("\n--- red ink rows profile (y 60..260, x 100..860) ---")
prof = red[:, 100:860].sum(axis=1)
y = 60
while y < 260:
    if prof[y] > 3:
        y2 = y
        while y2 < 260 and prof[y2] > 3:
            y2 += 1
        m = red[y:y2, :]
        xs = np.where(m.any(axis=0))[0]
        print(f"band y {y}-{y2-1} (h {y2-y}): x {xs.min()}-{xs.max()} | in y {y/72:.3f}-{y2/72:.3f} x {xs.min()/72:.3f}-{(xs.max()+1)/72:.3f}")
        # core color
        px = IM[y:y2, :][m]
        print(f"   core color ~ {np.median(px, axis=0).astype(int)} n={len(px)}")
        y = y2
    y += 1

# 3. credit block: red+blue ink center region
print("\n--- credit/instructor ink bands (y 260..540) ---")
mask_any = red | blue | dark
prof2 = mask_any[:, 30:930].sum(axis=1)
y = 260
while y < 540:
    if prof2[y] > 3:
        y2 = y
        while y2 < 540 and prof2[y2] > 3:
            y2 += 1
        seg_red = red[y:y2, :].sum()
        seg_blue = blue[y:y2, :].sum()
        seg_dark = dark[y:y2, :].sum()
        m = mask_any[y:y2, :]
        xs = np.where(m.any(axis=0))[0]
        print(f"band y {y}-{y2-1} (h {y2-y}): x {xs.min()}-{xs.max()} | red {seg_red} blue {seg_blue} dark {seg_dark}")
        if seg_red:
            xr = np.where(red[y:y2, :].any(axis=0))[0]
            print(f"   red x {xr.min()}-{xr.max()}  (in {xr.min()/72:.3f}-{(xr.max()+1)/72:.3f})")
        if seg_blue:
            xb = np.where(blue[y:y2, :].any(axis=0))[0]
            print(f"   blue x {xb.min()}-{xb.max()} (in {xb.min()/72:.3f}-{(xb.max()+1)/72:.3f}) core~{np.median(IM[y:y2,:,:][blue[y:y2,:]],axis=0).astype(int)}")
        if seg_dark:
            xd = np.where(dark[y:y2, :].any(axis=0))[0]
            print(f"   dark x {xd.min()}-{xd.max()}")
        y = y2
    y += 1

# 4. teal logo
print("\n--- teal emblem ---")
bbox(teal, label="teal emblem")

# 5. white-ish box in bottom-right (logo text box): bright pixels in region y 440..530, x 560..920
white = (r > 235) & (g > 235) & (b > 235)
bbox(white, 560, 930, 440, 535, "white box (logo area)")

# 6. maroon text in white box
maroon = (r > 90) & (r < 190) & (g < 80) & (b < 90)
bbox(maroon, 620, 930, 440, 535, "maroon text (logo box)")

# 7. '+' artifact: light gray small cluster mid-right per spec (~87%w, ~65%h) -> x~835,y~350
grayish = (abs(r - g) < 12) & (abs(g - b) < 12) & (r > 140) & (r < 210)
bbox(grayish, 780, 900, 300, 420, "gray artifact region")

# 8. black bottom strip?
print("\n--- bottom rows dark check ---")
for y in (536, 537, 538, 539):
    row = IM[y]
    print(f"row {y}: mean {row.mean(axis=0).astype(int)} min {row.min()} max {row.max()}")
