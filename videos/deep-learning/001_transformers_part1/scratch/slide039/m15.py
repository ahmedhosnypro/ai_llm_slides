#!/usr/bin/env python3
"""m15.py — remaining ground-truth scans + probe crops for the vision probes."""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/"
org = np.asarray(Image.open(BASE + "unique_slides/slide_039.jpg").convert("RGB")).astype(int)
out = []

def redm(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 120) & (R - G > 55) & (R - B > 55)
def blum(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (B > 100) & (B - R > 25) & (B - G > 18)
def yelm(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 195) & (G > 180) & (B < 170) & (R - B > 45)
def pinkm(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    return (R > 215) & (B > 185) & (R - G > 18) & (G < 225)

# ---- Y4 label window ----
for (x0, x1, y0, y1, tag) in [(665, 770, 55, 112, "Y4 label window"), (665, 770, 60, 100, "Y4 tight")]:
    reg = org[y0:y1, x0:x1]
    m = blum(reg)
    if m.sum() > 5:
        ys, xs = np.where(m)
        out.append(f"{tag}: blue_px={m.sum()} bbox x[{xs.min()+x0},{xs.max()+x0}] y[{ys.min()+y0},{ys.max()+y0}]")
    else:
        out.append(f"{tag}: blue_px={m.sum()}")

# ---- box fills ----
out.append(f"Wk fill (x204-222,y303-307): {org[303:308,204:223].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"Wk fill row2 (x204-222,y331-335): {org[331:336,204:223].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"WV fill (x578-596,y302-307): {org[302:308,578:597].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"WV fill2 (x578-596,y330-334): {org[330:335,578:597].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"right container fill (x620-660,y310-312): {org[310:313,620:661].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"right X-cell (x648-666,y295-298): {org[295:299,648:667].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"right X-cell (x648-666,y323-326): {org[323:327,648:667].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"right yellow cell (x615-630,y295-298): {org[295:299,615:631].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"left cell fill (x133-143,y290-293): {org[290:294,133:144].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"left cell pink part (x166-184,y295-298): {org[295:299,166:185].reshape(-1,3).mean(axis=0).round(0)}")
out.append(f"left cell yellow part (x133-146,y352-356): {org[352:357,133:147].reshape(-1,3).mean(axis=0).round(0)}")

# ---- row-line start x ----
for yy in [299, 327, 355, 384]:
    row = org[yy, 130:280]
    m = redm(row)
    xs = np.where(m)[0]
    out.append(f"row line y{yy}: red x[{xs.min()+130 if len(xs) else '-'},{xs.max()+130 if len(xs) else '-'}] px={m.sum()}")

# ---- left X cells: red glyph bbox + yellow/pink cols ----
for ci, (ya, yb) in enumerate([(286, 314), (315, 343), (344, 371), (372, 400)]):
    cell = org[ya:yb + 1, 131:188]
    rmg, ymg, pmg = redm(cell), yelm(cell), pinkm(cell)
    redys, redxs = np.where(rmg)
    ycols = np.where(ymg.sum(axis=0) >= 2)[0]
    pcols = np.where(pmg.sum(axis=0) >= 2)[0]

    def colruns(cols):
        if len(cols) == 0: return []
        runs = []; s = cols[0]; p = cols[0]
        for c in cols[1:]:
            if c - p > 2: runs.append((s, p)); s = c
            p = c
        runs.append((s, p))
        return [(a + 131, b + 131) for a, b in runs]

    if len(redxs):
        out.append(f"leftcell{ci+1} y[{ya},{yb}]: red x[{redxs.min()+131},{redxs.max()+131}] y[{redys.min()+ya},{redys.max()+ya}] px={rmg.sum()}")
    else:
        out.append(f"leftcell{ci+1}: no red")
    out.append(f"    yellow col runs: {colruns(ycols)}  pink col runs: {colruns(pcols)}")
    s_ = cell.sum(axis=2); idx = np.argsort(s_.ravel())[:50]
    out.append(f"    darkest-50 avg={cell.reshape(-1,3)[idx].mean(axis=0).round(0)}")

# ---- bottom row cells ----
for nm, xa, xb in [("cell1", 266, 326), ("cell2", 328, 374), ("cell3", 376, 422), ("cell4", 424, 470)]:
    cell = org[453:489, xa:xb]
    rmg, ymg, pmg, gmg = redm(cell), yelm(cell), pinkm(cell), None
    redys, redxs = np.where(rmg)
    runs = []
    if len(redxs):
        xs_sorted = np.unique(redxs)
        s = xs_sorted[0]; p = xs_sorted[0]
        for x in xs_sorted[1:]:
            if x - p > 2: runs.append((s + xa, p + xa)); s = x
            p = x
        runs.append((s + xa, p + xa))
    out.append(f"bot {nm}: red runs={runs} redpx={rmg.sum()} yellowpx={ymg.sum()} pinkpx={pmg.sum()}")
    # red vertical extent per run
    for (ra, rb) in runs:
        m2 = rmg[:, ra - xa:rb - xa + 1]
        ys2 = np.where(m2.any(axis=1))[0]
        out.append(f"    run x[{ra},{rb}]: y[{ys2.min()+453},{ys2.max()+453}]")

# ---- fraction region ----
out.append("fraction region (x325-412, y248-306) ink runs (R=red D=dark):")
for y in range(248, 307):
    row = org[y, 325:413]
    r, d = redm(row), row.sum(axis=1) < 430
    parts = []
    for mask, ch in [(r, "R"), (d, "D")]:
        xs = np.where(mask)[0]
        if len(xs) == 0: continue
        s = xs[0]; p = xs[0]
        runs = []
        for x in xs[1:]:
            if x - p > 2: runs.append((s, p)); s = x
            p = x
        runs.append((s, p))
        parts.append(ch + ":" + ",".join(f"[{a+325}-{b+325}]" for a, b in runs))
    if parts: out.append(f"  y={y}: " + " ".join(parts))

# ---- probe crops ----
S = BASE + "scratch/slide039/"
def crop(name, x0, y0, x1, y1, scale):
    c = org[y0:y1, x0:x1].astype(np.uint8)
    im = Image.fromarray(c)
    im = im.resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.LANCZOS)
    im.save(S + name)
    return f"{name}: frame x[{x0},{x1}] y[{y0},{y1}] scale x{scale} -> {im.size}"

out.append(crop("probe_bottomrow.png", 255, 445, 495, 500, 3))
out.append(crop("probe_leftxbox.png", 125, 278, 195, 408, 3))
out.append(crop("probe_rightside.png", 555, 268, 690, 420, 3))
out.append(crop("probe_fraction.png", 308, 246, 415, 308, 4))
out.append(crop("probe_pill.png", 378, 234, 452, 262, 6))
out.append(crop("probe_yband.png", 440, 60, 800, 235, 2))

print("\n".join(out))
