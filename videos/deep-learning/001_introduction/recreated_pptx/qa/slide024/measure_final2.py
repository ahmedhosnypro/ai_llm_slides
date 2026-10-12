#!/usr/bin/env python3
"""Round 4: ring count before col5, line colors, port dots, arrow fills, error text."""
from PIL import Image
import numpy as np
from collections import Counter

IM = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/unique_slides/slide_024.jpg").convert("RGB")
A = np.asarray(IM).astype(int)
r, g, b = A[:, :, 0], A[:, :, 1], A[:, :, 2]
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); OUT.append(s); print(s)

def modal(x0, x1, y0, y1, mask):
    ys, xs = np.where(mask[y0:y1, x0:x1])
    cols = [tuple(A[y0 + y, x0 + x]) for y, x in zip(ys, xs)]
    return Counter(cols).most_common(3)

# 1. high-zoom ring crop before col5 (row1) and after col1 (row1)
IM.crop((605, 198, 662, 228)).resize((57 * 8, 30 * 8), Image.LANCZOS).save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/z_rings_pre5_r1.png")
IM.crop((188, 198, 245, 228)).resize((57 * 8, 30 * 8), Image.LANCZOS).save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/z_rings_post1_r1.png")

# 2. mesh line color: sample the r1->r1 line y212..213 between col2 (281) and col3 (405)
redm = (r > 130) & (g < 110) & (b < 110)
P("mesh 23 r1r1 red modal:", modal(285, 400, 210, 216, redm))
P("mesh 34 r1r1 red modal:", modal(452, 565, 210, 216, redm))
# skip line through gap? scan a horizontal cut at y=250 (between rows) for red
for yy in (232, 250, 268):
    xs = [x for x in range(285, 400) if redm[yy, x]]
    P(f"gap23 y{yy} red xs:", xs[:40])
for yy in (232, 250, 268):
    xs = [x for x in range(452, 565) if redm[yy, x]]
    P(f"gap34 y{yy} red xs:", xs[:40])

# 3. col1->col2 connector + fan line colors (gray-ish on beige)
P("col1-col2 link modal (x185..240,y210..214):", modal(185, 240, 208, 216, (r + g + b < 560)))
P("fan line modal (x88..140,y250..320):", modal(88, 140, 250, 320, (r + g + b < 560)))

# 4. port dots: red clusters at col2 left/right edges, col3 left/right, col4 left/right
for tag, (x0, x1) in (("col2L", (238, 248)), ("col2R", (275, 285)), ("col3L", (403, 413)),
                      ("col3R", (441, 451)), ("col4L", (566, 576)), ("col4R", (604, 614)),
                      ("col5L", (656, 666))):
    m = redm[195:230, x0:x1]
    ys, xs = np.where(m)
    if len(ys):
        P(f"port {tag}: n={len(ys)} x {x0+xs.min()}..{x0+xs.max()} y {195+ys.min()}..{195+ys.max()} color", Counter(tuple(A[195+y, x0+x]) for y, x in zip(ys, xs)).most_common(1))
    else:
        P(f"port {tag}: none")

# 5. arrow fills (block arrows y388..433): modal saturated color in core
for tag, (x0, x1) in (("i", (245, 285)), ("j", (410, 450)), ("k", (570, 610))):
    zone = A[395:425, x0:x1].reshape(-1, 3)
    sat = zone[(zone.max(axis=1) - zone.min(axis=1) > 40)]
    P(f"arrow {tag} sat modal:", Counter(map(tuple, sat)).most_common(3))

# 6. error text core: brightest pixels in bar x800..816
zone = A[190:390, 799:817]
bright = zone[(zone[:, :, 0] > 200)]
P("error-bar R>200 modal:", Counter(map(tuple, bright)).most_common(4))
# check if text has green channel high (white text) 
whiteish = zone[(zone[:, :, 0] > 200) & (zone[:, :, 1] > 150)]
P("error-bar R>200&G>150 count:", len(whiteish))
redtxt = zone[(zone[:, :, 0] > 200) & (zone[:, :, 1] < 120) & (zone[:, :, 2] < 120)]
P("error-bar pure-red count:", len(redtxt), "modal:", Counter(map(tuple, redtxt)).most_common(2))

# 7. class box border color: dark px on box perimeter (box r1: x826..889 y205..220)
darkm = (r + g + b < 330)
P("class border modal:", modal(824, 892, 203, 222, darkm))

# 8. output box border/text: box r1 white fill x726..804 y203..222?
P("output r1 white modal:", modal(730, 800, 206, 220, (r > 235) & (g > 235) & (b > 235)))
darkm2 = (r + g + b < 300)
P("output r1 dark modal:", modal(722, 808, 200, 226, darkm2))

# 9. callout fills + borders
P("callout prev fill modal:", modal(230, 300, 432, 455, (b - r > 8)))
P("callout cur fill modal:", modal(395, 465, 432, 455, (g - r > 25)))
P("callout nxt fill modal:", modal(570, 625, 432, 455, (r - b > 25)))

# 10. magenta box fill/border + dashed line color
P("magenta box fill modal:", modal(70, 135, 130, 152, (r - g > 60)))
P("dash line modal:", modal(200, 800, 138, 144, (r - g > 50)))

# 11. panel bbox tight (beige DAD0C4 +-10)
beige = (abs(r - 0xDA) < 10) & (abs(g - 0xD0) < 10) & (abs(b - 0xC4) < 10)
# largest connected-ish: restrict to y>150
seg = beige[150:470, :]
ys, xs = np.where(seg)
P("panel bbox (y>150): x", xs.min(), xs.max(), "y", 150 + ys.min(), 150 + ys.max())

# 12. title bbox tight (red text y60..95)
redt = (r - g > 70) & (r - b > 70) & (r > 120)
seg = redt[55:100, 200:760]
ys, xs = np.where(seg)
P("title bbox: x", 200 + xs.min(), 200 + xs.max(), "y", 55 + ys.min(), 55 + ys.max())

# 13. neuron ring border colors per column (sample circle edge)
for tag, (cx, cy) in (("col1", (163, 212)), ("col2", (261, 212)), ("col3", (426, 212)),
                      ("col4", (589, 212)), ("col5", (677, 212))):
    band = A[cy - 21:cy + 21, cx - 21:cx + 21].reshape(-1, 3)
    edge = band[(band.max(axis=1) - band.min(axis=1) > 45)]
    P(f"neuron {tag} saturated modal:", Counter(map(tuple, edge)).most_common(2))
    fill = band[(band.max(axis=1) - band.min(axis=1) < 30) & (band.sum(axis=1) > 400)]
    P(f"neuron {tag} fill modal:", Counter(map(tuple, fill)).most_common(2))

with open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction/recreated_pptx/qa/slide024/measure_final2_out.txt", "w") as f:
    f.write("\n".join(OUT) + "\n")
