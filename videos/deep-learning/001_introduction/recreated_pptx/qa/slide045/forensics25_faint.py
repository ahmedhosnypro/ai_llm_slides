#!/usr/bin/env python3
"""forensics25: faint-ink scan + zoom of anything in the two callout corridors."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
org = np.asarray(Image.open(VID + "/unique_slides/slide_045.jpg").convert("RGB")).astype(int)
r, g, b = org[:, :, 0], org[:, :, 1], org[:, :, 2]
# anything meaningfully darker than the E9E9E7 panel background
faint = (r < 213) | (g < 213) | (b < 211)


def scan(name, x0, x1, y0, y1):
    n = 0
    print(f"== {name} x{x0}..{x1} y{y0}..{y1} ==")
    for y in range(y0, y1):
        cols = list(np.where(faint[y, x0:x1])[0] + x0)
        if cols:
            n += len(cols)
            print(f"  y{y}: {cols}")
    if not n:
        print("  CLEAN (pure background)")


scan("corridor A faint x701..735 y352..372", 701, 735, 352, 372)
scan("corridor A faint wide x622..735 y352..385", 622, 735, 352, 385)
scan("corridor B faint x701..734 y430..465", 701, 734, 430, 465)
scan("corridor B faint wide x622..734 y450..465", 622, 734, 450, 465)
scan("mystery dark x642..649 y381..385 zoom", 630, 662, 375, 392)

print("== enhanced view of arrowhead zone x688..712 y342..360 (chars: <=180 '#' <=205 '+' <=213 '.') ==")
for y in range(342, 360):
    row = ""
    for x in range(688, 712):
        v = min(r[y, x], g[y, x], b[y, x])
        row += "#" if v <= 180 else ("+" if v <= 205 else ("." if v <= 213 else " "))
    print(f"  y{y} |{row}|")
