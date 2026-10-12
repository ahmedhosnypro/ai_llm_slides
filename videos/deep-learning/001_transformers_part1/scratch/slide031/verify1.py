#!/usr/bin/env python3
"""Closed-loop verify: render_1.png (2001x1125, 150dpi) vs frame-measured geometry.
scale = 2000/960 (frame px -> 150dpi px). Tolerance ~4px in 150dpi space."""
from PIL import Image

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide031/render_1.png"
im = Image.open(RENDER).convert("RGB")
W, H = im.size
px = im.load()
def c(x, y): return px[x, y]
S = 2000 / 960.0

def bb(pred, x0, y0, x1, y1):
    xs = []; ys = []
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            if 0 <= x < W and 0 <= y < H and pred(c(x, y)):
                xs.append(x); ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None

def check(name, expect_frame, got, tol=4.5):
    if got is None:
        print(f"  FAIL {name}: NOT FOUND (expected {tuple(round(v*S,1) for v in expect_frame)})")
        return
    e = [v * S for v in expect_frame]
    d = [got[i] - e[i] for i in range(4)]
    ok = all(abs(v) <= tol for v in d)
    print(f"  {'ok  ' if ok else 'FAIL'} {name}: got {got[:4]} expected ({e[0]:.0f},{e[1]:.0f},{e[2]:.0f},{e[3]:.0f}) d=({d[0]:+.0f},{d[1]:+.0f},{d[2]:+.0f},{d[3]:+.0f})")

pred_red = lambda cc: cc[0] > 120 and cc[0] - cc[1] > 45 and cc[0] - cc[2] > 45
pred_blue = lambda cc: cc[2] > 110 and cc[2] - cc[0] > 40 and cc[2] - cc[1] > 30
pred_grn = lambda cc: cc[1] > 80 and cc[1] - cc[0] > 18 and cc[1] - cc[2] > 18
pred_peach = lambda cc: 235 <= cc[0] <= 258 and 205 <= cc[1] <= 240 and 185 <= cc[2] <= 225 and cc[0] - cc[2] > 22 and cc[0] - cc[1] > 10
pred_yel = lambda cc: cc[0] > 235 and cc[1] > 210 and cc[2] < 175
isw = lambda cc: cc[0] > 244 and cc[1] > 244 and cc[2] > 244
pred_pinkpill = lambda cc: abs(cc[0]-255) < 12 and abs(cc[1]-208) < 25 and abs(cc[2]-246) < 25

print("=== peach canvas ===")
xs = [x for x in range(50, W) if pred_peach(c(x, 620))]
ys = [y for y in range(150, H) if pred_peach(c(1000, y))]
print(f"  row620 peach x {min(xs)}..{max(xs)} (exp {46*S:.0f}..{901*S:.0f}); col1000 peach y {min(ys)}..{max(ys)} (exp {92*S:.0f}..{536*S:.0f})")

print("=== panels (borders) ===")
def panel_scan(name, x0f, x1f, y0f, y1f, pred):
    # top/bottom rows
    for y in range(int(y0f*S)-14, int(y0f*S)+14):
        n = sum(1 for x in range(int(x0f*S)+30, int(x1f*S)-30) if pred(c(x, y)))
        if n > (x1f - x0f - 60) * S * 0.6:
            print(f"  {name} top stroke y={y} (exp {y0f*S:.0f})"); break
    for y in range(int(y1f*S)+14, int(y1f*S)-14, -1):
        n = sum(1 for x in range(int(x0f*S)+30, int(x1f*S)-30) if pred(c(x, y)))
        if n > (x1f - x0f - 60) * S * 0.6:
            print(f"  {name} bottom stroke y={y} (exp {y1f*S:.0f})"); break
    for x in range(int(x0f*S)-14, int(x0f*S)+14):
        n = sum(1 for y in range(int(y0f*S)+30, int(y1f*S)-30) if pred(c(x, y)))
        if n > (y1f - y0f - 60) * S * 0.6:
            print(f"  {name} left stroke x={x} (exp {x0f*S:.0f})"); break
    for x in range(int(x1f*S)+14, int(x1f*S)-14, -1):
        n = sum(1 for y in range(int(y0f*S)+30, int(y1f*S)-30) if pred(c(x, y)))
        if n > (y1f - y0f - 60) * S * 0.6:
            print(f"  {name} right stroke x={x} (exp {x1f*S:.0f})"); break
panel_scan("Q", 56, 467, 97, 300, pred_red)
panel_scan("V", 479, 888, 98, 299, pred_blue)
panel_scan("K", 58, 468, 311, 529, pred_grn)

print("=== Q internals ===")
check("Q input pill", (74, 136, 212, 172), bb(pred_pinkpill, 140, 260, 470, 390))
check("Q matrix (rose)", (218, 112, 374, 290), bb(lambda cc: abs(cc[0]-242)<14 and abs(cc[1]-199)<16 and abs(cc[2]-202)<16, 420, 200, 820, 640))
check("Q outcap outline", (411, 117, 452, 289), bb(pred_red, 830, 220, 990, 630))
check("Q W_Q label", (190, 240, 259, 299), bb(pred_red, 380, 480, 570, 640))
check("Q X2 label", (112, 178, 158, 218), bb(pred_red, 220, 360, 340, 460))
check("Q equals", (389, 199, 399, 207), bb(pred_red, 780, 395, 850, 450))
check("Q role letter", (415, 100, 450, 116), bb(pred_red, 850, 195, 965, 255))
print("=== V internals ===")
check("V outcap outline", (826, 116, 871, 289), bb(pred_red, 1690, 220, 1860, 630))
check("V W_V label", (608, 240, 677, 299), bb(pred_red, 1220, 480, 1450, 640))
check("V matrix (peri)", (635, 112, 791, 290), bb(lambda cc: abs(cc[0]-188)<16 and abs(cc[1]-188)<16 and abs(cc[2]-242)<16, 1280, 200, 1690, 640))
print("=== K internals ===")
check("K outcap outline", (413, 332, 456, 504), bb(pred_red, 830, 660, 990, 1080))
check("K matrix (mint)", (221, 330, 377, 505), bb(lambda cc: abs(cc[0]-201)<18 and abs(cc[1]-240)<18 and abs(cc[2]-216)<18, 420, 660, 820, 1080))
check("K role letter", (415, 299, 455, 315), bb(pred_grn, 850, 600, 965, 680))
print("=== callouts ===")
pred_ink = lambda cc: sum(cc) < 690 and not isw(cc)
check("callout1", (445, 272, 680, 314), bb(pred_ink, 890, 540, 1440, 690))
check("callout2", (700, 305, 919, 344), bb(pred_ink, 1440, 610, 1940, 750))
check("callout3", (445, 332, 680, 374), bb(pred_ink, 890, 670, 1440, 810))
print("=== boxes ===")
check("emphasis yellow", (645, 386, 881, 435), bb(pred_yel, 1300, 770, 1900, 950))
check("note box (border)", (491, 448, 903, 519), bb(lambda cc: sum(cc) < 690 and not isw(cc), 980, 900, 1920, 1110))
print("=== title / subtitle bands ===")
pred_dark = lambda cc: sum(cc) < 200
print("  title ink:", bb(pred_dark, 150, 90, 1790, 150), " exp x", 186*S, "..", 747*S, " y", 50*S, "..", 68*S)
print("  subtitle ink:", bb(lambda cc: sum(cc) < 620, 150, 148, 1790, 196), " exp x", 109*S, "..", 859*S, " y", 72*S, "..", 92*S)
