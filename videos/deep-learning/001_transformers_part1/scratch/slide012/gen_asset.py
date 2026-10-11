#!/usr/bin/env python3
"""Generate the slide-012 page asset: bake instructor highlights into the v5 page-1
raster (300dpi), crop to the frame's visible window, pad left, save.

Also prints: refined highlight rects (profile-based), border z-order samples,
and the exact JS placement constants.
"""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
FR = f"{VID}/unique_slides/slide_012.jpg"
PG = f"{VID}/scratch/slide012/page300-01.png"
OUT = f"{VID}/recreated_pptx/build/assets/slide012_page1.png"

frame = np.asarray(Image.open(FR).convert("RGB")).astype(float)
page = Image.open(PG).convert("RGB")
pa = np.asarray(page).astype(float)

SX, OX = 0.28909, 97.13
SY, OY = 0.28480, -60.52
f2p_x = lambda fx: (fx - OX) / SX
f2p_y = lambda fy: (fy - OY) / SY

# ---------- refined frame box bounds via profiles ----------
def profile_bounds(x0, x1, y0, y1, core, tol, axis, name):
    reg = frame[y0:y1, x0:x1]
    d = np.abs(reg - np.array(core)).sum(axis=2)
    m = (d < tol)
    frac = m.mean(axis=1 if axis == "y" else 0)
    idx = np.where(frac > 0.35)[0]
    if len(idx) == 0:
        print(f"  {name}: EMPTY"); return None
    lo, hi = idx.min(), idx.max()
    if axis == "y":
        print(f"  {name}: y[{y0+lo},{y0+hi}] (frac span)")
        return (y0 + lo, y0 + hi)
    print(f"  {name}: x[{x0+lo},{x0+hi}] (frac span)")
    return (x0 + lo, x0 + hi)

print("== refined highlight bounds (frame px) ==")
PINK = (240, 167, 242); TAN = (249, 215, 177)
# vertical bounds from a text-free column slice of each box, horizontal from a row slice
boxes = {}
for name, (cx0, cx1, cy0, cy1) in {
    "vaswani": (262, 332, 160, 200), "shazeer": (388, 457, 160, 200),
    "parmar": (497, 580, 160, 200), "uszkoreit": (612, 695, 160, 200),
    "jones": (257, 340, 222, 252), "kaiser": (575, 643, 222, 252),
}.items():
    by = profile_bounds(cx0, cx1, cy0, cy1, PINK, 110, "y", name + " y")
    bx = profile_bounds(cx0 - 6, cx1 + 6, cy0, cy1, PINK, 110, "x", name + " x")
    boxes[name] = (bx, by)
ty = profile_bounds(340, 592, 45, 90, TAN, 70, "y", "title y")
tx = profile_bounds(320, 610, 55, 82, TAN, 70, "x", "title x")

print("== border vs date-band z-order samples (raw 1px) ==")
for (x, y) in [(93, 150), (94, 150), (93, 250), (94, 250), (91, 250), (92, 250), (91, 150), (92, 150)]:
    print(f"  ({x},{y}) = {frame[y, x].astype(int)}")

# ---------- bake highlights in page coords ----------
def bake(arr, fx0, fx1, fy0, fy1, alpha, color):
    x0, x1 = int(round(f2p_x(fx0))), int(round(f2p_x(fx1)))
    y0, y1 = int(round(f2p_y(fy0))), int(round(f2p_y(fy1)))
    x0c, y0c = max(0, x0), max(0, y0)
    x1c, y1c = min(arr.shape[1], x1), min(arr.shape[0], y1)
    reg = arr[y0c:y1c, x0c:x1c]
    arr[y0c:y1c, x0c:x1c] = alpha * np.array(color) + (1 - alpha) * reg
    print(f"  baked page rect x[{x0},{x1}] y[{y0},{y1}] (clipped x[{x0c},{x1c}] y[{y0c},{y1c}])")

ALPHA_TAN, COL_TAN = 0.275, (233, 109, 0)
ALPHA_PINK, COL_PINK = 0.52, (226, 86, 230)

print("== baking ==")
bake(pa, tx[0], tx[1] + 1, ty[0], ty[1] + 1, ALPHA_TAN, COL_TAN)
for name, (bx, by) in boxes.items():
    bake(pa, bx[0], bx[1] + 1, by[0], by[1] + 1, ALPHA_PINK, COL_PINK)

# ---------- crop + pad ----------
PAD_L = 13  # page px of white padding left (frame x93.37..97.13)
x0, x1 = -PAD_L, 2419
y0, y1 = 397, 2054
canvas = np.full((y1 - y0, x1 - x0, 3), 255.0)
sx0 = max(0, x0)
canvas[:, sx0 - x0:, :] = pa[y0:y1, sx0:x1]
Image.fromarray(canvas.astype(np.uint8)).save(OUT)
print(f"== asset saved {OUT} size {canvas.shape[1]}x{canvas.shape[0]}")

# ---------- placement constants for the JS ----------
ix0 = (OX + x0 * SX) / 72.0
iy0 = y0 * SY + OY
iw = (x1 - x0) * SX / 72.0
ih = (y1 - y0) * SY / 72.0
print("== JS placement ==")
print(f"  image: x={ix0:.5f} y={iy0/72:.5f} w={iw:.5f} h={ih:.5f}  (in)")
print(f"  border rect: x={93.5/72:.5f} y={52.5/72:.5f} w={703/72:.5f} h={472/72:.5f}")
print(f"  date band shape: x={91/72:.5f} y={186/72:.5f} w={(136.5-91)/72:.5f} h={(309.5-186)/72:.5f}")
