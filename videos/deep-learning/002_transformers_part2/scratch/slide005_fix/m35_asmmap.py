# m35_asmmap.py — color-class ASCII maps of the h-assembly region:
# original frame vs render_4 (current build state), same frame coordinates.
from PIL import Image
import sys

VID = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2"
FR = Image.open(VID + "/unique_slides/slide_005.jpg").convert("RGB")
RD = Image.open(VID + "/recreated_pptx/qa/slide005/render_4.png").convert("RGB")
SX, SY = 2.16770, 2.17684  # frame px -> render px

def classify(r, g, b):
    L = 0.299 * r + 0.587 * g + 0.114 * b
    if L < 90:
        return "D"                      # dark ink (black curve, dark text, dark border)
    if r > 150 and g < 125 and (r - g) > 55 and (r - b) > 55:
        return "P"                      # red/pink stroke (C00000 / C47070)
    if r > 185 and 140 < g < 215 and 90 < b < 200 and (r - b) > 25:
        return "T"                      # tan fill (D4BCA0 family) / brown head blend
    if 140 < L < 215 and abs(r - g) < 16 and abs(g - b) < 16:
        return "G"                      # gray (ghost ring, shadow border, faint stroke)
    return "."

X0, X1, Y0, Y1 = 442, 516, 322, 392   # frame window

def frame_map(img, step):
    px = img.load()
    out = []
    for fy in range(Y0, Y1, step):
        row = []
        for fx in range(X0, X1, step):
            row.append(classify(*px[fx, fy]))
        out.append("".join(row))
    return out

def render_map(step):
    px = RD.load()
    out = []
    for fy in range(Y0, Y1, step):
        row = []
        for fx in range(X0, X1, step):
            rx = round((fx - 18.0787) * SX)
            ry = round((fy - 0.4700) * SY)
            row.append(classify(*px[rx, ry]))
        out.append("".join(row))
    return out

step = 1 if len(sys.argv) < 2 else int(sys.argv[1])
hdr = "     " + "".join(str((X0 + i) // 10 % 10) if (X0 + i) % 10 == 0 else " " for i in range(0, X1 - X0, step))
o = frame_map(FR, step)
r = render_map(step)
print("ORIGINAL FRAME (frame px, cols are x, rows are y):")
print(hdr)
for i, line in enumerate(o):
    print(f"{Y0 + i * step:4d} {line}")
print()
print("RENDER_4 (same frame coordinates):")
print(hdr)
for i, line in enumerate(r):
    print(f"{Y0 + i * step:4d} {line}")
