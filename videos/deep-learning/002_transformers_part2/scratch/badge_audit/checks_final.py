#!/usr/bin/env python3
"""1) Raw-pixel view under the 048 occlusion line (any faint ink rows below y=68?)
   2) slide_046 badge status  3) the four unreadable sweep slides 014/053/054/055."""
from PIL import Image
import numpy as np
from scipy import ndimage
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import badge_audit as ba

ROOT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"

# ---- 1) raw luminance grid around 048's right digit ----
a = np.array(Image.open(os.path.join(ROOT, "unique_slides", "slide_048.jpg")).convert("RGB"))
r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
lum = (0.299 * r + 0.587 * g + 0.114 * b)
print("048 raw luminance grid rows 64..76, cols 866..886 (dark=@ light=space):")
lmin, lmax = 40, 255
chars = "@%#*+=-:. "
for y in range(64, 77):
    row = "".join(chars[min(9, max(0, int((255 - lum[y, x]) / (255 - 40) * 9.99)))] for x in range(866, 887))
    print(f"{y:3d} |{row}|")
print("cols 866..886; note where the green box (dark border) starts per column")
# green box border rows: find greenest pixel per column
print("\ngreen-occluder top edge (first y where (g-r)>40 and g>110) per column:")
for x in range(866, 887):
    edge = None
    for y in range(60, 90):
        if (g[y, x] - r[y, x]) > 40 and g[y, x] > 110:
            edge = y
            break
    print(f"  x={x}: box_edge_y={edge}", end=";")
print()

# ---- 2) slide_046 badge ----
print("\nslide_046 badge check:")
a46 = np.array(Image.open(os.path.join(ROOT, "unique_slides", "slide_046.jpg")).convert("RGB"))
r4, g4, b4 = a46[:, :, 0].astype(int), a46[:, :, 1].astype(int), a46[:, :, 2].astype(int)
ym = (r4 > 215) & (g4 > 205) & (b4 < 215) & ((r4 - b4) > 35) & ((g4 - b4) > 35)
reg = np.zeros(ym.shape, bool); reg[:170, 830:] = True
ym &= reg
print("  yellow px in badge region:", int(ym.sum()))
lab, n = ndimage.label(ym)
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) >= 40:
        print(f"    blob area={len(ys)} bbox=({xs.min()},{ys.min()})-({xs.max()},{ys.max()})")
l46 = (0.299 * r4 + 0.587 * g4 + 0.114 * b4)
print("  luminance grid rows 54..92 cols 856..896:")
for y in range(54, 93, 1):
    row = "".join(chars[min(9, max(0, int((255 - l46[y, x]) / (255 - 40) * 9.99)))] for x in range(856, 897))
    print(f"{y:3d} |{row}|")

# ---- 3) unreadable sweep slides ----
for name in ["slide_014", "slide_053", "slide_054", "slide_055"]:
    rec = ba.analyze_badge(name)
    print(f"\n{name}: expected '{name[-3:]}'")
    if "_glyph_masks" in rec:
        print("  badge bbox", rec["badge_bbox"], "n_glyphs:", rec["n_glyphs"])
        for gl in rec["glyphs"]:
            print(f"  glyph bbox={gl['bbox']} area={gl['area']}")
            print("  " + gl["ascii"].replace("\n", "\n  "))
    else:
        print("  error:", rec.get("error"))
