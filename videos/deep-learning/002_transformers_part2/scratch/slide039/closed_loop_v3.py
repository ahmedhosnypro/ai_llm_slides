#!/usr/bin/env python3
"""CLOSED-LOOP v3 (slide 039): measures the RENDER and the ORIGINAL FRAME with
IDENTICAL wide windows + predicates, maps both to slide-pt, and reports per-line
deltas. Targets are self-derived from the original (m5/m6 cross-checked), so
window-clip bugs from v2 are gone. Usage: closed_loop_v3.py <render.png> [tag]"""
from PIL import Image
import json, sys

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
REN = sys.argv[1] if len(sys.argv) > 1 else f"{BASE}/scratch/slide039/out1/slide-1.png"
TAG = sys.argv[2] if len(sys.argv) > 2 else "v3"
ORIG = f"{BASE}/unique_slides/slide_039.jpg"

# frame->slide transform (fitted from this frame's chrome landmarks, = slide_002's)
A, B = 0.96123, 18.63   # fx = A*sx + B
C = 0.95556             # fy = C*sy

rimg = Image.open(REN).convert("RGB"); W, H = rimg.size; SC = W / 960.0
oimg = Image.open(ORIG).convert("RGB"); OW, OH = oimg.size
rp, op = rimg.load(), oimg.load()

def redp(p): r, g, b = p; return r > 110 and r - g > 40 and r - b > 40
def bluep(p): r, g, b = p; return b > 90 and b - r > 40 and b - g > 30
def darkp(p): return sum(p) < 300

def bbox(img_px, x0, x1, y0, y1, pred):
    x0, x1, y0, y1 = int(x0), int(x1), int(y0), int(y1)
    pts = [(x, y) for y in range(y0, y1 + 1) for x in range(x0, x1 + 1) if pred(img_px[x, y])]
    if not pts: return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]

# id: (pred, window slide-pt (x0,x1,y0,y1)) — wide, clear of borders/dots/neighbors
LINES = {
    "title":     (redp,  (280, 700, 48, 96)),
    "quoteL1":   (bluep, (50, 900, 104, 138)),
    "covshift":  (redp,  (560, 892, 138, 160)),
    "f1l1":      (redp,  (100, 296, 182, 212)),
    "f1l2":      (darkp, (100, 296, 216, 248)),
    "f2l1":      (redp,  (330, 578, 184, 212)),
    "f2l2":      (redp,  (330, 578, 212, 244)),
    "f3l1":      (darkp, (616, 858, 184, 212)),
    "f3l2":      (redp,  (616, 858, 212, 244)),
    "conclusion":(redp,  (55, 260, 256, 285)),
    "stmt1":     (bluep, (140, 720, 280, 312)),
    "idea":      (redp,  (55, 520, 318, 348)),
    "stmt2":     (bluep, (140, 780, 344, 376)),
    "lc_norm":   (redp,  (55, 462, 384, 418)),
    "lc_trans":  (darkp, (55, 462, 384, 418)),
    "lc_zero":   (bluep, (462, 780, 384, 418)),
    "sumhead":   (redp,  (55, 440, 432, 462)),
    "b1":        (bluep, (74, 500, 458, 488)),
    "b2":        (bluep, (74, 780, 482, 510)),
}

def s2r_win(win):  # slide-pt window -> render px
    return [win[0] * SC, win[1] * SC, win[2] * SC, win[3] * SC]
def s2o_win(win):  # slide-pt window -> original frame px
    return [A * win[0] + B, A * win[1] + B, C * win[2], C * win[3]]
def o_bbox_to_slide(b):  # frame px bbox -> slide pt
    return [(b[0] - B) / A, b[1] / C, (b[2] - B) / A, b[3] / C]

print(f"render {W}x{H} (SC {SC:.4f}) | original {OW}x{OH} | tol 4 px @150dpi")
hdr = f"{'id':<11}{'tw':>7}{'rw':>7}{'dw':>6} | {'tx0':>7}{'rx0':>7}{'dx0':>6} | {'ty0':>7}{'ry0':>7}{'dy0':>6} | {'tx1':>7}{'rx1':>7}{'dx1':>6} | {'ty1':>7}{'ry1':>7}{'dy1':>6}"
print(hdr)
bad, out = [], {}
def measure():
    res = {}
    for id_, (pred, win) in LINES.items():
        wx0, wx1, wy0, wy1 = s2r_win(win)
        r = bbox(rp, wx0, wx1, wy0, wy1, pred)
        r = [v / SC for v in r] if r else None            # render px -> slide pt
        ox0, ox1, oy0, oy1 = s2o_win(win)
        o = bbox(op, ox0, ox1, oy0, oy1, pred)
        o = o_bbox_to_slide(o) if o else None             # frame px -> slide pt
        res[id_] = (o, r)
    return res

res = measure()
for id_, (o, r) in res.items():
    if o is None or r is None:
        print(f"{id_:<11}  ORIGINAL {'NO INK' if o is None else 'ok'} | RENDER {'NO INK' if r is None else 'ok'}  <<<")
        bad.append(id_); out[id_] = {"orig": o, "rend": r}; continue
    tw, rw = o[2] - o[0], r[2] - r[0]
    d = [r[0] - o[0], r[1] - o[1], r[2] - o[2], r[3] - o[3]]   # slide pt
    dp = [v * SC for v in d]                                    # render px @150dpi
    flag = ""
    if max(abs(v) for v in dp) > 4: flag = " <<<"; bad.append(id_)
    print(f"{id_:<11}{tw:>7.1f}{rw:>7.1f}{rw-tw:>6.1f} | {o[0]:>7.1f}{r[0]:>7.1f}{dp[0]:>6.1f} | "
          f"{o[1]:>7.1f}{r[1]:>7.1f}{dp[1]:>6.1f} | {o[2]:>7.1f}{r[2]:>7.1f}{dp[2]:>6.1f} | "
          f"{o[3]:>7.1f}{r[3]:>7.1f}{dp[3]:>6.1f}{flag}")
    out[id_] = {"orig": [round(v, 2) for v in o], "rend": [round(v, 2) for v in r],
                "d_pt": [round(v, 2) for v in d], "d_px": [round(v, 1) for v in dp]}

# ---- underlines: scan rows BELOW baseline only (blue), in render + original
UND = {  # id: (x-window slide-pt for run, baseline slide-pt, target-x from frame banked)
    "stmt2_cov": ((195, 340), 365.3, (202.3, 329.1)),
    "b1_stable": ((205, 435), 478.4, (212.6, 426.0)),
    "b2_accel":  ((78, 270), 499.9, (83.6, 260.5)),
}
print("\nunderlines (rows searched: baseline+1 .. baseline+6 pt):")
for id_, ((ux0, ux1), base_y, (tx0, tx1)) in UND.items():
    row = {}
    for label, img_px, conv in (("orig", op, "o"), ("rend", rp, "r")):
        found = None
        if conv == "o":
            X0, X1 = A * ux0 + B, A * ux1 + B
            for fy in range(int(C * (base_y + 1)), int(C * (base_y + 6)) + 1):
                xs = [x for x in range(int(X0), int(X1) + 1) if bluep(img_px[x, fy])]
                if len(xs) > 0.6 * (A * (tx1 - tx0)):
                    found = [(min(xs) - B) / A, (max(xs) - B) / A, fy / C]; break
        else:
            X0, X1 = ux0 * SC, ux1 * SC
            for py in range(int((base_y + 1) * SC), int((base_y + 6) * SC) + 1):
                xs = [x for x in range(int(X0), int(X1) + 1) if bluep(img_px[x, int(py)])]
                if len(xs) > 0.6 * ((tx1 - tx0) * SC):
                    found = [min(xs) / SC, max(xs) / SC, py / SC]; break
        row[label] = found
    o, r = row["orig"], row["rend"]
    if o and r:
        d = [r[0] - o[0], r[1] - o[1], (r[2] - o[2]) * SC]
        flag = " <<<" if max(abs(d[0]), abs(d[1])) * SC > 4 or abs(d[2]) > 4 else ""
        print(f"{id_:<11} orig x {o[0]:.1f}..{o[1]:.1f} y {o[2]:.1f} | rend x {r[0]:.1f}..{r[1]:.1f} y {r[2]:.1f} "
              f"| d(dx0,dx1,dy)px {d[0]*SC:.0f},{d[1]*SC:.0f},{d[2]:.0f}{flag}")
    else:
        print(f"{id_:<11} orig {'FOUND' if o else 'NONE'} | rend {'FOUND' if r else 'NONE'} <<<")
    out["und_" + id_] = row

# ---- dots + box edges + fills (render only, targets from frame banked)
d1 = bbox(rp, 58 * SC, 80 * SC, 460 * SC, 480 * SC, bluep)
d2 = bbox(rp, 58 * SC, 80 * SC, 483 * SC, 503 * SC, bluep)
if d1: print(f"\ndot1 rend bbox slide-pt [{d1[0]/SC:.1f},{d1[1]/SC:.1f},{d1[2]/SC:.1f},{d1[3]/SC:.1f}] target [64.9,467.7,70.1,473.4]")
if d2: print(f"dot2 rend bbox slide-pt [{d2[0]/SC:.1f},{d2[1]/SC:.1f},{d2[2]/SC:.1f},{d2[3]/SC:.1f}] target [64.9,490.7,70.1,496.3]")

def rowfrac(img_px, y, x0, x1, pred): return sum(1 for x in range(int(x0), int(x1)) if pred(img_px[x, int(y)])) / (int(x1) - int(x0))
def colfrac(img_px, x, y0, y1, pred): return sum(1 for y in range(int(y0), int(y1)) if pred(img_px[int(x), y])) / (int(y1) - int(y0))
def find_edge(img_px, fracfn, target_px, lo=-8, hi=8):
    for dd in range(lo, hi + 1):
        if fracfn(target_px + dd) > 0.5: return dd
    return None
edges = {}
edges["quote_top"] = find_edge(rp, lambda y: rowfrac(rp, y, 200 * SC, 1700 * SC, redp), 100.5 * SC)
edges["quote_bot"] = find_edge(rp, lambda y: rowfrac(rp, y, 200 * SC, 1700 * SC, redp), 160.1 * SC)
edges["cont_top"] = find_edge(rp, lambda y: rowfrac(rp, y, 200 * SC, 1700 * SC, redp), 169.5 * SC)
edges["cont_bot"] = find_edge(rp, lambda y: rowfrac(rp, y, 200 * SC, 1700 * SC, redp), 415.5 * SC)
edges["sum_top"] = find_edge(rp, lambda y: rowfrac(rp, y, 200 * SC, 1700 * SC, bluep), 429.1 * SC)
edges["sum_bot"] = find_edge(rp, lambda y: rowfrac(rp, y, 200 * SC, 1700 * SC, bluep), 526.4 * SC)
edges["fb1_left"] = find_edge(rp, lambda x: colfrac(rp, x, 400 * SC, 500 * SC, redp), 101.3 * SC)
edges["fb3_right"] = find_edge(rp, lambda x: colfrac(rp, x, 400 * SC, 500 * SC, redp), 855.5 * SC)
edges["fb_top"] = find_edge(rp, lambda y: rowfrac(rp, y, 250 * SC, 550 * SC, redp), 179.0 * SC)
edges["fb_bot"] = find_edge(rp, lambda y: rowfrac(rp, y, 250 * SC, 550 * SC, redp), 256.4 * SC)
print("box edges (d px):", edges)
samples = {"summary_fill": rp[int(780 * SC), int(445 * SC)], "flow_fill": rp[int(200 * SC), int(200 * SC)],
           "quote_fill": rp[int(500 * SC), int(140 * SC)], "container_fill": rp[int(500 * SC), int(280 * SC)]}
print("samples:", json.dumps({k: list(v) for k, v in samples.items()}))

print("\nBAD:", bad)
json.dump(out, open(f"{BASE}/scratch/slide039/closed_loop_{TAG}.json", "w"), indent=1)
