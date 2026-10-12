#!/usr/bin/env python3
"""Sample pixel colors near expected chrome border positions in frame 011."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
a = np.asarray(Image.open(f"{V}/unique_slides/slide_011.jpg").convert("RGB")).astype(int)

def darkest_run(vals, label):
    lum = vals.sum(axis=1)
    i = int(lum.argmin())
    print(label, "min-lum idx", i, "rgb", vals[i], "| neighborhood:", [tuple(v) for v in vals[max(0, i - 2):i + 3]])

# left border near x~58: row y=250, x 50..66
darkest_run(a[250, 50:66], "left border y250")
# right border near x~901: row y=250, x 893..910
darkest_run(a[250, 893:910], "right border y250")
# top border near y~43: col x=480, y 36..52
darkest_run(a[36:52, 480], "top border x480")
# bottom stroke near y~516: col x=480, y 508..522
darkest_run(a[508:522, 480], "bottom x480")
# badge: x 780..892 wide yellow — print a slice at y=70 x 860..900
print("y70 x860..902:", [tuple(v) for v in a[70, 860:902:3]])
# badge at y 56..129 seems too tall (73px) — the yellow detect may have caught the Y-box
# green/yellow content at left. restrict x>=855:
yl = (a[:, :, 0] > 230) & (a[:, :, 1] > 220) & (a[:, :, 2] > 120) & (a[:, :, 2] < 210)
ys, xs = np.where(yl[:130, 855:])
if len(xs):
    print("badge yellow bbox x", xs.min() + 855, xs.max() + 855, "y", ys.min(), ys.max())
