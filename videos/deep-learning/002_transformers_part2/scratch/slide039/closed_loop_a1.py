#!/usr/bin/env python3
"""CLOSED-LOOP attempt 1: compare render ink vs mapped original targets (150dpi render,
2001x1125 px; render_px = slide_pt * 2001/960 = *2.0844). Tolerance ~4px @150dpi."""
from PIL import Image
import json

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide039/slide-1.png"
img = Image.open(REN).convert("RGB")
W, H = img.size
px = img.load()
SC = W / 960.0  # render px per slide pt

def ink(p): return sum(p) < 640
def redp(p):
    r, g, b = p
    return r > 110 and r - g > 40 and r - b > 40
def bluep(p):
    r, g, b = p
    return b > 90 and b - r > 40 and b - g > 30
def darkp(p): return sum(p) < 300

def bbox(x0, x1, y0, y1, pred):
    pts = [(x, y) for y in range(int(y0), int(y1) + 1) for x in range(int(x0), int(x1) + 1) if pred(px[x, y])]
    if not pts: return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]

def S2R(x, y):  # slide pt -> render px
    return x * SC, y * SC

# targets: (id, pred, search window in slide pt, target bbox slide pt [x0,y0,x1,y1])
T = [
    ("title",     ink,  (300, 620, 45, 100),  [338.5, 60.7, 568.4, 87.9]),
    ("quoteL1",   bluep, (55, 900, 105, 137),  [64.9, 115.1, 878.4, 135.0]),
    ("covshift",  redp, (620, 900, 138, 159),  [697.4, 140.2, 858.7, 158.0]),
    ("f1l1",      redp, (95, 290, 180, 210),   [114.8, 190.5, 270.9, 205.1]),
    ("f1l2",      darkp, (95, 290, 212, 242),  [121.1, 224.0, 268.8, 238.6]),
    ("f2l1",      redp, (330, 580, 183, 209),  [347.9, 193.6, 557.0, 207.2]),
    ("f2l2",      redp, (330, 580, 210, 236),  [385.3, 220.8, 523.7, 234.4]),
    ("f3l1",      darkp, (615, 860, 183, 209), [662.0, 193.6, 817.0, 207.2]),
    ("f3l2",      redp, (615, 860, 210, 236),  [630.8, 220.8, 848.3, 234.4]),
    ("conclusion",redp, (60, 250, 258, 282),   [73.2, 264.8, 166.8, 277.3]),
    ("stmt1",     bluep, (140, 700, 282, 308), [152.3, 287.8, 643.3, 305.6]),
    ("idea",      redp, (60, 500, 322, 345),   [73.2, 327.6, 439.4, 341.2]),
    ("stmt2",     bluep, (140, 760, 346, 372), [153.3, 351.6, 720.3, 369.4]),
    ("lc_norm",   redp, (60, 210, 388, 410),   [73.2, 392.4, 202.2, 406.0]),
    ("lc_zero",   bluep, (440, 760, 388, 410), [466.5, 393.5, 718.2, 406.0]),
    ("sumhead",   redp, (60, 400, 434, 460),   [67.0, 439.5, 373.9, 456.3]),
    ("b1",        bluep, (80, 500, 460, 486),  [84.7, 464.6, 424.8, 482.4]),
    ("b2",        bluep, (80, 760, 482, 506),  [83.6, 484.5, 706.8, 503.4]),
]
res = {}
print(f"render {W}x{H}, scale {SC:.4f} render-px/slide-pt; tolerance ~4px @150dpi")
print(f"{'id':<11}{'dx0':>6}{'dy0':>6}{'dx1':>6}{'dy1':>6}  (render px; + = render right/below)")
for id_, pred, win, tgt in T:
    wx0, wx1 = S2R(win[0], win[1]); wy0, wy1 = S2R(win[2], win[3])
    b = bbox(wx0, wx1, wy0, wy1, pred)
    if b is None:
        print(f"{id_:<11} NO INK FOUND  <<<")
        res[id_] = None
        continue
    tx0, ty0 = S2R(tgt[0], tgt[1]); tx1, ty1 = S2R(tgt[2], tgt[3])
    d = [b[0] - tx0, b[1] - ty0, b[2] - tx1, b[3] - ty1]
    res[id_] = {"render_bbox_px": b, "target_px": [round(tx0, 1), round(ty0, 1), round(tx1, 1), round(ty1, 1)], "d": [round(v, 1) for v in d]}
    flag = " <<<" if max(abs(v) for v in d) > 4 else ""
    print(f"{id_:<11}{d[0]:>6.1f}{d[1]:>6.1f}{d[2]:>6.1f}{d[3]:>6.1f}{flag}")

# box edges: quote/container/summary/flow borders in render vs targets
def redrow(y, x0, x1):
    return sum(1 for x in range(int(x0), int(x1)) if redp(px[x, int(y)]))
def redcol(x, y0, y1):
    return sum(1 for y in range(int(y0), int(y1)) if redp(px[int(x), y]))
# quote box top border target slide y 100.5 -> px 209.5
for name, ty, x0, x1 in [("quote_top", 100.5, 100, 1800), ("quote_bot", 160.1, 100, 1800)]:
    yy = ty * SC
    found = None
    for dy in range(-8, 9):
        if redrow(yy + dy, x0, x1) > 300: found = yy + dy; break
    print(name, "target px", round(yy, 1), "found", round(found, 1) if found else None, "d", round(found - yy, 1) if found else "MISS")
json.dump(res, open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide039/closed_loop_a1.json", "w"), indent=1)
