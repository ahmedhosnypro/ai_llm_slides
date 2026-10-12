from PIL import Image
import numpy as np

F = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_017.jpg").convert("RGB")
R = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png").convert("RGB")
a = np.asarray(F).astype(int)   # 540x960
b = np.asarray(R).astype(int)   # 1125x2001
FH, FW = a.shape[:2]
RH, RW = b.shape[:2]

# my fitted mapping: frame = a + s*slide
AX, SX = 17.6, 0.9613
AY, SY = -0.14, 0.9586
KX = RW / 960.0   # render px per slide pt (x)
KY = RH / 540.0

# for each frame pixel -> slide -> render px
fy, fx = np.mgrid[0:FH, 0:FW]
sx = (fx - AX) / SX
sy = (fy - AY) / SY
rx = np.clip((sx * KX).astype(int), 0, RW-1)
ry = np.clip((sy * KY).astype(int), 0, RH-1)

d = np.abs(a - b[ry, rx]).sum(axis=2)
# exclude below-slide letterbox rows (frame rows where sy>540)
valid = sy <= 539.0
dm = np.where(valid, d, 0)

# hotspot grid 32 cols x 18 rows (30x30 frame px cells)
GH, GW = 18, 32
cell = np.zeros((GH, GW), dtype=int)
for gy in range(GH):
    for gx in range(GW):
        blk = dm[gy*30:(gy+1)*30, gx*30:(gx+1)*30]
        cell[gy, gx] = (blk > 120).sum()   # strong-diff pixel count
np.set_printoptions(linewidth=250)
print("strong-diff pixel counts per 30x30 cell (rows=y frame /30, cols=x/30):")
print("    " + "".join("%4d" % (gx*30) for gx in range(GW)))
for gy in range(GH):
    print("%3d" % (gy*30) + "".join("%4d" % cell[gy, gx] for gx in range(GW)))
tot = (dm > 120).sum()
print("total strong-diff px:", tot, "of", valid.sum())
