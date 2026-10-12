#!/usr/bin/env python3
# m10b_final.py — robust (alpha, O) from median pairs over two clean backgrounds;
# verify on a third; alpha map; subpixel rect edges; outside-SSD; cursor hole.
import numpy as np
from PIL import Image
from scipy import ndimage

S = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide004"
frame_im = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_004.jpg").convert("RGB")
frame = np.asarray(frame_im, dtype=np.float64)
render = np.asarray(Image.open(S + "/base-1.png").convert("RGB"), dtype=np.float64)
ax, sx, ay, sy = np.load(S + "/fit_content.npy")
W, H = render.shape[1], render.shape[0]

def fmed(rx0, rx1, ry0, ry1):
    """median frame color over a render-space rect (sampled at frame px)"""
    vals = []
    for ry in range(ry0, ry1, 2):
        for rx in range(rx0, rx1, 2):
            fx, fy = int(round((rx - ax) / sx)), int(round((ry - ay) / sy))
            if 1 <= fx <= 958 and 1 <= fy <= 539:
                patch = frame[fy - 1:fy + 2, fx - 1:fx + 2].reshape(-1, 3)
                if patch.std(axis=0).max() < 12:
                    vals.append(frame[fy, fx])
    vals = np.array(vals)
    return np.median(vals, axis=0), len(vals)

# background refs from the render (exact): peach FDEDDD, mint CEFFE1, warm box F7D6AC
cb_p = np.array([253, 237, 221.]); cb_m = np.array([206, 255, 225.]); cb_b = np.array([247, 214, 172.])
cf_p, np_ = fmed(1230, 1330, 755, 830)   # peach under H1
cf_m, nm_ = fmed(1755, 1855, 595, 670)   # mint under H2
cf_b, nb_ = fmed(1372, 1490, 752, 795)   # warm box under H1 (text-dense: check only)
print(f"peach pair  n={np_}: cf {cf_p.round(1)} cb {cb_p}")
print(f"mint  pair  n={nm_}: cf {cf_m.round(1)} cb {cb_m}")
print(f"box   pair  n={nb_}: cf {cf_b.round(1)} cb {cb_b}")

def solve_a(cf1, cb1, cf2, cb2):
    dcb = cb1 - cb2; dcf = cf1 - cf2
    return 1 - float((dcf @ dcb) / (dcb @ dcb))

a1 = solve_a(cf_p, cb_p, cf_m, cb_m)
a2 = solve_a(cf_p, cb_p, cf_b, cb_b)
a3 = solve_a(cf_m, cb_m, cf_b, cb_b)
print(f"alpha from pairs: peach-mint {a1:.3f}  peach-box {a2:.3f}  mint-box {a3:.3f}")
a = float(np.median([a1, a2, a3]))
O = (cf_p - (1 - a) * cb_p) / a
O2 = (cf_m - (1 - a) * cb_m) / a
O3 = (cf_b - (1 - a) * cb_b) / a
print(f"alpha {a:.3f}; O estimates: {O.round(1)} {O2.round(1)} {O3.round(1)}")
Oc = np.clip((O + O2 + O3) / 3, 0, 255)
hexO = "%02X%02X%02X" % tuple(int(round(q)) for q in Oc)
print(f"FINAL: alpha {a:.3f}, color {hexO} {tuple(Oc.round(0))}")

# predicted vs measured for each pair
for nm, cf, cb in [("peach", cf_p, cb_p), ("mint", cf_m, cb_m), ("box", cf_b, cb_b)]:
    pred = a * Oc + (1 - a) * cb
    print(f"  {nm}: pred {pred.round(1)} vs meas {cf.round(1)}  err {np.abs(pred - cf).max():.1f}")

# --- alpha map over the right panel ---
rys, rxs = np.mgrid[220:1070, 1180:1920]
fxi = np.clip(np.round((rxs - ax) / sx).astype(int), 0, 959)
fyi = np.clip(np.round((rys - ay) / sy).astype(int), 0, 539)
cf = frame[fyi, fxi]; cb = render[rys, rxs]
d = Oc[None, None, :] - cb
den = (d * d).sum(axis=2)
amap = np.where(den > 600, ((cf - cb) * d).sum(axis=2) / np.maximum(den, 1e-9), np.nan)
half = a / 2
bh = np.nan_to_num(amap, nan=0.0) > half
lab, n = ndimage.label(bh)
sizes = ndimage.sum(bh, lab, range(1, n + 1))
print("\nalpha-map components at 50% coverage:")
rects = []
for k in np.argsort(sizes)[::-1][:6]:
    if sizes[k] < 3000: break
    ys, xs = np.where(lab == k + 1)
    rects.append((xs.min() + 1180, xs.max() + 1180, ys.min() + 220, ys.max() + 220, int(sizes[k])))
    print(f"  n={int(sizes[k])} render x {xs.min()+1180}..{xs.max()+1180} y {ys.min()+220}..{ys.max()+220}"
          f"  (pt x {(xs.min()+1180)*0.48:.1f}..{(xs.max()+1180)*0.48:.1f} y {(ys.min()+220)*0.48:.1f}..{(ys.max()+220)*0.48:.1f})")

def sub_edges(rect):
    x0, x1, y0, y1, _ = rect
    sub = amap[max(0, y0 - 220 - 10):y1 - 220 + 10, max(0, x0 - 1180 - 10):x1 - 1180 + 10]
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
        le = interp(i0, True); re = interp(i1, False)
        return (le, re) if (le is not None and re is not None) else None
    ch = cross(prof_h, offx); cv = cross(prof_v, offy)
    if ch is None or cv is None: return None
    return ch[0], ch[1], cv[0], cv[1]

finals = []
for rect in rects:
    e = sub_edges(rect)
    if e is None:
        print(f"rect {rect[:4]}: edge extraction failed"); continue
    lx, rx_, ty, by = e
    f = 0.48
    finals.append((lx * f, rx_ * f, ty * f, by * f))
    print(f"rect: edges render ({lx:.1f},{rx_:.1f},{ty:.1f},{by:.1f}) -> BUILD PT "
          f"x {lx*f:.2f}..{rx_*f:.2f} (w {(rx_-lx)*f:.2f}) y {ty*f:.2f}..{by*f:.2f} (h {(by-ty)*f:.2f})")

# --- outside-SSD ---
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
bs = 16
hb, wb = H // bs, W // bs
bd = diff[:hb * bs, :wb * bs].reshape(hb, bs, wb, bs).mean(axis=(1, 3))
bm = m[:hb * bs, :wb * bs].reshape(hb, bs, wb, bs).mean(axis=(1, 3)) > 0.95
coords = np.argwhere(bm); vals = bd[bm]
order = np.argsort(vals)[::-1]
print("worst 12 blocks outside rects:")
for k in order[:12]:
    y, x = coords[k]
    print(f"  ({x * bs},{y * bs}) mean {vals[k]:.0f}")

np.save(S + "/amap.npy", amap)
np.save(S + "/highlight_solution.npy", np.array([a, *Oc]))
np.save(S + "/rects_final.npy", np.array(finals))
