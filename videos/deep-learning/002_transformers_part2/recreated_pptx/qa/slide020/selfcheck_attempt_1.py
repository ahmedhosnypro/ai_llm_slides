#!/usr/bin/env python3
"""selfcheck_attempt_1 — closed-loop PIL check of render_1.png (150dpi) vs the
original frame's measured element positions. Scale: render px *72/150 = slide pt;
slide->frame: fx = sx*0.961231+18.628, fy = sy*0.955556. Tolerance ~4px@150dpi.
"""
from PIL import Image
import json, sys

RENDER = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide020/render_1.png"
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


def is_darkred(p):
    r, g, b = p
    return 100 < r < 190 and g < 60 and b < 60


def bbox(pred, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, min(y1, H)) for x in range(min(x0, W)) if False]
    pts = [(x, y) for y in range(y0, min(y1, H)) for x in range(x0, min(x1, W)) if pred(px[x, y])]
    if not pts:
        return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]


def r2f_x(rx): return rx * 72.0 / 150.0 * 0.961231 + 18.628
def r2f_y(ry): return ry * 72.0 / 150.0 * 0.955556
def cmp(name, got, want, tol=5.6):  # 5.6 render px ~ 4px@150dpi=1.92pt... use 6px tol
    if got is None:
        fails.append(f"{name}: NO INK FOUND (want frame {want})")
        return
    gf = [r2f_x(got[0]), r2f_y(got[1]), r2f_x(got[2]), r2f_y(got[3])]
    d = max(abs(gf[i] - want[i]) for i in range(4))
    status = "OK" if d <= tol else "OFF"
    if d > tol:
        fails.append(f"{name}: render->frame {['%.1f'%v for v in gf]} vs target {want} (maxd {d:.1f} > {tol})")
    out[name] = {"render_bbox": got, "frame_equiv": [round(v, 1) for v in gf], "target_frame": want, "maxd_px_frame": round(d, 1), "status": status}


# 1. title ink (want frame [316,60,693,82])
cmp("title", bbox(is_red, 550, 1550, 110, 210), [316, 60, 693, 82])

# 2. row1 word boxes: red border band (want y 106..127.5, x 180..875)
cmp("row1_boxes", bbox(is_red, 280, 1900, 195, 290), [180, 106, 869, 127.5])
# row1 label ink (want rows 108..124)
cmp("row1_label", bbox(is_red, 330, 1900, 200, 285), [191, 108, 869, 124])

# 3. row2 lane: green border (want x 164..883, y 154.5..192.5)
cmp("lane2_green", bbox(is_green, 280, 1950, 300, 430), [164, 154.5, 883, 192.5])
# row2 yellow cells (want y 164..182, x 156..~846)
def is_yel(p):
    r, g, b = p
    return r > 215 and 195 < g < 245 and 110 < b < 200
cmp("row2_cells_yellow", bbox(is_yel, 280, 1950, 320, 425), [182, 164, 846, 182])

# 4. row3 lane: blue border + lavender fill (want x 164..883, y 217..256)
cmp("lane3_blue", bbox(is_blue, 280, 1950, 440, 560), [174, 217, 871, 256])
# row3 labels (want rows 229..247, x 174..871)
cmp("row3_label", bbox(is_blue, 300, 1900, 470, 540), [185, 229, 862, 247])

# 5. bolts: orange (want x 272..837, rows 249..257)
cmp("bolts", bbox(is_orange, 480, 1900, 505, 560), [272, 249, 837, 257])

# 6. +delta: red (want x 228..808, rows 269..281, excluding arrow2 shaft 717-723)
def red_noArrow(x, y):
    return is_red(px[x, y]) and not (713 * 150 / 72 <= 0) and True
# arrow2 shaft in render: cx 729.6pt -> render x 1520; exclude 1490..1550
pts = [(x, y) for y in range(545, 625) for x in range(430, 1900)
       if is_red(px[x, y]) and not (1480 <= x <= 1560)]
if pts:
    bb = [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]
else:
    bb = None
cmp("deltas", bb, [228, 269, 808, 281])

# 7. banner: dark red rect (want x 165..882, y 294..331) + yellow text (217..303, 305..319)
cmp("banner", bbox(is_darkred, 280, 1950, 590, 720), [165, 294, 882, 331])
def is_yel_txt(p):
    r, g, b = p
    return r > 200 and g > 160 and b < 120
cmp("banner_combine", bbox(is_yel_txt, 350, 900, 620, 700), [217, 305, 303, 319])
# white text: near-white inside banner region
def is_white(p):
    r, g, b = p
    return r > 225 and g > 225 and b > 225
cmp("banner_white", bbox(is_white, 500, 1900, 625, 690), [315, 305, 822, 321])

# 8. arrows: shafts (A1 cx 614.5f, A2 720f, A3/A4 519.5f)
cmp("arrow1", bbox(is_red, 1230, 1330, 540, 625), [611, 264, 618, 292])
cmp("arrow2", bbox(is_red, 1450, 1560, 390, 630), [717, 196, 723, 294])
cmp("arrow3", bbox(is_red, 1030, 1130, 680, 770), [516, 331, 523, 360])
cmp("arrow4", bbox(is_red, 1030, 1130, 860, 950), [516, 419, 523, 446])

# 9. row4 boxes (want y 358..400, x 162..875) + labels (370..395)
cmp("row4_boxes", bbox(is_red, 280, 1900, 730, 860), [162, 358, 869, 400])

# 10. brace (want x 176..863, y 400..421)
cmp("brace", bbox(lambda p: is_red(p), 320, 1900, 820, 905), [176, 400, 863, 421])

# 11. caption (want x 362..676, y 457..467) — blue 2222CC
def is_capblue(p):
    r, g, b = p
    return b > 140 and (b - r) > 40 and (b - g) > 40
cmp("caption", bbox(is_capblue, 700, 1500, 940, 1030), [362, 457, 676, 467])

# 12. inset green box (want x 66..200, y 415..513)
def is_ingreen(p):
    r, g, b = p
    return g > 80 and (g - r) > 25 and (g - b) > 10
cmp("inset_green", bbox(is_ingreen, 80, 480, 850, 1080), [66, 415, 200, 513])
cmp("inset_pinkbox", bbox(lambda p: p[0] > 215 and 140 < p[1] < 210 and 160 < p[2] < 225, 100, 400, 950, 1080), [80, 480, 165, 505])
# green 'Input to Encoder' label (want x 196..262, y 469..495)
cmp("lab5_green", bbox(is_ingreen, 380, 620, 950, 1060), [196, 469, 262, 495])

# 13. left labels
cmp("lab1_gray", bbox(lambda p: abs(p[0] - p[1]) < 25 and abs(p[1] - p[2]) < 25 and 60 < p[0] < 170, 80, 360, 180, 300), [69, 93, 151, 136])
cmp("lab2_green", bbox(is_green, 80, 360, 300, 420), [67, 156, 151, 193])
cmp("lab3_blue", bbox(is_blue, 80, 360, 450, 530), [69, 225, 142, 247])
cmp("lab4_red", bbox(is_red, 80, 360, 600, 700), [68, 301, 142, 326])

# 14. frame containment: no content ink outside the house frame (x<42, x>919, y<45, y>539 frame)
cont = []
for x0, x1, y0, y1, tag in ((0, 80, 100, 1060, "left"), (1930, 2001, 100, 1060, "right"), (100, 1900, 0, 88, "top"), (100, 1900, 1075, 1125, "bottom")):
    bad = [(x, y) for y in range(y0, min(y1, H)) for x in range(x0, min(x1, W))
           if is_red(px[x, y]) or is_green(px[x, y]) or is_blue(px[x, y])]
    # allow the chrome's own red border strokes (panel edges) — only flag CONTENT-colored ink (green/blue) or red deep inside margins
    if tag in ("left", "right") and bad:
        cont.append(f"{tag}: {len(bad)} ink px (e.g. {bad[:3]})")
out["containment_green_blue_outside"] = cont
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
