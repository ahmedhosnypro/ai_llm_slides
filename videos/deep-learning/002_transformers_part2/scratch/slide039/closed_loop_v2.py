#!/usr/bin/env python3
"""CLOSED-LOOP v2 (attempt-1 render): per-line ink deltas with border-safe windows,
box borders, underlines, dots, fills. render px = slide pt * 2.0844 (2001px/960pt)."""
from PIL import Image
import json

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide039/slide-1.png"
img = Image.open(REN).convert("RGB")
W, H = img.size
px = img.load()
SC = W / 960.0

def inkp(p): return sum(p) < 640
def redp(p):
    r, g, b = p
    return r > 110 and r - g > 40 and r - b > 40
def bluep(p):
    r, g, b = p
    return b > 90 and b - r > 40 and b - g > 30
def darkp(p): return sum(p) < 300

def bbox(x0, x1, y0, y1, pred):
    pts = [(x, y) for y in range(int(y0), int(y1) + 1) for x in range(int(x0), int(x1) + 1) if pred(px[x, y])]
    if not pts: return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]

def S2R(a, b): return a * SC, b * SC

# id: (pred, window slide-pt (x0,x1,y0,y1), target [x0,y0,x1,y1])
T = {
    "title":     (redp, (300, 700, 50, 96),    [338.5, 60.7, 568.4, 87.9]),
    "quoteL1":   (bluep, (56, 893, 106, 137),  [64.9, 115.1, 878.4, 135.0]),
    "covshift":  (redp, (620, 880, 138, 159),  [697.4, 140.2, 858.7, 158.0]),
    "f1l1":      (redp, (107, 279, 184, 208),  [114.8, 190.5, 270.9, 205.1]),
    "f1l2":      (darkp, (107, 279, 216, 240), [121.1, 224.0, 268.8, 238.6]),
    "f2l1":      (redp, (341, 568, 186, 206),  [347.9, 193.6, 557.0, 207.2]),
    "f2l2":      (redp, (341, 568, 213, 236),  [385.3, 220.8, 523.7, 234.4]),
    "f3l1":      (darkp, (628, 853, 186, 206), [662.0, 193.6, 817.0, 207.2]),
    "f3l2":      (redp, (624, 853, 213, 236),  [630.8, 220.8, 848.3, 234.4]),
    "conclusion":(redp, (62, 240, 259, 281),   [73.2, 264.8, 166.8, 277.3]),
    "stmt1":     (bluep, (142, 700, 283, 307), [152.3, 287.8, 643.3, 305.6]),
    "idea":      (redp, (62, 490, 323, 344),   [73.2, 327.6, 439.4, 341.2]),
    "stmt2":     (bluep, (143, 760, 347, 371), [153.3, 351.6, 720.3, 369.4]),
    "lc_norm":   (redp, (62, 208, 388, 410),   [73.2, 392.4, 202.2, 406.0]),
    "lc_trans":  (darkp, (208, 468, 388, 412), [213.7, 392.4, 460.2, 410.2]),
    "lc_zero":   (bluep, (440, 762, 388, 410), [466.5, 393.5, 718.2, 406.0]),
    "sumhead":   (redp, (62, 420, 435, 459),   [67.0, 439.5, 373.9, 456.3]),
    "b1":        (bluep, (95, 490, 461, 486),  [84.7, 464.6, 424.8, 482.4]),
    "b2":        (bluep, (95, 762, 483, 506),  [83.6, 484.5, 706.8, 503.4]),
}
res = {}
bad = []
print(f"render {W}x{H}, scale {SC:.4f}; tol 4px")
print(f"{'id':<11}{'dx0':>7}{'dy0':>7}{'dx1':>7}{'dy1':>7}")
for id_, (pred, win, tgt) in T.items():
    wx0, wx1 = S2R(win[0], win[1]); wy0, wy1 = S2R(win[2], win[3])
    b = bbox(wx0, wx1, wy0, wy1, pred)
    if b is None:
        print(f"{id_:<11}   NO INK <<<"); res[id_] = None; bad.append(id_); continue
    tx0, ty0 = S2R(tgt[0], tgt[1]); tx1, ty1 = S2R(tgt[2], tgt[3])
    d = [b[0] - tx0, b[1] - ty0, b[2] - tx1, b[3] - ty1]
    res[id_] = {"bbox": b, "d": [round(v, 1) for v in d]}
    flag = ""
    if max(abs(v) for v in d) > 4: flag = " <<<"; bad.append(id_)
    print(f"{id_:<11}{d[0]:>7.1f}{d[1]:>7.1f}{d[2]:>7.1f}{d[3]:>7.1f}{flag}")

# ---- box borders (render row/col scans near targets)
def redrow_frac(y, x0, x1):
    return sum(1 for x in range(int(x0), int(x1)) if redp(px[x, int(y)])) / (int(x1) - int(x0))
def redcol_frac(x, y0, y1):
    return sum(1 for y in range(int(y0), int(y1)) if redp(px[int(x), y])) / (int(y1) - int(y0))
def bluerow_frac(y, x0, x1):
    return sum(1 for x in range(int(x0), int(x1)) if bluep(px[x, int(y)])) / (int(x1) - int(x0))
def bluecol_frac(x, y0, y1):
    return sum(1 for y in range(int(y0), int(y1)) if bluep(px[int(x), y])) / (int(y1) - int(y0))

def find_edge(fracfn, target_px, lo=-8, hi=8, axis="row"):
    for d in range(lo, hi + 1):
        v = target_px + d
        if fracfn(v) > 0.5: return d
    return None

edges = {}
# quote box: top 100.5, bottom 160.1, left 57.6, right 896.1
edges["quote_top"] = find_edge(lambda y: redrow_frac(y, 200, 1700), 100.5 * SC)
edges["quote_bot"] = find_edge(lambda y: redrow_frac(y, 200, 1700), 160.1 * SC)
edges["quote_left"] = find_edge(lambda x: redcol_frac(x, 230, 320), 57.6 * SC, axis="col")
edges["quote_right"] = find_edge(lambda x: redcol_frac(x, 230, 320), 896.1 * SC, axis="col")
# container: top 169.5 bottom 415.5 left 55.5 right 894.0
edges["cont_top"] = find_edge(lambda y: redrow_frac(y, 200, 1700), 169.5 * SC)
edges["cont_bot"] = find_edge(lambda y: redrow_frac(y, 200, 1700), 415.5 * SC)
edges["cont_left"] = find_edge(lambda x: redcol_frac(x, 400, 700), 55.5 * SC, axis="col")
edges["cont_right"] = find_edge(lambda x: redcol_frac(x, 400, 700), 894.0 * SC, axis="col")
# summary: top 429.1 bottom 526.4 (blue)
edges["sum_top"] = find_edge(lambda y: bluerow_frac(y, 200, 1700), 429.1 * SC)
edges["sum_bot"] = find_edge(lambda y: bluerow_frac(y, 200, 1700), 526.4 * SC)
# flow boxes: box1 L 101.3 R 284.9; box2 L 335.4 R 574.6; box3 L 622.5 R 855.5; top 179.0 bot 256.4
edges["fb1_left"] = find_edge(lambda x: redcol_frac(x, 400, 500), 101.3 * SC, axis="col")
edges["fb1_right"] = find_edge(lambda x: redcol_frac(x, 400, 500), 284.9 * SC, axis="col")
edges["fb2_left"] = find_edge(lambda x: redcol_frac(x, 400, 500), 335.4 * SC, axis="col")
edges["fb3_left"] = find_edge(lambda x: redcol_frac(x, 400, 500), 622.5 * SC, axis="col")
edges["fb3_right"] = find_edge(lambda x: redcol_frac(x, 400, 500), 855.5 * SC, axis="col")
edges["fb_top"] = find_edge(lambda y: redrow_frac(y, 250, 550), 179.0 * SC)
edges["fb_bot"] = find_edge(lambda y: redrow_frac(y, 250, 550), 256.4 * SC)
print("\nbox edges (d px):", edges)

# ---- underlines (blue horizontal runs) in render vs targets
def underline_check(id_, y_lo, y_hi, x0, x1, tx0, tx1, ty):
    found = None
    for y in range(int(y_lo), int(y_hi)):
        n = sum(1 for x in range(int(x0), int(x1)) if bluep(px[x, y]))
        if n > (tx1 - tx0) * 0.7:
            xs = [x for x in range(int(x0), int(x1)) if bluep(px[x, y])]
            found = (min(xs), max(xs), y)
            break
    t = (tx0 * SC, tx1 * SC, ty * SC)
    if found:
        print(f"underline {id_}: found x {found[0]}..{found[1]} y {found[2]} | target x {t[0]:.0f}..{t[1]:.0f} y {t[2]:.0f} | d [{found[0]-t[0]:.0f},{found[2]-t[2]:.0f},{found[1]-t[1]:.0f}]")
    else:
        print(f"underline {id_}: NOT FOUND <<< | target x {t[0]:.0f}..{t[1]:.0f} y {t[2]:.0f}")

underline_check("stmt2_covshift", 355 * SC, 372 * SC, 150 * SC, 400 * SC, 202.3, 329.1, 367.3)
underline_check("b1_stable", 470 * SC, 484 * SC, 150 * SC, 480 * SC, 212.6, 426.0, 478.4)
underline_check("b2_accel", 495 * SC, 508 * SC, 95 * SC, 350 * SC, 83.6, 260.2, 500.2)

# ---- dots
d1 = bbox(58 * SC, 80 * SC, 462 * SC, 480 * SC, darkp)
print("dot1 render bbox px:", d1, "target center px", round(67.5 * SC, 1), round(470.4 * SC, 1))

# ---- fills / colors sampled in render
samples = {
    "panel_gap": px[int(480 * SC), int(165 * SC)],
    "quote_fill": px[int(500 * SC), int(140 * SC)],
    "container_fill": px[int(500 * SC), int(280 * SC)],
    "summary_fill": px[int(780 * SC), int(445 * SC)],
    "flow_fill": px[int(200 * SC), int(200 * SC)],
    "title_core": px[int(450 * SC), int(74 * SC)],
    "quote_core": px[int(300 * SC), int(125 * SC)],
}
print("samples:", json.dumps({k: list(v) for k, v in samples.items()}))

json.dump({"lines": res, "edges": edges}, open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide039/closed_loop_v2.json", "w"), indent=1)
print("\nBAD:", bad)
