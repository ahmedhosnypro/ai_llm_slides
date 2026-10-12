#!/usr/bin/env python3
"""PIL/numpy measurement of slide_027.jpg (960x540, 1px = 1pt = 1/72 in).

Measures every content block for the recreation:
  title lines, equation box, circle, spokes, word chips, arcs, +w labels, letterbox.
Prints frame-px values AND inches (/72).
"""
import numpy as np
from PIL import Image

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
H, W = A.shape[:2]
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
print(f"frame {W}x{H}")


def bbox_of(mask):
    ys, xs = np.where(mask)
    if not len(ys):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(mask.sum())


def rep(name, bb):
    if bb is None:
        print(f"{name}: NONE")
        return
    x0, y0, x1, y1, n = bb
    print(f"{name}: x {x0}..{x1} y {y0}..{y1}  (w {x1-x0+1} h {y1-y0+1}) n={n}  | in: x {x0/72:.3f}..{x1/72:.3f} y {y0/72:.3f}..{(y1+1)/72:.3f} w {(x1-x0+1)/72:.3f} h {(y1-y0+1)/72:.3f}")


# ---------- letterbox check ----------
print("\n== bottom rows darkness ==")
for row in (515, 518, 520, 525, 530, 535, 538):
    dark = (r[row] < 60).sum()
    print(f"row {row}: dark px {dark}")

# ---------- circle (pale yellow FBFCC9 ~ (251,252,201)), right side ----------
print("\n== circle ==")
circ = (abs(r - 251) < 14) & (abs(g - 252) < 14) & (abs(b - 201) < 25) & (np.arange(W)[None, :] > 350)
rep("circle blob", bbox_of(circ))
cy_m, cx_m = np.where(circ)
cx = cx_m.mean(); cy = cy_m.mean()
print(f"circle centroid px ({cx:.1f},{cy:.1f})  in ({cx/72:.3f},{cy/72:.3f})")
# radius from area and from horizontal/vertical extent through centroid
area = circ.sum()
rad_area = np.sqrt(area / np.pi)
row_c = circ[int(round(cy)), :]
col_c = circ[:, int(round(cx))]
rad_h = (np.where(row_c)[0].max() - np.where(row_c)[0].min()) / 2
rad_v = (np.where(col_c)[0].max() - np.where(col_c)[0].min()) / 2
print(f"radius: area {rad_area:.1f}px  horiz {rad_h:.1f}px  vert {rad_v:.1f}px")
# circle outline color: sample just outside the fill along +x
xs_row = np.where(row_c)[0]
edge_x = xs_row.max() + 3
print(f"outline sample at ({edge_x},{int(cy)}):", A[int(cy), edge_x], " fill sample:", A[int(cy), int(cx)])

# ---------- equation box (FFFFCC ~ (255,255,204)), left side ----------
print("\n== equation box ==")
eq = (abs(r - 255) < 10) & (abs(g - 255) < 10) & (abs(b - 204) < 22) & (np.arange(W)[None, :] < 350) & (np.arange(H)[:, None] > 140)
rep("equation box fill", bbox_of(eq))
# border color: sample ring just outside fill bbox
ebb = bbox_of(eq)
if ebb:
    x0, y0, x1, y1, _ = ebb
    print("border samples:")
    for dx, dy, tag in ((x0 - 3, (y0 + y1) // 2, "left"), (x1 + 3, (y0 + y1) // 2, "right"), ((x0 + x1) // 2, y0 - 3, "top"), ((x0 + x1) // 2, y1 + 3, "bottom")):
        print(f"  {tag} ({dx},{dy}):", A[dy, dx])
    # text ink inside box: blue/red/green
    sub = A[y0:y1 + 1, x0:x1 + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    blue = (sb > 120) & (sr < 110) & (sg < 110)
    redt = (sr > 140) & (sg < 90) & (sb < 90)
    grnt = (sg > 100) & (sr < 110) & (sb < 110)
    for nm, m in (("blue", blue), ("red", redt), ("green", grnt)):
        bb2 = bbox_of(m)
        if bb2:
            x0b, y0b, x1b, y1b, _ = bb2
            print(f"  ink {nm}: rel y {y0b}..{y1b} rel x {x0b}..{x1b} (abs y {y0+y0b}..{y0+y1b}, abs x {x0+x0b}..{x0+x1b}) n={bb2[4]}")
    # per-row ink profile to find line bands
    ink_any = blue | redt | grnt
    rows_ink = np.where(ink_any.sum(axis=1) > 0)[0]
    if len(rows_ink):
        bands = []
        s = p = rows_ink[0]
        for v in rows_ink[1:]:
            if v == p + 1:
                p = v
            else:
                bands.append((s, p)); s = p = v
        bands.append((s, p))
        print("  text line bands (abs y):", [(y0 + s, y0 + e) for s, e in bands])

# ---------- title (red CC0000-ish text, top-left) ----------
print("\n== title ==")
tit = (r > 130) & (g < 80) & (b < 80) & (np.arange(W)[None, :] < 400) & (np.arange(H)[:, None] < 180)
rows_t = np.where(tit.sum(axis=1) > 0)[0]
bands = []
if len(rows_t):
    s = p = rows_t[0]
    for v in rows_t[1:]:
        if v == p + 1:
            p = v
        else:
            bands.append((s, p)); s = p = v
    bands.append((s, p))
for i, (s, e) in enumerate(bands):
    band = tit[s:e + 1, :]
    xs = np.where(band.sum(axis=0) > 0)[0]
    print(f"title line {i+1}: y {s}..{e} (h {e-s+1}) x {xs.min()}..{xs.max()} | in: y {s/72:.3f}..{(e+1)/72:.3f} x {xs.min()/72:.3f}..{(xs.max()+1)/72:.3f}")

# ---------- word chips (mint CCFFCC) ----------
print("\n== word chips ==")
chips = (abs(r - 204) < 22) & (g > 225) & (abs(b - 204) < 22) & (np.arange(W)[None, :] > 380)
from scipy import ndimage as ndi
lbl, nlab = ndi.label(chips)
print(f"chip blobs: {nlab}")
for i in range(1, nlab + 1):
    m = lbl == i
    if m.sum() < 60:
        continue
    ys, xs = np.where(m)
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # PCA for orientation
    xm, ym = xs - xs.mean(), ys - ys.mean()
    cov = np.cov(np.vstack([xm, ym]))
    evals, evecs = np.linalg.eigh(cov)
    v = evecs[:, np.argmax(evals)]
    ang = np.degrees(np.arctan2(-(v[1]), v[0]))  # CCW angle from +x, screen y down
    if ang < 0:
        ang += 180
    cxp, cyp = xs.mean(), ys.mean()
    # angular position rel circle center
    phi = np.degrees(np.arctan2(-(cyp - cy), cxp - cx))
    rad = np.hypot(cxp - cx, cyp - cy)
    print(f"chip {i}: center ({cxp:.1f},{cyp:.1f}) bbox x{x0}..{x1} y{y0}..{y1} (w{x1-x0+1} h{y1-y0+1}) pca_angle {ang:.1f}  phi {phi:.1f} rad {rad:.1f}")
    print(f"    in: center ({cxp/72:.3f},{cyp/72:.3f}) w {(x1-x0+1)/72:.3f} h {(y1-y0+1)/72:.3f} phi {phi:.1f} rad {rad/72:.3f}in")
    # border color sample
    print(f"    border sample ({x0-2},{int(cyp)}):", A[int(cyp), max(0, x0 - 2)])

# ---------- arcs (orange E06010) ----------
print("\n== arcs (orange) ==")
arc = (r > 170) & (r < 250) & (g > 60) & (g < 140) & (b < 70) & (np.arange(W)[None, :] > 380)
lbl2, nlab2 = ndi.label(arc)
print(f"orange blobs: {nlab2}")
for i in range(1, nlab2 + 1):
    m = lbl2 == i
    if m.sum() < 15:
        continue
    ys, xs = np.where(m)
    phis = np.degrees(np.arctan2(-(ys - cy), xs - cx))
    rads = np.hypot(xs - cx, ys - cy)
    print(f"orange blob {i}: n={m.sum()} bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} phi {phis.min():.1f}..{phis.max():.1f} rad {rads.min():.1f}..{rads.max():.1f} (med {np.median(rads):.1f})")

# ---------- +w labels (red bold text outside circle) ----------
print("\n== +w labels ==")
# red text CC0000: strong red, low g/b, OUTSIDE the circle area, right half
yy, xx = np.mgrid[0:H, 0:W]
outside = np.hypot(xx - cx, yy - cy) > (rad_area + 15)
lab_red = (r > 150) & (g < 70) & (b < 70) & outside & (xx > 380)
lbl3, nlab3 = ndi.label(lab_red)
print(f"red-outside blobs: {nlab3}")
groups = []
for i in range(1, nlab3 + 1):
    m = lbl3 == i
    if m.sum() < 12:
        continue
    ys, xs = np.where(m)
    groups.append((xs.mean(), ys.mean(), xs.min(), xs.max(), ys.min(), ys.max(), m.sum()))
# merge blobs within 30px into label clusters
merged = []
used = [False] * len(groups)
for i, gi in enumerate(groups):
    if used[i]:
        continue
    gx, gy = gi[0], gi[1]
    cluster = [gi]
    used[i] = True
    changed = True
    while changed:
        changed = False
        for j, gj in enumerate(groups):
            if used[j]:
                continue
            if any(abs(gj[0] - c[0]) < 35 and abs(gj[1] - c[1]) < 35 for c in cluster):
                cluster.append(gj)
                used[j] = True
                changed = True
    xs0 = min(c[2] for c in cluster); xs1 = max(c[3] for c in cluster)
    ys0 = min(c[4] for c in cluster); ys1 = max(c[5] for c in cluster)
    merged.append((xs0, xs1, ys0, ys1, sum(c[6] for c in cluster)))
for xs0, xs1, ys0, ys1, n in sorted(merged, key=lambda t: -t[4]):
    cxl, cyl = (xs0 + xs1) / 2, (ys0 + ys1) / 2
    print(f"+w label cluster: x {xs0}..{xs1} y {ys0}..{ys1} (w {xs1-xs0+1} h {ys1-ys0+1}) n={n} center ({cxl:.0f},{cyl:.0f}) in ({cxl/72:.3f},{cyl/72:.3f})")

# ---------- spokes: sample along rays ----------
print("\n== spokes (red dotted along rays from center) ==")
spoke_red = (r > 150) & (g > 15) & (g < 110) & (b < 90)
for phi in range(0, 360, 30):
    a = np.radians(phi)
    hits = []
    for rad in np.arange(5, 320, 0.5):
        x = int(round(cx + rad * np.cos(a)))
        y = int(round(cy - rad * np.sin(a)))
        if 0 <= x < W and 0 <= y < H and spoke_red[y, x]:
            hits.append(rad)
    if hits:
        runs2 = []
        s = p = hits[0]
        for v in hits[1:]:
            if v - p <= 2.0:
                p = v
            else:
                runs2.append((s, p)); s = p = v
        runs2.append((s, p))
        seg = ", ".join(f"{s0:.0f}-{s1:.0f}" for s0, s1 in runs2[:8])
        print(f"phi {phi:3d}: red hits {len(hits)} max {max(hits):.0f} runs: {seg}")
    else:
        print(f"phi {phi:3d}: no red hits")

# badge in frame (for reference only — house chrome is fixed)
print("\n== frame badge (reference) ==")
badge = (r > 200) & (g > 200) & (b < 190) & (np.arange(W)[None, :] > 800) & (np.arange(H)[:, None] < 160)
rep("badge yellow", bbox_of(badge))
