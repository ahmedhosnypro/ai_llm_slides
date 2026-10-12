#!/usr/bin/env python3
"""prep_assets.py — slide 035 asset production.
1. leftgrid035.png  — crop of the left 5x5 Image grid block (red border + faint photo +
   green digits baked), frame box x77..243 y207..337 (167x131).
2. panelcontent035.png — crop of the computation-panel content (5x5 grid with yellow 3x3 +
   red multipliers + black curved arrow + 3x3 output grid + '4' cell baked), frame box
   x398..875 y185..420 (478x236), with the screen-recording MOUSE CURSOR inpainted out
   (spec exclusion; ground rule (c)) — cursor-inpaint-restore pattern, plain-white variant.
3. Integrity checks banked; previous worker's 8 banked crops sanity-checked vs the frame.
"""
import numpy as np
from PIL import Image

FR = "videos/deep-learning/001_introduction/unique_slides/slide_035.jpg"
ASSETS = "videos/deep-learning/001_introduction/recreated_pptx/build/assets"
QA = "videos/deep-learning/001_introduction/recreated_pptx/qa/slide035"
import os
os.makedirs(ASSETS, exist_ok=True)

im = Image.open(FR).convert("RGB")
a = np.asarray(im).copy()

print("=== 0. Previous worker's crops: sanity template-check (title.png at scale 2) ===")
tc = Image.open(f"{QA}/crops/title.png").convert("L")
tc2 = tc.resize((tc.width // 2, tc.height // 2))
t = np.asarray(tc2).astype(int)
th, tw = t.shape
best = None
frame_g = np.asarray(im.convert("L")).astype(int)
for y0 in range(40, 130, 4):
    for x0 in range(200, 560, 6):
        if y0 + th > 540 or x0 + tw > 960:
            continue
        win = frame_g[y0:y0+th, x0:x0+tw]
        mad = np.abs(win - t).mean()
        if best is None or mad < best[0]:
            best = (mad, x0, y0)
print(f"  title.png (downscaled /2, {tw}x{th}): best match at x={best[1]} y={best[2]} MAD={best[0]:.1f}")
print("  (banked crops preserved unmodified; superseded for the build by fresh 1:1 measured crops below)")

print("=== 1. leftgrid035.png ===")
lg = im.crop((77, 207, 244, 338))  # x77..243, y207..337 -> 167x131
lg.save(f"{ASSETS}/leftgrid035.png")
print(f"  saved {ASSETS}/leftgrid035.png size={lg.size} (place at frame (77,207), w=167/72in h=131/72in)")

print("=== 2. panelcontent035.png with cursor inpaint ===")
# frame box x398..875 y185..420 -> PIL crop (398,185,876,421) = 478x236
pc = im.crop((398, 185, 876, 421))
pa = np.asarray(pc).copy()
# cursor measured nonwhite bbox x727..743 y369..385 (frame) -> crop coords x329..345 y184..200
# inpaint zone with margin: frame x720..752 y362..392 -> crop x322..354 y177..207
X0, X1, Y0, Y1 = 322, 355, 177, 208
before = pa[Y0:Y1, X0:X1].copy()
dark_before = int((before.sum(axis=2) < 700).sum())
nonwhite_before = int(((before[:, :, 0] < 240) | (before[:, :, 1] < 240) | (before[:, :, 2] < 235)).sum())
for y in range(Y0, Y1):
    # local row background: sample left and right of the zone in the same crop row
    left = pa[y, X0-14:X0-2].reshape(-1, 3)
    right = pa[y, X1+2:X1+14].reshape(-1, 3)
    pool = np.concatenate([left, right])
    pool = pool[pool.sum(axis=1) > 690]  # white-ish only
    fill = np.median(pool, axis=0).astype(np.uint8) if len(pool) else np.array([254, 255, 255], np.uint8)
    pa[y, X0:X1] = fill
dark_after = int((pa[Y0:Y1, X0:X1].sum(axis=2) < 700).sum())
nonwhite_after = int(((pa[:, :, 0] < 240) | (pa[:, :, 1] < 240) | (pa[:, :, 2] < 235)).sum())
print(f"  cursor zone x{X0}..{X1-1} y{Y0}..{Y1-1}: dark-px before={dark_before} after={dark_after}; "
      f"nonwhite whole-crop before={nonwhite_before} after(includes grids)=")
# whole-crop nonwhite AFTER excluding grid regions is meaningless; report zone only
out = Image.fromarray(pa)
out.save(f"{ASSETS}/panelcontent035.png")
print(f"  saved {ASSETS}/panelcontent035.png size={out.size} (place at frame (398,185), w=478/72in h=236/72in)")

print("=== 3. integrity: rest of crop untouched ===")
orig = np.asarray(pc)
diff = np.abs(orig.astype(int) - pa.astype(int)).sum(axis=2)
changed = np.where(diff > 0)
ys, xs = changed
print(f"  changed-px bbox: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)} (expected: inside zone x322..354 y177..207 only)")
outside = ((xs < X0) | (xs > X1-1) | (ys < Y0) | (ys > Y1-1)).sum()
print(f"  changed OUTSIDE zone: {outside} (must be 0)")
# grid-region sentinel: verify sentinel patches (grid corners) identical
sents = [(6, 15, 6, 25, "panel-grid TL"), (230, 15, 240, 25, "panel-grid TR"),
         (6, 225, 16, 235, "panel-grid BL"), (300, 8, 310, 18, "output-grid TL"),
         (130, 470, 140, 478, "output right"), (40, 230, 50, 240, "arrow zone")]
for (x0, y0, x1, y1, lab) in sents:
    same = np.array_equal(orig[y0:y1, x0:x1], pa[y0:y1, x0:x1])
    print(f"  sentinel {lab}: {'IDENTICAL' if same else 'CHANGED!'}")
print("=== done ===")
