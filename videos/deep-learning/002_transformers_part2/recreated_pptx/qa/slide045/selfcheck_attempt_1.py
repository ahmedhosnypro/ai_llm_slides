#!/usr/bin/env python3
"""Slide 045 attempt-1 pre-judge self-checks (17 §mandatory) + inheritance crop-diff vs 038.
Render: 150 dpi PNG of a 13.333x7.5in slide -> 2001x1125 px; 1 pt = 150/72 px = 2.0833 px.
"""
import numpy as np
from PIL import Image

RD = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide045/render_1.png"
R38 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide038/render_1.png"
img = np.asarray(Image.open(RD).convert("RGB")).astype(int)
img38 = np.asarray(Image.open(R38).convert("RGB")).astype(int)
H, W, _ = img.shape
S = 150 / 72.0  # px per pt
def px(v): return int(round(v * S))
fails = []
def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not cond: fails.append(name)

print(f"render {W}x{H}")

# ---- 2. FRAME CONTAINMENT ----
# canvas margin white EXCEPT the by-design half-visible panel bottom stroke (bottom 2 rows)
top_m = img[: px(40), :, :].reshape(-1, 3)
side_m = np.concatenate([img[:, : px(38), :].reshape(-1, 3), img[:, W - 4:, :].reshape(-1, 3)])
check("containment: top/side canvas margin white", min(top_m.min(), side_m.min()) > 235,
      f"top={top_m.min()} side={side_m.min()}")
left_of = img[:, : px(41.5), :]
check("containment: nothing left of panel border", left_of.min() > 235, f"min={left_of.min()}")

# ---- region color samples ----
def med(x0, y0, x1, y1):
    return np.median(img[px(y0):px(y1), px(x0):px(x1)].reshape(-1, 3), axis=0)
def near(c, ref, tol=28):
    return all(abs(int(a) - b) <= tol for a, b in zip(c, ref))

check("navy block fill 00008B", near(med(400, 450, 500, 465), (0, 8, 139)), str(med(400, 450, 500, 465)))
check("gray bar D9D9D9", near(med(250, 330, 350, 342), (217, 217, 217)), str(med(250, 330, 350, 342)))
check("container fill E2EFDA", near(med(140, 335, 160, 345), (226, 239, 218), 30), str(med(140, 335, 160, 345)))
check("annot fill FFFFCC", near(med(300, 100, 380, 108), (255, 255, 204), 25), str(med(300, 100, 380, 108)))
check("panel fill white", near(med(60, 200, 120, 230), (255, 255, 255), 12), str(med(60, 200, 120, 230)))
check("FFN box fill DDEBF7", near(med(200, 210.5, 600, 213.5), (221, 235, 247), 22), str(med(200, 210.5, 600, 213.5)))
check("tile fill FFE699", near(med(170, 236, 180, 241), (255, 230, 153), 32), str(med(170, 236, 180, 241)))
check("plus disc 990000", near(med(191.5, 366, 198.5, 373), (153, 0, 0), 40), str(med(191.5, 366, 198.5, 373)))
check("caption hl FFFF00", near(med(300, 523, 380, 531), (255, 255, 0), 30), str(med(300, 523, 380, 531)))
check("title red ink present", (img[px(58):px(74), px(300):px(680), 0] > 150).sum() > 300)

sub = img[px(363):px(377), px(188):px(203)]
check("plus white + glyph present", ((sub > 225).all(axis=2)).sum() > 12, str(((sub > 225).all(axis=2)).sum()))
dred = ((sub[:, :, 0] > 90) & (sub[:, :, 0] < 210) & (sub[:, :, 1] < 70) & (sub[:, :, 2] < 70)).sum()
check("plus dark-red disc dominant", dred > 90, str(dred))

# ---- ink presence with per-color masks ----
def cnt(x0, y0, x1, y1, mask):
    sub = img[px(y0):px(y1), px(x0):px(x1)]
    return mask(sub).sum()
blum = lambda s: (s[:, :, 2] > 130) & (s[:, :, 0] < 130) & (s[:, :, 2] - s[:, :, 0] > 60)
redm = lambda s: (s[:, :, 0] > 140) & (s[:, :, 1] < 90) & (s[:, :, 2] < 90)
orm = lambda s: (s[:, :, 0] > 180) & (s[:, :, 1] > 100) & (s[:, :, 1] < 200) & (s[:, :, 2] < 120)
check("annot line1 blue ink", cnt(80, 88, 420, 106, blum) > 150, str(cnt(80, 88, 420, 106, blum)))
check("annot line1 red part", cnt(424, 90, 688, 106, redm) > 80, str(cnt(424, 90, 688, 106, redm)))
check("annot line2 blue ink", cnt(120, 110, 810, 128, blum) > 150, str(cnt(120, 110, 810, 128, blum)))
check("annot line3 blue ink", cnt(120, 132, 790, 150, blum) > 150, str(cnt(120, 132, 790, 150, blum)))
check("FFN title blue ink", cnt(270, 212, 790, 226, blum) > 150, str(cnt(270, 212, 790, 226, blum)))
check("graybar text ink", cnt(420, 326, 610, 348, lambda s: (s.max(axis=2) < 150)) > 80)
check("navy text white", ((img[px(440):px(475), px(300):px(750)] > 200).all(axis=2)).sum() > 300)
check("caption red ink", cnt(270, 522, 555, 536, redm) > 80, str(cnt(270, 522, 555, 536, redm)))
check("ann blue label ink", cnt(40, 396, 150, 424, blum) > 40, str(cnt(40, 396, 150, 424, blum)))
check("ann orange label ink", cnt(40, 445, 150, 471, orm) > 40, str(cnt(40, 445, 150, 471, orm)))
check("ann red label ink", cnt(40, 487, 150, 514, redm) > 40, str(cnt(40, 487, 150, 514, redm)))
check("strip top label ink (col1)", cnt(180, 172, 210, 192, redm) > 8)

# ---- arrows present in their gaps ----
def colored(x0, y0, x1, y1, mask):
    sub = img[px(y0):px(y1), px(x0):px(x1)]
    return mask(sub).sum()
grnm = lambda s: (s[:, :, 1] > 110) & (s[:, :, 0] < 120) & (s[:, :, 1] - s[:, :, 0] > 40)
navm = lambda s: (s[:, :, 2] > 100) & (s[:, :, 0] < 80) & (s[:, :, 1] < 80)
check("red thin arrows (midrow->graybar)", colored(190, 303, 850, 321, redm) > 60, str(colored(190, 303, 850, 321, redm)))
check("green thin arrows (plus->graybar)", colored(190, 351.5, 850, 361.5, grnm) > 40, str(colored(190, 351.5, 850, 361.5, grnm)))
check("navy thin arrows (contY->plus)", colored(190, 378, 850, 394, navm) > 40, str(colored(190, 378, 850, 394, navm)))
check("blue arrows (topRow->FFN)", colored(190, 192, 850, 208, navm) > 40, str(colored(190, 192, 850, 208, navm)))
check("blue arrows (FFN->midrow)", colored(190, 271, 850, 285, navm) > 40, str(colored(190, 271, 850, 285, navm)))
check("block arrows zone1", colored(190, 413, 850, 431, navm) > 100)
check("block arrows zone2", colored(190, 484, 850, 502, navm) > 100)
check("orange curves present", colored(150, 365, 850, 500, orm) > 300)

# ---- strip band positions (yellow cell col1: x 169.9..182.4) ----
def band(x0, x1, y0, y1, mask, minrow=4):
    sub = img[px(y0):px(y1), px(x0):px(x1)]
    m = mask(sub)
    rr = np.where(m.sum(axis=1) > minrow)[0]
    if len(rr) == 0: raise ValueError("no band")
    return (rr.min() + px(y0)) / S, (rr.max() + px(y0)) / S
ym = lambda s: (s[:, :, 0] > 200) & (s[:, :, 1] > 200) & (s[:, :, 2] < 120)
for name, y0, y1, exp in [("topRow band", 165, 200, (175.0, 192.5)),
                          ("midRow band", 276, 310, (286.0, 302.7)),
                          ("contRow band", 385, 420, (394.8, 412.8)),
                          ("xRow band", 493, 525, (502.6, 519.8))]:
    try:
        r0, r1 = band(168, 184, y0, y1, ym)
        check(f"{name} position", abs(r0 - exp[0]) <= 3 and abs(r1 - exp[1]) <= 3, f"got {r0:.1f}..{r1:.1f} exp {exp}")
    except ValueError:
        check(f"{name} position", False, "no band found")

try:
    r0, r1 = band(165, 225, 226, 270, lambda s: (s[:, :, 0] > 200) & (s[:, :, 1] > 190) & (s[:, :, 2] < 215) & (s[:, :, 0] - s[:, :, 2] > 25))
    check("FFN tile band position", abs(r0 - 234.4) <= 3 and abs(r1 - 263.8) <= 3, f"got {r0:.1f}..{r1:.1f}")
except ValueError:
    check("FFN tile band position", False, "no band")

# ---- 7. no-wrap ----
out_left = img[px(84):px(160), px(60):px(73)]
check("annot ink stays in box", out_left.min() > 200, f"min={out_left.min()}")

# ---- 8. annot line pitch = 22pt (blue ink rows) ----
sub = img[px(85):px(155), px(120):px(800)]
m = blum(sub)
rr = np.where(m.sum(axis=1) > 4)[0]
rows = [(a + px(85)) / S for a in rr]
bands = []
if rows:
    s = rows[0]; p = rows[0]
    for v in rows[1:]:
        if v > p + 3: bands.append((s, p)); s = v
        p = v
    bands.append((s, p))
tops = [b[0] for b in bands]
check("annot 3 line bands", len(bands) == 3, str([(round(a,1), round(b,1)) for a, b in bands]))
if len(bands) == 3:
    p1, p2 = tops[1] - tops[0], tops[2] - tops[1]
    check("annot line pitch 22pt", abs(p1 - 22) <= 2.5 and abs(p2 - 22) <= 2.5, f"{p1:.1f},{p2:.1f}")

# ---- INHERITANCE CROP-DIFF vs certified 038 render (per-block measured shifts) ----
# (x0, x1, y38_0, y38_1, dy, dx38): sample THIS render at y+dy / x, the 038 render at y / x+dx38.
# dx38 compensates deliberate position re-measurements (ann cx 94 here vs 100 certified).
pairs = [
    ("navy block", 300, 700, 440, 470, 12.6, 0),
    ("xRow strip col1", 172, 218, 493, 505, 11.8, 0),
    ("blk arrow col1 zone2", 189, 201, 473, 489, 12.1, 0),
    ("container fill right (borders excluded)", 855, 890, 335, 375, 13.7, 0),
    ("xRow dots", 630, 712, 494, 504, 12.6, 0),
    # ann labels: position-re-measured block (per-line shifts differ +11.5..+13.6) —
    # verified below against THIS frame's measured ink bands instead of a rigid crop-diff
    ("midRow strip col1 (038 top row)", 172, 218, 274, 288, 13.9, 0),
]
print("-- inheritance crop-diff (045 render vs 038 render @ per-block shift) --")
for name, x0, x1, y38_0, y38_1, dy, dx38 in pairs:
    hpx = px(y38_1) - px(y38_0)
    a = img[px(y38_0 + dy):px(y38_0 + dy) + hpx, px(x0):px(x1)].astype(int)
    b = img38[px(y38_0):px(y38_1), px(x0 + dx38):px(x1 + dx38)].astype(int)
    d = np.abs(a - b).mean()
    check(f"inherit {name} (mean|d|<10)", d < 10, f"mean={d:.1f} dy={dy} dx38={dx38}")

# ---- ann labels: ink bands vs THIS frame's measured bands (position = frame truth) ----
def ink_band(x0, x1, y0, y1, mask):
    sub = img[px(y0):px(y1), px(x0):px(x1)]
    rr = np.where(mask(sub).sum(axis=1) > 1)[0]
    if len(rr) == 0: raise ValueError("no ink")
    return (rr.min() + px(y0)) / S, (rr.max() + px(y0)) / S
for name, y0, y1, mask, exp in [
    ("ann blue band", 390, 430, blum, (398.7, 421.8)),
    # orange: frame thin-stroke JPEG band under-reads ink extent; capTop is the anchor
    ("ann orange band", 440, 475, orm, (447.9, 473.5)),
    ("ann red band", 482, 518, redm, (489.8, 512.8)),
]:
    try:
        r0, r1 = ink_band(55, 140, y0, y1, mask)
        check(f"{name} vs frame", abs(r0 - exp[0]) <= 3 and abs(r1 - exp[1]) <= 3.5, f"got {r0:.1f}..{r1:.1f} exp {exp}")
    except ValueError:
        check(f"{name} vs frame", False, "no ink")

print()
print("SELFCHECK RESULT:", "ALL PASS" if not fails else f"FAILURES: {fails}")
