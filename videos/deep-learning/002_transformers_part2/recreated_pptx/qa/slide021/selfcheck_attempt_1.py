#!/usr/bin/env python3
"""selfcheck attempt 1 — slide 021 closed-loop ink check (150dpi render vs original).
Expected bboxes derive from the original-frame measurements (measure4-7) through the
mapping RX(fx)=(fx-18.13)*150/72/0.961231, RY(fy)=fy*150/72/0.955556. Tolerance ~4px.
"""
import json
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide021/render_1.png"
img = Image.open(R).convert("RGB")
A = np.asarray(img).astype(int)
H, W = A.shape[:2]
KX = 150 / 72 / 0.961231
KY = 150 / 72 / 0.955556
RX = lambda fx: (fx - 18.13) * KX
RY = lambda fy: fy * KY

def ink_bbox(x0, x1, y0, y1, fn):
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    sub = A[y0:y1, x0:x1]
    m = fn(sub)
    if m.sum() < 4:
        return None
    ys, xs = np.where(m)
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max()), int(m.sum())]

F = {
    "title_red":   lambda p: (p[..., 0] > 120) & (p[..., 0] - p[..., 1] > 80) & (p[..., 0] - p[..., 2] > 60),
    "title_blue":  lambda p: (p[..., 2] - p[..., 0] > 80) & (p[..., 2] > 110) & (p[..., 0] < 90),
    "dbox":        lambda p: (p[..., 2] - p[..., 0] > 45) & (p[..., 2] > 90) & (p[..., 2] < 190) & (p[..., 0] < 110),
    "lane1_border":lambda p: (p[..., 2] - p[..., 0] > 25) & (p[..., 0] < 110) & (p[..., 2] > 60) & (p[..., 2] < 160),
    "lane1_fill":  lambda p: (p[..., 2] - p[..., 0] > 28) & (p[..., 0] > 180) & (p[..., 0] < 220) & (p[..., 2] > 230),
    "digit":       lambda p: (p[..., 2] - p[..., 0] > 50) & (p[..., 0] < 100) & (p[..., 2] > 100),
    "dot":         lambda p: (np.abs(p[..., 0] - 122) < 28) & (np.abs(p[..., 2] - 192) < 28) & (p[..., 2] - p[..., 0] > 40),
    "arrow":       lambda p: (p[..., 0] > 190) & (p[..., 1] < 70) & (p[..., 2] < 70),
    "navy":        lambda p: (p[..., 2] > 130) & (p[..., 0] < 45) & (p[..., 1] < 45),
    "yel":         lambda p: (p[..., 0] > 225) & (p[..., 1] > 225) & (p[..., 2] < 80),
    "wht":         lambda p: (p[..., 0] > 225) & (p[..., 1] > 225) & (p[..., 2] > 225),
    "lane3_fill":  lambda p: (p[..., 1] > 240) & (p[..., 0] > 220) & (p[..., 0] < 245) & (p[..., 2] > 195) & (p[..., 2] < 230),
    "vbox_border": lambda p: (np.abs(p[..., 0] - 209) < 22) & (np.abs(p[..., 1] - 203) < 22) & (np.abs(p[..., 2] - 170) < 22),
    "vector":      lambda p: (p[..., 0] < 45) & (p[..., 2] > 70) & (p[..., 2] < 130) & (p[..., 2] - p[..., 0] > 40),
    "sub":         lambda p: (p[..., 0] > 150) & (p[..., 1] < 60) & (p[..., 2] < 60),
    "brace":       lambda p: (np.abs(p[..., 0] - 139) < 30) & (p[..., 1] < 70) & (p[..., 2] < 80),
    "tan":         lambda p: (np.abs(p[..., 0] - 212) < 18) & (np.abs(p[..., 1] - 200) < 18) & (np.abs(p[..., 2] - 168) < 20),
    "ybox_fill":   lambda p: (p[..., 0] > 240) & (p[..., 1] > 240) & (p[..., 2] > 210) & (p[..., 2] < 235),
    "ybox_border": lambda p: (np.abs(p[..., 0] - 220) < 18) & (np.abs(p[..., 1] - 208) < 18) & (np.abs(p[..., 2] - 180) < 20),
    "gbox_border": lambda p: (np.abs(p[..., 0] - 71) < 30) & (np.abs(p[..., 1] - 131) < 30) & (np.abs(p[..., 2] - 69) < 30),
    "black":       lambda p: (p[..., 0] < 60) & (p[..., 1] < 60) & (p[..., 2] < 60),
    "lab_blue":    lambda p: (p[..., 2] - p[..., 0] > 50) & (p[..., 0] < 90) & (p[..., 2] > 90),
    "lab_red":     lambda p: (p[..., 0] > 150) & (p[..., 1] < 60) & (p[..., 2] < 60),
}

# (name, filter, expected frame bbox [x0,y0,x1,y1], search window padding px)
CHECKS = [
    ("title_red",    "title_red",    [274, 60, 477, 96], 30),
    ("title_blue",   "title_blue",   [493, 60, 662, 96], 30),
    ("dbox_top",     "dbox",         [200, 111, 800, 111], 6),
    ("dbox_bot",     "dbox",         [200, 356.5, 800, 356.5], 6),
    ("dbox_left",    "dbox",         [74, 200, 74, 330], 6),
    ("dbox_right",   "dbox",         [892.5, 200, 892.5, 330], 6),
    ("lane1_top",    "lane1_border", [300, 136, 800, 136.5], 6),
    ("lane1_bot",    "lane1_border", [300, 174.5, 800, 175], 6),
    ("lane1_left",   "lane1_border", [163.5, 147, 164.5, 162], 8),
    ("lane1_fill",   "lane1_fill",   [620, 150, 720, 164], 10),
    ("r1_box1",      "lane1_border", [177, 143.5, 236, 165.5], 8),
    ("r1_box8",      "lane1_border", [808, 143.5, 872, 165.5], 8),
    ("r1_digit0",    "digit",        [200, 149, 220, 161], 10),
    ("r1_digits",    "digit",        [195, 149, 216, 161], 10),
    ("dots",         "dot",          [631.5, 151.5, 709.5, 160.5], 10),
    ("arr1",         "arrow",        [517, 176, 528, 213.5], 8),
    ("arr2",         "arrow",        [516, 252, 527, 289.5], 8),
    ("navy",         "navy",         [165, 214.5, 892, 251.5], 8),
    ("navy_yel",     "yel",          [286, 226, 373, 240], 14),
    ("navy_wht",     "wht",          [383, 228, 769, 244], 14),
    ("lane3_top",    "lane3_fill",   [300, 295, 800, 297], 8),
    ("lane3_fill",   "lane3_fill",   [620, 300, 720, 318], 10),
    ("vbox1",        "vbox_border",  [175.5, 299.5, 236.5, 321.5], 8),
    ("vbox8",        "vbox_border",  [807, 299.5, 871.5, 321.5], 8),
    ("vector1_ink",  "vector",       [185, 304, 221, 313], 12),
    ("sub1_ink",     "sub",          [207, 312, 228, 319], 12),
    ("brace",        "brace",        [176, 336, 866, 351.5], 10),
    ("tan_line",     "tan",          [302, 251, 324, 380], 12),
    ("ybox",         "ybox_border",  [74, 380.5, 266, 495.5], 8),
    ("ybox_L1",      "lab_blue",     [84, 397, 199, 411], 12),
    ("ybox_L4",      "lab_blue",     [85, 468, 242, 478], 12),
    ("gbox_top",     "gbox_border",  [400, 371, 700, 372], 8),
    ("gbox_G1",      "black",        [340, 381, 733, 397], 14),
    ("gbox_G3",      "black",        [349, 445, 722, 462], 14),
    ("lab_blue",     "lab_blue",     [83, 141, 156, 171], 12),
    ("lab_red",      "lab_red",      [83, 220, 148, 247], 12),
]

res = {}
fails = []
for name, fk, bb, pad in CHECKS:
    x0, y0, x1, y1 = bb
    win = [RX(x0) - pad, RY(y0) - pad, RX(x1) + pad, RY(y1) + pad]
    got = ink_bbox(win[0], win[2], win[1], win[3], F[fk])
    exp = [RX(x0), RY(y0), RX(x1), RY(y1)]
    if got is None:
        res[name] = {"exp": [round(v, 1) for v in exp], "got": None, "ok": False}
        fails.append(name)
        continue
    d = [got[i] - exp[i] for i in range(4)]
    ok = all(abs(v) <= 4.5 for v in d[:2]) and all(abs(v) <= 4.5 for v in d[2:])
    res[name] = {"exp": [round(v, 1) for v in exp], "got": got, "d": [round(v, 1) for v in d], "ok": ok}
    if not ok:
        fails.append(name)

# text width tuning targets (render px)
tw = {}
for nm, fk, bb in [("navy_yel_w", "yel", [286, 226, 373, 240]), ("navy_wht_w", "wht", [383, 228, 769, 244]),
                   ("gbox_G1_w", "black", [340, 381, 733, 397]), ("ybox_L4_w", "lab_blue", [85, 468, 242, 478]),
                   ("vector1_w", "vector", [185, 304, 221, 313])]:
    x0, y0, x1, y1 = bb
    got = ink_bbox(RX(x0) - 16, RX(x1) + 16, RY(y0) - 8, RY(y1) + 8, F[fk])
    tw[nm] = {"target_w": round(RX(x1) - RX(x0), 1), "got_w": (got[2] - got[0]) if got else None}

print(json.dumps({"fails": fails, "checks": res, "widths": tw}, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide021/selfcheck_attempt_1_output.txt", "w") as f:
    f.write(json.dumps({"fails": fails, "checks": res, "widths": tw}, indent=1))
