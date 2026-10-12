#!/usr/bin/env python3
# m10_final.py — solve (alpha, highlight RGB) from clean flat-background samples,
# build the alpha map, extract the two highlight rectangles with subpixel edges,
# verify no other deltas outside them (masked SSD), locate the cursor hole.
import numpy as np
from PIL import Image
from scipy import ndimage

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
frame = np.asarray(frame_im, dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")
W, H = render.shape[1], render.shape[0]

# --- 1. clean sample pairs (frame px <-> render px via mapping), flat-flat only ---
# restrict to the two rough highlight zones (from m6): H1 render x1200..1560 y730..850,
# H2 render x1550..1880 y555..690
def frame_at(rx, ry):
    fx, fy = (rx - ax) / sx, (ry - ay) / sy
    x0, y0 = int(fx), int(fy)
    if not (1 <= x0 <= 958 and 1 <= y0 <= 539): return None
    patch = frame[y0 - 1:y0 + 2, x0 - 1:x0 + 2].reshape(-1, 3)
    return patch

pairs = []
zones = [(1200, 1560, 730, 850), (1550, 1880, 555, 690)]
rstd = ndimage.generic_gradient_magnitude(render.mean(axis=2), ndimage.sobel)
for zx0, zx1, zy0, zy1 in zones:
    for ry in range(zy0, zy1, 3):
        for rx in range(zx0, zx1, 3):
            if rstd[ry, rx] > 30:  # skip underlying edges/text
                continue
            p = frame_at(rx, ry)
            if p is None or p.std(axis=0).max() > 12:  # skip frame-side edges/text
                continue
            pairs.append((frame[int((ry - ay) / sy), int((rx - ax) / sx)], render[ry, rx]))
pairs = np.array(pairs)
print(f"clean pairs: {len(pairs)}")
A_rows, y_rows = [], []
for cf, cb in pairs:
    for c in range(3):
        row = np.zeros(4); row[0] = -cb[c]; row[1 + c] = 1.0
        A_rows.append(row); y_rows.append(cf[c] - cb[c])
sol, *_ = np.linalg.lstsq(np.array(A_rows), np.array(y_rows), rcond=None)
a_fit = sol[0]; O = sol[1:] / a_fit
Oc = np.clip(O, 0, 255)
hexO = "%02X%02X%02X" % tuple(int(round(q)) for q in Oc)
print(f"SOLVED: alpha {a_fit:.3f}  highlight rgb ({Oc[0]:.0f},{Oc[1]:.0f},{Oc[2]:.0f}) = {hexO}")
pred = a_fit * Oc[None, :] + (1 - a_fit) * pairs[:, 1, :]
print(f"blend residual mean {np.abs(pred - pairs[:, 0, :]).mean():.2f}")

# --- 2. alpha map over the right panel ---
rys, rxs = np.mgrid[220:1070:1, 1180:1920:1]
fxi = np.clip(np.round((rxs - ax) / sx).astype(int), 0, 959)
fyi = np.clip(np.round((rys - ay) / sy).astype(int), 0, 539)
cf = frame[fyi, fxi]; cb = render[rys, rxs]
d = Oc[None, None, :] - cb
den = (d * d).sum(axis=2)
amap = np.where(den > 600, ((cf - cb) * d).sum(axis=2) / np.maximum(den, 1e-9), np.nan)
half = a_fit / 2
bh = amap > half
bh[: 0] = False
lab, n = ndimage.label(bh)
sizes = ndimage.sum(bh, lab, range(1, n + 1))
print("\nalpha-map components at 50% coverage:")
rects = []
for k in np.argsort(sizes)[::-1][:6]:
    if sizes[k] < 4000: break
    ys, xs = np.where(lab == k + 1)
    rects.append((xs.min() + 1180, xs.max() + 1180, ys.min() + 220, ys.max() + 220, int(sizes[k])))
    print(f"  n={int(sizes[k])} render x {xs.min()+1180}..{xs.max()+1180} y {ys.min()+220}..{ys.max()+220}"
          f"  (pt x {(xs.min()+1180)*0.48:.1f}..{(xs.max()+1180)*0.48:.1f} y {(ys.min()+220)*0.48:.1f}..{(ys.max()+220)*0.48:.1f})")

# --- 3. subpixel edges: profile 50%-coverage crossings ---
def sub_edges(rect):
    x0, x1, y0, y1, _ = rect
    sub = amap[y0 - 220 - 10:y1 - 220 + 10, x0 - 1180 - 10:x1 - 1180 + 10]
    offx, offy = x0 - 10, y0 - 10
    prof_h = np.nanmedian(sub, axis=0)
    prof_v = np.nanmedian(sub, axis=1)
    def cross(prof, off):
        idx = np.where(prof > half)[0]
        if len(idx) == 0: return None
        i0, i1 = idx[0], idx[-1]
        def interp(i, up):
            j = i - 1 if up else i + 1
            if j < 0 or j >= len(prof): return off + i
            p0, p1 = prof[i], prof[j]
            if not np.isfinite(p0) or not np.isfinite(p1) or p0 == p1: return off + i
            t = (half - p1) / (p0 - p1)
            return off + j + t
        return interp(i0, True), interp(i1, False)
    lx, rx_ = cross(prof_h, offx)
    ty, by = cross(prof_v, offy)
    return lx, rx_, ty, by

finals = []
for rect in rects:
    lx, rx_, ty, by = sub_edges(rect)
    f = 0.48
    finals.append((lx * f, rx_ * f, ty * f, by * f))
    print(f"rect: edges render ({lx:.1f},{rx_:.1f},{ty:.1f},{by:.1f}) -> BUILD PT "
          f"x {lx*f:.2f}..{rx_*f:.2f} (w {(rx_-lx)*f:.2f}) y {ty*f:.2f}..{by*f:.2f} (h {(by-ty)*f:.2f})")

# --- 4. anything else? masked SSD outside the two rects (+5px pad) ---
warp = np.asarray(frame_im.transform((W, H), Image.AFFINE,
    (1 / sx, 0, -ax / sx, 0, 1 / sy, -ay / sy), resample=Image.BILINEAR), dtype=np.float64)
diff = np.abs(warp - render).sum(axis=2)
excl = np.zeros_like(diff, bool)
for lx, rx_, ty, by in finals:
    excl[max(0, int(ty / 0.48) - 6):int(by / 0.48) + 6, max(0, int(lx / 0.48) - 6):int(rx_ / 0.48) + 6] = True
valid = np.zeros_like(diff, bool)
valid[100:1118, 92:1908] = True
m = valid & ~excl
print(f"\nmasked SSD outside rects: mean {diff[m].mean():.2f}  p95 {np.percentile(diff[m], 95):.1f}  p99 {np.percentile(diff[m], 99):.1f}")
# worst blocks outside the rects
bs = 16
hb, wb = H // bs, W // bs
bd = diff[:hb * bs, :wb * bs].reshape(hb, bs, wb, bs).mean(axis=(1, 3))
bm = m[:hb * bs, :wb * bs].reshape(hb, bs, wb, bs).mean(axis=(1, 3)) > 0.95
coords = np.argwhere(bm)
vals = bd[bm]
order = np.argsort(vals)[::-1]
print("worst 15 blocks outside rects:")
for k in order[:15]:
    y, x = coords[k]
    print(f"  ({x * bs},{y * bs}) mean {vals[k]:.0f}")

# --- 5. cursor hole: low-alpha island inside H1 ---
np.save(S + "/amap.npy", amap)
np.save(S + "/highlight_solution.npy", np.array([a_fit, *Oc]))
