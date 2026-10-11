#!/usr/bin/env python3
"""m0_scan.py — PIL measurements of unique_slides/slide_019.jpg (960x540, 1px=1pt).

Delta facts to establish vs the certified slide-018 composition:
  A. three callout boxes (Normalization blue / Feed Forward gray / Residual green):
     bboxes, fills, borders, text colors
  B. leader lines from callouts toward the architecture (gap zone x488..575)
  C. green residual arrows looping the sublayers (near enc stack x628..728, dec x744..841)
  D. recoloring of the 5 'Add & Norm' + 2 'Feed Forward' compartments
  E. V/K/Q circle fills under the 3 architecture attention blocks ([?] item)
  F. confirm carried-over items (insets, enc/dec MHA boxes, yellow band, handles)
"""
from PIL import Image
import sys, collections

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
W, H = IM.size
px = IM.load()
print(f"size={W}x{H}")

def near(c, ref, tol):
    return all(abs(c[i] - ref[i]) <= tol for i in range(3))

def bbox_of(pred, x0, y0, x1, y1, step=1):
    minx, miny, maxx, maxy, n = 10**9, 10**9, -1, -1, 0
    for y in range(y0, y1, step):
        for x in range(x0, x1, step):
            if pred(px[x, y]):
                n += 1
                if x < minx: minx = x
                if x > maxx: maxx = x
                if y < miny: miny = y
                if y > maxy: maxy = y
    return (minx, miny, maxx, maxy, n)

def mode_of(x0, y0, x1, y1, exclude=None, tol=28):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if exclude and near(c, exclude, tol):
                continue
            cnt[(c[0] // 8 * 8, c[1] // 8 * 8, c[2] // 8 * 8)] += 1
    return cnt.most_common(6)

# ---- A. callout boxes: known palette candidates -------------------------------
CALLS = {
    "blue(CFE2F3)": (207, 226, 243),
    "gray(BFBFBF)": (191, 191, 191),
    "green(D9EAD3)": (217, 234, 211),
}
print("\n== A. callout fills (banner zone x40..540 y60..260) ==")
for name, ref in CALLS.items():
    bb = bbox_of(lambda c, r=ref: near(c, r, 14), 40, 60, 540, 260)
    print(f"{name}: bbox={bb[:4]} px={bb[4]}")

print("\n== A2. callout box edge/inner scan: horizontal profile at several rows ==")
# find, for each row band, runs of the three fills to get exact box extents
for name, ref in CALLS.items():
    rows = {}
    for y in range(60, 260):
        xs = [x for x in range(40, 560) if near(px[x, y], ref, 14)]
        if len(xs) > 30:
            rows[y] = (min(xs), max(xs), len(xs))
    if rows:
        ys = sorted(rows)
        # contiguous groups
        groups, cur = [], [ys[0]]
        for y in ys[1:]:
            if y - cur[-1] <= 2: cur.append(y)
            else: groups.append(cur); cur = [y]
        groups.append(cur)
        for g in groups:
            y0, y1 = g[0], g[-1]
            x0 = min(rows[y][0] for y in g); x1 = max(rows[y][1] for y in g)
            print(f"{name}: y {y0}..{y1}  x {x0}..{x1}")

# ---- A3. text colors inside each callout (dark pixel clusters) ----------------
print("\n== A3. dark-ink color modes inside callouts ==")
def text_modes(x0, y0, x1, y1):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if r + g + b < 420:  # darkish ink
                cnt[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
    return cnt.most_common(5)

# ---- B. leader lines in gap zone ----------------------------------------------
print("\n== B. gap-zone scan x488..578 y90..250: non-background ink ==")
BG = (255, 255, 255)
for y in range(90, 250):
    xs = [x for x in range(470, 578) if sum(px[x, y]) < 560 and not near(px[x, y], (192, 112, 112), 60)]
    if xs:
        # cluster
        print(f"y={y}: x {min(xs)}..{max(xs)} n={len(xs)} sample={px[xs[0], y]}")

# ---- C. green residual arrows near stacks --------------------------------------
print("\n== C. green ink (#38761D family) near encoder/decoder stacks ==")
GRN = (56, 118, 29)
def green_bbox(x0, y0, x1, y1, tol=45):
    return bbox_of(lambda c: near(c, GRN, tol), x0, y0, x1, y1)
print("enc zone  x600..745 y255..420:", green_bbox(600, 255, 745, 420))
print("dec zone  x735..860 y190..420:", green_bbox(735, 190, 860, 420))

# ---- D. compartment fill modes --------------------------------------------------
print("\n== D. fills of A&N / FF compartments in slide 019 ==")
REGIONS = {
    "enc A&N top   (630-725,268-287)": (632, 269, 723, 286),
    "enc FF        (651-720,289-314)": (653, 290, 718, 313),
    "enc A&N mid   (630-725,317-356)": (632, 318, 723, 355),
    "dec A&N top   (746-839,202-219)": (747, 203, 838, 218),
    "dec FF        (746-839,221-249)": (747, 222, 838, 248),
    "dec A&N mid   (746-839,251-264)": (747, 251, 838, 263),
    "dec purple A&N(748-816,328-347)": (750, 329, 815, 346),
}
for name, (x0, y0, x1, y1) in REGIONS.items():
    print(name, mode_of(x0, y0, x1, y1))

print("\n== D2. enc/dec MHA box fills (carry-over check) ==")
print("enc MHA (652-720,357-386):", mode_of(652, 357, 720, 386))
print("dec MHA (750-819,279-308):", mode_of(750, 279, 819, 308))

# ---- E. V/K/Q circle fills ------------------------------------------------------
print("\n== E. circle fills under the 3 architecture attention blocks ==")
CIRC = {
    "enc V(663.5,400.5)": (658, 395, 669, 406),
    "enc K(695,400.5)": (690, 395, 700, 406),
    "enc Q(717.5,400.5)": (712, 395, 723, 406),
    "decMaskV(752,391.5)": (746, 386, 758, 397),
    "decMaskK(795,391.5)": (788, 384, 802, 399),
    "decMaskQ(821.5,391.5)": (816, 386, 827, 397),
    "decCrossV(748.5,316)": (743, 311, 753, 321),
    "decCrossK(773,316.5)": (768, 311, 778, 322),
    "decCrossQ(820,316.5)": (815, 311, 825, 322),
}
for name, (x0, y0, x1, y1) in CIRC.items():
    print(name, mode_of(x0, y0, x1, y1))

# ---- F. carried-over checks ------------------------------------------------------
print("\n== F. carried-over items ==")
print("sdpa frame green (x59-189,y269-491) left edge col x59..61:",
      bbox_of(lambda c: near(c, (27, 113, 63), 40), 55, 260, 195, 500))
print("mha frame green (x300-508,y246-515) top edge row y246..248:",
      bbox_of(lambda c: near(c, (27, 113, 63), 40), 295, 240, 515, 260))
print("yellow band sample (700,258):", px[700, 258], " (736,290):", px[736, 290])
print("fig handles enc-stack corners (572,103) area:", bbox_of(lambda c: near(c, (27, 113, 63), 40), 565, 96, 585, 112))
print("title red mode (300-660,48-92):", text_modes(300, 48, 660, 92))
print("banner-zone old banner1 fill F2C699 present?", bbox_of(lambda c: near(c, (242, 198, 153), 12), 40, 60, 540, 260))
print("banner-zone old banner2 fill DECDBB present?", bbox_of(lambda c: near(c, (222, 205, 187), 12), 40, 60, 540, 260))
