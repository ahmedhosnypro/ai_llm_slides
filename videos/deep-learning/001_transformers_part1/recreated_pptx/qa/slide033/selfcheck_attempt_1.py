#!/usr/bin/env python3
"""Slide 033 pre-judge self-check (attempt 1) — 150dpi render vs frame-true expectations.

Checks: (2) frame/panel containment incl. playlist white-margin adaptation (content must
sit inside the gray panel; inner panels must contain their content, known legitimate
crossings excluded), (3) equation/schematic region ink, (7) title box wrap/band,
(8) explicit line-spacing pins, plus fill-presence for the major families.
Render: 2001x1125 (150dpi). Scale render->frame px: *0.48 (150dpi frame = 960 wide).
"""
import sys
import numpy as np
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide033/render/slide-1.png"
im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W = im.shape[:2]
S = H / 540.0

def fr(v):
    return v * S

fails = []
notes = []

# ---- (2a) content containment inside the gray panel (chrome border bands excluded) --
white = (im.min(axis=2) > 235)
graypanel = (np.abs(im - np.array((233, 233, 231))).sum(axis=2) <= 30)
content = ~(white | graypanel)
# exclude the chrome's own border strokes + AA: frame x<=44, x>=916, y<=47, y>=533
content[: int(fr(47)), :] = False
content[int(fr(533)):, :] = False
content[:, : int(fr(44.5))] = False
content[:, int(fr(915.5)):] = False
ys, xs = np.nonzero(content)
if len(ys):
    fx0, fx1, fy0 = xs.min() / S, xs.max() / S, ys.min() / S
    notes.append(f"content ink bbox (frame px): x {fx0:.1f}..{fx1:.1f}  y {fy0:.1f}..{ys.max()/S:.1f}")
    if fx0 < 45 or fx1 > 915 or fy0 < 48:
        fails.append(f"content outside gray panel: x {fx0:.1f}..{fx1:.1f} y {fy0:.1f}..{ys.max()/S:.1f}")
else:
    fails.append("no content ink found?!")

# ---- (2b) inner-panel containment: dark ink in bands 2..5px OUTSIDE each boundary -----
# known legitimate crossings excluded per panel
KLINE_ROWS = [(236, 258), (277, 299), (318, 340), (361, 383)]  # the four flow-line bands
def dark(x0, y0, x1, y1, thr=170):
    sub = im[int(fr(y0)):int(fr(y1)), int(fr(x0)):int(fr(x1))]
    return int((sub.max(axis=2) < thr).sum())

def check_panel(name, x0, y0, x1, y1, skip=()):
    L = dark(x0 - 5, y0, x0 - 2, y1)
    R = dark(x1 + 2, y0, x1 + 5, y1)
    T = dark(x0, y0 - 5, x1, y0 - 2)
    B = dark(x0, y1 + 2, x1, y1 + 5)
    for (a, b) in KLINE_ROWS:
        if "L" in skip:
            L -= dark(x0 - 5, a, x0 - 2, b)
        if "R" in skip:
            R -= dark(x1 + 2, a, x1 + 5, b)
    if "B" in skip:  # X2 block arrow region below the sentence container
        B -= dark(253, y1 + 2, 296, y1 + 5)
    if "T" in skip:  # W_q box bottom + W_q->X2 arrow above the sentence container
        T -= dark(265, y0 - 5, 325, y0 - 2)
    if name == "left container":  # green connector stub under the container
        B -= dark(88, y1 + 2, 110, y1 + 5)
    if name == "right container":  # green connector line under the container
        B -= dark(794, y1 + 2, 812, y1 + 5)
    if name == "DP box":  # K.q label legitimately crosses the right border
        R -= dark(x1 + 2, 194, x1 + 5, 216)
    for side, n in (("L", L), ("R", R), ("T", T), ("B", B)):
        if n > 30:
            fails.append(f"{name}: ink OUTSIDE {side} boundary (n={n})")
        else:
            notes.append(f"{name}: {side}-outside clean (n={n})")

check_panel("left container", 58, 226, 140, 396, skip={("R", 0)})
check_panel("right container", 763, 226, 846, 396)
check_panel("DP box", 255, 194, 342, 402, skip={("L", 0)})
check_panel("legend", 736, 467, 901, 530)
check_panel("sentence container", 177, 473, 492, 517, skip={"B", "T"})
# peach panel: legend overhangs right+bottom by design -> mask it out
def dark_masked(x0, y0, x1, y1, thr=200):
    sub = im[int(fr(y0)):int(fr(y1)), int(fr(x0)):int(fr(x1))]
    m = sub.max(axis=2) < thr
    m[: int(fr(460)) - int(fr(y0)), :] = m[: int(fr(460)) - int(fr(y0)), :] & ~(
        (np.arange(sub.shape[1]) + int(fr(x0)) >= int(fr(725))).reshape(1, -1)
    )
    return int(m.sum())
peL = dark_masked(46, 107, 49, 522)
peR = dark_masked(869, 107, 872, 522)
peT = dark_masked(51, 102, 868, 105)
peB = dark_masked(51, 523, 868, 526)
peB -= dark(730, 523, 905, 526)  # legend overhangs the panel bottom by design
peB -= dark(253, 523, 296, 526)  # X2 block-arrow tail overhangs by design
peR -= dark(869, 460, 872, 530)  # legend overhangs the panel right by design
for side, n in (("L", peL), ("R", peR), ("T", peT), ("B", peB)):
    if n > 60:
        fails.append(f"peach panel: ink OUTSIDE {side} boundary (n={n})")
    else:
        notes.append(f"peach panel: {side}-outside clean (n={n})")

# ---- (3) EQUATION/SCHEMATIC REGIONS HAVE INK ---------------------------------------
eq_regions = {
    "legend 1*d L": (764, 480, 800, 505),
    "legend W box": (798, 472, 828, 502),
    "legend d*d": (794, 498, 832, 516),
    "legend =": (822, 476, 840, 500),
    "legend 1*d R": (862, 492, 895, 518),
    "Sigma glyph": (570, 194, 600, 219),
    "Y2 label": (566, 116, 602, 162),
    "K4 label": (234, 227, 256, 246),
    "V4 label": (637, 224, 658, 244),
    "K.q corner": (330, 195, 360, 215),
    "caption blue": (746, 506, 895, 528),
}
for name, (x0, y0, x1, y1) in eq_regions.items():
    sub = im[int(fr(y0)):int(fr(y1)), int(fr(x0)):int(fr(x1))]
    if name == "caption blue":
        m = (sub[:, :, 2] - sub[:, :, 0] > 30) & (sub.max(axis=2) < 190)
    else:
        m = sub.max(axis=2) < 190
    n = int(m.sum())
    if n < 12:
        fails.append(f"EQUATION REGION EMPTY: {name} (n={n})")
    else:
        notes.append(f"ink ok: {name} n={n}")
# caption must not touch the legend's bottom border (blue ink rows within y<529)
sub = im[int(fr(506)):int(fr(532)), int(fr(746)):int(fr(895))]
mb = (sub[:, :, 2] - sub[:, :, 0] > 30) & (sub.max(axis=2) < 190)
brows = np.nonzero(mb.any(axis=1))[0]
if len(brows) and brows.max() / S + 506 > 528.5:
    fails.append(f"caption ink too low: bottom at frame y {brows.max()/S + 506:.1f} (legend border at 529)")
else:
    notes.append(f"caption clear of bottom border (last ink row frame y {brows.max()/S + 506 if len(brows) else -1:.1f})")

# ---- (7) TITLE BOX: no wrap to a third line + band (badge excluded) ------------------
tx0, tx1 = 150, 860
sub = (im[int(fr(40)):int(fr(110)), int(fr(tx0)):int(fr(tx1))].max(axis=2) < 120)
rows = np.where(sub.sum(axis=1) > 3)[0]
if len(rows) == 0:
    fails.append("title region empty")
else:
    cols = np.nonzero(sub.any(axis=0))[0]
    x_lo, x_hi = tx0 + cols.min() / S, tx0 + cols.max() / S
    notes.append(f"title ink x {x_lo:.0f}..{x_hi:.0f} (frame)")
    if x_lo < 176 or x_hi > 846:
        fails.append(f"title ink outside expected x-band: {x_lo:.0f}..{x_hi:.0f}")
    splits = np.where(np.diff(rows) > 2)[0]
    nlines = len(splits) + 1
    notes.append(f"title line bands: {nlines}")
    if nlines != 2:
        fails.append(f"title renders {nlines} line bands (expected 2)")
    bands = []
    s = p = rows[0]
    for v in rows[1:]:
        if v <= p + 2:
            p = v
        else:
            bands.append((s, p)); s = p = v
    bands.append((s, p))
    if len(bands) >= 2:
        pitch = (bands[1][0] - bands[0][0]) / S
        notes.append(f"title line pitch: {pitch:.1f} frame px (pinned 24)")
        if abs(pitch - 24) > 3:
            fails.append(f"title pitch {pitch:.1f} != 24")

# ---- (8) DP title pitch (Dot/Product) ------------------------------------------------
sub2 = (im[int(fr(194)):int(fr(234)), int(fr(262)):int(fr(336))].max(axis=2) < 150)
rows2 = np.where(sub2.sum(axis=1) > 1)[0]
if len(rows2):
    bands2 = []
    s = p = rows2[0]
    for v in rows2[1:]:
        if v <= p + 2:
            p = v
        else:
            bands2.append((s, p)); s = p = v
    bands2.append((s, p))
    if len(bands2) >= 2:
        pitch2 = (bands2[1][0] - bands2[0][0]) / S
        notes.append(f"DP title pitch: {pitch2:.1f} frame px (pinned 13)")
        if abs(pitch2 - 13) > 2.5:
            fails.append(f"DP title pitch {pitch2:.1f} != 13")

# ---- region fills -----------------------------------------------------------------------
majors = {
    "peach fill": [(300, 130, 340, 160), "peach"],
    "W_k band fill": [(160, 262, 190, 272), "band"],
    "softmax fill": [(465, 350, 485, 380), "soft"],
    "sigma fill": [(530, 200, 560, 212), "sigma"],
    "DP fill": [(270, 300, 300, 320), "dp"],
    "container fill L": [(62, 300, 68, 320), "mint"],
    "circle1 ring": [(522, 236, 542, 256), "red"],
    "pill S fill": [(290, 168, 320, 178), "pill"],
}
def has_color(x0, y0, x1, y1, kind):
    sub = im[int(fr(y0)):int(fr(y1)), int(fr(x0)):int(fr(x1))].reshape(-1, 3)
    r, g, b = sub[:, 0], sub[:, 1], sub[:, 2]
    if kind == "peach":
        return int((np.abs(sub - np.array((247, 226, 205))).sum(axis=1) <= 40).sum())
    if kind == "band":
        return int((np.abs(sub - np.array((247, 249, 107))).sum(axis=1) <= 70).sum())
    if kind == "soft":
        return int((np.abs(sub - np.array((248, 221, 252))).sum(axis=1) <= 60).sum())
    if kind == "sigma":
        return int((np.abs(sub - np.array((234, 254, 252))).sum(axis=1) <= 45).sum())
    if kind == "dp":
        return int((np.abs(sub - np.array((220, 203, 187))).sum(axis=1) <= 45).sum())
    if kind == "mint":
        return int((np.abs(sub - np.array((231, 255, 233))).sum(axis=1) <= 45).sum())
    if kind == "red":
        return int(((r - g > 40) & (r - b > 25) & (r > 130)).sum())
    if kind == "pill":
        return int((np.abs(sub - np.array((255, 255, 227))).sum(axis=1) <= 40).sum())
    return 0

for name, (reg, kind) in majors.items():
    n = has_color(*reg, kind)
    if n < 20:
        fails.append(f"REGION MISSING/WRONG COLOR: {name} ({kind} n={n})")
    else:
        notes.append(f"fill ok: {name} n={n}")

print("SELF-CHECK ATTEMPT 1")
for n in notes:
    print("  .", n)
if fails:
    print("SELF-CHECK: FAIL")
    for f in fails:
        print("  !!", f)
    sys.exit(1)
print("SELF-CHECK: PASS")
