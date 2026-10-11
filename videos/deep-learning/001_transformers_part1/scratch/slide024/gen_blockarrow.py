# Generate the hatched right block-arrow as a transparent PNG (600 dpi).
# Measured from the original frame (72dpi px): total bbox x[518,681] y[281,316]
# -> 164x36 px -> at 600dpi: 1367x300 px. Body y[283,314] (rel 2..33 of 36),
# head base x=644 (rel 126), tip x=681 (rel 163). Hatch: ~1pt red-ish diagonal
# lines, pitch ~18.5px(72dpi), on near-white pink bg; outline EE0000 ~1.5pt.
from PIL import Image, ImageDraw
import json

DPI = 600
S = DPI / 72.0  # 8.333 px per 72dpi px
W = round(164 * S)   # 1367
H = round(36 * S)    # 300

BODY_T = round(2 * S)     # rel y of body top
BODY_B = round(33.5 * S)  # rel y of body bottom
HEAD_BASE_X = round(127 * S)  # rel x where head triangle starts
TIP_X = W - round(1 * S)

im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(im)

# arrow polygon (PowerPoint rightArrow geometry)
poly = [
    (0, BODY_T), (HEAD_BASE_X, BODY_T), (HEAD_BASE_X, 0),
    (TIP_X, H / 2), (HEAD_BASE_X, H), (HEAD_BASE_X, BODY_B), (0, BODY_B),
]
# background fill: near-white pink
d.polygon(poly, fill=(253, 238, 239, 255))

# diagonal hatch lines (45 deg, going down-right), pitch 18.5*72dpi-px
pitch = 18.5 * S
lw = max(2, round(1.1 * S))
hatch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hatch)
x = -H
while x < W + H:
    hd.line([(x, 0), (x + H, H)], fill=(194, 92, 104, 255), width=lw)
    x += pitch
# clip hatch to polygon via mask
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).polygon(poly, fill=255)
im.paste(hatch, (0, 0), Image.composite(hatch.split()[3], Image.new("L", (W, H), 0), mask))

# outline: red EE0000, ~1.5pt
ow = max(3, round(1.5 * S))
d.line(poly + [poly[0]], fill=(238, 0, 0, 255), width=ow, joint="curve")

out = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/build/assets/blockarrow_024.png"
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
im.save(out)
sidecar = {
    "file": out, "dpi": DPI, "px_w": W, "px_h": H,
    "w_in": W / DPI, "h_in": H / DPI,
    "mathtext": None, "note": "hatched right block arrow, slide 024",
}
with open(out.replace(".png", ".json"), "w") as f:
    json.dump(sidecar, f, indent=1)
print(json.dumps(sidecar))
