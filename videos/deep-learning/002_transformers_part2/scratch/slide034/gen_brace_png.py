#!/usr/bin/env python3
"""gen_brace_png.py — slide-034 red curly brace as a transparent 600dpi PNG
(certified raster mechanism: LO mis-renders rotated leftBrace presets — 020 law).

Shape measured from the original frame (measure9/measure10):
  bbox x 178..870, y 336..351 (frame px). Spine y~343.5 full width, arms curling
  UP at both ends (tips to y336), central cusp pointing DOWN (apex ~(524.5, 351)),
  spine gap at the cusp (solid runs y343: (208,492)+(555,840)).
Target slide-pt box: w = (870-178)/0.962307 = 719.0 pt; h = (351-336)/0.955556 = 15.7 pt
(+ 1.0 pt stroke padding top/bottom in the canvas).
"""
from PIL import Image, ImageDraw

AX, SX = 17.943, 0.962307   # frame->slide-pt mapping (measure1)
SY = 0.955556
X0F, X1F = 178.0, 870.0     # brace frame bbox
Y0F, Y1F = 336.0, 351.0
PAD = 1.0                   # pt stroke padding in canvas

W_PT = (X1F - X0F) / SX     # 719.0
H_PT = (Y1F - Y0F) / SY + 2 * PAD  # 17.7
DPI = 600
W = round(W_PT / 72 * DPI)
H = round(H_PT / 72 * DPI)
S = DPI / 72.0

def xpt(fx): return ((fx - X0F) / SX) * S
def ypt(fy): return ((fy - Y0F) / SY + PAD) * S

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
RED = (138, 36, 54, 255)          # measured core (120,20,40) + JPEG lift -> 8A2436
SW = max(2, round(2.7 * S))       # spine stroke ~2.6 frame px = 2.7 slide pt

# spine (gap at the cusp): left 188..498, right 550..858 at frame y 343.5
y_sp = ypt(343.5)
d.line([(xpt(188), y_sp), (xpt(498), y_sp)], fill=RED, width=SW)
d.line([(xpt(550), y_sp), (xpt(858), y_sp)], fill=RED, width=SW)

# left arm: quarter-arc from west (tip x176) curling up to north, connecting to spine
d.arc([xpt(176), ypt(336.5), xpt(200), ypt(350.5)], start=180, end=270, fill=RED, width=SW)
# right arm mirrored
d.arc([xpt(848), ypt(336.5), xpt(872), ypt(350.5)], start=270, end=360, fill=RED, width=SW)

# central cusp: V from (498,343.5) down to apex (524.5,351) up to (550,343.5)
cx_apex = xpt(524.5)
y_apex = ypt(351.0)
d.line([(xpt(498), y_sp), (cx_apex, y_apex)], fill=RED, width=SW)
d.line([(cx_apex, y_apex), (xpt(550), y_sp)], fill=RED, width=SW)

OUT = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/brace_034.png"
img.save(OUT)
print("saved", img.size, f"W_PT={W_PT:.2f} H_PT={H_PT:.2f} PAD={PAD}")
