#!/usr/bin/env python3
"""Phase 2: content structure of slide_020.jpg — rows, boxes, dots, banner, arrows.
Frame coords (960x540). Mapping to slide pts: sx=(fx-18.63)/0.96123, sy=fy/0.95556."""
from PIL import Image
import json

SRC = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_020.jpg"
img = Image.open(SRC).convert("RGB")
W, H = img.size
px = img.load()
out = {}

def near(p, c, tol=45):
    return all(abs(p[i] - c[i]) <= tol for i in range(3))

def bbox(pred, x0, x1, y0, y1):
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if pred(px[x, y])]
    if not pts:
        return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]

RED = (192, 0, 0)
GREEN = (0, 165, 80)
BLUE = (51, 51, 204)

# row container bands: fills
FILLS = {
    "row1_fill": (251, 234, 234),   # FBEAEA
    "row2_fill": (232, 245, 233),   # E8F5E9
    "row3_fill": (204, 204, 242),   # CCCCF2
    "row4_fill": (251, 234, 234),   # FBEAEA
}
for name, c in FILLS.items():
    y0 = {"row1_fill": 80, "row2_fill": 130, "row3_fill": 190, "row4_fill": 340}[name]
    y1 = {"row1_fill": 140, "row2_fill": 200, "row3_fill": 260, "row4_fill": 410}[name]
    out[name] = bbox(lambda p, c=c: near(p, c, 12), 62, 900, y0, y1)

# border colors per row (dashed containers)
BORDERS = {"row1_border": RED, "row2_border": GREEN, "row3_border": BLUE, "row4_border": RED}
YBANDS = {"row1_border": (80, 140), "row2_border": (130, 200), "row3_border": (190, 265), "row4_border": (340, 410)}
for name, c in BORDERS.items():
    y0, y1 = YBANDS[name]
    out[name] = bbox(lambda p, c=c: near(p, c, 60), 62, 900, y0, y1)

# banner: dark red 990000-ish
out["banner_fill_bbox"] = bbox(lambda p: near(p, (153, 0, 0), 40), 62, 900, 275, 345)
# arrows: saturated red blocks between rows
out["arrow1"] = bbox(lambda p: near(p, RED, 60), 570, 660, 190, 300)   # x~64%
out["arrow2"] = bbox(lambda p: near(p, RED, 60), 660, 740, 245, 300)   # x~74%
out["arrow3"] = bbox(lambda p: near(p, RED, 60), 460, 550, 320, 360)   # x~54%
out["arrow4"] = bbox(lambda p: near(p, RED, 60), 460, 550, 395, 465)   # x~54% below brace
# brace: red ink band y 400..430
out["brace"] = bbox(lambda p: near(p, RED, 70), 62, 900, 398, 435)
# caption: blue text y 450..480
out["caption"] = bbox(lambda p: near(p, (34, 34, 204), 60), 300, 700, 445, 485)
# inset: green border box bottom-left
out["inset_border"] = bbox(lambda p: near(p, (0, 128, 0), 60), 30, 220, 400, 520)
out["inset_pinkbox"] = bbox(lambda p: near(p, (244, 184, 208), 30), 40, 220, 410, 520)
# delta symbols: red text y 255..278 x 100..880
out["delta_band"] = bbox(lambda p: near(p, RED, 70), 100, 890, 252, 285)
# lightning bolts: orange FFA500
out["bolts_band"] = bbox(lambda p: near(p, (255, 165, 0), 55), 62, 900, 230, 275)

def s(box):
    if not box:
        return None
    sx0 = (box[0] - 18.63) / 0.96123; sy0 = box[1] / 0.95556
    sx1 = (box[2] - 18.63) / 0.96123; sy1 = box[3] / 0.95556
    return {"frame": box, "slide": [round(sx0, 1), round(sy0, 1), round(sx1, 1), round(sy1, 1)],
            "w_pt": round(sx1 - sx0, 1), "h_pt": round(sy1 - sy0, 1)}

out["slide_coords"] = {k: s(v) for k, v in out.items() if isinstance(v, list)}
print(json.dumps(out, indent=1))
