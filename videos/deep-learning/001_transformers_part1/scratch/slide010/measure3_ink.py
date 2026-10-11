#!/usr/bin/env python3
"""Pass 3 (slide010): ink-component probes in named windows.

Ink = dark (r+g+b<560) or saturated-red/pink. Reports connected bboxes per
window so labels/arrows/curves can be pinned. Frame px (960x540).
"""
from PIL import Image
import numpy as np
from scipy import ndimage

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_010.jpg"
a = np.asarray(Image.open(IM).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

dark = (r + g + b) < 560
redish = (r > 110) & (g < 110) & (b < 110)                      # C00000 family ink
pinkish = (r > 200) & (g > 90) & (g < 200) & (b > 120) & (b < 230)  # FF80C0 family

def comps(mask, x0, y0, x1, y1, min_area=12, top=30, label=""):
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
    # merge into line clusters for readability
    print(f"-- {label} ({x0},{y0})-({x1},{y1}): {len(out)} comps")
    for area, cx0, cy0, cx1, cy1 in out[:top]:
        print(f"   area={area:5d} x{cx0}..{cx1} y{cy0}..{cy1} (w{cx1-cx0+1} h{cy1-cy0+1})")
    return out

print("========== TITLE / SUBTITLE ==========")
comps(dark | redish, 200, 50, 760, 84, 8, 40, "title line1 ink (y50..84)")
comps(dark | redish, 200, 84, 760, 112, 8, 40, "subtitle ink (y84..112)")

print("========== DECODER ==========")
comps(dark, 480, 112, 910, 152, 6, 40, "o labels band y112..152")
comps(dark, 480, 152, 910, 200, 6, 40, "up-arrow band y152..200")
comps(dark, 480, 160, 910, 195, 4, 40, "softmax band y160..195")
comps(dark, 480, 217, 910, 256, 6, 40, "down-arrows band y217..256")
comps(dark, 480, 240, 910, 300, 6, 40, "s-arrows/slabels band y240..300")
comps(redish, 480, 240, 560, 290, 4, 20, "dec dot red y240..290 x480..560")

print("========== ENCODER ==========")
comps(dark, 44, 296, 495, 340, 6, 40, "h labels + h-arrows band y296..340")
comps(dark, 44, 340, 495, 415, 6, 40, "emb arrows + labels y340..415")
comps(dark, 44, 415, 495, 440, 6, 40, "enc bottom cells edge y415..440")
comps(dark, 44, 440, 495, 500, 6, 40, "x-arrows + x labels y440..500")
comps(redish, 430, 300, 500, 350, 4, 20, "enc dot red x430..500 y300..350")
comps(dark, 44, 495, 495, 535, 6, 30, "Encoder caption y495..535")

print("========== DECODER caption ==========")
comps(dark | redish, 480, 82, 910, 115, 6, 30, "Decoder caption y82..115")

print("========== ATTENTION ==========")
comps(dark, 100, 225, 480, 305, 6, 40, "left box: node text + inner lines y225..305")
comps(dark, 100, 200, 480, 240, 6, 30, "left Attention caption y200..240")
comps(dark, 480, 340, 910, 375, 6, 30, "right Attention caption y340..375")

print("========== CALLOUTS ==========")
comps(dark, 60, 140, 360, 195, 6, 30, "green callout text y140..195")
comps(dark | redish, 550, 368, 850, 415, 6, 30, "pink callout text y368..415")
comps(dark | redish, 510, 425, 910, 535, 6, 40, "gray summary text y425..535")

print("========== RED / PINK INK GLOBAL (arcs, dots, dashed curves) ==========")
comps(redish, 430, 240, 560, 350, 4, 30, "red ink center (arc+dots) x430..560 y240..350")
comps(pinkish, 460, 270, 920, 430, 6, 40, "pink ink middle x460..920 y270..430")
comps(pinkish, 100, 230, 500, 320, 6, 20, "pink ink left x100..500 y230..320")
