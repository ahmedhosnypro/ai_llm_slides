#!/usr/bin/env python3
"""Deterministic XML post-pass for slide_042_recreated.pptx (idempotent, fail-loud).

LibreOffice renders baseline="30000" superscript runs with a raise of ~30% of the
run size — measured ~3 frame-px LOW vs the original's superscript r (ink top must
equal the W cap top). This pass raises the superscript baseline 30000 -> 43000
(43% of the 24pt run) in ppt/slides/slide1.xml ONLY for baseline="30000" runs
(the four red superscript r's). Subscript runs (-40000) verified correct (closed
loop: q ink top 303.5 vs original 304) and are left untouched.

Run AFTER every `node build/slide_042.js`:
    python3 build/slide_042_postpass.py
"""
import re
import shutil
import sys
import zipfile

PPTX = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/slide_042_recreated.pptx"
SLIDE_XML = "ppt/slides/slide1.xml"

with zipfile.ZipFile(PPTX) as z:
    xml = z.read(SLIDE_XML).decode("utf-8")

n_sup = xml.count('baseline="30000"')
n_sub = xml.count('baseline="-40000"')
if n_sup == 0 and 'baseline="43000"' not in xml:
    sys.exit(f"FAIL: no superscript runs found in {SLIDE_XML} — build regenerated without sups?")
if 'baseline="43000"' in xml and n_sup == 0:
    print(f"post-pass: already applied ({n_sub} sub runs untouched); no change")
    sys.exit(0)

xml2 = xml.replace('baseline="30000"', 'baseline="43000"')

tmp = PPTX + ".tmp"
with zipfile.ZipFile(PPTX) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == SLIDE_XML:
            data = xml2.encode("utf-8")
        zout.writestr(item, data)
shutil.move(tmp, PPTX)
print(f"post-pass: raised {n_sup} superscript baseline(s) 30000->43000; {n_sub} subscript(s) untouched")
