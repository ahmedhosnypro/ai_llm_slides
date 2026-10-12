#!/usr/bin/env python3
"""Element bbox refinement on the slide-coords resample. For each element: mask by
color family within an approximate zone, report tight bbox + row/col profiles.
"""
from PIL import Image
import json

img = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide015/frame_in_slide_coords.png").convert("RGB")
W, H = img.size
px = img.load()

def near(p, c, tol):
    return abs(p[0]-c[0]) <= tol and abs(p[1]-c[1]) <= tol and abs(p[2]-c[2]) <= tol

def bbox_mask(pred, x0, y0, x1, y1, label):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if pred(px[x, y])]
    if not pts:
        return {"label": label, "bbox": None, "n": 0}
    bb = (min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts))
    # column profile (per-x y-extent) sampled
    cols = {}
    for (x, y) in pts:
        c = cols.setdefault(x, [y, y])
        c[0] = min(c[0], y); c[1] = max(c[1], y)
    xs = sorted(cols)
    step = max(1, len(xs) // 12)
    prof = {str(x): cols[x] for x in xs[::step]}
    rows = {}
    for (x, y) in pts:
        r = rows.setdefault(y, [x, x])
        r[0] = min(r[0], x); r[1] = max(r[1], x)
    ys = sorted(rows)
    rstep = max(1, len(ys) // 12)
    rprof = {str(y): rows[y] for y in ys[::rstep]}
    return {"label": label, "bbox": bb, "n": len(pts), "col_profile": prof, "row_profile": rprof}

out = []

# orange ellipses (two fills) in zone x80..240, y200..400
out.append(bbox_mask(lambda p: near(p, (243, 129, 75), 30) or near(p, (192, 100, 45), 38), 80, 195, 245, 400, "orange_ellipses"))
# green ellipse zone x175..250, y235..340
out.append(bbox_mask(lambda p: near(p, (130, 214, 139), 34) or near(p, (95, 190, 110), 38), 170, 230, 255, 345, "green_ellipse"))
# W_k green boxes (6CBB45) zone x150..200, y230..345
out.append(bbox_mask(lambda p: near(p, (108, 187, 69), 40), 150, 230, 200, 350, "wk_boxes"))
# Dot Product tan box zone x220..300, y200..360
out.append(bbox_mask(lambda p: near(p, (216, 202, 186), 16), 215, 195, 305, 365, "dotproduct_box"))
# Scaling pill pink F6C6CC zone x305..345, y200..365
out.append(bbox_mask(lambda p: near(p, (246, 198, 204), 22), 300, 195, 350, 370, "scaling_pill"))
# Softmax pill F2BCE4 zone x355..400, y200..365
out.append(bbox_mask(lambda p: near(p, (242, 188, 228), 22), 350, 195, 400, 370, "softmax_pill"))
# Sigma box (aliceblue + blue border) zone x395..510, y200..240
out.append(bbox_mask(lambda p: near(p, (220, 243, 243), 24), 395, 198, 515, 245, "sigma_box"))
# multiply nodes: red rings zone x400..500, y235..350
out.append(bbox_mask(lambda p: (p[0] > 150 and p[0]-p[1] > 70 and p[0]-p[2] > 70), 400, 230, 500, 355, "mult_nodes_red"))
# V strips gold zone x500..540, y230..350
out.append(bbox_mask(lambda p: near(p, (250, 216, 130), 34), 495, 225, 545, 355, "v_strips"))
# W_v cyan boxes zone x530..570, y230..360
out.append(bbox_mask(lambda p: near(p, (170, 220, 240), 40), 528, 225, 575, 365, "wv_boxes"))
# blue dots zone x235..295, y235..345
out.append(bbox_mask(lambda p: near(p, (43, 75, 208), 60), 230, 230, 300, 350, "blue_dots"))
# climbing boxes fills
out.append(bbox_mask(lambda p: near(p, (192, 83, 16), 40), 400, 140, 500, 180, "climb_rust"))
out.append(bbox_mask(lambda p: near(p, (90, 90, 90), 26), 455, 125, 545, 160, "climb_gray"))
out.append(bbox_mask(lambda p: near(p, (255, 255, 0), 40), 490, 105, 595, 140, "climb_yellow"))
out.append(bbox_mask(lambda p: near(p, (144, 238, 144), 40), 535, 85, 635, 118, "climb_lgreen"))
out.append(bbox_mask(lambda p: near(p, (245, 203, 160), 30), 580, 65, 680, 98, "climb_tan"))
# h ovals: black masks per zone
for name, (x0, y0, x1, y1) in {
    "oval_h1": (590, 182, 645, 212), "oval_h2": (640, 160, 695, 195),
    "oval_h3": (685, 138, 740, 172), "oval_h4": (728, 118, 782, 152),
    "oval_h5": (770, 98, 825, 132)}.items():
    out.append(bbox_mask(lambda p: sum(p) < 160, x0, y0, x1, y1, name))
# title ink zone
out.append(bbox_mask(lambda p: sum(p) < 330, 300, 470, 700, 512, "title_ink"))
out.append(bbox_mask(lambda p: (p[0] > 140 and p[0]-p[1] > 60 and p[0]-p[2] > 60 and sum(p) < 480), 300, 470, 700, 512, "title_red_ink"))
# plane over white: gray 195..225 low chroma, zone x100..470, y60..230
out.append(bbox_mask(lambda p: max(abs(p[0]-p[1]), abs(p[1]-p[2]), abs(p[0]-p[2])) < 16 and 192 <= (p[0]+p[1]+p[2])//3 <= 226, 100, 60, 470, 235, "plane_over_white"))
# swoosh red zone x560..850, y220..390
out.append(bbox_mask(lambda p: (p[0] > 150 and p[0]-p[1] > 70 and p[0]-p[2] > 70), 555, 215, 860, 400, "swoosh_red"))
# query row container green dashed zone x165..400, y395..440
out.append(bbox_mask(lambda p: near(p, (0, 176, 80), 60), 160, 390, 410, 445, "query_container_green"))
# X2 highlight magenta zone x225..295, y400..435
out.append(bbox_mask(lambda p: (p[0] > 190 and p[2] > 150 and p[1] < 140), 220, 395, 300, 440, "x2_magenta"))

print(json.dumps(out, indent=1, default=str))
