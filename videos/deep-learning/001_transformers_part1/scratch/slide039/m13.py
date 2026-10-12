#!/usr/bin/env python3
"""m13.py — PIL verification of the cropcmp claims on the ORIGINAL frame.
Frame: unique_slides/slide_039.jpg (960x540). Frame = ground truth.
"""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
org = np.asarray(Image.open(BASE + "unique_slides/slide_039.jpg").convert("RGB")).astype(int)
H, W = org.shape[:2]
out = []

def redmask(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 120) & (R - G > 55) & (R - B > 55)

def blumask(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (B > 110) & (B - R > 35) & (B - G > 25)

def grnmask(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (G > 110) & (G - R > 30) & (G - B > 30)

def darkmask(a):
    return a.sum(axis=2) < 420

# ---------------------------------------------------------------- 1. sticker
# m12: top edge slope -18.43 deg; center approx (790, 477). Unrotate +18.43.
cy, cx = 477, 790
patch = org[420:535, 680:905]
im = Image.fromarray(patch.astype(np.uint8)).rotate(-18.43, resample=Image.BICUBIC, center=(cx - 680, cy - 420), fillcolor=(255, 255, 255))
u = np.asarray(im).astype(int)
# text band: sticker box now axis-aligned; find yellow bbox
ym = (u[..., 0] > 200) & (u[..., 1] > 200) & (u[..., 2] < 140)
ys, xs = np.where(ym)
if len(xs):
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    out.append(f"sticker unrotated yellow bbox: x[{x0+680},{x1+680}] y[{y0+420},{y1+420}] (w={x1-x0}, h={y1-y0})")
    band = u[y0:y1 + 1, x0:x1 + 1]
    rm, bm, dm = redmask(band), blumask(band), darkmask(band)
    out.append(f"sticker text band ink: red_px={rm.sum()} blue_px={bm.sum()} dark_px={dm.sum()}")
    # ink-only color: dark-ish pixels that are neither yellow bg nor white
    ink = dm & ~ym[y0:y1 + 1, x0:x1 + 1]
    if ink.sum() > 20:
        px = band[ink]
        out.append(f"sticker ink avg RGB = {px.mean(axis=0).round(1)}  (red-ish={ (px[:,0]-px[:,1]>40).sum() }, blue-ish={ (px[:,2]-px[:,0]>40).sum() })")
else:
    out.append("sticker: no yellow found in unrotated patch")

# ---------------------------------------------------------------- 2. Y-label band blue/red clusters
reg = org[108:242, 428:795]
rm, bm, gm = redmask(reg), blumask(reg), grnmask(reg)
out.append(f"Y-band (x428-795 y108-242): red_px={rm.sum()} blue_px={bm.sum()} green_px={gm.sum()}")
if bm.sum() > 30:
    from scipy import ndimage
    lab, n = ndimage.label(bm)
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(xs) > 12:
            out.append(f"  blue cluster: x[{xs.min()+428},{xs.max()+428}] y[{ys.min()+108},{ys.max()+108}] px={len(xs)} avg={reg[ys,xs].mean(axis=0).round(0)}")

# ---------------------------------------------------------------- 3. fraction region fine scan
out.append("fraction region red runs by row (x315-412, y252-298):")
for y in range(252, 299):
    row = org[y, 315:413]
    m = redmask(row)
    if m.sum() >= 2:
        xs = np.where(m)[0]
        runs = []
        s = xs[0]; p = xs[0]
        for x in xs[1:]:
            if x - p > 2:
                runs.append((s + 315, p + 315)); s = x
            p = x
        runs.append((s + 315, p + 315))
        out.append(f"  y={y}: " + " ".join(f"[{a}-{b}]" for a, b in runs))

# ---------------------------------------------------------------- 4. left X box cells
out.append("left X box (x131-187, cells at y286-314/315-343/344-371/372-400):")
for ci, (ya, yb) in enumerate([(288, 313), (316, 342), (345, 370), (373, 399)]):
    cell = org[ya:yb + 1, 131:188]
    rm, gm, dm = redmask(cell), grnmask(cell), darkmask(cell)
    px = cell.reshape(-1, 3)
    redish = (px[:, 0] - px[:, 1] > 40) & (px[:, 0] - px[:, 2] > 40) & (px[:, 0] > 130)
    grnish = (px[:, 1] - px[:, 0] > 15) & (px[:, 1] > 120)
    out.append(f"  cell{ci+1} y[{ya},{yb}]: strong_red={rm.sum()} strong_green={gm.sum()} dark={dm.sum()} redish_any={redish.sum()} greenish_any={grnish.sum()}")
    # red box strokes: column profile of red at cell left/right thirds
    rmcols = rm.sum(axis=0)
    lc = rmcols[:12].sum(); rc = rmcols[-12:].sum(); mid = rmcols[12:-12].sum()
    out.append(f"    red col distribution: left12={lc} mid={mid} right12={rc}")
# X letter color: strongest-ink pixels per cell (below avg sum)
for ci, (ya, yb) in enumerate([(288, 313), (316, 342), (345, 370), (373, 399)]):
    cell = org[ya:yb + 1, 131:188].reshape(-1, 3)
    s = cell.sum(axis=1)
    idx = np.argsort(s)[:40]  # darkest 40 = letter ink
    avg = cell[idx].mean(axis=0).round(0)
    out.append(f"  cell{ci+1} darkest-40 avg RGB = {avg}")

# ---------------------------------------------------------------- 5. bottom arrows heads
out.append("bottom arrows width profile (red px per row):")
for cx0 in [304.5, 394, 488.5, 593.5]:
    xs0, xs1 = int(cx0 - 14), int(cx0 + 14)
    prof = []
    for y in [490, 493, 496, 500, 505, 510, 513]:
        m = redmask(org[y, xs0:xs1])
        prof.append(f"y{y}:{m.sum()}")
    out.append(f"  arrow@x{cx0:.0f}: " + " ".join(prof))

# ---------------------------------------------------------------- 6. bottom row cells
out.append("bottom row cells (y453-487):")
for nm, xa, xb in [("cell1", 266, 326), ("cell2", 328, 374), ("cell3", 376, 422), ("cell4", 424, 470)]:
    cell = org[453:488, xa:xb]
    rm, gm, dm = redmask(cell), grnmask(cell), darkmask(cell)
    fill = cell[(cell.sum(axis=2) > 500)].mean(axis=0).round(0) if (cell.sum(axis=2) > 500).sum() else None
    out.append(f"  {nm} x[{xa},{xb}]: fill_avg={fill} red={rm.sum()} green={gm.sum()} dark={dm.sum()}")
    if rm.sum() > 5:
        ys, xs = np.where(rm)
        out.append(f"    red bbox: x[{xs.min()+xa},{xs.max()+xa}] y[{ys.min()+453},{ys.max()+453}]")

# ---------------------------------------------------------------- 7. right container borders
out.append("right container: greenish px per column x606-676 (y283-413):")
colg = grnmask(org[283:414, 606:677]).sum(axis=0)
out.append("  " + " ".join(f"{606+i}:{v}" for i, v in enumerate(colg) if v >= 2))

# ---------------------------------------------------------------- 8. panel2 bottom row region
reg = org[424:462, 336:412]
rm, gm = redmask(reg), grnmask(reg)
fill = reg[(reg.sum(axis=2) > 500)].mean(axis=0).round(0)
out.append(f"panel2 bottom-row cell1 (x336-412 y424-462): fill_avg={fill} red={rm.sum()} green={gm.sum()}")

print("\n".join(out))
