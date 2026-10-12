#!/usr/bin/env python3
"""Self-check attempt 1 for slide 042 (closed-loop PIL vs mapped frame targets).
Render: 2001x1125 @150dpi (1 px = 0.36 pt). frame->render: rx = (fx-18.66)/0.96055*200/72,
ry = fy/0.95556*200/72."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide042/render_1.png"
im = Image.open(R).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(int)
print(f"render {W}x{H}")

SX, SY = 200 / 72 / 0.96055, 200 / 72 / 0.95556   # frame px -> render px
def rx(fx): return (fx - 18.66) * SX
def ry(fy): return fy * SY

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (r > 130) & (r - g > 60) & (r - b > 60)
blue = (b > 110) & (b - r > 40) & (b - g > 20)
green = (g > 120) & (g - r > 40) & (g - b > 60)
issues = []

def bbox(mask, x0, y0, x1, y1):
    m = np.zeros_like(mask); m[y0:y1, x0:x1] = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(m)
    if len(xs) == 0: return None
    return xs.min(), ys.min(), xs.max(), ys.max()

def check(name, got, want, tol=6):
    if got is None:
        print(f"  FAIL {name}: NO INK"); issues.append(f"{name}: no ink"); return
    dx0, dy0 = got[0] - want[0], got[1] - want[1]
    dx1, dy1 = got[2] - want[2], got[3] - want[3]
    ok = max(abs(dx0), abs(dy0), abs(dx1), abs(dy1)) <= tol
    print(f"  {'ok  ' if ok else 'FAIL'} {name}: got({got[0]},{got[1]})..({got[2]},{got[3]}) want({want[0]},{want[1]})..({want[2]},{want[3]}) d=({dx0},{dy0},{dx1},{dy1})")
    if not ok: issues.append(f"{name}: d=({dx0},{dy0},{dx1},{dy1})")

# 1. TITLE: target frame ink x204..779 y72..111
t = bbox(red, 0, 0, W, int(ry(133)))
check("title", t, (round(rx(204)), round(ry(72)), round(rx(779)), round(ry(111))), tol=8)

# 2. BLUE frame: target frame x69..889.5 y134.5..510
t = bbox(blue, 0, int(ry(130)), W, H)
check("blue-frame", t, (round(rx(68)), round(ry(133)), round(rx(891)), round(ry(512))), tol=8)

# 3. label box borders: red thin rects — scan for horizontal runs in label band
# left box top border: frame y195 -> render ry(195); expect a red run near x rx(77)..rx(330)
def row_run(y, x0, x1, mask):
    xs = np.nonzero(mask[y, x0:x1])[0]
    return (x0 + xs.min(), x0 + xs.max()) if len(xs) else None
for name, (fy, fx0, fx1) in dict(Lbox_top=(195, 77, 330), Mbox_top=(193, 341, 598),
                                 Rbox_top=(165, 627, 882), Lbox_bot=(236, 77, 330),
                                 Mbox_bot=(235, 341, 598), Rbox_bot=(227, 627, 882)).items():
    y = round(ry(fy))
    got = None
    for dy in (-3, -2, -1, 0, 1, 2, 3):
        rr = row_run(y + dy, round(rx(fx0)) - 4, round(rx(fx1)) + 4, red)
        if rr and rr[1] - rr[0] > 0.7 * (rx(fx1) - rx(fx0)):
            got = rr; break
    print(f"  {'ok  ' if got else 'FAIL'} {name}: {got}")
    if not got: issues.append(f"{name}: border run missing")

# 4. diagrams: green ink bboxes
# left stack: frame (168,262)..(211,429); mid: (379,254)..(518,419)
t = bbox(green, round(rx(150)), round(ry(250)), round(rx(240)), round(ry(440)))
check("left-stack", t, (round(rx(168)), round(ry(262)), round(rx(211)), round(ry(429))), tol=8)
t = bbox(green, round(rx(360)), round(ry(245)), round(rx(530)), round(ry(430)))
check("mid-grid", t, (round(rx(379)), round(ry(254)), round(rx(518)), round(ry(419))), tol=8)
# right block: magenta ink
mag = (r > 110) & (b > 110) & (g < 110)
t = bbox(mag, round(rx(600)), round(ry(220)), round(rx(880)), round(ry(490)))
check("right-block-magenta", t, (round(rx(652)), round(ry(302)), round(rx(793)), round(ry(470))), tol=10)
yel = (r > 200) & (g > 200) & (b < 145)
t = bbox(yel, round(rx(600)), round(ry(220)), round(rx(880)), round(ry(490)))
check("right-block-yellow", t, (round(rx(710)), round(ry(250)), round(rx(840)), round(ry(440))), tol=14)

# 5. vertical arrow ink (strict red): target frame x640..646, y325..467
t = bbox(red, round(rx(600)), round(ry(320)), round(rx(660)), round(ry(480)))
check("vertical-arrow", t, (round(rx(640)), round(ry(325)), round(rx(646)), round(ry(467))), tol=10)
# horizontal arrow: frame (641,461)..(820,461) + heads
t = bbox(red, round(rx(655)), round(ry(450)), round(rx(880)), round(ry(478)))
check("horizontal-arrow", t, (round(rx(646)), round(ry(455)), round(rx(868)), round(ry(468))), tol=14)

# 6. containment: no content ink outside the blue frame (x 69..890, y 134..511 frame)
m = np.zeros_like(red)
m[int(ry(513)):, :] = red[int(ry(513)):, :]     # below blue frame bottom
m[:int(ry(133)), 60:] = red[:int(ry(133)), 60:]  # above blue frame (title excluded by x>60? title IS there)
# check only the band below the blue frame and left/right margins
left_band = red[int(ry(140)):int(ry(505)), :int(rx(66))]
right_band = red[int(ry(140)):int(ry(505)), int(rx(893)):]
bot_band = red[int(ry(513)):int(ry(517)), int(rx(70)):int(rx(890))]
print(f"  containment: ink px left-of-frame={int(left_band.sum())}, right-of-frame={int(right_band.sum())}, below-frame={int(bot_band.sum())}")
if left_band.sum() > 40 or right_band.sum() > 40: issues.append("containment: ink outside blue frame sides")

# 7. no letterbox/black band at bottom (render should end with white/gray)
print(f"  bottom rows black frac: {float((a[-6:, 200:1800].sum(axis=2) < 200).mean()):.4f} (expect 0)")

print()
print("ISSUES:" if issues else "ALL SELF-CHECKS PASSED")
for i in issues: print(" -", i)
