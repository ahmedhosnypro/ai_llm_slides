#!/usr/bin/env python3
"""Slide 055 redness-forensics: faint shafts/corridors (P4 pattern method), 3D arrows, V lines, mesh."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_055.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}

def redness(p):
    r, g, b = p
    return r - max(g, b)

# ---- 1. left/right red 3D arrows: loose redness bbox ----
for name, (x0, x1, y0, y1) in {"L3d": (55, 100, 170, 215), "R3d": (865, 915, 170, 215)}.items():
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if redness(px[x, y]) > 35]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        out[name] = [min(xs), min(ys), max(xs), max(ys), len(pts)]
        # row profile: per-row min/max x (arrow shape)
        rows = {}
        for p in pts:
            rows.setdefault(p[1], []).append(p[0])
        prof = {y: (min(v), max(v)) for y, v in sorted(rows.items()) if y % 2 == 0}
        out[name + "_rows"] = {str(k): v for k, v in prof.items()}

# ---- 2. hatch boxes: redness rows in x 95..205 (left) and 750..860 (right) ----
for name, (x0, x1) in {"Lhatch": (92, 208), "Rhatch": (745, 865)}.items():
    rr = {}
    for y in range(158, 220):
        xs = [x for x in range(x0, x1) if redness(px[x, y]) > 40]
        if len(xs) >= 2:
            rr[y] = (min(xs), max(xs), len(xs))
    out[name + "_redrows"] = {str(k): v for k, v in rr.items()}

# ---- 3. K->dot corridor: redness profile along the 4 dot rows, x 265..310 ----
DOTROWS = [237.5, 276.5, 316, 359]
corr = {}
for cy in DOTROWS:
    for x in range(262, 312):
        vals = [redness(px[x, yy]) for yy in range(int(cy) - 2, int(cy) + 3)]
        m = max(vals)
        if m > 25:
            corr.setdefault(int(cy), []).append((x, m))
out["corridor"] = {str(k): v[:6] + [("...", "")] + v[-6:] if len(v) > 12 else v for k, v in corr.items()}

# ---- 4. V lines: vertical strips at x 680,690,700,710,720 — red/dark rows ----
def is_dark(p):
    return sum(p) < 300
strips = {}
for xx in [680, 690, 700, 710, 720]:
    rows = []
    for y in range(210, 380):
        r = redness(px[xx, y]); d = is_dark(px[xx, y])
        if r > 35 or d:
            rows.append((y, "R" if r > 35 else "D"))
    strips[xx] = rows
out["Vstrips"] = {str(k): v for k, v in strips.items()}

# ---- 5. mesh diagonals inside dotprod box: redness>30 pixels x 295..405, y 220..380 ----
mesh = [(x, y) for y in range(215, 385) for x in range(292, 408) if redness(px[x, y]) > 35]
out["mesh_pts_count"] = len(mesh)
# cluster into lines: for each pixel record (x,y); print grouped by y bands
mb = {}
for x, y in mesh:
    mb.setdefault(y // 10, []).append((x, y))
out["mesh_bands"] = {str(k * 10): (min(v), max(v), len(v)) for k, v in sorted(mb.items())}

# ---- 6. query line: redness along x 305..320, y 355..395 ----
qpts = [(x, y) for y in range(355, 398) for x in range(300, 325) if redness(px[x, y]) > 35]
out["query_pts"] = qpts[:40]

# ---- 7. green arrow full: looser green ----
def is_greenish(p):
    r, g, b = p
    return g > 110 and (g - r) > 25 and (g - b) > 10
ga = [(x, y) for y in range(140, 195) for x in range(555, 660) if is_greenish(px[x, y])]
if ga:
    xs = [p[0] for p in ga]; ys = [p[1] for p in ga]
    out["green_arrow_loose"] = [min(xs), min(ys), max(xs), max(ys), len(ga)]
    rows = {}
    for x, y in ga:
        rows.setdefault(y, []).append(x)
    out["green_arrow_rows"] = {str(y): (min(v), max(v)) for y, v in sorted(rows.items()) if y % 3 == 0}

# ---- 8. O box + flanking cells exact: greenish bbox rows ----
ob = [(x, y) for y in range(112, 168) for x in range(540, 710) if is_greenish(px[x, y]) or redness(px[x, y]) < -20]
if ob:
    xs = [p[0] for p in ob]; ys = [p[1] for p in ob]
    out["O_zone"] = [min(xs), min(ys), max(xs), max(ys), len(ob)]

# ---- 9. softmax->node corridor: redness along node rows x 516..545 ----
sn = {}
for cy in DOTROWS:
    xs = [(x, max(redness(px[x, yy]) for yy in range(int(cy) - 2, int(cy) + 3))) for x in range(514, 550)]
    xs = [(x, m) for x, m in xs if m > 25]
    sn[str(cy)] = xs[:8]
out["softmax_to_nodes"] = sn

# ---- 10. node->Sigma verticals: redness columns at node x, y 210..235 ----
ns = {}
for nx in [557, 587, 616, 645]:
    ys = [(y, redness(px[nx, y])) for y in range(208, 236)]
    ys = [(y, m) for y, m in ys if m > 25]
    ns[str(nx)] = ys[:8]
out["node_to_sigma"] = ns

# ---- 11. fraction region rows: redness in x 408..470, y 180..222 ----
frr = {}
for y in range(180, 224):
    xs = [x for x in range(405, 472) if redness(px[x, y]) > 40]
    if xs:
        frr[y] = (min(xs), max(xs), len(xs))
out["fraction_rows"] = {str(k): v for k, v in frr.items()}

# ---- 12. K.q label rows: x 372..404, y 186..206 ----
kqr = {}
for y in range(186, 208):
    xs = [x for x in range(370, 406) if redness(px[x, y]) > 40]
    if xs:
        kqr[y] = (min(xs), max(xs), len(xs))
out["kq_rows"] = {str(k): v for k, v in kqr.items()}

# ---- 13. Z-row cells: pale cell columns + Z labels red positions ----
def near(p, c, tol):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))
zred = {}
for x in range(195, 545):
    xs = [y for y in range(450, 500) if redness(px[x, y]) > 45]
    if len(xs) >= 3:
        zred[x] = (min(xs), max(xs), len(xs))
# group columns
zx = sorted(zred)
groups, cur = [], []
for v in zx:
    if cur and v - cur[-1] > 4:
        groups.append((cur[0], cur[-1]))
        cur = []
    cur.append(v)
if cur:
    groups.append((cur[0], cur[-1]))
out["zrow_red_col_groups"] = groups

# ---- 14. caption text rows precise + white arrow shape ----
def is_mag(p):
    r, g, b = p
    return r > 140 and b > 140 and g < 110 and abs(r - b) < 80
mc = [(x, y) for y in range(450, 500) for x in range(520, 680) if is_mag(px[x, y])]
mrows = {}
for x, y in mc:
    mrows.setdefault(y, []).append(x)
out["caption_rows"] = {str(y): (min(v), max(v), len(v)) for y, v in sorted(mrows.items()) if y % 2 == 0}
def is_white(p):
    return all(v > 235 for v in p)
wa = [(x, y) for y in range(450, 500) for x in range(660, 730) if is_white(px[x, y]) ]
wrows = {}
for x, y in wa:
    wrows.setdefault(y, []).append(x)
out["white_arrow_rows"] = {str(y): (min(v), max(v), len(v)) for y, v in sorted(wrows.items()) if y % 2 == 0}

# ---- 15. legend: dark ink col groups (structure), pale green fill bbox, cells ----
def is_darkink(p):
    return sum(p) < 320
lg = [(x, y) for y in range(415, 515) for x in range(725, 910) if is_darkink(px[x, y])]
lcols = {}
for x, y in lg:
    lcols.setdefault(x, []).append(y)
lgs = sorted(lcols)
groups2, cur = [], []
for v in lgs:
    if cur and v - cur[-1] > 4:
        groups2.append((cur[0], cur[-1]))
        cur = []
    cur.append(v)
if cur:
    groups2.append((cur[0], cur[-1]))
out["legend_ink_col_groups"] = [(a, b, len(lcols[a])) for a, b in groups2]
lrows = {}
for x, y in lg:
    lrows.setdefault(y, []).append(x)
out["legend_ink_row_groups"] = [(y, min(v), max(v), len(v)) for y, v in sorted(lrows.items()) if y % 3 == 0][:30]

print(json.dumps(out, indent=1))
