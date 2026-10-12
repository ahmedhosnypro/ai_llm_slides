#!/usr/bin/env python3
"""Second measurement pass: color dumps along rays + looser masks."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
CX, CY = 578.7, 283.9  # provisional center from pass 1

print("== ray color dump: phi=0 (+x) rad 120..330 step 3 ==")
for rad in range(120, 331, 3):
    x = int(round(CX + rad)); y = int(round(CY))
    print(f"rad {rad:3d} ({x},{y}):", tuple(A[y, x]))

print("\n== ray color dump: phi=90 (up) rad 120..330 step 3 ==")
for rad in range(120, 331, 3):
    x = int(round(CX)); y = int(round(CY - rad))
    print(f"rad {rad:3d} ({x},{y}):", tuple(A[y, x]))

print("\n== center neighborhood colors (rad 0..120 step 10, phi 0) ==")
for rad in range(0, 121, 10):
    x = int(round(CX + rad)); y = int(round(CY))
    print(f"rad {rad:3d}:", tuple(A[y, x]))

print("\n== chips: mint-ish mask (g-r>20, g-b>20, g>170) right half ==")
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
mint = (g - r > 20) & (g - b > 20) & (g > 170) & (np.arange(W)[None, :] > 380)
lbl, nlab = ndi.label(mint, structure=np.ones((3, 3)))
print("blobs:", nlab)
for i in range(1, nlab + 1):
    m = lbl == i
    if m.sum() < 100:
        continue
    ys, xs = np.where(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    xm, ym = xs - xs.mean(), ys - ys.mean()
    cov = np.cov(np.vstack([xm, ym]))
    evals, evecs = np.linalg.eigh(cov)
    v = evecs[:, np.argmax(evals)]
    ang = np.degrees(np.arctan2(-(v[1]), v[0]))
    if ang < 0:
        ang += 180
    cxp, cyp = xs.mean(), ys.mean()
    phi = np.degrees(np.arctan2(-(cyp - CY), cxp - CX))
    rad = np.hypot(cxp - CX, cyp - CY)
    elong = np.sqrt(evals.max() / max(evals.min(), 1e-6))
    print(f"chip {i}: n={m.sum()} center ({cxp:.1f},{cyp:.1f}) bbox x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) angle {ang:.1f} phi {phi:.1f} rad {rad:.1f} elong {elong:.1f}")
    print(f"    IN: center ({cxp/72:.4f},{cyp/72:.4f})in w {(x1-x0+1)/72:.4f} h {(y1-y0+1)/72:.4f} phi {phi:.2f} rad {rad/72:.4f}in")
    print(f"    fill sample ({int(cxp)},{int(cyp)}):", tuple(A[int(cyp), int(cxp)]), " border-left sample:", tuple(A[int(cyp), max(0, x0 - 2)]))

print("\n== arcs: orange-ish (r-b>50, r-g>50, r>140) whole right half ==")
orange = (r - b > 50) & (r - g > 50) & (r > 140) & (np.arange(W)[None, :] > 380)
lbl2, nlab2 = ndi.label(orange, structure=np.ones((3, 3)))
print("blobs:", nlab2)
for i in range(1, nlab2 + 1):
    m = lbl2 == i
    if m.sum() < 8:
        continue
    ys, xs = np.where(m)
    phis = np.degrees(np.arctan2(-(ys - CY), xs - CX))
    rads = np.hypot(xs - CX, ys - CY)
    print(f"orange {i}: n={m.sum()} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} phi {phis.min():.1f}..{phis.max():.1f} rad {rads.min():.1f}..{rads.max():.1f} med {np.median(rads):.1f}")

print("\n== red text anywhere (r>130,g<90,b<90) right half, blob list ==")
redm = (r > 130) & (g < 90) & (b < 90) & (np.arange(W)[None, :] > 380)
lbl3, nlab3 = ndi.label(redm, structure=np.ones((3, 3)))
print("blobs:", nlab3)
for i in range(1, nlab3 + 1):
    m = lbl3 == i
    if m.sum() < 8:
        continue
    ys, xs = np.where(m)
    print(f"red {i}: n={m.sum()} x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} center ({xs.mean():.0f},{ys.mean():.0f})")

print("\n== circle fill robust: histogram over disk r<100 ==")
yy, xx = np.mgrid[0:H, 0:W]
disk = (np.hypot(xx - CX, yy - CY) < 100)
px = A[disk]
med = np.median(px, axis=0)
print("disk median color:", med, " 25th/75th:", np.percentile(px, 25, axis=0), np.percentile(px, 75, axis=0))

print("\n== circle edge: along phi=45 find fill->outside transition ==")
a45 = np.radians(45)
prev = None
for rad in np.arange(100, 200, 1.0):
    x = int(round(CX + rad * np.cos(a45))); y = int(round(CY - rad * np.sin(a45)))
    c = tuple(A[y, x])
    if c != prev:
        print(f"rad {rad:.0f} ({x},{y}): {c}")
        prev = c

print("\n== circle top/bottom/left/right extremes (fill-ish pale yellow loose: r>230,g>230,150<b<225) ==")
pale = (r > 225) & (g > 225) & (b > 140) & (b < 228) & (np.arange(W)[None, :] > 380)
ys, xs = np.where(pale)
print("pale bbox x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max())
colc = pale[:, int(round(CX))]
rows_c = np.where(colc)[0]
print(f"vert extent through cx: {rows_c.min()}..{rows_c.max()} (center {(rows_c.min()+rows_c.max())/2:.1f}, r_v {(rows_c.max()-rows_c.min())/2:.1f})")
rowc = pale[int(round(CY)), :]
cols_c = np.where(rowc)[0]
print(f"horiz extent through cy: {cols_c.min()}..{cols_c.max()} (center {(cols_c.min()+cols_c.max())/2:.1f}, r_h {(cols_c.max()-cols_c.min())/2:.1f})")

print("\n== spokes: dump colors along phi=30 ray rad 130..330 step 2 (find dots) ==")
a30 = np.radians(30)
seq = []
for rad in np.arange(130, 331, 2.0):
    x = int(round(CX + rad * np.cos(a30))); y = int(round(CY - rad * np.sin(a30)))
    c = A[y, x]
    reddish = int(c[0]) - max(int(c[1]), int(c[2]))
    seq.append((rad, tuple(c), reddish))
hits = [s for s in seq if s[2] > 40]
print("reddish hits (rad, color):", [(f"{h[0]:.0f}", h[1]) for h in hits[:40]])

print("\n== +w label exact colors: sample around (816,227) 85%/42% ==")
for yy2 in range(215, 245, 3):
    row = []
    for xx2 in range(795, 845, 5):
        row.append(tuple(A[yy2, xx2]))
    print(yy2, row)
