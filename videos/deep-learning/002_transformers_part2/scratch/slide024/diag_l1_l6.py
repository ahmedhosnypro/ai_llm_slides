#!/usr/bin/env python3
"""Diagnose L1 (too narrow?) and L6 (too wide?) in render_1.png: word runs + right-end ASCII."""
import numpy as np
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
rend = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide024/render_1.png").convert("RGB")).astype(int)
PXPT = 150 / 72.0
def R(pt): return int(round(pt * PXPT))

r_, g_, b_ = rend[..., 0], rend[..., 1], rend[..., 2]
inkm = ((b_ > 100) & (b_ > r_ + 30)) | ((r_ > 110) & (r_ > b_ + 40) & (g_ < r_ - 30))

def word_runs(py0, py1, px0, px1, gap=5):
    reg = inkm[py0:py1, px0:px1]
    prof = reg.any(axis=0)
    d = np.diff(np.concatenate(([0], prof.astype(int), [0])))
    st = np.where(d == 1)[0]; en = np.where(d == -1)[0]
    runs = []
    for s_, e_ in zip(st, en):
        if runs and s_ - runs[-1][1] <= gap: runs[-1][1] = e_
        else: runs.append([s_, e_])
    return [((s_ + px0) / PXPT, (e_ + px0) / PXPT) for s_, e_ in runs]

print("L1 words (render):", [(round(a,1), round(b_,1)) for a, b_ in word_runs(R(385), R(401), R(58), R(660))])
print("L1 words (frame target): [63.8..85.8][100.4..111.7][116..162][167.1..224.5][229.7..249.5][255.8..299.6][305.8..325.6][330.9..370.5][375.7..451.8][457..486.2][492.5..531.1][536.3..612.4]")
print()
print("L6 words (render):", [(round(a,1), round(b_,1)) for a, b_ in word_runs(R(496), R(512), R(94), R(760))])
print("L6 words (frame target): [99.2..117][123..164]...[99.2..683.9 total]")
print()
# ASCII of L1 right end (frame x slide 560..640, render rows around baseline)
py0, py1 = R(382), R(404)
px0, px1 = R(555), R(640)
print(f"L1 right end ASCII (slide x 555..640, y 382..404):")
reg = inkm[py0:py1, px0:px1]
for yy in range(reg.shape[0]):
    print(f"{382+yy*72/150:.0f} " + "".join("#" if reg[yy, xx] else "." for xx in range(reg.shape[1])))
