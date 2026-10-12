#!/usr/bin/env python3
"""Closed-loop self-check attempt 1: measure render_1.png (150dpi, 2000x1125) and compare
every measured band against the original frame's PIL measurements (scale x2000/960 = 2.0833).
Tolerance ~4px @150dpi (self-check law). Prints PASS/FAIL per element."""
import json
from collections import Counter
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide014/render_1.png"
S = 2000 / 960.0
img = Image.open(REN).convert("RGB")
W, H = img.size
px = img.load()
results = []

def bbox(pred, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if pred(px[x, y])]
    if not pts: return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), max(xs), min(ys), max(ys))

def is_red(p): r,g,b=p; return r>140 and g<80 and b<80
def is_whiteish(p): r,g,b=p; return r>225 and g>225 and b>225
def is_black(p): r,g,b=p; return r<90 and g<90 and b<90

def check(name, target_px, got_px150, tol=4.0):
    """target_px: original frame px tuple (x0,x1,y0,y1) or None; got in 150dpi px."""
    if target_px is None or got_px150 is None:
        results.append((name, "FAIL", f"missing (target={target_px} got={got_px150})"))
        return
    t = [v * S for v in target_px]
    errs = [abs(a - b) for a, b in zip(t, got_px150)]
    ok = all(e <= tol for e in errs)
    results.append((name, "PASS" if ok else "FAIL",
                    f"err={['%.1f' % e for e in errs]} target150={['%.0f' % v for v in t]} got={list(got_px150)}"))

# ---- title ----
tb = bbox(is_red, int(100*S), int(850*S), int(55*S), int(115*S))
check("title_ink", (162, 776, 77, 102), tb)
# ---- takeaway ----
tk = bbox(is_red, int(90*S), int(840*S), int(425*S), int(465*S))
check("takeaway_ink", (108, 815, 437, 452), tk)
# ---- green box + text ----
def is_green(p): r,g,b=p; return 0<r<60 and 100<g<160 and 30<b<90
gb = bbox(is_green, int(80*S), int(290*S), int(200*S), int(310*S))
check("green_box", (99, 263, 224, 281), gb)
if gb:
    gt = bbox(is_whiteish, gb[0]+3, gb[1]-3, gb[2]+3, gb[3]-3)
    check("green_text", (114, 245, 247, 260), gt)
# ---- darkred box + lines ----
def is_dr(p): r,g,b=p; return 130<r<185 and g<35 and b<35
db = bbox(is_dr, int(290*S), int(545*S), int(170*S), int(330*S))
check("darkred_box", (304, 521, 197, 307), db)
if db:
    def lines_from(pred, x0, x1, y0, y1, gap=2):
        rows = [y for y in range(y0, y1) if any(pred(px[x, y]) for x in range(x0, x1))]
        ls = []
        for y in rows:
            if ls and y - ls[-1][1] <= gap: ls[-1][1] = y
            else: ls.append([y, y])
        res = []
        for l in ls:
            cols = [x for x in range(x0, x1) if any(pred(px[x, y]) for y in range(l[0], l[1] + 1))]
            res.append((min(cols), max(cols), l[0], l[1]))
        return res
    dt = lines_from(is_whiteish, db[0]+4, db[1]-4, db[2]+4, db[3]-4)
    tgt = [(343, 475, 224, 236), (384, 440, 247, 261), (309, 514, 270, 285)]
    results.append(("darkred_lines_n", "PASS" if len(dt) == 3 else "FAIL", f"n={len(dt)}"))
    for i, t in enumerate(tgt):
        if i < len(dt): check(f"darkred_line{i+1}", t, dt[i], tol=5.0)
# ---- ice box + text ----
def is_ice(p): r,g,b=p; return 200<r<245 and g>230 and b>230
ib = bbox(is_ice, int(540*S), int(680*S), int(190*S), int(300*S))
check("ice_fill", (563, 654, 217, 290), ib)
if ib:
    it = bbox(is_black, ib[0]+3, ib[1]-3, ib[2]+3, ib[3]-3)
    check("ice_text", (572, 644, 229, 279), it, tol=5.0)  # target excludes the cursor sliver (x655..656 y291..292, recording artifact)
# navy borders of ice box: check row/col at borders
def is_navy(p): r,g,b=p; return b>90 and b-r>50 and b-g>50 and r<160
nb = bbox(is_navy, int(545*S), int(675*S), int(205*S), int(300*S))
check("ice_border_navy", (559, 657, 214, 293), nb, tol=5.0)
# ---- tan box + Error text ----
def is_tan(p): r,g,b=p; return 235<r<255 and 205<g<235 and 180<b<210
tn = bbox(is_tan, int(675*S), int(740*S), int(145*S), int(360*S))
check("tan_box", (691, 726, 159, 347), tn)
if tn:
    tt = bbox(is_black, tn[0]+2, tn[1]-2, tn[2]+2, tn[3]-2)
    check("error_text_vert", (702, 715, 228, 277), tt, tol=5.0)
# ---- yellow box + text ----
def is_yel(p): r,g,b=p; return 240<r<256 and 244<g<256 and 200<b<232
yb = bbox(is_yel, int(745*S), int(875*S), int(150*S), int(350*S))
check("yellow_fill", (760, 859, 228, 279), yb)
if yb:
    yt = bbox(is_black, yb[0]+2, yb[1]-2, yb[2]+2, yb[3]-2)
    check("yellow_text", (770, 844, 231, 277), yt, tol=5.0)
# ---- arrows: red bboxes in gaps ----
gaps = {"arrow1": (264, 304, 240, 265), "arrow2": (523, 560, 240, 265),
        "arrow3": (661, 691, 240, 265), "arrow4": (727, 761, 240, 265)}
tgtA = {"arrow1": (268, 302, 248, 256), "arrow2": (523, 558, 249, 257),
        "arrow3": (666, 687, 249, 258), "arrow4": (730, 753, 249, 258)}
for name, (x0, x1, y0, y1) in gaps.items():
    ab = bbox(is_red, int(x0*S), int(x1*S), int(y0*S), int(y1*S))
    check(name, tgtA[name], ab, tol=5.0)
# ---- L-frame ----
def is_red_loose(p): r,g,b=p; return r>100 and r-g>35 and r-b>35
xs = [x for x in range(int(30*S), int(950*S)) if is_red_loose(px[x, int(43*S)])]
check("L_top_x", (57, 899), (min(xs), max(xs)) if xs else None, tol=5.0)
ys = [y for y in range(int(30*S), int(530*S)) if is_red_loose(px[int(58*S), y])]
check("L_left_y", (42, 517), (min(ys), max(ys)) if ys else None, tol=5.0)
# ---- black bar ----
bb = bbox(is_black, 0, W - 1, int(505*S), H - 1)
check("black_bar", (38, 921, 519, 537), bb, tol=5.0)
# ---- panel navy strokes ----
out = {}
out["navy_top_rows"] = [y for y in range(int(120*S), int(150*S)) if sum(1 for x in range(int(100*S), int(800*S), 4) if is_navy(px[x, y])) > int(500*S/4)]
out["navy_bot_rows"] = [y for y in range(int(360*S), int(385*S)) if sum(1 for x in range(int(100*S), int(800*S), 4) if is_navy(px[x, y])) > int(500*S/4)]
out["navy_left_cols"] = [x for x in range(int(65*S), int(85*S)) if sum(1 for y in range(int(140*S), int(370*S), 4) if is_navy(px[x, y])) > int(150*S/4)]
out["navy_right_cols"] = [x for x in range(int(875*S), int(895*S)) if sum(1 for y in range(int(140*S), int(370*S), 4) if is_navy(px[x, y])) > int(150*S/4)]
ok = (out["navy_top_rows"] and abs(out["navy_top_rows"][0] - 134*S) <= 4 and
      out["navy_bot_rows"] and abs(out["navy_bot_rows"][0] - 371*S) <= 4 and
      out["navy_left_cols"] and abs(out["navy_left_cols"][0] - 74*S) <= 4 and
      out["navy_right_cols"] and abs(out["navy_right_cols"][0] - 885*S) <= 5)
results.append(("panel_border", "PASS" if ok else "FAIL", json.dumps(out)))

# ---- font-size sanity: title/takeaway ink widths ----
if tb:
    w_t = (tb[1] - tb[0]) / S
    results.append(("title_width_px_orig_scale", "INFO", f"got={w_t:.0f} target=614"))
if tk:
    w_k = (tk[1] - tk[0]) / S
    results.append(("takeaway_width_px_orig_scale", "INFO", f"got={w_k:.0f} target=707"))

nfail = sum(1 for r in results if r[1] == "FAIL")
for r in results:
    print(f"[{r[1]:4s}] {r[0]}: {r[2]}")
print(f"\nSELF-CHECK ATTEMPT 1: {'PASS' if nfail == 0 else f'{nfail} FAILURES'}")
