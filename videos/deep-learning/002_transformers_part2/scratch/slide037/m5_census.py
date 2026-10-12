#!/usr/bin/env python3
"""Per-region color census: base_960.png vs slide037_slide_space.png.
For each named rect: top colors + how many px are 'same' (dist<=30)."""
from PIL import Image
from collections import Counter
import json

base = Image.open("base_960.png").convert("RGB")
mine = Image.open("slide037_slide_space.png").convert("RGB")
pb, pm = base.load(), mine.load()

REGIONS = {
  "title_band":        (90, 50, 860, 95),
  "legend1_area":      (141, 102, 342, 130),
  "legend2_area":      (311, 143, 514, 171),
  "legend3_area":      (264, 181, 465, 209),
  "badge":             (868, 50, 916, 95),
  "left_inset_frame":  (52, 260, 200, 500),
  "left_header":       (54, 225, 195, 268),
  "left_circles":      (70, 460, 195, 500),
  "left_boxes":        (70, 280, 190, 460),
  "center_inset_frame":(295, 240, 515, 520),
  "center_header":     (294, 205, 508, 240),
  "center_linear_row": (300, 395, 470, 425),
  "center_sdpa":       (300, 340, 480, 400),
  "center_circles":    (310, 480, 470, 515),
  "right_enc_panel":   (577, 108, 738, 300),
  "right_dec_panel":   (740, 108, 894, 300),
  "enc_container":     (630, 270, 726, 410),
  "enc_mha_area":      (630, 350, 730, 410),
  "enc_addn_ff":       (630, 268, 726, 345),
  "enc_pe_embed":      (590, 410, 740, 495),
  "dec_container":     (744, 200, 842, 310),
  "dec_low":           (744, 320, 842, 410),
  "dec_top":           (740, 108, 845, 200),
  "dec_embed_pe":      (740, 405, 895, 495),
  "nx_area":           (590, 320, 630, 360),
  "dec_nx_area":       (840, 295, 875, 330),
  "funnel_corridor":   (200, 240, 575, 440),
  "pin_area":          (590, 150, 740, 270),
}

def census(p, x0, y0, x1, y1):
    c = Counter()
    for y in range(y0, min(y1,540)):
        for x in range(x0, min(x1,960)):
            c[p[x,y]] += 1
    return c.most_common(6)

out = {}
for name, (x0,y0,x1,y1) in REGIONS.items():
    cb = census(pb, x0,y0,x1,y1)
    cm = census(pm, x0,y0,x1,y1)
    # same-pixel count
    same = 0; tot = 0
    for y in range(y0, min(y1,540)):
        for x in range(x0, min(x1,960)):
            a, b = pb[x,y], pm[x,y]
            tot += 1
            if abs(a[0]-b[0])+abs(a[1]-b[1])+abs(a[2]-b[2]) <= 90:
                same += 1
    out[name] = {
        "same_frac": round(same/tot, 3) if tot else 0,
        "base_top": [[list(c), n] for c, n in cb],
        "mine_top": [[list(c), n] for c, n in cm],
    }
print(json.dumps(out, indent=1))
