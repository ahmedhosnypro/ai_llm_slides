#!/usr/bin/env python3
# m11_delta.py — delta-mask rectangles (|cf-cb| threshold) with subpixel edges;
# title-ink and block-arrow bbox comparison frame vs render.
import numpy as np
from PIL import Image
from scipy import ndimage

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
frame = np.asarray(frame_im, dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")
W, H = render.shape[1], render.shape[0]

warp = np.asarray(frame_im.transform((W, H), Image.AFFINE,
    (1 / sx, 0, -ax / sx, 0, 1 / sy, -ay / sy), resample=Image.BILINEAR), dtype=np.float64)
Image.fromarray(warp.astype(np.uint8)).save(S + "/frame_warped_contentfit.png")

# --- delta mask in the right panel ---
d = np.abs(warp - render).sum(axis=2)
dm = np.zeros_like(d, bool)
dm[540:900, 1195:1875] = d[540:900, 1195:1875] > 110
dm = ndimage.median_filter(dm, 3)
dm = ndimage.binary_closing(dm, iterations=2)
dm = ndimage.binary_opening(dm, iterations=1)
lab, n = ndimage.label(dm)
sizes = ndimage.sum(dm, lab, range(1, n + 1))
print("delta components (right panel, render px):")
comps = []
for k in np.argsort(sizes)[::-1][:8]:
    if sizes[k] < 2000: break
    ys, xs = np.where(lab == k + 1)
    comps.append((xs.min(), xs.max(), ys.min(), ys.max(), int(sizes[k])))
    print(f"  n={int(sizes[k])} x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")

# subpixel edges via coverage profile crossings
def cov_edges(x0, x1, y0, y1):
    sub = dm[y0:y1 + 1, x0:x1 + 1]
    colcov = sub.mean(axis=0); rowcov = sub.mean(axis=1)
    def cross(prof, off):
        idx = np.where(prof > 0.5)[0]
        i0, i1 = idx[0], idx[-1]
        def interp(i, up):
            j = i - 1 if up else i + 1
            if j < 0 or j >= len(prof) or prof[i] == prof[j]: return off + i
            t = (0.5 - prof[j]) / (prof[i] - prof[j])
            return off + j + t
        return interp(i0, True), interp(i1, False)
    lx, rx_ = cross(colcov, x0)
    ty, by = cross(rowcov, y0)
    return lx, rx_, ty, by

rects = []
for (x0, x1, y0, y1, _) in comps:
    lx, rx_, ty, by = cov_edges(x0, x1, y0, y1)
    f = 0.48
    rects.append((lx * f, rx_ * f, ty * f, by * f))
    print(f"  -> subpixel render ({lx:.1f},{rx_:.1f},{ty:.1f},{by:.1f}) BUILD PT x {lx*f:.2f}..{rx_*f:.2f} "
          f"(w {(rx_-lx)*f:.2f}) y {ty*f:.2f}..{by*f:.2f} (h {(by-ty)*f:.2f})")

# --- title ink comparison ---
def redmask(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 140) & (r - (g + b) / 2 > 45)
tr = redmask(render)[100:200, 500:1700]
tw = redmask(warp)[100:200, 500:1700]
for nm, m in [("render", tr), ("frame", tw)]:
    ys, xs = np.where(m)
    print(f"title {nm}: ink x {xs.min()+500}..{xs.max()+500} y {ys.min()+100}..{ys.max()+100} n={len(xs)}")
# column profile crossing for left/right title edges (subpixel)
for nm, m in [("render", tr), ("frame", tw)]:
    colcov = m.mean(axis=0); rowcov = m.mean(axis=1)
    xs = np.where(colcov > 0.02)[0]; ys = np.where(rowcov > 0.02)[0]
    print(f"  {nm} cov>2%: x {xs[0]+500}..{xs[-1]+500}, y {ys[0]+100}..{ys[-1]+100}")

# --- block arrow comparison ---
ar = redmask(render)[540:700, 880:1130]
aw = redmask(warp)[540:700, 880:1130]
for nm, m in [("render", ar), ("frame", aw)]:
    ys, xs = np.where(m)
    if len(xs):
        print(f"arrow {nm}: ink x {xs.min()+880}..{xs.max()+880} y {ys.min()+540}..{ys.max()+540} n={len(xs)}")
        colcov = m.mean(axis=0); rowcov = m.mean(axis=1)
        xs2 = np.where(colcov > 0.05)[0]; ys2 = np.where(rowcov > 0.05)[0]
        print(f"  cov>5%: x {xs2[0]+880}..{xs2[-1]+880} (pt {(xs2[0]+880)*0.48:.1f}..{(xs2[-1]+880)*0.48:.1f}), "
              f"y {ys2[0]+540}..{ys2[-1]+540} (pt {(ys2[0]+540)*0.48:.1f}..{(ys2[-1]+540)*0.48:.1f})")
