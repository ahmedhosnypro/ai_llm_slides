#!/usr/bin/env python3
"""Closed-loop check: 150dpi render_1.png (2001x1125) vs ORIGINAL slide_007.jpg
(960x540, 1px=1pt) measured geometry. Scale render->frame = 2001/960.
Asserts: L lines, inner frame, black strip, title box + title lines, domain boxes
+ label inks, arrow fan (band ink + head tips). Tolerance ~4px frame-space (8px render).
"""
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide007/render_1.png"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_007.jpg"

R = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
O = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
S = R.shape[1] / O.shape[1]  # 2.084
fails = []

def check(name, measured_frame, expected_frame, tol=4.0):
    ok = all(abs(m - e) <= tol for m, e in zip(measured_frame, expected_frame))
    status = "OK " if ok else "FAIL"
    print(f"[{status}] {name}: measured(frame-px) {['%.1f'%m for m in measured_frame]} vs expected {expected_frame} (tol {tol})")
    if not ok:
        fails.append(name)

def to_frame(vals):
    return [v / S for v in vals]

def red_mask(a, thr=120):
    return (a[..., 0] > thr) & (a[..., 1] < 110) & (a[..., 2] < 110)

def dark_mask(a, thr=80):
    lum = 0.299*a[...,0] + 0.587*a[...,1] + 0.114*a[...,2]
    return lum < thr

print(f"scale render->frame = {S:.4f}")

# --- outer L: top line (scan x400..600) ---
r_red = red_mask(R)
band = r_red[int(30*S):int(55*S), int(400*S):int(600*S)]
rows = np.where(band.any(axis=1))[0] + int(30*S)
if len(rows):
    f = to_frame([rows.min(), rows.max()])
    check("L top line y-span", f, [42, 44.5], tol=3)
# window y40.5..44 only (excludes the chrome panel top border at y44.5..45.5)
band = r_red[int(40.5*S):int(44*S), int(30*S):int(950*S)]
cols = np.where(band.any(axis=0))[0] + int(30*S)
if len(cols):
    f = to_frame([cols.min(), cols.max()])
    check("L top line x-span", f, [57, 903], tol=4.5)
# left line (window excludes the inner-frame stroke at x70)
band = r_red[int(60*S):int(200*S), int(50*S):int(66*S)]
cols = np.where(band.any(axis=0))[0] + int(50*S)
if len(cols):
    f = to_frame([cols.min(), cols.max()])
    check("L left line x-span", f, [57, 59.5], tol=3)
band = r_red[int(30*S):int(525*S), int(55*S):int(63*S)]
rows = np.where(band.any(axis=1))[0] + int(30*S)
if len(rows):
    f = to_frame([rows.min(), rows.max()])
    check("L left line y-span", f, [42, 517], tol=5)

# --- inner frame strokes (rows 200..400 for cols) ---
band = r_red[int(200*S):int(400*S), int(60*S):int(80*S)]
cols = np.where(band.any(axis=0))[0] + int(60*S)
if len(cols):
    f = to_frame([cols.min(), cols.max()])
    check("inner frame left stroke x", f, [70, 70.5], tol=2.5)
band = r_red[int(200*S):int(400*S), int(885*S):int(905*S)]
cols = np.where(band.any(axis=0))[0] + int(885*S)
if len(cols):
    f = to_frame([cols.min(), cols.max()])
    check("inner frame right stroke x", f, [894, 895.5], tol=2.5)
band = r_red[int(112*S):int(128*S), int(300*S):int(600*S)]
rows = np.where(band.any(axis=1))[0] + int(112*S)
if len(rows):
    f = to_frame([rows.min(), rows.max()])
    check("inner frame top stroke y", f, [119, 119.5], tol=2.5)
band = r_red[int(476*S):int(492*S), int(300*S):int(600*S)]
rows = np.where(band.any(axis=1))[0] + int(476*S)
if len(rows):
    f = to_frame([rows.min(), rows.max()])
    check("inner frame bottom stroke y", f, [483, 483.5], tol=2.5)

# --- black strip ---
r_dark = dark_mask(R, thr=60)
band = r_dark[int(500*S):R.shape[0], int(400*S):int(600*S)]
rows = np.where(band.any(axis=1))[0] + int(500*S)
f = to_frame([rows.min(), rows.max()])
check("black strip y-span", f, [519, 539], tol=4)
band = r_dark[int(525*S):int(535*S), 0:R.shape[1]]
cols = np.where(band.any(axis=0))[0]
f = to_frame([cols.min(), cols.max()])
check("black strip x-span", f, [38, 921], tol=4)

# --- title box ---
rows = np.where((dark_mask(R[int(128*S):int(250*S), int(300*S):int(670*S)], thr=60)).all(axis=1))[0] + int(128*S)
cols = np.where((dark_mask(R[int(140*S):int(250*S), int(250*S):int(720*S)], thr=60)).any(axis=0))[0] + int(250*S)
f = to_frame([rows.min(), rows.max(), cols.min(), cols.max()])
check("title box y/y/x/x", f, [136, 249, 296, 677], tol=4)

# title yellow lines
tb = R[int(136*S):int(250*S), int(296*S):int(678*S)]
ylw = (tb[...,0] > 200) & (tb[...,1] > 200) & (tb[...,2] < 120)
ys = np.where(ylw.any(axis=1))[0]
runs = []
st = ys[0]; pv = ys[0]
for y in ys[1:]:
    if y > pv + 3:
        runs.append((st, pv)); st = y
    pv = y
runs.append((st, pv))
print(f"title lines found: {len(runs)} (expect 3)")
for i, (exp) in enumerate([(155, 177), (184, 200), (212, 235)]):
    if i < len(runs):
        a, b = runs[i]
        f = to_frame([a + int(136*S), b + int(136*S)])
        check(f"title line {i+1} y-span", f, list(exp), tol=4.5)

# --- domain boxes ---
row = R[int(345*S)]
for (name, ref, lo, hi, exp) in [("blue",(2,0,167),80,290,(90,270)),("green",(10,135,59),290,495,(299,474)),
                                  ("brown",(111,59,2),495,695,(504,679)),("darkred",(159,0,0),700,888,(709,883))]:
    seg = row[int(lo*S):int(hi*S)]
    m = (np.abs(seg - np.array(ref)).sum(axis=1) < 90)
    xs = np.where(m)[0] + int(lo*S)
    if len(xs):
        f = to_frame([xs.min(), xs.max()])
        check(f"{name} box x-span", f, list(exp), tol=3)
col = R[:, int(95*S)]
m = (np.abs(col - np.array([2,0,167])).sum(axis=1) < 90)
ys = np.where(m)[0]
f = to_frame([ys.min(), ys.max()])
check("blue box y-span", f, [330, 441], tol=3)

# --- box label inks (white) ---
def white_runs(x0, x1, y0=332, y1=440):
    reg = R[int(y0*S):int(y1*S), int(x0*S):int(x1*S)]
    wm = (reg[...,0] > 200) & (reg[...,1] > 200) & (reg[...,2] > 200)
    ys = np.where(wm.any(axis=1))[0] + int(y0*S)
    if not len(ys): return []
    out = []; st = ys[0]; pv = ys[0]
    for y in ys[1:]:
        if y > pv + 3: out.append((st, pv)); st = y
        pv = y
    out.append((st, pv))
    return [(a/S, b/S) for (a, b) in out]

print("TS runs:", [(round(a,1), round(b,1)) for a, b in white_runs(92, 268)], "expect [(376,393)]")
print("CV runs:", [(round(a,1), round(b,1)) for a, b in white_runs(301, 472)], "expect [(363,384),(391,407)]")
print("NLP runs:", [(round(a,1), round(b,1)) for a, b in white_runs(711, 881)], "expect [(348,364),(377,398)*,(405,427)] (*cursor-free)")
# hard checks on key caps
ts = white_runs(92, 268)
if ts:
    check("TS cap top", [ts[0][0]], [376], tol=4)
cv = white_runs(301, 472)
if len(cv) >= 2:
    check("CV cap tops", [cv[0][0], cv[1][0]], [363, 391], tol=4.5)
nlp = white_runs(711, 881)
if len(nlp) >= 3:
    check("NLP cap tops (1st,3rd)", [nlp[0][0], nlp[2][0]], [348, 405], tol=4.5)

# --- arrows: fan band ink + head tips ---
band = r_red[int(252*S):int(314*S), int(90*S):int(880*S)]
n = int(band.sum())
print(f"arrow band red px (render): {n}")
if n < 400:
    fails.append("arrow band nearly empty")
# head tips at y~327 (allow band 322..332): expect 4 blobs near x 180/386.5/590/795
band2 = r_red[int(322*S):int(333*S), int(90*S):int(880*S)]
cols = np.where(band2.any(axis=0))[0] + int(90*S)
groups = []
if len(cols):
    st = cols[0]; pv = cols[0]
    for x in cols[1:]:
        if x > pv + int(6*S):
            groups.append((st, pv)); st = x
        pv = x
    groups.append((st, pv))
centers = [round(((a+b)/2)/S, 1) for a, b in groups]
print("head-tip column groups (frame x):", centers, "expect near [180, 386.5, 590, 795]")
if len(centers) != 4:
    fails.append(f"expected 4 head tips, found {len(centers)}")
else:
    check("head tips x", centers, [180, 386.5, 590, 795], tol=5)

print()
if fails:
    print("CLOSED-LOOP RESULT: FAIL —", len(fails), "issue(s):")
    for f in fails: print("  -", f)
    sys.exit(1)
print("CLOSED-LOOP RESULT: PASS (all measured elements within tolerance)")
