#!/usr/bin/env python3
"""measure5b — slide 022 fine pass (this run; distinct name avoids the dead
builder's leftover files): box x-edges per row via border-row scans, label line
profiles, line1/bullet text boxes, title/subtitle glyph caps, dash columns."""
import json
from PIL import Image
import numpy as np

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_022.jpg"
img = Image.open(FR).convert("RGB")
A = np.asarray(img).astype(int)
R, G, B = A[..., 0], A[..., 1], A[..., 2]
out = {}

def runs_of(mask_row, minw=1):
    runs, s = [], None
    for i, v in enumerate(mask_row):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= minw:
                runs.append([s, i - 1])
            s = None
    if s is not None:
        runs.append([s, len(mask_row) - 1])
    return runs

# --- row2 box edges: top border row 195, bottom 216 (strong blue > 30, dark-ish)
for y in [195, 216]:
    m = (B[y, :] - R[y, :] > 30) & (R[y, :] < 170) & (B[y, :] < 210)
    out[f"r2_border_y{y}"] = runs_of(m, 2)
# row2 vertical border columns: count strong-blue per column in 197..214 (text zone excluded partially)
sub = ((B[190:222, :] - R[190:222, :] > 45) & (R[190:222, :] < 150)).sum(axis=0)
out["r2_vcount"] = [[x, int(sub[x])] for x in range(170, 890) if sub[x] >= 12]

# --- row1 box edges: top border rows 126-127 (pinkish), bottom 147
for y in [126, 147]:
    m = (R[y, :] - G[y, :] > 22) & (R[y, :] > 150) & (G[y, :] > 100)
    out[f"r1_border_y{y}"] = runs_of(m, 2)
sub = ((R[124:150, :] - G[124:150, :] > 22) & (R[124:150, :] > 140) & (G[124:150, :] > 95)).sum(axis=0)
out["r1_vcount"] = [[x, int(sub[x])] for x in range(170, 890) if sub[x] >= 10]

# --- row3 box edges: vertical soft borders; use column profile of soft red in 280..298
sub = ((R[280:298, :] - G[280:298, :] > 25) & (R[280:298, :] > 140)).sum(axis=0)
out["r3_vcount"] = [[x, int(sub[x])] for x in range(170, 890) if sub[x] >= 8]
# row3 box top: scan y=277/278 across one box
for y in [277, 278]:
    m = (R[y, :] - G[y, :] > 40) & (R[y, :] < 200)
    out[f"r3_top_y{y}"] = runs_of(m, 2)
# row3 digit band: dark red rows in box1 zone
sub = ((R[:, 195:220] - G[:, 195:220] > 70) & (R[:, 195:220] < 170)).sum(axis=1)
out["r3_digit_rows_box1"] = [[y, int(sub[y])] for y in range(270, 310) if sub[y] > 2]
# row1 text band rows
sub = ((R[:, 185:880] - G[:, 185:880] > 55) & (R[:, 185:880] < 190)).sum(axis=1)
out["r1_text_rows"] = [[y, int(sub[y])] for y in range(120, 155) if sub[y] > 8]
# row2 text band rows
sub = ((B[:, 190:880] - R[:, 190:880] > 70) & (R[:, 190:880] < 100)).sum(axis=1)
out["r2_text_rows"] = [[y, int(sub[y])] for y in range(185, 230) if sub[y] > 8]

# --- dash columns fine
for nm, ys in [("r1", [122, 128, 136, 144, 152]), ("r2", [191, 200, 208, 217, 222]), ("r3", [267, 273, 283, 293, 298])]:
    for y in ys:
        out[f"{nm}_L_y{y}"] = " ".join("%02X%02X%02X" % tuple(A[y, x]) for x in range(161, 177))
        out[f"{nm}_R_y{y}"] = " ".join("%02X%02X%02X" % tuple(A[y, x]) for x in range(877, 893))

# --- label line profiles
bluem = (B - R > 55) & (B > 90) & (R < 120)
redm = (R - G > 55) & (R - B > 45) & (R > 110)
graym = (abs(R - G) < 22) & (abs(G - B) < 22) & (A.sum(axis=2) < 480) & (A.sum(axis=2) > 150)
out["lab2_prof"] = [[y, int(bluem[y, 70:165].sum())] for y in range(178, 234) if bluem[y, 70:165].sum() > 0]
out["lab3_prof"] = [[y, int(redm[y, 70:165].sum())] for y in range(256, 300) if redm[y, 70:165].sum() > 0]
out["lab1_prof"] = [[y, int(graym[y, 70:165].sum())] for y in range(108, 164) if graym[y, 70:165].sum() > 0]

def line_x(mask, y0, y1, x0=70, x1=168):
    s2 = mask[y0:y1, x0:x1]
    ys, xs = np.where(s2)
    if len(xs) == 0:
        return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max())]

# use profiles to split lines
out["lab2_l1"] = line_x(bluem, 186, 207)
out["lab2_l2"] = line_x(bluem, 207, 230)
out["lab3_l1"] = line_x(redm, 258, 277)
out["lab3_l2"] = line_x(redm, 277, 296)
out["lab1_l1"] = line_x(graym, 110, 127)
out["lab1_l2"] = line_x(graym, 127, 142)
out["lab1_l3"] = line_x(graym, 142, 160)

# --- bottom panel text
dark = (A.sum(axis=2) < 430)
sub = dark[364:386, 72:888]
ys, xs = np.where(sub)
out["line1_text_bbox"] = [72 + int(xs.min()), 364 + int(ys.min()), 72 + int(xs.max()), 364 + int(ys.max())] if len(xs) else None
for nm, y0, y1 in [("b1a", 406, 430), ("b1b", 430, 452), ("b2", 452, 472), ("b3", 474, 494)]:
    s2 = dark[y0:y1, 72:888]
    ys, xs = np.where(s2)
    out[f"{nm}_bbox"] = [72 + int(xs.min()), y0 + int(ys.min()), 72 + int(xs.max()), y0 + int(ys.max())] if len(xs) else None
s2 = dark[377:383, 600:900]
ys, xs = np.where(s2)
out["line1_underline_bbox"] = [600 + int(xs.min()), 377 + int(ys.min()), 600 + int(xs.max()), 377 + int(ys.max())] if len(xs) else None
# bullet dot bboxes
for nm, y0, y1 in [("dot1", 412, 428), ("dot2", 455, 471), ("dot3", 477, 493)]:
    s2 = dark[y0:y1, 76:96]
    ys, xs = np.where(s2)
    out[f"{nm}_bbox"] = [76 + int(xs.min()), y0 + int(ys.min()), 76 + int(xs.max()), y0 + int(ys.max())] if len(xs) else None

# --- title / subtitle glyph metrics
redm2 = (R - G > 40) & (R > 100)
bluem2 = (B - R > 55) & (B > 90)
def glyph(mask, x0, x1, y0, y1):
    s2 = mask[y0:y1, x0:x1]
    ys, xs = np.where(s2)
    if len(xs) == 0:
        return None
    return [x0 + int(xs.min()), y0 + int(ys.min()), x0 + int(xs.max()), y0 + int(ys.max())]
out["title_S"] = glyph(redm2, 338, 364, 52, 85)
out["title_E"] = glyph(redm2, 596, 622, 52, 85)
out["title_full"] = glyph(redm2, 300, 740, 52, 85)
out["sub_parenL"] = glyph(bluem2, 318, 336, 80, 110)
out["sub_U"] = glyph(bluem2, 348, 372, 80, 110)
out["sub_full"] = glyph(bluem2, 300, 760, 80, 110)

# --- clean fill censuses
def census(x0, x1, y0, y1, maskfn, topn=5):
    s2 = A[y0:y1, x0:x1].reshape(-1, 3)
    m = maskfn(s2)
    sel = s2[m]
    if len(sel) == 0:
        return None
    q = (sel // 4 * 4)
    vals, counts = np.unique(q, axis=0, return_counts=True)
    o = counts.argsort()[::-1][:topn]
    return {"n": int(m.sum()), "modes": [["%02X%02X%02X" % tuple(vals[i]), int(counts[i])] for i in o]}

out["c_r1_lane"] = census(614, 728, 121, 132, lambda s: s.sum(axis=1) > 580)
out["c_r1_lane2"] = census(614, 728, 145, 155, lambda s: s.sum(axis=1) > 580)
out["c_r1_boxfill"] = census(455, 535, 128, 132, lambda s: s.sum(axis=1) > 560)
out["c_r1_boxfill2"] = census(455, 535, 143, 146, lambda s: s.sum(axis=1) > 560)
out["c_r1_bordercore"] = census(180, 880, 125, 128, lambda s: (s[:, 0] - s[:, 1] > 30) & (s[:, 0] < 215))
out["c_r3_bordercore_top"] = census(180, 880, 276, 280, lambda s: (s[:, 0] - s[:, 1] > 60) & (s[:, 0] < 190))
out["c_r3_bordercore_bot"] = census(180, 880, 299, 303, lambda s: (s[:, 0] - s[:, 1] > 60) & (s[:, 0] < 190))
out["c_r3_vborder"] = census(176, 181, 281, 297, lambda s: (s[:, 0] - s[:, 1] > 30) & (s[:, 0] < 220))
out["c_r2_bordercore_top"] = census(180, 880, 194, 197, lambda s: (s[:, 2] - s[:, 0] > 40) & (s[:, 0] < 150))
out["c_r2_bordercore_bot"] = census(180, 880, 214, 218, lambda s: (s[:, 2] - s[:, 0] > 40) & (s[:, 0] < 150))
out["c_r3_lane"] = census(614, 728, 265, 275, lambda s: (s[:, 0] > 228) & (s[:, 0] - s[:, 2] > -6))
out["c_r3_digit"] = census(195, 870, 280, 298, lambda s: (s[:, 0] - s[:, 1] > 80) & (s[:, 0] < 160))
out["c_r1_text"] = census(185, 880, 132, 143, lambda s: (s[:, 0] - s[:, 1] > 70) & (s[:, 0] < 160))
out["c_r2_text"] = census(190, 880, 196, 214, lambda s: (s[:, 2] - s[:, 0] > 90) & (s[:, 0] < 70))
out["c_delta_dark"] = census(215, 810, 314, 330, lambda s: (s[:, 0] - s[:, 2] > 60) & (s[:, 0] < 170) & (s[:, 1] < 90))
out["c_arrow_core"] = census(265, 850, 293, 306, lambda s: (s[:, 0] - s[:, 2] > 90) & (s[:, 1] > 70) & (s[:, 1] < 180) & (s[:, 0] > 150))

print(json.dumps(out, indent=1))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide022/measure5b_output.txt", "w") as f:
    f.write(json.dumps(out, indent=1))
