#!/usr/bin/env python3
"""selfcheck_attempt_2 — closed-loop PIL check of render_13.png vs the original's
measured element positions (windows tightened after attempt 1's false alarms).
"""
from PIL import Image
import json, sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide020/render_13.png"
img = Image.open(RENDER).convert("RGB")
W, H = img.size
px = img.load()
out = {"size": [W, H]}
fails = []


def is_red(p):
    r, g, b = p
    return r > 130 and (r - g) > 45 and (r - b) > 45


def is_green(p):
    r, g, b = p
    return g > 100 and (g - r) > 40 and (g - b) > 20


def is_blue(p):
    r, g, b = p
    return b > 120 and (b - r) > 40 and (b - g) > 40


def is_orange(p):
    r, g, b = p
    return r > 180 and 100 < g < 210 and b < 150 and (r - b) > 50


def bbox(pred, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, min(y1, H)) for x in range(x0, min(x1, W)) if pred(px[x, y])]
    if not pts:
        return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]


def r2f_x(rx): return rx * 0.48 * 0.961231 + 18.628
def r2f_y(ry): return ry * 0.48 * 0.955556


def cmp(name, got, want, tol=6.0):
    if got is None:
        fails.append(f"{name}: NO INK FOUND (want frame {want})")
        return
    gf = [r2f_x(got[0]), r2f_y(got[1]), r2f_x(got[2]), r2f_y(got[3])]
    d = max(abs(gf[i] - want[i]) for i in range(4))
    status = "OK" if d <= tol else "OFF"
    if d > tol:
        fails.append(f"{name}: render->frame {['%.1f' % v for v in gf]} vs target {want} (maxd {d:.1f} > {tol})")
    out[name] = {"frame_equiv": [round(v, 1) for v in gf], "target_frame": want, "maxd_px_frame": round(d, 1), "status": status}


# 1. title ink
cmp("title", bbox(is_red, 550, 1550, 110, 210), [316, 60, 693, 82])

# 2. row1: boxes+labels band
cmp("row1_band", bbox(is_red, 300, 1900, 195, 290), [180, 106, 875, 127.5])
cmp("row1_container", bbox(lambda p: abs(p[0]-p[1])<20 and abs(p[1]-p[2])<20 and sum(p)<420, 300, 1900, 195, 300), [166, 96, 883, 138])
# label-only band (window excludes box top/bottom borders)
cmp("row1_labels", bbox(is_red, 340, 1880, 236, 274), [180, 108, 875, 125])

# 3. row2 lane (green dashed) + yellow cells
cmp("lane2_green", bbox(is_green, 300, 1950, 300, 430), [164, 154.5, 883, 192.5])
def is_yel(p):
    r, g, b = p
    return r > 215 and 195 < g < 245 and 110 < b < 200
cmp("row2_cells_yellow", bbox(is_yel, 280, 1950, 320, 425), [186, 164, 826, 182])

# 4. row3 lane + labels (lane extent)
cmp("lane3_blue", bbox(is_blue, 280, 1950, 440, 560), [164, 217, 883, 256])

# 5. bolts
cmp("bolts", bbox(lambda p: is_orange(p), 480, 1830, 505, 560), [272, 249, 837, 257])

# 6. +delta (below bolts, excluding arrow2 shaft x 1480-1560)
pts = [(x, y) for y in range(578, 622) for x in range(430, 1830)
       if is_red(px[x, y]) and not (1270 <= x <= 1315) and not (1480 <= x <= 1560)]
bb = [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)] if pts else None
cmp("deltas", bb, [228, 265, 808, 287])

# 7. banner rect + Combine + white text (windows inside the banner)
def is_darkred(p):
    r, g, b = p
    return 100 < r < 190 and g < 60 and b < 60
cmp("banner", bbox(is_darkred, 280, 1950, 590, 720), [165, 294, 882, 331])
def is_yel_txt(p):
    r, g, b = p
    return r > 200 and g > 160 and b < 120
def is_white(p):
    r, g, b = p
    return r > 235 and g > 235 and b > 235
cmp("banner_sentence", bbox(lambda p: is_yel_txt(p) or is_white(p), 380, 1860, 645, 715), [217, 305, 822, 321])
def is_white(p):
    r, g, b = p
    return r > 235 and g > 235 and b > 235

# 8. arrows (full-length windows)
cmp("arrow1", bbox(is_red, 1275, 1310, 545, 638), [611, 264, 618, 292])
cmp("arrow2", bbox(is_red, 1506, 1536, 390, 636), [717, 196, 723, 294])
cmp("arrow3", bbox(is_red, 1080, 1112, 724, 778), [516, 331, 523, 360])
cmp("arrow4", bbox(is_red, 1080, 1112, 908, 982), [516, 419, 523, 446])

# 9. row4 lane+boxes band
cmp("row4_lane_top", bbox(is_red, 300, 1050, 770, 790), [162, 357, 505, 361])
cmp("row4_band", bbox(is_red, 280, 1900, 782, 865), [162, 358, 883, 398])

# 10. brace (window below row4)
cmp("brace_left", bbox(is_red, 300, 1060, 869, 975), [176, 400, 505, 413.5])
cmp("brace_right", bbox(is_red, 1140, 1880, 869, 975), [544, 400, 863, 413.5])

# 11. caption
def is_capblue(p):
    r, g, b = p
    return b > 140 and (b - r) > 40 and (b - g) > 40
cmp("caption", bbox(is_capblue, 700, 1500, 940, 1030), [362, 457, 676, 467])

# 12. inset (window excludes lab5)
def is_ingreen(p):
    r, g, b = p
    return g > 80 and (g - r) > 25 and (g - b) > 10
cmp("inset_green", bbox(is_ingreen, 80, 390, 850, 1120), [66, 415, 200, 513])
cmp("inset_pinkbox", bbox(lambda p: p[0] > 200 and 140 < p[1] < 215 and 150 < p[2] < 230 and (p[0]-p[1])>10, 100, 400, 930, 1115), [131, 451, 200, 474])
cmp("lab5_green", bbox(is_ingreen, 400, 640, 950, 1100), [204, 469, 262, 495])

# 13. left labels (windows exclude lanes/banner)
cmp("lab1_gray", bbox(lambda p: abs(p[0] - p[1]) < 25 and abs(p[1] - p[2]) < 25 and 60 < p[0] < 170, 95, 300, 180, 300), [69, 93, 151, 136])
cmp("lab2_green", bbox(is_green, 95, 300, 300, 420), [67, 156, 151, 193])
cmp("lab3_blue", bbox(is_blue, 95, 300, 450, 530), [69, 225, 142, 247])
cmp("lab4_red", bbox(is_red, 95, 310, 640, 720), [68, 301, 142, 326])

# 14. containment: no green/blue content ink outside the house frame
cont = []
for x0, x1, y0, y1, tag in ((0, 80, 100, 1060, "left"), (1930, 2001, 100, 1060, "right"), (100, 1900, 0, 88, "top"), (100, 1900, 1120, 1125, "bottom")):
    bad = [(x, y) for y in range(y0, min(y1, H)) for x in range(x0, min(x1, W))
           if is_green(px[x, y]) or is_blue(px[x, y])]
    if bad:
        cont.append(f"{tag}: {len(bad)} ink px (e.g. {bad[:3]})")
out["containment"] = cont
if cont:
    fails.append(f"containment: {cont}")

print(json.dumps(out, indent=1))
print()
if fails:
    print("SELFCHECK: FAIL")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELFCHECK: ALL OK")
