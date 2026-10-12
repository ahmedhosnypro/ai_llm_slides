#!/usr/bin/env python3
"""Self-check attempt 1 (v2, checker fixed) — render vs original for slide 021.

Fixes vs v1: red-text band searches restricted to x 200..1800 render px (away from
the chrome border columns); text-line mask = dark|blue|red inside the blue box
interior only; containment excludes chrome border strokes + badge zone explicitly.
"""
from PIL import Image
import numpy as np
import sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide021/render_1.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
sc = 2000 / 960.0

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 140) & (G < 90) & (B < 90)
blue = (B > 120) & (R < 110) & (G < 110)
dark = (R < 150) & (G < 150) & (B < 150)

fails = []
def chk(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'OK ' if ok else 'FAIL'} {name}: got {got:.1f} want {want} (tol {tol})")
    if not ok:
        fails.append(name)

def band_in(mask, y0, y1, x0, x1, min_px=2, gap=3):
    m = mask[y0:y1, x0:x1]
    rows = np.where(m.sum(axis=1) >= min_px)[0]
    if len(rows) == 0:
        return None
    s = p = rows[0]
    out = []
    for r in rows[1:]:
        if r - p > gap:
            out.append((s + y0, p + y0)); s = r
        p = r
    out.append((s + y0, p + y0))
    return out

def colspan(mask, y0, y1, x0, x1):
    sub = mask[y0:y1 + 1, x0:x1]
    cols = np.where(sub.sum(axis=0) >= 1)[0]
    return (int(cols[0] + x0), int(cols[-1] + x0)) if len(cols) else None

TX0, TX1 = 200, 1800  # render px: inside chrome border, outside text-free zones

# --- title (red text band in y 140..236) ---
tb = band_in(red, 140, 236, TX0, TX1)
print("-- title --")
if not tb or len(tb) != 1:
    fails.append(f"title bands {tb}")
else:
    y0, y1 = tb[0]
    cs = colspan(red, y0, y1, TX0, TX1)
    chk("title top", y0 / sc, 77, 4)
    chk("title bottom", y1 / sc, 109, 4)
    chk("title center x", (cs[0] + cs[1]) / 2 / sc, 493, 6)
    chk("title ink width", (cs[1] - cs[0]) / sc, 288, 10)
    chk("title ink height", (y1 - y0) / sc, 33, 4)

# --- subtitle (red band in y 237..300) ---
sb = band_in(red, 237, 300, TX0, TX1)
print("-- subtitle --")
if not sb or len(sb) != 1:
    fails.append(f"subtitle bands {sb}")
else:
    y0, y1 = sb[0]
    cs = colspan(red, y0, y1, TX0, TX1)
    chk("subtitle top", y0 / sc, 115, 4)
    chk("subtitle bottom", y1 / sc, 139, 4)
    chk("subtitle center x", (cs[0] + cs[1]) / 2 / sc, 494, 6)
    chk("subtitle ink width", (cs[1] - cs[0]) / sc, 724, 12)

# --- blue box ---
rows = np.where(blue.sum(axis=1) > 600)[0]
cols = np.where(blue.sum(axis=0) > 200)[0]
print("-- blue box --")
chk("box top", rows.min() / sc, 170, 4)
chk("box bottom", rows.max() / sc, 471, 4)
chk("box left", cols.min() / sc, 69, 4)
chk("box right", cols.max() / sc, 879, 4)

# --- text line bands INSIDE box interior (exclude border: frame 173..468, x 74..874) ---
mask = dark | blue | red
inner = mask.copy()
inner[:int(172.5 * sc), :] = False
inner[int(468.5 * sc):, :] = False
inner[:, :int(74 * sc)] = False
inner[:, int(874 * sc):] = False
lb = band_in(inner, int(172.5 * sc), int(468.5 * sc), int(74 * sc), int(874 * sc), min_px=4, gap=4)
print("-- text line bands (render -> frame) --")
targets = [("HDR1", 201, 80, 385), ("P1L1", 224, 80, 854), ("P1L2", 246, 80, 863),
           ("P1L3", 269, 80, 655), ("HDR2", 313, 80, 354), ("P2L1", 336, 80, 807),
           ("P2L2", 358, 80, 163), ("P3L1", 403, 80, 854), ("P3L2", 425, 80, 660)]
print(f"   {len(lb)} bands")
if len(lb) != 9:
    fails.append(f"band count {len(lb)} != 9")
else:
    tops = []
    for i, (y0, y1) in enumerate(lb):
        cs = colspan(inner, y0, y1, int(74 * sc), int(874 * sc))
        nm, wt, wl, wr = targets[i]
        tops.append(y0)
        print(f"   {nm}: frame y {y0/sc:.1f}..{y1/sc:.1f}  x {cs[0]/sc:.1f}..{cs[1]/sc:.1f}")
        chk(f"{nm} top", y0 / sc, wt, 4)
        chk(f"{nm} left", cs[0] / sc, wl, 4)
        chk(f"{nm} right", cs[1] / sc, wr, 7)
    pitch = (tops[8] - tops[0]) / 10  # 9 bands over 10 slots (2 blank lines)
    chk("line pitch", pitch / sc, 22.4, 1.0)

# --- P3 blue runs ---
if len(lb) == 9:
    y0, y1 = lb[7]
    sub = blue[y0:y1 + 1, 160:1810]
    colsB = np.where(sub.sum(axis=0) >= 1)[0]
    runs = []
    if len(colsB):
        sB = pB = colsB[0]
        for x in colsB[1:]:
            if x - pB > 8:
                runs.append((sB + 160, pB + 160)); sB = x
            pB = x
        runs.append((sB + 160, pB + 160))
    print("-- P3L1 blue runs (frame):", [(round(r[0]/sc,1), round(r[1]/sc,1)) for r in runs])
    # original measured 4 runs: 96..211 (bag-of-words), 219..270 (model),
    # 709..794 (skip-gram), 802..854 (model)
    want_runs = [(96, 211), (219, 270), (709, 794), (802, 854)]
    okb = len(runs) == len(want_runs) and all(
        abs(r[0]/sc - w[0]) < 8 and abs(r[1]/sc - w[1]) < 8 for r, w in zip(runs, want_runs))
    print(f"   {'OK' if okb else 'FAIL'} blue term runs vs original 4 runs")
    if not okb:
        fails.append("P3L1 blue runs")
    y0, y1 = lb[8]
    nb = blue[y0:y1 + 1, 160:1810].sum()
    print(f"   P3L2 blue px (want ~0): {nb}")
    if nb > 20:
        fails.append("P3L2 blue ink")

# --- containment ---
# content ink excluding chrome border (frame x 42-45.5 / 914.5-918, y 45-48 & 536-540)
# and excluding badge zone (frame x>860, y<95)
print("-- containment --")
ink = (dark | blue | red).copy()
ink[:, :int(46 * sc)] = False
ink[:, int(914 * sc):] = False
ink[:int(49 * sc), :] = False
ink[int(535 * sc):, :] = False
ink[:int(96 * sc), int(860 * sc):] = False   # badge zone
ys, xs = np.where(ink)
chk("content min x", xs.min() / sc, 69, 6)
chk("content max x", xs.max() / sc, 879, 8)
chk("content min y", ys.min() / sc, 77, 6)
chk("content max y", ys.max() / sc, 471, 8)

print()
if fails:
    print(f"SELF-CHECK v2: FAIL ({len(fails)}): {fails}")
    sys.exit(1)
print("SELF-CHECK v2: ALL PASS")
