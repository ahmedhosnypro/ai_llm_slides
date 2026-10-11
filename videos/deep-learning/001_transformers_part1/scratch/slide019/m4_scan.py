#!/usr/bin/env python3
"""m4_scan.py — exact unquantized color modes + circle centers + leader-line colors."""
from PIL import Image
import collections

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_019.jpg").convert("RGB")
px = IM.load()

def mode_excl_dark(x0, y0, x1, y1, thresh=380, topn=5):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if sum(c) >= thresh:
                cnt[c] += 1
    return cnt.most_common(topn)

def mode_dark(x0, y0, x1, y1, thresh=340, topn=5):
    cnt = collections.Counter()
    for y in range(y0, y1):
        for x in range(x0, x1):
            c = px[x, y]
            if sum(c) < thresh:
                cnt[c] += 1
    return cnt.most_common(topn)

print("== A&N blue boxes (non-dark modes) ==")
print("enc top (660,275)-(718,285):", mode_excl_dark(660, 275, 718, 285))
print("enc mid (662,344)-(716,353):", mode_excl_dark(662, 344, 716, 353))
print("dec top (760,210)-(814,217):", mode_excl_dark(760, 210, 814, 217))
print("dec purp (754,332)-(812,342):", mode_excl_dark(754, 332, 812, 342))
print("\n== FF boxes ==")
print("enc FF (656,296)-(716,310) excl dark:", mode_excl_dark(656, 296, 716, 310))
print("dec FF (756,226)-(816,246) excl dark:", mode_excl_dark(756, 226, 816, 246))
print("\n== vivid green jogs ==")
print("enc jog y325-331 x645-680:", mode_excl_dark(645, 325, 680, 331, 200))
print("dec chan y300-306 x830-838:", mode_excl_dark(830, 300, 838, 306, 200))
print("\n== callout fills ==")
print("blue callout (200,110)-(320,124):", mode_excl_dark(200, 110, 320, 124))
print("gray callout (330,150)-(500,164):", mode_excl_dark(330, 150, 500, 164))
print("green callout (280,186)-(440,203):", mode_excl_dark(280, 186, 440, 203))
print("\n== callout text colors (dark modes) ==")
print("blue callout text (160,108)-(330,126):", mode_dark(160, 108, 330, 126))
print("gray callout text (320,148)-(505,168):", mode_dark(320, 148, 505, 168))
print("green callout text (270,184)-(455,206):", mode_dark(270, 184, 455, 206))
print("\n== leader-line samples ==")
for (x, y) in [(400,118),(460,119),(490,121),(520,126),(556,138),(540,160),(556,162),(566,166),(500,199),(511,205),(523,211),(529,214),(540,228),(548,244)]:
    print(f"({x},{y}) -> {px[x,y]}")

# circle centers: scan 40x40 windows for the dominant saturated blob
def circle_probe(cx, cy, r, name):
    xs, ys, greens, blues, reds = [], [], 0, 0, 0
    for y in range(cy - r, cy + r):
        for x in range(cx - r, cx + r):
            R, G, B = px[x, y]
            if G > R + 40 and G > B + 40 and G > 90:
                greens += 1; xs.append(x); ys.append(y)
            elif B > 100 and R < 80 and G < 80:
                blues += 1; xs.append(x); ys.append(y)
            elif R > 110 and R > G + 60 and R > B + 60:
                reds += 1; xs.append(x); ys.append(y)
    if xs:
        n = len(xs)
        print(f"{name}: blob n={n} center~({sum(xs)//n},{sum(ys)//n}) greens={greens} blues={blues} reds={reds}")

print("\n== circle probes (40px windows) ==")
circle_probe(663, 401, 20, "enc V (663,401)")
circle_probe(695, 401, 20, "enc K (695,401)")
circle_probe(717, 401, 20, "enc Q (717,401)")
circle_probe(752, 392, 20, "decMask V (752,392)")
circle_probe(795, 392, 20, "decMask K (795,392)")
circle_probe(821, 392, 20, "decMask Q (821,392)")
circle_probe(748, 316, 20, "decCross V (748,316)")
circle_probe(773, 316, 20, "decCross K (773,316)")
circle_probe(820, 316, 20, "decCross Q (820,316)")

# exact circle fill mode at found centers
print("\n== circle fill exact ==")
for name, (cx, cy) in {"encV": (663, 401), "decMaskV": (752, 392), "decCrossV": (748, 316)}.items():
    print(name, mode_excl_dark(cx - 4, cy - 4, cx + 4, cy + 4, 250, 6))

# 18 vs 19 inheritance sanity: SDPA/MHA insets unchanged? sample key features
print("\n== inset carry-over checks ==")
print("sdpa frame left edge x59-61 y350:", [px[x, 350] for x in range(58, 63)])
print("mha red rect (x303-475 y354-396) top edge y354:", [px[x, 354] for x in range(310, 470, 40)])
print("enc mha box fill (660-715,362-380):", mode_excl_dark(660, 362, 715, 380))
print("dec mha box fill (752-817,282-305):", mode_excl_dark(752, 282, 817, 305))
print("title text y60-84 x300-660 dark mode:", mode_dark(300, 60, 660, 84, 400, 3))
