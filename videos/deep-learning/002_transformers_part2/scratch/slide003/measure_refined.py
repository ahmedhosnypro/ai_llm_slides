#!/usr/bin/env python3
"""Refined measurement for slide_003.jpg.
1) chrome border landmarks (fine detector) -> frame->slide mapping fit
2) badge cross-check vs house (893,71)
3) word-level segmentation of title/subtitle blue ink; per-word cap heights
4) mixed-size title font fit (Arial Bold advances)
Outputs JSON to measure_refined_output.txt
"""
import numpy as np
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_003.jpg"
im = Image.open(SRC).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
out = {}

def runs(v):
    out_ = []
    if not v: return out_
    s = p = v[0]
    for x in v[1:]:
        if x == p + 1: p = x
        else: out_.append((s, p, (s + p) / 2)); s = p = x
    out_.append((s, p, (s + p) / 2))
    return out_

# ---- 1. chrome landmarks: red-dominant, lower threshold, count in panel band ----
# C00000=(192,0,0); 8B1A1A=(139,26,26). JPEG noise -> allow wider.
red = (R > 100) & (R - G > 40) & (R - B > 40)
# vertical strokes: count red per column across rows 100..500 (avoid badge/bottom)
colcount = red[100:500, :].sum(axis=0)
vcols = [c for c in range(W) if colcount[c] > 100]
out["vertical_red_cols"] = vcols
out["vertical_red_runs"] = runs(vcols)
# horizontal strokes: count red per row across cols 100..850
rowcount = red[:, 100:850].sum(axis=1)
hrows = [r for r in range(H) if rowcount[r] > 100]
out["horizontal_red_rows"] = runs(hrows)

# left/right border column: strongest red columns near expected 59/902
prof = [(c, int(colcount[c])) for c in range(40, 75)]
out["col_prof_left"] = prof
prof2 = [(c, int(colcount[c])) for c in range(890, 920)]
out["col_prof_right"] = prof2
# top border row: strongest red rows near expected 43
prof3 = [(r, int(rowcount[r])) for r in range(30, 60)]
out["row_prof_top"] = prof3
# bottom border row near 516
prof4 = [(r, int(rowcount[r])) for r in range(505, 525)]
out["row_prof_bottom"] = prof4

# ---- 2. badge ----
yellow = (R > 200) & (G > 200) & (B < 210) & (B < G - 25) & (B < R - 25)
ys, xs = np.nonzero(yellow)
m = (xs > W * 0.75) & (ys < H * 0.35)
bx, by = xs[m], ys[m]
out["badge"] = {"x0": int(bx.min()), "x1": int(bx.max()), "y0": int(by.min()), "y1": int(by.max()),
                "cx": float((bx.min() + bx.max()) / 2), "cy": float((by.min() + by.max()) / 2)}

# ---- 3. blue ink word segmentation ----
blue = (B > 110) & (B - R > 60) & (B - G > 60) & (R < 120)
ys, xs = np.nonzero(blue)
bands = [(173, 214), (285, 317)]
words = []
for (y0, y1) in bands:
    m2 = (ys >= y0) & (ys <= y1)
    bx2, by2 = xs[m2], ys[m2]
    colh = np.zeros(W, dtype=int)
    for x in bx2: colh[x] += 1
    # word gaps: columns with no ink, gap >= 4px (space at these sizes ~15-20px; letter gaps smaller)
    segs = []
    inseg = False
    for x in range(W):
        if colh[x] > 0 and not inseg: s = x; inseg = True
        elif colh[x] == 0 and inseg:
            segs.append([s, x - 1]); inseg = False
    if inseg: segs.append([s, W - 1])
    # merge segments separated by < 5px (intra-word letter gaps)
    merged = []
    for sgm in segs:
        if merged and sgm[0] - merged[-1][1] <= 5: merged[-1][1] = sgm[1]
        else: merged.append(sgm)
    wl = []
    for (sx0, sx1) in merged:
        m3 = (bx2 >= sx0) & (bx2 <= sx1)
        wy, wx = by2[m3], bx2[m3]
        wl.append({"x0": int(wx.min()), "x1": int(wx.max()), "y0": int(wy.min()), "y1": int(wy.max()),
                   "w": int(wx.max() - wx.min() + 1), "h": int(wy.max() - wy.min() + 1),
                   "cx": float((wx.min() + wx.max()) / 2)})
    words.append({"band": [y0, y1], "words": wl})

out["words"] = words

# ---- 4. mapping fit ----
# landmarks: use measured frame positions; slide-side knowns from chrome law:
# panel left border col ~59 <-> slide x 42 ; right ~902 <-> slide x 919(+1 border outer edge?)
# slide 002 precedent: frame 59,902,43,516 <-> slide 42,919,45,540
fl = out["vertical_red_runs"]
fr = runs(hrows)
out["landmarks_raw"] = {"vruns": fl, "hruns": fr}

print(json.dumps(out, indent=1, default=int))
