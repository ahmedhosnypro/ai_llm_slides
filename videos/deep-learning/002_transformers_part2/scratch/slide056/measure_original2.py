#!/usr/bin/env python3
# measure_original2.py — corrected PIL measurement of slide_056.jpg.
# Chrome borders via JPEG-tolerant redness mask; content via tight per-color masks;
# font sizes estimated with real Arial Bold advances (PIL ImageFont).
import json
from PIL import Image, ImageFont
import numpy as np

IM = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_056.jpg"
im = Image.open(IM).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

FB = "/usr/share/fonts/TTF/Arialbd.TTF"
f1000 = ImageFont.truetype(FB, 1000)
def adv_em(s):  # Arial Bold advance width in em
    return f1000.getlength(s) / 1000.0

def ink_h_em(s):  # ink height in em (bbox at size 1000)
    img = Image.new("L", (int(f1000.getlength(s)) + 40, 1400), 0)
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    d.text((20, 200), s, font=f1000, fill=255)
    bb = img.getbbox()
    return (bb[3] - bb[1]) / 1000.0, bb

# ---- masks (JPEG-tolerant)
reddish = (r - g > 50) & (r - b > 40) & (r > 90)          # borders, title, labels, brace, arrows
darkred = (r - g > 80) & (r > 110) & (g < 70)             # softmax bar B00000
white   = (r > 245) & (g > 245) & (b > 245)               # text on bars only
bluetxt = (b - r > 60) & (b > 130) & (g < 120)            # subtitle 2222CC
navy    = (b - r > 30) & (b > 140) & (b - g > 20)         # arrows + thin lines 3366CC/2222AA
darkbl  = (b - r > 100) & (b > 130) & (r < 90)            # bottom bar 1010B0
palebl  = (b - r > 10) & (b > 238) & (g > 232)            # pale circle fill EAF5FF
mag     = (r > 180) & (b > 150) & (g < 120)               # EE00EE
green   = (g - r > 40) & (g - b > 40) & (g > 100)         # greens
palegr  = (g - r > 12) & (g > 235) & (b > 210)            # E2FFE3 fill
yellow  = (r > 200) & (g > 200) & (b < 180)

def bbox(m, x0=0, x1=None, y0=0, y1=None):
    x1 = W if x1 is None else x1
    y1 = H if y1 is None else y1
    sub = np.zeros_like(m); sub[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: return None
    return dict(x0=int(xs.min()), x1=int(xs.max()), y0=int(ys.min()), y1=int(ys.max()), n=int(len(xs)))

out = {}

# ---- chrome landmarks (thin 1px lines: max reddish count in narrow windows)
col = reddish[100:450, :].sum(axis=0)   # avoid title/labels rows partially
row = reddish[:, 150:800].sum(axis=1)
lb = 50 + int(np.argmax(col[50:75]))
rb = 890 + int(np.argmax(col[890:915]))
tb = 35 + int(np.argmax(row[35:55]))
bbm = 505 + int(np.argmax(row[505:525]))
out["chrome_frame"] = dict(left=lb, right=rb, top=tb, bottom=bbm)

# badge
yb = bbox(yellow, 845, 920, 40, 110)
out["badge_yellow_bbox"] = yb
bcx, bcy = (yb["x0"] + yb["x1"]) / 2.0, (yb["y0"] + yb["y1"]) / 2.0

# ---- mapping (slide chrome L42 R919 T45 B540)
sx = (rb - lb) / (919.0 - 42.0); ix = lb - sx * 42.0
sy = (bbm - tb) / (540.0 - 45.0); iy = tb - sy * 45.0
def mx(fx): return (fx - ix) / sx
def my(fy): return (fy - iy) / sy
out["mapping"] = dict(scale_x=round(sx, 5), off_x=round(ix, 2), scale_y=round(sy, 5), off_y=round(iy, 2))
out["badge_center_slide"] = [round(mx(bcx), 1), round(my(bcy), 1)]
out["badge_delta_vs_house_px"] = [round(mx(bcx) - 893, 1), round(my(bcy) - 71, 1)]

def slide_bb(bb_):
    return dict(x0=round(mx(bb_["x0"]), 1), x1=round(mx(bb_["x1"] + 1), 1),
                y0=round(my(bb_["y0"]), 1), y1=round(my(bb_["y1"] + 1), 1),
                cx=round(mx((bb_["x0"] + bb_["x1"] + 1) / 2.0), 1),
                cy=round(my((bb_["y0"] + bb_["y1"] + 1) / 2.0), 1),
                w=round(mx(bb_["x1"] + 1) - mx(bb_["x0"]), 1),
                h=round(my(bb_["y1"] + 1) - my(bb_["y0"]), 1))

def band(name, m, x0, x1, y0, y1):
    bb_ = bbox(m, x0, x1, y0, y1)
    if bb_: bb_["slide"] = slide_bb(bb_)
    out[name] = bb_
    return bb_

# ---- content
title = band("title", reddish, lb + 3, rb - 3, tb + 8, 100)
sub   = band("subtitle", bluetxt, 200, 800, 98, 125)
brace = band("brace", reddish, 150, 850, (sub["y1"] if sub else 117) + 2, 143)
palef = band("pale_row_fill", palebl, lb + 3, rb - 3, 128, 182)
vl1   = band("vocab_label_1", reddish, lb + 3, 170, 135, 175)
sm    = band("softmax_bar", darkred, lb + 3, rb - 3, 200, 290)
if sm: band("softmax_text", white, sm["x0"] + 3, sm["x1"] - 3, sm["y0"] + 3, sm["y1"] - 2)
gbf   = band("greenbox_fill", palegr, lb + 3, rb - 3, 275, 460)
gbb   = band("greenbox_border", green, lb + 3, rb - 3, 275, 460)
magr  = band("magenta_row", mag, lb + 3, rb - 3, 285, 385)
gcir  = band("green_circles", green, 200, 700, 385, 450)
lp    = band("linproj_label", green, 600, rb - 5, 385, 450)
vl2   = band("vocab_label_2", reddish, lb + 3, 170, 300, 370)
blb   = band("blue_bar", darkbl, lb + 3, rb - 3, 450, 512)
if blb: band("blue_bar_text", white, blb["x0"] + 3, blb["x1"] - 3, blb["y0"] + 3, blb["y1"] - 2)
# arrows
if palef and sm: band("blue_arrows", navy, lb + 3, rb - 3, palef["y1"] + 3, sm["y0"] - 1)
if sm and gbf:   band("red_arrows", darkred, lb + 3, rb - 3, sm["y1"] + 2, gbf["y0"] - 1)
if gbb and blb:  band("green_arrows", green, 200, 700, gbb["y1"] + 2, blb["y0"] - 1)
if magr and gcir: band("conn_lines", navy, 170, 830, magr["y1"] + 2, gcir["y0"] - 1)

# ---- runs / clusters
def runs(m, y0, y1, min_run=2, x0=0, x1=None):
    x1 = W if x1 is None else x1
    colhit = m[y0:y1, x0:x1].sum(axis=0) > 0
    rr, s = [], None
    for i, v in enumerate(colhit):
        if v and s is None: s = i
        elif not v and s is not None:
            if i - s >= min_run: rr.append((x0 + s, x0 + i - 1))
            s = None
    if s is not None: rr.append((x0 + s, x1 - 1))
    return rr

def circ_report(name, m, bb_, min_run=3, x0=lb + 3, x1=rb - 3):
    if not bb_: return
    rr = runs(m, bb_["y0"], bb_["y1"] + 1, min_run, x0, x1)
    out[name + "_n"] = len(rr)
    if rr:
        d = float(np.median([e - s2 + 1 for s2, e in rr]))
        out[name + "_diam_frame"] = d
        out[name + "_diam_slide"] = round(d / sx, 1)
        out[name + "_centers_slide_x"] = [round(mx((s2 + e + 1) / 2.0), 1) for s2, e in rr]
        out[name + "_first_center_slide_x"] = out[name + "_centers_slide_x"][0]
        out[name + "_last_center_slide_x"] = out[name + "_centers_slide_x"][-1]

circ_report("pale", palebl, palef)
# pale circle vertical extent from fill+outline rows at the first circle column
if palef:
    ys, xs = np.nonzero((palebl | ((b - r > 8) & (b > 150) & (r < 200)))[palef["y0"] - 12:palef["y1"] + 12, 186:210])
    if len(ys):
        out["pale_row_y_frame"] = [int(ys.min()) + palef["y0"] - 12, int(ys.max()) + palef["y0"] - 12]
        out["pale_row_y_slide"] = [round(my(ys.min() + palef["y0"] - 12), 1), round(my(ys.max() + palef["y0"] - 12 + 1), 1)]
circ_report("magenta", mag, magr)
if magr:
    ys, xs = np.nonzero(mag[magr["y0"] - 6:magr["y1"] + 6, 190:214])
    out["magenta_row_y_frame"] = [int(ys.min()) + magr["y0"] - 6, int(ys.max()) + magr["y0"] - 6]
    out["magenta_row_y_slide"] = [round(my(ys.min() + magr["y0"] - 6), 1), round(my(ys.max() + magr["y0"] - 6 + 1), 1)]
circ_report("green", green, gcir, min_run=3, x0=200, x1=700)
if gcir:
    ys, xs = np.nonzero(green[gcir["y0"] - 6:gcir["y1"] + 6, 390:414])
    out["green_row_y_frame"] = [int(ys.min()) + gcir["y0"] - 6, int(ys.max()) + gcir["y0"] - 6]
    out["green_row_y_slide"] = [round(my(ys.min() + gcir["y0"] - 6), 1), round(my(ys.max() + gcir["y0"] - 6 + 1), 1)]

for nm in ("blue_arrows", "red_arrows", "green_arrows"):
    z = out.get(nm)
    if z:
        mmask = {"blue_arrows": navy, "red_arrows": darkred, "green_arrows": green}[nm]
        rr = runs(mmask, z["y0"], z["y1"] + 1, 1, lb + 3, rb - 3)
        out[nm + "_n"] = len(rr)
        out[nm + "_centers_slide_x"] = [round(mx((s2 + e + 1) / 2.0), 1) for s2, e in rr]

# ---- font size estimates (ink width / advance em)
def fs(name, text, bb_):
    if not bb_: return
    w_pt = bb_["slide"]["w"]
    ae = adv_em(text)
    out[name + "_font"] = dict(text=text, ink_w_pt=w_pt, adv_em=round(ae, 3),
                               est_pt=round(w_pt / ae, 1),
                               est_from_h=round(bb_["slide"]["h"] / ink_h_em(text)[0], 1))

fs("title_fs", "Decoder Final Output", title)
fs("subtitle_fs", "Probability of each word in Vocab", sub)
fs("vl1_fs", "Vocab Size", vl1)
fs("vl2_fs", "Vocab Size", vl2)
fs("softmax_fs", "Softmax", out.get("softmax_text"))
fs("bluebar_fs", "Last Decoder Block", out.get("blue_bar_text"))
fs("linproj_fs", "Linear Projection", lp)

print(json.dumps(out, indent=1, default=str))
