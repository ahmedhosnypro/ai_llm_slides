#!/usr/bin/env python3
"""Resume-verification probe for slide 017 (002) vs parent 001:43 certified render.

1. Re-verify the frame->slide mapping on four chrome landmarks.
2. Scan the ff_left / ff_right delta columns row-by-row in BOTH images at slide
   coords, printing color runs so geometry deltas are checkable numerically.
Mapping (banked fit): fx = 18.25 + 0.96150*sx ; fy = 1.95 + 0.95500*sy
"""
from PIL import Image
import numpy as np

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
F = np.asarray(Image.open(f"{VID}/unique_slides/slide_017.jpg").convert("RGB")).astype(np.int16)
R = np.asarray(Image.open(
    "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/001_transformers_part1/recreated_pptx/qa/slide043/render_2.png"
).convert("RGB").resize((960, 540), Image.LANCZOS)).astype(np.int16)

AX, SX, AY, SY = 18.250, 0.96150, 1.950, 0.95500

def frame_win(sx0, sy0, sx1, sy1):
    x0, y0 = int(round(AX + SX * sx0)), int(round(AY + SY * sy0))
    x1, y1 = int(round(AX + SX * sx1)), int(round(AY + SY * sy1))
    return F[y0:y1, x0:x1]

def hexc(px):
    return "%02X%02X%02X" % tuple(int(v) for v in px)

def runs(img, row, x0, x1, tol=28):
    """Collapse a row into color runs."""
    out = []
    cur = None
    for x in range(x0, min(x1, img.shape[1])):
        c = tuple(img[row, x])
        if cur and abs(c[0]-cur[1][0]) + abs(c[1]-cur[1][1]) + abs(c[2]-cur[1][2]) <= tol:
            cur[2] = x
        else:
            if cur and cur[2] - cur[0] >= 1:
                out.append((cur[0], cur[2], hexc(cur[1])))
            cur = [x, c, x]
    if cur:
        out.append((cur[0], cur[2], hexc(cur[1])))
    # merge tiny runs into neighbours for readability: keep only runs >=2 px
    return [r for r in out if r[1] - r[0] >= 1]

print("== 1. chrome landmark re-verification ==")
# left border: parent panel left edge is slide x=42 (red border) -> frame x = 18.25+0.9615*42 = 58.6
col = F[:, 40:120]
red = np.abs(col - np.array([192, 0, 0])).sum(axis=2) < 150
rows = red.sum(axis=1)
first_red_rows = [int(r) for r in np.where(rows > 20)[0][:3]] if rows.any() else []
print("  frame left-border red rows begin at frame y:", first_red_rows, "(predict fy(45)=%.1f -> ~45)" % (AY + SY * 45))
xs = np.where(red[300 - int(AY)])[0] + 40
print("  frame left border x at fy(300)=%d: %s (predict %.1f)" % (int(AY + SY * 300), xs[:3].tolist(), AX + SX * 42))
# panel top: slide y=45 -> frame y=44.9 ; scan column x=400 for gray panel start
colv = F[:, 400]
gray = np.abs(colv - np.array([233, 233, 231])).sum(axis=1) < 30
tops = np.where(gray)[0]
print("  frame panel-top gray at frame y:", tops[:3].tolist() if len(tops) else "none", "(predict %.1f)" % (AY + SY * 45))
# badge center: slide (893,71) -> frame (876.3, 69.7). Find purple ring pixels near there.
bx, by = int(AX + SX * 893), int(AY + SY * 71)
win = F[by - 25:by + 25, bx - 25:bx + 25]
pur = np.abs(win - np.array([106, 90, 205])).sum(axis=2) < 160
ys2, xs2 = np.where(pur)
if len(xs2):
    print("  badge purple-ring bbox in frame: x %d..%d y %d..%d (center %.1f,%.1f; predict %.1f,%.1f)" % (
        xs2.min() + bx - 25, xs2.max() + bx - 25, ys2.min() + by - 25, ys2.max() + by - 25,
        (xs2.min() + xs2.max()) / 2 + bx - 25, (ys2.min() + ys2.max()) / 2 + by - 25, bx, by))
else:
    print("  badge purple ring NOT found near predicted center")
# bottom stroke: slide y=538.5 -> frame y=516
print("  frame bottom stroke predict fy(538.5)=%.1f; frame row 516 grayish?" % (AY + SY * 538.5))
print("   frame px(516,480):", hexc(F[516, 480]), " frame px(518,480):", hexc(F[518, 480]))

print()
print("== 2. ff_left rows (slide y = 335/363/391/419), x 88..200 ==")
for sy in (335, 363, 391, 419):
    fy = int(round(AY + SY * sy))
    fr = runs(F, fy, 88, 205)
    pr = runs(R, sy, 88, 205)
    print(f" frame y{fy} (slide {sy}):", [(a, b, h) for a, b, h in fr])
    print(f" parent    {sy}:", [(a, b, h) for a, b, h in pr])
    print()

print("== 2b. ff_right rows, x 425..615 ==")
for sy in (335, 363, 391, 419):
    fy = int(round(AY + SY * sy))
    fr = runs(F, fy, 425, 615)
    pr = runs(R, sy, 425, 615)
    print(f" frame y{fy} (slide {sy}):", [(a, b, h) for a, b, h in fr])
    print(f" parent    {sy}:", [(a, b, h) for a, b, h in pr])
    print()

print("== 2c. gold panel vertical extent (slide x=140 and x=520 columns) ==")
for sx in (140, 520):
    fx = int(round(AX + SX * sx))
    colr = F[:, fx]
    ys = [y for y in range(250, 500) if abs(colr[y][0]-213)+abs(colr[y][1]-196)+abs(colr[y][2]-77) < 210]
    print(f" frame gold-ish rows at fx({sx})={fx}: {min(ys) if ys else '-'}..{max(ys) if ys else '-'} n={len(ys)}")

print("== 2d. arrowheads right of W_v boxes? slide x 534..558, rows 331..423 ==")
for sy in (335, 363, 391, 419):
    fy = int(round(AY + SY * sy))
    fr = runs(F, fy, 530, 562)
    pr = runs(R, sy, 530, 562)
    print(f" frame y{fy}:", [(a, b, h) for a, b, h in fr])
    print(f" parent    {sy}:", [(a, b, h) for a, b, h in pr])
