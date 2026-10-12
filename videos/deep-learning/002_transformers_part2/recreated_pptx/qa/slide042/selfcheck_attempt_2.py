#!/usr/bin/env python3
"""Self-check attempt 2 (correct 150dpi mapping: 1 render px = 0.48pt; 2.08333 px/pt).
frame->render: rx = (fx-18.66)/0.96055 * 150/72 ; ry = fy/0.95556 * 150/72."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide042/render_1.png"
im = Image.open(R).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"render {W}x{H}")
K = 150 / 72
def rx(fx): return (fx - 18.66) / 0.96055 * K
def ry(fy): return fy / 0.95556 * K

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 130) & (r - g > 60) & (r - b > 60)
blue = (b > 110) & (b - r > 40) & (b - g > 20)
green = (g > 120) & (g - r > 40) & (g - b > 60)
mag = (r > 110) & (b > 110) & (g < 110)
yel = (r > 200) & (g > 200) & (b < 145)
issues = []

def bbox(mask, x0, y0, x1, y1):
    m = np.zeros_like(mask); m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(m)
    if len(xs) == 0: return None
    return xs.min(), ys.min(), xs.max(), ys.max()

def check(name, got, want, tol=7):
    if got is None:
        print(f"  FAIL {name}: NO INK"); issues.append(f"{name}: no ink"); return
    d = tuple(got[i] - want[i] for i in range(4))
    ok = max(abs(v) for v in d) <= tol
    print(f"  {'ok  ' if ok else 'FAIL'} {name}: d={d} got({got[0]},{got[1]})..({got[2]},{got[3]}) want({want[0]},{want[1]})..({want[2]},{want[3]})")
    if not ok: issues.append(f"{name}: d={d}")

# TITLE: frame ink x204..779, y72..111
check("title", bbox(red, int(rx(150)), int(ry(60)), int(rx(850)), int(ry(133))), (round(rx(204)), round(ry(72)), round(rx(779)), round(ry(111))), tol=9)
# BLUE frame: frame x68..891, y133..512
check("blue-frame", bbox(blue, 0, int(ry(126)), W, H), (round(rx(68)), round(ry(133)), round(rx(891)), round(ry(512))), tol=8)
# diagrams
check("left-stack", bbox(green, round(rx(140)), round(ry(250)), round(rx(240)), round(ry(440))),
      (round(rx(168)), round(ry(262)), round(rx(211)), round(ry(429))), tol=8)
check("mid-grid", bbox(green, round(rx(350)), round(ry(245)), round(rx(535)), round(ry(430))),
      (round(rx(379)), round(ry(254)), round(rx(518)), round(ry(419))), tol=8)
check("right-magenta", bbox(mag, round(rx(600)), round(ry(220)), round(rx(880)), round(ry(490))),
      (round(rx(652)), round(ry(303)), round(rx(792)), round(ry(470))), tol=10)
check("right-yellow", bbox(yel, round(rx(600)), round(ry(220)), round(rx(880)), round(ry(490))),
      (round(rx(710)), round(ry(250)), round(rx(852)), round(ry(435))), tol=14)
# arrows
check("vertical-arrow", bbox(red, round(rx(630)), round(ry(318)), round(rx(658)), round(ry(478))),
      (round(rx(640)), round(ry(325)), round(rx(646)), round(ry(467))), tol=12)
check("horizontal-arrow", bbox(red, round(rx(630)), round(ry(450)), round(rx(880)), round(ry(474))),
      (round(rx(646)), round(ry(455)), round(rx(868)), round(ry(468))), tol=14)
check("diagonal-arrow", bbox(red, round(rx(795)), round(ry(392)), round(rx(880)), round(ry(478))),
      (round(rx(812)), round(ry(402)), round(rx(868)), round(ry(466))), tol=18)

# label-box borders: horizontal red runs at expected frame rows
def row_run(y, x0, x1):
    for dy in (-3, -2, -1, 0, 1, 2, 3):
        yy = int(ry(y)) + dy
        xs = np.nonzero(red[yy, int(rx(x0)) - 4:int(rx(x1)) + 4])[0]
        if len(xs) and xs.max() - xs.min() > 0.75 * (rx(x1) - rx(x0)):
            return True
    return False
for name, (fy, fx0, fx1) in dict(Lbox_top=(195, 77, 330), Mbox_top=(193, 341, 598),
                                 Rbox_top=(165, 627, 882), Lbox_bot=(236, 77, 330),
                                 Mbox_bot=(235, 341, 598), Rbox_bot=(227, 627, 882)).items():
    ok = row_run(fy, fx0, fx1)
    print(f"  {'ok  ' if ok else 'FAIL'} {name} border")
    if not ok: issues.append(f"{name}: border missing")

# label text ink presence (slide-space boxes)
def ink_in(x0, y0, x1, y1, mask):
    return int(mask[int(y0 * K):int(y1 * K), int(x0 * K):int(x1 * K)].sum())
checks_ink = [
    ("Lbox-line1-red", (100, 205, 240, 220), red), ("Lbox-green-OneInput", (210, 205, 290, 222), green),
    ("Mbox-line1", (345, 205, 470, 220), red), ("Mbox-blue-L2", (355, 218, 465, 240), blue),
    ("Mbox-magenta-L2", (478, 218, 580, 240), mag),
    ("Rbox-line1", (640, 175, 770, 192), red), ("Rbox-green-L2", (640, 192, 780, 210), green),
    ("Rbox-magenta-miniBatch", (782, 190, 880, 212), mag), ("Rbox-blue-L3", (640, 208, 735, 228), blue),
    ("FeatureVector-label", (615, 360, 665, 460), red), ("Channels-label", (660, 485, 760, 515), red),
    ("BatchSize-label", (820, 415, 900, 465), red),
]
for name, (x0, y0, x1, y1), m in checks_ink:
    n = ink_in(x0, y0, x1, y1, m)
    ok = n > 60
    print(f"  {'ok  ' if ok else 'FAIL'} {name}: ink px {n}")
    if not ok: issues.append(f"{name}: ink {n}")

# containment: no red/green/magenta ink outside blue frame sides
band = slice(int(ry(145)), int(ry(500)))
lft = int(red[band, int(rx(45)):int(rx(50))].sum() + green[band, int(rx(45)):int(rx(50))].sum() + mag[band, int(rx(45)):int(rx(50))].sum())
rgt = int(red[band, int(rx(913)):int(rx(918))].sum() + green[band, int(rx(913)):int(rx(918))].sum() + mag[band, int(rx(913)):int(rx(918))].sum())
print(f"  containment: outside-left {lft}, outside-right {rgt} px")
if lft > 60 or rgt > 60: issues.append(f"containment outside frame: L{lft} R{rgt}")

print()
print("ISSUES:" if issues else "ALL SELF-CHECKS PASSED")
for i in issues: print(" -", i)
