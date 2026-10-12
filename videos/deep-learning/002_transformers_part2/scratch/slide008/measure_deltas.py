#!/usr/bin/env python3
"""Delta-zone measurements on 002:slide_008.jpg (frame px).

Zones: W_k green boxes, W_v blue boxes, W_q purple box, blue annotation circle,
Y output strip (subscript?), multiply nodes (glyph/count), q2 label, X2 arrow.
Also transform-checks the DP box and prints converted slide-px values.
"""
import numpy as np
from PIL import Image

F8 = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
im = np.asarray(Image.open(F8).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

AX, SX, SY = 17.628, 0.961232, 0.955556
def to_slide_x(fx): return (fx - AX) / SX
def to_slide_y(fy): return fy / SY

def region(x0, x1, y0, y1):
    return dict(x0=x0, x1=x1, y0=y0, y1=y1)

def mask_in(reg, cr, cg, cb, tol):
    xs = slice(reg["x0"], reg["x1"]); ys = slice(reg["y0"], reg["y1"])
    return ((abs(r[ys, xs] - cr) < tol) & (abs(g[ys, xs] - cg) < tol) & (abs(b[ys, xs] - cb) < tol))

def bb(m, ox, oy):
    ys, xs = np.where(m)
    if not len(xs): return None
    return (ox + xs.min(), ox + xs.max(), oy + ys.min(), oy + ys.max(), len(xs))

def show(name, box, conv=True):
    if box is None:
        print(f"{name}: NONE"); return
    x0, x1, y0, y1, n = box
    line = f"{name}: frame x {x0}..{x1} (w {x1-x0+1}), y {y0}..{y1} (h {y1-y0+1}), n={n}"
    if conv:
        line += (f"  | slide x {to_slide_x(x0):.1f}..{to_slide_x(x1):.1f} (w {(to_slide_x(x1)-to_slide_x(x0)):.1f})"
                 f", y {to_slide_y(y0):.1f}..{to_slide_y(y1):.1f} (h {(to_slide_y(y1)-to_slide_y(y0)):.1f})")
    print(line)

# --- 1. sample raw colors along the W_k / W_v columns (centers of expected rows)
print("== W_k column samples (frame x 165..205) ==")
for y in [222, 246, 264, 288, 305, 329, 349, 372]:
    px = im[y, 180]; px2 = im[y, 175]; print(f"y={y}: @(180,{y})={tuple(px)} @(175,{y})={tuple(px2)}")
print("== W_v column samples (frame x 692..732) ==")
for y in [222, 246, 264, 288, 305, 329, 349, 372]:
    px = im[y, 710]; print(f"y={y}: @(710,{y})={tuple(px)}")
print("== W_q box samples (frame ~278..327, y ~409..447) ==")
for (x, y) in [(290, 420), (300, 428), (310, 435), (300, 415), (300, 440)]:
    print(f"@({x},{y})={tuple(im[y, x])}")

# --- 2. green box masks (spec 8FBC8F; try a few tol)
reg = region(140, 240, 205, 415)
m = mask_in(reg, 0x8F, 0xBC, 0x8F, 30)
show("green_wk_all", bb(m, 140, 205))
# per-row split: histogram of green rows
ys, xs = np.where(m)
if len(ys):
    rows = np.zeros(reg["y1"] - reg["y0"])
    for yy in ys: rows[yy] += 1
    runs = []
    s = None
    for i, v in enumerate(rows):
        if v > 8 and s is None: s = i
        elif v <= 8 and s is not None: runs.append((s, i - 1)); s = None
    if s is not None: runs.append((s, len(rows) - 1))
    print("green row runs (frame y):", [(205 + a, 205 + bb_) for a, bb_ in runs])
    for (a, bb_) in runs:
        sub = m[a:bb_ + 1, :]
        yy, xx = np.where(sub)
        print(f"  run y {205+a}..{205+bb_}: x {140+xx.min()}..{140+xx.max()}")

# --- 3. blue box masks (spec B8D8F0)
reg = region(660, 760, 205, 415)
m = mask_in(reg, 0xB8, 0xD8, 0xF0, 28)
show("blue_wv_all", bb(m, 660, 205))
ys, xs = np.where(m)
if len(ys):
    rows = np.zeros(reg["y1"] - reg["y0"])
    for yy in ys: rows[yy] += 1
    runs = []
    s = None
    for i, v in enumerate(rows):
        if v > 8 and s is None: s = i
        elif v <= 8 and s is not None: runs.append((s, i - 1)); s = None
    if s is not None: runs.append((s, len(rows) - 1))
    print("blue row runs (frame y):", [(205 + a, 205 + bb_) for a, bb_ in runs])
    for (a, bb_) in runs:
        sub = m[a:bb_ + 1, :]
        yy, xx = np.where(sub)
        print(f"  run y {205+a}..{205+bb_}: x {660+xx.min()}..{660+xx.max()}")

# --- 4. purple W_q (spec C9A0DC)
reg = region(260, 350, 395, 465)
m = mask_in(reg, 0xC9, 0xA0, 0xDC, 30)
show("purple_wq", bb(m, 260, 395))

# --- 5. blue annotation circle: bluish over peach
reg = region(180, 440, 320, 517)
R, G, B = r[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]], g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]], b[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]]
m = (B > R + 25) & (B > G + 15) & (B > 120)
show("blue_circle", bb(m, reg["x0"], reg["y0"]))
# sample the circle interior color
if m.sum() > 100:
    yy, xx = np.where(m)
    cy, cx = int(np.median(yy)), int(np.median(xx))
    print("blue circle approx center (frame):", reg["x0"] + cx, reg["y0"] + cy, "color:", tuple(im[reg["y0"] + cy, reg["x0"] + cx]))
    # per-row extents for center/size
    for dy in (-40, -20, 0, 20, 40):
        row = m[cy + dy, :]
        xr = np.where(row)[0]
        if len(xr): print(f"  row y={reg['y0']+cy+dy}: x {reg['x0']+xr.min()}..{reg['x0']+xr.max()} (w {xr.max()-xr.min()+1})")

# --- 6. Y output strip (parent slide 549..619,121..146 -> frame ~545..612,116..140)
reg = region(535, 625, 105, 150)
m = mask_in(reg, 0x9C, 0xCB, 0x96, 30)  # y2c1 green cells
show("out_cells_green", bb(m, 535, 105))
m2 = mask_in(reg, 0xC9, 0xD6, 0xDA, 25)  # y2c4 blue-gray cells
show("out_cells_gray", bb(m2, 535, 105))
# dark ink in the strip region (the Y label + possible subscript)
ink = (R_ := r[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]]) 
dk = (r[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] < 120) & (g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] < 150)
show("out_ink_dark", bb(dk, 535, 105))
# green text ink (Y label ~ green)
grn = (g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 110) & (g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] - r[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 40) & (g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] - b[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 30)
show("out_ink_green", bb(grn, 535, 105))

# --- 7. multiply nodes: white circles with red ring, x 500..640, y 215..385
reg = region(495, 650, 215, 390)
wt = (r[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 235) & (g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 235) & (b[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 230)
show("white_circ_all", bb(wt, 495, 215))
ys, xs = np.where(wt)
if len(ys):
    # cluster by y gaps
    order = np.argsort(ys)
    ys_s = ys[order]; xs_s = xs[order]
    clusters = []
    cur = [0]
    for i in range(1, len(ys_s)):
        if ys_s[i] - ys_s[i - 1] > 8:
            clusters.append(cur); cur = []
        cur.append(i)
    clusters.append(cur)
    print(f"white clusters: {len(clusters)}")
    for cl in clusters:
        cys = ys_s[cl]; cxs = xs_s[cl]
        if len(cl) > 20:
            print(f"  cluster y {215+cys.min()}..{215+cys.max()} x {495+cxs.min()}..{495+cxs.max()} n={len(cl)} center=({495+cxs.mean():.0f},{215+cys.mean():.0f})")

# --- 8. DP box transform check (parent slide 255..342, 194..402 -> frame ~263..346, 185..384)
reg = region(240, 370, 175, 400)
m = mask_in(reg, 0xDC, 0xCB, 0xBB, 14)
show("dp_box_f8", bb(m, 240, 175))

# --- 9. X2->W_q arrow + q2 label ink (dark red) around frame x 283..320, y 380..460
reg = region(275, 330, 375, 470)
dkred = (r[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 90) & (r[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] - g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] > 50) & (g[reg["y0"]:reg["y1"], reg["x0"]:reg["x1"]] < 90)
show("q_ink_darkred", bb(dkred, 275, 375))
