# Forensics pass 5: fine details for the build.
from PIL import Image
import json
from collections import Counter

BASE = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_introduction'
im = Image.open(f'{BASE}/unique_slides/slide_037.jpg').convert('RGB')
im36 = Image.open(f'{BASE}/unique_slides/slide_036.jpg').convert('RGB')
W, H = im.size
px = im.load()
px36 = im36.load()
out = {}

# 1) title ink x-extent excluding artifact cols 54..68
xs = []
for x in range(70, 916):
    for y in range(76, 116):
        p = px[x, y]
        if p[0] > 120 and p[1] < 110 and p[2] < 110 and p[0] > p[1] + 40:
            xs.append(x); break
out['title_x'] = dict(x0=min(xs), x1=max(xs)) if xs else None
# title modal color
c = Counter()
for y in range(80, 112):
    for x in range(70, 850):
        p = px[x, y]
        if p[0] > 120 and p[1] < 110 and p[2] < 110 and p[0] > p[1] + 40:
            c[p] += 1
out['title_modal'] = c.most_common(3)

# 2) yellow box: line x-extents + border colors
lines = [(148, 175), (182, 202), (214, 240)]
lx = []
for (y0, y1) in lines:
    xs2 = []
    for x in range(60, 910):
        for y in range(y0, y1):
            if sum(px[x, y]) < 300:
                xs2.append(x); break
    lx.append((min(xs2), max(xs2)) if xs2 else None)
out['yellow_line_x'] = lx
cb = Counter()
for x in range(100, 880):
    for y in (136, 137):
        p = px[x, y]
        if sum(p) < 640: cb[p] += 1
out['ybox_top_border_modal'] = cb.most_common(3)
cb2 = Counter()
for x in range(100, 880):
    for y in (243, 244):
        p = px[x, y]
        if sum(p) < 640: cb2[p] += 1
out['ybox_bot_border_modal'] = cb2.most_common(3)
# fill modal
cf = Counter()
for y in range(140, 240, 2):
    for x in range(80, 890, 2):
        cf[px[x, y]] += 1
out['ybox_fill_modal'] = cf.most_common(2)
# right border cols
rb = []
for x in range(895, 912):
    dark = sum(1 for y in range(150, 230) if sum(px[x, y]) < 640)
    if dark > 10: rb.append((x, dark))
out['ybox_right_border'] = rb
lb = []
for x in range(58, 70):
    dark = sum(1 for y in range(150, 230) if sum(px[x, y]) < 640)
    if dark > 10: lb.append((x, dark))
out['ybox_left_border'] = lb

# 3) '3 dims' label: red vs black in x50..180, y280..430
reds = []; blacks = []
for y in range(280, 430):
    for x in range(50, 178):
        p = px[x, y]
        if p[0] > 120 and p[1] < 110 and p[2] < 110 and p[0] > p[1] + 40: reds.append((x, y))
        elif sum(p) < 260: blacks.append((x, y))
if reds:
    xs3 = [a for a, b in reds]; ys3 = [b for a, b in reds]
    out['threedims_red'] = dict(x0=min(xs3), x1=max(xs3), y0=min(ys3), y1=max(ys3), n=len(reds))
if blacks:
    xs4 = [a for a, b in blacks]; ys4 = [b for a, b in blacks]
    out['threedims_black'] = dict(x0=min(xs4), x1=max(xs4), y0=min(ys4), y1=max(ys4), n=len(blacks))

# 4) '5' above stack: black ink x340..520, y280..302
pts = []
for y in range(278, 304):
    for x in range(340, 520):
        if sum(px[x, y]) < 260: pts.append((x, y))
if pts:
    xs5 = [a for a, b in pts]; ys5 = [b for a, b in pts]
    out['five_label'] = dict(x0=min(xs5), x1=max(xs5), y0=min(ys5), y1=max(ys5), n=len(pts))
else:
    out['five_label'] = None

# 5) '3' below stack: black ink x330..480, y391..430
pts = []
for y in range(391, 432):
    for x in range(300, 500):
        if sum(px[x, y]) < 260: pts.append((x, y))
if pts:
    xs6 = [a for a, b in pts]; ys6 = [b for a, b in pts]
    out['three_label'] = dict(x0=min(xs6), x1=max(xs6), y0=min(ys6), y1=max(ys6), n=len(pts))
else:
    out['three_label'] = None

# 6) '=' bars: cyan 3EAEC6-ish (90<r<200, g 150-230, b 150-230, b>r) in x480..525, y330..380
pts = []
for y in range(330, 380):
    for x in range(478, 528):
        p = px[x, y]
        if 80 < p[0] < 210 and 140 < p[1] < 235 and 140 < p[2] < 240 and p[2] >= p[0] + 20: pts.append((x, y))
if pts:
    xs7 = [a for a, b in pts]; ys7 = [b for a, b in pts]
    out['equals_cyan'] = dict(x0=min(xs7), x1=max(xs7), y0=min(ys7), y1=max(ys7), n=len(pts))
    ccc = Counter(px[a, b] for a, b in pts)
    out['equals_modal'] = ccc.most_common(3)
else:
    out['equals_cyan'] = None

# 7) cube bottom stroke + right edge
# bottom: dark-ish rows in x540..760, y440..460
br = {}
for y in range(440, 462):
    cnt = sum(1 for x in range(540, 760) if sum(px[x, y]) < 560)
    if cnt > 10: br[y] = cnt
out['cube_bottom_rows'] = br
rr2 = {}
for x in range(775, 800):
    cnt = sum(1 for y in range(300, 440) if sum(px[x, y]) < 560)
    if cnt > 10: rr2[x] = cnt
out['cube_right_cols'] = rr2

# 8) equation color modal + exact bbox
ep = []
for y in range(474, 500):
    for x in range(100, 500):
        p = px[x, y]
        if p[0] > 110 and p[1] < 95 and p[2] < 95 and p[0] > p[1] + 50: ep.append((x, y))
if ep:
    xs8 = [a for a, b in ep]; ys8 = [b for a, b in ep]
    out['eq_bbox'] = dict(x0=min(xs8), x1=max(xs8), y0=min(ys8), y1=max(ys8), n=len(ep))
    ce = Counter(px[a, b] for a, b in ep)
    out['eq_modal'] = ce.most_common(4)

# 9) question exact bbox
qp = []
for y in range(448, 484):
    for x in range(60, 640):
        if sum(px[x, y]) < 260: qp.append((x, y))
xs9 = [a for a, b in qp]; ys9 = [b for a, b in qp]
out['question_bbox'] = dict(x0=min(xs9), x1=max(xs9), y0=min(ys9), y1=max(ys9), n=len(qp))

# 10) artifact check: frame 36 columns x56..68 and x894..898 over y270..505
def colcount(img_px, x, y0, y1):
    return sum(1 for y in range(y0, y1) if (lambda p: p[0] > 110 and p[1] < 90 and p[2] < 100)(img_px[x, y]))
out['f37_x58'] = colcount(px, 58, 270, 505)
out['f37_x65'] = colcount(px, 65, 270, 505)
out['f36_x58'] = colcount(px36, 58, 270, 505)
out['f36_x65'] = colcount(px36, 65, 270, 505)
out['f37_x896'] = colcount(px, 896, 270, 505)
out['f36_x896'] = colcount(px36, 896, 270, 505)
# what does f36 have at those x? (its own box was x110..839)
out['f36_x58_probe'] = {y: list(px36[58, y]) for y in [300, 400]}
out['f37_x58_probe'] = {y: list(px[58, y]) for y in [300, 400]}
out['f37_x65_probe'] = {y: list(px[65, y]) for y in [300, 400]}
out['f37_x64_66'] = {x: [list(px[x, 350]), list(px[x, 400])] for x in [63, 64, 65, 66, 67]}

# 11) slab strokes bbox (crop safety): any non-white ink in x150..300, y264..450
pts = []
for y in range(264, 452):
    for x in range(140, 310):
        if sum(px[x, y]) < 700: pts.append((x, y))
xs11 = [a for a, b in pts]; ys11 = [b for a, b in pts]
out['slab_ink_bbox'] = dict(x0=min(xs11), x1=max(xs11), y0=min(ys11), y1=max(ys11), n=len(pts))

# 12) cube/panel right region ink bbox x780..900, y264..452
pts = []
for y in range(264, 452):
    for x in range(780, 896):
        if sum(px[x, y]) < 700: pts.append((x, y))
xs12 = [a for a, b in pts]; ys12 = [b for a, b in pts]
out['right_ink_bbox'] = dict(x0=min(xs12), x1=max(xs12), y0=min(ys12), y1=max(ys12), n=len(pts)) if pts else None

# 13) Depth label bbox: ink x700..895, y264..320
pts = []
for y in range(264, 322):
    for x in range(690, 896):
        if sum(px[x, y]) < 400: pts.append((x, y))
if pts:
    xs13 = [a for a, b in pts]; ys13 = [b for a, b in pts]
    out['depth_label'] = dict(x0=min(xs13), x1=max(xs13), y0=min(ys13), y1=max(ys13), n=len(pts))

print(json.dumps(out, indent=0, default=str))
