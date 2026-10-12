#!/usr/bin/env python3
"""Generate matched-scale dense-region crop pairs (render_5 vs original frame).
Both crops end at the SAME pixel size and the SAME effective px-per-frame-px scale:
  render: native 150dpi (2.16766 px/frame-px) -> x2 upscale
  original: 1 px/frame-px -> x4.335 (= 2.16766*2) upscale
Regions (frame coords):
  intro    x80..900  y98..192
  panelbot x150..556 y392..500
"""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
REN = f"{VID}/recreated_pptx/qa/slide040/render_5.png"
FRM = f"{VID}/unique_slides/slide_040.jpg"
OUT = f"{VID}/recreated_pptx/qa/slide040/crops2"

import os
for sub in ("intro", "panelbot"):
    os.makedirs(f"{OUT}/{sub}", exist_ok=True)

SX, SY = 2.16766, 2.18013   # frame->render (150dpi)
UP = 2                      # post-crop upscale for render; frame uses UP*S

regions = {"intro": (80, 900, 98, 192), "panelbot": (150, 556, 392, 500)}
ren_im = Image.open(REN).convert("RGB")
frm_im = Image.open(FRM).convert("RGB")

for name, (fx0, fx1, fy0, fy1) in regions.items():
    # render crop
    rx0, ry0 = (fx0 - 18.63) * SX, fy0 * SY
    rx1, ry1 = (fx1 - 18.63) * SX, fy1 * SY
    rc = ren_im.crop((int(round(rx0)), int(round(ry0)), int(round(rx1)), int(round(ry1))))
    target_w = int(round(rc.width * UP))
    rc2 = rc.resize((target_w, int(round(rc.height * UP))), Image.LANCZOS)
    # original crop at matched scale
    oc = frm_im.crop((fx0, fy0, fx1, fy1))
    s = SX * UP
    oc2 = oc.resize((target_w, int(round(oc.height * s))), Image.LANCZOS)
    if oc2.width != rc2.width or oc2.height != rc2.height:
        oc2 = oc2.resize(rc2.size, Image.LANCZOS)
    rc2.save(f"{OUT}/{name}/crop_render.png")
    oc2.save(f"{OUT}/{name}/crop_original.png")
    print(name, "render", rc2.size, "orig", oc2.size)
