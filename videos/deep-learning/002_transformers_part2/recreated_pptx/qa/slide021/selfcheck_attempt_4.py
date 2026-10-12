#!/usr/bin/env python3
"""selfcheck attempt 2 — cleaned windows/filters (no cross-line contamination)."""
import json
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide021/render_4.png"
A = np.asarray(Image.open(R).convert("RGB")).astype(int)
KX = 150 / 72 / 0.961231
KY = 150 / 72 / 0.955556
RX = lambda fx: (fx - 18.13) * KX
RY = lambda fy: fy * KY

def bbox(x0, x1, y0, y1, fn, minc=4):
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    sub = A[y0:y1, x0:x1]
    m = fn(sub)
    if m.sum() < minc:
        return None
    ys, xs = np.where(m)
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(m.sum())]

F = {
    "red":    lambda p: (p[..., 0] > 120) & (p[..., 0] - p[..., 1] > 80) & (p[..., 0] - p[..., 2] > 60),
    "blue":   lambda p: (p[..., 2] - p[..., 0] > 80) & (p[..., 2] > 110) & (p[..., 0] < 90),
    "blk":    lambda p: (p[..., 0] < 60) & (p[..., 1] < 60) & (p[..., 2] < 60),
    "yel":    lambda p: (p[..., 0] > 225) & (p[..., 1] > 225) & (p[..., 2] < 80),
    "wht":    lambda p: (p[..., 0] > 225) & (p[..., 1] > 225) & (p[..., 2] > 225),
    "dig":    lambda p: (p[..., 2] - p[..., 0] > 50) & (p[..., 0] < 100) & (p[..., 2] > 100),
    "vec":    lambda p: (p[..., 0] < 60) & (p[..., 2] > 70) & (p[..., 2] < 150) & (p[..., 2] - p[..., 0] > 35),
    "labblu": lambda p: (p[..., 2] - p[..., 0] > 50) & (p[..., 0] < 110) & (p[..., 2] > 90),
    "labblu2": lambda p: ((p[..., 2] - p[..., 0] > 50) & (p[..., 0] < 110) & (p[..., 2] > 90)) | ((p[..., 0] > 140) & (p[..., 1] < 70) & (p[..., 2] < 70)),
    "labred": lambda p: (p[..., 0] > 150) & (p[..., 1] < 70) & (p[..., 2] < 70),
    "tan":    lambda p: (np.abs(p[..., 0] - 212) < 20) & (np.abs(p[..., 1] - 200) < 20) & (np.abs(p[..., 2] - 168) < 22),
}
CHECKS = [
    # name, filter, window (frame x0,x1, render y0,y1), expected frame bbox
    ("t_red",  "red",  (250, 490, 118, 222), [274, 60, 477, 96]),
    ("t_blue", "blue", (480, 690, 118, 222), [493, 60, 662, 96]),
    ("navy_yel", "yel", (270, 390, 480, 540), [286, 226, 373, 240]),
    ("navy_wht", "wht", (378, 800, 480, 545), [383, 228, 769, 244]),
    ("gbox_G1", "blk", (325, 750, 822, 872), [340, 381, 733, 397]),
    ("gbox_G2", "blk", (325, 750, 874, 928), [422, 402, 650, 419]),
    ("gbox_G3", "blk", (325, 750, 960, 1012), [349, 445, 722, 462]),
    ("ybox_L1", "labblu2", (78, 215, 858, 902), [84, 398.5, 199, 411]),
    ("ybox_L2", "labblu2", (78, 220, 904, 940), [84, 417.5, 209, 426]),
    ("ybox_L3", "labblu2", (78, 210, 976, 1016), [84, 451.5, 199, 464]),
    ("ybox_L4", "labblu2", (78, 262, 1014, 1050), [84, 468, 257, 478]),
    ("lab_blue", "labblu", (77, 160, 300, 378), [83, 141, 156, 167]),
    ("lab_red", "labred", (77, 160, 470, 545), [83, 220, 148, 247]),
    ("vec1", "vec", (176, 240, 655, 690), [185, 304, 221, 313]),
    ("dig0", "dig", (196, 226, 320, 356), [206, 150, 214, 160]),
]
out, fails = {}, []
for name, fk, (fx0, fx1, ry0, ry1), bb in CHECKS:
    got = bbox(RX(fx0), RX(fx1), ry0, ry1, F[fk])
    exp = [RX(bb[0]), RY(bb[1]), RX(bb[2]), RY(bb[3])]
    if got is None:
        out[name] = {"exp": [round(v, 1) for v in exp], "got": None}
        fails.append(name)
        continue
    d = [round(got[i] - exp[i], 1) for i in range(4)]
    ok = abs(d[0]) <= 4.5 and abs(d[1]) <= 4.5 and abs(d[2]) <= 4.5 and abs(d[3]) <= 5.5
    out[name] = {"exp": [round(v, 1) for v in exp], "got": got[:4], "d": d, "ok": ok}
    if not ok:
        fails.append(name)
# tan line: trace columns (rows 570..820 only, away from bar edge)
sub = A[570:820, 590:690]
m = F["tan"](sub)
cols = np.where(m.sum(axis=0) > 8)[0]
out["tan_cols"] = [590 + int(cols.min()), 590 + int(cols.max())] if len(cols) else None
out["tan_exp"] = [round(RX(302), 1), round(RX(324), 1)]
if out["tan_cols"] and (out["tan_cols"][0] < RX(302) - 6 or out["tan_cols"][1] > RX(324) + 6):
    fails.append("tan_line")
print(json.dumps({"fails": fails, "checks": out}, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide021/selfcheck_attempt_4_output.txt", "w") as f:
    f.write(json.dumps({"fails": fails, "checks": out}, indent=1))
