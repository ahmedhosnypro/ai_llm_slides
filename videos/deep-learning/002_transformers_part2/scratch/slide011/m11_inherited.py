#!/usr/bin/env python3
"""m11: consolidated verification of 015-inherited structures against frame11.
Each check prints PASS/DELTA with measured values."""
from PIL import Image
from collections import Counter
import json

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
im = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
px = im.load()
res = {}

def near(p, t, tol):
    return all(abs(p[i] - t[i]) <= tol for i in range(3))

def mask_bbox(pts):
    if not pts: return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys), len(pts))

# cards' fill colors sampled from frame11 at 015-card interior points
samples = {
    "h5(267+400,104+40)=(667,144)": px[667, 144],
    "h4(223+400,122+40)=(623,162)": px[623, 162],
    "h3(181+400,143+40)=(581,183)": px[581, 183],
    "h2(140+400,163+40)=(540,203)": px[540, 203],
    "h1(91+400,186+40)=(491,226)": px[491, 226],
}
res["card_fill_samples"] = {k: '#%02X%02X%02X' % v for k, v in samples.items()}

# h1 card edges: red-fill runs at y=300 and vertical at x=300
r1 = [x for x in range(40, 940) if near(px[x, 300], (240, 139, 150), 26)]
res["h1_row300_span"] = (min(r1), max(r1)) if r1 else None
r2 = [y for y in range(60, 520) if near(px[300, y], (240, 139, 150), 26)]
res["h1_col300_span"] = (min(r2), max(r2)) if r2 else None

# card left edges above h1: at y=175 (h2 strip), y=155 (h3), y=135 (h4), y=115 (h5)
for y, lbl in ((175, "h2"), (155, "h3"), (135, "h4"), (115, "h5")):
    row = [x for x in range(45, 935) if not near(px[x, y], (255, 255, 255), 16) and not near(px[x, y], (233, 233, 231), 12)]
    if row:
        res[f"{lbl}_y{y}_first_ink"] = min(row)

# pills row: white ovals (Similarity/Probabilities/Weighted SUM) — white runs at y=195
w = [x for x in range(92, 646) if near(px[x, 195], (255, 255, 255), 14)]
runs = []
if w:
    s = e = w[0]
    for x in w[1:]:
        if x - e <= 5: e = x
        else: runs.append((s, e)); s = e = x
    runs.append((s, e))
res["pillrow_y195_runs"] = runs

# Probabilities ovals (015: 349,186,53x18 & 396,167,53x18): white at y=175 x340..460
w2 = [x for x in range(335, 470) if near(px[x, 175], (255, 255, 255), 14)]
runs2 = []
if w2:
    s = e = w2[0]
    for x in w2[1:]:
        if x - e <= 5: e = x
        else: runs2.append((s, e)); s = e = x
    runs2.append((s, e))
res["probrow_y175_runs"] = runs2

# outContainers: dashed border green at x575/639/691/735/763 (015) — check vertical green runs at x=575+21 etc
for cx in (596, 656, 707, 754, 784):
    g = [y for y in range(130, 380) if px[cx, y][1] - px[cx, y][0] > 35 and px[cx, y][1] > 110 and px[cx, y][0] < 160]
    res[f"outcont_x{cx}_green_rows"] = (min(g), max(g), len(g)) if g else None

# nodes: red rings around (417.6,248),(438.4,275.2),(458.3,302.9),(479.7,333.8)
for nx, ny in ((417.6, 248), (438.4, 275.2), (458.3, 302.9), (479.7, 333.8)):
    ring = [1 for y in range(int(ny) - 9, int(ny) + 10) for x in range(int(nx) - 9, int(nx) + 10)
            if near(px[x, y], (204, 34, 34), 60) and px[x, y][0] - px[x, y][1] > 80]
    res[f"node_{int(nx)}_{int(ny)}_redpx"] = len(ring)

# W_v right boxes (015: x538..558, tops 241/268/295/325): mint fill E0F0E0
for yt in (241, 268, 295, 325):
    m = [(x, y) for y in range(yt - 4, yt + 19) for x in range(532, 566) if near(px[x, y], (224, 240, 224), 14)]
    res[f"wvbox_y{yt}_mint"] = mask_bbox(m)

# K bars + labels left (015: bars x156..184, K labels x177..193 above rows)
res["kbar_check_y248"] = [ (x, '#%02X%02X%02X' % px[x, 248]) for x in (158, 168, 178, 182) ]

# dots (blue similarity dots 015 DOTS): dark blue circles at (280.5,247),(269.5,272),(254.5,304),(244,333)
for dx, dy in ((280.5, 247), (269.5, 272), (254.5, 304), (244, 333)):
    b = [1 for y in range(int(dy) - 7, int(dy) + 8) for x in range(int(dx) - 7, int(dx) + 8)
         if near(px[x, y], (43, 75, 208), 60) and px[x, y][2] - px[x, y][0] > 60]
    res[f"dot_{int(dx)}_{int(dy)}_bluepx"] = len(b)

# green arrow (015: 427,175 -> 448,186 bright green 2.5w)
ga = [(x, y) for y in range(168, 192) for x in range(420, 455)
      if near(px[x, y], (0, 170, 0), 60) and px[x, y][1] - px[x, y][0] > 80]
res["green_arrow_bbox"] = mask_bbox(ga)

# red up-arrows chain (015: x501/543/586/630, y2->y1): red vertical segments
for x0, y1, y2 in ((501, 160, 150), (543, 140, 130), (586, 120, 110), (630, 100, 90)):
    r = [1 for y in range(min(y1, y2) - 6, max(y1, y2) + 12) for x in range(x0 - 4, x0 + 5)
         if near(px[x, y], (204, 0, 0), 70) and px[x, y][0] - px[x, y][1] > 100]
    res[f"chainarrow_x{x0}_redpx"] = len(r)

# plane (015 gray translucent 110,65,335x163): gray (153,153,153)@45% over card colors
res["plane_sample_(300,120)"] = '#%02X%02X%02X' % px[300, 120]
res["plane_sample_(200,90)"] = '#%02X%02X%02X' % px[200, 90]
res["plane_sample_(400,180)"] = '#%02X%02X%02X' % px[400, 180]

print(json.dumps(res, indent=1, default=str))
