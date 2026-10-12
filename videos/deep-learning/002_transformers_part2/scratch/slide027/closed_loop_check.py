#!/usr/bin/env python3
"""Closed-loop check: render_1.png (2001x1125 @150dpi, 1px = 0.36 slide pt)
vs measured targets (slide pt * 2000/1440... actually px = pt * 150/72 = pt*2.08333).
Wait: 13.333in * 150 = 2000px wide -> 2001 with rounding. px = pt/72*150 = pt*2.0833."""
import numpy as np
from PIL import Image
from scipy import ndimage
import json, math, sys

RENDER = sys.argv[1] if len(sys.argv) > 1 else "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide027/render_1.png"
im = np.asarray(Image.open(RENDER).convert("RGB")).astype(int)
H, W, _ = im.shape
r, g, b = im[..., 0], im[..., 1], im[..., 2]
PX = 150.0 / 72.0  # pt -> px
res = {"size": [W, H]}

def bbox_of(mask):
    ys, xs = np.where(mask)
    if not len(ys): return None
    return [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]

def cmp(name, got, tgt, tol=4.0, tol_bottom=None):
    # got/tgt: [x0,y0,x1,y1] in px; tol_bottom applies to the y1 (descender) edge
    if got is None:
        res.setdefault("fails", []).append(f"{name}: NO INK"); return
    d = max(abs(got[0]-tgt[0]), abs(got[1]-tgt[1]), abs(got[2]-tgt[2]))
    db = abs(got[3]-tgt[3])
    ok = d <= tol and db <= (tol_bottom if tol_bottom is not None else tol)
    res.setdefault("checks", []).append({"name": name, "got": got, "tgt": [round(v,1) for v in tgt], "max_delta_px": round(float(d),2), "bottom_delta_px": round(float(db),2), "ok": bool(ok)})
    if not ok: res.setdefault("fails", []).append(f"{name}: delta {max(d,db):.1f}px")

# ---------- title lines (red ink in left region)
red = (r > 130) & (r - g > 50) & (r - b > 50)
tm = np.zeros_like(red); tm[120:400, 100:850] = True
tred = red & tm
ys, xs = np.where(tred)
rows = np.unique(ys)
segs, cur = [], [rows[0]]
for y in rows[1:]:
    if y - cur[-1] <= 4: cur.append(y)
    else: segs.append((cur[0], cur[-1])); cur = [y]
segs.append((cur[0], cur[-1]))
tlines = []
for (ya, yb) in segs:
    mm = (ys >= ya) & (ys <= yb)
    lx = xs[mm]
    tlines.append([int(lx.min()), int(ya), int(lx.max()), int(yb)])
print("title lines found:", tlines)
T = 2.0833
cmp("title.L1", tlines[0] if len(tlines) else None, [56.6*T, 61.7*T, 296.9*T, 82.7*T], tol_bottom=8)
cmp("title.L2", tlines[1] if len(tlines) > 1 else None, [55.5*T, 89.0*T, 297.9*T, 106.7*T])
cmp("title.L3", tlines[2] if len(tlines) > 2 else None, [122.1*T, 117.2*T, 230.3*T, 139.2*T], tol_bottom=8)

# ---------- eq box (pale yellow rect left)
paleY = (r > 238) & (g > 238) & (b > 160) & (b < 240)
pm = np.zeros_like(paleY); pm[380:780, 120:640] = True
pb = paleY & pm
lab, n = ndimage.label(pb)
if n:
    sizes = ndimage.sum(pb, lab, range(1, n+1))
    m = lab == (int(np.argmax(sizes)) + 1)
    cmp("eqbox", bbox_of(m), [65.9*T, 190.5*T, 205.4*T, 257.4*T], tol=5)
    # eq text ink: blue/red/green inside box
    ys, xs = np.where(m)
    x0, x1 = xs.min(), xs.max()
    blue = (b > 110) & (b - r > 40) & (b - g > 40)
    green = (g > 100) & (g - r > 40) & (g - b > 40)
    redm = (r > 130) & (r - g > 50) & (r - b > 50)
    inner = np.zeros_like(pb); inner[ys.min()+3:ys.max()-2, x0+3:x1-2] = True
    ink = ((blue | green | redm) & inner)
    res["eq_ink_px"] = int(ink.sum())
    if ink.sum() == 0: res.setdefault("fails", []).append("eqbox text: EMPTY (BLOCKER)")
    # per-line rows
    yy = np.where(ink.any(axis=1))[0]
    if len(yy):
        segs2, cur = [], [yy[0]]
        for y in yy[1:]:
            if y - cur[-1] <= 4: cur.append(y)
            else: segs2.append((cur[0], cur[-1])); cur = [y]
        segs2.append((cur[0], cur[-1]))
        res["eq_lines_n"] = len(segs2)
        # line pitches
        pitches = [segs2[i+1][0]-segs2[i][0] for i in range(len(segs2)-1)]
        res["eq_line_top_px"] = [s[0] for s in segs2]
        res["eq_pitches_px"] = pitches
        # target tops (slide pt): 197.8, 218.8, 237.6
        for i, (ttop) in enumerate([197.8, 218.8, 237.6]):
            if i < len(segs2):
                d = abs(segs2[i][0] - ttop*T)
                res.setdefault("checks", []).append({"name": f"eq.line{i+1}.top", "got": segs2[i][0], "tgt": round(ttop*T,1), "delta_px": round(float(d),2), "ok": bool(d <= 5)})
                if d > 5: res.setdefault("fails", []).append(f"eq.line{i+1}.top delta {d:.1f}px")

# ---------- circle: fill + ring (axis lines split the fill -> union big comps)
cm = paleY.copy(); cm[:, :640] = False
cm[:250, :] = False
lab2, n2 = ndimage.label(cm)
bb = None
if n2:
    minx, miny, maxx, maxy = 10**9, 10**9, -1, -1
    for i in range(1, n2+1):
        m = lab2 == i
        if m.sum() < 5000: continue
        ys2, xs2 = np.where(m)
        minx = min(minx, int(xs2.min())); maxx = max(maxx, int(xs2.max()))
        miny = min(miny, int(ys2.min())); maxy = max(maxy, int(ys2.max()))
    if maxx > 0: bb = [minx, miny, maxx, maxy]
    cx, cy = (bb[0]+bb[2])/2, (bb[1]+bb[3])/2
    res["circle_bbox"] = bb
    res["circle_center_px"] = [round(cx,1), round(cy,1)]
    tgt_c = [581.0*T, 297.2*T]
    d = math.hypot(cx-tgt_c[0], cy-tgt_c[1])
    res["checks"] = res.get("checks", [])
    res["checks"].append({"name": "circle.center", "delta_px": round(float(d),2), "ok": bool(d <= 6)})
    if d > 6: res.setdefault("fails", []).append(f"circle.center delta {d:.1f}px")
    rad = ((bb[2]-bb[0]) + (bb[3]-bb[1])) / 4
    dd = abs(rad - 130.75*T)
    res["checks"].append({"name": "circle.radius", "got": round(rad,1), "tgt": round(130.75*T,1), "delta_px": round(float(dd),2), "ok": bool(dd <= 6)})
    if dd > 6: res.setdefault("fails", []).append(f"circle.radius delta {dd:.1f}px")

# ---------- chips (mint fill comps)
chip = (g > 220) & (g - r > 8) & (g - b > 8) & (r > 165) & (r < 240)
chip[:, :640] = False
lab3, n3 = ndimage.label(chip)
chips_found = []
for i in range(1, n3+1):
    m = lab3 == i
    if m.sum() < 400: continue
    ys3, xs3 = np.where(m)
    chips_found.append((round(float(xs3.mean()),1), round(float(ys3.mean()),1), int(m.sum())))
chips_found.sort(key=lambda c: -c[2])
res["chips_found"] = chips_found[:8]
chip_tgt = {0: (762.6, 297.2), 1: (738.4, 204.6), 2: (672.3, 138.6), 3: (581.1, 113.3), 4: (490.4, 139.9)}
found5 = chips_found[:5]
for k, (tx, ty) in chip_tgt.items():
    best, bd = None, 1e9
    for (fx, fy, cnt) in chips_found:
        d = math.hypot(fx - tx*T, fy - ty*T)
        if d < bd: bd, best = d, (fx, fy)
    res["checks"].append({"name": f"chip{k}.center", "delta_px": round(float(bd),2), "ok": bool(bd <= 6)})
    if bd > 6: res.setdefault("fails", []).append(f"chip{k}.center delta {bd:.1f}px")

# ---------- +w labels (STRICT red: excludes orange arc ink E06010)
redm2 = (r > 150) & (r - g > 80) & (g < 70) & (r - b > 80)
redm2[:, :1000] = False; redm2[850:, :] = False; redm2[:120, :] = False
lab4, n4 = ndimage.label(redm2)
lbls = []
for i in range(1, n4+1):
    m = lab4 == i
    if m.sum() < 25: continue
    ys4, xs4 = np.where(m)
    lbls.append([int(xs4.min()), int(ys4.min()), int(xs4.max()), int(ys4.max()), int(m.sum())])
res["label_comps"] = lbls[:15]
lbl_tgt = {"L1": (840.2, 236.5), "L2": (788.8, 104.1), "L3": (642.8, 75.4), "L4": (520.6, 75.4)}
for name, (tx, ty) in lbl_tgt.items():
    # union of all comps whose pixels fall within 14px of the target center
    px_t, py_t = tx * T, ty * T
    ux0, uy0, ux1, uy1 = 10**9, 10**9, -1, -1
    for lb in lbls:
        cx4, cy4 = (lb[0]+lb[2])/2, (lb[1]+lb[3])/2
        if math.hypot(cx4 - px_t, cy4 - py_t) <= 40:
            ux0 = min(ux0, lb[0]); uy0 = min(uy0, lb[1])
            ux1 = max(ux1, lb[2]); uy1 = max(uy1, lb[3])
    if ux1 < 0:
        res["checks"].append({"name": f"label.{name}", "ok": False, "note": "no comp"})
        res.setdefault("fails", []).append(f"label.{name}: no ink")
        continue
    cxu, cyu = (ux0+ux1)/2, (uy0+uy1)/2
    d = math.hypot(cxu - px_t, cyu - py_t)
    res["checks"].append({"name": f"label.{name}", "union_center": [round(cxu,1), round(cyu,1)], "delta_px": round(float(d),2), "ok": bool(d <= 7)})
    if d > 7: res.setdefault("fails", []).append(f"label.{name} delta {d:.1f}px")

# ---------- arrowheads: solid orange ink density near target (arc-merge robust)
orm = (r > 170) & (g > 55) & (g < 185) & (b < 110) & (r - b > 60)
head_tgt = {"h01": (776.4, 188.4), "h12": (692.6, 100.5), "h23": (585.6, 71.2), "h34": (473.3, 101.5)}
for name, (tx, ty) in head_tgt.items():
    x0h, y0h = int(tx * T) - 10, int(ty * T) - 10
    patch = orm[y0h:y0h + 21, x0h:x0h + 21]
    cnt = int(patch.sum())
    res["checks"].append({"name": f"head.{name}", "warm_px_near": cnt, "ok": bool(cnt >= 25)})
    if cnt < 25: res.setdefault("fails", []).append(f"head.{name} weak ({cnt}px)")

# ---------- arcs present? (orange ink along expected arc paths)
cnt_arc = 0
for (a0, a1) in [(12, 28.5), (42, 58.5), (72, 88.5), (102, 118.5)]:
    for a10 in range(int(a0*2), int(a1*2)+1):
        a = a10 / 2.0
        x = int(round((581.0 + 224 * math.cos(math.radians(a))) * T))
        y = int(round((297.2 - 224 * math.sin(math.radians(a))) * T))
        if 0 <= y < H and 0 <= x < W:
            patch = im[max(0,y-2):y+3, max(0,x-2):x+3]
            if ((patch[...,0] > 150) & (patch[...,0] - patch[...,2] > 40)).any(): cnt_arc += 1
res["arc_ink_samples"] = cnt_arc
if cnt_arc < 40: res.setdefault("fails", []).append(f"arcs faint/missing: {cnt_arc} samples")

# ---------- axis lines
row_y = int(round(296.7 * T))
band = im[row_y-2:row_y+3, 700:2500]
grayish = (np.abs(band[...,0]-band[...,1]) < 45) & (band[...,0] < 225) & (band[...,0] > 120)
res["haxis_px"] = int(grayish.sum())
col_x = int(round(581.0 * T))
bandv = im[160:1470, col_x-2:col_x+3]
grayishv = (np.abs(bandv[...,0]-bandv[...,1]) < 45) & (bandv[...,0] < 225) & (bandv[...,0] > 120)
res["vaxis_px"] = int(grayishv.sum())

fails = res.get("fails", [])
print(json.dumps(res, indent=1, default=str)[:4000])
print("\n=== FAILS ===" if fails else "\n=== ALL INK CHECKS PASS ===")
for f in fails: print(" -", f)
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/closed_loop_attempt1.json", "w") as f:
    json.dump(res, f, indent=1, default=str)
