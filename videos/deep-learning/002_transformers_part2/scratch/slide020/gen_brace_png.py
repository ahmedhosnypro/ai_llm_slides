#!/usr/bin/env python3
"""Generate the slide-020 underbrace as a transparent 600dpi PNG (certified
mechanism: raster -> pptxgenjs addImage at exact size w=px/600 in).

Shape measured from the original frame (rows 400-421, x 176-863):
  spine y~411-413.5 full width, arms curling UP at both ends (to y~400),
  central cusp pointing DOWN (apex ~x519.5, y421), spine gap at the cusp.
Target ink box: 714.6 x 21.9 pt -> 5955 x 183 px @600dpi.
"""
from PIL import Image, ImageDraw
import math

W_PT, H_PT = 714.6, 21.9
DPI = 600
W = round(W_PT / 72 * DPI)   # 5955
H = round(H_PT / 72 * DPI)   # 183
S = DPI / 72.0               # pt -> px scale (8.333)

# frame-geometry -> brace-local pt (origin at frame (176,400), 1 frame px = 1.0403 slide pt)
def fx2pt(fx): return (fx - 176) * (714.6 / 687.0)   # frame 176..863 -> 0..714.6
def fy2pt(fy): return (fy - 400) * (21.9 / 21.0)     # frame 400..421 -> 0..21.9

img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
RED = (192, 0, 0, 255)
SW = max(2, round(2.6 * S))  # spine stroke ~2.6pt

# spine (leave the cusp gap 509..530 frame)
y_sp = fy2pt(412.2) * S
x_a, x_b = fx2pt(189) * S, fx2pt(509) * S
x_c, x_d = fx2pt(530) * S, fx2pt(850) * S
d.line([(x_a, y_sp), (x_b, y_sp)], fill=RED, width=SW)
d.line([(x_c, y_sp), (x_d, y_sp)], fill=RED, width=SW)

# left arm: quarter-arc curling up from the spine end to the left edge
# original arm ink: x 176..197, y 400..411.5 (frame)
arm_r = (197 - 176) * (714.6 / 687.0) * S
arm_h = (411.5 - 400) * (21.9 / 21.0) * S
d.arc([fx2pt(176) * S - 26, y_sp - arm_h, fx2pt(197) * S - 26, y_sp + arm_h], start=180, end=270, fill=RED, width=SW)
# right arm mirrored (frame 840..863)
d.arc([fx2pt(840) * S + 26, y_sp - arm_h, fx2pt(863) * S + 26, y_sp + arm_h], start=270, end=360, fill=RED, width=SW)

# central cusp: V from (509,412) down to apex (519.5,421) up to (530,412)
cx_apex = fx2pt(519.5) * S
y_apex = fy2pt(421) * S
d.line([(x_b, y_sp), (cx_apex, y_apex)], fill=RED, width=SW)
d.line([(cx_apex, y_apex), (x_c, y_sp)], fill=RED, width=SW)

img.save("/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/recreated_pptx/build/assets/brace_020.png")
print("saved", img.size)
