#!/usr/bin/env python3
"""Final census: exact fill colors per region + text band bboxes for remaining labels."""
from PIL import Image
import numpy as np
from collections import Counter

F = "/home/ahmed/Projects/ai_llm_slides/videos/deep-learning/002_transformers_part2/unique_slides/slide_026.jpg"
img = Image.open(F).convert("RGB")
a = np.asarray(img).astype(int)

def census(x0, x1, y0, y1, label, drop_edge=3):
    reg = a[y0 + drop_edge:y1 - drop_edge, x0 + drop_edge:x1 - drop_edge].reshape(-1, 3)
    cnt = Counter(map(tuple, reg))
    top = cnt.most_common(4)
    s = " | ".join(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}x{int(n / (len(reg) / 100))}%" for c, n in top)
    print(f"{label:34s} {s}")

census(240, 370, 245, 280, "blue_box_fill")
census(240, 315, 256, 280, "sub1_fill")
census(240, 315, 310, 332, "sub2_fill")
census(240, 315, 362, 384, "sub3_fill")
census(410, 655, 195, 215, "container_fill_top")
census(468, 540, 250, 277, "dual_adc_pentagon")
census(548, 575, 255, 272, "amp_tri_top")
census(465, 580, 224, 240, "whitebox16_fill")
census(475, 545, 300, 335, "amp_tri_mid+around")
census(462, 596, 352, 398, "comparators_box")
census(474, 512, 362, 390, "comp_triangle")
census(465, 522, 420, 452, "power_supplies")
census(397, 413, 425, 440, "box24V")
census(397, 410, 260, 380, "host_bar")
census(651, 664, 285, 370, "enc_conn_bar")
census(695, 828, 250, 277, "diff_box")
census(745, 795, 402, 423, "sincos_box")
census(690, 852, 195, 460, "right_rect_fill")
census(760, 800, 365, 393, "motor_body")
# container dashed border color: pixels on left border column band
reg = a[195:245, 401:405].reshape(-1, 3)
cnt = Counter(map(tuple, reg))
print("cont_border_left:", " | ".join(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}x{n}" for c, n in cnt.most_common(5)))
# right rect border
reg = a[300:340, 686:690].reshape(-1, 3)
cnt = Counter(map(tuple, reg))
print("rr_border:", " | ".join(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}x{n}" for c, n in cnt.most_common(5)))
# 16bit dashed group border color
reg = a[283:288, 465:595].reshape(-1, 3)
dk = [tuple(c) for c in reg if sum(c) < 480]
cnt = Counter(dk)
print("dash16_border:", " | ".join(f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}x{n}" for c, n in cnt.most_common(5)))

# text bands: dark-ink column profile helper
r, g, b = a[..., 0], a[..., 1], a[..., 2]
def band(y0, y1, x0, x1, label, thr=380):
    m = (r + g + b) < thr
    ys, xs = np.nonzero(m[y0:y1, x0:x1])
    if len(xs) == 0:
        print(f"{label:38s} EMPTY")
        return
    print(f"{label:38s} x {x0 + xs.min()}..{x0 + xs.max()}  y {y0 + ys.min()}..{y0 + ys.max()}  n={len(xs)}")

band(495, 514, 250, 800, "caption_L2")
band(478, 492, 250, 800, "caption_L1")
band(315, 345, 350, 430, "pos_label_l1(l?)")   # Position/(Angle) rows
band(296, 345, 130, 230, "pos_block_all", 430)
band(425, 445, 355, 400, "24V_text")
band(428, 444, 545, 600, "5V_label")
band(443, 458, 545, 600, "3.3V_label")
band(448, 462, 560, 700, "enc_supply_note")
band(398, 415, 780, 865, "AC_motor_label")
band(322, 358, 735, 855, "shielded_note")
band(248, 282, 690, 840, "diff_box_text")
band(400, 424, 740, 800, "sincos_box_text")
band(190, 212, 570, 660, "tida_tag_text")
band(252, 282, 362, 398, "spi+icon")
band(310, 340, 362, 398, "12bit_adc")
band(370, 388, 362, 398, "eqep")
band(246, 280, 585, 660, "out_label_top")
band(320, 365, 580, 660, "out_label_mid_R")
band(378, 400, 520, 600, "comparators_text")
band(452, 462, 520, 700, "enc_supply_note2")
# title/subtitle precise
band(58, 78, 300, 650, "title_ink")
band(80, 102, 180, 760, "subtitle_ink")
