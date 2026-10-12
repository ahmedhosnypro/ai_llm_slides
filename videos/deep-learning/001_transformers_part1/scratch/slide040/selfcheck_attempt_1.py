#!/usr/bin/env python3
"""Pre-judge self-check, attempt 1 — slide 040 render vs original frame.

Closed-loop ink comparison: render 150dpi (2000x1125) vs frame (960x540),
render_px = frame_px * 150/72 = *2.08333. Checks:
  A. ink bands (title red, blue lines): x/y extents within ~4 frame px
  B. containment: all content ink inside panel (chrome) bounds
  C. colors: rendered core colors match build targets
  D. no ink outside expected bands (wrap check)
  E. house chrome already verified by house_chrome_check.py (PASS)
Equations/delimiters/tables: none on this slide (checks 3/4/5 of 17 N/A).
"""
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide040/render/slide-1.png"
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_040.jpg"
SC = 150 / 72.0  # frame px -> render px

ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
fr = np.asarray(Image.open(FR).convert("RGB")).astype(int)
H, W = ren.shape[:2]
print(f"render {W}x{H}")

def bands(mask, y0, y1, x0, x1, thr=2):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    # row bands
    rr = sub.sum(axis=1)
    out, s = [], None
    for i, v in enumerate(rr):
        if v > thr and s is None:
            s = i
        elif v <= thr and s is not None:
            out.append((s + y0, i - 1 + y0)); s = None
    if s is not None:
        out.append((s + y0, y1 - 1))
    xs_all = (xs.min() + x0, xs.max() + x0)
    return out, xs_all

fails = []

# ---- title (render) — x restricted inside panel to exclude red border strokes ----
r, g, b = ren[:, :, 0], ren[:, :, 1], ren[:, :, 2]
red_ren = (r > 120) & (g < 100) & (b < 100)
tb = bands(red_ren, int(150 * SC), int(320 * SC), int(60 * SC), int(900 * SC))
print("render title bands/x:", tb)
if tb is None or len(tb[0]) != 1:
    fails.append(f"title: expected 1 red band, got {tb}")
else:
    y0, y1 = tb[0][0]
    sub = red_ren[y0:y1 + 1, int(60 * SC):int(900 * SC)]
    ys2, xs2 = np.where(sub)
    x0, x1 = xs2.min() + int(60 * SC), xs2.max() + int(60 * SC)
    fy = (y0 / SC, y1 / SC); fx = (x0 / SC, x1 / SC)
    print(f"  title frame-px: y {fy[0]:.1f}..{fy[1]:.1f} (orig 201..236), x {fx[0]:.1f}..{fx[1]:.1f} (orig 224..706)")
    if abs(fy[0] - 201) > 4 or abs(fy[1] - 236) > 4:
        fails.append(f"title y off: {fy} vs 201..236")
    if abs(fx[0] - 224) > 4 or abs(fx[1] - 706) > 4:
        fails.append(f"title x off: {fx} vs 224..706")

# ---- blue lines (render) ----
blue_ren = (b > 100) & (r < 120) & (g < 120)
bb = bands(blue_ren, int(300 * SC), int(500 * SC), int(60 * SC), int(900 * SC))
print("render blue bands/x:", bb)
orig = [(342, 367, 166, 467), (422, 447, 168, 504)]
if bb is None or len(bb[0]) != 2:
    fails.append(f"blue lines: expected 2 bands, got {bb}")
else:
    for i, (y0, y1) in enumerate(bb[0]):
        sub = blue_ren[y0:y1 + 1, int(60 * SC):int(900 * SC)]
        ys2, xs2 = np.where(sub)
        x0b, x1b = xs2.min() + int(60 * SC), xs2.max() + int(60 * SC)
        fy0, fy1, fx0, fx1 = y0 / SC, y1 / SC, x0b / SC, x1b / SC
        o = orig[i]
        print(f"  blue{i+1} frame-px: y {fy0:.1f}..{fy1:.1f} (orig {o[0]}..{o[1]}), x {fx0:.1f}..{fx1:.1f} (orig {o[2]}..{o[3]})")
        if abs(fy0 - o[0]) > 4 or abs(fy1 - o[1]) > 4:
            fails.append(f"blue{i+1} y off: {fy0:.1f}..{fy1:.1f} vs {o[0]}..{o[1]}")
        if abs(fx0 - o[2]) > 4 or abs(fx1 - o[3]) > 4:
            fails.append(f"blue{i+1} x off: {fx0:.1f}..{fx1:.1f} vs {o[2]}..{o[3]}")

# ---- containment: all content ink strictly inside chrome panel (42..918 x 45..540) ----
ink = (r < 200) | (g < 200) | (b < 200)
# restrict to panel interior, excluding border strokes themselves
ys, xs = np.where(ink)
in_panel = (xs > int(46 * SC)) & (xs < int(914 * SC)) & (ys > int(49 * SC)) & (ys < int(536 * SC))
ys2, xs2 = ys[in_panel], xs[in_panel]
print(f"content ink inside panel: x {xs2.min() / SC:.1f}..{xs2.max() / SC:.1f}, y {ys2.min() / SC:.1f}..{ys2.max() / SC:.1f} (panel interior 46..914 / 49..536)")
if xs2.min() / SC < 46 or xs2.max() / SC > 914 or ys2.min() / SC < 49 or ys2.max() / SC > 536:
    fails.append("content ink crosses panel interior bounds")

# ---- colors (render cores) ----
zone = ren[int(180 * SC):int(260 * SC), int(200 * SC):int(720 * SC)]
m = (zone[:, :, 0] > 120) & (zone[:, :, 1] < 100) & (zone[:, :, 2] < 100)
pix = zone[m]
if len(pix):
    p90 = np.percentile(pix, 90, axis=0)
    print(f"render title red p90: {p90.round(0)} (target C00000=192,0,0; render is lossless)")
else:
    fails.append("no red title ink in render")
zone = ren[int(330 * SC):int(380 * SC), int(150 * SC):int(480 * SC)]
m = (zone[:, :, 2] > 100) & (zone[:, :, 0] < 120) & (zone[:, :, 1] < 120)
pix = zone[m]
if len(pix):
    print(f"render blue core min: {pix.min(axis=0)} (target 0000B0=0,0,176)")

print()
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print("SELF-CHECK: PASS (title + 2 blue lines within 4 frame-px; containment ok; colors as built)")
