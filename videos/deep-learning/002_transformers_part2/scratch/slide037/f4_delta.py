# f4: comprehensive delta measurement on 002:37 frame (frame px), converted to build pt.
# Fit (f3): frame = 21.15 + 0.95635*bx ; 2.00 + 0.95695*by  => build = (frame-off)/scale.
from PIL import Image
import numpy as np
import json

A, B, C, D = 21.15, 0.95635, 2.00, 0.95695
def to_build(fx, fy):
    return (fx - A)/B, (fy - C)/D

img = np.asarray(Image.open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_037.jpg').convert('RGB')).astype(int)
H, W, _ = img.shape
out = {}

def bbox(mask, x0=0, x1=W, y0=0, y1=H):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0: return None
    return [int(x0+xs.min()), int(y0+ys.min()), int(x0+xs.max()), int(y0+ys.max()), int(len(xs))]

def pr(name, bb, note=""):
    if bb is None:
        print(f"{name}: EMPTY {note}")
        return
    bx0, by0 = to_build(bb[0], bb[1]); bx1, by1 = to_build(bb[2], bb[3])
    print(f"{name}: frame x{bb[0]}-{bb[2]} y{bb[1]}-{bb[3]} n={bb[4]}  -> build x{bx0:.1f}-{bx1:.1f} y{by0:.1f}-{by1:.1f} {note}")
    out[name] = {"frame": bb[:4], "build": [round(bx0,1), round(by0,1), round(bx1,1), round(by1,1)], "n": bb[4]}

# ---- 1. TITLE: red ink full width (exclude badge x>840)
red = ((img[...,0] > 140) & (img[...,1] < 95) & (img[...,2] < 95))
tb = bbox(red, 60, 840, 40, 100)
pr("title_ink", tb)
# row bands + column word gaps
sub = red[40:100, 60:840]
rows = sub.sum(axis=1)
bands = []
s = None
for i, v in enumerate(rows):
    if v > 2 and s is None: s = i
    elif v <= 2 and s is not None: bands.append((s+40, i-1+40)); s = None
if s is not None: bands.append((s+40, 99))
print("title row bands:", bands)
if tb:
    cols = red[tb[1]:tb[3]+1, :].sum(axis=0)
    gaps = []
    inglyph = False
    for x in range(tb[0], tb[2]+1):
        if cols[x] > 0 and not inglyph: inglyph = True; gs = x
        elif cols[x] == 0 and inglyph:
            inglyph = False
            if x - 1 - gs >= 0: gaps.append((gs, x-1))
    # merge glyphs into words with gap>7
    words = []
    for g0, g1 in gaps:
        if words and g0 - words[-1][1] <= 7: words[-1][1] = g1
        else: words.append([g0, g1])
    print("title word spans (frame x):", words)
    out["title_words"] = words

# ---- 2. LEGENDS present? sample the legend1 zone fill (build 141-342 x 102-130)
lx0, ly0 = int(A + B*141), int(C + D*102)
lx1, ly1 = int(A + B*342), int(C + D*130)
zone = img[ly0+3:ly1-3, lx0+3:lx1-3].reshape(-1, 3)
from collections import Counter
mc = Counter(map(tuple, zone)).most_common(3)
print("legend1 zone mode colors:", mc)
out["legend1_mode"] = mc[0][0]
# cyan fill check C8FCFC=(200,252,252)
cyan = (np.abs(img - np.array([200, 252, 252])).sum(axis=2) < 60)
pr("legend_cyan_all", bbox(cyan, 100, 560, 80, 220))

# ---- 3. PIN: strong red blob upper area
strongred = ((img[...,0] > 150) & (img[...,1] < 70) & (img[...,2] < 80))
pb = bbox(strongred, 560, 780, 120, 300)
pr("pin_red", pb)
# pin white text
wt = (img[...,0] > 235) & (img[...,1] > 235) & (img[...,2] > 235)
wb = bbox(wt, 590, 720, 150, 240)
pr("pin_white_text", wb)

# ---- 4. RED DISC near (678,352): solid red
disc = bbox(strongred, 640, 720, 320, 390)
pr("red_disc", disc)

# ---- 5. RED DASHED ROUNDED BOX around encoder stack (p1: encloses A&N/FF/A&N/MHA)
# scan for red dashed strokes in x590-740 y240-420 excluding disc/pin
dashzone = red.copy()
dashzone[:115, :] = False; dashzone[430:, :] = False
dashzone[:, :585] = False; dashzone[:, 785:] = False
# remove solid pin/disc cores: erode by checking neighbors
print("red dash px in x585-785 y115-430:", int(dashzone.sum()))

# ---- 6. FUNNEL DASHES: red thin strokes between insets and arch
# region A: from insetA right edge (x~203) to arch (x~570), y 200-500
fb = bbox(red, 205, 565, 190, 510)
pr("funnel_left_zone", fb)
# region B: from insetB right edge (x~509) to arch left border (x~568)
fb2 = bbox(red, 512, 566, 190, 510)
pr("funnel_mid_zone", fb2)
# per-row red runs in x205-565 (dash segments)
rows_red = {}
for y in range(190, 510):
    xs = np.where(red[y, 205:565])[0]
    if len(xs) >= 2:
        rows_red[y] = [int(xs.min()+205), int(xs.max()+205), int(len(xs))]
print("funnel rows (y: xmin-xmax n) sample:", {k: rows_red[k] for k in sorted(rows_red)[:40]})
out["funnel_rows"] = rows_red

# ---- 7. DECODER chevrons/shafts: navy pixels (build chevrons zone-1/2/3)
navy = (np.abs(img - np.array([5, 0, 143])).sum(axis=2) < 120)
nb = bbox(navy, 740, 840, 170, 350)
pr("navy_chevrons", nb)
navy_rows = {}
for y in range(170, 350):
    xs = np.where(navy[y, 740:840])[0]
    if len(xs) >= 2: navy_rows[y] = [int(xs.min()+740), int(xs.max()+740), int(len(xs))]
print("navy rows:", navy_rows)
out["navy_rows"] = navy_rows
# gap shafts: dark thin vertical at x~771-773 (build 785) in gap bands
for g0, g1, lbl in [(184, 202, "gap1"), (238, 257, "gap2")]:
    seg = img[g0:g1, 768:776]
    dark = (seg.sum(axis=2) < 3*120).sum()
    print(f"{lbl} shaft dark px in x768-776 y{g0}-{g1}:", int(dark))
    out[lbl] = int(dark)

# ---- 8. enc V circle green zone
grn = (np.abs(img - np.array([85, 160, 33])).sum(axis=2) < 130) | (np.abs(img - np.array([140, 203, 44])).sum(axis=2) < 120)
gb = bbox(grn, 600, 700, 380, 420)
pr("encV_green", gb)

# ---- 9. red dashed rounded box: trace red rows x585-785 y240-430
rz = {}
for y in range(235, 432):
    xs = np.where(red[y, 585:785])[0]
    if len(xs) >= 2: rz[y] = [int(xs.min()+585), int(xs.max()+585), int(len(xs))]
print("arch red rows (x585-785):", rz)
out["arch_red_rows"] = rz

with open('/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/scratch/slide037/f4_delta_out.json', 'w') as f:
    json.dump(out, f, indent=1)
print("saved f4_delta_out.json")
