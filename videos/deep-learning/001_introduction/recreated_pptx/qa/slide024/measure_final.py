#!/usr/bin/env python3
"""Round 3 (builder): definitive geometry for slide_024 build.
Banks build-ready constants + zoomed sub-crops for the 6 blue weight labels."""
from PIL import Image
import numpy as np

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_024.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a)
    OUT.append(s); print(s)

# ---- 1. beige panel bbox (beige ~ DAD0C4) ----
beige = (abs(r - 0xDA) < 14) & (abs(g - 0xD0) < 14) & (abs(b - 0xC4) < 14)
ys, xs = np.where(beige)
P("PANEL beige bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max())

# ---- 2. col1 gray neurons (fill ~ EBEDEA/CCCCCC, ring darker gray) ----
# scan rows at y=212,286,367 for the col1 circle: non-beige run between x=100..200
for yy in (212, 286, 367):
    row = A[yy]
    nz = [x for x in range(100, 205) if not beige[yy, x]]
    if nz:
        P(f"col1 row y{yy}: ink x {nz[0]}..{nz[-1]} (cx~{(nz[0]+nz[-1])/2:.1f})")

# vertical extent at col1 center x=163
for yy in (212, 286, 367):
    col = A[:, 163]
    nz = [y for y in range(yy - 30, yy + 30) if not beige[y, 163]]
    if nz:
        P(f"col1 col x163 near y{yy}: ink y {nz[0]}..{nz[-1]} (cy~{(nz[0]+nz[-1])/2:.1f})")

# ---- 3. o-o-o rings after col1 (dark ring strokes on the row center) ----
for yy in (212, 286, 367):
    nz = [x for x in range(185, 245) if (r[yy, x] + g[yy, x] + b[yy, x]) < 500]
    P(f"ring-strokes after col1 y{yy}:", nz)

# ---- 4. o-o rings before col5 (row-center scan, O_k label y ends <=287) ----
for yy in (207, 290, 367):
    nz = [x for x in range(595, 660) if (r[yy, x] + g[yy, x] + b[yy, x]) < 500]
    P(f"ring-strokes before col5 y{yy}:", nz)

# ---- 5. col5 neuron bbox (gray fill; scan rows) ----
for yy in (207, 285, 368):
    nz = [x for x in range(655, 710) if not beige[yy, x]]
    if nz: P(f"col5 row y{yy}: ink x {nz[0]}..{nz[-1]}")
for xx in (677,):
    runs = []; in_g = False
    for y in range(180, 400):
        v = not beige[y, xx]
        if v and not in_g: in_g = True; st = y
        elif not v and in_g: in_g = False; runs.append((st, y - 1))
    if in_g: runs.append((st, 399))
    P(f"col5 col x{xx}: ink y-runs:", runs)

# ---- 6. output boxes: near-black mask x700..820 ----
black = (r < 70) & (g < 70) & (b < 70)
seg = black[150:420, 700:820]
rows = seg.sum(axis=1)
runs = []; in_g = False
for i, v in enumerate(rows):
    if v > 2 and not in_g: in_g = True; st = i
    elif v <= 2 and in_g: in_g = False; runs.append((150 + st, 150 + i - 1))
if in_g: runs.append((150 + st, 419))
P("OUTPUT black boxes y-runs (x700..820):", runs)
for (y0, y1) in runs:
    sub = black[y0:y1 + 1, 700:820]
    cols = sub.sum(axis=0)
    xs2 = np.where(cols > 2)[0]
    if len(xs2): P(f"  box y{y0}..{y1}: x {700+xs2[0]}..{700+xs2[-1]}")

# ---- 7. error bar (red-dominant x790..830) ----
red = (r > 110) & (g < 90) & (b < 90)
seg = red[150:430, 790:830]
ys3, xs3 = np.where(seg)
P("ERROR bar bbox: x", 790 + xs3.min(), 790 + xs3.max(), "y", 150 + ys3.min(), 150 + ys3.max())

# ---- 8. class boxes (light green E8FFC8..) ----
lg = (g > 200) & (r > 150) & (r < 240) & (b < 210) & (g - b > 25)
seg = lg[150:430, 815:910]
rows = seg.sum(axis=1)
runs = []; in_g = False
for i, v in enumerate(rows):
    if v > 4 and not in_g: in_g = True; st = i
    elif v <= 4 and in_g: in_g = False; runs.append((150 + st, 150 + i - 1))
if in_g: runs.append((150 + st, 429))
P("CLASS boxes y-runs:", runs)
for (y0, y1) in runs:
    sub = lg[y0:y1 + 1, 815:910]
    cols = sub.sum(axis=0); xs2 = np.where(cols > 1)[0]
    if len(xs2): P(f"  class y{y0}..{y1}: x {815+xs2[0]}..{815+xs2[-1]}")

# ---- 9. blue weight labels: b-dominant clusters, grouped ----
blue = (b - r > 40) & (b - g > 40) & (b > 90)
ys4, xs4 = np.where(blue[180:300, 300:530])
pts = sorted(zip(xs4 + 300, ys4 + 180))
# simple grid-cluster merge (8px gap)
clusters = []
used = [False] * len(pts)
for i, (x, y) in enumerate(pts):
    if used[i]: continue
    qx = [x]; qy = [y]; used[i] = True
    changed = True
    while changed:
        changed = False
        for j, (x2, y2) in enumerate(pts):
            if used[j]: continue
            if min(abs(x2 - a) + abs(y2 - bb) < 9 for a in qx[:1] for bb in qy[:1]):
                pass
    clusters.append(None)
# simpler: label by scanning columns profile per gap zone
for tag, (x0, x1) in (("GAP23", (300, 400)), ("GAP34", (465, 560))):
    seg2 = blue[185:300, x0:x1]
    cols = seg2.sum(axis=0)
    runs2 = []; in_g = False
    for i, v in enumerate(cols):
        if v > 0 and not in_g: in_g = True; st = i
        elif v == 0 and in_g:
            in_g = False
            if i - st > 3: runs2.append((x0 + st, x0 + i - 1))
    if in_g: runs2.append((x0 + st, x1 - 1))
    P(f"BLUE {tag} column-runs:", runs2)
    for (rx0, rx1) in runs2:
        sub2 = blue[185:300, rx0:rx1 + 1]
        rr = sub2.sum(axis=1)
        ys5 = np.where(rr > 0)[0]
        P(f"   x{rx0}..{rx1}: y {185+ys5[0]}..{185+ys5[-1]}")

# ---- 10. magenta dashed line + boxes ----
mag = (r - g > 60) & (b - g > 40)
seg6 = mag[120:160, 130:830]
ys6, xs6 = np.where(seg6)
P("DASHED magenta: y", 120 + ys6.min(), 120 + ys6.max(), "x", 130 + xs6.min(), 130 + xs6.max())

# ---- 11. net labels (red, above panel) ----
red2 = (r - g > 60) & (r - b > 60) & (r > 120)
for tag, (x0, x1) in (("Net_i", (195, 240)), ("Net_j", (360, 410)), ("Net_k", (525, 575))):
    seg7 = red2[160:195, x0:x1]
    ys7, xs7 = np.where(seg7)
    if len(ys7): P(f"{tag} red ink: x {x0+xs7.min()}..{x0+xs7.max()} y {160+ys7.min()}..{160+ys7.max()}")

# ---- 12. block arrows + callouts precise bboxes ----
for tag, (x0, x1) in (("arrow_i", (225, 305)), ("arrow_j", (390, 470)), ("arrow_k", (550, 630))):
    nz = [x for x in range(x0, x1) if not beige[400, x]]
    P(f"{tag} @y400: x {nz[0] if nz else '?'}..{nz[-1] if nz else '?'}")

# ---- 13. zoomed sub-crops of the 6 blue labels ----
crops = {
    "z_lbl_A1.png": (315, 188, 365, 218, 6),
    "z_lbl_A2.png": (312, 218, 352, 252, 6),
    "z_lbl_A3.png": (320, 252, 355, 292, 6),
    "z_lbl_B1.png": (478, 190, 522, 218, 6),
    "z_lbl_B2.png": (480, 218, 520, 255, 6),
    "z_lbl_B3.png": (483, 252, 515, 292, 6),
}
for name, (x0, y0, x1, y1, z) in crops.items():
    c = IM.crop((x0, y0, x1, y1)).resize(((x1 - x0) * z, (y1 - y0) * z), Image.LANCZOS)
    c.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/" + name)
P("zoom label crops saved")

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/measure_final_out.txt", "w") as f:
    f.write("\n".join(OUT) + "\n")
