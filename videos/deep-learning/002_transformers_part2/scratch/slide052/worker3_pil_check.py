# Third-dispatch independent corroboration (v2, geometry-correct).
# Sample the SAME content point in both images:
#   slide-pt space (960x540, house chrome space) -> render px via *2000/960,
#   slide-pt space -> frame px via the measured 002 capture transform
#   (inverse of sx=(fx-18.63)/0.96123, sy=fy/0.95556).
# Corroboration only - never a substitute for the visual judge.
from PIL import Image
import statistics
orig = Image.open("unique_slides/slide_052.jpg").convert("RGB")
rend = Image.open("recreated_pptx/qa/slide052/render_5.png").convert("RGB")
SR = rend.width / 960.0          # slide-pt -> render px
def to_frame(sx, sy):            # slide-pt -> frame px (inverse chrome transform)
    return (sx * 0.96123 + 18.63, sy * 0.95556)
def mean_rgb(im, cx, cy, r=4):
    px = im.load()
    pts = [px[x, y] for x in range(int(round(cx))-r, int(round(cx))+r+1)
                      for y in range(int(round(cy))-r, int(round(cy))+r+1)]
    return tuple(round(statistics.mean(c[i] for c in pts)) for i in range(3))
regions = [  # (name, slide-pt x, y, expected approx hex)
    ("canvas white margin",        30, 250, "FFFFFF"),
    ("upper bar1 Residual 990000", 600, 120, "990000"),
    ("FFN bar green 00A800",       600, 155, "00A800"),
    ("upper bar3 Residual 990000", 600, 186, "990000"),
    ("encoder box 0010C8",         180, 360, "0010C8"),
    ("masked box1 0010C8",         360, 390, "0010C8"),
    ("purple bar 800080",          600, 445, "800080"),
    ("word box SOS C8E8C8",        350, 485, "C8E8C8"),
    ("legend box C8E8C8",          180, 500, "C8E8C8"),
    ("lower container fill",       412, 415, "FFE1EE-ish"),
]
print(f"render scale {SR:.4f} px/pt; frame transform inverse: fx=0.96123sx+18.63, fy=0.95556sy")
for name, sx, sy, exp in regions:
    fx, fy = to_frame(sx, sy)
    o = mean_rgb(orig, fx, fy)
    r = mean_rgb(rend, sx * SR, sy * SR)
    print(f"{name:28s} exp~{exp:12s} orig={o} render={r}")
