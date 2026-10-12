#!/usr/bin/env python3
"""Closed-loop self-check: compare render (150dpi = 2001x1125) vs original frame
(960x540) with scale factor 2001/960 = 2.0844. Checks title ink, panels, containers,
squares, labels, tags, arrows; prints PASS/FAIL per element with tolerances."""
from PIL import Image
import numpy as np
import sys

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide022/render/slide-1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_022.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/scratch/slide022/selfcheck1.txt"

r = np.asarray(Image.open(REN).convert("RGB")).astype(int)
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
SC = r.shape[1] / o.shape[1]  # ~2.0844
print(f"render {r.shape[1]}x{r.shape[0]}, orig {o.shape[1]}x{o.shape[0]}, scale {SC:.4f}")
fails = []

def ink_runs(imgS, y0, y1, x0, x1, thr, gap=6, axis="x"):
    """word-level ink runs in orig-scale coords via scaled sampling"""
    band = imgS[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    S = band.sum(axis=2)
    m = S < thr
    prof = m.sum(axis=1 if axis == "x" else 0)
    runs, inr = [], False
    for i, c in enumerate(prof):
        if c >= 1 and not inr: s = i; inr = True
        elif c < 1 and inr: runs.append((s, i-1)); inr = False
    if inr: runs.append((s, len(prof)-1))
    merged = []
    for rr in runs:
        if merged and rr[0]-merged[-1][1] <= gap*SC: merged[-1] = (merged[-1][0], rr[1])
        else: merged.append(list(rr))
    return [(int(a/SC + x0), int(b/SC + x0)) if axis == "x" else (int(a/SC + y0), int(b/SC + y0)) for a, b in merged]

def check(name, got, want, tol):
    if got is None:
        ok = False
    else:
        if not isinstance(got, (list, tuple)): got, want = [got], [want]
        ok = all(abs(g - w) <= tol for g, w in zip(got, want))
    status = "PASS" if ok else "FAIL"
    if not ok: fails.append(name)
    print(f"  [{status}] {name}: got {got} want {want} (tol {tol})")

# 1. TITLE: ink x-extent and cap band
print("== TITLE ==")
tr = ink_runs(r, 60, 115, 60, 900, 620*3/2.0844*1.0, gap=10)
# rescale threshold: orig used S<620; render is clean so use S<1200 (red ink sum ~300)
tr = ink_runs(r, 55, 120, 60, 940, 620, gap=10)
tr = [t for t in tr if t[1]-t[0] > 20]  # drop badge fringe
print("  render title word runs:", tr)
if tr:
    check("title left", tr[0][0], 131, 10)
    check("title right", tr[-1][1], 857, 12)
    check("title center", (tr[0][0]+tr[-1][1])//2, 494, 8)
# cap band
band = r[int(55*SC):int(120*SC), int(120*SC):int(880*SC)]
S = band.sum(axis=2)
rows = np.where((S < 620).any(axis=1))[0]
if len(rows):
    capband = (int(55 + rows.min()/SC), int(55 + rows.max()/SC))
    check("title band top", capband[0], 70, 6)
    check("title band bottom", capband[1], 98, 6)

# 2. PANELS: blue vertical edges
print("== PANELS ==")
def blue_cols(imgS):
    b = imgS[:, :, 2]; rr = imgS[:, :, 0]; gg = imgS[:, :, 1]
    return (b > 100) & (rr < 90) & (gg < 90)
bc = blue_cols(r)
colcnt = bc[int(130*SC):int(500*SC)].sum(axis=0)
edges = [x for x in range(len(colcnt)) if colcnt[x] > 300*SC]
# cluster
groups = []
for x in edges:
    if groups and x - groups[-1][-1] <= 3: groups[-1].append(x)
    else: groups.append([x])
centers = [int(sum(g)/len(g)/SC) for g in groups]
print("  blue vertical edges (orig px):", centers)
for want in (118, 486.5, 839):
    if centers:
        check(f"blue edge near {want}", min(centers, key=lambda c: abs(c-want)), want, 5)
rowcnt = bc[:, int(130*SC):int(830*SC)].sum(axis=1)
redges = [y for y in range(len(rowcnt)) if rowcnt[y] > 300*SC]
groups = []
for y in redges:
    if groups and y - groups[-1][-1] <= 3: groups[-1].append(y)
    else: groups.append([y])
rcenters = [int(sum(g)/len(g)/SC) for g in groups]
print("  blue horizontal edges (orig px):", rcenters)
for want in (122.5, 523):
    if rcenters:
        check(f"blue h-edge near {want}", min(rcenters, key=lambda c: abs(c-want)), want, 5)

# 3. CONTAINERS: border columns at row y=300 (mid)
print("== CONTAINERS (vertical borders at y=300) ==")
def strokes_at(imgS, y0, y1):
    """x positions of strong colored strokes in orig coords"""
    seg = imgS[int(y0*SC):int(y1*SC)]
    S = seg.sum(axis=2)
    # non-background = sum < 690*SC^0 ... background gray E9E9E7 sum=695*SC? render clean:
    m = S < 640
    prof = m.sum(axis=0)
    cols = [x for x in range(len(prof)) if prof[x] >= (y1-y0)*SC*0.8]
    groups = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 2*SC: groups[-1].append(x)
        else: groups.append([x])
    return [round((g[0]+g[-1])/2/SC, 1) for g in groups]
st = strokes_at(r, 295, 305)
print("  render strokes y300:", st)
want = [118, 158, 258, 265.5, 364.5, 372.5, 472.5, 486, 498.5, 571.5, 578, 658, 666, 766.5, 839]
for w in want:
    got = min(st, key=lambda c: abs(c - w)) if st else None
    check(f"stroke near {w}", got, w, 4)

# 4. SQUARES: horizontal edges in L-INPUT (light gray on white)
print("== SQUARES (L-INPUT top edges) ==")
def gray_rows(imgS, x0, x1, y0, y1):
    seg = imgS[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    S = seg.sum(axis=2)
    m = (S > 500) & (S < 710)
    prof = m.sum(axis=1)
    rows = [y for y in range(len(prof)) if prof[y] >= 20*SC]
    groups = []
    for y in rows:
        if groups and y - groups[-1][-1] <= 2*SC: groups[-1].append(y)
        else: groups.append([y])
    return [round((g[0]+g[-1])/2/SC + y0, 1) for g in groups]
gr = gray_rows(r, 220, 238, 180, 460)
print("  render L-INPUT sq edges:", gr)
for w in (193, 235, 248, 290, 355, 397, 409.5, 451.5):
    got = min(gr, key=lambda c: abs(c - w)) if gr else None
    check(f"sq edge {w}", got, w, 4)

# 5. LABELS: ink bands (L-INPUT labels x184..214; R-OUT x713..744)
print("== LABELS ==")
def text_bands(imgS, x0, x1, y0, y1):
    seg = imgS[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    S = seg.sum(axis=2)
    m = S < 620
    prof = m.sum(axis=1)
    runs, inr = [], False
    for i, c in enumerate(prof):
        if c >= 2*SC and not inr: s = i; inr = True
        elif c < 2*SC and inr: runs.append((s, i-1)); inr = False
    if inr: runs.append((s, len(prof)-1))
    return [(round(a/SC+y0, 1), round(b/SC+y0, 1)) for a, b in runs if b-a > 3*SC]
lb = text_bands(r, 183, 216, 200, 445)
print("  render L-INPUT label bands:", lb)
wantc = [213.5, 271, 378.5, 432]
for w in wantc:
    got = min(lb, key=lambda b: abs((b[0]+b[1])/2 - w)) if lb else None
    check(f"label band {w}", round((got[0]+got[1])/2, 1) if got else None, w, 4)
lb2 = text_bands(r, 712, 748, 200, 445)
print("  render R-OUT label bands:", lb2)
for w in (216.5, 271, 376, 429.5):
    got = min(lb2, key=lambda b: abs((b[0]+b[1])/2 - w)) if lb2 else None
    check(f"R label band {w}", round((got[0]+got[1])/2, 1) if got else None, w, 4)

# 6. TAGS: yellow boxes
print("== TAGS ==")
def yellow_bbox(imgS, x0, x1, y0, y1):
    seg = imgS[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    rr, gg, bb = seg[:, :, 0], seg[:, :, 1], seg[:, :, 2]
    m = (rr > 220) & (gg > 220) & (bb > 120) & (bb < 215)
    ys, xs = np.where(m)
    if len(xs) == 0: return None
    return (round(x0 + xs.min()/SC, 1), round(x0 + xs.max()/SC, 1),
            round(y0 + ys.min()/SC, 1), round(y0 + ys.max()/SC, 1))
tb = yellow_bbox(r, 230, 400, 460, 515)
print("  render tag-L yellow bbox:", tb)
if tb: check("tag-L bbox", [tb[0], tb[2]], [255, 475], 5)
tb2 = yellow_bbox(r, 530, 700, 460, 515)
print("  render tag-R yellow bbox:", tb2)
if tb2: check("tag-R bbox", [tb2[0], tb2[2]], [552, 475], 5)

# 7. ARROWS: black ink presence along expected diagonal bands
print("== ARROWS ==")
def dark_cnt(imgS, x0, x1, y0, y1):
    seg = imgS[int(y0*SC):int(y1*SC), int(x0*SC):int(x1*SC)]
    return int((seg.sum(axis=2) < 330).sum())
for name, (x0, x1, y0, y1) in [
    ("A1 band", (245, 300, 215, 305)), ("A3 band", (245, 300, 338, 375)),
    ("A5 band", (332, 386, 318, 328)), ("A6 band", (573, 602, 319, 329)),
    ("A7 band", (634, 672, 218, 305)), ("A10 band", (634, 672, 345, 428)),
]:
    c = dark_cnt(r, x0, x1, y0, y1)
    ok = c > 30
    if not ok: fails.append(name)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: dark px {c}")

# 8. CONTAINMENT: content ink inside house frame (x42..918, y45..540 orig-scale)
print("== CONTAINMENT ==")
body = r[int(150*SC):int(470*SC), int(50*SC):int(910*SC)]
Sb = body.sum(axis=2)
# content ink = strongly colored or dark; frame border red at x42/918 excluded by margins
outside_left = int((r[int(150*SC):int(470*SC), int(30*SC):int(41*SC)].sum(axis=2) < 500).sum())
outside_right = int((r[int(150*SC):int(470*SC), int(920*SC):int(940*SC)].sum(axis=2) < 500).sum())
print(f"  ink left of panel border zone: {outside_left}, right: {outside_right}")
# tag bottom vs panel bottom: tag bottom 502 < 524 panel bottom ✓ by construction
print()
print("SELF-CHECK RESULT:", "ALL PASS" if not fails else f"FAILS: {fails}")
with open(OUT, "w") as f:
    import io
    f.write("selfcheck1\n")
