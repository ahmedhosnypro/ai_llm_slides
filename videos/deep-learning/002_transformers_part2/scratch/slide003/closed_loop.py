#!/usr/bin/env python3
"""Closed-loop check for slide 003 (word-level, robust):
- segment render words by TARGET word-space midpoints (no gap-threshold fragility)
- halo-corrected frame targets: JPEG halo inflates frame bboxes ~1px/side, so the
  true ink edge sits ~1px OUTSIDE the strict-blue bbox (established slide_002
  closed-loop practice; strict-vs-wide-net bands here differ by exactly ~2px).
  target_slide_x0 = (fx0-1-18.128)/0.961232 ; x1 = (fx1+1-18.128)/0.961232
Tolerance ~4px @150dpi (1.92pt). Vertical targets likewise halo-corrected.
"""
from PIL import Image
import numpy as np
import json, sys

RENDER = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide003/render_K.png"
K = sys.argv[2] if len(sys.argv) > 2 else "K"
img = Image.open(RENDER).convert("RGB")
W, H = img.size
a = np.asarray(img).astype(int)
R, G, B = a[..., 0], a[..., 1], a[..., 2]
print(f"render size: {W}x{H} (attempt {K})")

PXPT = 150 / 72.0
MX = lambda fx0, fx1: ((fx0 - 1 - 18.128) / 0.961232, (fx1 + 1 - 18.128) / 0.961232)
MY = lambda fy: (fy + 0.591) / 0.957576

# halo-corrected word targets (strict-blue frame CC bboxes ± 1px halo)
words = [
    ("Review",    *MX(286, 479)),
    ("of",        *MX(498, 549)),
    ("Part",      *MX(569, 651)),
    ("I",         *MX(668, 674)),
    ("Self",      *MX(209, 288)),
    ("Attention", *MX(302, 492)),
    ("Mechanism", *MX(512, 748)),
]
# vertical targets (halo-corrected): R capTop strict 174 -> 173 ; baseline last ink 215 -> 216
T_TITLE_CAPTOP = MY(173.0)   # 182.2
T_TITLE_BASE = MY(216.0)     # 226.1
T_SUB_CAPTOP = MY(284.0)     # 297.8  (S cap strict 285 -> 284)
T_SUB_BASE = MY(319.0)       # 333.6  (last ink 318 -> 319)

blue = (B - R > 60) & (B - G > 60) & (B > 110) & (R < 120)
blue[80:250, 1770:1950] = False  # badge ring zone (purple ring matches blue mask)

Y0, Y1, X0, X1 = 120, 1000, 150, 1850
ys, xs = np.nonzero(blue[Y0:Y1, X0:X1])
xs = xs + X0; ys = ys + Y0

rowh = np.bincount(ys, minlength=H)
bands, inb = [], False
for y in range(Y0, Y1):
    if rowh[y] > 0 and not inb: s = y; inb = True
    elif rowh[y] == 0 and inb: bands.append((s, y - 1)); inb = False
if inb: bands.append((s, Y1 - 1))
bands = [b for b in bands if b[1] - b[0] >= 3]

def segs_nogap(y0, y1):
    m = (ys >= y0) & (ys <= y1)
    bx = xs[m]
    colh = np.bincount(bx, minlength=W)
    segs, inseg = [], False
    for x in range(W):
        if colh[x] > 0 and not inseg: st = x; inseg = True
        elif colh[x] == 0 and inseg: segs.append([st, x - 1]); inseg = False
    if inseg: segs.append([st, W - 1])
    return segs

def bbox(seg, y0, y1):
    x0, x1 = seg
    m = (xs >= x0) & (xs <= x1) & (ys >= y0) & (ys <= y1)
    bx, by = xs[m], ys[m]
    return int(bx.min()), int(bx.max()), int(by.min()), int(by.max())

ok_all = True
report = []
if len(bands) != 2:
    print(f"EXPECTED 2 content bands, got {bands}"); ok_all = False
else:
    title_words = words[:4]
    sub_words = words[4:]
    # split points: midpoint between adjacent target words (px)
    tsp = [ (title_words[i][2] + title_words[i+1][1]) / 2 * PXPT for i in range(3) ]
    ssp = [ (sub_words[i][2] + sub_words[i+1][1]) / 2 * PXPT for i in range(2) ]
    tsegs = segs_nogap(*bands[0]); ssegs = segs_nogap(*bands[1])
    print("title raw segs:", tsegs)
    print("subtitle raw segs:", ssegs)
    def assign(segs, splits):
        out = [[] for _ in range(len(splits) + 1)]
        for sg in segs:
            c = (sg[0] + sg[1]) / 2
            idx = sum(1 for sp in splits if c > sp)
            out[idx].append(sg)
        return out
    tby = assign(tsegs, tsp); sby = assign(ssegs, ssp)
    print("title by word:", tby)
    print("subtitle by word:", sby)
    if any(len(g) == 0 for g in tby + sby):
        print("EMPTY WORD GROUP — segmentation broken"); ok_all = False
    for (name, tx0, tx1), grp in list(zip(title_words, tby)) + list(zip(sub_words, sby)):
        if not grp: continue
        allseg = [s for sg in grp for s in [sg]]
        x0 = min(s[0] for s in allseg); x1 = max(s[1] for s in allseg)
        d = {"x0": round(x0 / PXPT - tx0, 2), "x1": round(x1 / PXPT - tx1, 2)}
        dpx = {k: round(v * PXPT, 1) for k, v in d.items()}
        worst = max(abs(v) for v in dpx.values())
        p = worst <= 4.0
        if not p: ok_all = False
        report.append({"word": name, "meas_pt": [round(x0 / PXPT, 2), round(x1 / PXPT, 2)],
                       "target_pt": [round(tx0, 2), round(tx1, 2)], "delta_px150": dpx,
                       "worst_px": worst, "pass_4px": p})
    tb, sb = bands
    v = {"title_capTop_d_px": round((tb[0] / PXPT - T_TITLE_CAPTOP) * PXPT, 1),
         "title_baseline_d_px": round(((tb[1] + 1) / PXPT - T_TITLE_BASE) * PXPT, 1),
         "sub_capTop_d_px": round((sb[0] / PXPT - T_SUB_CAPTOP) * PXPT, 1),
         "sub_baseline_d_px": round(((sb[1] + 1) / PXPT - T_SUB_BASE) * PXPT, 1)}
    for k, val in v.items():
        if abs(val) > 4.0: ok_all = False
    cont = {"x0": int(xs.min()), "x1": int(xs.max()), "y0": int(ys.min()), "y1": int(ys.max())}
    inside = xs.min() > 91 and xs.max() < 1911 and ys.min() > 97 and ys.max() < 1123
    cont["inside_frame"] = bool(inside)
    if not inside: ok_all = False
    report.append({"vertical_px": v})
    report.append({"containment": cont})
    print("vertical(px):", json.dumps(v))
    print("containment:", json.dumps(cont))

for r in report: print(json.dumps(r))
print("CLOSED-LOOP:", "PASS (all within 4px @150dpi)" if ok_all else "FAIL — adjust build")
