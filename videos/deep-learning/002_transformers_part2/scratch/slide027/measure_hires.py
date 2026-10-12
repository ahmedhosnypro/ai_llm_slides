#!/usr/bin/env python3
"""Measure the native 1280x720 frame: arrowhead apex directions, spoke dash
pattern/color, arc radius, center blob, cursor, refined circle."""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/hi_res_1545.png").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
S = 1280 / 960.0
CX, CY = 578.5 * S, 283.5 * S  # (771.3, 378.0)
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]

print("== refine circle: outline ring along 8 rays ==")
for phi in (0, 45, 90, 135, 180, 225, 270, 315):
    aa = np.radians(phi)
    rads = []
    for rad in np.arange(150, 190, 0.5):
        x = int(round(CX + rad * np.cos(aa)))
        y = int(round(CY - rad * np.sin(aa)))
        c = A[y, x]
        if c.sum() < 560 and abs(int(c[0]) - int(c[1])) < 30:
            rads.append(rad)
    if rads:
        print(f"phi {phi}: outline rad {min(rads):.1f}..{max(rads):.1f} (n={len(rads)})")

print("\n== chips hi-res (mint mask) ==")
mint = (g - r > 20) & (g - b > 20) & (g > 170) & (np.arange(W)[None, :] > 380 * S)
lbl, nlab = ndi.label(mint, structure=np.ones((3, 3)))
chips = []
for i in range(1, nlab + 1):
    m = lbl == i
    if m.sum() < 200:
        continue
    ys, xs = np.where(m)
    cxp, cyp = xs.mean(), ys.mean()
    phi = np.degrees(np.arctan2(-(cyp - CY), cxp - CX))
    rad = np.hypot(cxp - CX, cyp - CY)
    chips.append((phi, cxp, cyp, xs.min(), xs.max(), ys.min(), ys.max(), rad, m.sum()))
for phi, cxp, cyp, x0, x1, y0, y1, rad, n in sorted(chips):
    print(f"chip phi {phi:6.2f}: center ({cxp:.1f},{cyp:.1f}) bbox x{x0}..{x1} y{y0}..{y1} rad {rad:.1f} n={n} | 960-scale center ({cxp/S:.1f},{cyp/S:.1f}) rad {rad/S:.1f}")

print("\n== arrowheads hi-res: blob + apex (farthest px from centroid) ==")
orange = (r - (g + b) / 2 > 25) & (r > 150)
lbl2, nlab2 = ndi.label(orange, structure=np.ones((3, 3)))
for i in range(1, nlab2 + 1):
    m = lbl2 == i
    if m.sum() < 40:
        continue
    ys, xs = np.where(m)
    cxp, cyp = xs.mean(), ys.mean()
    rad = np.hypot(xsp := xs - CX, ysp := ys - CY)
    phi = np.degrees(np.arctan2(-ysp, xsp))
    if not (180 < np.median(rad) < 260):
        continue
    d2 = (xs - cxp) ** 2 + (ys - cyp) ** 2
    j = np.argmax(d2)
    ax, ay = xs[j], ys[j]
    # apex direction relative to circle center
    phi_apex = np.degrees(np.arctan2(-(ay - CY), ax - CX))
    rad_apex = np.hypot(ax - CX, ay - CY)
    v = (ax - cxp, ay - cyp)
    print(f"AH blob: n={m.sum()} centroid ({cxp:.1f},{cyp:.1f}) phi {np.median(phi):.1f} rad {np.median(rad):.1f} | apex ({ax},{ay}) d=({v[0]:.1f},{v[1]:.1f}) phi_apex {phi_apex:.1f} rad_apex {rad_apex:.1f}")

print("\n== arc trace hi-res: orange px in annulus rad 250..320, excluding AH/label boxes ==")
lab_boxes = [(826 * S, 226 * S, 30), (778 * S, 99.5 * S, 30), (636.5 * S, 72 * S, 30), (519 * S, 72 * S, 30)]
pts = []
for phi10 in range(-200, 1401, 5):
    phi = phi10 / 10.0
    aa = np.radians(phi)
    for rad in np.arange(240, 330, 1.0):
        x = int(round(CX + rad * np.cos(aa)))
        y = int(round(CY - rad * np.sin(aa)))
        if not (0 <= x < W and 0 <= y < H):
            continue
        if any(np.hypot(x - lx, y - ly) < lr for lx, ly, lr in lab_boxes):
            continue
        c = A[y, x]
        om = c[0] - (c[1] + c[2]) / 2.0
        if om > 30 and c[0] > 150:
            pts.append((phi, rad, om))
if pts:
    rads = np.array([p[1] for p in pts])
    phis = np.array([p[0] for p in pts])
    print(f"arc pts n={len(pts)} rad med {np.median(rads):.1f} (10-90pct {np.percentile(rads,10):.1f}..{np.percentile(rads,90):.1f})")
    hist = {}
    for p, rd, _ in pts:
        hist.setdefault(round(p / 5) * 5, []).append(rd)
    for k in sorted(hist):
        v = hist[k]
        print(f"  phi {k:4d}..{k+5}: n={len(v):3d} rad {np.median(v):6.1f}")

print("\n== spokes hi-res: along-ray darkness (d = dark vs panel) at 12 angles ==")
panel = np.array([233, 233, 231])
for phi in range(0, 360, 30):
    aa = np.radians(phi)
    prof = []
    for rad in np.arange(170, 340, 2.0):
        best = 0
        for off in np.arange(-3, 3.1, 1.0):
            x = int(round(CX + rad * np.cos(aa) - off * np.sin(aa)))
            y = int(round(CY - rad * np.sin(aa) - off * np.cos(aa)))
            c = A[y, x].astype(int)
            d = int(np.abs(c - panel).sum())
            best = max(best, d)
        prof.append(best)
    # summarize: ranges where d>40
    segs = []
    s = None
    for i, v in enumerate(prof):
        rr = 170 + i * 2
        if v > 40 and s is None:
            s = rr
        elif v <= 40 and s is not None:
            segs.append((s, rr - 2)); s = None
    if s is not None:
        segs.append((s, 338))
    print(f"phi {phi:3d}: dark segs (960-scale) {[(round(a/S), round(bb/S)) for a, bb in segs]}")

print("\n== spoke perpendicular profile hi-res (phi=0 at x=1100, y 374..384; phi=180 at x=420) ==")
for x in range(1094, 1107):
    print(f" x={x}:", tuple(A[378, x]))
for x in range(414, 427):
    print(f" x={x} (left):", tuple(A[378, x]))

print("\n== spoke dot pitch: phi=0 darkness along y=378, x 1080..1195 step 2 (d) ==")
vals = []
for x in range(1080, 1196, 2):
    c = A[378, x].astype(int)
    vals.append((x, int(np.abs(c - panel).sum())))
print(" ".join(f"{x}:{d}" for x, d in vals))

print("\n== center region hi-res: dark+warm map x 735..810 y 345..420 ==")
for y in range(345, 421, 2):
    line = ""
    for x in range(735, 811):
        c = A[y, x]
        dk = int(np.abs(c.astype(int) - panel).sum())
        dark = c[0] < 140 and c[1] < 140 and c[2] < 140
        warm = (int(c[0]) - int(c[2])) > 45 and c[0] > 170
        line += "@" if dark else ("o" if warm else ("." if dk > 40 else " "))
    print(f"{y:3d} {line}")

print("\n== cursor: dark pixels inside disk rad<210 ==")
yy, xx = np.mgrid[0:H, 0:W]
disk = (np.hypot(xx - CX, yy - CY) < 215)
darkpix = disk & (r < 130) & (g < 130) & (b < 130)
ys, xs = np.where(darkpix)
if len(ys):
    print(f"dark bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} n={len(ys)} | 960-scale ({xs.min()/S:.0f}..{xs.max()/S:.0f}, {ys.min()/S:.0f}..{ys.max()/S:.0f})")
else:
    print("no dark pixels in disk")
