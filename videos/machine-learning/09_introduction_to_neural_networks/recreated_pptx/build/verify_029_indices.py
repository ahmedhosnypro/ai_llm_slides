#!/usr/bin/env python3
"""Closed-loop check for slide 029's judge-cited diagram fixes.

Verifies that the current PPTX embeds the current diagram asset, that both
Net_i/Net_j headers have clear top margins in that asset, and that the i/j
callout labels are present in the slide XML.
"""
import hashlib
import re
import sys
import zipfile

import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
DIAGRAM = f"{V}/recreated_pptx/build/slide_029_diagram.png"
PPTX = f"{V}/recreated_pptx/build/slide_029_recreated.pptx"
RENDER = f"{V}/recreated_pptx/build/slide_029_rendered-1.png"

failures = []
a = np.asarray(Image.open(DIAGRAM).convert("RGB")).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 120) & (r - g > 50) & (r - b > 50) & (g < 170)
for name, x0, x1 in [("Net_i", 450, 650), ("Net_j", 900, 1100)]:
    m = red[:60, x0:x1]
    ys, xs = np.where(m)
    if not len(xs):
        failures.append(f"{name}: no red header ink found")
        continue
    top = int(ys.min())
    print(f"{name}: bbox=({x0 + int(xs.min())},{top},{x0 + int(xs.max())},{int(ys.max())}) "
          f"top_clearance={top}px top_row_ink={int(m[0].sum())}")
    if top < 4 or m[0].any():
        failures.append(f"{name}: clipped at diagram top")

diagram_md5 = hashlib.md5(open(DIAGRAM, "rb").read()).hexdigest()
with zipfile.ZipFile(PPTX) as z:
    matches = [n for n in z.namelist()
               if n.startswith("ppt/media/") and hashlib.md5(z.read(n)).hexdigest() == diagram_md5]
    xml = z.read("ppt/slides/slide1.xml").decode("utf-8")
print(f"diagram_md5={diagram_md5} pptx_matches={matches}")
if not matches:
    failures.append("PPTX does not embed the current diagram asset")
for label in ("i", "j"):
    if not re.search(rf"<a:t>{label}</a:t>", xml):
        failures.append(f"callout label {label!r} missing from slide XML")

im = Image.open(RENDER).convert("RGB")
arr = np.asarray(im)
print(f"render={im.size} mean={float(arr.mean()):.3f}")
if im.size != (2001, 1125):
    failures.append(f"unexpected render size {im.size}")

if failures:
    print("VERIFY RESULT: FAIL")
    for f in failures:
        print("  - " + f)
    sys.exit(1)
print("VERIFY RESULT: PASS")
