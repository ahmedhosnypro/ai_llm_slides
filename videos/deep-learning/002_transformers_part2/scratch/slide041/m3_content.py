#!/usr/bin/env python3
"""m3_content.py — measure every content region of slide_041.jpg and map to true slide pts.

Fit (from m1/m2 chrome landmarks):
  left border frame 58.5 <-> slide 42 ; right 901 <-> 919 ; top 43 <-> 45 ; bottom 517 <-> 540
  slide_x = 42 + (fx-58.5)*877/842.5 ;  slide_y = 45 + (fy-43)*495/474
Badge cross-check: yellow-bbox center (875.5,71.0) -> slide (892.4, 74.2) vs house (893,71): ~3px (PASS).
"""
from PIL import Image
import numpy as np, json

IM = '/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_041.jpg'
im = np.asarray(Image.open(IM).convert('RGB')).astype(int)
H, W, _ = im.shape
R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]

SX = lambda fx: 42 + (fx - 58.5) * (919 - 42) / (901 - 58.5)
SY = lambda fy: 45 + (fy - 43.0) * (540 - 45) / (517.0 - 43.0)
def sl(bb):
    x0, y0, x1, y1 = bb
    return [round(SX(x0), 1), round(SY(y0), 1), round(SX(x1), 1), round(SY(y1), 1)]

# ---- masks (loose cores, JPEG-tolerant)
peach  = (R > 235) & (G > 195) & (G < 248) & (B > 175) & (B < 235)          # FCE3D0
navy   = (R < 80) & (G < 80) & (B > 95)                                     # 00008B-family
green  = (R < 90) & (G > 85) & (G < 175) & (B < 110) & (G - B > 30)         # 007A3D
lcyan  = (R > 185) & (R < 240) & (G > 225) & (B > 230)                      # D4F4F7
lgreen = (R > 185) & (R < 240) & (G > 225) & (B > 185) & (B < 235) & (G - B > 12)  # D8F5D8
redink = (R > 120) & (G < 95) & (B < 95)
white  = (R > 225) & (G > 225) & (B > 225)
dark   = (R < 120) & (G < 120) & (B < 150)

def bbox(mask, x0, y0, x1, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if len(xs) == 0:
        return None
    return [x0 + xs.min(), y0 + ys.min(), x0 + xs.max(), y0 + ys.max(), int(len(xs))]

def show(name, bb_frame, extra=''):
    if bb_frame is None:
        print(name, 'EMPTY'); return
    f = bb_frame[:4]
    print('%-12s frame[%d,%d -> %d,%d] npx=%-6d slide[%s] %s' % (
        name, f[0], f[1], f[2], f[3], bb_frame[4], ','.join(str(v) for v in sl(f)), extra))

print('=== fit check: badge ->', sl([875.5 - 0.5, 71 - 0.5, 875.5 + 0.5, 71 + 0.5]))

# ---- TITLE red text (frame band y 60..110, x 200..760)
show('title_red', bbox(redink, 200, 60, 760, 112))

# ---- ROOT peach box (frame band y 110..180, x 300..640)
rb = bbox(peach, 300, 110, 640, 185)
show('root_box', rb)
# red text inside root
show('root_text', bbox(redink, rb[0] + 3, rb[1] + 3, rb[2] - 3, rb[3] - 3))

# ---- LEFT parent navy box (frame band y 200..290, x 100..380)
nb = bbox(navy, 100, 195, 380, 295)
show('blue_box', nb)
show('blue_txtW', bbox(white, nb[0] + 3, nb[1] + 3, nb[2] - 3, nb[3] - 3))

# ---- RIGHT parent green box (frame band y 200..290, x 540..820)
gb = bbox(green, 540, 195, 820, 295)
show('green_box', gb)
show('grn_txtW', bbox(white, gb[0] + 3, gb[1] + 3, gb[2] - 3, gb[3] - 3))

# ---- CYAN stack: 4 boxes in frame band y 285..500, x 230..520
cyan_band = lcyan.copy()
cyan_band[:280, :] = False
# row profile to split boxes
rowhas = cyan_band[:, 260:500].sum(axis=1)
runs = []
inrun = False
for y in range(280, 510):
    if rowhas[y] > 30 and not inrun:
        inrun, y0 = True, y
    elif rowhas[y] <= 30 and inrun:
        inrun = False
        runs.append((y0, y - 1))
if inrun:
    runs.append((y0, 509))
print('cyan box row runs:', runs)
for i, (y0, y1) in enumerate(runs):
    cb = bbox(lcyan, 230, y0, 520, y1 + 1)
    show('cyan%d_box' % (i + 1), cb)
    tb = bbox(navy, cb[0] + 3, cb[1] + 3, cb[2] - 3, cb[3] - 3)
    show('cyan%d_txt' % (i + 1), tb)

# ---- GREEN leaf (frame band y 310..380, x 520..830)
gl = bbox(lgreen, 520, 300, 830, 390)
show('grnleaf_box', gl)
# dark green text: greenish dark text on light green — reuse navy? no. text is dark green 1A7A1A
dkg = (R < 110) & (G > 70) & (G < 165) & (B < 110)
show('grnleaf_txt', bbox(dkg, gl[0] + 3, gl[1] + 3, gl[2] - 3, gl[3] - 3))

# ---- connectors (red)
# arrows from root bottom: band y 175..215 full width
show('conn_top', bbox(redink, 100, 178, 860, 215))
# left spine: x 200..270, y 270..500
show('conn_spine', bbox(redink, 200, 270, 272, 500))
# right vertical arrow: x 640..710, y 270..330
show('conn_right', bbox(redink, 640, 270, 712, 335))
