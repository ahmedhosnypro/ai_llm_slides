#!/usr/bin/env python3
"""Metric-solve font sizes for slide 040 text lines against measured ink widths,
and crop the three photos (incl. their baked red borders) into build/assets/.

Measured ink (frame px, 1px = 1pt):
  title 'How many filters we should apply'  x 204..762  (559)  bold
  L1    'Example: 30 different filters'     x 83..364   (282)  bold
  L2    'Each filter can detect different information from the image' x 84..632 (549)
  L3    'Apply those 30 filters on the image  (each one should be applied on the whole' x 84..612 (529)
  L4    'locations on the image)'           x 83..503   (421)
"""
from PIL import Image, ImageFont

AR = "/usr/share/fonts/TTF/Arial.TTF"
ARB = "/usr/share/fonts/TTF/Arialbd.TTF"

TARGETS = [
    ("title", "How many filters we should apply", ARB, 559),
    ("L1", "Example: 30 different filters", ARB, 282),
    ("L2", "Each filter can detect different information from the image", AR, 549),
    ("L3", "Apply those 30 filters on the image  (each one should be applied on the whole", AR, 529),
    ("L4", "locations on the image)", AR, 421),
]

for name, text, path, target in TARGETS:
    # ink width = bbox of rendered text (L bearing to R bearing)
    best = None
    for size10 in range(160, 441):  # 16.0 .. 44.0 pt in 0.1 steps
        f = ImageFont.truetype(path, size10)  # size in units; we treat 10 == 1pt
        bbox = f.getbbox(text)
        w = bbox[2] - bbox[0]
        if best is None or abs(w - target * 10) < best[0]:
            best = (abs(w - target * 10), size10 / 10.0, w / 10.0, bbox)
    err, size, w, bbox = best
    print(f"{name}: solved {size:.1f}pt -> ink width {w:.1f}px (target {target}, err {err/10:.1f}px); "
          f"bbox {bbox}")
