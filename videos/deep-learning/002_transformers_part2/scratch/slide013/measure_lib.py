#!/usr/bin/env python3
"""Precise region measurements for slide_013.jpg. Each function prints row/col
projections + bboxes for one shape group (frame px coords)."""
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_013.jpg').convert('RGB')
W, H = im.size
px = im.load()

def runs(vals, minlen=1):
    """Return list of (start,end) runs of True."""
    out = []
    s = None
    for i, v in enumerate(vals):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= minlen:
                out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(vals) - 1))
    return out

def colproj(x0, x1, y0, y1, fn):
    return [any(fn(*px[x, y]) for y in range(y0, y1)) for x in range(x0, x1)]

def rowproj(x0, x1, y0, y1, fn):
    return [any(fn(*px[x, y]) for x in range(x0, x1)) for y in range(y0, y1)]

def bbox(x0, x1, y0, y1, fn):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if fn(*px[x, y]):
                xs.append(x)
                ys.append(y)
    if not xs:
        return None
    return (min(xs), max(xs), min(ys), max(ys), len(xs))

def show(name, bb):
    if bb is None:
        print(name, 'EMPTY')
    else:
        print('%s bbox x %d..%d  y %d..%d  n=%d' % (name, bb[0], bb[1], bb[2], bb[3], bb[4]))

# color fns
def peach(r, g, b): return 243 <= r <= 252 and 220 <= g <= 232 and 198 <= b <= 212
def mint(r, g, b): return 110 <= r <= 170 and g >= 228 and 130 <= b <= 195
def bluegray(r, g, b): return 165 <= r <= 200 and 182 <= g <= 208 and 193 <= b <= 218
def dpgray(r, g, b): return 205 <= r <= 232 and 192 <= g <= 215 and 172 <= b <= 198
def softpink(r, g, b): return 240 <= r <= 255 and 210 <= g <= 232 and 240 <= b <= 255
def sigma_cyan(r, g, b): return 225 <= r <= 242 and 246 <= g <= 255 and 244 <= b <= 255
def yellowbox(r, g, b): return 240 <= r <= 255 and 238 <= g <= 255 and 85 <= b <= 135
def lightgreen_cell(r, g, b): return 150 <= r <= 190 and 200 <= g <= 225 and 130 <= b <= 165
def white(r, g, b): return r >= 246 and g >= 246 and b >= 246
def red_ink(r, g, b): return 130 <= r <= 215 and g <= 70 and b <= 70 and (r - g) > 75
def dark_red(r, g, b): return 80 <= r <= 135 and g <= 55 and 15 <= b <= 75
def black_ink(r, g, b): return r <= 80 and g <= 80 and b <= 80
def navy(r, g, b): return r <= 75 and g <= 75 and b >= 95
def blue_mid(r, g, b): return r <= 90 and 80 <= g <= 150 and b >= 160
def green_txt(r, g, b): return r <= 110 and 120 <= g <= 200 and b <= 120
def dkgreen_border(r, g, b): return 55 <= r <= 115 and 100 <= g <= 155 and 55 <= b <= 110
def pill_fill(r, g, b): return r >= 248 and g >= 246 and 195 <= b <= 240
def salmon(r, g, b): return 245 <= r <= 255 and 110 <= g <= 160 and 110 <= b <= 160
def lavender_cell(r, g, b): return 185 <= r <= 215 and 150 <= g <= 180 and 210 <= b <= 235
def bright_green_arrow(r, g, b): return 40 <= r <= 110 and 150 <= g <= 210 and 50 <= b <= 115
