#!/usr/bin/env python3
"""Round 2: row/column scans + zoomed crops for slide_024.jpg."""
import numpy as np
from PIL import Image

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_024.jpg"
OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/"
IM = Image.open(SRC).convert("RGB")
A = np.asarray(IM).astype(int)
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]

def hexs(t):
    return "#%02X%02X%02X" % tuple(int(v) for v in t)

def runs_in_row(y, x0, x1, pred, minrun=2):
    """return runs of x where pred true"""
    out = []
    s = None
    for x in range(x0, x1):
        if pred(x, y):
            if s is None:
                s = x
        else:
            if s is not None and x - s >= minrun:
                out.append((s, x - 1))
            s = None
    if s is not None:
        out.append((s, x1 - 1))
    return out

BEIGE = lambda x, y: abs(r[y, x] - 214) < 26 and abs(g[y, x] - 198) < 26 and abs(b[y, x] - 182) < 30

print("== ROW SCANS: non-beige runs (neurons/lines) ==")
for y in (213, 285, 363):
    rr = runs_in_row(y, 60, 800, lambda x, yy: not BEIGE(x, yy), 2)
    print(f"row {y}: " + " ".join(f"{a}-{b}" for a, b in rr))

print("\n== COLUMN SCANS: non-beige runs ==")
for x in (172, 250, 425, 585, 670):
    rr = runs_in_col = []
    s = None
    for y in range(165, 425):
        if not BEIGE(x, y):
            if s is None:
                s = y
        else:
            if s is not None and y - s >= 2:
                runs_in_col.append((s, y - 1))
            s = None
    if s is not None:
        runs_in_col.append((s, 424))
    print(f"col {x}: " + " ".join(f"{a}-{b}" for a, b in runs_in_col))

print("\n== SAMPLE COLORS along row 213 (key x) ==")
for x in [150, 158, 162, 168, 172, 178, 185, 195, 205, 215, 225, 235, 245, 250, 255, 262, 270, 280, 290, 300]:
    print(f"  x{x}: {hexs(A[213, x])}", end="")
print()
print("== SAMPLE COLORS col2 neuron row1: scan x 235..290 at y213 ==")
for x in range(235, 292, 2):
    print(f"  x{x}: {hexs(A[213, x])}", end="")
print()

print("\n== OUTPUT BOX + arrow zone: row 213 x 690..800 ==")
for x in range(690, 800, 2):
    print(f"  x{x}: {hexs(A[213, x])}", end="")
print()

print("\n== CLASS BOX zone: row 210 x 820..900 ==")
for x in range(820, 900, 2):
    print(f"  x{x}: {hexs(A[210, x])}", end="")
print()
print("== CLASS BOX zone vertical x855 y190..230 ==")
for y in range(190, 232, 2):
    print(f"  y{y}: {hexs(A[y, 855])}", end="")
print()

print("\n== ERROR BAR vertical x806 y170..410 ==")
for y in range(170, 412, 8):
    print(f"  y{y}: {hexs(A[y, 806])}", end="")
print()

print("\n== DASHED LINE: scan y 125..150 at x=400 ==")
for y in range(125, 150):
    print(f"  y{y}: {hexs(A[y, 400])}", end="")
print()
print("== DASHED LINE: scan x 130..820 at best-y ==")
# find the y with most magenta-ish px in x130..820
best_y, best_n = None, -1
for y in range(125, 150):
    n = int(((r[y, 130:820] > 150) & (b[y, 130:820] > 150) & (g[y, 130:820] < r[y, 130:820] - 20)).sum())
    if n > best_n:
        best_y, best_n = y, n
print("best dashed y:", best_y, "n:", best_n)
y = best_y
xs = [x for x in range(128, 825) if r[y, x] > 150 and b[y, x] > 150 and g[y, x] < r[y, x] - 20]
if xs:
    print("dash x extent:", min(xs), max(xs), "count:", len(xs))
    print("dash color sample:", hexs(A[y, xs[0]]), hexs(A[y, xs[len(xs)//2]]))

print("\n== MAGENTA BOXES vertical/horizontal extents ==")
def box_extent(x0, x1, y0, y1, pred):
    ys, xs = [], []
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            if pred(xx, yy):
                ys.append(yy); xs.append(xx)
    if not xs:
        return None
    return (min(xs), max(xs), min(ys), max(ys))
magpred = lambda x, y: r[y, x] > 180 and b[y, x] > 180 and g[y, x] < r[y, x] - 30
print("InputSamples magenta extent:", box_extent(50, 145, 110, 170, magpred))
print("SampleLabel magenta extent:", box_extent(810, 905, 110, 170, magpred))
print("InputSamples fill sample (96,40):", hexs(A[40, 96]), "(96,48):", hexs(A[48, 96]))
print("InputSamples arrow-left scan x55..70 y38..46:", [hexs(A[41, x]) for x in range(55, 72, 2)])

print("\n== MAGENTA DOTS x70..90 y240..335 ==")
dotpred = lambda x, y: r[y, x] > 170 and b[y, x] > 170 and g[y, x] < r[y, x] - 40
for y in range(240, 336):
    xs = [x for x in range(65, 95) if dotpred(x, y)]
    if xs:
        print(f"  y{y}: x{min(xs)}..{max(xs)} {hexs(A[y, xs[len(xs)//2]])}")

print("\n== FAN LINES: scan row y=300 x 85..165 ==")
for x in range(85, 166, 2):
    print(f"  x{x}: {hexs(A[300, x])}", end="")
print()

print("\n== CALLOUT BOXES precise ==")
# light blue 99CCFF-ish, green, orange at y 432..462
for nm, (x0, x1) in (("prev", (200, 330)), ("cur", (360, 490)), ("nxt", (530, 660))):
    ys, xs = [], []
    for yy in range(428, 470):
        for xx in range(x0, x1):
            px = A[yy, xx]
            if not (px[0] > 240 and px[1] > 240 and px[2] > 240) and not (abs(px[0]-233) < 12 and abs(px[1]-233) < 12 and abs(px[2]-231) < 14):
                ys.append(yy); xs.append(xx)
    if xs:
        print(f"  {nm}: x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} fill sample {hexs(A[(min(ys)+max(ys))//2, (min(xs)+max(xs))//2])}")

print("\n== BLOCK ARROWS precise ==")
for nm, (x0, x1) in (("i", (240, 290)), ("j", (405, 455)), ("k", (565, 615))):
    ys, xs = [], []
    for yy in range(388, 434):
        for xx in range(x0, x1):
            px = A[yy, xx]
            # non-beige, non-gray, colored
            if not (abs(px[0]-233) < 14 and abs(px[1]-233) < 14 and abs(px[2]-231) < 16) and not (px[0] > 245 and px[1] > 245 and px[2] > 245):
                if max(px) - min(px) > 18 or (px[0] < 150):
                    ys.append(yy); xs.append(xx)
    if xs:
        print(f"  arrow {nm}: x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} fill {hexs(A[(min(ys)+max(ys))//2, (min(xs)+max(xs))//2])}")

print("\n== NEURON OUTLINES: sample edge colors col3r1 ==")
# col3r1 center ~(425,213)? find circle extents by scanning row 213 x 400..455 for green
for x in range(398, 458):
    px = A[213, x]
    if px[1] > 200 and px[0] < 230 and px[2] < 200:
        print(f"  first green at x{x} {hexs(px)}", end="")
        break
print()
for x in range(458, 398, -1):
    px = A[213, x]
    if px[1] > 200 and px[0] < 230 and px[2] < 200:
        print(f"  last green at x{x} {hexs(px)}", end="")
        break
print()
for y in range(185, 245):
    px = A[y, 425]
    if px[1] > 200 and px[0] < 230 and px[2] < 200:
        print(f"  first green row1 at y{y} {hexs(px)}", end="")
        break
print()
for y in range(245, 185, -1):
    px = A[y, 425]
    if px[1] > 200 and px[0] < 230 and px[2] < 200:
        print(f"  last green row1 at y{y} {hexs(px)}", end="")
        break
print()

print("\n== TITLE ink bbox + cap height ==")
redt = (r > 140) & (g < 100) & (b < 100)
tt = redt[40:110, :]
ys, xs = np.where(tt)
print("title bbox:", xs.min(), xs.max(), ys.min() + 40, ys.max() + 40)
print("title color sample:", hexs(A[80, 480]))

print("\n== NET LABELS + ARROWS (red) ==")
for nm, (x0, x1, y0, y1) in [("Net_i+arrow", (195, 250, 165, 192)), ("Net_j+arrow", (360, 415, 165, 192)), ("Net_k+arrow", (525, 580, 165, 192))]:
    m = redt[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {nm}: x{xs.min()+x0}..{xs.max()+x0} y{ys.min()+y0}..{ys.max()+y0}")

print("\n== O LABELS (red) precise windows ==")
for nm, (x0, x1, y0, y1) in [("O_i r1", (262, 302, 188, 216)), ("O_i r2", (262, 302, 260, 288)), ("O_i r3", (262, 302, 338, 366)),
                              ("O_j r1", (430, 470, 188, 216)), ("O_j r2", (430, 470, 260, 288)), ("O_j r3", (430, 470, 338, 366)),
                              ("O_k r1", (594, 634, 188, 216)), ("O_k r2", (594, 634, 260, 288)), ("O_k r3", (594, 634, 338, 366))]:
    m = redt[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"  {nm}: x{xs.min()+x0}..{xs.max()+x0} y{ys.min()+y0}..{ys.max()+y0} n={len(ys)}")
    else:
        print(f"  {nm}: none")

print("\n== BLUE WEIGHT LABELS (b-dominant) ==")
bluew = (b > 120) & (b - r > 40) & (b - g > 30)
bw = bluew.copy(); bw[:165] = False; bw[430:] = False; bw[:, :60] = False; bw[:, 700:] = False
ys, xs = np.where(bw)
if len(ys):
    lab_pts = sorted(set(zip(ys.tolist(), xs.tolist())))
    # cluster by proximity
    clusters = []
    used = set()
    pts = set(lab_pts)
    for p in lab_pts:
        if p in used:
            continue
        stack = [p]; comp = []
        used.add(p)
        while stack:
            cy, cx = stack.pop()
            comp.append((cy, cx))
            for dy in (-2, -1, 0, 1, 2):
                for dx in (-2, -1, 0, 1, 2):
                    q = (cy + dy, cx + dx)
                    if q in pts and q not in used:
                        used.add(q); stack.append(q)
        cys = [c[0] for c in comp]; cxs = [c[1] for c in comp]
        clusters.append((min(cxs), max(cxs), min(cys), max(cys), len(comp)))
    for c in sorted(clusters, key=lambda c: (c[2], c[0])):
        print(f"  x{c[0]}..{c[1]} y{c[2]}..{c[3]} w={c[1]-c[0]+1} h={c[3]-c[2]+1} n={c[4]}")

print("\n== OUTPUT BOXES (near-black) x695..805 y170..430 ==")
blk = (r < 110) & (g < 110) & (b < 110)
ob = blk.copy(); ob[:170] = False; ob[430:] = False; ob[:, :695] = False; ob[:, 806:] = False
ys, xs = np.where(ob)
if len(ys):
    # cluster by rows
    rows = sorted(set(ys.tolist()))
    groups = []
    cur = [rows[0]]
    for y in rows[1:]:
        if y - cur[-1] <= 3:
            cur.append(y)
        else:
            groups.append(cur); cur = [y]
    groups.append(cur)
    for gr in groups:
        m = ob[gr[0]:gr[-1]+1, :]
        ys2, xs2 = np.where(m)
        print(f"  box y{gr[0]}..{gr[-1]} x{xs2.min()}..{xs2.max()} n={len(ys2)}")

print("\n== Sigma/S glyph ink per neuron (dark px within r=15 of centers) ==")
for cy, rws in ((213, "r1"), (285, "r2"), (363, "r3")):
    line = []
    for cx in (172, 250, 425, 585, 670):
        win = A[cy-15:cy+15, cx-15:cx+15]
        dk = (win[:, :, 0] < 110) & (win[:, :, 1] < 110) & (win[:, :, 2] < 110)
        ys2, xs2 = np.where(dk)
        if len(ys2):
            line.append(f"c{cx}: n={len(ys2)} x{xs2.min()+cx-15}..{xs2.max()+cx-15} y{ys2.min()+cy-15}..{ys2.max()+cy-15}")
        else:
            line.append(f"c{cx}: none")
    print(f" {rws}: " + " | ".join(line))

# crops for visual inspection
crops = {
    "crop_topleft.png": (50, 110, 350, 170, 3),
    "crop_col1.png": (60, 180, 260, 250, 3),
    "crop_col2o.png": (225, 185, 310, 245, 4),
    "crop_mesh23.png": (270, 185, 440, 310, 2),
    "crop_mesh34.png": (430, 185, 610, 310, 2),
    "crop_col5out.png": (600, 185, 800, 250, 3),
    "crop_errclass.png": (780, 165, 910, 415, 2),
    "crop_bottom.png": (195, 385, 665, 470, 2),
    "crop_title.png": (250, 50, 710, 100, 2),
    "crop_netlabels.png": (190, 160, 590, 195, 2),
}
for name, (x0, y0, x1, y1, z) in crops.items():
    c = IM.crop((x0, y0, x1, y1))
    c = c.resize(((x1 - x0) * z, (y1 - y0) * z), Image.LANCZOS)
    c.save(OUT + name)
print("\ncrops saved")
