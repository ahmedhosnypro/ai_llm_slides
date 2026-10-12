#!/usr/bin/env python3
"""Fit frame->slide mapping (frame = A + s*slide) by minimizing mean abs diff
against 001 slide 43's certified render (2001x1125 @150dpi). Resumes 017 worker."""
from PIL import Image
import numpy as np

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png").convert("RGB")
a = np.asarray(F).astype(np.int16)   # 540x960
b = np.asarray(R).astype(np.int16)   # 1125x2001
FH, FW = a.shape[:2]
RH, RW = b.shape[:2]
KX = RW / 960.0
KY = RH / 540.0

# subsample frame for speed
SY_STEP, SX_STEP = 2, 2
fy, fx = np.mgrid[0:FH:SY_STEP, 0:FW:SX_STEP]
af = a[::SY_STEP, ::SX_STEP]

def score(AX, SX, AY, SYy):
    sx = (fx - AX) / SX
    sy = (fy - AY) / SYy
    valid = (sx >= 0) & (sx <= 959.4) & (sy >= 0) & (sy <= 539.4)
    rx = np.clip((sx * KX).astype(np.int32), 0, RW - 1)
    ry = np.clip((sy * KY).astype(np.int32), 0, RH - 1)
    d = np.abs(af - b[ry, rx]).sum(axis=2)
    return d[valid].mean(), valid.sum()

best = None
# stage 1: y params (x fixed at landmark fit)
for AY in np.arange(-3.0, 5.01, 0.5):
    for SYy in np.arange(0.948, 0.967, 0.002):
        m, n = score(17.6, 0.9610, AY, SYy)
        if best is None or m < best[0]:
            best = (m, 17.6, 0.9610, AY, SYy)
print("stage1 best: mean=%.2f AX=%.2f SX=%.4f AY=%.2f SY=%.4f" % best)
# stage 2: x params
m0, AX0, SX0, AY0, SY0 = best
for AX in np.arange(15.5, 20.01, 0.25):
    for SX in np.arange(0.956, 0.966, 0.0005):
        m, n = score(AX, SX, AY0, SY0)
        if m < best[0]:
            best = (m, AX, SX, AY0, SY0)
print("stage2 best: mean=%.2f AX=%.2f SX=%.4f AY=%.2f SY=%.4f" % best)
# stage 3: fine joint refine
m0, AX0, SX0, AY0, SY0 = best
for AX in np.arange(AX0 - 0.4, AX0 + 0.41, 0.1):
    for SX in np.arange(SX0 - 0.001, SX0 + 0.0011, 0.00025):
        for AY in np.arange(AY0 - 0.6, AY0 + 0.61, 0.15):
            for SYy in np.arange(SY0 - 0.002, SY0 + 0.0021, 0.0005):
                m, n = score(AX, SX, AY, SYy)
                if m < best[0]:
                    best = (m, AX, SX, AY, SYy)
print("FINAL: mean=%.3f  AX=%.3f SX=%.5f AY=%.3f SY=%.5f  (n=%d)" % (best[0], best[1], best[2], best[3], best[4], best[5]))
