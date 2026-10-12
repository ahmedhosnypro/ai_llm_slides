#!/usr/bin/env python3
# m2_elements.py — slide 016 element ink bboxes + fills (frame coords fx,fy).
# Mapping (certified 009/010, re-fit on this frame in m1_chrome_output.txt):
#   slide_x = (fx - 17.582) / 0.962329 ;  slide_y = fy / 0.955556
# All bboxes are INK bboxes (tight around drawn pixels), frame px.
from PIL import Image
import numpy as np
from scipy import ndimage

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_016.jpg"
im = Image.open(FR).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def cc(mask, minpx=4):
    lab, n = ndimage.label(mask, structure=np.ones((3, 3)))
    comps = []
    for sl in ndimage.find_objects(lab):
        ys, xs = sl
        h, w = ys.stop - ys.start, xs.stop - xs.start
        npx = int(mask[sl].sum())
        if npx >= minpx:
            comps.append((xs.start, ys.start, xs.stop - 1, ys.stop - 1, w, h, npx))
    return sorted(comps, key=lambda c: (c[1], c[0]))

def show(name, comps, note=""):
    print(f"--- {name}: {len(comps)} comps {note}")
    for (x0, y0, x1, y1, w, h, npx) in comps:
        print(f"    fx {x0:4d}..{x1:4d}  fy {y0:3d}..{y1:3d}  w{w:3d} h{h:3d} ({npx}px)")

def patch_med(x0, y0, x1, y1):
    p = a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3)
    m = np.median(p, axis=0).astype(int)
    return "#%02X%02X%02X" % (m[0], m[1], m[2]), tuple(m)

print("=== TITLE (red ink, region 100..805 x 48..100) ===")
reg = np.zeros((H, W), bool)
reg[48:100, 100:806] = True
tmask = reg & ((R - (G + B) / 2 > 50) & (R > 110))
tcomps = cc(tmask, 6)
xs0 = min(c[0] for c in tcomps); xs1 = max(c[2] for c in tcomps)
ys0 = min(c[1] for c in tcomps); ys1 = max(c[3] for c in tcomps)
print(f"TITLE BBOX fx {xs0}..{xs1} fy {ys0}..{ys1} (w {xs1-xs0+1} h {ys1-ys0+1})  -> slide x {(xs0-17.582)/0.962329:.1f}..{(xs1-17.582)/0.962329:.1f} y {ys0/0.955556:.1f}..{ys1/0.955556:.1f}")
caps = [c for c in tcomps if c[4] >= 10 and c[5] >= 14]  # tall caps
print("tall caps (w>=10,h>=14):", [(c[0], c[1], c[2], c[3]) for c in caps[:6]])
if caps:
    caph = np.median([c[3] - c[1] + 1 for c in caps])
    print(f"cap height (frame px) median {caph} -> slide {caph/0.955556:.1f} pt")

print("=== SUBTITLE (region 100..830 x 100..130) — blue runs vs red runs ===")
reg = np.zeros((H, W), bool)
reg[100:130, 100:831] = True
smask_b = reg & ((B - (R + G) / 2 > 35) & (B > 110))
smask_r = reg & ((R - (G + B) / 2 > 50) & (R > 110))
bcomps = cc(smask_b, 4); rcomps = cc(smask_r, 4)
if bcomps:
    print(f"subtitle BLUE bbox fx {min(c[0] for c in bcomps)}..{max(c[2] for c in bcomps)} fy {min(c[1] for c in bcomps)}..{max(c[3] for c in bcomps)} ({len(bcomps)} comps)")
if rcomps:
    print(f"subtitle RED  bbox fx {min(c[0] for c in rcomps)}..{max(c[2] for c in rcomps)} fy {min(c[1] for c in rcomps)}..{max(c[3] for c in rcomps)} ({len(rcomps)} comps)")
    show("subtitle RED comps (the W_k run + anything else red)", rcomps)
# color cores
for nm, m in (("blue", smask_b), ("red", smask_r)):
    if m.sum() > 20:
        px = a[m]
        print(f"subtitle {nm} core median #{int(np.median(px[:,0])):02X}{int(np.median(px[:,1])):02X}{int(np.median(px[:,2])):02X} n={m.sum()}")
# darkest/most saturated blue core
if smask_b.sum() > 20:
    px = a[smask_b]
    idx = np.argsort(-(px[:, 2] - (px[:, 0] + px[:, 1]) / 2))[:30]
    core = px[idx]
    print(f"subtitle blue SATURATED core (top30 by b-score): #{int(np.median(core[:,0])):02X}{int(np.median(core[:,1])):02X}{int(np.median(core[:,2])):02X}")

print("=== UPPER PANEL + LOWER PANEL (fill F2F1EF-ish vs chrome E9E9E7) ===")
fillmask = (np.abs(R - 242) <= 6) & (np.abs(G - 241) <= 6) & (np.abs(B - 239) <= 7)
lab, n = ndimage.label(fillmask, structure=np.ones((3, 3)))
sizes = ndimage.sum(fillmask, lab, range(1, n + 1))
big = np.argsort(-sizes)[:4]
for i in big:
    if sizes[i] < 5000:
        continue
    sl = ndimage.find_objects(lab)[i]
    ys, xs = sl
    print(f"panel comp: fx {xs.start}..{xs.stop-1} fy {ys.start}..{ys.stop-1} (w {xs.stop-xs.start} h {ys.stop-ys.start}) px {int(sizes[i])}")
# panel border color samples: just outside/inside panel1 top edge
print("panel1 border probes (row across x=200..210):")
for y in range(112, 124):
    print(f"  fy {y}: " + " ".join("%02X%02X%02X" % tuple(a[y, x]) for x in range(200, 206)))

print("=== EMBEDDING AREA (x 60..310, y 112..315) ===")
reg = np.zeros((H, W), bool)
reg[112:315, 60:311] = True
ermask = reg & ((R - (G + B) / 2 > 50) & (R > 110))
ecomps = cc(ermask, 5)
# cluster into rows by fy bands
rows = {}
for c in ecomps:
    key = c[1] // 20
    rows.setdefault(key, []).append(c)
print(f"red comps in embedding area: {len(ecomps)} (row-banded below)")
for k in sorted(rows):
    cs = rows[k]
    x0 = min(c[0] for c in cs); x1 = max(c[2] for c in cs)
    y0 = min(c[1] for c in cs); y1 = max(c[3] for c in cs)
    print(f"  band fy {y0}..{y1}: {len(cs)} comps fx {x0}..{x1}")
# big X letters: tall comps h>=13
show("embedding-area TALL red comps (X_N letters, h>=13)", [c for c in ecomps if c[5] >= 13])

print("=== EMBEDDING PILLS (pink fill) ===")
pillmask = (R > 240) & (G > 195) & (G < 240) & (B > 215) & (B < 250) & (R - B > 5)
pcomps = cc(pillmask, 300)
show("pink pill fills (>=300px)", pcomps)
for c in pcomps[:6]:
    x0, y0, x1, y1 = c[0], c[1], c[2], c[3]
    med, _ = patch_med(x0 + 2, y0 + 2, x0 + 6, y0 + 6)
    print(f"    pill ({x0},{y0})..({x1},{y1}) fill {med}")
# pill outlines: sample left edge ink of pill1
if pcomps:
    x0, y0, x1, y1 = pcomps[0][:4]
    print("pill1 left-edge samples fy mid:", " ".join("%02X%02X%02X" % tuple(a[(y0+y1)//2, x]) for x in range(x0 - 3, x0 + 2)))
    # circles: white comps inside pill
    wmask = np.zeros((H, W), bool)
    wmask[y0 + 2:y1 - 1, x0 + 2:x1 - 1] = True
    wmask &= (R > 244) & (G > 244) & (B > 244)
    wcomps = cc(wmask, 20)
    show("pill1 white circle fills", wcomps)
    # circle rim color: sample just above first circle
    if wcomps:
        cx0, cy0, cx1, cy1 = wcomps[0][:4]
        print("circle1 rim samples (top edge):", " ".join("%02X%02X%02X" % tuple(a[cy0 - 1, x]) for x in range(cx0, cx0 + 8, 2)))
# row5 pill outline (blue?) — sample edges of last pill
if len(pcomps) >= 5:
    x0, y0, x1, y1 = pcomps[4][:4]
    print("pill5 left-edge samples:", " ".join("%02X%02X%02X" % tuple(a[(y0+y1)//2, x]) for x in range(x0 - 3, x0 + 2)))
    print("pill5 top-edge samples:", " ".join("%02X%02X%02X" % tuple(a[y0 - 1, x]) for x in range(x0 + 10, x0 + 30, 4)))
    print("pill1 top-edge samples:", " ".join("%02X%02X%02X" % tuple(a[pcomps[0][1] - 1, x]) for x in range(pcomps[0][0] + 10, pcomps[0][0] + 30, 4)))

print("=== MATRIX CONTAINERS (3 tinted rounded rects) ===")
for nm, (r0, g0, b0, tol) in [("Head1 green", (226, 239, 218, 10)), ("Head2 orange", (252, 228, 214, 10)), ("Head3 lavender", (228, 223, 236, 10))]:
    m = (np.abs(R - r0) <= tol) & (np.abs(G - g0) <= tol) & (np.abs(B - b0) <= tol)
    cs = cc(m, 2000)
    show(nm, cs[:2])
    if cs:
        c = cs[0]
        med, _ = patch_med(c[0] + 3, c[1] + 3, c[0] + 8, c[1] + 8)
        print(f"    {nm} fill sample {med}")

print("=== MATRIX HEADERS (region 300..830 x 112..140) red vs blue ink ===")
reg = np.zeros((H, W), bool)
reg[112:142, 300:831] = True
hmask_r = reg & ((R - (G + B) / 2 > 50) & (R > 110))
hmask_b = reg & ((B - (R + G) / 2 > 25) & (B > 100))
show("header RED comps", cc(hmask_r, 5))
show("header BLUE comps", cc(hmask_b, 5))

print("=== RED BRACKETS around matrices (left x 300..325, right x 780..810, y 110..315) ===")
for nm, (rx0, rx1) in (("LEFT bracket", (300, 326)), ("RIGHT bracket", (778, 812))):
    reg = np.zeros((H, W), bool)
    reg[108:318, rx0:rx1] = True
    m = reg & ((R - (G + B) / 2 > 45) & (R > 100))
    cs = cc(m, 10)
    show(nm, cs)
    if cs:
        x0 = min(c[0] for c in cs); x1 = max(c[2] for c in cs)
        y0 = min(c[1] for c in cs); y1 = max(c[3] for c in cs)
        print(f"    {nm} TOTAL ink bbox fx {x0}..{x1} fy {y0}..{y1} -> slide x {(x0-17.582)/0.962329:.1f}..{(x1-17.582)/0.962329:.1f} y {y0/0.955556:.1f}..{y1/0.955556:.1f}")
        # vertical stroke x + horizontal tick extents
        colcount = {}
        for c in cs:
            for x in range(c[0], c[2] + 1):
                colcount[x] = colcount.get(x, 0) + 1
        spine = max(colcount, key=colcount.get)
        print(f"    spine column (most ink): fx {spine}")

print("=== EQUALS SIGN (region 255..300 x 385..425) ===")
reg = np.zeros((H, W), bool)
reg[385:426, 255:301] = True
m = reg & ((R - (G + B) / 2 > 45) & (R > 100))
cs = cc(m, 8)
show("= ink", cs)
if cs:
    x0 = min(c[0] for c in cs); x1 = max(c[2] for c in cs)
    y0 = min(c[1] for c in cs); y1 = max(c[3] for c in cs)
    print(f"= BBOX fx {x0}..{x1} fy {y0}..{y1} (w {x1-x0+1} h {y1-y0+1}) -> slide x {(x0-17.582)/0.962329:.1f}..{(x1-17.582)/0.962329:.1f} y {y0/0.955556:.1f}..{y1/0.955556:.1f}")

print("=== LOWER PANEL fill (region 260..835 x 315..505) ===")
fillmask2 = (np.abs(R - 242) <= 6) & (np.abs(G - 241) <= 6) & (np.abs(B - 239) <= 7)
reg = np.zeros((H, W), bool)
reg[315:506, 255:840] = True
lab2, n2 = ndimage.label(fillmask2 & reg, structure=np.ones((3, 3)))
szs = ndimage.sum(fillmask2 & reg, lab2, range(1, n2 + 1))
for i in np.argsort(-szs)[:2]:
    if szs[i] < 3000:
        continue
    sl = ndimage.find_objects(lab2)[i]
    ys, xs = sl
    print(f"lower panel comp: fx {xs.start}..{xs.stop-1} fy {ys.start}..{ys.stop-1} (w {xs.stop-xs.start} h {ys.stop-ys.start}) px {int(szs[i])}")

print("=== RIGHT ANNOTATIONS (x 835..935, y 325..490) red ink ===")
reg = np.zeros((H, W), bool)
reg[325:490, 835:936] = True
m = reg & ((R - (G + B) / 2 > 45) & (R > 100))
cs = cc(m, 4)
# cluster into 5 blocks by fy
blocks = {}
for c in cs:
    key = c[1] // 30
    blocks.setdefault(key, []).append(c)
merged = []
for k in sorted(blocks):
    csb = blocks[k]
    x0 = min(c[0] for c in csb); x1 = max(c[2] for c in csb)
    y0 = min(c[1] for c in csb); y1 = max(c[3] for c in csb)
    merged.append((x0, y0, x1, y1))
# merge blocks with small fy gaps
final = []
for b_ in merged:
    if final and b_[1] - final[-1][3] <= 6:
        p = final[-1]
        final[-1] = (min(p[0], b_[0]), p[1], max(p[2], b_[2]), max(p[3], b_[3]))
    else:
        final.append(list(b_))
for i, (x0, y0, x1, y1) in enumerate(final, 1):
    print(f"annotation #{i}: fx {x0}..{x1} fy {y0}..{y1} (w {x1-x0+1} h {y1-y0+1}) -> slide y {y0/0.955556:.1f}..{y1/0.955556:.1f}")

print("=== CAPTIONS under output groups (y 485..515) red vs blue ===")
reg = np.zeros((H, W), bool)
reg[483:516, 260:840] = True
cmask_r = reg & ((R - (G + B) / 2 > 45) & (R > 100))
cmask_b = reg & ((B - (R + G) / 2 > 35) & (B > 110))
show("caption RED comps", cc(cmask_r, 4))
show("caption BLUE comps", cc(cmask_b, 4))

print("=== SUMMARY BOX (x 55..265, y 405..505) ===")
reg = np.zeros((H, W), bool)
reg[405:506, 55:266] = True
bmask = reg & ((B - (R + G) / 2 > 35) & (B > 100))
rmask = reg & ((R - (G + B) / 2 > 45) & (R > 100))
bcs = cc(bmask, 4)
if bcs:
    x0 = min(c[0] for c in bcs); x1 = max(c[2] for c in bcs)
    y0 = min(c[1] for c in bcs); y1 = max(c[3] for c in bcs)
    print(f"summary blue ink TOTAL bbox fx {x0}..{x1} fy {y0}..{y1}")
show("summary BLUE comps", bcs)
rcs = cc(rmask, 4)
show("summary RED comps (highlights)", rcs)
# box fill sample
print("summary box fill sample @(150,440):", patch_med(148, 438, 154, 444))
