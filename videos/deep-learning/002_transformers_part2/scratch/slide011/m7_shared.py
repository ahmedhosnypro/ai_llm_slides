#!/usr/bin/env python3
"""m7: verify shared structures of 015's certified build against the 011 frame."""
from PIL import Image
import json
from collections import Counter

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
im = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
px = im.load()
out = {}

def near(p, t, tol):
    return all(abs(p[i] - t[i]) <= tol for i in range(3))

def bbox_of(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))

# 1) blue frame rect: purple line (78,70,160) tol 40, exclude badge area
bp = [(x, y) for y in range(40, 520) for x in range(40, 925)
      if near(px[x, y], (78, 70, 160), 45) and px[x, y][2] - px[x, y][0] > 40]
out["blue_frame_n"] = len(bp)
if bp:
    colc = Counter(p[0] for p in bp); rowc = Counter(p[1] for p in bp)
    out["blue_cols>100"] = sorted(c for c, n in colc.items() if n > 100)
    out["blue_rows>100"] = sorted(r for r, n in rowc.items() if n > 100)
    out["blue_bbox"] = bbox_of(bp)

# 2) Dot Product box tan D8C0B4
tp = [(x, y) for y in range(180, 380) for x in range(200, 320)
      if near(px[x, y], (216, 192, 180), 24)]
out["dotprod_tan"] = {"n": len(tp)}
if tp:
    out["dotprod_tan"]["bbox"] = bbox_of(tp)

# 3) Scaling pill F6C6CC
sp = [(x, y) for y in range(180, 380) for x in range(290, 345)
      if near(px[x, y], (246, 198, 204), 22)]
out["scaling_pill"] = {"n": len(sp)}
if sp:
    out["scaling_pill"]["bbox"] = bbox_of(sp)
# 4) Softmax pill FAD2FA
sm = [(x, y) for y in range(180, 380) for x in range(345, 400)
      if near(px[x, y], (250, 210, 250), 20)]
out["softmax_pill"] = {"n": len(sm)}
if sm:
    out["softmax_pill"]["bbox"] = bbox_of(sm)
# 5) Sigma DCF3F3
sg = [(x, y) for y in range(195, 245) for x in range(395, 515)
      if near(px[x, y], (220, 243, 243), 14)]
out["sigma_box"] = {"n": len(sg)}
if sg:
    out["sigma_box"]["bbox"] = bbox_of(sg)

# 6) white pill ovals row: white pixels y183..207 x92..645
wp = [(x, y) for y in range(183, 208) for x in range(92, 646) if near(px[x, y], (255, 255, 255), 12)]
out["pillrow_white_n"] = len(wp)
if wp:
    colc = Counter(p[0] for p in wp)
    cols = sorted(c for c, n in colc.items() if n > 6)
    runs = []
    if cols:
        s = e = cols[0]
        for c in cols[1:]:
            if c - e <= 6: e = c
            else: runs.append((s, e)); s = e = c
        runs.append((s, e))
    out["pillrow_col_runs"] = runs

# 7) nodes: white circles w/ red ring — red ring pixels x400..500 y230..350
nr = [(x, y) for y in range(225, 355) for x in range(398, 505)
      if near(px[x, y], (204, 34, 34), 55) and px[x, y][0] - px[x, y][1] > 90]
out["node_red_n"] = len(nr)
if nr:
    rowc = Counter(p[1] for p in nr)
    bands = []
    ys_s = sorted(set(p[1] for p in nr)); s = e = ys_s[0]
    for y in ys_s[1:]:
        if y - e <= 4: e = y
        else: bands.append((s, e)); s = e = y
    bands.append((s, e))
    out["node_red_row_bands"] = bands

# 8) W_v right boxes x530..565: white fill blue border
wv = [(x, y) for y in range(225, 350) for x in range(528, 568) if near(px[x, y], (255, 255, 255), 10)]
out["wv_white_n"] = len(wv)
if wv:
    colc = Counter(p[0] for p in wv)
    out["wv_cols>8"] = sorted(c for c, n in colc.items() if n > 8)

# 9) outContainers dashed green borders right side x560..830 y140..360
oc = [(x, y) for y in range(130, 370) for x in range(560, 835)
      if near(px[x, y], (46, 139, 87), 42) and px[x, y][1] - px[x, y][0] > 35]
out["outcont_green_n"] = len(oc)
if oc:
    colc = Counter(p[0] for p in oc)
    out["outcont_cols>20"] = sorted(c for c, n in colc.items() if n > 20)

# 10) W chips columns: red/green/blue bordered small boxes x600..815 y290..430
chq = [(x, y) for y in range(285, 435) for x in range(598, 818)
       if (near(px[x, y], (204, 34, 34), 45) or near(px[x, y], (46, 139, 87), 40) or near(px[x, y], (47, 85, 200), 45))
       and px[x, y][1] - px[x, y][0] > 30 or (near(px[x, y], (204, 34, 34), 45) and px[x, y][0] - px[x, y][1] > 90)]
out["chips_n"] = len(chq)
if chq:
    colc = Counter(p[0] for p in chq)
    cols = sorted(c for c, n in colc.items() if n > 12)
    runs = []
    if cols:
        s = e = cols[0]
        for c in cols[1:]:
            if c - e <= 8: e = c
            else: runs.append((s, e)); s = e = c
        runs.append((s, e))
    out["chips_col_runs"] = runs

# 11) h ovals black tags x590..815 y100..215
hb = [(x, y) for y in range(100, 215) for x in range(588, 818) if sum(px[x, y]) < 200]
out["htags_n"] = len(hb)
if hb:
    rowc = Counter(p[1] for p in hb)
    bands = []
    ys_s = sorted(set(p[1] for p in hb)); s = e = ys_s[0]
    for y in ys_s[1:]:
        if y - e <= 5: e = y
        else: bands.append((s, e)); s = e = y
    bands.append((s, e))
    out["htags_row_bands"] = bands
    colc = Counter(p[0] for p in hb)
    out["htags_col_runs"] = None

# 12) K·q label + fraction zone x285..375 y205..240: dark red text pixels
kq = [(x, y) for y in range(205, 242) for x in range(285, 378)
      if sum(px[x, y]) < 430 and px[x, y][0] > px[x, y][2]]
out["kq_n"] = len(kq)
if kq:
    colc = Counter(p[0] for p in kq)
    cols = sorted(c for c, n in colc.items() if n > 2)
    runs = []
    if cols:
        s = e = cols[0]
        for c in cols[1:]:
            if c - e <= 8: e = c
            else: runs.append((s, e)); s = e = c
        runs.append((s, e))
    out["kq_col_runs"] = runs

# 13) query row strips: X2 purple highlight (D296C8) + others F7F3D8
q2 = [(x, y) for y in range(400, 432) for x in range(220, 300) if near(px[x, y], (210, 150, 200), 30)]
out["qstrip_x2_n"] = len(q2)
if q2:
    out["qstrip_x2_bbox"] = bbox_of(q2)
q1 = [(x, y) for y in range(400, 432) for x in range(170, 400) if near(px[x, y], (247, 243, 216), 14)]
out["qstrip_beige_n"] = len(q1)
if q1:
    colc = Counter(p[0] for p in q1)
    cols = sorted(c for c, n in colc.items() if n > 6)
    runs = []
    if cols:
        s = e = cols[0]
        for c in cols[1:]:
            if c - e <= 6: e = c
            else: runs.append((s, e)); s = e = c
        runs.append((s, e))
    out["qstrip_beige_runs"] = runs

print(json.dumps(out, indent=1, default=str))
