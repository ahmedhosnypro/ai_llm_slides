#!/usr/bin/env python3
"""Pass 5 (slide010): parent-frame (slide_006.jpg) ink probes in the same windows
as measure3_ink.py, for block-by-block inherit/replace decisions."""
from PIL import Image
import numpy as np
from scipy import ndimage

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_006.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
dark = (r + g + b) < 560
redish = (r > 110) & (g < 110) & (b < 110)

def comps(mask, x0, y0, x1, y1, min_area=12, top=25, label=""):
    win = mask[y0:y1, x0:x1]
    lab, n = ndimage.label(win, structure=np.ones((3, 3)))
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        ys, xs = sl
        area = int((lab[sl] == i + 1).sum())
        if area < min_area:
            continue
        out.append((area, x0 + xs.start, y0 + ys.start, x0 + xs.stop - 1, y0 + ys.stop - 1))
    out.sort(reverse=True)
    print(f"-- {label}: {len(out)} comps")
    for area, cx0, cy0, cx1, cy1 in out[:top]:
        print(f"   area={area:5d} x{cx0}..{cx1} y{cy0}..{cy1} (w{cx1-cx0+1} h{cy1-cy0+1})")
    return out

print("== PARENT decoder ==")
comps(dark, 480, 112, 910, 152, 6, 15, "o labels y112..152")
comps(dark, 480, 152, 910, 200, 6, 15, "up-arrows y152..200")
comps(dark, 480, 217, 910, 256, 6, 15, "down-arrows y217..256")
comps(dark, 480, 240, 910, 300, 6, 15, "s band y240..300")
comps(redish, 480, 240, 560, 290, 4, 10, "dec dot red")
comps(redish, 430, 240, 560, 350, 4, 10, "arc region red x430..560 y240..350")
comps(dark, 480, 179, 910, 199, 4, 15, "curve tops y179..199")
print("== PARENT encoder ==")
comps(dark, 44, 296, 495, 340, 6, 15, "h labels/arrows y296..340")
comps(dark, 44, 340, 495, 415, 6, 15, "emb band y340..415")
comps(dark, 44, 440, 495, 500, 6, 15, "x band y440..500")
comps(redish, 430, 300, 500, 350, 4, 10, "enc dot red")
print("== PARENT captions/title ==")
comps(dark, 480, 82, 910, 115, 6, 15, "Decoder (RNN) caption")
comps(dark, 44, 495, 495, 535, 6, 15, "Encoder (RNN) caption")
comps(dark | redish, 200, 50, 760, 84, 8, 15, "title line1")
print("== PARENT callout/leader ==")
comps(dark, 550, 395, 850, 450, 6, 15, "callout y395..450")
comps(dark | redish, 460, 320, 570, 410, 4, 15, "leader line y320..410 x460..570")
