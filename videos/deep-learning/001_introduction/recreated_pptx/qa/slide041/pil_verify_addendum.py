#!/usr/bin/env python3
"""PIL verification of the worker_report.md addendum claim (slide 041, 001_introduction).

Claim under test:
  L1 span `(x,y)`  frame x177..212, y386..406  -> BLACK (modal (0,0,0), n=184); red `I` stem x165..167
  L2 span `(-a:a , -b:b)` frame x183..276, y413..429 -> BLACK (modal (0,0,0), n=370);
     ZERO red pixels anywhere in x175..309 of that band.
  Certified render draws both spans solid C00000 (render region x183..276: 1,340 pure-red px, 0 dark).
Controls (far side): `a=1,b=1` red text x239..264 y334..359 (frame says RED), `Filter:`/`Image:` black prefixes.
"""
from collections import Counter
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_041.jpg").convert("RGB")).astype(int)
rend = np.asarray(Image.open(f"{VID}/recreated_pptx/qa/slide041/render_1.png").convert("RGB")).astype(int)
SCALE = rend.shape[0] / 540.0  # render px per frame px


def census(im, x0, x1, y0, y1, tag):
    """Ink census in a frame-scale region (works for both frame and scaled render)."""
    reg = im[int(y0):int(y1), int(x0):int(x1)]
    dark = (reg.max(axis=2) < 100)
    red = (reg[:, :, 0] >= 120) & (reg[:, :, 1] <= 90) & (reg[:, :, 2] <= 90)
    ink = dark | red
    modal = Counter(map(tuple, reg[ink])) if ink.any() else {}
    m = modal.most_common(1)[0] if modal else (None, 0)
    print(f"{tag:44s} region x[{x0:.0f}..{x1:.0f}] y[{y0:.0f}..{y1:.0f}]  "
          f"dark={dark.sum():5d}  red={red.sum():5d}  modal={m[0]} n={m[1]}")
    return dark.sum(), red.sum(), m


print(f"render size {rend.shape[1]}x{rend.shape[0]}  scale render/frame = {SCALE:.5f}")
print("\n=== FRAME (ground truth) — claimed spans ===")
census(frame, 177, 212, 386, 406, "FRAME L1 '(x,y)' x177..212 y386..406")
census(frame, 165, 168, 386, 406, "FRAME L1 'I' stem x165..167 y386..406")
census(frame, 183, 276, 413, 429, "FRAME L2 '(-a:a , -b:b)' x183..276 y413..429")
census(frame, 175, 309, 413, 429, "FRAME L2 zero-red band x175..309 y413..429")
print("\n=== FRAME — wider context census (find h / Filter: colors) ===")
census(frame, 92, 160, 413, 429, "FRAME L2 'Filter:' zone x92..160")
census(frame, 160, 183, 413, 429, "FRAME L2 'h' zone x160..183")
census(frame, 276, 404, 413, 429, "FRAME L2 '(odd dimension)' zone x276..404")
census(frame, 92, 163, 386, 406, "FRAME L1 'Image:' zone x92..163")
census(frame, 168, 177, 386, 406, "FRAME L1 gap I..(x,y) x168..177")
print("\n=== FRAME — controls (method sanity) ===")
census(frame, 239, 264, 334, 359, "CTRL frame 'a=1,b=1' x239..264 y334..359 (expect RED)")
census(frame, 459, 842, 363, 419, "CTRL frame equation x459..842 y363..419 (expect BLACK)")
print("\n=== CERTIFIED RENDER — same frame-scale regions ===")
census(rend, 177 * SCALE, 212 * SCALE, 386 * SCALE, 406 * SCALE, "RENDER L1 '(x,y)' region")
census(rend, 165 * SCALE, 168 * SCALE, 386 * SCALE, 406 * SCALE, "RENDER L1 'I' stem region")
census(rend, 183 * SCALE, 276 * SCALE, 413 * SCALE, 429 * SCALE, "RENDER L2 '(-a:a , -b:b)' region")
census(rend, 175 * SCALE, 309 * SCALE, 413 * SCALE, 429 * SCALE, "RENDER L2 band x175..309")
census(rend, 160 * SCALE, 183 * SCALE, 413 * SCALE, 429 * SCALE, "RENDER L2 'h' zone")
print("\n=== COLUMN PROFILE of frame L1/L2 bands (which x-columns hold red vs dark ink) ===")
for (x0, x1, y0, y1, tag) in [(92, 320, 386, 406, "L1 band"), (92, 320, 413, 429, "L2 band")]:
    reg = frame[y0:y1, x0:x1]
    dark = (reg.max(axis=2) < 100)
    red = (reg[:, :, 0] >= 120) & (reg[:, :, 1] <= 90) & (reg[:, :, 2] <= 90)
    dcols = [x0 + i for i in range(reg.shape[1]) if dark[:, i].any()]
    rcols = [x0 + i for i in range(reg.shape[1]) if red[:, i].any()]
    def runs(c):
        out, s, p = [], None, None
        for i in c:
            if s is None: s = p = i
            elif i == p + 1: p = i
            else: out.append((s, p)); s = p = i
        if s is not None: out.append((s, p))
        return out
    print(f"{tag}: dark col runs={runs(dcols)}")
    print(f"{tag}: red  col runs={runs(rcols)}")
