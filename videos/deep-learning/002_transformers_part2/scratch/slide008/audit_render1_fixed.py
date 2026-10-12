#!/usr/bin/env python3
"""CORRECTED render audit: frame px -> slide px -> render px composite mapping.
frame->slide: sx=(fx-17.628)/0.961232, sy=fy/0.955556; slide->render: *150/72."""
import numpy as np
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/qa/slide008/render_1.png"
F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_008.jpg"
ren = np.asarray(Image.open(R).convert("RGB")).astype(int)
frm = np.asarray(Image.open(F).convert("RGB")).astype(int)
SC = 150 / 72.0  # slide pt -> render px

def f2r(fx, fy):
    sx = (fx - 17.628) / 0.961232
    sy = fy / 0.955556
    return int(sx * SC), int(sy * SC)

def rpx(fx, fy):
    x, y = f2r(fx, fy)
    return ren[y, x]

# 1) circle coverage: does their tint cover the frame's tinted points?
tint_pts = [(262, 415), (350, 400), (306, 380), (270, 440), (300, 470), (330, 300)]
print("circle tint (render vs frame):")
for fx, fy in tint_pts:
    print(f"  frame({fx},{fy}): render {tuple(rpx(fx, fy))}  frame {tuple(frm[fy, fx])}")

# 2) tint bbox in render: find (181,182,212)-ish pixels
m = (abs(ren[:, :, 0] - 181) < 12) & (abs(ren[:, :, 1] - 182) < 12) & (abs(ren[:, :, 2] - 212) < 14)
ys, xs = np.where(m)
if len(xs):
    print("tint px:", len(xs), "render bbox x", xs.min(), "..", xs.max(), " y", ys.min(), "..", ys.max())
    print("  -> slide bbox x", xs.min() / SC, "..", xs.max() / SC, " y", ys.min() / SC, "..", ys.max() / SC)

# 3) highlight region: frame magenta band (281..337, 469..483) -> what did they draw there?
print("highlight band samples (render vs frame):")
for fx, fy in [(290, 475), (300, 477), (320, 475), (335, 472), (285, 480)]:
    print(f"  frame({fx},{fy}): render {tuple(rpx(fx, fy))}  frame {tuple(frm[fy, fx])}")

# 4) q2 label: frame ink (284..300, 389..405) region -> render ink?
sub_x0, sub_x1, sub_y0, sub_y1 = f2r(276, 380) + (f2r(315, 412)[0], f2r(315, 412)[1])
x0, y0 = f2r(276, 380); x1, y1 = f2r(315, 412)
sub = ren[y0:y1, x0:x1]
m2 = (sub[:, :, 0] > 100) & (sub[:, :, 0] - sub[:, :, 1] > 45) & (sub[:, :, 1] < 110)
ys2, xs2 = np.where(m2)
if len(xs2):
    print(f"q2 red ink in render: n={len(xs2)} render x {x0+xs2.min()}..{x0+xs2.max()} y {y0+ys2.min()}..{y0+ys2.max()}")
    print(f"  -> frame-px x {(x0+xs2.min())/SC*0.961232+17.628:.0f}..{(x0+xs2.max())/SC*0.961232+17.628:.0f} y {(y0+ys2.min())/SC*0.955556:.0f}..{(y0+ys2.max())/SC*0.955556:.0f}")
else:
    print("q2: no red ink found in their render window")

# 5) node rows at TRUE centerlines: red at both sides? (render side)
for i, (cx, cy) in enumerate([(532, 246), (563, 288), (592, 328), (622, 372)]):
    fx, fy = cx * 0.961232 + 17.628, cy * 0.955556
    rx, ry = f2r(fx, fy)
    row = ren[ry, rx - 60:rx + 60]
    reds = [j - 60 for j in range(120) if row[j][0] > 140 and row[j][0] - row[j][1] > 50 and row[j][0] - row[j][2] > 40]
    print(f"node{i+1} slide({cx},{cy}): red offsets(render px) from center: {reds[:14]}...")

# 6) W-box fills at corrected points (interior, avoiding text): frame (185,247) etc.
print("W-box fills (render vs frame):")
for fx, fy, nm in [(185, 230, "W_k r1 top"), (185, 248, "W_k r1 bot"), (185, 290, "W_k r2"),
                   (715, 232, "W_v r1"), (715, 290, "W_v r2")]:
    print(f"  {nm} frame({fx},{fy}): render {tuple(rpx(fx, fy))}  frame {tuple(frm[fy, fx])}")

# 7) K.q correct-position check (their render): red text ink near slide (347..370, 199..212)
x0, y0 = f2r(345, 188); x1, y1 = f2r(380, 212)
sub = ren[y0:y1, x0:x1]
m3 = (sub[:, :, 0] > 120) & (sub[:, :, 0] - sub[:, :, 1] > 50) & (sub[:, :, 0] - sub[:, :, 2] > 40)
ys3, xs3 = np.where(m3)
if len(xs3):
    fx0 = (x0 + xs3.min()) / SC * 0.961232 + 17.628; fx1 = (x0 + xs3.max()) / SC * 0.961232 + 17.628
    fy0 = (y0 + ys3.min()) / SC * 0.955556; fy1 = (y0 + ys3.max()) / SC * 0.955556
    print(f"their K.q ink -> frame x {fx0:.0f}..{fx1:.0f} y {fy0:.0f}..{fy1:.0f} (frame truth: 352..373, 192..203)")
