#!/usr/bin/env python3
"""m05_containers.py — precise container geometry on slide_051 frame.
Finds connected components of key fill colors, reports bboxes (frame px + slide pt).
Mapping (fitted m01/m02): slide_x = (fx - 18.41)/0.96038 ; slide_y = (fy + 0.05)/0.95657
"""
import numpy as np
from PIL import Image
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_051.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W, _ = im.shape

def to_slide(fx, fy):
    return (fx - 18.41) / 0.96038, (fy + 0.05) / 0.95657

def comps(mask, min_px=60, label=""):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) < min_px:
            continue
        out.append((len(xs), xs.min(), xs.max(), ys.min(), ys.max()))
    out.sort(reverse=True)
    for npx, x0, x1, y0, y1 in out[:14]:
        sx0, sy0 = to_slide(x0, y0)
        sx1, sy1 = to_slide(x1 + 1, y1 + 1)
        print(f"  {label} n={npx:6d} frame x {x0:3d}..{x1:3d} y {y0:3d}..{y1:3d}  slide x {sx0:6.1f}..{sx1:6.1f} y {sy0:6.1f}..{sy1:6.1f} (w {sx1-sx0:5.1f} h {sy1-sy0:5.1f})")

def near(rgb, tol):
    return np.abs(im - np.array(rgb)).max(axis=2) <= tol

print("== peach FBE5D6 (encoder panel fill) =="); comps(near((251,229,214), 10), 500, "peach")
print("== bright green 00E100 (encoder overlay) =="); comps(near((0,225,0), 55), 500, "grn")
print("== orange ED7D31 (decoder panel fill) =="); comps(near((237,125,49), 28), 500, "orange")
print("== light green CCFFCC (decoder overlay) =="); comps(near((204,255,204), 14), 500, "ccffcc")
print("== blue 4472C4 boxes =="); comps(near((68,114,196), 30), 60, "blue")
print("== gray 7F7F7F boxes =="); comps(near((127,127,127), 22), 60, "gray")
print("== pink FFC7CE boxes =="); comps(near((255,199,206), 16), 60, "pink")
print("== purple C9A0DC box =="); comps(near((201,160,220), 28), 60, "purple")
print("== teal 66CCCC =="); comps(near((102,204,204), 30), 40, "teal")
print("== yellow boxes =="); comps(near((255,255,0), 45), 60, "yellow")
print("== brown A0622D =="); comps(near((160,98,45), 30), 60, "brown")
print("== pure red FF0000 (arrows) =="); comps(near((255,0,0), 60), 80, "red")
print("== title red C00000 =="); comps((np.abs(im-np.array([192,0,0])).max(axis=2)<=45), 60, "C00000")
print("== white callouts =="); comps(near((255,255,255), 8), 80, "white")
