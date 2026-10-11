#!/usr/bin/env python3
"""CLOSED-LOOP v3b (slide 039): tight windows (v2-corrected), identical predicates
on RENDER and ORIGINAL FRAME, self-derived targets (m5/m6 cross-checked).
Fixes vs v2: b1/b2 x-windows start at 75 (v2 clipped at 95), lc_trans y-window
open to 417 (v2 clipped 'g' descender), covshift window excludes quote bottom
border, blackish predicate excludes red box borders, underline rows scanned only
below baseline. Usage: closed_loop_v3b.py <render.png> <tag>"""
from PIL import Image
import json, sys

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
REN = sys.argv[1] if len(sys.argv) > 1 else f"{BASE}/scratch/slide039/out1/slide-1.png"
TAG = sys.argv[2] if len(sys.argv) > 2 else "v3b"
ORIG = f"{BASE}/unique_slides/slide_039.jpg"

A, B = 0.96123, 18.63   # fx = A*sx + B
C = 0.95556             # fy = C*sy

rimg = Image.open(REN).convert("RGB"); W, H = rimg.size; SC = W / 960.0
oimg = Image.open(ORIG).convert("RGB")
rp, op = rimg.load(), oimg.load()

def redp(p): r, g, b = p; return r > 110 and r - g > 40 and r - b > 40
def bluep(p): r, g, b = p; return b > 90 and b - r > 40 and b - g > 30
def blackish(p):
    if redp(p) or bluep(p): return False
    return sum(p) < 300

def bbox(img_px, x0, x1, y0, y1, pred):
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if pred(img_px[x, y])]
    if not pts: return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]

# id: (pred, window slide-pt (x0,x1,y0,y1)) — tight, excludes borders/dots/neighbors/underlines-of-others
LINES = {
    "title":     (redp,     (285, 640, 50, 94)),
    "quoteL1":   (bluep,    (56, 890, 106, 137)),
    "covshift":  (redp,     (560, 890, 139, 158)),
    "f1l1":      (redp,     (106, 280, 183, 210)),
    "f1l2":      (blackish, (106, 280, 216, 245)),
    "f2l1":      (redp,     (340, 570, 186, 211)),
    "f2l2a":     (blackish, (340, 472, 213, 241)),   # "of each layer" — black (pixel-measured)
    "f2l2b":     (redp,     (472, 570, 213, 241)),   # "change" — red (pixel-measured)
    "f3l1":      (blackish, (627, 851, 186, 211)),
    "f3l2":      (redp,     (627, 851, 213, 241)),
    "conclusion":(redp,     (60, 250, 258, 283)),
    "stmt1":     (bluep,    (145, 700, 283, 310)),
    "idea":      (redp,     (60, 500, 320, 345)),
    "stmt2":     (bluep,    (145, 770, 347, 372)),
    "lc_norm":   (redp,     (60, 208, 386, 417)),
    "lc_trans":  (blackish, (208, 462, 386, 417)),
    "lc_zero":   (bluep,    (463, 780, 386, 412)),
    "sumhead":   (redp,     (60, 430, 434, 460)),
    "b1":        (bluep,    (75, 495, 461, 484.5)),
    "b2":        (bluep,    (75, 770, 484.5, 507)),
}

def measure():
    res = {}
    for id_, (pred, win) in LINES.items():
        wx0, wx1, wy0, wy1 = [v * SC for v in win]
        r = bbox(rp, wx0, wx1, wy0, wy1, pred)
        r = [v / SC for v in r] if r else None
        ox0, ox1, oy0, oy1 = A * win[0] + B, A * win[1] + B, C * win[2], C * win[3]
        o = bbox(op, ox0, ox1, oy0, oy1, pred)
        o = [(o[0] - B) / A, o[1] / C, (o[2] - B) / A, o[3] / C] if o else None
        res[id_] = (o, r)
    return res

print(f"render {W}x{H} (SC {SC:.4f}) | tol 4 px @150dpi (pt*{SC:.3f})")
print(f"{'id':<11}{'tw':>7}{'rw':>7}{'dw':>6} | {'dx0':>6}{'dy0':>6}{'dx1':>6}{'dy1':>6}  (d in px @150dpi)")
bad, out = [], {}
for id_, (o, r) in measure().items():
    if o is None or r is None:
        print(f"{id_:<11}  orig {'NO INK' if o is None else 'ok'} | rend {'NO INK' if r is None else 'ok'} <<<")
        bad.append(id_); out[id_] = {"orig": o, "rend": r}; continue
    tw, rw = o[2] - o[0], r[2] - r[0]
    dp = [(r[0] - o[0]) * SC, (r[1] - o[1]) * SC, (r[2] - o[2]) * SC, (r[3] - o[3]) * SC]
    flag = ""
    if max(abs(v) for v in dp) > 4: flag = " <<<"; bad.append(id_)
    print(f"{id_:<11}{tw:>7.1f}{rw:>7.1f}{rw-tw:>6.1f} | {dp[0]:>6.1f}{dp[1]:>6.1f}{dp[2]:>6.1f}{dp[3]:>6.1f}{flag}")
    out[id_] = {"orig": [round(v, 2) for v in o], "rend": [round(v, 2) for v in r],
                "w_pt": [round(tw, 2), round(rw, 2)], "d_px": [round(v, 1) for v in dp]}

# ---- underlines: rows strictly below baseline; informational (JPEG noise high)
UND = {
    "stmt2_cov": ((195, 340), 365.3),
    "b1_stable": ((205, 435), 478.4),
    "b2_accel":  ((78, 268), 499.9),
}
print("\nunderlines (informational):")
for id_, ((ux0, ux1), base_y) in UND.items():
    row = {}
    X0r, X1r = ux0 * SC, ux1 * SC
    xs_r = [(x / SC, py / SC) for py in range(int((base_y + 1) * SC), int((base_y + 6) * SC) + 1)
            for x in range(int(X0r), int(X1r) + 1) if bluep(rp[x, py])]
    X0o, X1o = A * ux0 + B, A * ux1 + B
    xs_o = [((x - B) / A, fy / C) for fy in range(int(C * (base_y + 1)), int(C * (base_y + 6)) + 1)
            for x in range(int(X0o), int(X1o) + 1) if bluep(op[x, fy])]
    for label, xs in (("orig", xs_o), ("rend", xs_r)):
        row[label] = ([round(min(p[0] for p in xs), 1), round(max(p[0] for p in xs), 1),
                       round(min(p[1] for p in xs), 1)] if xs else None)
    print(f"{id_:<11} orig {row['orig']} | rend {row['rend']}")
    out["und_" + id_] = row

# ---- dots
for i, (yc0, yc1) in enumerate(((460, 478), (483, 501)), 1):
    d = bbox(rp, 58 * SC, 80 * SC, yc0 * SC, yc1 * SC, bluep)
    if d: print(f"dot{i} rend slide-pt [{d[0]/SC:.1f},{d[1]/SC:.1f},{d[2]/SC:.1f},{d[3]/SC:.1f}]")

# ---- box edges (v2 logic, px-space scans)
def rowfrac(y, x0, x1, pred): return sum(1 for x in range(int(x0), int(x1)) if pred(rp[x, int(y)])) / (int(x1) - int(x0))
def colfrac(x, y0, y1, pred): return sum(1 for y in range(int(y0), int(y1)) if pred(rp[int(x), y])) / (int(y1) - int(y0))
def find_edge(fracfn, target_px, lo=-8, hi=8):
    for dd in range(lo, hi + 1):
        if fracfn(target_px + dd) > 0.5: return dd
    return None
edges = {}
edges["quote_top"] = find_edge(lambda y: rowfrac(y, 200, 1700, redp), 100.5 * SC)
edges["quote_bot"] = find_edge(lambda y: rowfrac(y, 200, 1700, redp), 160.1 * SC)
edges["cont_top"] = find_edge(lambda y: rowfrac(y, 200, 1700, redp), 169.5 * SC)
edges["cont_bot"] = find_edge(lambda y: rowfrac(y, 200, 1700, redp), 415.5 * SC)
edges["sum_top"] = find_edge(lambda y: rowfrac(y, 200, 1700, bluep), 429.1 * SC)
edges["sum_bot"] = find_edge(lambda y: rowfrac(y, 200, 1700, bluep), 526.4 * SC)
edges["fb1_left"] = find_edge(lambda x: colfrac(x, 400, 500, redp), 101.3 * SC)
edges["fb3_right"] = find_edge(lambda x: colfrac(x, 400, 500, redp), 855.5 * SC)
edges["fb_top"] = find_edge(lambda y: rowfrac(y, 250, 550, redp), 179.0 * SC)
edges["fb_bot"] = find_edge(lambda y: rowfrac(y, 250, 550, redp), 256.4 * SC)
print("box edges (d px):", edges)
samples = {"summary_fill": rp[int(780 * SC), int(445 * SC)], "flow_fill": rp[int(200 * SC), int(200 * SC)],
           "quote_fill": rp[int(500 * SC), int(140 * SC)], "container_fill": rp[int(500 * SC), int(280 * SC)]}
print("samples:", json.dumps({k: list(v) for k, v in samples.items()}))

print("\nBAD:", bad)
json.dump(out, open(f"{BASE}/scratch/slide039/closed_loop_{TAG}.json", "w"), indent=1)
