#!/usr/bin/env python3
"""patch_arrow_adj.py — inject preset adjusts into the two rightArrow shapes of
slide_043_recreated.pptx (pptxgenjs 4.0.1 cannot set preset-geometry adjusts).

The original frame's block arrows have head length ~= full short side (20px of a
50x20 arrow) -> DrawingML adj2 = 100000 (default 50000 gives a 10px head).
adj1 = 50000 (shaft = half height, default) — both injected explicitly.

Usage: python3 patch_arrow_adj.py <pptx>
Idempotent: skips shapes that already carry the adjust guides. Fails loudly if
the expected rightArrow count != 2.
"""
import sys
import zipfile
import shutil
import tempfile
import os
import re

PPTX = sys.argv[1]
TMP = tempfile.mkdtemp(prefix="adjpatch_")

with zipfile.ZipFile(PPTX) as z:
    z.extractall(TMP)

target = os.path.join(TMP, "ppt", "slides", "slide1.xml")
with open(target, "r", encoding="utf-8") as f:
    xml = f.read()

n_arrow = xml.count('prst="rightArrow"')
if n_arrow != 2:
    print(f"FAIL: expected 2 rightArrow shapes, found {n_arrow}")
    sys.exit(1)

old = '<a:prstGeom prst="rightArrow"><a:avLst></a:avLst></a:prstGeom>'
new = ('<a:prstGeom prst="rightArrow"><a:avLst>'
       '<a:gd name="adj1" fmla="val 50000"/>'
       '<a:gd name="adj2" fmla="val 100000"/>'
       '</a:avLst></a:prstGeom>')

cnt = xml.count(old)
if cnt == 2:
    xml = xml.replace(old, new)
    print("patched 2 rightArrow shapes (adj1=50000, adj2=100000)")
elif xml.count(new) == 2:
    print("already patched (idempotent no-op)")
else:
    print(f"FAIL: unexpected rightArrow avLst forms (plain={cnt})")
    sys.exit(1)

with open(target, "w", encoding="utf-8") as f:
    f.write(xml)

# rezip
out_tmp = PPTX + ".tmp"
with zipfile.ZipFile(out_tmp, "w", zipfile.ZIP_DEFLATED) as z:
    for root, _, files in os.walk(TMP):
        for fn in files:
            full = os.path.join(root, fn)
            rel = os.path.relpath(full, TMP)
            z.write(full, rel)
os.replace(out_tmp, PPTX)
shutil.rmtree(TMP)
print("rezipped " + PPTX)
