#!/usr/bin/env python3
"""ASCII crops of render_1.png at the two underlined lines + band tops, frame coords."""
from PIL import Image
import numpy as np

a = np.asarray(Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide049/render_1.png").convert("RGB")).astype(int)
S = a.shape[0] / 540.0

def crop(y0, y1, x0, x1, tag, thr=560):
    r0, r1, c0, c1 = int(y0*S), int(y1*S), int(x0*S), int(x1*S)
    sub = a[r0:r1, c0:c1]
    d = sub.sum(axis=2) < thr
    print(f"--- {tag} frame y{y0}..{y1} x{x0}..{x1} (render rows {r0}..{r1}) ---")
    for i, row in enumerate(d):
        fr = y0 + i/S
        print(f"{fr:6.1f} " + "".join("#" if v else "." for v in row[::2]))  # every 2nd render px ~ frame px

crop(213, 232, 440, 710, "render band1 underline region")
crop(322, 340, 130, 480, "render band4 underline region")
crop(156, 168, 140, 220, "render band0 cap-top region")
