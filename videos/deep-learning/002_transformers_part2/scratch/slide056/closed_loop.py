#!/usr/bin/env python3
# closed_loop.py — PIL-measure the 150dpi render and compare every element's ink
# bbox/centers against the frame-mapped targets (slide pt -> px: *150/72).
# Tolerance ~4px @150dpi (= 1.92pt). Prints per-element deltas.
import json
from PIL import Image
import numpy as np

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide056/render_1.png"
im = Image.open(RENDER).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
K = 150.0 / 72.0  # slide pt -> render px

def px(v): return v * K

masks = {
    "red_txt":   (r > 150) & (g < 70) & (b < 70),                 # C00000
    "softmaxbar":(r > 140) & (g < 40) & (b < 40),                 # B00000
    "white":     (r > 240) & (g > 240) & (b > 240),
    "subtitle":  (b > 150) & (b - r > 80) & (g < 80),             # 2222CC
    "pale":      (np.abs(r - 229) < 18) & (np.abs(g - 254) < 6) & (np.abs(b - 250) < 8),
    "ring":      (r < 90) & (g < 90) & (b > 110),                 # 2222AA ring
    "mag":       (r > 200) & (b > 200) & (g < 90),                # EE00EE
    "grnc":      (g > 150) & (g - r > 100) & (g - b > 100),       # 22C022 circles
    "gline":     (g > 100) & (g - r > 40) & (g - b > 40),         # 00A000/00AA00
    "conn":      (b > 150) & (b - r > 60) & (g > 60) & (g < 160), # 3366CC
    "bluebar":   (b > 130) & (r < 60) & (g < 60),                 # 1010B0
    "brace":     (r > 150) & (g < 60) & (b < 60),                 # CC0000
}

def bbox(m, x0, x1, y0, y1):
    sub = np.zeros_like(m); sub[y0:y1, x0:x1] = m[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0: return None
    return [int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max()), int(len(xs))]

def runs(m, y0, y1, x0, x1, min_run=3):
    colhit = m[y0:y1, x0:x1].sum(axis=0) > 0
    rr, s = [], None
    for i, v in enumerate(colhit):
        if v and s is None: s = i
        elif not v and s is not None:
            if i - s >= min_run: rr.append((x0 + s, x0 + i - 1))
            s = None
    if s is not None: rr.append((x0 + s, x1 - 1))
    return rr

# targets: [x0,x1,y0,y1] in slide pt (from measure2/debug passes)
T = {
    "title":    [342.7, 655.8, 64.8, 95.1],
    "subtitle": [380.1, 625.6, 109.7, 123.3],
    "brace":    [182.4, 819.7, 126.5, 143.2],
    "vocab1":   [62.8, 142.9, 153.6, 166.1],
    "softmaxbar":[152.3, 847.3, 235.6, 276.3],
    "gbox":     [152.8, 846.7, 315.5, 450.7],
    "linproj":  [655.8, 816.0, 420.9, 437.7],
    "vocab2":   [62.8, 144.0, 345.8, 358.3],
    "bluebar":  [152.3, 847.3, 483.1, 522.7],
}
BANDS = {
    "title":    ("red_txt", 600, 1450, 100, 230),
    "subtitle": ("subtitle", 700, 1400, 210, 275),
    "brace":    ("brace", 300, 1750, 250, 305),
    "vocab1":   ("red_txt", 100, 340, 300, 360),
    "softmaxbar":("softmaxbar", 250, 1850, 460, 600),
    "gbox":     ("gline", 250, 1850, 630, 970),
    "linproj":  ("gline", 1330, 1740, 850, 930),
    "vocab2":   ("red_txt", 100, 340, 700, 770),
    "bluebar":  ("bluebar", 250, 1850, 980, 1110),
}
out = {}
for name, (mk, x0, x1, y0, y1) in BANDS.items():
    bb = bbox(masks[mk], x0, x1, y0, y1)
    t = T[name]
    if bb:
        d = [round(bb[i] - px(t[i]), 1) for i in range(4)]
        out[name] = dict(render=bb[:4], target_px=[round(px(v), 1) for v in t], delta=d, n=bb[4])
    else:
        out[name] = dict(render=None, target_px=[round(px(v), 1) for v in t])

# pale row: fill+ring
pr = bbox(masks["pale"] | masks["ring"], 300, 1780, 290, 410)
t = [173.5, 825.25, 149.7, 185.7]  # grid x0-18 .. last+18 ; cy 167.7 +- 18
if pr:
    out["pale_row"] = dict(render=pr[:4], target_px=[round(px(v), 1) for v in t],
                           delta=[round(pr[i] - px(t[i]), 1) for i in range(4)], n=pr[4])
    rr = runs(masks["pale"] | masks["ring"], pr[2], pr[3] + 1, 300, 1780, 5)
    out["pale_n"] = len(rr)
    if rr:
        out["pale_first_c"] = round((rr[0][0] + rr[0][1]) / 2, 1)
        out["pale_last_c"] = round((rr[-1][0] + rr[-1][1]) / 2, 1)
        out["pale_target_first_last"] = [round(px(191.5), 1), round(px(807.25), 1)]

# softmax text (white inside bar)
sb = out["softmaxbar"]["render"]
if sb:
    st = bbox(masks["white"], sb[0] + 5, sb[1] - 5, sb[2] + 5, sb[3] - 4)
    if st:
        out["softmax_text"] = dict(render=st[:4], n=st[4],
                                   cx=round((st[0] + st[1]) / 2, 1), cy=round((st[2] + st[3]) / 2, 1),
                                   target_cx=round(px(498.6), 1), target_cy=round(px(254.9), 1))
# blue bar text
bb_ = out["bluebar"]["render"]
if bb_:
    bt = bbox(masks["white"], bb_[0] + 5, bb_[1] - 5, bb_[2] + 5, bb_[3] - 4)
    if bt:
        out["bluebar_text"] = dict(render=bt[:4], n=bt[4],
                                   cx=round((bt[0] + bt[1]) / 2, 1), cy=round((bt[2] + bt[3]) / 2, 1),
                                   target_cx=round(px(500.2), 1), target_cy=round(px(503.4), 1))
# magenta row
mr = bbox(masks["mag"], 300, 1780, 680, 790)
if mr:
    out["mag_row"] = dict(render=mr[:4], target_px=[round(px(176), 1), round(px(822.75), 1), round(px(336), 1), round(px(367)), 1],
                          delta=[round(mr[i] - px([176, 822.75, 336, 367][i]), 1) for i in range(4)])
    rr = runs(masks["mag"], mr[2], mr[3] + 1, 300, 1780, 5)
    out["mag_n"] = len(rr)
# green circles
gc = bbox(masks["grnc"], 700, 1300, 830, 960)
if gc:
    out["grn_row"] = dict(render=gc[:4], target_px=[round(px(380.8), 1), round(px(561.5), 1), round(px(411.9), 1), round(px(445.9), 1)],
                          delta=[round(gc[i] - px([380.8, 561.5, 411.9, 445.9][i]), 1) for i in range(4)])
    rr = runs(masks["grnc"], gc[2], gc[3] + 1, 700, 1300, 5)
    out["grn_n"] = len(rr)
# red arrow band (between bar and box)
ra = bbox(masks["brace"], 300, 1780, 576, 660)
if ra:
    out["red_arrows_band"] = dict(render=ra[:4], n=ra[4],
                                  target_y=[round(px(276.3), 1), round(px(315.5), 1)])
# blue arrow band
ba = bbox(masks["ring"] | masks["conn"], 300, 1780, 392, 492)
if ba:
    out["blue_arrows_band"] = dict(render=ba[:4], n=ba[4],
                                   target_y=[round(px(190.5), 1), round(px(235.6), 1)])
# green arrow band (below box, above bar) - green line color
ga = bbox(masks["gline"], 700, 1300, 920, 1006)
if ga:
    out["green_arrows_band"] = dict(render=ga[:4], n=ga[4],
                                    target_y=[round(px(444.2), 1), round(px(483.1), 1)])
# connector lines band (inside box, between rows)
cl = bbox(masks["conn"], 350, 1750, 760, 860)
if cl:
    out["conn_band"] = dict(render=cl[:4], n=cl[4],
                            target_y=[round(px(351.5), 1), round(px(428.9), 1)])

print(json.dumps(out, indent=1))
