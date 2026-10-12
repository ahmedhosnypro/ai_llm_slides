#!/usr/bin/env python3
"""Targeted PIL measurements of the 002:37 delta elements, in FRAME px of
unique_slides/slide_037.jpg (slide_pt = (fx-17.101)/0.962329, (fy+0.224)/0.96053).
Measures: red disc, dashed rounded box, pin (+text rotation), PE icons (clock?),
funnel lines, yellow band, encoder interior fills, decoder PE icons."""
from PIL import Image
from collections import Counter
import json, math

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg").convert("RGB")
px = img.load()
W, H = img.size
AX, SX = 17.101, 0.962329
BY, SY = -0.224, 0.96053
def S(fx, fy): return (round((fx - AX) / SX, 1), round((fy - BY) / SY, 1))
def Sbox(b): return [S(b[0], b[1])[0], S(b[0], b[1])[1], S(b[2], b[3])[0], S(b[2], b[3])[1]]
out = {}

def is_red(p):    return p[0] > 120 and (p[0] - p[1]) > 60 and (p[0] - p[2]) > 60
def is_strong_red(p): return p[0] > 150 and (p[0] - p[1]) > 90 and (p[0] - p[2]) > 90
def is_yellow(p): return p[0] > 210 and p[1] > 200 and p[2] < 140
def is_white(p):  return p[0] > 235 and p[1] > 235 and p[2] > 230
def is_dark(p):   return p[0] < 90 and p[1] < 90 and p[2] < 90

def blob(x0, y0, x1, y1, pred, min_px=30):
    """Connected components of pred in window; return list of (bbox, n)."""
    seen = set(); comps = []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x, y) in seen or not pred(px[x, y]):
                continue
            stack = [(x, y)]; seen.add((x, y))
            bx0 = bx1 = x; by0 = by1 = y; n = 0
            while stack:
                cx, cy = stack.pop(); n += 1
                bx0 = min(bx0, cx); bx1 = max(bx1, cx); by0 = min(by0, cy); by1 = max(by1, cy)
                for nx, ny in ((cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1),(cx+1,cy+1),(cx-1,cy-1),(cx+1,cy-1),(cx-1,cy+1)):
                    if x0 <= nx < x1 and y0 <= ny < y1 and (nx, ny) not in seen and pred(px[nx, ny]):
                        seen.add((nx, ny)); stack.append((nx, ny))
            if n >= min_px:
                comps.append(([bx0, by0, bx1, by1], n))
    comps.sort(key=lambda c: -c[1])
    return comps

# 1. red disc: strong red blob in the encoder stack zone
out["disc_blobs"] = [[b, n, Sbox(b)] for b, n in blob(630, 320, 730, 380, is_strong_red, 40)]

# 2. dashed rounded box: all red-ish px in the encoder zone EXCLUDING the disc bbox
disc = None
if out["disc_blobs"]:
    disc = max(out["disc_blobs"], key=lambda t: t[1])[0]
red_zone = []
dx0, dy0, dx1, dy1 = disc if disc else (0, 0, 0, 0)
for y in range(255, 440):
    for x in range(610, 745):
        if disc and dx0 - 3 <= x <= dx1 + 3 and dy0 - 3 <= y <= dy1 + 3:
            continue
        if is_red(px[x, y]):
            red_zone.append((x, y))
xs = [p[0] for p in red_zone]; ys = [p[1] for p in red_zone]
out["dashed_box_zone"] = {
    "n": len(red_zone),
    "bbox_frame": [min(xs), min(ys), max(xs), max(ys)] if red_zone else None,
    "bbox_slide": Sbox([min(xs), min(ys), max(xs), max(ys)]) if red_zone else None,
}
# column/row histograms to see the ring shape
colh = Counter(p[0] for p in red_zone); rowh = Counter(p[1] for p in red_zone)
out["dashed_box_cols"] = sorted(colh.items())
out["dashed_box_rows"] = sorted(rowh.items())

# 3. pin: red blob around (590-670, 185-300); white text inside it
pin_blobs = blob(575, 175, 685, 305, is_red, 60)
out["pin_blobs"] = [[b, n, Sbox(b)] for b, n in pin_blobs[:3]]
if pin_blobs:
    pb = max(pin_blobs, key=lambda t: t[1])[0]
    # white text pixels inside pin bbox
    wxs = []; wys = []
    for y in range(pb[1], pb[3]):
        for x in range(pb[0], pb[2]):
            if is_white(px[x, y]):
                # white inside the red blob (surrounded by red-ish neighborhood)
                nb_red = sum(1 for nx in range(max(pb[0],x-4), min(pb[2],x+4)) for ny in range(max(pb[1],y-4), min(pb[3],y+4)) if is_red(px[nx, ny]))
                if nb_red > 20:
                    wxs.append(x); wys.append(y)
    if wxs:
        wb = [min(wxs), min(wys), max(wxs), max(wys)]
        out["pin_text_bbox_frame"] = wb
        out["pin_text_bbox_slide"] = Sbox(wb)
        # rotation: per-row x centroid progression of white text ink
        rows = {}
        for x, y in zip(wxs, wys):
            rows.setdefault(y, []).append(x)
        cents = sorted((y, sum(v) / len(v)) for y, v in rows.items() if len(v) >= 2)
        out["pin_text_centroids"] = [[y, round(c, 1)] for y, c in cents[::4]]

# 4. PE nodes: dark outline circles (clock?) inside the PE node boxes
# encoder PE node frame ~(642-718, 430-468); decoder PE node frame ~(765-835, 425-465)
def dark_circles(x0, y0, x1, y1):
    comps = blob(x0, y0, x1, y1, is_dark, 12)
    return [[b, n, Sbox(b)] for b, n in comps[:8]]
out["enc_pe_dark"] = dark_circles(630, 425, 730, 475)
out["dec_pe_dark"] = dark_circles(755, 420, 850, 470)
# also non-dark outline (parent's circles are colored outlines)
def anyink(p): return p[0] < 160 or p[1] < 160 or p[2] < 160
out["enc_pe_ink"] = [[b, n, Sbox(b)] for b, n in blob(630, 425, 730, 475, anyink, 25)[:8]]
out["dec_pe_ink"] = [[b, n, Sbox(b)] for b, n in blob(755, 420, 850, 470, anyink, 25)[:8]]

# 5. yellow band presence
yel = [(x, y) for y in range(240, 350) for x in range(650, 800) if is_yellow(px[x, y])]
if yel:
    yxs = [p[0] for p in yel]; yys = [p[1] for p in yel]
    out["yellow_band"] = {"n": len(yel), "bbox_frame": [min(yxs), min(yys), max(yxs), max(yys)], "bbox_slide": Sbox([min(yxs), min(yys), max(yxs), max(yys)])}
else:
    out["yellow_band"] = {"n": 0}

# 6. encoder interior fills (tight windows avoiding text/dashes)
def mode_win(x0, y0, x1, y1, pred=None):
    c = Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            p = px[x, y]
            if pred is None or pred(p):
                c[p] += 1
    return [[list(k), v] for k, v in c.most_common(3)]
out["fill_an_top"]  = mode_win(655, 288, 700, 296)   # slide y~279-288
out["fill_ff"]      = mode_win(655, 305, 700, 325)   # slide y~300-322
out["fill_an_bot"]  = mode_win(655, 358, 700, 368)   # slide y~346-357
out["fill_mha"]     = mode_win(655, 380, 700, 395)   # slide y~366-381
out["fill_container_left"] = mode_win(618, 300, 626, 400)

# 7. funnel lines: red px in mid band excluding pin/box
fun = []
for y in range(140, 465):
    for x in range(186, 655):
        if is_red(px[x, y]):
            fun.append((x, y))
out["funnel_n"] = len(fun)
# cluster: split into connected-ish strokes by proximity grid
fun_set = set(fun)
visited = set(); strokes = []
for p in fun:
    if p in visited: continue
    stack = [p]; visited.add(p); comp = []
    while stack:
        cx, cy = stack.pop(); comp.append((cx, cy))
        for ddx in (-3, -2, -1, 0, 1, 2, 3):
            for ddy in (-3, -2, -1, 0, 1, 2, 3):
                q = (cx + ddx, cy + ddy)
                if q in fun_set and q not in visited:
                    visited.add(q); stack.append(q)
    if len(comp) >= 25:
        xs = [c[0] for c in comp]; ys = [c[1] for c in comp]
        strokes.append({"n": len(comp), "bbox_frame": [min(xs), min(ys), max(xs), max(ys)], "bbox_slide": Sbox([min(xs), min(ys), max(xs), max(ys)])})
strokes.sort(key=lambda s: -s["n"])
out["funnel_strokes"] = strokes[:14]

print(json.dumps(out, indent=1, default=str))
