#!/usr/bin/env python3
# m13_segfit.py — highlight pixels = those lying on the cb->O blend segment
# (kills thin-line JPEG noise); subpixel edges from coverage profiles.
import numpy as np
from PIL import Image
from scipy import ndimage

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
warp = np.asarray(Image.open(S + "/frame_warped_contentfit.png").convert("RGB"), dtype=np.float64)
frame = np.asarray(frame_im, dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")

O = np.array([240, 122, 2.])   # m10b: alpha 0.50 solution (fit err <=1.5 on clean pairs)
A = 0.50

rys, rxs = np.mgrid[220:1070, 1180:1920]
fxi = np.clip(np.round((rxs - ax) / sx).astype(int), 0, 959)
fyi = np.clip(np.round((rys - ay) / sy).astype(int), 0, 539)
cf = frame[fyi, fxi]; cb = render[rys, rxs]
dv = O[None, None, :] - cb
den = (dv * dv).sum(axis=2)
t = ((cf - cb) * dv).sum(axis=2) / np.maximum(den, 1e-9)
proj = t[..., None] * dv
off = np.sqrt(((cf - cb - proj) ** 2).sum(axis=2))
sig = np.sqrt(den)  # |O-cb|
hl = (t > A - 0.16) & (t < A + 0.16) & (off < 32) & (t * sig > 45)
print(f"highlight px: {hl.sum()}")

lab, n = ndimage.label(hl)
sizes = ndimage.sum(hl, lab, range(1, n + 1))
print("components:")
comps = []
for k in np.argsort(sizes)[::-1][:8]:
    if sizes[k] < 2500: break
    ys, xs = np.where(lab == k + 1)
    comps.append((xs.min() + 1180, xs.max() + 1180, ys.min() + 220, ys.max() + 220, int(sizes[k])))
    print(f"  n={int(sizes[k])} x {xs.min()+1180}..{xs.max()+1180} y {ys.min()+220}..{ys.max()+220}"
          f"  (pt x {(xs.min()+1180)*0.48:.1f}..{(xs.max()+1180)*0.48:.1f} y {(ys.min()+220)*0.48:.1f}..{(ys.max()+220)*0.48:.1f})")

# check alpha clustering inside comps
for (x0, x1, y0, y1, _) in comps:
    sel_t = t[y0 - 220:y1 - 220, x0 - 1180:x1 - 1180][hl[y0 - 220:y1 - 220, x0 - 1180:x1 - 1180]]
    print(f"  comp x{x0}..{x1}: t median {np.median(sel_t):.3f} (alpha), iqr {np.percentile(sel_t,25):.3f}..{np.percentile(sel_t,75):.3f}")

def cov_edges(x0, x1, y0, y1, pad=12):
    sub = hl[y0 - 220 - pad:y1 - 220 + pad, x0 - 1180 - pad:x1 - 1180 + pad]
    sm = ndimage.uniform_filter(sub.astype(float), 5)
    colcov = sm.mean(axis=0); rowcov = sm.mean(axis=1)
    def cross(prof, off):
        idx = np.where(prof > 0.5)[0]
        if len(idx) == 0: return None
        i0, i1 = idx[0], idx[-1]
        def interp(i, up):
            j = i - 1 if up else i + 1
            if j < 0 or j >= len(prof) or prof[i] == prof[j]: return off + i
            tt = (0.5 - prof[j]) / (prof[i] - prof[j])
            return off + j + tt
        return interp(i0, True), interp(i1, False)
    ch = cross(colcov, x0 - pad); cv = cross(rowcov, y0 - pad)
    f = 0.48
    if ch and cv:
        lx, rx_ = ch; ty, by = cv
        print(f"  comp x{x0}..{x1} y{y0}..{y1}: edges render L {lx:.1f} R {rx_:.1f} T {ty:.1f} B {by:.1f}"
              f"  -> PT x {lx*f:.2f}..{rx_*f:.2f} (w {(rx_-lx)*f:.2f}) y {ty*f:.2f}..{by*f:.2f} (h {(by-ty)*f:.2f})")
        return (lx * f, rx_ * f, ty * f, by * f)
    print(f"  comp x{x0}..{x1}: edge fail {ch} {cv}")
    return None

finals = []
for c in comps:
    r = cov_edges(*c[:4])
    if r: finals.append(r)
np.save(S + "/rects_segfit.npy", np.array(finals))
print("\nFINAL rects (build pt, x0 y0 x1 y1):")
for r in finals:
    print(f"  x {r[0]:.2f}..{r[1]:.2f}  y {r[2]:.2f}..{r[3]:.2f}  (w {r[1]-r[0]:.2f} h {r[3]-r[2]:.2f})")
