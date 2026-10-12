#!/usr/bin/env python3
# m6_highlights.py — detect the two orange highlight rectangles in MY frame's right
# panel, measure edges precisely, solve (alpha, color) against the known underlying
# fills from the certified render, and express in build pt via the content fit.
import numpy as np
from PIL import Image
from scipy import ndimage

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
frame = np.asarray(frame_im, dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")

# warp frame into render space with the content fit (for background lookup)
W, H = render.shape[1], render.shape[0]
warped = np.asarray(frame_im.transform((W, H), Image.AFFINE,
    (1 / sx, 0, -ax / sx, 0, 1 / sy, -ay / sy), resample=Image.BILINEAR), dtype=np.float64)
Image.fromarray(warped.astype(np.uint8)).save(S + "/frame_warped_contentfit.png")

# --- orange mask on the WARPED frame (render-grid) inside the right panel ---
r, g, b = warped[..., 0], warped[..., 1], warped[..., 2]
orange = (r > 195) & (b < 190) & (g > 120) & (g < 235) & ((r - b) > 45) & ((g - b) > 18)
panel = np.zeros_like(orange); panel[220:1000, 1180:1910] = True
orange &= panel
lab, n = ndimage.label(orange)
sizes = ndimage.sum(orange, lab, range(1, n + 1))
order = np.argsort(sizes)[::-1]
print("orange components (warped space):")
comps = []
for k in order[:6]:
    if sizes[k] < 300: break
    ys, xs = np.where(lab == k + 1)
    comps.append((xs.min(), xs.max(), ys.min(), ys.max(), int(sizes[k])))
    print(f"  n={int(sizes[k])} x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")

# --- precise edges: alpha-ramp 50% crossing per row/col around each component ---
def refine(x0, x1, y0, y1):
    # left/right edges: for rows in the band, find where orange-ness crosses 50%
    oness_r = ((warped[..., 0] > 195) & (warped[..., 2] < 190) &
               ((warped[..., 0] - warped[..., 2]) > 45)).astype(np.float64)
    xmids, ymids = [], []
    for yy in range(y0 + 6, y1 - 6):
        row = oness_r[yy, x0 - 8: x1 + 8]
        idx = np.where(row > 0)[0]
        if len(idx) > (x1 - x0) * 0.5:
            xmids.append((idx[0] + x0 - 8 + idx[-1] + x0 - 8) / 2)
    ymids_done = []
    col_ones = oness_r
    for xx in range(x0 + 6, x1 - 6):
        col = col_ones[y0 - 8: y1 + 8, xx]
        idx = np.where(col > 0)[0]
        if len(idx) > (y1 - y0) * 0.5:
            ymids_done.append((idx[0] + y0 - 8 + idx[-1] + y0 - 8) / 2)
    return (np.median(xmids) if xmids else None, np.median(ymids_done) if ymids_done else None)

print("\nrefined centers (warped space):")
for (x0, x1, y0, y1, npx) in comps:
    cx, cy = refine(x0, x1, y0, y1)
    print(f"  comp x{x0}..{x1} y{y0}..{y1}: center ({cx:.1f},{cy:.1f})")

# --- hard edges via coverage fractions (leftmost/rightmost/topmost/bottommost col/row
#     where >50% of the rect's extent is orange) ---
def hard_edges(x0, x1, y0, y1):
    oness = ((warped[..., 0] > 195) & (warped[..., 2] < 190) &
             ((warped[..., 0] - warped[..., 2]) > 45))
    sub = oness[y0:y1 + 1, x0:x1 + 1]
    colcov = sub.mean(axis=0); rowcov = sub.mean(axis=1)
    xs = np.where(colcov > 0.5)[0]; ys = np.where(rowcov > 0.5)[0]
    return x0 + xs[0], x0 + xs[-1], y0 + ys[0], y0 + ys[-1]

print("\nhard edges (warped render px) -> build pt (x0.48):")
rects = []
for (x0, x1, y0, y1, npx) in comps:
    ex0, ex1, ey0, ey1 = hard_edges(x0, x1, y0, y1)
    bx0, bx1, by0, by1 = ex0 * 0.48, ex1 * 0.48, ey0 * 0.48, ey1 * 0.48
    rects.append((ex0, ex1, ey0, ey1))
    print(f"  rect render x {ex0}..{ex1} y {ey0}..{ey1}  -> build pt x {bx0:.1f}..{bx1:.1f} (w {bx1-bx0:.1f}) y {by0:.1f}..{by1:.1f} (h {by1-by0:.1f})")

# --- solve (alpha, orange RGB) per rect: sample flat-background pixels ---
def solve_alpha(ex0, ex1, ey0, ey1, name):
    rows, eqs = [], []
    inner = (slice(ey0 + 6, ey1 - 6), slice(ex0 + 6, ex1 - 6))
    wsub = warped[inner]; rsub = render[inner]
    flat = (ndimage.uniform_filter(rsub.mean(axis=2), 5) -
            ndimage.uniform_filter(rsub.mean(axis=2), 5) ** 0)  # placeholder
    localstd = ndimage.generic_gradient_magnitude(rsub.mean(axis=2), ndimage.sobel)
    sel = localstd < 12  # flat underlying fill
    ys, xs = np.where(sel)
    for yy, xx in zip(ys[::13], xs[::13]):
        cf = wsub[yy, xx]; cb = rsub[yy, xx]
        for c in range(3):
            # cf_c - cb_c = v_c - u*cb_c  with u=alpha, v_c=alpha*color_c
            rows.append([(1 if c == 0 else 0) * 0 - cb[c] * -1, 0, 0, 0])
    # build joint LSQ properly
    A_rows, y_rows = [], []
    for yy, xx in zip(ys[::13], xs[::13]):
        cf = wsub[yy, xx]; cb = rsub[yy, xx]
        for c in range(3):
            row = np.zeros(4)
            row[0] = -cb[c]           # u coefficient
            row[1 + c] = 1.0          # v_c coefficient
            A_rows.append(row)
            y_rows.append(cf[c] - cb[c])
    A_m = np.array(A_rows); y_m = np.array(y_rows)
    sol, res, *_ = np.linalg.lstsq(A_m, y_m, rcond=None)
    u, vR, vG, vB = sol
    if abs(u) > 1e-6:
        col = (vR / u, vG / u, vB / u)
    else:
        col = (0, 0, 0)
    hexc = "%02X%02X%02X" % tuple(int(round(min(255, max(0, q)))) for q in col)
    print(f"{name}: alpha {u:.3f}, color rgb ({col[0]:.0f},{col[1]:.0f},{col[2]:.0f}) = {hexc}"
          f"  (n={len(y_rows)})")
    # sanity: predicted vs measured on sample
    pred = np.array(col)[None, :] * u + rsub[ys[::200], xs[::200]] * (1 - u)
    meas = wsub[ys[::200], xs[::200]]
    print(f"   blend check mean abs err {np.abs(pred - meas).mean():.1f}")
    return u, hexc

for i, (ex0, ex1, ey0, ey1) in enumerate(rects):
    solve_alpha(ex0, ex1, ey0, ey1, f"rect{i+1}")
