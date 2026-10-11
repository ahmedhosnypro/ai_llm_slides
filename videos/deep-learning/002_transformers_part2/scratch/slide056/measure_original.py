#!/usr/bin/env python3
# measure_original.py — PIL-measure slide_056.jpg (960x540) chrome landmarks + all
# content ink, then map frame px -> true slide pt through the four chrome border
# landmarks (method of certified slide_002 build).
import json
from PIL import Image
import numpy as np

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_056.jpg"
im = Image.open(IM).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

def bbox(m, x0=0, x1=None, y0=0, y1=None):
    x1 = W if x1 is None else x1
    y1 = H if y1 is None else y1
    sub = np.zeros_like(m)
    sub[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None
    return dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()),
                n=int(len(xs)))

# ---- masks
red    = (r > 120) & (g < 80) & (b < 80)                       # C00000-ish (border, title, labels, arrows, brace)
darkred= (r > 120) & (g < 60) & (b < 60)
white  = (r > 225) & (g > 225) & (b > 225)
blue_t = (b > 120) & (r < 110) & (g < 110)                     # blue text (subtitle)
navy   = (b > 100) & (b - r > 60) & (b - g > 40)               # navy arrows / bar / lines
darkbl = (b > 120) & (r < 70) & (g < 70)                       # dark blue bar
palebl = (b > 230) & (r > 195) & (r < 250) & (g > 225)         # pale circle fill EAF5FF
blgr   = (b > 150) & (b - r > 20) & (g > 110) & (g < 200) & (r < 170)  # blue-gray outline
mag    = (r > 190) & (b > 170) & (g < 110)                     # magenta EE00EE
green  = (g > 110) & (g - r > 60) & (g - b > 60)               # greens (border, circles, label, arrows)
palegr = (g > 200) & (r > 190) & (b > 190) & (g - r > 8)       # pale green fill E2FFE3
yellow = (r > 200) & (g > 200) & (b < 170)
black  = (r < 60) & (g < 60) & (b < 60)

out = {}
out["size"] = [W, H]

# ---- chrome landmarks
colcnt = red[:, :].sum(axis=0)
rowcnt = red[:, :].sum(axis=1)
# left border: column with most red in x 40..90 (vertical line)
lb = 40 + int(np.argmax(colcnt[40:90]))
rb = 880 + int(np.argmax(colcnt[880:930]))
tb = 30 + int(np.argmax(rowcnt[30:60]))
# bottom border: strongest red row 495..535
bb = 495 + int(np.argmax(rowcnt[495:535]))
out["chrome_frame"] = dict(left=lb, right=rb, top=tb, bottom=bb)

# badge yellow bbox (top right)
yb = bbox(yellow, 850, 960, 20, 110)
out["badge_yellow_bbox"] = yb
bcx = (yb["x0"] + yb["x1"]) / 2.0
bcy = (yb["y0"] + yb["y1"]) / 2.0
out["badge_center_frame"] = [bcx, bcy]

# ---- mapping frame->slide (slide chrome: L=42 R=919 T=45 B=540)
sx = (rb - lb) / (919.0 - 42.0)
ix = lb - sx * 42.0
sy = (bb - tb) / (540.0 - 45.0)
iy = tb - sy * 45.0
out["mapping"] = dict(scale_x=sx, off_x=ix, scale_y=sy, off_y=iy)
def mx(fx): return (fx - ix) / sx
def my(fy): return (fy - iy) / sy
out["badge_center_slide"] = [round(mx(bcx), 1), round(my(bcy), 1)]
out["badge_expect_slide"] = [893, 71]
out["badge_delta_px"] = [round(mx(bcx) - 893, 1), round(my(bcy) - 71, 1)]

# ---- content ink measurements (frame coords) -------------------------------
def band(name, m, x0, x1, y0, y1):
    bb_ = bbox(m, x0, x1, y0, y1)
    if bb_:
        bb_["slide"] = dict(
            x0=round(mx(bb_["x0"]), 1), x1=round(mx(bb_["x1"]), 1),
            y0=round(my(bb_["y0"]), 1), y1=round(my(bb_["y1"]), 1),
            cx=round(mx((bb_["x0"] + bb_["x1"]) / 2.0), 1),
            cy=round(my((bb_["y0"] + bb_["y1"]) / 2.0), 1))
    out[name] = bb_
    return bb_

# title: red text near top (exclude border columns)
band("title", red, lb + 5, rb - 5, tb + 5, 110)
# subtitle: blue text
band("subtitle", blue_t, 200, 800, 95, 122)
# brace: red pixels between subtitle bottom and circles top
band("brace", red, 150, 850, 118, 142)
# pale circles row (fill)
band("pale_row_fill", palebl, lb + 5, rb - 5, 130, 180)
# pale circle outlines
band("pale_row_outline", blgr, lb + 5, rb - 5, 130, 180)
# Vocab Size label 1 (left, red text, aligned with pale row)
band("vocab_label_1", red, lb + 5, 165, 130, 185)
# softmax bar: rows where darkred count is big
rowdr = darkred.sum(axis=1)
smrows = [y for y in range(180, 320) if rowdr[y] > 300]
out["softmax_rows_frame"] = [min(smrows), max(smrows)] if smrows else None
if smrows:
    band("softmax_bar", darkred, lb + 5, rb - 5, min(smrows), max(smrows) + 1)
    # white text inside bar
    band("softmax_text", white, lb + 5, rb - 5, min(smrows), max(smrows) + 1)
# green box: pale green fill + green border
band("greenbox_fill", palegr, lb + 5, rb - 5, 280, 470)
band("greenbox_border", green, lb + 5, rb - 5, 280, 470)
# magenta row
band("magenta_row", mag, lb + 5, rb - 5, 280, 380)
# green circles (solid green, below magenta row, above box bottom)
band("green_circles", green, lb + 5, rb - 5, 380, 445)
# Linear Projection label: green text right side
band("linproj_label", green, 600, rb - 5, 380, 445)
# Vocab Size label 2
band("vocab_label_2", red, lb + 5, 165, 300, 370)
# blue bar bottom
rowdb = darkbl.sum(axis=1)
dbrows = [y for y in range(430, 530) if rowdb[y] > 300]
out["bluebar_rows_frame"] = [min(dbrows), max(dbrows)] if dbrows else None
if dbrows:
    band("blue_bar", darkbl, lb + 5, rb - 5, min(dbrows), max(dbrows) + 1)
    band("blue_bar_text", white, lb + 5, rb - 5, min(dbrows), max(dbrows) + 1)
# blue arrows band: navy pixels between pale row bottom and softmax top
pale_b = out["pale_row_fill"]["y1"] if out["pale_row_fill"] else 172
sm_t = out["softmax_rows_frame"][0] if smrows else 226
band("blue_arrows", navy, lb + 5, rb - 5, pale_b + 2, sm_t - 1)
# red arrows band: between softmax bottom and green box top
sm_b = out["softmax_rows_frame"][1] if smrows else 258
gb_t = out["greenbox_fill"]["y0"] if out["greenbox_fill"] else 300
band("red_arrows", darkred, lb + 5, rb - 5, sm_b + 2, gb_t - 1)
# green arrows: between blue bar top and green circles bottom
gb_b = out["greenbox_border"]["y1"] if out["greenbox_border"] else 432
bl_t = out["blue_bar"]["y0"] if out["blue_bar"] else 462
band("green_arrows", green, lb + 5, rb - 5, gb_b + 2, bl_t - 1)
# thin blue connector lines inside green box
band("conn_lines", navy, 170, 830, 320, 400)
# black letterbox strip
band("black_strip", black, 0, W, 505, H)

# ---- per-circle clustering -------------------------------------------------
def runs(m, y0, y1, min_run=3, x0=0, x1=None):
    x1 = W if x1 is None else x1
    colhit = m[y0:y1, x0:x1].sum(axis=0) > 0
    rr = []
    s = None
    for i, v in enumerate(colhit):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= min_run:
                rr.append((x0 + s, x0 + i - 1))
            s = None
    if s is not None:
        rr.append((x0 + s, x0 + x1 - 1))
    return rr

pale_f = out["pale_row_fill"]
if pale_f:
    rr = runs(palebl, pale_f["y0"], pale_f["y1"] + 1, min_run=4)
    out["pale_circles_frame"] = [[a, b_] for a, b_ in rr]
    out["pale_circles_n"] = len(rr)
    if rr:
        d = np.median([b_ - a + 1 for a, b_ in rr])
        cxs = [round(mx((a + b_) / 2.0), 1) for a, b_ in rr]
        out["pale_circ_diam_frame"] = int(d)
        out["pale_circ_diam_slide"] = round(mx(d) - mx(0), 1)
        out["pale_circ_centers_slide_x"] = cxs
        out["pale_circ_first_last_slide_x"] = [cxs[0], cxs[-1]]

mag_f = out["magenta_row"]
if mag_f:
    rr = runs(mag, mag_f["y0"], mag_f["y1"] + 1, min_run=4)
    out["magenta_circles_n"] = len(rr)
    if rr:
        d = np.median([b_ - a + 1 for a, b_ in rr])
        out["magenta_diam_frame"] = int(d)
        out["magenta_diam_slide"] = round(mx(d) - mx(0), 1)
        out["magenta_centers_slide_x"] = [round(mx((a + b_) / 2.0), 1) for a, b_ in rr]

gc = out["green_circles"]
if gc:
    rr = runs(green, gc["y0"], gc["y1"] + 1, min_run=4, x0=200, x1=700)
    out["green_circles_n"] = len(rr)
    if rr:
        d = np.median([b_ - a + 1 for a, b_ in rr])
        out["green_diam_frame"] = int(d)
        out["green_diam_slide"] = round(mx(d) - mx(0), 1)
        out["green_centers_slide_x"] = [round(mx((a + b_) / 2.0), 1) for a, b_ in rr]

# arrow column clusters (count arrows)
for nm in ("blue_arrows", "red_arrows", "green_arrows"):
    z = out.get(nm)
    if z:
        mmask = {"blue_arrows": navy, "red_arrows": darkred, "green_arrows": green}[nm]
        rr = runs(mmask, z["y0"], z["y1"] + 1, min_run=1, x0=lb + 5, x1=rb - 5)
        out[nm + "_n"] = len(rr)
        out[nm + "_centers_slide_x"] = [round(mx((a + b_) / 2.0), 1) for a, b_ in rr]

# connector line sample rows inside box (between magenta bottom and green top)
m_b = out["magenta_row"]["y1"] if out["magenta_row"] else 350
g_t = out["green_circles"]["y0"] if out["green_circles"] else 392
band("conn_band", navy, 170, 830, m_b + 2, g_t - 1)

print(json.dumps(out, indent=1, default=str))
