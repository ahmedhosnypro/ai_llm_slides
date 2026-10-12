#!/usr/bin/env python3
"""selfcheck_attempt_1: closed-loop PIL checks of render_1 (2001x1125 -> 960x540
slide coords) against frame11_slide.png. Delta regions + containment + eq ink."""
from PIL import Image, ImageChops
import json

SCR = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide011"
QA = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide011"
ren = Image.open(f"{QA}/render_1.png").convert("RGB").resize((960, 540), Image.LANCZOS)
frm = Image.open(f"{SCR}/frame11_slide.png").convert("RGB")
ren.save(f"{SCR}/render1_960.png")
rp, fp = ren.load(), frm.load()
out = {}
FAILED = []

def near(p, t, tol):
    return all(abs(p[i] - t[i]) <= tol for i in range(3))

def ink_bbox(px, x0, y0, x1, y1, thresh=690, exclude_gray=True):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1)
           if sum(px[x, y]) < thresh and not (exclude_gray and near(px[x, y], (233, 233, 231), 14))]
    if not pts: return None
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys), len(pts))

# 1) blue frame lines present in render (purple ~ (65,57,152) at tol 45)
for lbl, pts in (
    ("blue_left", [(57, y) for y in range(80, 500, 7)]),
    ("blue_right", [(879, y) for y in range(80, 500, 7)]),
):
    n = sum(1 for x, y in pts if rp[x, y][2] - rp[x, y][0] > 30 and rp[x, y][2] > 110)
    out[f"chk_blue_{lbl}"] = f"{n}/{len(pts)}"
    if n < len(pts) * 0.7: FAILED.append(f"blue {lbl}")
# blue top/bottom rows
for lbl, y0, y1 in (("top", 62, 69), ("bottom", 511, 518)):
    n = sum(1 for y in range(y0, y1) for x in range(70, 870, 9)
            if rp[x, y][2] - rp[x, y][0] > 30 and rp[x, y][2] > 110)
    out[f"chk_blue_{lbl}"] = n
    if n < 60: FAILED.append(f"blue {lbl}")

# 2) beam zone: bright yellow-green present (core ~ (250,249,95))
pts = [(x, y) for y in range(70, 175, 3) for x in range(420, 660, 3) if near(rp[x, y], (250, 249, 95), 34)]
out["chk_beam_core_px"] = len(pts)
if len(pts) < 300: FAILED.append("beam core")

# 3) chain boxes: cream/green/yellow dashed boxes + orange arrows
out["chk_chainA(590..665,72..85)"] = ink_bbox(rp, 585, 68, 670, 88, 740)
out["chk_chainB(546..622,91..108)"] = ink_bbox(rp, 541, 88, 627, 111, 740)
out["chk_orange_arrow_x629"] = sum(1 for y in range(85, 92) for x in range(626, 633) if near(rp[x, y], (232, 120, 48), 60))
out["chk_olive_box"] = ink_bbox(rp, 455, 129, 547, 160, 640)
out["chk_orange_box"] = ink_bbox(rp, 375, 181, 573, 208, 660)

# 4) left zone: mint container + W boxes + K labels
out["chk_left_container"] = ink_bbox(rp, 86, 228, 154, 350, 700)
out["chk_leftWboxes"] = ink_bbox(rp, 160, 232, 190, 342, 700)
out["chk_Klabels_red"] = sum(1 for y in range(255, 340) for x in range(210, 230)
                             if rp[x, y][0] > 130 and rp[x, y][0] - rp[x, y][1] > 60)

# 5) eq ink: fraction + rotated labels + K·q
out["chk_kq_label"] = ink_bbox(rp, 286, 208, 312, 230, 500)
out["chk_fraction"] = ink_bbox(rp, 342, 204, 364, 238, 500)
out["chk_scaling_rot"] = ink_bbox(rp, 316, 235, 333, 330, 520)
out["chk_softmax_rot"] = ink_bbox(rp, 372, 252, 384, 310, 520)

# 6) title ink
out["chk_title"] = ink_bbox(rp, 240, 470, 780, 516, 430)

# 7) q zone: strips + ellipses + arrow
out["chk_q_container"] = ink_bbox(rp, 170, 398, 395, 436, 720)
out["chk_blue_ellipse"] = sum(1 for y in range(370, 440, 2) for x in range(230, 285, 2)
                              if near(rp[x, y], (123, 159, 232), 55))
out["chk_q_downarrow"] = sum(1 for y in range(415, 438) for x in range(246, 255) if rp[x, y][0] > 150 and rp[x, y][0] - rp[x, y][1] > 90)

# 8) containment: content ink outside house panel (x42..918, y45..539)
viol = 0
for y in range(0, 540, 2):
    for x in range(0, 960, 2):
        inside_panel = 42 <= x <= 918 and 45 <= y <= 539
        if not inside_panel:
            p = rp[x, y]
            if sum(p) < 690 and not near(p, (233, 233, 231), 14) and not (x < 4 or x > 956 or y < 4 or y > 536):
                # white margin expected outside panel
                if not near(p, (255, 255, 255), 16):
                    viol += 1
out["chk_panel_containment_violations"] = viol
if viol > 40: FAILED.append("panel containment")

# 9) global diff map (render vs frame) 20px blocks — report worst zones (corroboration)
d = ImageChops.difference(ren, frm)
r, g, b = d.split()
mx = ImageChops.lighter(ImageChops.lighter(r, g), b)
dpx = mx.load()
blocks = []
for cy in range(0, 540, 20):
    for cx in range(0, 960, 20):
        n = t = 0
        for y in range(cy, min(cy + 20, 540), 2):
            for x in range(cx, min(cx + 20, 960), 2):
                t += 1
                if dpx[x, y] > 60: n += 1
        if n / t > 0.30: blocks.append((cx, cy, round(n / t, 2)))
out["diff_hot_blocks(>0.30)"] = sorted(blocks, key=lambda z: -z[2])[:24]

out["FAILED"] = FAILED
print(json.dumps(out, indent=1, default=str))
