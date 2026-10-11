#!/usr/bin/env python3
"""Attempt-2 pre-judge self-check: containment, anchors, region presence.
Render 150dpi 2001x1125 (1 px = 1/200 in); original frame 960x540 (1 px = 1 pt).
scale render->frame: *960/2000 = *0.48; frame->render: *2000/960 = *2.0833."""
from PIL import Image

QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide041/"
ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/unique_slides/slide_041.jpg"
ren = Image.open(QA + "render_3.png").convert("RGB")
org = Image.open(ORIG).convert("RGB")
rp, op = ren.load(), org.load()
RW, RH = ren.size
print(f"render {RW}x{RH} (expect 2001x1125)")
ok = True

def bbox(pixels, pred, x0, y0, x1, y1):
    xs, ys = [], []
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(pixels[x, y]):
                xs.append(x); ys.append(y)
    if not xs:
        return None
    return (min(xs), min(ys), max(xs), max(ys), len(xs))

def framescale(bb):  # render bbox -> frame px
    return tuple(round(v * 960 / 2000, 1) for v in bb[:4])

# 1) FRAME CONTAINMENT: no ink outside the chrome panel (white margin + panel border zone)
# panel: x 42..918 frame -> render x 87..1912; y 45..540 -> 94..1125
def not_white_not_chrome(c):
    r, g, b = c
    return not (r > 235 and g > 235 and b > 235)
stray = 0
for y in range(0, 94):
    for x in range(0, RW):
        if not_white_not_chrome(rp[x, y]): stray += 1
for y in range(94, RH):
    for x in range(0, 87):
        if not_white_not_chrome(rp[x, y]): stray += 1
    for x in range(1913, RW):
        if not_white_not_chrome(rp[x, y]): stray += 1
print(f"containment: {stray} ink px in white margin (excl chrome edge AA)")
if stray > 400: ok = False; print("[FAIL] containment")
else: print("[PASS] frame-containment")

# 2) ANCHORS vs original (render bbox vs orig bbox, max delta in frame px)
def close(a, b, tol):
    return all(abs(a[i] - b[i]) <= tol for i in range(4))

anchors = []
# center container tan fill
tan = lambda c: abs(c[0]-223) < 35 and abs(c[1]-170) < 40 and abs(c[2]-117) < 45
rb = bbox(rp, tan, 560, 400, 1120, 1120); ob = bbox(op, tan, 270, 195, 545, 540)
anchors.append(("center container", rb, ob))
# right panel green border
grn = lambda c: c[1] > 110 and c[1] > c[0] + 60 and c[1] > c[2] + 60
rb = bbox(rp, grn, 1150, 180, 1920, 1120); ob = bbox(op, grn, 550, 90, 930, 540)
anchors.append(("right panel border", rb, ob))
# left schematic green border
rb = bbox(rp, grn, 100, 520, 420, 1060); ob = bbox(op, grn, 45, 250, 210, 500)
anchors.append(("left schematic box", rb, ob))
for name, rb, ob in anchors:
    if not rb or not ob:
        print(f"[FAIL] anchor {name}: missing ink"); ok = False; continue
    fb = framescale(rb)
    d = max(abs(fb[i] - ob[i]) for i in range(4))
    stat = "PASS" if d <= 6 else "FAIL"
    if d > 6: ok = False
    print(f"[{stat}] anchor {name}: render(frame-px) {fb} vs orig {ob} maxD {d:.1f}")

# 3) REGION PRESENCE (render): colored evidence in expected zones (render px)
def zone_check(name, pred, x0, y0, x1, y1, minn):
    global ok
    bb = bbox(rp, pred, x0, y0, x1, y1)
    n = bb[4] if bb else 0
    stat = "PASS" if n >= minn else "FAIL"
    if n < minn: ok = False
    print(f"[{stat}] {name}: n={n}" + (f" bbox {bb[:4]}" if bb else ""))
    return bb

blue = lambda c: c[2] > 130 and c[2] > c[0] + 30 and c[2] > c[1] + 20
zone_check("blue Add&Norm x5 (render col)", blue, 1350, 400, 1740, 800, 800)
tanmha = lambda c: abs(c[0]-206) < 30 and abs(c[1]-128) < 35 and abs(c[2]-90) < 40
zone_check("encoder MHA tan fill", tanmha, 1340, 720, 1520, 830, 400)
zone_check("cross-MHA tan fill", tanmha, 1540, 560, 1730, 670, 300)
purple = lambda c: c[0] > 130 and c[2] > 150 and c[0] + c[2] > 2 * c[1] + 40
zone_check("masked MHA purple", purple, 1540, 700, 1740, 860, 800)
yell = lambda c: c[0] > 200 and c[1] > 200 and c[2] < 130
zone_check("yellow highlights (3)", yell, 1380, 200, 1720, 1090, 500)
zone_check("SDPA red border stack", lambda c: c[0] > 150 and c[1] < 90 and c[2] < 90, 610, 720, 1030, 850, 400)
zone_check("pin red", lambda c: c[0] > 150 and c[1] < 90 and c[2] < 90, 500, 260, 660, 420, 500)
lgreen = lambda c: c[1] > 180 and c[0] < 200 and c[1] > c[0] + 20 and c[1] > c[2] + 20
zone_check("decoder Linear/Softmax green boxes", lgreen, 1540, 290, 1740, 420, 200)
pink = lambda c: c[0] > 200 and 130 < c[1] < 210 and 150 < c[2] < 225
zone_check("left Mask (opt.) pink", pink, 140, 730, 330, 810, 150)
zone_check("left lavender MatMul", lambda c: abs(c[0]-197) < 40 and abs(c[1]-202) < 40 and abs(c[2]-233) < 40, 150, 880, 380, 950, 150)

# 4) x-h ink present near stack right (render zone)
dark = lambda c: sum(c) < 340
zone_check("x-h annotation ink", lambda c: (c[0] > 130 and c[1] < 90 and c[2] < 90) or sum(c) < 300, 990, 740, 1050, 810, 15)

# 5) q->Linear3 red arrow head (triangle) present
zone_check("q red arrow head", lambda c: c[0] > 150 and c[1] < 90 and c[2] < 90, 880, 870, 945, 935, 150)

# 6) line-spacing audit: explicit lineSpacing on multi-line boxes in build
src = open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/slide_041.js").read()
import re
multi = re.findall(r'"([^"\\]*\\n[^"\\]*)"', src)
print(f"line-spacing: {len(multi)} multi-line string literals; explicit lineSpacing occurrences: {src.count('lineSpacing')}")

print("RESULT:", "ALL CHECKS PASS" if ok else "CHECKS FAILED")
