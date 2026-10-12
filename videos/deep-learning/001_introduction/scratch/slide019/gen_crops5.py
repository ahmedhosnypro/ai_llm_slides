#!/usr/bin/env python3
"""Dense-region crop pairs (render_5 vs original) for pre-judge crop comparisons.
Regions upscaled so the vision model sees them at legible resolution."""
from PIL import Image
import os
B = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
Q = f"{B}/recreated_pptx/qa/slide019/crops_attempt_5"
os.makedirs(Q, exist_ok=True)
ren = Image.open(f"{B}/recreated_pptx/qa/slide019/render_5.png").convert("RGB")
ori = Image.open(f"{B}/unique_slides/slide_019.jpg").convert("RGB")
S = ren.size[0] / 960.0  # render scale vs frame px

def pair(name, x0, y0, x1, y1, up):
    rb = ren.crop((int(x0 * S), int(y0 * S), int(x1 * S), int(y1 * S)))
    ob = ori.crop((x0, y0, x1, y1))
    rb = rb.resize((rb.size[0] * up, rb.size[1] * up), Image.LANCZOS)
    ob = ob.resize((ob.size[0] * up, ob.size[1] * up), Image.LANCZOS)
    rb.save(f"{Q}/{name}_render.png"); ob.save(f"{Q}/{name}_original.png")
    print(name, "render", rb.size, "original", ob.size)

pair("verr", 735, 158, 818, 312, 3)     # Prediction Error vertical box + rotated 7pt text
pair("pencil", 230, 192, 300, 248, 4)   # pencil glyph in Pre processing top-right
pair("chain_left", 70, 188, 300, 282, 2)  # Input Samples + Pre processing + arrow + container left
