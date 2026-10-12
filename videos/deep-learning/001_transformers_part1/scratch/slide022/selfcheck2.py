#!/usr/bin/env python3
"""Closed-loop self-check v2: render (150dpi) vs original frame, orig-px coords.
Detector fixes: color-specific container-border detection (peach fill no longer
fools the y300 stroke scan), row-mean square-edge detection, halo-excluded tag
windows, badge-excluded title window."""
from PIL import Image
import numpy as np

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide022/render/slide-1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"

r = np.asarray(Image.open(REN).convert("RGB")).astype(int)
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
SC = r.shape[1] / o.shape[1]
print(f"render {r.shape[1]}x{r.shape[0]}, scale {SC:.4f}")
fails = []

def check(name, got, want, tol):
    if got is None:
        ok = False
    else:
        if not isinstance(got, (list, tuple)): got = [got]
        if not isinstance(want, (list, tuple)): want = [want]
        ok = all(abs(g - w) <= tol for g, w in zip(got, want))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got} want {want} (tol {tol})")
    if not ok: fails.append(name)

# ---- 1. TITLE (clean window, excludes badge x>860 and panel border y>118) ----
print("== TITLE ==")
def ink_bbox(img, Sthr, x0, x1, y0, y1):
    sc = img.shape[1] / 960.0
    S = img.sum(axis=2)
    m = S[int(y0*sc):int(y1*sc), int(x0*sc):int(x1*sc)] < Sthr
    sc0 = sc
    rows = np.where(m.any(axis=1))[0]
    cols = np.where(m.any(axis=0))[0]
    if not len(rows): return None
    return (round(x0+cols.min()/sc0,1), round(x0+cols.max()/sc0,1),
            round(y0+rows.min()/sc0,1), round(y0+rows.max()/sc0,1))
tr = ink_bbox(r, 620, 125, 858, 50, 118)
to = ink_bbox(o, 620, 125, 858, 50, 118)
print("  render:", tr, " orig:", to)
check("title left", tr[0], to[0], 10)
check("title right", tr[1], to[1], 12)
check("title center", round((tr[0]+tr[1])/2,1), round((to[0]+to[1])/2,1), 8)
check("title top", tr[2], to[2], 5)
check("title bottom", tr[3], to[3], 5)

# ---- 2. PANELS (blue) ----
print("== PANELS ==")
def blue_cols(img):
    return (img[:,:,2] > 100) & (img[:,:,0] < 90) & (img[:,:,1] < 90)
bc = blue_cols(r)
colcnt = bc[int(130*SC):int(500*SC)].sum(axis=0)
edges = [x for x in range(len(colcnt)) if colcnt[x] > 300*SC]
groups = []
for x in edges:
    if groups and x - groups[-1][-1] <= 3: groups[-1].append(x)
    else: groups.append([x])
centers = [round(sum(g)/len(g)/SC,1) for g in groups]
print("  blue v-edges:", centers)
for w in (118, 486.5, 839):
    check(f"blue edge {w}", min(centers, key=lambda c: abs(c-w)), w, 5)
rowcnt = bc[:, int(130*SC):int(830*SC)].sum(axis=1)
redges = [y for y in range(len(rowcnt)) if rowcnt[y] > 300*SC]
groups = []
for y in redges:
    if groups and y - groups[-1][-1] <= 3: groups[-1].append(y)
    else: groups.append([y])
rcenters = [round(sum(g)/len(g)/SC,1) for g in groups]
print("  blue h-edges:", rcenters)
for w in (122.5, 523):
    check(f"blue h-edge {w}", min(rcenters, key=lambda c: abs(c-w)), w, 5)

# ---- 3. CONTAINERS: color-specific border columns at y=250 (no squares there) --
print("== CONTAINERS (border cols at y=250, color-specific) ==")
def border_cols(img, kind, y):
    row = img[int(y*SC):int(y*SC)+1][0]
    if kind == "dkred":
        m = (row[:,0] > 60) & (row[:,0] < 170) & (row[:,1] < 80) & (row[:,2] < 100)
    elif kind == "orange":
        m = (row[:,0] > 190) & (row[:,1] > 110) & (row[:,1] < 200) & (row[:,2] < 160)
    elif kind == "green":
        m = (row[:,1] > 80) & (row[:,0] < 130) & (row[:,2] < 150) & (row[:,1] > row[:,0] + 20)
    cols = [x for x in range(len(m)) if m[x]]
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 2*SC: groups[-1].append(x)
        else: groups.append([x])
    return [round((g[0]+g[-1])/2/SC,1) for g in groups]
for kind, wants in [("dkred", (158, 258, 498.5, 571.5)), ("orange", (265.5, 364.5, 578, 658)),
                    ("green", (372.5, 472.5, 666, 766))]:
    got = border_cols(r, kind, 250)
    print(f"  {kind} cols:", got)
    for w in wants:
        c = min(got, key=lambda c: abs(c-w)) if got else None
        check(f"{kind} border {w}", c, w, 4)

# ---- 4. SQUARES: row-mean darkness in L-INPUT square column -------------------
print("== SQUARES ==")
def sq_edges(img, x0, x1, y0, y1):
    S = img.sum(axis=2)
    seg = S[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    rm = seg.mean(axis=1)
    ys = [y for y, v in enumerate(rm) if v < 752]
    groups = []
    for y in ys:
        if groups and y - groups[-1][-1] <= 2*SC: groups[-1].append(y)
        else: groups.append([y])
    return [round(y0 + sum(g)/len(g)/SC, 1) for g in groups]
gr = sq_edges(r, 221, 237, 180, 460)
print("  render L-INPUT sq edges:", gr)
for w in (193, 235, 248, 290, 355, 397, 409.5, 451.5):
    c = min(gr, key=lambda c: abs(c-w)) if gr else None
    check(f"sq edge {w}", c, w, 4)
gr2 = sq_edges(r, 678, 696, 180, 460)
print("  render R-OUT sq edges:", gr2)
for w in (193, 235, 248, 290, 355, 397, 409.5, 451.5):
    c = min(gr2, key=lambda c: abs(c-w)) if gr2 else None
    check(f"R sq edge {w}", c, w, 4)
# PROJ squares: white-square presence inside peach (white cols at y320)
def white_cols(img, y, x0, x1):
    row = img[int(y*SC), int(x0*SC):int(x1*SC)]
    m = (row[:,0] > 235) & (row[:,1] > 235) & (row[:,2] > 225)
    xs = [x for x in range(len(m)) if m[x]]
    groups = []
    for x in xs:
        if groups and x - groups[-1][-1] <= 2*SC: groups[-1].append(x)
        else: groups.append([x])
    return [(round(x0+g[0]/SC,1), round(x0+g[-1]/SC,1)) for g in groups if len(g) > 8]
wl = white_cols(r, 320, 270, 360)
wr = white_cols(r, 320, 583, 653)
print("  L-PROJ white sq cols:", wl, " R-PROJ:", wr)
check("L-PROJ sq", [round(sum(wl[0])/2,1)] if wl else None, [316.5], 5)
check("R-PROJ sq", [round(sum(wr[0])/2,1)] if wr else None, [618.5], 5)

# ---- 5. LABELS / HEADERS / SUM -------------------------------------------------
print("== LABELS/HEADERS/SUM ==")
def text_bands(img, x0, x1, y0, y1):
    S = img.sum(axis=2)
    m = S[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)] < 620
    prof = m.sum(axis=1)
    runs, inr = [], False
    for i, c in enumerate(prof):
        if c >= 2*SC and not inr: s = i; inr = True
        elif c < 2*SC and inr: runs.append((s, i-1)); inr = False
    if inr: runs.append((s, len(prof)-1))
    return [(round(y0+a/SC,1), round(y0+b/SC,1)) for a, b in runs if b-a > 3*SC]
for name, (x0, x1, y0, y1), wants in [
    ("L-INPUT labels", (183, 216, 200, 445), (213.5, 271, 378.5, 432)),
    ("R-OUT labels", (712, 748, 200, 445), (216.5, 271, 376, 429.5)),
    ("L-INPUT header", (200, 260, 155, 185), (168.5)),
    ("L-PROJ header", (266, 362, 155, 185), (168.5)),
    ("L-OUT header", (374, 470, 155, 185), (168.5)),
    ("R-INPUT header", (500, 570, 155, 185), (168.5)),
    ("R-PROJ header", (579, 655, 155, 185), (168.5)),
    ("R-OUT header", (667, 763, 155, 185), (168.5)),
    ("SUM", (295, 340, 270, 300), (287.5)),
    ("L-OUT w(t)", (418, 445, 305, 340), (323)),
    ("R-IN w(t)", (500, 530, 305, 340), (324)),
]:
    bb = text_bands(r, x0, x1, y0, y1)
    got = round((bb[0][0]+bb[0][1])/2, 1) if bb else None
    check(f"{name}", got, wants, 5)

# ---- 6. TAGS ----
print("== TAGS ==")
def yellow_bbox(img, x0, x1, y0, y1):
    seg = img[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    rr, gg, bb = seg[:,:,0], seg[:,:,1], seg[:,:,2]
    m = (rr > 220) & (gg > 220) & (bb > 120) & (bb < 215)
    ys, xs = np.where(m)
    if not len(xs): return None
    return (round(x0+xs.min()/SC,1), round(x0+xs.max()/SC,1),
            round(y0+ys.min()/SC,1), round(y0+ys.max()/SC,1))
for name, (x0, x1), want in [("tag-L", (230, 400), (255, 377, 475, 501)),
                              ("tag-R", (530, 700), (552, 674, 475, 501))]:
    tb = yellow_bbox(r, x0, x1, 466, 515)
    print(f"  {name}: {tb}")
    check(f"{name} left/top", [tb[0], tb[2]], [want[0], want[2]], 5)
    check(f"{name} right/bottom", [tb[1], tb[3]], [want[1], want[3]], 6)

# ---- 7. ARROWS ----
print("== ARROWS ==")
def dark_cnt(img, x0, x1, y0, y1):
    seg = img[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    return int((seg.sum(axis=2) < 330).sum())
for name, box in [("A1", (245, 300, 215, 305)), ("A2", (245, 300, 272, 315)),
                  ("A3", (245, 300, 335, 373)), ("A4", (245, 300, 347, 428)),
                  ("A5", (332, 386, 318, 328)), ("A6", (573, 602, 319, 329)),
                  ("A7", (634, 672, 218, 305)), ("A8", (634, 672, 273, 316)),
                  ("A9", (634, 672, 333, 374)), ("A10", (634, 672, 345, 428))]:
    c = dark_cnt(r, *box)
    ok = c > 30
    if not ok: fails.append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: dark px {c}")

# ---- 8. CONTAINMENT (content inside chrome panel x42..918, y45..539) ----------
print("== CONTAINMENT ==")
left = int((r[int(150*SC):int(470*SC), 0:int(41*SC)].sum(axis=2) < 500).sum())
right = int((r[int(150*SC):int(470*SC), int(919*SC):].sum(axis=2) < 500).sum())
top = int((r[0:int(44*SC), int(60*SC):int(900*SC)].sum(axis=2) < 500).sum())
bot = int((r[int(540*SC-3):, int(60*SC):int(900*SC)].sum(axis=2) < 500).sum())
print(f"  stray ink: left {left}, right {right}, top {top}, bottom {bot}")
check("no stray ink outside panel", 0, 0, 0) if (left+right+top+bot) == 0 else fails.append("containment")

print()
print("SELF-CHECK RESULT:", "ALL PASS" if not fails else f"FAILS: {fails}")
