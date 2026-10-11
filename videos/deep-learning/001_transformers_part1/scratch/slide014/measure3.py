#!/usr/bin/env python3
"""Pass 3: circle-fit the arc, find gap/arrowhead/stroke; refine panel borders + figure rects."""
import numpy as np
from PIL import Image

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1"
frame = np.asarray(Image.open(f"{VID}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)

# ---------- arc circle fit (Kasa) ----------
R, G, B = frame[..., 0], frame[..., 1], frame[..., 2]
red = (R > 120) & (R - G > 60) & (R - B > 60)
ys, xs = np.where(red)
m = (xs >= 400) & (xs <= 520) & (ys >= 230) & (ys <= 380)
xs, ys = xs[m].astype(float), ys[m].astype(float)
A = np.c_[2 * xs, 2 * ys, np.ones(len(xs))]
b = xs**2 + ys**2
sol, *_ = np.linalg.lstsq(A, b, rcond=None)
cx, cy = sol[0], sol[1]
r = np.sqrt(sol[2] + cx**2 + cy**2)
print(f"arc circle fit: center=({cx:.2f},{cy:.2f}) r={r:.2f}")
rr = np.hypot(xs - cx, ys - cy)
ang = np.degrees(np.arctan2(-(ys - cy), xs - cx))
hist, _ = np.histogram(rr, bins=44, range=(0, 44))
print("radial hist (1px bins):", [int(v) for v in hist])
# angular coverage at 2-degree bins
h2, _ = np.histogram(ang, bins=180, range=(-180, 180))
occ = [i * 2 - 180 for i, v in enumerate(h2) if v > 2]
print(f"occupied 2deg bins: {occ[0]}..{occ[-1]}, count={len(occ)}")
gaps = []
prev = occ[0]
for a in occ[1:]:
    if a - prev > 2:
        gaps.append((prev + 2, a - 2))
    prev = a
print("gaps (deg, y-up):", gaps)
# arrowhead: per-4deg pixel count + radial band
for lo in range(-180, 180, 4):
    mm = (ang >= lo) & (ang < lo + 4)
    n = mm.sum()
    if n > 5:
        # pixels per degree of arc length at radius r
        expected = np.radians(4) * r * 3.2  # stroke ~3.2px thick baseline
        print(f"  [{lo:+4d},{lo+4:+4d}): n={n:4d} r=[{rr[mm].min():5.1f},{rr[mm].max():5.1f}] dens={n/expected:.2f}")

# stroke thickness estimate: robust band via percentiles away from ends
core = (np.abs(ang) > 60) & (np.abs(ang) < 150)
if core.sum() > 50:
    print(f"stroke band p5/p50/p95: {np.percentile(rr[core],5):.1f}/{np.percentile(rr[core],50):.1f}/{np.percentile(rr[core],95):.1f}")

# ---------- panel borders & refined figure rects ----------
def probe_row(y, x0, x1):
    row = frame[y, x0:x1]
    return [f"{p[0]:02X}{p[1]:02X}{p[2]:02X}" for p in row[::4]]

print("\nleft panel edge row y=300, x 88..135:", probe_row(300, 88, 135))
print("left panel top col x=250, y 100..150:", [f"{frame[y,250,0]:02X}{frame[y,250,1]:02X}{frame[y,250,2]:02X}" for y in range(100, 150, 2)])
print("right panel edge row y=310, x 470..500:", probe_row(310, 470, 500))
print("right panel right col x=893, y 300..320:", [f"{frame[y,893,0]:02X}{frame[y,893,1]:02X}{frame[y,893,2]:02X}" for y in range(300, 320, 2)])

def content_bbox_loose(x0, y0, x1, y1, tag):
    sub = frame[y0:y1, x0:x1]
    Rr, Gg, Bb = sub[..., 0], sub[..., 1], sub[..., 2]
    mx = np.maximum(np.maximum(Rr, Gg), Bb); mn = np.minimum(np.minimum(Rr, Gg), Bb)
    pastel = (mx - mn > 18) & (mx > 140)
    ink = (Rr < 120) & (Gg < 120) & (Bb < 120)
    m = pastel | ink
    ys2, xs2 = np.where(m)
    print(f"{tag}: content x[{xs2.min()},{xs2.max()}] y[{ys2.min()},{ys2.max()}] (panel {x1-x0}x{y1-y0})")

content_bbox_loose(95, 108, 411, 522, "left panel loose")
content_bbox_loose(478, 154, 892, 470, "right panel loose")

# check area just above figure inside left panel (should be pure white)
sub = frame[112:135, 100:405]
print("left panel top strip mean:", sub.mean(axis=(0, 1)).round(1))
sub2 = frame[158:180, 485:885]
print("right panel top strip mean:", sub2.mean(axis=(0, 1)).round(1))

# ---------- caption pixel rows (for font size calibration) ----------
def rowprofile(x0, x1, y0, y1, mask_fn, tag):
    sub = frame[y0:y1, x0:x1]
    m = mask_fn(sub)
    rows = m.sum(axis=1)
    nz = [(y0 + i, int(v)) for i, v in enumerate(rows) if v > 0]
    print(f"{tag}: rows {nz[0][0]}..{nz[-1][0]} peak={max(v for _, v in nz)}")

rowprofile(430, 780, 100, 150, lambda s: (s[..., 0] > 120) & (s[..., 0] - s[..., 1] > 60) & (s[..., 0] - s[..., 2] > 60), "red caption")
rowprofile(420, 920, 460, 540, lambda s: (s[..., 2] > 120) & (s[..., 2] - s[..., 0] > 60) & (s[..., 2] - s[..., 1] > 60), "blue takeaway")
rowprofile(150, 830, 40, 100, lambda s: (s[..., 0] > 120) & (s[..., 0] - s[..., 1] > 60) & (s[..., 0] - s[..., 2] > 60), "title")
