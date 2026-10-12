#!/usr/bin/env python3
"""m27: rect extents/colors (eq3, eq4), L3 underline structure, stem-level italic test,
underline-under-gamma/beta, highlight fill modes."""
import numpy as np
from PIL import Image, ImageFont, ImageDraw

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_040.jpg").convert("RGB")
a = np.asarray(F).astype(int)
lum = (a[:, :, 0]*299 + a[:, :, 1]*587 + a[:, :, 2]*114)//1000

print("== A. eq3 rect: ASCII x150..315 y392..452 thr215 (edge-only view) ==")
for y in range(392, 453):
    row = "".join("#" if lum[y, x] < 130 else ("+" if lum[y, x] < 215 else ".") for x in range(150, 316))
    print(f"{y:3d} {row}")
print("edge-stroke colors:")
def sample_pts(pts, label):
    for (x, y) in pts:
        print(f"  {label} ({x},{y}): {tuple(a[y, x])}")
sample_pts([(200, 399), (250, 399), (289, 410), (289, 430), (170, 399), (160, 399), (155, 399)], "eq3 top edge y399")
sample_pts([(289, 446), (289, 451), (289, 399)], "eq3 right edge x289")

print()
print("== B. eq4 rect: ASCII x150..350 y446..480 thr215 ==")
for y in range(446, 481):
    row = "".join("#" if lum[y, x] < 130 else ("+" if lum[y, x] < 215 else ".") for x in range(150, 351))
    print(f"{y:3d} {row}")
sample_pts([(164, 460), (164, 470), (300, 452), (300, 475), (320, 452), (340, 452), (250, 452), (230, 452)], "eq4 edges")

print()
print("== C. L3 underline fine structure: per-row, x104..445, y174..190: count + mean color of dark px ==")
for y in range(174, 191):
    xs = np.where(lum[y, 104:445] < 200)[0]
    if len(xs):
        cols = a[y, 104:445][xs]
        print(f"  y={y}: n={len(xs)} x {xs.min()+104}..{xs.max()+104} mean={cols.mean(axis=0).round(0)}")
    else:
        print(f"  y={y}: -")

print()
print("== D. underline under gamma/and/beta: x528..615, y150..172 ==")
for y in range(150, 173):
    xs = np.where(lum[y, 528:616] < 200)[0]
    if len(xs):
        cols = a[y, 528:616][xs]
        print(f"  y={y}: n={len(xs)} x {xs.min()+528}..{xs.max()+528} mean={cols.mean(axis=0).round(0)}")

print()
print("== E. stem-level italic test: per-row run-centers in narrow windows ==")
def stems(x0, x1, y0, y1, label, thr=185):
    print(f"-- {label} x{x0}..{x1} y{y0}..{y1}")
    for y in range(y0, y1):
        xs = np.where(lum[y, x0:x1] < thr)[0]
        if len(xs) == 0:
            print(f"  y={y}: -"); continue
        runs = []
        start = xs[0]; prev = xs[0]
        for v in xs[1:]:
            if v > prev + 1:
                runs.append((start + x0, prev + x0)); start = v
            prev = v
        runs.append((start + x0, prev + x0))
        cs = [f"{(r[0]+r[1])/2:.1f}" for r in runs]
        print(f"  y={y}: runs {[(r[0], r[1]) for r in runs]}")
stems(633, 642, 119, 134, "'m' left stem of mean (blue)")
stems(703, 712, 116, 134, "'d' stem of and L1 (blue)")
stems(575, 585, 116, 136, "'t' stem of strictly")
stems(609, 618, 140, 158, "'h' stem of that (black ctrl)")
stems(693, 701, 142, 160, "'t' stem of convert (red)")
stems(130, 138, 165, 190, "'i' stem of variance L3 (red)")
stems(315, 324, 165, 190, "'M' left stem of Minimizes")
stems(407, 415, 169, 190, "'L' stem of Loss.")
stems(105, 113, 115, 133, "'I' of Instead (ctrl)")

print()
print("== F. reference calibration: PIL-render 'mean' & 'mean' italic Times 20px, same slope test ==")
def ref_slant(italic):
    W, H = 400, 120
    im = Image.new("L", (W, H), 255)
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("/usr/share/fonts/TTF/Times_New_Roman_TTF/TimesNewRoman.ttf" if not italic
                               else "/usr/share/fonts/TTF/Times_New_Roman_TTF/TimesNewRoman-Italic.ttf", 100)
    except OSError:
        import glob
        cand = glob.glob("/usr/share/fonts/**/*imes*oman*", recursive=True) + glob.glob("/usr/share/fonts/**/*Liberation*Serif*", recursive=True)
        if not cand:
            print("  no Times/Liberation Serif found"); return
        path = [c for c in cand if "talic" in c or "Italic" in c] if italic else [c for c in cand if "talic" not in c and "Italic" not in c]
        f = ImageFont.truetype(path[0] if path else cand[0], 100)
    d.text((30, 10), "mean", font=f, fill=0)
    arr = np.asarray(im).astype(int)
    rows = []
    for y in range(H):
        xs = np.where(arr[y] < 128)[0]
        if len(xs) >= 2:
            rows.append((y, xs.mean()))
    ys = np.array([r[0] for r in rows], float); cs = np.array([r[1] for r in rows], float)
    lo, hi = np.percentile(ys, 15), np.percentile(ys, 85)
    m = (ys >= lo) & (ys <= hi)
    A = np.vstack([ys[m] - ys[m].mean(), np.ones(m.sum())]).T
    slope = np.linalg.lstsq(A, cs[m], rcond=None)[0][0]
    print(f"  reference {'ITALIC' if italic else 'roman'} 'mean': slope={slope:+.3f} px/px (frame px = pt here)")
import glob, os
print("font candidates:", glob.glob("/usr/share/fonts/**/*iberation*erif*", recursive=True)[:4])
ref_slant(False)
ref_slant(True)

print()
print("== G. eq4 gamma/beta highlight fill modes ==")
def modecol(x0, x1, y0, y1, lmin=140, lmax=256, label=""):
    box = a[y0:y1, x0:x1].reshape(-1, 3)
    L = (box[:, 0]*299 + box[:, 1]*587 + box[:, 2]*114)//1000
    sel = box[(L >= lmin) & (L < lmax)]
    if len(sel) == 0:
        print(f"  {label}: none"); return
    q = (sel//8)*8
    keys, counts = np.unique(q, axis=0, return_counts=True)
    m = keys[counts.argmax()]
    print(f"  {label}: mode {tuple(int(v) for v in m)} (n={int(counts.max())} of {len(sel)})")
modecol(213, 224, 455, 470, label="eq4 gamma hl")
modecol(262, 273, 455, 470, label="eq4 beta hl")
modecol(392, 530, 146, 158, label="intro learn-params hl (wide)")
modecol(206, 424, 228, 248, label="panel params hl (wide)")
modecol(459, 546, 412, 431, label="// normalize pink")
modecol(427, 546, 453, 472, label="// scale orange")
modecol(166, 190, 456, 472, label="ellipse interior")
