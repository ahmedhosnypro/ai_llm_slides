#!/usr/bin/env python3
# selfcheck_attempt_2.py — closed-loop ink-band comparison, render (150dpi, 2001x1125)
# vs original frame (960x540) mapped through slide_x=(fx-18.63)/0.96123,
# slide_y=fy/0.95556; 1 slide pt = 2001/960 render px. Tolerance ~8 render px
# (== ~4 frame px) unless noted. v2: coordinate-correct, contamination-free windows.
import numpy as np
from PIL import Image

REN = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide042/render_2.png"
FR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_042.jpg"
ren = np.asarray(Image.open(REN).convert("RGB")).astype(int)
fr = np.asarray(Image.open(FR).convert("RGB")).astype(int)
RH, RW = ren.shape[:2]
K = RW / 960.0

def R2(fx, fy):
    return ((fx - 18.63) / 0.96123 * K, fy / 0.95556 * K)

def bbox_of(mask, ox, oy):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return (int(ox + xs.min()), int(oy + ys.min()), int(ox + xs.max()), int(oy + ys.max()), len(xs))

def dark(img):
    return img.sum(axis=-1) < 560

def rmask(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    return (r - g > 40) & (r - b > 40) & (r > 110)

def gmask(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    return (g - r > 40) & (g - b > 40)

def cmask(img, kind):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    if kind == "m":
        return (r - g > 60) & (b - g > 40) & (r > 80)
    if kind == "b":
        return (b - r > 50) & (b - g > 20)
    if kind == "y":
        return (r - b > 80) & (g - b > 60) & (r > 150)
    if kind == "o":
        return (r - b > 90) & (r - g > 40) & (g - b > 10) & (g > 60) & (g < 190)
    if kind == "g":
                return (g - r > 40) & (g - b > 40)
    if kind == "bg":
        return (b - r > 15) & (b > 90) & (r > 40) & (g > 60)
    return None

fails = 0
print(f"render {RW}x{RH}")

def cmp(tag, fx0, fy0, fx1, fy1, mask_fn=dark, tol=8):
    gx0, gy0 = R2(fx0, fy0); gx1, gy1 = R2(fx1, fy1)
    g = bbox_of(mask_fn(ren)[int(gy0):int(gy1), int(gx0):int(gx1)], gx0, gy0)
    w = bbox_of(mask_fn(fr)[fy0:fy1, fx0:fx1], fx0, fy0)
    if g is None or w is None:
        print(f"  FAIL {tag}: missing ink (render {g}, want {w})"); return 1
    wr = (int(R2(w[0], 0)[0]), int(R2(0, w[1])[1]), int(R2(w[2], 0)[0]), int(R2(0, w[3])[1]))
    d = tuple(int(g[i] - wr[i]) for i in range(4))
    ok = all(abs(v) <= tol for v in d)
    print(f"  {'ok  ' if ok else 'FAIL'} {tag}: d={d} got{g[:4]} want{wr[:4]}(frame{w[:4]})")
    return 0 if ok else 1

print("TITLE")
fails += cmp("title", 150, 45, 850, 131)

print("BLUE FRAME (navy lines)")
def navy_f(img):
    return (img[..., 2] - img[..., 0] > 40) & (img[..., 2] - img[..., 1] > 20) & (img[..., 2] > 100) & (img[..., 1] < 140)
for tag, fx0, fy0, fx1, fy1 in [("top", 200, 128, 800, 140), ("bottom", 200, 503, 800, 516),
                                ("left", 62, 300, 76, 450), ("right", 884, 300, 898, 450)]:
    gx0, gy0 = R2(fx0, fy0); gx1, gy1 = R2(fx1, fy1)
    g = bbox_of(navy_f(ren)[int(gy0):int(gy1), int(gx0):int(gx1)], gx0, gy0)
    w = bbox_of(navy_f(fr)[fy0:fy1, fx0:fx1], fx0, fy0)
    if w is None:
        ok = g is not None
        print(f"  {'ok* ' if ok else 'FAIL'} {tag}: orig faded, render {g[:4] if g else None}"); fails += 0 if ok else 1; continue
    if g is None:
        print(f"  FAIL {tag}: render missing (want {w[:4]})"); fails += 1; continue
    wr = (int(R2(w[0], 0)[0]), int(R2(0, w[1])[1]), int(R2(w[2], 0)[0]), int(R2(0, w[3])[1]))
    d = tuple(int(g[i] - wr[i]) for i in range(4))
    ok = abs(d[0]) <= 20 and abs(d[1]) <= 8 and abs(d[2]) <= 20 and abs(d[3]) <= 8
    print(f"  {'ok  ' if ok else 'FAIL'} {tag}: d={d} got{g[:4]} want{wr[:4]}(frame{w[:4]})")
    fails += 0 if ok else 1

print("LABEL BOXES (red borders)")
def reddish(img):
    r, g, b = img[..., 0], img[..., 1], img[..., 2]
    return (r - g > 25) & (r - b > 25) & (r > 110)
def cmp_border(tag, fx0, fy0, fx1, fy1):
    gx0, gy0 = R2(fx0, fy0); gx1, gy1 = R2(fx1, fy1)
    g = bbox_of(reddish(ren)[int(gy0):int(gy1), int(gx0):int(gx1)], gx0, gy0)
    w = bbox_of(reddish(fr)[fy0:fy1, fx0:fx1], fx0, fy0)
    if w is None:  # original line faded below the reddish threshold (1px JPEG line)
        ok = g is not None
        print(f"  {'ok* ' if ok else 'FAIL'} {tag}: orig faded, render {g[:4] if g else None}")
        return 0 if ok else 1
    if g is None:
        print(f"  FAIL {tag}: render missing (want {w[:4]})"); return 1
    wr = (int(R2(w[0], 0)[0]), int(R2(0, w[1])[1]), int(R2(w[2], 0)[0]), int(R2(0, w[3])[1]))
    d = tuple(int(g[i] - wr[i]) for i in range(4))
    vertical = (fx1 - fx0) < (fy1 - fy0)  # window taller than wide -> vertical line
    if vertical:
        gc, wc = (g[0] + g[2]) / 2, (wr[0] + wr[2]) / 2
        ok = abs(gc - wc) <= 8 and g[1] <= wr[3] and g[3] >= wr[1]
    else:
        gc, wc = (g[1] + g[3]) / 2, (wr[1] + wr[3]) / 2
        ok = abs(gc - wc) <= 8 and g[0] <= wr[2] and g[2] >= wr[0]
    print(f"  {'ok  ' if ok else 'FAIL'} {tag}: d={d} got{g[:4]} want{wr[:4]}(frame{w[:4]})")
    return 0 if ok else 1
for tag, fx0, fy0, fx1, fy1 in [("Ltop", 85, 191, 290, 200), ("Lbot", 85, 232, 290, 241),
                                ("Mtop", 350, 189, 590, 198), ("Mbot", 350, 230, 590, 239),
                                ("Rtop", 640, 161, 860, 170), ("Rbot", 640, 223, 860, 232),
                                ("Lleft", 72, 200, 82, 232), ("Mleft", 337, 198, 347, 230),
                                ("Rleft", 624, 170, 634, 222)]:
    fails += cmp_border(tag, fx0, fy0, fx1, fy1)

print("TEXT LINES (dark ink)")
for tag, fx0, fy0, fx1, fy1 in [("L-L1", 82, 197, 295, 213), ("L-L2", 82, 215, 295, 233),
                                ("M-L1", 344, 197, 594, 213), ("M-L2", 344, 215, 594, 233),
                                ("R-L1", 633, 169, 868, 185), ("R-L2", 633, 187, 868, 203),
                                ("R-L3", 633, 205, 868, 221)]:
    fails += cmp(tag, fx0, fy0, fx1, fy1)

print("WORD COLORS (ink-count ratio)")
def ratio(tag, fx0, fy0, fx1, fy1, kind):
    gx0, gy0 = R2(fx0, fy0); gx1, gy1 = R2(fx1, fy1)
    n_ren = int(cmask(ren, kind)[int(gy0):int(gy1), int(gx0):int(gx1)].sum())
    n_fr = int(cmask(fr, kind)[fy0:fy1, fx0:fx1].sum())
    r = n_ren / max(1, n_fr)
    ok = 0.3 < r < 9  # orig is a JPEG frame: colored small-text ink ~3-5x smaller
    print(f"  {'ok  ' if ok else 'FAIL'} {tag}: render {n_ren} vs orig {n_fr} (x{r:.2f})")
    return 0 if ok else 1
fails += ratio("L-L1-green(OneInput)", 213, 197, 282, 213, "g")
fails += ratio("L-L2-green(Sample)", 102, 215, 155, 233, "g")
fails += ratio("L-L2-blue(Usingfilter)", 156, 215, 274, 233, "b")
fails += ratio("M-L1-green", 465, 197, 589, 213, "g")
fails += ratio("M-L2-blue", 357, 215, 465, 233, "b")
fails += ratio("M-L2-magenta", 476, 215, 570, 233, "m")
fails += ratio("R-L2-green", 635, 187, 779, 203, "g")
fails += ratio("R-L2-magenta", 786, 187, 875, 203, "m")
fails += ratio("R-L3-blue", 635, 205, 733, 221, "b")
fails += ratio("R-L3-magenta", 735, 205, 831, 221, "m")

print("CUBES")
fails += cmp("left-stack", 150, 250, 240, 445, gmask, 10)
fails += cmp("mid-grid", 360, 240, 545, 440, gmask, 10)
fails += cmp("magenta-front", 645, 300, 795, 480, lambda im: cmask(im, "m"), 10)
fails += cmp("green-layer", 660, 280, 812, 462, lambda im: cmask(im, "g"), 16)
fails += cmp("orange-layer", 690, 265, 820, 447, lambda im: cmask(im, "o"), 16)
fails += cmp("yellow-layer", 700, 250, 845, 430, lambda im: cmask(im, "y"), 20)
fails += cmp("bluegray-layer", 700, 238, 860, 412, lambda im: cmask(im, "bg"), 20)

print("ARROWS + ROTATED LABELS (red)")
fails += cmp("v-arrow-heads+shaft", 637, 318, 652, 472, rmask, 12)
fails += cmp("v-label(strip)", 620, 340, 640, 440, dark, 10)
def cmp_y(tag, fx0, fy0, fx1, fy1, tol=8):
    gx0, gy0 = R2(fx0, fy0); gx1, gy1 = R2(fx1, fy1)
    g = bbox_of(rmask(ren)[int(gy0):int(gy1), int(gx0):int(gx1)], gx0, gy0)
    w = bbox_of(rmask(fr)[fy0:fy1, fx0:fx1], fx0, fy0)
    if g is None or w is None:
        print(f"  FAIL {tag}: missing (render {g}, want {w})"); return 1
    gc = (g[1] + g[3]) / 2
    wc = (R2(0, w[1])[1] + R2(0, w[3])[1]) / 2
    ok = abs(gc - wc) <= tol
    print(f"  {'ok  ' if ok else 'FAIL'} {tag}: ycenter render {gc:.0f} vs orig {wc:.0f} (got{g[:4]} want{w[:4]})")
    return 0 if ok else 1
fails += cmp_y("h-left-head", 644, 478, 668, 496)
fails += cmp_y("h-shaft-mid", 738, 480, 798, 494)
fails += cmp_y("h-right-head", 764, 478, 784, 496)
fails += cmp("Channels-label", 660, 468, 748, 484, dark, 8)
fails += cmp("(4 Filters)-label", 664, 489, 746, 500, dark, 8)
fails += cmp("d-arrow+labels", 783, 370, 875, 482, rmask, 20)

print("STACKING ARROW (white px on colored bg)")
def whitecount(img, conv, fx0=800, fy0=292, fx1=822, fy1=315):
    if conv:
        gx0, gy0 = R2(fx0, fy0); gx1, gy1 = R2(fx1, fy1)
        seg = img[int(gy0):int(gy1), int(gx0):int(gx1)]
    else:
        seg = img[fy0:fy1, fx0:fx1]
    return int((seg.sum(axis=-1) > 720).sum())
wr, wf = whitecount(ren, True), whitecount(fr, False)
ok = wr >= max(12, 0.3 * wf)
print(f"  {'ok  ' if ok else 'FAIL'} stack-arrow white px: render {wr} vs orig {wf}")
fails += 0 if ok else 1

print("CONTAINMENT (content ink in the ring around the blue frame)")
content = rmask(ren) | gmask(ren) | cmask(ren, "m") | cmask(ren, "bg")
strips = {
    "left": (62, 145, 67.5, 500), "right": (892, 145, 898, 500),
    "top": (75, 122, 885, 131.5), "bottom": (75, 513, 885, 515.5),
}
tot = 0
for tag, (fx0, fy0, fx1, fy1) in strips.items():
    gx0, gy0 = R2(fx0, fy0); gx1, gy1 = R2(fx1, fy1)
    n = int(content[int(gy0):int(gy1), int(gx0):int(gx1)].sum())
    tot += n
    print(f"  {tag} strip: {n}")
ok = tot < 300
print(f"  {'ok  ' if ok else 'FAIL'} ring ink total {tot}")
fails += 0 if ok else 1

print(f"\nTOTAL FAILS: {fails}")
