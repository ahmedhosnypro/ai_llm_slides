#!/usr/bin/env python3
"""selfcheck_attempt_3 — word-run diagnostics: for each text line, print column runs
in RENDER and (precomputed) FRAME, so ems/positions can be fitted exactly."""
import json
from PIL import Image
import numpy as np

REND = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide022/render_1.png"
K = 150.0 / 72.0
AX, SX, SY = 17.72, 0.961231, 0.955556
def RX(fx): return (fx - AX) / SX * K
def RY(fy): return fy / SY * K
def IX(rx): return rx / K * SX + AX  # render px -> frame px

img = Image.open(REND).convert("RGB")
A = np.asarray(img).astype(int)
R, Gc, B = A[..., 0], A[..., 1], A[..., 2]
res = {}

def runs_of(mask2d, ox, mingap=6, minw=2):
    colc = mask2d.sum(axis=0)
    on = colc > 0
    out, s = [], None
    for i, v in enumerate(on):
        if v and s is None: s = i
        elif not v and s is not None:
            out.append([ox + s, ox + i - 1]); s = None
    if s is not None: out.append([ox + s, len(on) - 1 + ox])
    # merge runs separated by < mingap
    merged = []
    for r in out:
        if merged and r[0] - merged[-1][1] <= mingap: merged[-1][1] = r[1]
        else: merged.append(r)
    return [r for r in merged if r[1] - r[0] >= minw]

def wordruns(mask, y0, y1, x0, x1, mingap=6):
    sub = mask[y0:y1, x0:x1]
    rr = runs_of(sub, x0, mingap)
    # frame-space equivalents
    return [[int(IX(r[0])), int(IX(r[1]))] for r in rr], rr

dk = (A.sum(axis=2) < 460)
blum = (B - R > 45) & (B > 90)
redm = (R > 100) & (R - Gc > 35) & (R - B > 30)

# subtitle (blue) rows 180-240, x 600-1840
fr, px = wordruns(blum, 182, 236, 600, 1840)
res["sub_words_frame"] = fr
# line1 (dark) rows 795-838, x 115-1878
fr, px = wordruns(dk, int(RY(365)), int(RY(384)), 115, 1878, mingap=9)
res["line1_words_frame"] = fr
# problems (red) rows 845-880
fr, px = wordruns(redm, int(RY(387)), int(RY(404)), 115, 700)
res["problems_words_frame"] = fr
# b1a rows 888-935 (exclude dot zone x<160 for text runs)
fr, px = wordruns(dk, int(RY(409)), int(RY(428)), 160, 1878, mingap=9)
res["b1a_words_frame"] = fr
fr, px = wordruns(dk, int(RY(431)), int(RY(450)), 160, 900)
res["b1b_words_frame"] = fr
fr, px = wordruns(dk, int(RY(452)), int(RY(471)), 160, 1878, mingap=9)
res["b2_words_frame"] = fr
fr, px = wordruns(dk, int(RY(473)), int(RY(493)), 160, 1700, mingap=9)
res["b3_words_frame"] = fr
# labels
gm = (abs(R - Gc) < 20) & (abs(Gc - B) < 20) & (A.sum(axis=2) < 480)
fr, px = wordruns(gm, int(RY(112)), int(RY(161)), 120, 340, mingap=8)
res["lab1_words_frame"] = fr
fr, px = wordruns(blum, int(RY(190)), int(RY(226)), 120, 340, mingap=8)
res["lab2_words_frame"] = fr
fr, px = wordruns(redm, int(RY(260)), int(RY(297)), 120, 340, mingap=8)
res["lab3_words_frame"] = fr
# title
fr, px = wordruns(redm, 122, 182, 600, 1900, mingap=10)
res["title_words_frame"] = fr

# vertical: cap tops per band (row profiles)
def rowprof(mask, y0, y1, x0, x1):
    sub = mask[y0:y1, x0:x1]
    rc = sub.sum(axis=1)
    rows = [y0 + i for i in range(len(rc)) if rc[i] > 2]
    return [rows[0], rows[-1]] if rows else None
res["vp_sub"] = rowprof(blum, 175, 245, 600, 1500)
res["vp_line1"] = rowprof(dk, int(RY(363)), int(RY(386)), 130, 1700)
res["vp_problems"] = rowprof(redm, int(RY(386)), int(RY(406)), 130, 500)
res["vp_b1a"] = rowprof(dk, int(RY(408)), int(RY(429)), 170, 1700)
res["vp_b1b"] = rowprof(dk, int(RY(430)), int(RY(451)), 170, 700)
res["vp_b2"] = rowprof(dk, int(RY(452)), int(RY(472)), 170, 1700)
res["vp_b3"] = rowprof(dk, int(RY(473)), int(RY(494)), 170, 1500)
res["vp_lab1"] = rowprof(gm, int(RY(110)), int(RY(162)), 130, 330)
res["vp_lab2"] = rowprof(blum, int(RY(188)), int(RY(228)), 130, 330)
res["vp_lab3"] = rowprof(redm, int(RY(258)), int(RY(298)), 130, 330)
res["vp_delta1"] = rowprof((R - B > 55) & (R > 110) & (R < 200) & (Gc < 110), int(RY(312)), int(RY(332)), int(RX(219)), int(RX(234)))
res["vp_title"] = rowprof(redm, 118, 190, 700, 1500)

print(json.dumps(res, indent=1, default=str))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide022/selfcheck_attempt_3_output.txt", "w") as f:
    f.write(json.dumps(res, indent=1, default=str))
