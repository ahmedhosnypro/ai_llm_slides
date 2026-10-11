#!/usr/bin/env python3
"""Phase 6: diagnostic — exact color histograms per band + full row/col profiles."""
from PIL import Image
from collections import Counter
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}


def hist(x0, x1, y0, y1, topn=14):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c[px[x, y]] += 1
    return [[f"#{r:02X}{g:02X}{b:02X}", n] for (r, g, b), n in c.most_common(topn)]


# band histograms (frame coords)
out["hist_title_row1"] = hist(60, 910, 55, 150)
out["hist_row2"] = hist(60, 910, 125, 210)
out["hist_row3_delta"] = hist(60, 910, 210, 270)
out["hist_row4"] = hist(60, 910, 330, 425)
out["hist_labelcol"] = hist(35, 170, 330, 430)   # where 'Final Embedding' should be
out["hist_brace"] = hist(60, 910, 425, 460)


def rowprof(x0, x1, y0, y1, pred):
    prof = []
    for y in range(y0, y1):
        n = sum(1 for x in range(x0, x1) if pred(px[x, y]))
        if n > 0:
            prof.append([y, n])
    return prof


def is_red(p):
    r, g, b = p
    return r > 130 and (r - g) > 45 and (r - b) > 45


def is_green(p):
    r, g, b = p
    return g > 100 and (g - r) > 40 and (g - b) > 20


def is_blue(p):
    r, g, b = p
    return b > 120 and (b - r) > 40 and (b - g) > 40


out["red_rows_55_165"] = rowprof(60, 910, 55, 165, is_red)
out["green_rows_115_215"] = rowprof(60, 910, 115, 215, is_green)
out["blue_rows_205_275"] = rowprof(60, 910, 205, 275, is_blue)
out["red_rows_320_465"] = rowprof(60, 910, 320, 465, is_red)
out["red_rows_labelcol"] = rowprof(30, 170, 60, 510, is_red)
out["red_rows_left_all"] = rowprof(30, 175, 60, 510, lambda p: True and is_red(p))[:0]  # skip

# where IS red in the left column? scan x 30..170 rows 60..510 per-row (any red)
out["red_in_x30_170"] = rowprof(30, 170, 60, 510, is_red)

# scanline samples: vertical line x=480 from y=50..160 and y=320..470
out["vline_480"] = [[y, f"#{r:02X}{g:02X}{b:02X}"] for y, (r, g, b) in
                    [(y, px[480, y]) for y in range(50, 165, 3)]]
out["vline_480_low"] = [[y, f"#{r:02X}{g:02X}{b:02X}"] for y, (r, g, b) in
                        [(y, px[480, y]) for y in range(320, 470, 3)]]
# horizontal line y=110 (row1) x 55..915 step 5
out["hline_110"] = [[x, f"#{r:02X}{g:02X}{b:02X}"] for x, (r, g, b) in
                    [(x, px[x, 110]) for x in range(55, 915, 10)]]

print(json.dumps(out, indent=1))
