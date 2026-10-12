#!/usr/bin/env python3
# m7_refgeom.py — reference geometry from the certified render + clean (alpha, color)
# regression + subpixel highlight edges in frame space.
import numpy as np
from PIL import Image
from scipy import ndimage

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
frame = np.asarray(frame_im, dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")
W, H = render.shape[1], render.shape[0]

def to_frame_pts(rx, ry):
    return (rx - ax) / sx, (ry - ay) / sy

def to_render_px(fx, fy):
    return ax + sx * fx, ay + sy * fy

# ---------- 1. reference geometry in the render ----------
def colmask(a, hexcol, tol=18):
    c = np.array([int(hexcol[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float64)
    return np.abs(a - c[None, None, :]).sum(axis=2) < tol * 3

RP = (slice(230, 1060), slice(1190, 1910))  # right panel interior
print("== render reference geometry (render px / build pt) ==")
for name, hexcol in [("peach FDEDDD", "FDEDDD"), ("mint CEFFE1", "CEFFE1"),
                     ("yellow F5E6A8", "F5E6A8"), ("white card", "FFFFFF")]:
    m = colmask(render, hexcol)
    mm = np.zeros_like(m); mm[RP] = m[RP]
    lab, n = ndimage.label(mm)
    if n == 0:
        print(f"  {name}: none"); continue
    sizes = ndimage.sum(mm, lab, range(1, n + 1))
    for k in np.argsort(sizes)[::-1][:4]:
        if sizes[k] < 800: break
        ys, xs = np.where(lab == k + 1)
        print(f"  {name}: n={int(sizes[k])} x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}"
              f"  (pt x {xs.min()*0.48:.1f}..{xs.max()*0.48:.1f} y {ys.min()*0.48:.1f}..{ys.max()*0.48:.1f})")

# green card stroke columns (border) for inner-edge reference
rg, gg, bg = render[..., 0], render[..., 1], render[..., 2]
greenstroke = (gg > 100) & (gg - rg > 40) & (gg - bg > 20)
gcols = np.where(greenstroke[300:900, 1150:1250].mean(axis=0) > 0.3)[0] + 1150
gcols_r = np.where(greenstroke[300:900, 1830:1930].mean(axis=0) > 0.3)[0] + 1830
print(f"  card left stroke cols {gcols}, right stroke cols {gcols_r}")

# ---------- 2. clean (alpha, color) regression ----------
# classify render flat pixels; sample the frame at the inverse-mapped position
flat_classes = {"white": "FFFFFF", "peach": "FDEDDD", "mint": "CEFFE1", "yellow": "F5E6A8"}
samples = []
for name, hexcol in flat_classes.items():
    m = colmask(render, hexcol, tol=10)
    mm = np.zeros_like(m); mm[RP] = m[RP]
    er = ndimage.binary_erosion(mm, iterations=4)  # away from edges/text
    ys, xs = np.where(er)
    for yy, xx in zip(ys[::29], xs[::29]):
        fxq, fyq = to_frame_pts(xx + 0.5, yy + 0.5)
        fx0, fy0 = int(fxq), int(fyq)
        if 0 <= fx0 < 959 and 0 <= fy0 < 539:
            # only if the frame patch is flat too (avoid text/border bleed)
            patch = frame[fy0 - 1:fy0 + 2, fx0 - 1:fx0 + 2].reshape(-1, 3)
            if patch.std(axis=0).max() < 14:
                samples.append((name, frame[fy0, fx0], render[yy, xx]))

print(f"\nflat samples: {len(samples)}")
A_rows, y_rows = [], []
for name, cf, cb in samples:
    for c in range(3):
        row = np.zeros(4); row[0] = -cb[c]; row[1 + c] = 1.0
        A_rows.append(row); y_rows.append(cf[c] - cb[c])
sol, *_ = np.linalg.lstsq(np.array(A_rows), np.array(y_rows), rcond=None)
u = sol[0]; col = sol[1:] / u
hexc = "%02X%02X%02X" % tuple(int(round(min(255, max(0, q)))) for q in col)
print(f"JOINT fit: alpha {u:.3f}, highlight rgb ({col[0]:.0f},{col[1]:.0f},{col[2]:.0f}) = {hexc}")
# residual per class
for name in flat_classes:
    sel = [(cf, cb) for (nm, cf, cb) in samples if nm == name]
    if not sel: continue
    cf = np.array([s[0] for s in sel]); cb = np.array([s[1] for s in sel])
    pred = col[None, :] * u + cb * (1 - u)
    print(f"   {name}: n={len(sel)} mean measured {cf.mean(axis=0).round(0)} pred {pred.mean(axis=0).round(0)} err {np.abs(pred-cf).mean():.1f}")

# ---------- 3. subpixel highlight edges in frame space ----------
# alpha map: alpha(px) = <cf-cb, d>/<d,d>, d = col - cb  (cb from render via mapping)
warp_of_render_in_frame = None
# build render->frame sampling grid once (per render px step 2)
rys, rxs = np.mgrid[230:1060:2, 1190:1910:2]
fxs = (rxs - ax) / sx; fys = (rys - ay) / sy
fxi = np.clip(np.round(fxs).astype(int), 0, 959); fyi = np.clip(np.round(fys).astype(int), 0, 539)
cf_grid = frame[fyi, fxi]           # frame color at each render grid pos
cb_grid = render[rys, rxs]          # render color
d = col[None, None, :] - cb_grid
denom = (d * d).sum(axis=2)
alpha_map = np.where(denom > 900, ((cf_grid - cb_grid) * d).sum(axis=2) / np.maximum(denom, 1e-9), np.nan)
np.save(S + "/alpha_map.npy", alpha_map)
print(f"\nalpha map: n={np.isfinite(alpha_map).sum()}, alpha>0.35: {(alpha_map > 0.35).sum()}")

# highlight bbox from alpha map
am = np.where(alpha_map > 0.32, 1.0, 0.0)
lab, n = ndimage.label(am)
sizes = ndimage.sum(am, lab, range(1, n + 1))
print("alpha-map components (render grid, step2 -> render px = idx*2 + offset):")
rects = []
for k in np.argsort(sizes)[::-1][:4]:
    if sizes[k] < 1500: break
    ys, xs = np.where(lab == k + 1)
    x0, x1, y0, y1 = xs.min() * 2 + 1190, xs.max() * 2 + 1190, ys.min() * 2 + 230, ys.max() * 2 + 230
    rects.append((x0, x1, y0, y1))
    print(f"  n={int(sizes[k])} render x {x0}..{x1} y {y0}..{y1} -> pt x {x0*0.48:.1f}..{x1*0.48:.1f} y {y0*0.48:.1f}..{y1*0.48:.1f}")

# subpixel edges: average alpha profile across the rect, 50% crossing
def edge_profile(rect):
    x0, x1, y0, y1 = rect
    xc0, xc1, yc0, yc1 = x0 - 14, x1 + 14, y0 - 14, y1 + 14
    sub = alpha_map[(yc0 - 230) // 2:(yc1 - 230) // 2, (xc0 - 1190) // 2:(xc1 - 1190) // 2]
    prof_h = np.nanmean(sub, axis=0)  # along x
    prof_v = np.nanmean(sub, axis=1)  # along y
    def cross(prof, off, step):
        idx = np.where(prof >= 0.5)[0]
        if len(idx) == 0: return None, None
        i0, i1 = idx[0], idx[-1]
        def interp(i, up):
            j = i - 1 if up else i + 1
            if j < 0 or j >= len(prof) or np.isnan(prof[i]) or np.isnan(prof[j]) or prof[i] == prof[j]:
                return off + i * step
            t = (0.5 - prof[j]) / (prof[i] - prof[j])
            return off + (j + t) * step
        return interp(i0, True), interp(i1, False)
    lx, rx_ = cross(prof_h, xc0, 2)
    ty, by = cross(prof_v, yc0, 2)
    return lx, rx_, ty, by

for i, rect in enumerate(rects):
    lx, rx_, ty, by = edge_profile(rect)
    f = lambda v: v * 0.48
    print(f"rect{i+1} subpixel (render px -> build pt): left {lx:.1f}->{f(lx):.2f} right {rx_:.1f}->{f(rx_):.2f} "
          f"top {ty:.1f}->{f(ty):.2f} bottom {by:.1f}->{f(by):.2f}  "
          f"w {f(rx_-lx):.2f} h {f(by-ty):.2f}")
