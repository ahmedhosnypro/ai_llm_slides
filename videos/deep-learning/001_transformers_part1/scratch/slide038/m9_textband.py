#!/usr/bin/env python3
"""m9: rotated-text band inside the Scaling box, both frames; also box top/bottom
edge rows at a clean column, and inner-rect edges."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
for tag, fn in [("37", "slide_037.jpg"), ("38", "slide_038.jpg")]:
    a = np.asarray(Image.open(f"{V}/unique_slides/{fn}").convert("RGB")).astype(int)
    R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    # orange text glyph pixels (E8890C family), inside box x376..414
    txt = (R > 170) & (R - B > 70) & (G < 185) & (G - B > 15) & (G < R - 30)
    m = np.zeros(txt.shape, bool); m[150:460, 376:415] = txt[150:460, 376:415]
    rows = m.sum(axis=1)
    bands = []
    inb = False
    for y in range(150, 460):
        if rows[y] > 2 and not inb:
            s = y; inb = True
        elif rows[y] <= 2 and inb:
            bands.append((s, y - 1)); inb = False
    print(f"{tag} text bands:", bands)
    # box top/bottom at column x395 (yellow run)
    yel = (R > 215) & (G > 200) & (B < 170) & (R - B > 60)
    col = np.where(yel[150:460, 395])[0] + 150
    print(f"{tag} yellow run at x395: y[{col.min()}..{col.max()}]" if len(col) else f"{tag}: no yellow at x395")
    col408 = np.where(yel[150:460, 408])[0] + 150
    print(f"{tag} yellow run at x408: y[{col408.min()}..{col408.max()}]" if len(col408) else f"{tag}: no yellow at x408")
    # box left/right edge at row y300 (avoid text? text is centered ~x386-404)
    yrow = np.where(yel[300, 350:470])[0] + 350
    print(f"{tag} yellow run at y300: x[{yrow.min()}..{yrow.max()}]" if len(yrow) else f"{tag}: no yellow at y300")
    # darker-yellow border (DDBA3C ~ (221,186,60)) columns
    bor = (np.abs(R - 221) < 45) & (np.abs(G - 186) < 45) & (B < 110)
    mb = np.zeros(bor.shape, bool); mb[150:460, 360:430] = bor[150:460, 360:430]
    cols = mb.sum(axis=0)
    print(f"{tag} border cols>25:", [(x + 360, int(c)) for x, c in enumerate(cols) if c > 25])
    brows = mb.sum(axis=1)
    print(f"{tag} border rows>25:", [(y + 150, int(c)) for y, c in enumerate(brows) if c > 25])
