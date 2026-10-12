#!/usr/bin/env python3
"""Probe arcs, cursor, circle fill/outline, gray lines, inset glyph colors, spoke dots."""
import numpy as np
from PIL import Image
import math, json

FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_027.jpg"
im = np.asarray(Image.open(FR).convert("RGB")).astype(int)
r, g, b = im[..., 0], im[..., 1], im[..., 2]
H, W = r.shape
CX, CY = 577.2, 284.0

def classify(px):
    rr, gg, bb = int(px[0]), int(px[1]), int(px[2])
    if rr > 238 and gg > 238 and bb > 168: return "paleY"
    if rr < 70 and gg < 70 and bb < 70: return "black"
    if rr > 130 and rr - gg > 55 and rr - bb > 55: return "red"
    if gg > 100 and gg - rr > 40 and gg - bb > 40: return "green"
    if bb > 110 and bb - rr > 40 and bb - gg > 40: return "blue"
    if rr > 170 and 40 < gg < 170 and bb < 90: return "orange"
    if abs(rr-gg) < 30 and abs(gg-bb) < 30 and 100 < rr < 220: return "gray"
    return f"({rr},{gg},{bb})"

out = {}

# ---- probe along rays between consecutive words for arc ink (radius 150..260)
for name, a0, a1 in [("W0-W1", 0, 30), ("W1-W2", 30, 60), ("W2-W3", 60, 90), ("W3-W4", 90, 120)]:
    found = {}
    for rad in range(140, 275, 4):
        for a10 in range(a0*10, (a1+1)*10, 5):
            a = a10 / 10.0
            x = int(round(CX + rad * math.cos(math.radians(a))))
            y = int(round(CY - rad * math.sin(math.radians(a))))
            if 0 <= x < W and 0 <= y < H:
                c = classify(im[y, x])
                if c in ("orange", "red"):
                    found.setdefault((c, rad // 20 * 20), []).append((x, y, tuple(int(v) for v in im[y, x])))
    out["arc_probe_" + name] = {f"{k[0]}@r{k[1]}": v[:4] for k, v in found.items()}

# ---- cursor: scan region (540..640, 190..280) for dark pixels
reg = im[190:280, 540:640]
dk = (reg[..., 0] < 120) & (reg[..., 1] < 120) & (reg[..., 2] < 120)
ys, xs = np.where(dk)
out["cursor_dark"] = {"count": int(dk.sum()),
                      "bbox": [int(xs.min())+540, int(ys.min())+190, int(xs.max())+540, int(ys.max())+190] if dk.sum() else None,
                      "samples": [[int(x)+540, int(y)+190, tuple(int(v) for v in reg[y, x])] for y, x in list(zip(ys, xs))[:6]]}

# ---- circle fill boundary: walk IN from outside along several clean angles
def first_pale_in(a_deg, rmax=300):
    for rad in range(rmax, 60, -1):
        x = int(round(CX + rad * math.cos(math.radians(a_deg))))
        y = int(round(CY - rad * math.sin(math.radians(a_deg))))
        if 0 <= x < W and 0 <= y < H:
            rr, gg, bb = im[y, x]
            if rr > 238 and gg > 238 and bb > 168:
                return rad, (x, y, tuple(int(v) for v in im[y, x])), tuple(int(v) for v in im[y, x]) if False else None
    return None
bounds = {}
for a in [-45, -20, -10, 10, 20, 45, 135, 160, 200, 225, 300, 330]:
    res = first_pale_in(a)
    if res: bounds[a] = [res[0], res[1]]
out["fill_boundary_inward"] = bounds

# ---- outline color just OUTSIDE fill along -30 deg
a = -30
for rad in range(170, 195):
    x = int(round(CX + rad * math.cos(math.radians(a))))
    y = int(round(CY - rad * math.sin(math.radians(a))))
    out.setdefault("outline_scan_m30", []).append([rad, (x, y), tuple(int(v) for v in im[y, x])])

# ---- gray horizontal line: full extent at rows 282..287
out["gray_line"] = {}
for y in range(280, 290):
    row = im[y]
    gl = [(x, tuple(int(v) for v in row[x])) for x in range(150, 940)
          if abs(int(row[x][0])-int(row[x][1])) < 28 and abs(int(row[x][1])-int(row[x][2])) < 28
          and 110 < row[x][0] < 215]
    if gl:
        xs_ = [p[0] for p in gl]
        out["gray_line"][y] = {"n": len(xs_), "min": min(xs_), "max": max(xs_), "mid_sample": gl[len(gl)//2]}

# gray vertical line probe through center column
col = im[:, int(round(CX))]
gv = [(y, tuple(int(v) for v in col[y])) for y in range(60, 500)
      if abs(int(col[y][0])-int(col[y][1])) < 28 and abs(int(col[y][1])-int(col[y][2])) < 28 and 110 < col[y][0] < 215]
out["gray_vline_center"] = {"n": len(gv), "sample": gv[:3] + gv[-3:] if gv else []}

# ---- inset box: border color probe (top edge) + per-glyph color runs
bx0, by0, bx1, by1 = 82, 182, 216, 246
out["eqbox_border_samples"] = [tuple(int(v) for v in im[by0, x]) for x in range(100, 200, 20)]
out["eqbox_border_left"] = [tuple(int(v) for v in im[y, bx0]) for y in range(190, 240, 10)]
# text lines inside box: rows with ink
sub = im[by0:by1+1, bx0:bx1+1]
sr, sg, sb = sub[..., 0], sub[..., 1], sub[..., 2]
ink = (sr < 205) & ~(sr > 230)
rowink = ink.sum(axis=1)
print("eqbox rowink:", [(i, int(v)) for i, v in enumerate(rowink) if v > 0])
# per-column color class in band rows 5..20 (line 1) and 25..40 (line 2), 45..62 (line3)
def col_classes(y0, y1):
    res = []
    for x in range(sub.shape[1]):
        cc = None
        for y in range(y0, y1):
            rr, gg, bb = sub[y, x]
            if rr > 130 and rr - gg > 55 and rr - bb > 55: cc = "R" if cc in (None, "R") else "mix"
            elif bb > 110 and bb - rr > 40 and bb - gg > 40: cc = "B" if cc in (None, "B") else "mix"
            elif gg > 100 and gg - rr > 40 and gg - bb > 40: cc = "G" if cc in (None, "G") else "mix"
            elif rr < 120 and gg < 120 and bb < 120: cc = "k" if cc in (None, "k") else "mix"
        res.append(cc or ".")
    # compress to runs
    runs, cur, n = [], None, 0
    for c in res:
        if c == cur: n += 1
        else:
            if cur: runs.append((cur, n))
            cur, n = c, 1
    if cur: runs.append((cur, n))
    return runs
out["line1_runs"] = col_classes(5, 21)
out["line2_runs"] = col_classes(26, 42)
out["line3_runs"] = col_classes(45, 62)

# ---- spoke dots: for each of 12 rays, count red-ish pixels along it (outside fill R>~180)
spokes = {}
for k in range(12):
    a = k * 30
    cnt, rng = 0, []
    for rad in range(120, 320):
        x = int(round(CX + rad * math.cos(math.radians(a))))
        y = int(round(CY - rad * math.sin(math.radians(a))))
        if not (0 <= x < W and 0 <= y < H): break
        rr, gg, bb = im[y, x]
        # red-ish: check 3x3 neighborhood max redness
        hit = False
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                yy, xx = y+dy, x+dx
                if 0 <= yy < H and 0 <= xx < W:
                    r2, g2, b2 = im[yy, xx]
                    if r2 > 140 and r2 - g2 > 40 and r2 - b2 > 40:
                        hit = True
        if hit:
            cnt += 1; rng.append(rad)
    spokes[a] = {"hits": cnt, "r_range": [min(rng), max(rng)] if rng else None}
out["spokes"] = spokes

# ---- arcs: full-image orange-ish scan with looser threshold (any saturated warm non-red)
warm = (r > 150) & (b < 140) & (g < r - 20) & (g > 40)
warm[:, :300] = False; warm[470:, :] = False; warm[:50, :] = False
ys, xs = np.where(warm)
out["warm_scan_count"] = int(len(xs))
if len(xs):
    # cluster roughly by grid
    from scipy import ndimage
    lab, n = ndimage.label(warm)
    comps = []
    for i in range(1, n+1):
        m = lab == i
        c = int(m.sum())
        if c < 12: continue
        yy, xx = np.where(m)
        comps.append({"px": c, "bbox": [int(xx.min()), int(yy.min()), int(xx.max()), int(yy.max())],
                      "mean_rgb": [int(im[yy, xx][:, 0].mean()), int(im[yy, xx][:, 1].mean()), int(im[yy, xx][:, 2].mean())]})
    comps.sort(key=lambda c: -c["px"])
    out["warm_components"] = comps[:25]

print(json.dumps(out, indent=1, default=str))
with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide027/probe3.json", "w") as f:
    json.dump(out, f, indent=1, default=str)
