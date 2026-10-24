"""Slide 019 — judge-r4: re-cut Procedure B crop pairs from the current render.

Method (per judge_protocol_03.md Procedure B, matched effective scale):
  sx = W_render/960, sy = H_render/540
  render crop box = (round(x0*sx), round(y0*sy), round(x1*sx), round(y1*sy))
  original crop = frame bbox (x0,y0,x1,y1) LANCZOS-upscaled to the SAME size
Writes qa/slide019/q_r4_<name>_<side>.png and diffs against the banked crop_7_*.
"""

import sys
from PIL import Image

Q = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
V = "videos/machine-learning/03_ridger_regression_gradient_descent"
RENDER = Q + "/render_7.png"
ORIG = V + "/unique_slides/slide_019.jpg"

REGIONS = [
    ("noreg_rows", 124, 199, 380, 485),
    ("table_right", 400, 157, 904, 530),
    ("table_left", 58, 157, 480, 360),
]

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
sx = r.size[0] / o.size[0]
sy = r.size[1] / o.size[1]

for name, x0, y0, x1, y1 in REGIONS:
    box = (round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy))
    size = (box[2] - box[0], box[3] - box[1])

    rc = r.crop(box)
    oc = o.crop((x0, y0, x1, y1)).resize(size, Image.LANCZOS)

    rc.save("%s/q_r4_%s_render.png" % (Q, name))
    oc.save("%s/q_r4_%s_orig.png" % (Q, name))

    br = Image.open("%s/crop_7_%s_render.png" % (Q, name)).convert("RGB")
    bo = Image.open("%s/crop_7_%s_orig.png" % (Q, name)).convert("RGB")

    dr = db = 0
    same_size = br.size == rc.size and bo.size == oc.size
    if same_size:
        dr = list(rc.getdata())
        db = list(br.getdata())
        dr = sum(1 for a, b in zip(dr, db) if a != b)
        dr2 = list(oc.getdata())
        db2 = list(bo.getdata())
        db = sum(1 for a, b in zip(dr2, db2) if a != b)
    print(
        "%-12s bbox=%s  fresh=%s banked=%s  size_ok=%s  diff render=%d orig=%d"
        % (name, (x0, y0, x1, y1), size, br.size, same_size, dr, db)
    )
    sys.stdout.flush()
